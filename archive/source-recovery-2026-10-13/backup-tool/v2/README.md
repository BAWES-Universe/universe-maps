# Universe durable backup tool (chunked format v2)

## Status

Implemented and locally tested. R2 is **not configured, authenticated, contacted, or operating**. No credentials were entered; no bucket, billing, permissions, Git branches, deployments, or scheduled watchers were changed. Python 3 is available here; boto3 is not installed here. Unit tests use an in-memory object store and fake SDK clients, never a real bucket. A real R2 backup and a clean restore drill are still required before declaring the project protected.

## What it does

- Named, explicitly configured project roots only. Never backs up the whole computer.
- Fixed 8 MiB SHA-256 content-addressed chunks preserve each file's relative path, whole-file hash and ordered chunk hashes in one immutable global manifest. Identical chunks share one object. Changed versions create new keys; old checkpoints remain usable.
- A full local scan happens before R2 access. HEAD planning checks the entire incremental write budget before the first upload.
- Missing objects use conditional `PutObject(IfNoneMatch='*')`. Existing objects are never overwritten. Every object is downloaded and hash-checked, even when it already existed.
- A second complete local content scan detects changed, added, removed, or unreadable eligible files before checkpoint creation. The manifest is uploaded and downloaded/verified next; the checkpoint is last and is also downloaded/verified.
- Interrupted runs can be rerun. Already uploaded matching objects are reused; corrupt existing objects cause a hard failure, never repair-by-overwrite. Partial remote data is retained. An accepted checkpoint PUT followed by lost response is not reported locally as success; retry verifies it.
- Restore requires an entirely new destination directory. It verifies checkpoint, manifest, downloaded objects and written files; uses no-follow/exclusive creation and fsync. Failure preserves a partial destination for inspection; retry into a different fresh destination.
- No delete, overwrite, mirror, `sync --delete`, force, merge, deploy, watcher, garbage-collection or credential-writing functionality exists.

## Boundaries and exclusions

The format stores files, paths and executable bits; not ACLs, ownership, timestamps, xattrs, or empty directories. This is file-level recovery, not a complete filesystem image or an application-transactional snapshot. For mutually dependent live-writing files, quiesce their writer or point this tool at a filesystem snapshot. Two scans improve consistency but do not provide a transaction across a live project.

The default allowlist covers source, common artwork/fonts/media and map JSON formats (`tmj`, `tsj`, `wam`). Unknown extensions and archives are explicitly listed as excluded. ZIP/tar/7z/rar originals remain excluded even under `reviewed_include`. A separate `reviewed_gzip` map can admit only exact compressed hashes already independently bounded-decompressed and scanned; the backup verifies those raw hashes before upload. It does not itself decompress archives. Use reviewed extracted project roots for source recovery. Hidden credential directories/files, `.env*`, key files, cookie/session files, raw download/upload JSON and common secret names are excluded. Eligible file contents are scanned for common credentials, signed URL parameters, credential-bearing URLs and private keys. Matches stop the run. Literal credential assignments are distinguished from token-named code expressions; there is no broad path waiver. A 4 KiB rolling overlap catches ordinary cross-chunk secrets, but extreme separator formatting longer than that overlap and encoded/obfuscated credentials can evade detection. These heuristics are deliberately conservative and **cannot guarantee that every secret is detected**. Review the intended roots and exclusions before activation. Never silently waive a match or infer it is harmless from the filename. An optional `reviewed_include` dictionary admits an exact manifest path and SHA-256 after review, overriding only its filename/extension filter. Missing or changed reviewed files stop the run, and all content-secret checks still apply. It never admits an entire directory or overrides `extra_exclude`. `root_files` restricts a named root to exact relative files; unrelated sibling names are not uploaded. Nonarchive and gzip review maps cannot overlap. A separately named `reviewed_nonsecret_matches` entry may exempt only independently inspected nonsecret spans (synthetic test fixtures or validated encoded PDF image bytes), pinned to exact whole-file SHA-256 and each match’s offset, length and SHA-256. Every other match still stops the run. Changing any reviewed file or span invalidates its exception.

Symlinks in eligible sources or any source/restore ancestor, hardlinks and special files are rejected. Paths are strict POSIX relative paths. Restore is designed for a private Linux executor, not case-insensitive Windows/macOS filesystems. A malicious same-UID local process can interfere with any process's files; do not run alongside an untrusted local writer.

The process streams files in fixed 8 MiB chunks and retains source references and bounded metadata instead of whole-file contents. Files and inventories can exceed the former 64/512 MiB limits: a 101 MiB fixture was backed up, cleanly restored, and retried with about 50 MiB peak process RAM. Explicit source limits can be configured up to 1 TiB, with 100,000 files, 8 MiB scanned path/chunk metadata, and a 32 MiB manifest cap; these safety budgets are checked before upload. The metadata ceiling may be reached before the configured byte ceiling (for a single file, below 512 GiB); this is deliberately bounded rather than unlimited. Inventory limits and approved incremental upload budgets are separate. The example supports a 16 GiB inventory and 2 GiB individual files while still limiting new remote data to 128 MiB per run. Chunks are automatically split; upload budgets are never automatically raised.

Additional explicit upload limits: `max_new_bytes` includes new content, manifest and checkpoint. `max_upload_operations` reserves up to 3 PUT attempts per missing key, matching the SDK's maximum attempts. These are per-run bounds, not billing guarantees. HEAD/GET operations and repeated runs can still incur charges. Default example caps are 128 MiB new data and 6,000 PUT attempts. Account allowance, bucket contents, existing storage and prices remain unknown; check them before authorizing real uploads.

## Nonsecret configuration and secure setup

