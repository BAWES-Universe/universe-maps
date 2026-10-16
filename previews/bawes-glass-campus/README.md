# BAWES town — architecture and interaction candidate

An isolated original 96×80 campus at native 32px scale. Spawn stays beside the team tower and its near-entrance meeting room. The tower's entire 24×19 projected footprint becomes a continuous office when its shell is hidden. Coworking, staff offices and a glass portal pavilion stand behind it, separated by a connected street. Side routes lead to the StudentHub court, conversation booths, outdoor stage, staff terrace and beach promenade.

This is an architecture/layout iteration, **not a visually finished or deployed world**. Current furniture and architectural detailing are still schematic. The full tower/podium cover now masks the complete footprint outside, rather than exposing an unrelated office floor around the crown. Its retained generated facade still needs visual review alongside the newly authored buildings.

The latest arrival correction moves spawn to (22,53) and front seats into the transparent window band. A fresh paired capture is in progress; the 26-route sweep precedes that small adjustment.

## Current behavior

- Four independent full-footprint shell cutaways, with floor, furniture and permanent collision kept separate.
- Six-tile main circulation and tower entrances. 6,504 connected walkable cells, 86 statically reachable seats and six reachable portal bays.
- Native main-office front/rear door layers open on approach and remain passable for occupants leaving. A near-spawn meeting enclosure has a shared courtesy lock controlled by an explicit Apps-menu button (including the mobile profile menu). Occupants can always leave; the owner can unlock from outside. A 15-minute lease prevents an indefinitely abandoned lock. This is not authorization or audio isolation.
- Six original portal arches are ready for configuration through the **existing** area editor’s “Portal to any room”. `source/portal-areas.json` contains pixel rectangles with empty properties. These records are not installed WAM/editor areas. Destinations are deliberately unbound; no fake room URLs or new portal engine feature.
- The stage, offices and booths are useful physical places. Live event/media settings and staffing are not inferred from furnishing. No walking popups, quest triggers, background audio or conversation-disabling `silent` property.

## Evidence and reproduction

- `review/town-client-routes.json`: 26 actual-client routes covering spawn, meeting entry/seating/exit, full-height tower interior, rear street, coworking, portal bays, staff rooms/terrace, stage, beach and StudentHub.
- `review/town-doors.json`: 10 passing two-client checks covering lock action, late joining, collision, reconnect, safe exit, propagated unlock, touch lock/unlock and independent shell visibility. `review/town-crossing.json` records a separate opposing-direction doorway crossing.
- `review/static-validation.json`: all-cell connectivity, reachable seats, portal bays and four full-footprint reveal masks. Static checks do not prove native avatar overlap or visual quality for every seat.
- `review/outside.png` and `review/inside.png`: **offline full-map layer exports**. `review/town-*.png` are actual client captures. `town-overview.png` is a zoomed-out southern district view, not the complete map. `town-northern-district.png` is a zoomed-out view of the buildings behind the tower. Other captures use normal camera scale except the explicitly narrow touch-client captures.
- Retained failure evidence records the first closed-door exit/pathfinding issue and first unlock-propagation observation. It is not passing evidence.

Build with `python3 source/build.py` from this directory, then `python3 source/validate.py` and `node source/test-reveal.cjs`. The repository `npm run build` optimizes maps without deploying. Existing local runtime instructions are in `source/runtime/README.md`; the engine remains pinned to `274114560c5ec95fdf8e51e67986a53069f3cf06`.

## Source and scope

`source/REFERENCE-CONTRACTS.md` records the WA Village study, 100 Roads provenance, user-reported partnership permission and exact existing portal contracts. All candidate art/layout/code is original or the retained BAWES-generated tower source; no reference-map assets were copied. `source/ART-PROVENANCE.md` describes compilation.

The rejected facade prototype is preserved at `eeebac0`; the full-footprint geometry checkpoint is `5aaee09`. Prior `client-*`, `geometry-*`, table/door reports and historical sweep files refer to those old layouts and cannot certify this town revision. Only `town-*` and the rebuilt static report apply here.

All changes stay under `previews/bawes-glass-campus/`, on `feat/bawes-glass-campus`, draft PR #21. Existing maps, Azure and engine tracked source remain unchanged. No merge, deployment or world registration has occurred.
