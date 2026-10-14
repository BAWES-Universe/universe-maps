# Astral Concourse — Local Lobby Candidate 01

A separate native32 shared arrival lobby for the approved magical multi-hall conference/esports venue. This continues the reviewed visual concept into a local functional map candidate. The frozen Flagship and campus were not changed.

## Deliverables

- `map32/astral-concourse-lobby.tmj`: finite orthogonal 36 × 28 map, 1152 × 896 px, 32 px world tiles.
- `map32/astral-concourse-lobby.wam`: companion WAM v2 with quiet areas and a default arrival region.
- `map32/*.png`: complete local native32 runtime atlases.
- `review/lobby-runtime-review.png`: final overview rendered from compiled map layers, shown at 1 image pixel per world pixel.
- `review/lobby-runtime-occupied-native.png`: native 1152 × 896 runtime composition with original 32 × 32 Woka reference frames.
- `review/lobby-collision-native.png`: collision overlay and tested landmark anchors.
- `source/`, `assets/`, `tools/`, `validation/`: preserved masters, explicit geometry, reproducible build and source-matched offline evidence.

## Implemented locally

South arrival, reception and clearly sample directory/program boards; open central circulation; north Flagship approach; west Forum and east Arena approaches; peripheral planted social furniture. The room has no stage or audience banks.

The art is segmented into actual below-actor and above-actor source layers around authored architecture/furniture geometry. Conservative native32 collisions protect reception, boards, palms, pillars, social furniture and walls. The two layers reconstruct the original runtime art exactly. Original avatar frames remain 32 × 32, scale 1.

Default south arrival and the main foyer have mirrored native TMJ/WAM quiet regions. The north central circulation is also quiet. Social interior standing anchors are outside map-imposed silence; the inclusive lower boundary of those areas is quiet. Social furniture is solid scenery, with no custom seating controller. No ambience, embedded media, custom script, broadcast or teleport was added.

## Verified offline

- All 253 walkable cells connect to arrival.
- All 10 landmark anchors are reachable and body/head clear.
- 4,574 source-matched movement legs pass: nine practical floor-click points per walkable cell, both directions, plus portal/reception/social landmarks.
- Zero head conflicts across 236,257 reachable body-clear integer placements, using the union of all 12 original Greg/Woka upper-head masks.
- All 4,225 nominal zero-inset default WAM spawn positions are body/head clear and quiet. A conservative 131-position numerical fringe also passes, for 4,356 positions in total.
- Named WAM and native TMJ start areas use a 16 px inset; their 1,089 nominal positions and 1,156-position conservative fringe are quiet.
- 47/47 pinned current-engine schema, migration and quiet-start contract checks pass.
- Compiled native32 atlas layers reproduce authored source pixels exactly.
- Every portal approach is reachable; portal bodies remain blocked; all exit-target properties are absent.

The movement adapter is matched to engine commit `75666c0ccae779515b6fcbd83446ebd1eee29d1b`, with source-default speed 9 and a 60 Hz plus 0.5 px swept check. A deployed environment can override speed. Same-cell exact-click behavior is not claimed; the exhaustive route test uses an alternate approach origin for the spawn cell. Actors are not dynamic obstacles in this pathfinder.

## Integration limits

This is a local candidate, not an active Universe room. No live browser playthrough, keyboard/touch/mobile acceptance, multi-user rendering, proximity/media, load/capacity or room-transition check was performed.

Keep all `map32/` files together. Tiled can inspect the TMJ directly. The companion WAM is a validated authored configuration; it is not automatically installed by uploading a raw TMJ. The current Universe custom-TMJ room flow creates its own map-storage WAM with empty areas/entities. Authored WAM areas must be integrated into that actual room WAM before relying on its WAM behavior.

Flagship is visibly LINK PENDING. Forum and Arena are visibly UNAVAILABLE. No `exitUrl` or deprecated `exitSceneUrl` is present, even as an empty placeholder. A raw published TMJ/WAM URL is not a verified Universe room destination. Future binding requires a verified `/@/universe/world/room` URL and reviewed authored WAM integration. Legacy `/_/` fallback links must not be invented. See `docs/integration-gate.md`.

Quiet geometry does not prove initial socket/media timing, force a saved busy/silent status to change, or relocate returning users. Saved `initPosition` overrides default starts. No live all-audio-silence guarantee is made.

## Preserve and rebuild

The built-in imagegen master remains unchanged in `source/lobby-architecture-master.png` (1422 × 1106). The complete prompt, supplied reference artwork, original Woka sheet, reviewed concept PNG/SVG and original concept archive are retained. `docs/original-concept-readme.md` documents that earlier review-only checkpoint. The original `SOURCE-CHECKPOINT.json` belongs to that historical concept archive; `RUNTIME-CHECKPOINT.json` is the current full package freeze.

The architectural master is rendered once into a 1152 × 896 native32 canvas. Physical status plaques are authored SVG elements. Geometry and depth masks are generated from explicit source rectangles plus the native actor/head safety model, rather than treated as a flat image-only map. No flagship art or runtime files were edited.

Dependencies: Node.js with `sharp`; Python 3 with Pillow and NumPy. The pinned WAM validator includes its local Zod dependency.

From this directory:

1. `node tools/build-runtime-art.mjs`
2. `python3 tools/build-lobby.py`
3. `python3 tools/verify-lobby-geometry.py`
4. `node tools/test-lobby-routes.mjs`
5. `node tools/verify_lobby_contract.mjs`
6. `python3 tools/verify-lobby-package.py`
7. `node tools/render-runtime-review.mjs`

The generated master is the reproducible visual checkpoint. Re-running imagegen from the saved prompt is stochastic; rebuilding from the preserved master and source is deterministic apart from timestamped reports.
