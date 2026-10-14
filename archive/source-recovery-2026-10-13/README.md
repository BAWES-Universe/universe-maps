# Recoverable map source checkpoint

This source tree preserves small authoring code, configuration, tests, reconstruction sources and exact recovery manifests. Large artwork, runtime assets and bulky evidence remain in their authenticated Library originals. It is not an all-assets Git mirror, an R2 backup or a deployment.

## Verified source and asset coverage

- Commit 4333cac6d627df9e3f4a3f215fa0bdf2b9591c9f preserved 1,859 recovered source/manifest entries. This tree adds the separately labeled reconstructed authoring described below.
- All 50 old maps: complete source and runtime packages recovered and hash-verified. Selected source text is under old50/source; exact remaining artifact/member mappings are in asset-manifests. N35 Lighthouse Festival Island belongs to this group.
- Original 12 templates: complete rebuild/source archives recovered, with selected text under original12 and every remaining byte Library-backed. Last Signal r2 separately has complete recovered source and runtime.
- Keeper Return r2: original runtime and all 16 artwork inputs survive. Newly reconstructed editable source reproduces all 19 runtime files byte-for-byte. Its inherited teleport-race failure remains documented. The original full source archive is still unavailable.
- Studio r8 and Reading r4: surviving original runtime fixtures support separately reconstructed editable layers/builders, reproducing 11 outputs exactly. The original full source archives remain unavailable.
- Media House: original r7c source/runtime survive; the partial reconstruction reproduces five original runtime files and adds two test landmarks only. Missing r9 and its visual repairs have not been recovered.
- The 33 H-series original packages remain unavailable. H009-initial, H025 and H039 are clearly labeled partial recoveries. Historical READY files and test results do not turn them into complete originals.
- A separate authenticated Library catalogue inventories 181 historical archives and 9,018 exact members, including the original 12. These counts overlap the groups above. Diagnostic, blocked and concept packages retain their historical limitations. Selected unique historical authoring/build/configuration text and complete restore manifests are under lean-historical.

## Restore

Use ASSET-INDEX.json and RESTORE-CATALOG.json to locate the exact Library identity, archive hash and member mappings. An assistant can materialize these through authenticated Library tools without asking the user to manage ZIP files. Signed download URLs and credentials are absent. The restore tool verifies outer archives, nested archives and every member before restoring exact paths. See restore-tool/README.md and reconstructed/RESTORE-RECONSTRUCTIONS.md.

Restore a complete package before building. Typical prerequisites are Python 3, Pillow, NumPy and Node.js; some historical review tools also use ReportLab, pdftoppm and DejaVu Sans. Recovered original artwork is reused without regeneration. Source reconstruction and byte-exact rebuilding are separate from live GPU, body/head/depth, touch or multiplayer acceptance, which remain open unless specifically documented.

No merge or deployment is included. SOURCE-AVAILABILITY.json records remaining gaps, and each preserved test report retains its original scope.

## Find a map by name

Start with [MAP-CATALOG.md](MAP-CATALOG.md), or use the machine-readable [MAP-CATALOG.json](MAP-CATALOG.json). These connect retained revisions to source paths, exact asset manifests, retained generation prompts and build recipes, historical comparison/failure evidence, and missing pieces.

## Historical revisions

[Historical maps by name and revision](lean-historical/HISTORICAL-MAP-CATALOG.md) covers 22 families and all 181 original archive revisions. [Historical index](lean-historical/INDEX.json) pins all 9,018 original members. Only 823 unique authoring/config files are added; identical existing files are referenced, while original artwork/runtime and large QA evidence stay in Library. Use [historical restore instructions](historical-restore/README.md) before building complete original packages.

## Backup implementation

The [frozen v2 backup tool](backup-tool/v2/GIT-CHECKPOINT-NOTES.md) has offline chunked restore/retry tests. Its [README](backup-tool/v2/README.md) documents secure setup and explicit budgets still required. R2 remains unconfigured; source preservation does not establish a live remote backup service. Full reviewed configurations and detailed audit evidence remain pinned in Library.
