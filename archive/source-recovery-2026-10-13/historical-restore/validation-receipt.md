# Historical restore validation

Final code verified 2026-10-13 at 11:01 UTC.

- **181/181 original archives passed**, with zero failures.
- **9,018 original members** passed exact paths, SHA-256, sizes, and Git blob SHA-1 checks.
- Archive bytes checked: **3,741,310,564**; uncompressed member bytes: **4,124,093,000**.
- ZIP member sets exactly matched the manifests.
- Verify-only created no output; all 181 input manifests retained their original hashes.
- Clean sample `native32-same-tile-replan-reproduction`: **9 files** independently rehashed.
- Clean sample `timber-gym-only-r1-review2-source`: **11 files** independently rehashed, including Library artwork and alias-backed source files.
- Repeated restores wrote **zero files** and retained all 20 files' bytes and modification times.
- Post-restore verification passed for both samples. Temporary outputs were removed.
- **29 safety/compatibility tests passed**, including direct CLI verify-only without bytecode-cache writes.
- The original generic restore tool and frozen lean proposal were not edited.

The six frozen `security_hold` labels were included in read-only verification.
A separate review cleared those originals as fixture/encoded-image false positives;
the labels remain unchanged historical metadata, and the test files remain outside
the lean Git source scope. No source archive contents were uploaded.

No map build, runtime execution, deployment, latest-version claim, or acceptance
was performed. Only authenticated Library-materialized archive inputs were used;
GitHub release-asset availability is not assumed.

`validation-summary.json` is the compact Git-ready receipt, containing final code
hashes, sample results, and the detailed audit's SHA-256. The full
`validation-receipt.json` remains local for separate preservation and is excluded
from `DELIVERABLES.json`. Repeat the audit with `validate_snapshot.py`; use a
separate receipt directory to retain the original evidence.
