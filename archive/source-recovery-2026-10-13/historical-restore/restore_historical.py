#!/usr/bin/env python3
"""Verify and restore a complete original archive from a lean historical manifest."""
import argparse
import json
from pathlib import Path
import sys
import zipfile

# Keep --verify-only free of local bytecode-cache writes, even without python -B.
sys.dont_write_bytecode = True
import restore_core as core


def normalize(manifest):
    """Translate metadata only. Never substitute Git aliases for original paths."""
    if not isinstance(manifest, dict):
        raise core.RestoreError("Historical manifest must be an object")
    name = core.safe_path(manifest.get("archive_name"), "archive name")
    if "/" in name:
        raise core.RestoreError("Archive name must be a filename")
    destination = core.safe_path(manifest.get("extracted_directory"), "extracted directory")
    library = manifest.get("library")
    if not isinstance(library, dict) or not isinstance(library.get("library_file_id"), str) or not library["library_file_id"]:
        raise core.RestoreError("Historical manifest needs its Library identity")
    if library.get("name") != name or library.get("size_bytes") != manifest.get("archive_bytes"):
        raise core.RestoreError("Library metadata disagrees with archive name/size")
    members = manifest.get("members")
    if not isinstance(members, list) or not members:
        raise core.RestoreError("Historical manifest must list every original file")
    files = []
    for item in members:
        if not isinstance(item, dict):
            raise core.RestoreError("Invalid historical member")
        files.append({
            "path": item.get("path"), "size_bytes": item.get("size"),
            "sha256": item.get("sha256"), "git_blob_sha1": item.get("git_blob_sha1"),
            "storage": "library", "reason": item.get("selection", "historical_original"),
        })
        if not isinstance(files[-1]["git_blob_sha1"], str):
            raise core.RestoreError("Historical member needs its Git blob SHA-1")
    result = {
        "schema_version": 1, "package_id": name, "destination": destination,
        "artifact": {"name": name, "sha256": manifest.get("archive_sha256"),
                     "size_bytes": manifest.get("archive_bytes"),
                     "library_file_id": library["library_file_id"], "version_id": library.get("version_id")},
        "nested_archives": [], "files": files, "require_exact_members": True,
    }
    core.read_manifest(result)
    return result


def restore(manifest_path, archives_dir, output, verify_only=False):
    with open(manifest_path, encoding="utf-8") as source:
        historical = json.load(source)
    result = core.restore(normalize(historical), archives_dir, output, verify_only)
    result["manifest_security_hold_labels"] = sum(item.get("selection") == "security_hold" for item in historical["members"])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--archives-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--verify-only", action="store_true", help="Check all original bytes and existing targets without writing files")
    args = parser.parse_args()
    try:
        result = restore(args.manifest, args.archives_dir, args.output, args.verify_only)
    except (core.RestoreError, OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as error:
        print(f"Historical restore failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
