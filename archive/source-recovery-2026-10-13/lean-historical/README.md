# Lean historical source checkpoint

This source tree adds selected historical authoring text and complete Library restore mappings.
The selection and exact aliases were verified against source commit 4333cac6d627df9e3f4a3f215fa0bdf2b9591c9f. The preceding backup commit is 070215b801971310726daa48e914d740911473df. No package is newly declared accepted or latest.

## What belongs in Git

Keep exact UTF-8 authoring/build scripts, bounded authored patches, editable layout and
core build/configuration text, and minimal build documentation. Deduplicate by exact
SHA-256 against the verified base checkpoint, then across historical packages. A
representative authoring path is a storage choice, not a claim that its package is
preferred, approved, complete, or latest. The mobile app checkpoint is limited to its
map-camera/input authoring surface and original mobile patch.

Generated routes, reports, receipts, QA output, provenance copies, pinned engine/vendor
reference trees, runtime payloads/copies, unrelated app/server/test/deployment scope,
bulky text, artwork, audio, fonts, and binary packages stay out of the new Git payload.
Small metadata manifests below preserve every original byte's exact restore address.
This is intentionally not a standalone build checkout: restore each complete original
package, inspect its build instructions and review its dependencies before running it.

## Restore any original member

INDEX.json maps all 181 archive identities to their manifests. Each manifest preserves
the original Library identity, version when recorded, original archive name, bytes and
SHA-256, extracted-directory name, and all original members' exact paths, bytes,
SHA-256 and Git blob SHA-1. Member selection records explain omissions; git_path points
to an identical selected file here or at the recorded base commit when applicable.

1. Use the connected Library's supported materialization route for library_file_id.
2. Verify archive_bytes and archive_sha256 before opening the archive. For the 156
   identities without version_id, never substitute changed current-version bytes.
3. Select the exact member path and verify size, sha256 and git_blob_sha1.
4. Restore to the original member path inside a new safe destination. Reject absolute
   paths, traversal, duplicate names and unexpected links; never overwrite originals.

All omission reasons retain the same Library restore mapping. The six originally flagged test files remain outside this authoring selection, including identical-byte copies. A later independent nested scan cleared all 200 original archives, including these synthetic fixture/image false positives; see SECURITY-REVIEW.json. Original historical selection labels are retained as provenance, not an unresolved credential finding. Additional pattern-screen holds are listed by
archive/path/flag only in SELECTION.json. Do not copy held members into Git without a
separate security review. Screening is heuristic, not proof of absence of secrets.

## Boundaries and verification

All 181 local archive hashes and all 9,018 extracted member hashes were rechecked.
Selection files are byte-identical to their original members. The portable manifest
preserves all original member mappings and hashes. Local originals, earlier prepared
checkpoints, and their paths were not edited. The checkpoint is source-only; no merge, deployment or release publication is included.
No fresh rebuild, runtime test, latest-version recovery or live acceptance is claimed.
Earlier missing-source gaps remain gaps; historical READY or PASS labels are evidence
inside an original package, not new acceptance. Restore-only source references may
depend on Library-only artwork, generated files, upstream packages and evidence.

HISTORICAL-MAP-CATALOG.md and its JSON companion provide human-name/revision recall,
with exact source/art/runtime/recipe/prompt/evidence member links and latest-source gaps.
Counts and omission reasons are in SELECTION.json. Portable expected file hashes and
the exact payload/metadata byte comparison are delivered alongside this directory.

## Automated archive verification and restore

Use ../historical-restore/restore_historical.py with these manifests and archives materialized through authenticated Library access. See ../historical-restore/README.md. GitHub release asset uploads are not currently claimed; Library remains the source of exact archived artwork/runtime bytes.
