# Astral Concourse — Concept 01

One shared arrival lobby for a magical multi-hall conference or esports venue. This is a **visual design checkpoint for review**, not a configured room or a playable map.

## Review first

- `review/lobby-concept-review.png` — the one review sheet. The map occupies exactly 1152 × 896 pixels within a 1600 × 1056 sheet, shown at 1 image pixel per world pixel.
- `assets/lobby-concept-native.png` — the same concept without the surrounding review annotations, 36 × 28 tiles at 32 pixels per tile.

## Design

The south entrance leads to a clear central crossroads. Flagship is north; Forum is west; Arena is east. A reception desk and sample directory sit beside the arrival route, with an empty sample-program board on the opposite side. Two small, planted social alcoves are tucked toward the north corners, outside the through-routes.

The concourse is intentionally distinct from the auditorium: there is no stage, central object, audience bank, or repeated seating grid. Warm sandstone, gold craft, deep teal and amber light carry the approved flagship's visual family into a welcoming civic hub.

## Honest limits and review gate

- No TMJ, WAM, collision map, live room, server setup, public publishing, GitHub changes or deployment was created.
- All three portal destinations are unconfigured. The portal artwork is decorative at this stage.
- Silent arrival is design intent only. No audio, proximity, broadcast or media behavior has been configured or tested.
- The directory and program board are explicitly samples. No real event times, speakers, schedule, attendance capacity or operational claims are implied.
- The 32-pixel world canvas and Woka scale are exact. The architectural drawing is concept art: object edges and traversable areas have not yet been grid-snapped, segmented or collision-tested. It should not be treated as a production tileset.
- Four unchanged, unscaled 32 × 32 frames from the provided Woka sheet are illustrative scale references, not attendee-count or spawn configuration.
- Further map implementation and other hall art should wait for parent review of this single concept.

## Source and reproducibility

`source/lobby-architecture-master.png` is the original built-in imagegen output, preserved at 1422 × 1106 pixels. The prompt requested 1152 × 896; the tool returned the same 9:7 aspect ratio at a larger size. The review compositor renders that master into the native32 canvas once. Woka frames are then placed at their original 32 × 32 size with no avatar scaling.

`source/generation-prompt.txt` stores the complete generation recipe. Imagegen was used in built-in mode with the provided flagship artwork as a style reference; no external paid media service was used. Regeneration is stochastic. The preserved master and SVG sources are the deterministic checkpoint.

`references/style-reference.png` and `references/greg-reference.png` are untouched copies of the provided frozen references. Original files elsewhere in the workspace were not modified.

`tools/build-review.mjs` rebuilds the native map and review sheet with Node.js and the installed `sharp` package. Run `node tools/build-review.mjs` from this folder. It produces self-contained SVG sources and PNG renders. Text uses DejaVu Sans; preserve this font for matching review typography.

`source/scale-reference-positions.json` records the exact sprite placements and frame indices. The supplied sheet is three columns by four rows; north = 10, south = 1, east = 7, west = 4, using zero-based row-major indices.

`SOURCE-CHECKPOINT.json` records file hashes and dimensions for this reviewed checkpoint. `docs/visual-qa.md` records the limits of the checks performed.
