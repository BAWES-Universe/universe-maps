# Revision 03: assembled-art geometry freeze

This is the physical handoff for `tools/assemble_office_v2.py` and its current native layers. It replaces the earlier conceptual wall and low-divider geometry. All earlier geometry revisions remain unchanged.

## Authoritative compiler inputs

| File | Coordinate space |
|---|---|
| `collision-grid.json` | Full rendered canvas, translation **already applied**. 156 × 88 cells at 16px = 2496 × 1408 px. |
| `collision-grid-source.json` | Office source coordinates, 152 × 84 cells at 16px = 2432 × 1344 px. |
| `source-coordinate-geometry.json` | Office source coordinates. Add (32,32) once when rendering. |
| `checkpoint-manifest.json`, `route-manifest.json` | Office source coordinates. |
| `checkpoint-manifest-full-canvas.json`, `route-manifest-full-canvas.json` | Full rendered coordinates, translation already applied. |
| `personal-areas.offline-draft.wam` | Full rendered coordinates, translation already applied. Offline data only. |
| `claim-manifest.json` | Source-coordinate draft personal areas. |

The source and full-canvas grids were checked cell-for-cell under the exact 32px translation. The full canvas's outer margin is blocked. Do not translate `collision-grid.json` a second time.

## Accepted integration corrections

- Every entire workbench group and its four personal plots moved **32px east**. Tables now begin at pod+(144,144); Operations starts at (208,208). All original native table/chair/body relationships remain unchanged.
- Both cross-aisle guest-chair canvases moved **8px south**, to y592. Their north-facing seat center is y608, exactly at their coffee table's south edge.
- Coffee-table front pixels remain below actors. Promoting their foot/front mask above actors clipped both guest heads; removing that promotion fixed the two overlaps without changing geometry. Real chair/sofa foregrounds remain above actors.

The authoritative assembler and art manifests are hashed in the geometry file and final delivery record.

## Physical blockers

`furniture-collision-rectangles.json` contains all 75 explicit source rectangles: permanent boundaries/glass rails, receiver cabinets and movable-looking but fixed furniture. `source-coordinate-geometry.json` includes the same set as `allCollisionRectangles`.

The rear main wall blocks y0..176. The side strips, main entrance, real office/gallery doorway, gallery rails and south corridor openings follow the assembled native receiver rather than the old proposal. Southern U cabinets close the direct north approach into their furniture area; routes go around their sides and enter through the open south.

Pixel inspection added the inner lantern/bookcase elbow omitted from the initial U rectangles. Left-style receivers include the floor elbow at pod.x+80..144, y176..208 (or y816..848 in the south). Mirrored receivers place it at pod.x+272..336. These are real cabinet blockers; their geometry was retained when the bench art moved east.

Sofa source arms remain their actual 12px width. Their cells are conservatively covered in the 16px grid, with no blanket sofa rectangle. The north-facing sofa's physical rear blocker starts at canvas-local y48, separate from its elevated back artwork at y33. Every exact seat and path was verified against both the source rectangles and this conservatively packed grid. No preview-only collision substitute was used.

## Exact goals and contact sequences

There are 62 named goal anchors: 28 team seats, 26 meeting/lounge/reception positions, and 8 navigation checkpoints. The 28 workbench stations each include `approach` and `contactApproach` fields.

For north-side workbench seats, the valid approach is lateral from the clear center between the opposed pair of seats. Walk from that approach to the seat, then attempt a 1px move south toward the table. The body must remain at the specified contact anchor. A hypothetical straight approach from 32px farther north would enter the rear cabinet/wall; do not reuse that older assumption.

South-side workbench seats approach from 32px south, walk north to the seat, and stop at the table's exact edge. Meeting/cardinal contacts follow their recorded facing directions. These are unchanged directional standing frames at functional seating anchors; no sitting animation is claimed.

The routes block every other furniture/reception goal body as a conservative occupied-room fixture. Draft personal ownership areas are not physical entry restrictions. Some final paths cross unoccupied work-edge portions of another draft area while avoiding every occupied body; no privacy or access policy is implied.

## Checks

- `geometry-validation.json`: **191 passing** geometry/schema/integrity checks.
- `route-validation.json`: **122 complete source routes, 244 directional checks**, from the main entrance and reception to every other goal; **62 clear anchors** and **45 exact contact checks**.
- `foyer-seat-access-manifest.json`: **8 explicit side-entry paths, 16 directional checks**, proving entry/exit from both sides for every facing-sofa seat while all other positions are occupied. The north sofa uses the actual narrow gap beside the table; no furniture was moved or enlarged.
- `assembled-head-clearance.json`: **54 directional Woka head checks**, zero furniture-foreground overlap in every protected head region. The separate low-alpha overhead shade intentionally tints actors and is not a clipping occluder.

The Woka stays native 32 × 32 px with its unchanged 16 × 16 px body at center+(-8,0). Map collision cells are 16px. World coordinates, art dimensions and avatar scale are unchanged.

## Claims and runtime scope

All 28 compact personal plots remain unassigned 64 × 112 px seat/work-edge proposals. Fixed shared benches are baked fixtures, not WAM entities. The WAM's entities and collections are empty; owners are null. Its empty tag arrays are schema placeholders, not an approved audience policy. Some plot area includes the nearest fixed table/cabinet work edge; that does not make the fixtures movable or privately owned.

A companion WAM does not activate claims by file adjacency. Room routing, effective permissions and claim persistence need separate live verification. No live claiming, audio/video behavior, permissions or account configuration was changed here.

These results establish source geometry, packed collision and static head clearance. The compiler owns the actual runtime walk, rendering and contact verification.

## Reproduction

Run inside this directory:

1. `python build_final_geometry.py`
2. `node verify_final_routes.cjs`
3. `python verify_final_geometry.py`
4. `python verify_foyer_access.py`
5. `python verify_assembled_heads.py`

The generator reads the authoritative assembly manifest and asserts the accepted art corrections before rebuilding. The scripts write only inside revision-03. Earlier revisions and original assets are inputs only.
