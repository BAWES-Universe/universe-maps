import hashlib
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

from restore import RestoreError, restore


def fingerprint(data):
    return {"size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def zipped(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries:
            archive.writestr(name, data)
    return output.getvalue()


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.output = self.base / "out"
        self.manifest = self.base / "manifest.json"
        self.files = [("src/map.js", b"export const map = 1;\n"), ("assets/map.bin", b"\x00\xff\x01")]
        self.prepare()

    def prepare(self, entries=None, nested=True):
        entries = self.files if entries is None else entries
        payload = zipped(entries)
        chain = []
        if nested:
            chain = [{"member": "bundle/source.zip", **fingerprint(payload)}]
            payload = zipped([("bundle/source.zip", payload)])
        self.data = {
            "schema_version": 1, "package_id": "selftest", "destination": "old50/source/N01-r3",
            "artifact": {"name": "maps.zip", "library_file_id": "test-only", "version_id": "test-only", **fingerprint(payload)},
            "nested_archives": chain,
            "files": [{"path": name, **fingerprint(data), "git_blob_sha1": hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest(),
                       "storage": "git" if name.endswith("js") else "library", "reason": "selftest"} for name, data in self.files],
        }
        (self.base / "maps.zip").write_bytes(payload)
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")

    def run_restore(self, verify=False):
        return restore(self.manifest, self.base, self.output, verify)

    def target(self, name):
        return self.output / self.data["destination"] / name

    def test_nested_success_restores_code_and_assets(self):
        self.assertEqual(self.run_restore(), {"verified": 2, "written": 2, "existing": 0})
        for name, data in self.files:
            self.assertEqual(self.target(name).read_bytes(), data)

    def test_sequential_nested_success(self):
        payload = (self.base / "maps.zip").read_bytes()
        self.data["nested_archives"].insert(0, {"member": "wrapper.zip", **fingerprint(payload)})
        payload = zipped([("wrapper.zip", payload)])
        (self.base / "maps.zip").write_bytes(payload)
        self.data["artifact"].update(fingerprint(payload))
        self.save()
        self.assertEqual(self.run_restore()["written"], 2)

    def test_verify_only_writes_nothing(self):
        before = sorted(p.relative_to(self.base) for p in self.base.rglob("*"))
        self.assertEqual(self.run_restore(True)["written"], 0)
        self.assertEqual(before, sorted(p.relative_to(self.base) for p in self.base.rglob("*")))

    def test_outer_nested_and_member_bad_hash(self):
        for record in ("artifact", "nested", "file"):
            with self.subTest(record=record):
                self.prepare()
                spec = self.data["artifact"] if record == "artifact" else self.data["nested_archives"][0] if record == "nested" else self.data["files"][-1]
                spec["sha256"] = "0" * 64
                self.save()
                with self.assertRaises(RestoreError):
                    self.run_restore()
                self.assertFalse(self.output.exists())

    def test_bad_size_and_git_blob_hash(self):
        for field, value in (("size_bytes", 99), ("git_blob_sha1", "0" * 40)):
            with self.subTest(field=field):
                self.prepare()
                self.data["files"][-1][field] = value
                self.save()
                with self.assertRaises(RestoreError):
                    self.run_restore()
                self.assertFalse(self.output.exists())

    def test_verify_only_detects_conflict(self):
        target = self.target(self.files[0][0])
        target.parent.mkdir(parents=True)
        target.write_bytes(b"existing edits")
        with self.assertRaisesRegex(RestoreError, "conflicting"):
            self.run_restore(True)
        self.assertEqual(target.read_bytes(), b"existing edits")
        self.assertFalse(self.target(self.files[1][0]).exists())

    def test_unsafe_zip_paths_even_unlisted(self):
        for name in ("../escape", "/escape", "C:/escape", "..\\escape", "safe/../../escape", "a//b", "NUL", "a."):
            with self.subTest(name=name):
                self.prepare(self.files + [(name, b"unsafe")])
                with self.assertRaises(RestoreError):
                    self.run_restore()
                self.assertFalse(self.output.exists())

    def test_unsafe_destination_and_file_paths(self):
        for field in ("destination", "file"):
            with self.subTest(field=field):
                self.prepare()
                if field == "destination":
                    self.data[field] = "../escape"
                else:
                    self.data["files"][0]["path"] = "../escape"
                self.save()
                with self.assertRaises(RestoreError):
                    self.run_restore()
                self.assertFalse(self.output.exists())

    def test_conflict_writes_no_other_members(self):
        target = self.target(self.files[-1][0])
        target.parent.mkdir(parents=True)
        target.write_bytes(b"keep my edits")
        with self.assertRaisesRegex(RestoreError, "conflicting"):
            self.run_restore()
        self.assertEqual(target.read_bytes(), b"keep my edits")
        self.assertFalse(self.target(self.files[0][0]).exists())

    def test_exact_existing_file_is_retained(self):
        name, data = self.files[0]
        target = self.target(name)
        target.parent.mkdir(parents=True)
        target.write_bytes(data)
        original_time = target.stat().st_mtime_ns
        self.assertEqual(self.run_restore(), {"verified": 2, "written": 1, "existing": 1})
        self.assertEqual(target.stat().st_mtime_ns, original_time)
        self.assertEqual(self.run_restore()["written"], 0)

    def test_missing_member(self):
        self.prepare(self.files[:1])
        with self.assertRaisesRegex(RestoreError, "Missing"):
            self.run_restore()
        self.assertFalse(self.output.exists())

    def test_symlink_zip_member(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.prepare(self.files + [(link, b"../../escape")])
        with self.assertRaisesRegex(RestoreError, "Symlink"):
            self.run_restore()

    def test_output_symlink_escape(self):
        outside = self.base / "outside"
        outside.mkdir()
        try:
            self.output.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        with self.assertRaisesRegex(RestoreError, "Symlink"):
            self.run_restore()
        self.assertEqual(list(outside.iterdir()), [])

    def test_case_collision_and_file_parent_collision(self):
        for extra in [("SRC/map.js", b"collision"), ("src", b"collision")]:
            with self.subTest(extra=extra):
                self.prepare(self.files + [extra])
                with self.assertRaises(RestoreError):
                    self.run_restore()


if __name__ == "__main__":
    unittest.main()