`config.example.json` contains placeholders, never usable credentials. Create a reviewed configuration with exact roots, account ID, private bucket, prefix, and limits. Keep credentials external to Git and this configuration. boto3 uses its standard secure environment/config chain:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` only if required by temporary credentials

The user must provision these through their selected environment's secure credential setup. Do not paste them in chat, source, command arguments, logs, this README, or config. Use bucket-scoped access; the script itself has no delete method, but standard bucket read/write credentials may still authorize deletion by other software. Credentials are not an enforcement boundary against a compromised process. Stronger bucket retention/locks require separate review and permission.

The R2 endpoint is derived from account ID; no arbitrary URL or presigned URL is accepted in config. The region is `auto`. Install a current official boto3 package in the chosen environment when authorized. The script checks SDK conditional-create support and fails if unavailable. Network timeouts/retries are bounded; API errors are printed only as exception type, never SDK request/credential details. Do not enable external SDK debug logging.

## Commands (from this directory)

Local-only preflight, no credentials or boto3 needed:

    python3 universe_backup.py --config source-assets.local.json preflight

For configured, reviewed roots on the chosen executor:

    python3 universe_backup.py --config /absolute/path/backup-config.json preflight

Only after R2 authorization, cost review, source review and secure setup:

    python3 universe_backup.py --config /absolute/path/backup-config.json backup --enable-r2-writes

Record the returned checkpoint SHA-256 in an independent location. There is deliberately no mutable `latest` pointer.

    python3 universe_backup.py --config /absolute/path/backup-config.json restore --checkpoint CHECKPOINT_SHA256 --destination /absolute/path/NEW-empty-name

The destination must not exist; its parent must already exist. Restoring does not scan source roots, so those paths need not exist on the recovery machine. The config's file/byte budgets still apply.

    python3 -m unittest -v test_backup

## Evidence and coverage

`TEST-RESULTS.txt` records 60 local unit tests. `LARGE-FILE-TEST-RESULTS.json` records the 101 MiB / 13-chunk clean-restore and idempotent-retry proof using a local disk fixture store, with 50,364 KiB measured peak RAM and no network requests. `SOURCE-ASSETS-PREFLIGHT-v2.json` covers only reconstructed Keeper, Studio/Reading, Media House source directories and Keeper runtime. It is not full recovery-artifact coverage. `ALL-RECOVERIES-PREFLIGHT.json` inventories the broader five explicitly named recovery roots and reports their budget failure without reading/uploading all content. `RECONSTRUCTIONS-PREFLIGHT-v2.json` now passes for the broader reconstruction roots after correcting literal-credential recognition. The earlier conservative rejection involved token-named function/variable expressions in vendor GameScene.ts (SHA-256 7c901514db24890c3750631d8e32124643e87de41750fb90e4a2d7f54ac1c146); no source file was modified or path/hash waiver introduced. `FULL-LOCAL-HASH-AUDIT-summary.json` reports 11,889 eligible files, 4,808,214,404 logical bytes and 3,078,222,884 unique whole-file bytes. That separate audit hashes bytes only; it did not run the full secret scan and is not a live backup. Its 352 exclusions remain a separately reviewed coverage gap, including archives and documents.

No live S3/R2 integration test has run. Validate on a small non-sensitive fixture using the real selected bucket first, including conditional-write refusal, downloaded hash verification, interruption/retry and clean restore. Then approve the actual source batch and budget. No indefinite watcher is installed.

## References

- Official R2 S3 compatibility, including conditional PutObject: https://developers.cloudflare.com/r2/api/s3/api/
- Official R2 S3 SDK authentication: https://developers.cloudflare.com/r2/api/tokens/

Wrangler OAuth was considered but not used: the documented CLI put lacks equivalent conditional-create controls, and broad OAuth scope is unnecessary for this script.

Format v1 was a locally tested baseline and was never used for R2. Its Library checkpoint remains preserved; format v2 is intentionally distinct and does not interpret v1 manifests.

## Reviewed wider coverage (still offline)

`recovery-reviewed-complete.local.json` includes 133 independently screened nonarchive exclusions (including both distinct testing workbooks), 15 bounded-decompressed gzip validation proofs, exact-hash nonsecret match reviews covering synthetic fixtures, code comparisons, local-storage key names, and independently decoded SVG/PDF image streams. It selects only the current requested workbook from its output directory. Candidate scope: 12,037 files / 4,947,929,698 logical bytes. All 200 original ZIP bundles passed bounded nested-member screening and are ready for a separate authorized archive-preservation workflow. The script still intentionally excludes those original ZIPs. Their scope is: 4,660,506,066 logical bytes, 195 unique hashes / 4,559,698,609 unique bytes. The five remaining cache directories are deliberately omitted. Original-archive screening details are summarized in SCREENED-ORIGINAL-ARCHIVES-MANIFEST.json; every original hash must still be verified after remote upload.

The finite full raw-byte audit is complete: 12,037 candidates were scanned and all flagged spans were reconciled to independently reviewed exact file/match hashes; zero unreviewed matches remain. Five incidental raw-pattern hits across three PDFs were independently traced to successfully decoded image streams and admitted only by exact file/match hashes; no blanket PDF exception is used. The actual production scanner also passed a local preflight of all 187 reviewed files (216,182,101 bytes), including the real 101,316,600-byte compressed validation proof. A full 4.95 GB production preflight/backup and a real full-scope clean restore have not been run. Upload is still unconfigured/disabled, and the 128 MiB new-data cap remains unchanged.

Final aggregate estimates: extracted/source/review/gzip scope is 4,947,929,698 logical bytes and 3,217,865,585 unique whole-file bytes (6,671 whole-file hashes). This is not an exact R2 chunk upload estimate. Original ZIP scope adds 4,559,698,609 unique bytes; actual destination contents, charges and upload authorization remain separate.
