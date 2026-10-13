# Compact lush office module

The integration-ready module is 1536×960 native pixels, campus origin (704,64). All authored geometry/anchors are module-local, including the32px source margin. Original art and Greg remain scale1. No original files were changed, no generated art was purchased, and nothing was published.

Use `module.json` for exact layer paths, floor envelopes, permanent colliders,29 anchors,23 reversible canonical routes, native body/frame dimensions and entrance integration points. Render `office-base.png` below actors and the fixed `office-foreground.png`, `office-glass.png`, `office-overhead-shade.png` above. `collision-grid.json` is96×60 with16px cells; outside the listed walkable module floor is blocked. The two entry pads reach the southern canvas edge.

- Eight ordinary work seats: four on each side of the clear shared spine. Source Operations and Recruitment IDs are retained only as stable geometry identifiers; no people, roles, team capacity or ownership is inferred.
- Two reception service places, each with staff and visitor anchor. Staff columns160px apart; intended visitor contact48px apart. Counter uses original first and last end sections, removing the unused middle service span without any resize. Original gold/teal welcome inlay surrounds it.
- One six-seat meeting gallery, with direct public southern entrance and internal hall link.
- One welcoming three-person lounge. No rendered floor text, extra work bays, invented live services, claims or bot behavior.

Main entry opening: x480–608,y912–960; center(544,944), inside(544,880). Gallery public entry: x1088–1184,y912–960; center(1136,944), inside(1136,880). These coordinates add directly to campus(704,64).

Chair backs remain fixed foreground and obscure seated torsos. Native rear-foot blockers keep the16px-tall seat pocket clear and enforce lateral entry. Only chair pixels below the occupied32px avatar frame and the sofa's low front lip move into the furniture base; occupied appearance and all flattened furniture art remain unchanged. Sofa arms stay foreground. There are no actor-following alpha masks.

`verification.json` passes all29 anchor reachability checks,23 one-pixel approach/return routes,156108 animation/head checks plus348 anchor/frame checks,18 blocked-contact checks and four reciprocal reception acquisition/retention checks. Stationary peers use64px acquire and96px retention; work egress stays80px from other desk occupants and the shared crosslane is112px below the final work row. Meeting/lounge routes intentionally join only their own conversation group.

This verification is offline geometry and original32px Greg alpha-mask evidence; the parent campus task owns actual native runtime, tap/camera and one-scene integration verification.

Rebuild with `python build_office.py`, then `python verify_office.py`. Exact source crops, deterministic fixed-layer changes and all source hashes are in `compositing-manifest.json`. `office-overview.png` is the empty native review; `office-occupied-review.png` shows unchanged Greg at every occupied seat/service point for inspection.
