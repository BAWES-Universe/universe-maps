# Restore a lean historical archive

This standard-library-only Python 3 adapter restores the **complete original ZIP**
identified by one lean-historical manifest. Keep `restore_historical.py` and
`restore_core.py` together. No network requests, download links, credentials,
builds, uploads, commits, or changes to the archived originals are performed.

## Obtain and verify the original bytes

Ask your assistant to materialize the manifest's `library.library_file_id` through
the connected Library's supported download route into a local archive cache.
Use `library.version_id` when recorded. For manifests without a recorded version,
the SHA-256 and byte size remain the required exact identity: never substitute
changed current-version bytes. If the original cannot be obtained, stop and
report that archive as unavailable. You need not open or extract ZIPs manually.

This adapter uses authenticated Library-materialized archives only; no GitHub
release-asset availability is assumed.

The downloaded filename must exactly match `archive_name`. Keep the archive cache
and restore output outside your Git checkout, sync/upload folders, and deployment
roots. Choose a private output directory without concurrent untrusted writers.

```sh
python3 -B restore_historical.py --manifest PATH_TO_MANIFEST.json --archives-dir LOCAL_ARCHIVE_CACHE --output LOCAL_RECOVERY --verify-only
python3 -B restore_historical.py --manifest PATH_TO_MANIFEST.json --archives-dir LOCAL_ARCHIVE_CACHE --output LOCAL_RECOVERY
```

Run the second command again to check idempotence: identical files are retained,
and the count of newly written files should be zero. Different existing bytes,
symlinks, or special files cause failure rather than being overwritten.

## Exact restore contract

- Output is `LOCAL_RECOVERY / extracted_directory / members[].path`. Original
  member paths and their hierarchy are preserved; no directory stripping occurs.
- `git_path` is a deduplication/storage alias. It is **never** used as the restore
  source or destination. `selection` does not filter the restored members.
- The outer archive's SHA-256 and byte size, the complete non-directory ZIP member
  set, and every original member's SHA-256, byte size, and Git blob SHA-1 are
  checked. Extra unlisted files and missing files fail verification.
- ZIP paths are validated before extraction. Traversal, absolute paths, duplicate
  or case/Unicode-colliding filenames, links, special entries, and file/directory
  collisions are rejected. These same checks come from the verified generic
  engine bundled here, with only in-memory manifest input and exact-member-set
  validation added. The generic source tool itself is unchanged.
- All expected members are verified and temporarily staged before destination
  writes start. Sufficient temporary disk space is needed for the full
  uncompressed package. Interrupted restoration may leave earlier complete files;
  rerun to finish. Directory timestamps and executable modes are not restored.
- `--verify-only` writes no output, temporary manifest, or staged content. It
  streams hashes and checks existing destination files for conflicts. Success
  with absent output establishes recoverability, not that restoration occurred.
- Full local restoration includes all original members, including six test files
  whose frozen manifests retain the historical `security_hold` label. A separate
  review cleared those six as fixture/encoded-image false positives. They remain
  outside the lean Git source scope; the label is preserved metadata, not a
  current unresolved-secret finding. Verification prints no member contents;
  the CLI reports the count as `manifest_security_hold_labels`.
- Content hashes prove agreement with the supplied manifest. They do not prove
  provenance, absence of secrets, buildability, freshness, or acceptance.

No map builds or runtime acceptance tests are part of this tool or its validation.
Historical labels such as READY/PASS do not become current acceptance claims.

## Tests and evidence

```sh
python3 -B -m unittest -v test_historical.py test_core.py
```

Fixture tests cover manifest translation, aliases, all fingerprints, exact ZIP
membership, no-write verification, unsafe paths and links, conflicting files,
retaining identical files, and idempotence. See `validation-receipt.md` for the
real-archive check summary and `validation-summary.json` for compact counts and
code fingerprints. The detailed local `validation-receipt.json` is excluded from
Git; the compact summary records its SHA-256 for separate preservation.

To repeat the complete real-archive audit and temporary sample restores:

```sh
python3 -B validate_snapshot.py --manifests-dir LEAN_HISTORICAL/manifests --archives-dir LOCAL_ARCHIVE_CACHE --receipt-dir LOCAL_RECEIPTS --sample native32-same-tile-replan-reproduction.json --sample timber-gym-only-r1-review2-source.json
```

A fresh output directory is recommended for a clean-room check. Existing output
is also supported: the restore engine retains matching files and refuses
conflicting bytes. Use a separate receipt directory to preserve the checked-in
receipt. `DELIVERABLES.json` lists the stable files intended for Git.
