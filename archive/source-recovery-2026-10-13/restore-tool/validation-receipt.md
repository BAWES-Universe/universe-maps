# Map-source restore validation receipt

Validated 2026-10-13 at 09:23 UTC. Elapsed execution: 78.35 seconds.

- Manifest verification: **116/116 passed**, zero errors.
- Files verified: **3,430**, totaling **1,137,905,801 uncompressed bytes**.
- Outer ZIPs, each nested ZIP, and every expected member passed size and SHA-256 checks; listed Git blob SHA-1 checks also passed.
- Every package used the real authenticated-Library-materialized artifact named by its manifest.
- `--verify-only` created no output.
- Clean restore of `N35-r3-source`: 26/26 files written and independently SHA-256/size checked.
- Clean restore of `lighthouse-last-signal-r2-source`: 47/47 files written and independently SHA-256/size checked.
- Output file sets exactly matched both manifests, with no extra files.
- Repeated restores wrote **zero files**; all 73 existing files retained their bytes and modification times.
- Post-restore `--verify-only` passed for both packages.
- Focused generated-fixture self-tests: **14 passed**.
- No builds, generated map assets, remote writes, or changes to original archives/manifests. Temporary restore outputs were removed.

Tested `restore.py` SHA-256: `5713f6c8abc235a9ecf8361b71fdca53e8ffedef75209f710abd1fea5e09c2f0`.

The accompanying `validation-receipt.json` records per-manifest hashes, artifact names and fingerprints, per-package counts, and all 73 independently checked output fingerprints.

These checks establish byte agreement with the supplied manifests and local materialized archives. They do not establish independent manifest provenance or future Library availability.

## Repeat

```sh
python3 -B restore.py --manifest PATH_TO_MANIFEST.json --archives-dir AUTHENTICATED_ARCHIVE_CACHE --output FRESH_OUTPUT --verify-only
python3 -B restore.py --manifest PATH_TO_MANIFEST.json --archives-dir AUTHENTICATED_ARCHIVE_CACHE --output FRESH_OUTPUT
python3 -B restore.py --manifest PATH_TO_MANIFEST.json --archives-dir AUTHENTICATED_ARCHIVE_CACHE --output FRESH_OUTPUT
```
