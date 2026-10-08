# Lantern Courtyard · layered animated proof

A 24×18 map on a 32px grid (768×576), revised for original native-scale furnishings, real alpha foliage, grounded collision footprints, water/light animation and a covered alcove reveal.

## Status

This is a local, tested map candidate. It has not been published, deployed, or accepted in a full Universe room. No remote repository or live room was changed for this revision.

The included motion preview was recorded in a focused local Phaser3.86.0 harness using source-extracted Universe depth, layer and body primitives and the fork's pinned animated-tiles plugin. It is not a recording of the complete Universe app. The documented full development setup requires Docker, which was unavailable in this environment. Production script-sandbox integration, hosting/CORS, real Universe keyboard/right-click/touch controls, role permissions and server persistence remain acceptance checks.

## Choose an entry

- `lantern-courtyard.tmj`: self-contained static tile-map variant. It contains all table/chair/plant visuals, with separately authored upper/foot layers and an independent collision mask. This is the candidate for a simple public TMJ URL.
- `lantern-courtyard-editable.tmj` + `lantern-courtyard-editable.wam`: optional true whole-object Y-sorted variant. The WAM supplies11 entities: one low table, four olive trees and six small chairs. Its TMJ omits those static objects to avoid duplicates. It uses4 prefab definitions in `collections/courtyard-furniture.json`.

Pasting a TMJ URL into Universe Admin does not automatically load a neighboring WAM. Admin may create a fresh canonical WAM with empty entities. An authorized operator must import/carry the editable data into the actual room's canonical WAM. Back up a canonical WAM before using room update flows, which can regenerate it and discard edits.

The WAM's absolute collection/map URLs are bound to the verified repository base `https://bawes-universe.github.io/universe-maps/lantern-courtyard/`. The new folder is a future publication path, not evidence of live hosting. Do not treat these paths as working links until publication and fetch/CORS checks succeed. If another host is chosen, update both absolute WAM URLs together; the collection's PNG paths stay relative to the collection.

## What changed

- Four freestanding olive/pot silhouettes are separate transparent sprites. The clean ground no longer contains ghost copies. Internal leaf gaps have real alpha.
- Only support cells collide. Leaves/upper table art do not block movement. The arch opening is clear.
- The low tea table was redrawn at56×23 visible pixels in a64×64 cell. Each small chair uses28×27 visible pixels in a32×64 cell. Greg's accepted32px sprite was not modified. Chairs are scenery; no sitting function is claimed.
- The two oversized upholstered sofas were removed together with their oversized arched backs and raised seat platforms. Modest wall tile bands now sit behind three small chairs in each bay.
- Upper sprites and lower support pixels have separate static layers. Optional WAM objects use one genuine ground-contact threshold for their complete alpha image, using the authored rear-contact plane for furniture and actual pot ground contact for trees, with shadow/padding excluded. Static tile splitting is not generic dynamic Y sorting and should be checked at diagonal approaches in the target room.
- The western alcove roof hides on entering and returns on leaving. Roof posts remain visible, and permanent support collision never hides. Initial position, re-entry and unload are handled.
- Eight synchronized water frames create restrained ripples; eight warm-light frames illuminate nearby tiles and pool reflections. Existing butterflies flutter in the gathering zone.
- Reduced motion uses steady warm light and hides water/flicker/butterfly animation. A preference change during the session is handled.
- The optional gathering camera pan preserves the user's zoom. It occurs only after a confirmed wide viewport event; unknown/narrow views stay in player-follow. Exit restores follow once. A shrinking viewport or side panel immediately restores follow if the camera was locked. There is no popup or player-control lock.

The large olive canopies, sandstone architecture and entry arch are intentionally architectural. This is not the separate enormous-door cinematic concept.

## Files

- TMJ/WAM, `collections/`, `images/`, `tilesets/`, and plain `scripts/courtyard.js`: runtime dependencies
- `validate.mjs`: offline structural and script lifecycle tests (`node validate.mjs`)
- `validation/`: actual local results and precise test scope
- `preview.png`: local rendered view with unchanged Greg, not a live-room screenshot
- `ART-PROVENANCE.txt`, `LICENSE.assets.txt`, `SOURCES.txt`: provenance and reference notices

No build step, framework import, online service, audio/video service or map-added tracking is required by the map script.

## Verified locally

Both entries pass the unmodified pinned Universe MapValidator and WAM/collection schemas. Structural checks cover dimensions, GIDs, paths, animation frames, entity/static footprint parity, all184 walkable cells connected, and4 clear spawn cells. Script tests cover repeated entry/exit, reload inside each area, delayed initial position, unload-before-init, reduced motion at startup and during play, narrow/unknown viewport safety and camera restoration.

Focused browser physics checks use the fork's16×16 foot body at offset(0,8), avatar depth centerY+16, before/after-floorLayer depth construction, and whole-entity depth formula. See the JSON results for exact tested cases. Those checks do not certify full-game import or networking.

## Real Universe acceptance before calling this ready

1. Publish only after authorization, into a new isolated directory/room. ZIP upload can replace/delete that selected directory's contents; never select an existing room or the root without a reviewed backup.
2. Confirm every TMJ/WAM/PNG/script/collection URL returns the intended asset with required CORS.
3. Join with Greg at native scale. Test keyboard, right-click pathfinding and touch around all table/chair/pot sides and diagonal corners. Confirm canopy overlap and alpha gaps at real zoom.
4. Enter/leave/re-enter the alcove and gathering; reload inside each. Check roof posts and collision remain, animations stay aligned, and the camera returns safely.
5. Check a narrow portrait viewport, side panels, and reduced motion before and during play.
6. For the WAM variant, test authorized object movement/reload persistence and visitor restrictions. No edit permission is granted by this package.

Keep the ordinary32px collision-grid margins in mind around irregular art. If those margins feel wrong in the real game, revise the asset/contact plane or footprint rather than scaling Greg.


## Maps-repository build / draft-PR workflow

The proposed repository path is `public/lantern-courtyard/` in `BAWES-Universe/universe-maps`. Its existing Vite build copies this folder unchanged. From that repository root, run:

```sh
node public/lantern-courtyard/validate.mjs
npm run build
```

Compare every file in `public/lantern-courtyard/` against its matching `dist/lantern-courtyard/` file; they must be byte-identical. The final future standalone URL is `https://bawes-universe.github.io/universe-maps/lantern-courtyard/lantern-courtyard.tmj`. This is a planned publication path, not a currently hosted-map claim. A draft PR does not merge or deploy it. Keep the motion MP4 as a separate review attachment rather than a required map dependency.
