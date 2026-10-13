# Runtime restore receipt

[All maps](../../MAPS.md) · [Testing register](README.md)

**PASS: independent fresh download from GitHub**, checked 2026-10-13T13:08:08.014841+00:00. This verifies backup restoration and file integrity. It does not establish deployment, design approval or live game acceptance.

- Repository: BAWES-Universe/universe-maps
- Exact commit: [`9f80f9020df16993a4d1811552b0d816d403ccb1`](https://github.com/BAWES-Universe/universe-maps/commit/9f80f9020df16993a4d1811552b0d816d403ccb1)
- Exact tree: `99563233ab2962604ff0f71cce0a8d18faed0c3d`
- Runtime directory: [archive/runtime-recovery-2026-10-13](../../archive/runtime-recovery-2026-10-13/)
- Scope: **80 selected candidates/experiences; 596 original runtime file paths plus 4 metadata files = 600 files**. Historical/experimental/rejected options retain their separate status.
- Original runtime bytes by path: **341,991,574 bytes**. Identical content accounts for **489 distinct original Git blobs**; this is not a count of newly accepted maps.
- Total downloaded bytes including the four metadata files: **342,366,026 bytes**.

## Checks actually completed

- Downloaded all 600 files into a fresh directory from the exact GitHub commit; no local recovery copy substituted for the download.
- Matched all 600 Git blob identities/sizes/modes to the committed tree; all 596 original runtime SHA-256 hashes matched the frozen manifest.
- Decoded/checked 420 PNG files and 2 WAV files; parsed 155 JSON files; checked syntax of 11 JavaScript files and headers of 8 MP3 files.
- Resolved all 517 recorded local dependency edges; no missing local dependencies.
- Unresolved errors: **0**. [Machine-readable receipt](data/runtime-restore-verification.json).

## Use the restored package

Choose the exact revision in [CATALOG.json](../../archive/runtime-recovery-2026-10-13/CATALOG.json). Restore its entire subtree, preserve relative paths, and verify [SHA256-MANIFEST.json](../../archive/runtime-recovery-2026-10-13/SHA256-MANIFEST.json) before using its TMJ/WAM entrypoints. A GitHub file URL is not a playable room. Import/configure companion WAM areas separately and test the actual engine build before any approved deployment.

## What remains open

- 33 H-series originals remain missing; their master artwork, final TMJ/textures, source workflow and original freeze evidence have not been recovered.
- Media House r9 remains missing. r7c and its partial reconstruction do not recover the later repairs or configure the four empty service areas.
- Studio r8, Reading r4 and Keeper r2 retain exact frozen/runtime bytes, but their complete original authoring packages remain unavailable. Reconstructed authoring is labeled separately.
- This runtime backup contains runtime textures, not a claim that every generation master, original image prompt/seed, historical ZIP or source asset has been recovered.
- Keeper’s teleport-recovery race and Studio/Reading pixelation, black-edge and seam complaints remain open. No browser, GPU, game-engine, native-body, phone, audio/multi-user or design acceptance was established by this readback.
