# Verified map-source restore

A portable, standard-library-only Python 3 tool. GitHub keeps reviewable source,
this tool, and manifests; the user's durable ChatGPT Library keeps the complete
ZIP artifacts, including large assets. A manifest does **not** contain the assets
or make GitHub a self-contained backup.

## Restore

1. Ask your assistant to resolve the manifest's `artifact.library_file_id` and
   `artifact.version_id` through the connected Library tools and current Library
   skill, then materialize that exact artifact in a local archives directory.
   This authenticated download is a separate step. You do not need to open,
   extract, or manually handle the ZIPs. If that version is unavailable, stop;
   do not silently substitute a newer artifact.
2. Run:

   ```sh
   python3 restore.py --manifest manifests/example.json --archives-dir ./archives --output ./restored
   ```

   For a read-only integrity check first:

   ```sh
   python3 restore.py --manifest manifests/example.json --archives-dir ./archives --output ./restored --verify-only
   ```

The downloaded filename must match `artifact.name`. The tool uses local bytes
only; it has no network client, public links, signed URLs, credentials, or
account-specific download logic. Do not commit downloaded archives or restored
large assets accidentally. Keep the archive cache outside your Git checkout.

## Contract and guarantees

- Schema version 1 requires `destination`, `artifact`, `nested_archives`, and
  `files`. Fingerprints are SHA-256 and byte size. A file's optional
  `git_blob_sha1` is also checked when present.
- `nested_archives` is an ordered chain: each `member` names the ZIP inside the
  previous ZIP. Every chain archive is verified before opening it.
- Each `files[].path` is an exact member name in the deepest ZIP. There is no
  implicit directory stripping. The restored location is
  `OUTPUT / destination / path`.
- **All listed members are restored**, including `storage: "git"` files.
  `storage` and `reason` describe backup placement, not extraction filters.
  Extra safe ZIP members are ignored. Missing listed members fail.
- SHA-256/size checks cover the outer artifact, every nested ZIP and every
  expected file. ZIP CRC checks also run while members are read. All expected
  files are verified and staged before any destination file is written.
- Unsafe ZIP/manifest names, duplicate or case/Unicode-colliding member names,
  file/directory collisions, symlinks, and special ZIP entries are rejected.
  Existing destination symlinks or nonregular files are rejected. Existing
  identical files are retained; different bytes fail before restoration starts.
- No existing file is overwritten. A newly created partial file is removed if
  its write fails. An interrupted restore can leave complete earlier files;
  rerun the same command to finish safely.
- `--verify-only` performs no filesystem writes and also checks any existing
  destination files for conflicts. It does not require the output to exist.
- Use a private output directory with no concurrent untrusted writers. Path
  checks guard against preexisting symlinks; this portable implementation does
  not claim protection against hostile concurrent filesystem modifications.
- Nested ZIP bytes reside in memory. A normal restore also temporarily stages
  all listed uncompressed files; allow sufficient RAM and temporary disk space.
  Fingerprints prove agreement with a trusted manifest, not manifest provenance.

Success prints a JSON count summary and exits 0. Validation or restore errors
print a diagnostic and exit 1. Verification succeeds even if the output is
absent; this validates recoverability, not that a restore already exists.

## Self-tests

```sh
python3 -m unittest -v test_restore.py
```

Tests generate their own temporary manifests and ZIPs; no real Library files,
network access, third-party packages, or credentials are needed.
