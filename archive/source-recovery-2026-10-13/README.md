# Recoverable map source checkpoint

This branch preserves small authoring code, configuration, source documentation and exact recovery manifests. Large artwork, runtime assets and bulky evidence stay in their durable Library originals. This is not a complete all-assets Git mirror, an R2 backup or a deployment.

## Verified coverage

- All 50 old maps: complete source and runtime packages recovered and hash-verified. Source text is in old50/source; every remaining file has an exact artifact/member mapping in asset-manifests.
- Original 12 templates: complete rebuild archives recovered; source text and exact Library mappings preserved under original12.
- N35 Lighthouse Festival Island is part of the 50-map collection. Last Signal r2 separately has recovered complete source and runtime. Keeper Return r2 has recovered runtime only; its full rebuild source is missing.
- The rendering investigation preserves Studio r8 and Reading r4 runtime fixtures, not their complete source generators. Media r9 source/runtime remain missing.
- The 33 new H-series original packages remain unavailable. H009-initial, H025 and H039 folders contain clearly labeled partial recoveries. Historical READY files and scoped test results do not make those partials complete.

## Restore without handling ZIPs manually

An assistant uses the connected Library tools to materialize the artifact IDs named in ASSET-INDEX.json and each package manifest. Signed download URLs and credentials are deliberately absent from this repository. The restore tool verifies the artifact, nested archive, and every original member before restoring files to their exact paths. See restore-tool/README.md.

Restore a complete package before running its original build instructions. Typical prerequisites include Python 3, Pillow, NumPy, Node.js, and for some review tools ReportLab, pdftoppm and DejaVu Sans fonts. No paid image generation is needed for these recovered original packages. This checkpoint does not claim fresh builds or live-game acceptance.

The testing workbook and SOURCE-AVAILABILITY.json distinguish source recovery, runtime recovery, historical QA and live acceptance. Existing master, gh-pages and published maps are unchanged.
