#!/usr/bin/env python3
"""Read-only archive audit plus temporary clean restore samples; writes receipts only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def invoke(manifest, archives, output, verify=False):
    command = [sys.executable, "-B", str(Path(__file__).with_name("restore_historical.py")),
               "--manifest", str(manifest), "--archives-dir", str(archives), "--output", str(output)]
    if verify:
        command.append("--verify-only")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifests-dir", required=True, type=Path)
    parser.add_argument("--archives-dir", required=True, type=Path)
    parser.add_argument("--receipt-dir", required=True, type=Path)
    parser.add_argument("--sample", action="append", default=[], help="Manifest filename for an additional clean restore check")
    args = parser.parse_args()
    args.receipt_dir.mkdir(parents=True, exist_ok=True)
    manifests = sorted(args.manifests_dir.glob("*.json"))
    if not manifests:
        parser.error("No JSON manifests found")
    before = {path.name: sha(path) for path in manifests}
    receipt = {"schema_version": 1, "scope": "Local archive verification and temporary byte restoration; no builds, uploads, source edits, or acceptance claims.",
               "tools_sha256": {name: sha(Path(__file__).with_name(name)) for name in ("restore_historical.py", "restore_core.py", "validate_snapshot.py")},
               "packages": [], "samples": [], "errors": []}
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="historical-restore-check-", dir=args.receipt_dir) as temporary:
        workspace = Path(temporary)
        for index, path in enumerate(manifests, 1):
            data = json.loads(path.read_text())
            record = {"manifest": path.name, "manifest_sha256": before[path.name], "archive_name": data["archive_name"],
                      "archive_sha256": data["archive_sha256"], "archive_bytes": data["archive_bytes"], "expected_members": len(data["members"]),
                      "expected_member_bytes": sum(item["size"] for item in data["members"])}
            try:
                record["result"] = invoke(path, args.archives_dir, workspace / "verify-unused", True)
                record["status"] = "passed"
            except Exception as error:
                record["status"] = "failed"
                record["error"] = str(error)
                receipt["errors"].append({"manifest": path.name, "error": str(error)})
            receipt["packages"].append(record)
            if index % 20 == 0 or index == len(manifests):
                print(f"Verified {index}/{len(manifests)} archives; {len(receipt['errors'])} errors", flush=True)
        receipt["verify_only_created_output"] = (workspace / "verify-unused").exists()
        for index, name in enumerate(args.sample):
            if Path(name).name != name or name not in before:
                raise ValueError("Sample must name one audited manifest filename")
            path = args.manifests_dir / name
            data = json.loads(path.read_text())
            record = {"manifest": name}
            try:
                if any(item.get("selection") == "security_hold" for item in data["members"]):
                    raise ValueError("Choose a sample without historical security_hold labels; full read-only verification still covers all members")
                output = workspace / f"sample-{index}"
                record["first_restore"] = invoke(path, args.archives_dir, output)
                root = output / data["extracted_directory"]
                actual = {item.relative_to(root).as_posix(): item for item in root.rglob("*") if item.is_file()}
                expected = {item["path"]: item for item in data["members"]}
                if set(actual) != set(expected):
                    raise ValueError("Restored file set differs from manifest")
                output_hashes = {name: sha(file) for name, file in actual.items()}
                for name, file in actual.items():
                    if output_hashes[name] != expected[name]["sha256"] or file.stat().st_size != expected[name]["size"]:
                        raise ValueError("Independent restored-file fingerprint mismatch")
                mtimes = {name: file.stat().st_mtime_ns for name, file in actual.items()}
                record["second_restore"] = invoke(path, args.archives_dir, output)
                if record["second_restore"]["written"] != 0 or record["second_restore"]["existing"] != len(actual):
                    raise ValueError("Idempotence counts differ")
                if mtimes != {name: file.stat().st_mtime_ns for name, file in actual.items()} or output_hashes != {name: sha(file) for name, file in actual.items()}:
                    raise ValueError("Idempotence changed existing bytes or modification times")
                record["post_restore_verify"] = invoke(path, args.archives_dir, output, True)
                record["independent_sha256"] = output_hashes
                record["idempotent_bytes_and_mtimes"] = True
                record["status"] = "passed"
            except Exception as error:
                record["status"] = "failed"
                record["error"] = str(error)
                receipt["errors"].append({"sample": name, "error": str(error)})
            receipt["samples"].append(record)
            print("Clean restore:", record["manifest"], record["status"], flush=True)
    receipt["manifest_hashes_unchanged"] = before == {path.name: sha(path) for path in manifests}
    receipt["summary"] = {"archives": len(manifests), "passed": sum(row["status"] == "passed" for row in receipt["packages"]),
                          "members": sum(row["expected_members"] for row in receipt["packages"]),
                          "archive_bytes": sum(row["archive_bytes"] for row in receipt["packages"]),
                          "member_bytes": sum(row["expected_member_bytes"] for row in receipt["packages"]),
                          "manifest_security_hold_labels_hashed": sum(row.get("result", {}).get("manifest_security_hold_labels", 0) for row in receipt["packages"]),
                          "errors": len(receipt["errors"])}
    receipt["elapsed_seconds"] = round(time.monotonic() - started, 3)
    (args.receipt_dir / "validation-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt["summary"], indent=2))
    return int(bool(receipt["errors"]) or receipt["verify_only_created_output"] or not receipt["manifest_hashes_unchanged"])


if __name__ == "__main__":
    sys.exit(main())
