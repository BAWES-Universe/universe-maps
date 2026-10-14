#!/usr/bin/env python3
"""Verify Library ZIP artifacts and restore every manifest-listed source member."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import unicodedata
import zipfile


class RestoreError(Exception):
    """Untrusted input or an unsafe/conflicting restore destination."""


def safe_path(value, label="path", directory=False):
    if not isinstance(value, str) or not value:
        raise RestoreError(f"Invalid {label}")
    name = value[:-1] if directory and value.endswith("/") else value
    parts = name.split("/")
    reserved = {"CON", "PRN", "AUX", "NUL", *[f"{p}{i}" for p in ("COM", "LPT") for i in range(1, 10)]}
    if any(not p or p in (".", "..") or p[-1:] in (" ", ".")
           or p.split(".")[0].upper() in reserved
           or any(ord(c) < 32 or c in '<>:"\\|?*' for c in p) for p in parts):
        raise RestoreError(f"Unsafe {label}: {value!r}")
    return name


def fingerprint(spec, label):
    if not isinstance(spec, dict):
        raise RestoreError(f"Invalid {label} record")
    size, digest = spec.get("size_bytes"), spec.get("sha256")
    if type(size) is not int or size < 0 or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        raise RestoreError(f"Invalid size/SHA-256 for {label}")
    blob = spec.get("git_blob_sha1")
    if blob is not None and (not isinstance(blob, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", blob)):
        raise RestoreError(f"Invalid Git blob SHA-1 for {label}")
    return size, digest.lower(), blob.lower() if blob else None


def verify_stream(source, spec, label, sink=None):
    size, expected, blob = fingerprint(spec, label)
    sha = hashlib.sha256()
    git = hashlib.sha1(f"blob {size}\0".encode()) if blob else None
    count = 0
    while True:
        chunk = source.read(min(1024 * 1024, size - count + 1))
        if not chunk:
            break
        count += len(chunk)
        if count > size:
            raise RestoreError(f"Size mismatch: {label}")
        sha.update(chunk)
        if git:
            git.update(chunk)
        if sink:
            sink.write(chunk)
    if count != size or sha.hexdigest() != expected:
        raise RestoreError(f"Size/SHA-256 mismatch: {label}")
    if git and git.hexdigest() != blob:
        raise RestoreError(f"Git blob SHA-1 mismatch: {label}")


def key(path):
    return unicodedata.normalize("NFD", path).casefold()


def check_paths(entries):
    """Reject duplicates, cross-platform name collisions and file/dir conflicts."""
    seen, files, directories = {}, set(), set()
    for name, is_dir in entries:
        canonical = key(name)
        if canonical in seen:
            raise RestoreError(f"Duplicate/colliding path: {name!r}")
        seen[canonical] = name
        (directories if is_dir else files).add(canonical)
        pieces = name.split("/")
        for i in range(1, len(pieces)):
            directories.add(key("/".join(pieces[:i])))
    if files & directories:
        raise RestoreError("A file path is also used as a directory")


def inspect_zip(archive):
    members, entries = {}, []
    for item in archive.infolist():
        name = safe_path(item.orig_filename, "ZIP member", directory=item.is_dir())
        kind = stat.S_IFMT(item.external_attr >> 16)
        allowed = (0, stat.S_IFDIR) if item.is_dir() else (0, stat.S_IFREG)
        if kind not in allowed:
            raise RestoreError(f"Symlink/special ZIP member rejected: {name!r}")
        entries.append((name, item.is_dir()))
        members[name] = item
    check_paths(entries)
    return members


def member(archive, members, name, spec):
    item = members.get(name)
    if item is None or item.is_dir():
        raise RestoreError(f"Missing file in ZIP: {name!r}")
    if item.file_size != spec["size_bytes"]:
        raise RestoreError(f"ZIP size mismatch: {name!r}")
    return archive.open(item)


def checked_path(path, expect_dir=False, create=False):
    """Refuse symlinks and special files at every existing path component."""
    path = Path(os.path.abspath(path))
    cursor = Path(path.anchor)
    for i, piece in enumerate(path.parts[1:]):
        cursor /= piece
        last = i == len(path.parts) - 2
        try:
            mode = cursor.lstat().st_mode
        except FileNotFoundError:
            if create and (not last or expect_dir):
                cursor.mkdir()
                mode = cursor.lstat().st_mode
            else:
                continue
        if stat.S_ISLNK(mode):
            raise RestoreError(f"Symlink in destination: {cursor}")
        if not last or expect_dir:
            if not stat.S_ISDIR(mode):
                raise RestoreError(f"Destination parent is not a directory: {cursor}")
        elif not stat.S_ISREG(mode):
            raise RestoreError(f"Destination is not a regular file: {cursor}")
    return path


def existing_matches(target, spec):
    checked_path(target)
    if target.exists():
        with target.open("rb") as source:
            try:
                verify_stream(source, spec, str(target))
            except RestoreError as error:
                raise RestoreError(f"Refusing conflicting existing file: {target}") from error
        return True
    return False


def read_manifest(path):
    with open(path, encoding="utf-8") as source:
        manifest = json.load(source)
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise RestoreError("Expected manifest schema_version 1")
    destination = safe_path(manifest.get("destination"), "destination")
    artifact = manifest.get("artifact")
    fingerprint(artifact, "artifact")
    name = safe_path(artifact.get("name"), "artifact filename")
    if "/" in name:
        raise RestoreError("Artifact name must be a filename, not a path")
    nested, files = manifest.get("nested_archives", []), manifest.get("files")
    if not isinstance(nested, list) or not isinstance(files, list) or not files:
        raise RestoreError("Expected nested_archives list and nonempty files list")
    for spec in nested:
        fingerprint(spec, "nested archive")
        safe_path(spec.get("member"), "nested archive member")
    for spec in files:
        fingerprint(spec, "file")
        safe_path(spec.get("path"), "file path")
        if spec.get("storage") not in ("git", "library"):
            raise RestoreError("File storage must be git or library")
    check_paths([(spec["path"], False) for spec in files])
    return manifest, destination, artifact, nested, files


def restore(manifest_path, archives_dir, output, verify_only=False):
    manifest, destination, artifact, nested, files = read_manifest(manifest_path)
    archive_path = Path(archives_dir) / artifact["name"]
    if archive_path.is_symlink() or not archive_path.is_file():
        raise RestoreError(f"Archive must be an existing regular file: {archive_path}")
    root = checked_path(Path(output) / destination, expect_dir=True)
    # Keep outer file open; use memory for nested ZIPs so --verify-only writes nothing.
    with archive_path.open("rb") as outer:
        verify_stream(outer, artifact, artifact["name"])
        outer.seek(0)
        stream = outer
        for spec in nested:
            with zipfile.ZipFile(stream) as archive:
                members = inspect_zip(archive)
                buffer = io.BytesIO()
                with member(archive, members, spec["member"], spec) as source:
                    verify_stream(source, spec, spec["member"], buffer)
                stream = buffer
                stream.seek(0)
        with zipfile.ZipFile(stream) as archive:
            members = inspect_zip(archive)
            if verify_only:
                existing = 0
                for spec in files:
                    with member(archive, members, spec["path"], spec) as source:
                        verify_stream(source, spec, spec["path"])
                    existing += existing_matches(root / spec["path"], spec)
                return {"verified": len(files), "written": 0, "existing": existing}
            # Validate and stage every file before making any destination changes.
            with tempfile.TemporaryDirectory(prefix="verified-map-restore-") as temporary:
                staged = Path(temporary)
                for index, spec in enumerate(files):
                    with member(archive, members, spec["path"], spec) as source, (staged / str(index)).open("wb") as sink:
                        verify_stream(source, spec, spec["path"], sink)
                already = [existing_matches(root / spec["path"], spec) for spec in files]
                written = 0
                for index, spec in enumerate(files):
                    target = root / spec["path"]
                    if already[index]:
                        continue
                    checked_path(target.parent, expect_dir=True, create=True)
                    checked_path(target)
                    try:
                        sink = target.open("xb")
                    except FileExistsError:
                        existing_matches(target, spec)
                        already[index] = True
                        continue
                    try:
                        with sink, (staged / str(index)).open("rb") as source:
                            shutil.copyfileobj(source, sink)
                    except BaseException:
                        target.unlink()
                        raise
                    written += 1
                return {"verified": len(files), "written": written, "existing": sum(already)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--archives-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--verify-only", action="store_true", help="Hash artifacts and members; check existing files; write nothing")
    args = parser.parse_args()
    try:
        result = restore(args.manifest, args.archives_dir, args.output, args.verify_only)
    except (RestoreError, OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as error:
        print(f"Restore failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
