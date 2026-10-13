import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

import restore_core as core
from restore_historical import normalize, restore


def hashes(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()}


class HistoricalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.output = self.base / "output"
        self.path = self.base / "manifest.json"
        self.contents = {"original folder/build.py": b"print('fixture')\n", "art/map.bin": b"\0\xfffixture"}
        self.make_manifest()

    def make_manifest(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("original folder/", b"")
            for path, value in self.contents.items():
                archive.writestr(path, value)
        raw = data.getvalue()
        self.manifest = {
            "archive_name": "historical original.zip", "archive_sha256": hashlib.sha256(raw).hexdigest(), "archive_bytes": len(raw),
            "library": {"library_file_id": "fixture-only", "version_id": None, "name": "historical original.zip", "size_bytes": len(raw)},
            "extracted_directory": "original-package", "source_status": "historical_original_not_a_latest_or_acceptance_claim",
            "members": [{"path": path, **hashes(value), "selection": "identical_in_base_checkpoint", "git_path": "some/other/alias"} for path, value in self.contents.items()],
        }
        (self.base / self.manifest["archive_name"]).write_bytes(raw)
        self.save()

    def save(self):
        self.path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def run_restore(self, verify=False):
        return restore(self.path, self.base, self.output, verify)

    def target(self, name):
        return self.output / self.manifest["extracted_directory"] / name

    def test_translation_preserves_original_paths_and_null_version(self):
        normalized = normalize(self.manifest)
        self.assertEqual(normalized["destination"], "original-package")
        self.assertEqual([spec["path"] for spec in normalized["files"]], list(self.contents))
        self.assertIsNone(normalized["artifact"]["version_id"])
        self.assertTrue(normalized["require_exact_members"])

    def test_complete_restore_ignores_storage_aliases_and_is_idempotent(self):
        self.assertEqual(self.run_restore()["written"], 2)
        self.assertFalse((self.output / "some").exists())
        before = {}
        for path, data in self.contents.items():
            target = self.target(path)
            self.assertEqual(target.read_bytes(), data)
            before[path] = target.stat().st_mtime_ns
        second = self.run_restore()
        self.assertEqual((second["written"], second["existing"]), (0, 2))
        self.assertEqual(before, {path: self.target(path).stat().st_mtime_ns for path in self.contents})

    def test_untrusted_alias_is_never_resolved_or_written(self):
        for member in self.manifest["members"]:
            member["git_path"] = "../../outside/alias"
        self.save()
        self.assertEqual(self.run_restore()["written"], 2)
        self.assertFalse((self.base / "outside").exists())

    def test_verification_never_stages_or_creates_output(self):
        before = sorted(path.relative_to(self.base) for path in self.base.rglob("*"))
        with mock.patch.object(core.tempfile, "TemporaryDirectory", side_effect=AssertionError("verification must not stage")):
            self.assertEqual(self.run_restore(True)["verified"], 2)
        self.assertEqual(before, sorted(path.relative_to(self.base) for path in self.base.rglob("*")))

    def test_cli_verification_without_B_creates_no_bytecode_or_output(self):
        tool_dir = self.base / "tool-copy"
        tool_dir.mkdir()
        for name in ("restore_core.py", "restore_historical.py"):
            shutil.copyfile(Path(__file__).with_name(name), tool_dir / name)
        before = sorted(path.relative_to(self.base) for path in self.base.rglob("*"))
        result = subprocess.run([sys.executable, str(tool_dir / "restore_historical.py"),
                                 "--manifest", str(self.path), "--archives-dir", str(self.base),
                                 "--output", str(self.output), "--verify-only"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, sorted(path.relative_to(self.base) for path in self.base.rglob("*")))

    def test_incomplete_manifest_rejected(self):
        self.manifest["members"].pop()
        self.save()
        with self.assertRaisesRegex(core.RestoreError, "file-set"):
            self.run_restore()
        self.assertFalse(self.output.exists())

    def test_missing_member_rejected(self):
        self.manifest["members"][0]["path"] = "missing-file"
        self.save()
        with self.assertRaisesRegex(core.RestoreError, "file-set"):
            self.run_restore(True)

    def test_invalid_member_hash_or_size(self):
        for field, value in (("size", 12345), ("sha256", "0" * 64), ("git_blob_sha1", "0" * 40), ("git_blob_sha1", None)):
            with self.subTest(field=field, value=value):
                self.make_manifest()
                self.manifest["members"][-1][field] = value
                self.save()
                with self.assertRaises(core.RestoreError):
                    self.run_restore()
                self.assertFalse(self.output.exists())

    def test_outer_hash_required(self):
        self.manifest["archive_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(core.RestoreError, "mismatch"):
            self.run_restore()

    def test_unsafe_destination_or_member_rejected(self):
        for location in ("destination", "member"):
            with self.subTest(location=location):
                self.make_manifest()
                if location == "destination":
                    self.manifest["extracted_directory"] = "../outside"
                else:
                    self.manifest["members"][0]["path"] = "../outside"
                self.save()
                with self.assertRaisesRegex(core.RestoreError, "Unsafe"):
                    self.run_restore()

    def test_malformed_archive_identity_rejected(self):
        for field, value in (("archive_name", "../escape.zip"), ("archive_bytes", -1)):
            with self.subTest(field=field):
                self.make_manifest()
                self.manifest[field] = value
                self.save()
                with self.assertRaises(core.RestoreError):
                    self.run_restore(True)

    def test_library_metadata_disagreement_rejected(self):
        self.manifest["library"]["name"] = "different.zip"
        self.save()
        with self.assertRaisesRegex(core.RestoreError, "disagrees"):
            self.run_restore()

    def test_conflict_blocks_entire_restore(self):
        last = list(self.contents)[-1]
        target = self.target(last)
        target.parent.mkdir(parents=True)
        target.write_bytes(b"local edits")
        with self.assertRaisesRegex(core.RestoreError, "conflicting"):
            self.run_restore()
        self.assertEqual(target.read_bytes(), b"local edits")
        self.assertFalse(self.target(next(iter(self.contents))).exists())

    def test_security_hold_is_preserved_only_locally(self):
        self.manifest["members"][-1]["selection"] = "security_hold"
        self.save()
        result = self.run_restore(True)
        self.assertEqual(result["manifest_security_hold_labels"], 1)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.run_restore()["written"], 2)


if __name__ == "__main__":
    unittest.main()
