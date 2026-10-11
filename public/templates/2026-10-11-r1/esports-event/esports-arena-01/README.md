# Circuit Arena — esports event template

A new contemporary native32 venue: two opposing team pods, a separate caster/presentation platform, short spectator banks with clear sightlines, and a useful arrival, check-in, coffee and social area. The charcoal concrete, steel shell, task chairs, desks and broadcast furniture are newly generated project artwork, distinct from the earlier ornate auditorium family.

## Review in this order

1. `review/OVERVIEW-occupied-50percent.png` — whole venue, explicitly reduced to 50%.
2. `review/COMPILED-native32-west-team.png` — exact native team-pod art, desk distance and lower backrests.
3. `review/COMPILED-native32-caster.png` — separate display, broadcast desk and presentation space.
4. `review/COMPILED-native32-spectator.png` — 24 native spectator seats, central aisle and row spacing.
5. `review/COMPILED-native32-arrival-social.png` — coffee and two casual pairs.
6. `review/CHAIRBACK-DEPTH-native32.png` — empty, actor-only and safe foreground comparison.
7. `review/COUNTER-DEPTH-native32.png` — corrected staff/counter depth before and after.

These are offline raster reconstructions of the actual compiled TMJ and PNG atlases with unchanged 32px QA actors. They are not browser or device screenshots. QA actors are absent from runtime.

## What is included

- A 2048 × 1472 map: 64 × 46 native32 tiles; unchanged avatar scale and 16 × 16 body convention.
- 12 team positions in two separate six-seat pods; 24 spectator seats; two caster positions; four casual sofa seats; check-in and coffee service positions. These are geometry counts, not a concurrency promise.
- Real steel wall pods with 96px south openings and readable perimeter routes. Spectator banks leave a broad central sightline to the caster/display platform.
- Two separately named native Video call rooms; one speaker/podium and one audience/listener area. Role rectangles do not overlap.
- A single transparent noncolliding silent tile layer on just four arrival tiles. Social seating and all meetings remain outside it.
- Real `map32/esports-arena.tmj`, companion `map32/esports-arena.wam`, two art atlases, collision/quiet marker PNGs, source masters/prompts, scale manifest, rebuild tools and evidence.

The display is a blank decorative event display. There are no live scores, game integrations, purchases, portals, external destinations, audio streams, roof scripts or camera scripts. The platform is decorative depth on a single collision plane, not true multiheight physics.

## Verified locally

- 1,959,977 reachable body-clear integer positions: zero upper-head foreground conflicts using all 12 Greg v3 head masks.
- All 2,138 walkable cells connected; all 56 anchors body-clear, head-clear and reachable.
- All 1,089 conservative WAM spawn samples safe and silent; no social anchors in quiet tiles.
- 1,628 actual-source route legs, 2,649,618 movement samples and 2,616 native area-boundary membership checks: zero body collisions, head conflicts, unintended team rooms, loops or native fitted-endpoint errors.
- 127 exact native-anchor, area, role, silence and isolation checks passed.
- All 38 north task-chair backrests restore at least 252 lower-body alpha pixels at occupied anchors while covering zero upper-head pixels.
- Both service-counter staff anchors hide278 lower-body pixels behind the counter while covering zero upper-head pixels. Visitors remain completely unobstructed. The empty map composition, physics, anchors and communication areas are unchanged by this bounded depth correction.
- Actual pinned-source WAM schema passes. Both runtime atlases reconstruct their source layers pixel-exactly, and occupied compiled renders match source compositions.

Engine evidence is pinned to `60e7afdc3f96ef32525597cd46bd41175d61a2ef`. No engine changes were made. This does not validate a particular deployed build, browser rendering, live media, device behavior, multi-user concurrency or performance.

## Setup and rebuild

Read `integration/ROOM-SETUP.md` before use. Loading a Custom TMJ does not automatically import the adjacent companion WAM. No room has been created and no media setup is live.

To rebuild using the included final native assets:

    python tools/build_arena.py
    python tools/compile_runtime.py
    python tools/verify_runtime_geometry.py
    python tools/render_compiled.py
    node validation/route-proof/route-audit.cjs
    node validation/route-proof/check-contract.cjs

`tools/prepare_final_assets.py` can reproduce selected native assets from included generation masters and the scale manifest. Python requires Pillow and NumPy. The route proof uses its included pinned source fixture and EasyStar without an engine checkout. The additional pinned source/schema provenance check requires the inspected engine checkout noted in that script; its successful report and official JSON schema are also included.

Status: refined local template frozen for independent QA; source checks passed. Not published or configured live. Earlier rejected and revised samples remain for traceability; only `map32/` is the runtime package. The complete pre-refinement checkpoint is retained separately under `checkpoints/pre-apron-refinement/`. The refinement removed six native rows from the south apron, grouped arrival services into two architectural alcoves and added matching caster/perimeter structural depth.
