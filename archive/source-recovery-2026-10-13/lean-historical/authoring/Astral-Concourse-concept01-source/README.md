# Astral Concourse · Flagship Hall

A local, separate-map prototype for a magical multi-hall conference or esports venue. It preserves the existing campus and uses a new warm sandstone, gold and teal stage. The proposed shared arrival hub, Forum, Arena, Studios and Expo remain a masterplan; only the Flagship Hall is implemented here.

## Contents

- `map32/grand-auditorium.tmj`: native 32px Tiled map, 48 × 40 cells (1536 × 1280px)
- `map32/grand-auditorium.wam`: companion native Podium/Audience configuration
- `map32/*.png`: complete local runtime tilesets; no external texture dependency
- `source/`, `assets/`, `tools/`: source artwork, exact chair/podium pixels, registration recipe and reproducible map build
- `review/`: compiled-map overview, native 1:1 Woka composition, furniture depth and collision evidence
- `validation/`: source-level route, geometry, spawn and current-engine schema reports
- `integration/`: unbound venue linking contract and live acceptance checklist

## What is implemented

210 visible chairs: three banks × ten seats × seven rows, with 32px horizontal pitch and 64px row pitch. Woka sprites remain native 32 × 32 at scale 1. The two continuous blue aisles align with the two rear hall portals. The stage is reachable via both side stair approaches; the lectern has its own protected physical footprint. The uncluttered arrival vestibule and all possible default spawn points are silent.

Native chair backs and lectern foreground are split above/below actors. Chair outer arms remain below actors; the central lower back remains above actors. Empty-seat source pixels are preserved exactly. The native collision rows prevent walking through chair backs. This is ordinary map depth, with no snapping, custom seat controller or engine patch.

## Open correctly

Keep every file in `map32/` together under the same directory. Tiled can open the TMJ directly for inspection. For the actual native presenter/listener behavior, a compatible WorkAdventure room must load the companion WAM as its room map/configuration. The WAM resolves `./grand-auditorium.tmj` relative to itself.

A plain TMJ import is insufficient for the complete native audience/podium role pair. Do not describe this prototype as an active broadcast until its WAM is installed in the intended room and live joining is verified. The legacy TMJ carries explicit quiet-spawn geometry; it intentionally does not pretend to configure broadcast roles.

The current `universe-develop` source (commit `75666c0ccae779515b6fcbd83446ebd1eee29d1b`) contains the WAM runtime handlers and schema. Its editor Podium/Audience controls are gated by `FEATURE_FLAG_BROADCAST_AREAS`, whose source default is false. The deployment flag and available room/WAM import route have not been checked. No feature flag or engine code was changed.

## Universe Custom TMJ activation

The inspected Universe admin creates a new room-specific WAM with empty areas when a Custom TMJ room is resolved. It does not automatically import the published companion WAM. Use the actual room’s native Stage/Audience editor if its gated controls are available, or an authorized supported map-storage reconciliation route. Preserve the actual room WAM’s absolute TMJ URL and every unrelated field/area. Explicitly resubmitting or changing mapUrl in admin can reset stored areas/entities. See [the activation and backup guide](integration/universe-room-activation.md) for pinned source links, supported routes, reset precautions and exact current blockers. No live route or interface has been verified.

## Roles and audio

- Podium area ID: `astral-flagship-podium`
- Podium broadcast name: `astral-flagship-stage`
- Audience references the podium AREA ID via `speakerZoneName`
- Audience chat is disabled by configuration
- No music, waterfall, ambience, iframe or legacy Jitsi audio is added

Successfully joined native Podium/Audience roles are excluded from proximity groups by the current engine. This source fact does not prove a successful media join, no cross-room audio leakage, or zero transient bubbles during initial connection or transitions. A 48px neutral band separates stage/audience regions; the audience/quiet boundary has a 1px gap. Presenter speech is the only intended event audio.

## Verified locally

- 210/210 seat anchors are reachable, body-clear and head-clear
- 3,800 movement legs pass using the current-source-matched native path/player adapter, including nine practical floor-click points per seat in both directions, doors and both stage approaches
- All 716 walkable cells belong to the arrival-connected component
- Zero furniture/head conflicts across 554,924 reachable body-clear integer placements, tested with the union of all twelve native Greg head frames
- 1,089 inset TMJ start positions and all 4,225 nominal default-WAM positions are body/head clear and inside silence; a conservative one-pixel rounding fringe (4,356 total WAM placements) also passes
- 26/26 current-engine WAM schema, migration, reference and role-geometry checks pass
- Compiled 32px atlas pixels reconstruct both visual layers exactly

The movement harness uses source-default speed 9; the deployed environment may override it. Players are not dynamic obstacles in the native pathfinder, so this is not a guarantee that automatic routes avoid every other attendee's body. No user-capacity/load claim is made from the 210-chair count.

## Not yet verified or connected

No live browser playthrough, keyboard/touch/mobile acceptance, real multi-user renderer, media broadcast, load/capacity test, deployed feature-flag check or cross-hall sound-isolation test has been performed. No public URL, GitHub branch/PR, existing campus edit or live-world update was created.

The south doorway is an arrival/return receiver only. It has no broken placeholder exit URL. The shared hub and other halls need their own reviewed maps before their destinations are bound. Give each hall distinct podium area IDs and broadcast names; do not duplicate the Flagship broadcast identifiers across halls.

## Rebuild

Python 3 with Pillow and NumPy; Node.js for the route adapter. From this directory:

1. `python tools/register_architecture.py`
2. `python tools/build_map.py`
3. `python tools/render_final_reviews.py`
4. `python tools/verify_geometry.py`
5. `python tools/verify_spawn_silence.py map32/grand-auditorium.tmj --report validation/spawn-silence.json`
6. `node tools/test_native_routes.mjs`
7. `python tools/verify_package.py`

The current-source WAM audit is retained in `validation/current-source-audit/`; it was run independently against the exact current schema. Generated architecture is normalized and registered to authored grid regions; furniture and avatar pixels are never rescaled. Both generated masters are retained non-destructively.
