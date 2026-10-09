# Revision 02: compact shared workbenches

This offline draft replaces the former four corner desks with one shared 128 × 96 px workbench in each of seven team bays. Each workbench has four provisional seat/work-edge places. Growth stays empty. These are map capacity placeholders, not inferred headcounts or staff assignments.

All files in the frozen parent baseline remain byte-identical. `frozen-baseline-sha256.json` records and verifies their hashes. Existing pod positions, shared spines, gallery rooms, walls, low dividers, doors and furnishing reservations are unchanged.

## Integration files

- `source-coordinate-geometry.json`: complete revised source geometry, table and chair placement, seat/body anchors, compact claims and pending-mask warning.
- `furniture-collision-rectangles.json`: the seven exact shared table blockers plus the fourteen retained low dividers. Chairs are walkable.
- `route-manifest.json`: 41 explicit routes, tested forward and reverse.
- `claim-manifest.json` and `personal-areas.offline-draft.wam`: matching 28 unassigned 64 × 112 px claim quadrants. WAM entities and entity collections are empty.
- `geometry-validation.json`: 274 passing static geometry, containment, schema and baseline-integrity checks.
- `route-validation.json`: 82 passing directional paths and 28 table-contact checks using the unchanged 16 × 16 px body.
- `collision-grid.json`: 16px cell indices for the currently specified exact physical geometry. Receiver/cabinet masks are absent pending final assembly.

## Exact table collision rectangles

All rectangles are half-open world-pixel `(x, y, width, height)` values relative to the main office's upper-left corner:

| Team | Table collision |
|---|---|
| Operations | (176, 208, 128, 96) |
| Recruitment | (656, 208, 128, 96) |
| Sales | (1168, 208, 128, 96) |
| Tech | (1648, 208, 128, 96) |
| Design / Media | (176, 848, 128, 96) |
| Marketing | (656, 848, 128, 96) |
| Research | (1168, 848, 128, 96) |

Each table starts at pod+(112,144). It is one fixed baked fixture, unowned and non-movable. No personal plot owns the entire bench. Draw the original table and chair assets at their recorded origins without scaling, rotation or reflection.

## Seats and compact claims

For a table at `(L,T)`, the seat centers are `(L+32,T−16)` and `(L+96,T−16)`, facing south, plus `(L+32,T+96)` and `(L+96,T+96)`, facing north. Each unchanged 32 × 32 Woka has its body at center+`[-8,0,16,16]`. The north bodies touch the table's north edge; south bodies touch its south edge. A one-pixel move toward the table is blocked at each seat.

The four 64 × 112 plots are:

- North west: `(L,T−64,64,112)`
- North east: `(L+64,T−64,64,112)`
- South west: `(L,T+48,64,112)`
- South east: `(L+64,T+48,64,112)`

They touch at boundaries and never overlap. Each contains its own full 48 × 64 chair canvas and player body. Each addresses one seat and the nearest work-edge quadrant. The whole fixed table and combined furniture canvas deliberately cross multiple plots, which is valid here because neither is a movable WAM entity.

The first bay's plots are `(176,144,64,112)`, `(240,144,64,112)`, `(176,256,64,112)` and `(240,256,64,112)`.

All owners remain null. `allowedTags: []` is an offline schema placeholder, not an approved audience policy; the verified source claim prompt treats it as any logged-in user. Neither TMJ guide objects nor a neighboring WAM file activate claims. Live WAM routing, effective claim permissions and persistence still require separate verification.

## Required map packaging

Use actual 16 × 16 px TMJ cells for this revision: 152 × 84 cells preserve the full 2432 × 1344 px office/gallery envelope. The table origins have 16px offsets, so rounding them to 32px cells would incorrectly block the north seats.

This changes collision-cell granularity only. Wokas remain native 32px, furniture remains native size, and every world-pixel coordinate stays unchanged. A preview-only custom static collider is not an acceptable substitute for correctly packaged map collision. `route-core.js` is reused unmodified with its supported cell-size argument set to 16.

## Route scope and remaining blocker

Every seat route enters the real bay opening and avoids the other 27 player bodies and every other personal plot. North seats use lateral approaches from their nearest side. South seats approach from below. Seven additional circulation routes pass through each bay opening and around its workbench with all four seats occupied.

These are source-geometry tests, not final assembled-room acceptance. The revised painted receiver's back and side cabinets have not yet been converted into exact pixel-aligned obstacle masks. Parent observations place the first receiver's back cabinet around y144..176 and side cabinets around x96..144 / x400..448 down to y352; these observations are deliberately not invented final collision rectangles. Final cabinet/planter/trim masks may require a route or claim adjustment.

After assembling and registering the receiver artwork, extract the actual obstacle masks, include them in the real map collision, and rerun every route. Integrate final reception/lounge/meeting footprints as well. No artwork, runtime code or live configuration was edited by this revision.

## Reproduce

Run only the scripts inside this revision directory:

1. `python build_revision.py`
2. `python verify_geometry.py`
3. `node verify_routes.cjs`

The generator reads the frozen baseline and validated `art-workbench` manifests, writes only inside `revision-02`, and fails if any frozen baseline hash changed.
