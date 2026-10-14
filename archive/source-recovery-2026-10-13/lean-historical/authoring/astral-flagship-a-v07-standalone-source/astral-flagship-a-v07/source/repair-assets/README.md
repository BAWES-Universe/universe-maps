# Flagship A: bounded native furniture and reception benchmark

## Decision

Reuse the accepted lounge-chair family at its existing native resolution. Put casual companions side by side at 56 px centers, with an unobstructed principal escape route. Use the native north-facing chair for the view-facing placements. The two small pavilion tables are deliberately removed so the center entrance remains clear. No architectural, floor, stage, meeting-seat or garden expansion is included here.

The reception source is one newly generated coherent wide counter, reduced once from its transparent master to 192×51 px. The master produced a wider/shallow silhouette than the requested approximate 192×72 target; its aspect ratio is preserved instead of distorting it or enlarging the old 112×68 raster. The inspected result is the selected source candidate.

## Review first

- `review/corrective-a-before-after-native-1x.png`: primary occupied BEFORE/AFTER benchmark. Every source art pixel is shown 1:1. This is a bounded composition, not a runtime screenshot.
- `review/corrective-a-before-after-2x-nearest.png`: separately labeled nearest-neighbor inspection view only.
- `review/geometry-proof-native.png`: dimensions, 16×16 body and 32×32 visual-clearance checks, and approach routes. Annotation colors are not runtime art.
- `review/six-pair-components-native-1x.png`: all six source placement candidates occupied at native scale, displayed on a common existing floor swatch for asset comparison. It is not a floor-change proposal.

The first direct chair comparison uses a south-facing pair so the cushion/arm improvement is easy to see. The actual six-pair contract uses north-facing native variants toward the intended foyer/garden view; all copied chair images remain byte-identical to the accepted source family.

## Integration contract

`source/six-pair-placement-contract.json` is the authoritative component-only handoff. It contains all 19 removed object IDs, twelve seat anchors and floorClick points, exact native-art origins, collision footprints, per-placement foreground rules and matching above/below images, four low-table positions, two deliberate table omissions, and the reception component.

Do not copy a generic full-width foreground strip between locations. Each above image is the intersection of source alpha with a narrow safe area derived from that location's collision tile. Its complement stays below actors, preserving the original pixels exactly.

### Reception

- Native asset: `assets/reception-counter-native-192x51.png`
- World art: `[960,1549,192,51]`
- Collision: `[960,1568,192,32]`, entirely within the visible counter bounds; no north padding
- Depth partitions: `assets/reception-counter-below.png` and `assets/reception-counter-above.png`
- Foreground rectangle before alpha intersection: `[968,1552,1144,1584]` XYXY
- Staff: `(1048,1551)`, facing south
- Visitor: `(1048,1600)`, facing north
- East return: 64 px; staff allowance: 64 px; customer apron: 96 px
- The two service points are 49 px apart, within the specified56px ordinary-proximity target. This is a two-player position candidate only; no new meeting area or live communication guarantee is added.
- Native tap-fit is exact: staff floorClick `(1048,1567)` and visitor floorClick `(1048,1616)`. The visitor body begins exactly below the counter collision at y1600. Its32px sprite extends16px over the front fascia, which is intentionally below actors. The counter above mask ends at y1584 exclusive, where the visitor sprite begins, so no head pixels are hidden. This is normal depth, not a full32px bounding-box clearance claim. A full-box-clear tap-fitted alternative is anchor `(1048,1632)` / floorClick `(1048,1648)`.
- A separate code-authored RECEPTION fascia overlay is at `[977,1583,56,10]`; layer its `nameplate-below` and `nameplate-above` partitions with the counter partitions. Counter scale and compass ornament are unchanged.
- Remove both the old left welcome object and its old WELCOME label. Keep the main central arrival corridor open.

### Pair centers

| Pair | Center | Adjustment | Table |
|---|---:|---|---|
| Indoor casual | 1264,1583 | Original anchor positions retained; face north | Northeast at 1312,1532; clear of the citrus tree |
| Terrace view | 2256,1223 | 27 px south for a clear north/view apron | East at 2400,1244 |
| Terrace lower | 1776,1607 | 7 px south for fitted native north-chair depth | East at 1920,1628 |
| Terrace garden | 2224,1607 | 7 px south for fitted native north-chair depth | West at 2016,1628 |
| Pavilion 1 | 2068,231 | 4 px east, 7 px south | Removed |
| Pavilion 2 | 2284,231 | 4 px west, 7 px south | Removed |

All twelve casual seats use 56 px within-pair spacing. Pavilion center entry stays `[2144,144,64,208]`. The accepted 210 hall seats, 16 meeting seats, rugs, stage and map/garden connections are outside this change contract.

## Evidence and limits

- Initial reception/direct-chair benchmark: 89,582 body-clear integer placements checked, zero upper-head conflicts across all twelve frames of the original Greg32 fixture.
- Final six-pair contract: 235,684 bounded body-clear integer placements checked, zero upper-head conflicts; 2,714 approach-route samples pass both the 16×16 body and full 32×32 visual-box collision check.
- All twelve casual anchor positions are body-clear and full-box visually clear. All twelve floorClick targets reproduce their authored anchors under the verified native fit function (body16, X offset0, Y offset8).
- These are static source/component checks. Full integrated TMJ pathfinding, final art compositing, full-map head checks, runtime camera behavior and live playtesting remain separate requirements.
- No frozen source, TMJ, WAM, or runtime map was changed. `source/frozen-input-verification.json` checks every entry in the original v05 freeze manifest.

## Source and rebuild

The one built-in image-generation prompt and full transparent source are saved under `source/imagegen-prompt-reception.txt` and `source/reception-counter-generated-master.png`. `PROVENANCE.json` records generation, source hashes and unchanged native asset copies. No paid external media service was used.

Run `python source/build_benchmark.py` and then `python source/build_placement_contract.py` to reproduce the selected benchmark and placement contract from the frozen v03/v05 inputs plus saved counter master. Earlier `seating-benchmark-*` review files are the first bounded chair proof, retained for comparison only.
