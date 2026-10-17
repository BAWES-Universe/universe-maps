# Review evidence — 2026-10-17

Status: runnable local review candidate; owner visual acceptance pending. No production deployment, Azure changes, merge, existing-map edits or engine patch.

## Actual checks

- `geometry.json`: 22,852 connected walkable cells, all nine named destinations connected, all 74 seat anchors reachable, all tileset files present, native16 layer dimensions consistent. This is a graph check, not 74 separate avatar visits.
- `runtime-checks.json`: 15 actual-client checks for native outdoor spawn, desktop/touch chair entry and exit, meeting entry, locked-room safe exit, front/rear exits and six outdoor routes. The route pass preceded the final café scenery cleanup and stage lectern; affected café/stage behavior was rerun below.
- `multiclient-checks.json`: six two-client checks: shared lock, blocked outsider, safe owner exit, unlocked entry, client-local roof state and a remotely visible indoor occupant. State changes in this suite use the iframe API; microphone/camera remained disabled. This is not a live audio isolation test.
- `final-checks.json`: seven checks after the final café cleanup/stage lectern: wall collision while roof hidden, cliff keyboard collision, stage platform, audience chair, café route, café chair entry/exit.
- `camera-checks.json`: actual desktop1440×900 and touch430×900 camera worldViews at four boundary walkable cells, after five sequential supported 0.8 zoom operations. Camera-only placement was used to isolate coverage; it is not a walk test. Screenshots include the actual client UI. The earlier single-step camera rows were superseded by this suite.
- TypeScript `tsc`: passed. Map compiler and standalone ZIP integrity: passed.
- Repository Vite optimizer: **failed for this candidate** (`Accept only 32 tile size`), with ten existing maps succeeding. The raw native16 TMJ and pages load in the pinned client. The direct ZIP intentionally bypasses this optimizer; it is not evidence that the repository build passes.

Runtime: BAWES Universe `274114560c5ec95fdf8e51e67986a53069f3cf06`; Chromium with software rendering; Node22 from the saved toolchain. Tests are under `source/validation/`. Local server uses map8090, game8000, Vite8080 and CDP9222. Synthetic test users only.

## Camera extent and limits

World:8192×7168. Walkable bounds: x1952..6256, y1536..4592. Painted margins: left1952, right1936, top1536, bottom2576 pixels. Final camera anchors are north(4024,1536), south(5688,4576), west(1960,3280), east(6248,3312), chosen from actual collision-free boundary cells.

At five completed zoom-out steps the desktop worldView is about2197×1373; mobile is about1312×2747. Read exact x/y and final zoom from camera-checks.json. All four views stay inside the painted map. Avatar scale remains1. Camera zoom alone is not a reliable physical scale report because this engine also resizes its canvas.

Whole-map fitting has an unavoidable aspect-ratio limit: the world ratio is1.143, versus1.6 desktop and0.478 mobile. Fitting the entire world requires blank side margins on desktop or top/bottom margins on mobile unless cropping is accepted. Explore permits panning outside the finite map. Added scenery therefore covers the measured normal/five-step views, not arbitrary Explore panning or unlimited zoom. No engine restriction was introduced to hide that limit.

## Failures found and corrected

The initial stage edge had no walking connection; its native floor opening was added. Repeating paving-border samples were replaced. Separate tiny café paving patches were rejected during visual inspection; a whole-scene cleanup now supplies continuous native furniture space. The office initially looked like a floating rectangular sheet; a separate cliff foundation and continuous bridge were added. Stretched side foliage was removed.

The first rear-exit approach left the door shut: both office exits now remain open to inside occupants. Visibility changes caused repeated active-path endpoint shifts on the16px grid: cutaway changes and door closing now wait until movement stops. Doors can open during approach. This map-level mitigation means the roof reveal occurs when the player stops inside, not continuously on the first boundary pixel.

## Review limits

The main office is one continuous navigable floor, despite its tall architectural cover. The façade interprets the approved folded BAWES identity rather than tracing the vector mark exactly. Outside lower glazing is translucent; upper cover pixels remain opaque. Reference scenery is enlarged3× and is visibly softer than separately authored native furniture. Western conservatory and perimeter decorative furniture remain part of the illustration, not individually usable native furniture. Owner review must judge this mixed detail level and the office's enlarged footprint.

No real StudentHub URL, portal destination, private audio zones or meeting service is configured. The right wing and rooms provide usable shared-campus space; these integrations need real destination/configuration details. Meeting locks are ephemeral courtesy locks, not security. The local server disables persisted-variable validation. No separate Tiled GUI import, real mobile hardware run, audio call or independent third-party reproduction is claimed.

`campus-exterior.png` and `office-plan.png` are offline compositions. `desktop-*`, `mobile-*`, `outside-visible-occupant.png` and `inside-front-room.png` are actual-client screenshots. A screenshot proves only the recorded view, not owner visual approval.
