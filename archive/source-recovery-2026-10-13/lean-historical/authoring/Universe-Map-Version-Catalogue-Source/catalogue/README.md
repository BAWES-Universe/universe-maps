# Universe Map Version Catalogue — staged review

This self-contained source recreates the all-maps visual review PDF. It does not build maps or publish anything.

## Maintained identities and state

- PDF identity: `libfile_29638069434c8191a05f1336ef190bbc`; last saved version 4 before this staged update.
- Source identity: `libfile_b20a8aaae09c8191bc7db0d0c4b15b46`; last saved version 3 before this staged update.
- Testing workbook identity: `libfile_304bdb1b4c7c8191a0b1ec1ccab946e7`; saved version 8 is the historical base. The supplied staged workbook has not been uploaded.
- Current staged review: 68 retained versions/studies across 22 visual families, 32 pages, 9 awaiting publication, 1 family in progress, and 0 current verified test links.
- 57 original records are preserved. Eight checked later versions, two frozen held Media versions and the Saltwind Performance visual concept are added. The already-tracked Workshop r2 is also in the nine awaiting publication.
- Media r7 is an additional visual archive beyond the staged workbook's 58 archive records. Media r7b is represented in both. Neither is testable.

## Testing pause and status separation

The user paused testing until the corrected current list is ready. All 18 older published TMJ URLs are retained exactly as archived references only. New candidate URLs are null. Do not turn historical publication or source checks into current test readiness.

The nine awaiting publication are Academy r6, Souk r7 booth repair, Yoga Studio r4, Gym r3, Yoga Retreat r4, Workshop r2 review3, Media House r7c, Reading Conservatory base r2, and Reading Conservatory Garden r1. Their exact staged-workbook records are embedded in each current catalogue row and preserved in `sources/staged-workbook-snapshot.json`.

Saltwind Performance Courtyard r1 is a visual concept with user approval pending, no runtime and unvalidated grid/collision/occupancy/audio.

Celestial's calmer rebuild remains in progress and has no new checked release. Its family page shows archived r4, explicitly labelled as such. Original user design approvals remain distinct from source/native acceptance and live browser/device testing.

Checked candidate images are actual existing decoded native occupied/arrival previews from the frozen source packages. Standing avatars and native facing are retained. No automatic sitting, snapping, turning or live browser/device/AV acceptance is claimed. Animated water is represented by a still frame. Reading Garden paths meet map boundaries; no cross-map transition is configured.

## Production-entry facts

The staged workbook snapshot preserves all 6 category-entry proposals, 8 template-entry proposals and 18 map-variant planning entries verbatim. Observed category names/descriptions/counts remain separate from proposed copy. UUIDs remain blank, slugs are not runtime-verified, and proposals are not deployed changes. The PDF includes a concise category/template appendix; full entry facts remain in the snapshot.

## Rebuild

Requirements: Python 3, Pillow, ReportLab, pypdf and DejaVu Sans fonts at the paths in `build_catalogue.py`. Run `python build_catalogue.py` from this folder. It reads `catalogue-data.json` and the included compressed source-preview assets, and creates `Universe-Map-Version-Catalogue.pdf`.

The build checks unique IDs, complete register text and the URL whitelist. `asset-provenance.json` records original preview paths/hashes and included presentation asset hashes. Original paths are provenance only; no external source image is needed to rebuild the PDF. This bundle contains the image assets needed for the PDF, not runtime source, engine fixtures or full-resolution map releases.

The PDF uses deterministic metadata and content-based image resources. A clean extraction rebuild must match the original PDF byte-for-byte. Render using `pdftoppm -scale-to-x 1400 -scale-to-y -1 -png Universe-Map-Version-Catalogue.pdf qa/page` and inspect every page before delivery. Keep the PDF under 15 MB.

## Future updates

Preserve all prior IDs, design approvals, historical URLs and original images. New checked versions need their own row, existing verified source preview, source/native scope, publication state and live-test state. Do not treat ephemeral work-in-progress as a checked release. `update_catalogue.py` supports an individual canonical row/preview update; `sync_canonical.py` expects a complete list of canonical rows and refuses silent ID loss. The staged workbook snapshot itself is a richer object and must not be passed directly to that list-only sync tool.

The builder separates the current release queue from design history and limits earlier thumbnails to four per family page. Extra visual history continues on a separate page. Existing source snapshots remain for provenance; `catalogue-data.json` is the current rendering source.

Do not upload or replace the maintained Library files until the parent review is complete. On approval, use the verified current versions as guards and preserve both identities. No GitHub or hosting action is part of this source bundle.
