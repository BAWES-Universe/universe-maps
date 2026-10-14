# Collection directory

[Whole collection](../../COLLECTION.md) · [HTML directory](index.html) · [Directory data](collection.json)

This additive directory presents all 80 exact preserved runtime candidates in nine groups. All 123 review cards and their imported feedback remain unchanged in `../map-testing/`.

## Publication contract

The public directory and all original files share this prefix:
`https://bawes-universe.github.io/universe-maps/recovered/2026-10-13-collection-v1/`

Directory assets live at its root. Runtime paths retain the entire suffix after `archive/runtime-recovery-2026-10-13/`. The links in `collection.json` point to TMJ/WAM file responses, never GitHub HTML source pages. Publication and HTTP hash verification must be recorded separately from the original GitHub restore receipt. There are no fabricated or verified play-room URLs in this prepared catalogue.

## Updating the directory

- Keep all 80 runtime IDs discoverable. Show related variants together; preserve rejected / paused / historical status.
- Update matching entries in `collection.json`, `index.html` and the relevant family guide. Preserve revision labels, exact hashes, review links and original feedback.
- Add a room URL only after verifying its registered map and WAM, and record actual acceptance separately.
- Do not label themed service areas as working services when properties are empty or setup is disabled.
- The rendered images use the original TMJ and image bytes. `preview-manifest.json` and `crop-manifest.json` record provenance. Cropped island and room previews are explicitly separate views, not newly drawn artwork.
- `collection.js` only filters existing HTML, expands a linked card and copies URLs. No external dependencies, trackers, backend, account actions or map execution are present.

## Evidence and checks

- `functional-crosswalk.json`: independent source-level feature inspection.
- `preview-validation.json`: deterministic rerender and image provenance checks.
- `preview-manifest.json`: full scene thumbnail hashes and source dependencies.
- `crop-manifest.json`: original-pixel crop bounds and hashes.
- `../../tools/map-collection/`: reproducible source-image rendering tools.
- [Existing common tests](../map-testing/COMMON-CHECKS.md): mobile, desktop, collision, interaction, AV, reconnect and engine regressions.

Static previews and configured features are not live acceptance. Missing 33 H originals, Media r9 and original-master limitations remain in [the missing ledger](missing.md).
