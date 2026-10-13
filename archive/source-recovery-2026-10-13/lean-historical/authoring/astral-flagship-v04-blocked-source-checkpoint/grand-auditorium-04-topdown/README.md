# Astral Concourse: Flagship v04

Separate native32 candidate with a top-down scenic garden, authored wall faces/cast shadows, full-room roofs, immediate room reveal and auditorium camera focus. Original v01 and published-baseline v03 are not changed.

## Runtime

`map32/grand-auditorium.tmj` is the entry map. Keep its referenced local PNG atlases and `flagship-focus.js` beside it. `grand-auditorium.wam` is a portable setup candidate, not a live room configuration.

- 210 auditorium chairs; four 4-seat lounge squares; four 2-seat casual pairs
- Same collision, quiet route, social anchors and auditorium geometry as v03
- Full roof reveal; independent decorative visibility groups
- One stage camera owner; immediate entry/exit, no per-move camera commands
- Scenery remains outside the walkable railing

Read [room setup and safe activation](integration/ROOM-SETUP.md). A Custom TMJ does not import the adjacent WAM. Back up the actual room WAM before changes; explicit map URL updates and ZIP replacement can reset stored configuration.

## Validation status: RELEASE BLOCKED

The full native-source route matrix found213 visibility-transition wrong-tile arrivals and9 baseline same-tile tap cases across8,952 legs. Collisions, unwanted meetings and loops remained zero. A full unmodified-source reproduction confirms same-tile nearest-target fallback. No map-only workaround is being applied. This is an art/source checkpoint, not an accepted playable release.

Local integration is complete enough to reproduce the blocker. Current-source checks and final native route reports are saved under `validation/`; do not infer live browser, multiplayer, media or load acceptance. Native visibility operations can replan a click path and adjust its endpoint within the intended tile. Route acceptance requires safe arrival, unchanged blockers and zero loops, not exact pointer-pixel matching.

No v04 publication or live room setup has been performed. This version requires visual review before publication.
