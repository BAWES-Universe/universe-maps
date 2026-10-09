# Original shared four-person workbench

Built-in imagegen authored one original continuous honey-oak workbench, matching the native fixture's high-angle orthographic camera, teal/brass craft and warm upper-left light. Four compact monitors, keyboards and mice support two opposed pairs. The upper devices face north-side users; the lower devices face south-side users. An imagegen refinement corrected the upper keyboard spacebars and mouse scroll-wheel ends. No room art or rug was added.

## Review

- `proofs/workbench-four-occupied-native.png`: actual 256×256 native proof; four unchanged 32×32 directional Greg frames are scale fixtures only.
- `proofs/workbench-four-occupied-3x.png`: nearest-neighbor enlargement.
- `proofs/workbench-four-empty-native.png`: same registration without occupants.
- `proofs/workbench-four-geometry-3x.png`: labeled route/body/table diagram.
- `proofs/checks.json`: all four protected heads have zero foreground pixel overlap. All eight entry/exit sweeps pass at 1px increments, using 16×16 bodies with the other three occupied bodies blocked.
- `proofs/source-integrity.json`: north/south chairs, foregrounds and contacts are byte-identical copies of the existing cardinal assets. Contact and foreground overlays retain original RGBA source pixels.

## Integration

All geometry is native pixels, with half-open rectangles. Let the visible table's upper-left corner be `(L,T)`.

The visible table is 128×96. `assets/workbench-native.png` is a 160×128 padded canvas, painted bounds `[16,16,144,112)`. Place this canvas at `(L−16,T−16)`. The tight alternative is `assets/workbench-visible-native.png`, 128×96, at `(L,T)`. Draw only one alternative.

The table's useful top is approximately 128×86, with a shallow front and tiny feet. Its conservative movement obstacle is `[L,T,128,96]`. The source-pixel contact mask traces the two lower feet separately; it is not an extra collision obstacle. Exact measurements, source crop and alpha thresholds are in `asset-manifest.json`.

The four avatar centers relative to `(L,T)` are:

- north-1: `(32,−16)`, facing south, Greg frame 1
- north-2: `(96,−16)`, facing south, Greg frame 1
- south-1: `(32,96)`, facing north, Greg frame 10
- south-2: `(96,96)`, facing north, Greg frame 10

Each Woka stays 32×32 at scale 1 with sprite origin center minus `(16,16)` and body rectangle center plus `[-8,0,16,16]`. North body bottoms touch the table's north edge at 0. South body tops touch the table's south edge at 96.

Each chair remains a 48×64 canvas with 30×36 visible bounds `[9,8,39,44)`. North-side positions use the original south-facing chair and anchor `(24,32)`, so its canvas origin is `(seatX−24,−48)` relative to the table. South-side positions use the original north-facing chair and anchor `(24,16)`, so canvas origin is `(seatX−24,80)`. Do not rotate or reflect either asset. The chair foreground stays at the exact same origin as its chair base.

Draw order: chair bases, table, occupants, original chair foregrounds. The tabletop needs no separate foreground at these four positions. North head protection covers the upper 14 rows of each sprite; the nearer armrest ends overlay only the lower body. South chair backs overlay the torso below the head.

Optional combined base and foreground canvases are 256×256, with table upper-left at `(64,80)`. Place those canvases at `(L−64,T−80)`, then render occupants between them. Their combined furniture bounds relative to table are `[0,−40,128,164]`. The proof margin is a neutral receiver only, not room art. The combined asset itself has real transparency.

This is one shared fixed fixture. It has no owner or whole-table claim. Each claim should address only the corresponding seat/work edge; exact claim rectangles and runtime claim wiring belong to the integrating parent. There are four static fixture seats, with no invented live team or occupancy data.

## Provenance and reproduction

- Guide: `guides/workbench-geometry.png` and native diagram
- Exact first prompt: `source/workbench-prompt.txt`
- Exact correction prompt: `source/workbench-orientation-refine-prompt.txt`
- Original first attempt: `source/workbench-master-attempt-01.png`
- Final transparent master: `source/workbench-master.png`
- Built-in imagegen was used for both generation calls; no paid external API was used.
- `tools/make_guide.py` creates technical geometry diagrams only.
- `tools/package_assets.py` trims transparent padding and registers the master with premultiplied LANCZOS resizing, copies unchanged chairs, composes proofs and checks routes.
- `tools/verify_integrity.py` checks provenance and overlay pixel identity.

This package does not edit the engine, publish anything, set live claims or assert multiplayer/runtime acceptance.
