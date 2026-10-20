# Initial bounded cafe restoration — 2026-10-18

The initial pass was not visually accepted as finished. See [subsequent café corrections and counter blocker](OUTDOOR-RESTORATION-PASS.md).

This pass reconstructs the timber surface inside a hand-traced mask on the existing cafe. It does not paste the unregistered ground candidate or move the pond, waterfall, bar, cliff, lamps, balustrade or bridge. No generation, engine change or deployment was used. The accepted interior at45b7535 is pixel-identical and retains identical collision and runtime script.

## Registered surface and foreground

Source-to-world transform remains `(1792+3*x, 2048+3*y)`. The native aligned patch is `(2176,4192,1120,352)`, enclosing the requested deck region `(130,720)-(480,810)`. `source/cafe-ground.py` stores the actual perimeter vertices; `registered-deck-mask.png` and `registered-foreground-mask.png` are reproducible outputs. The original current deck, not the candidate's shifted cliff or bridge, determines the mask.

Matching wood is sampled from candidate `(480,460)-(820,500)` at1:1 native detail, repeated with reflected seams and restrained board joints. No old deck pixels are enlarged to supply its detail. Timber stays inside the existing stone rim; the right stone landing remains stone.

The foreground trace covers the complete front railing and its lamp/planter/foliage silhouette. Inspection extended it left of the provisional262 bound to cover the railing at130 and foliage near224. Pale floor fringes are reduced only along the traced upper edge; the lamp core and stonework remain. The foreground copies the existing scene at exactly the existing world transform and is rendered above players. It is not a rectangular cover over the deck. The source's existing blur and bright lamp glow remain visible; the surrounding bar/scenery was deliberately not redrawn.

`cafe-registration.json` verifies no static pixel outside the timber mask changed. `cafe-preservation.json` independently verifies unchanged scenic source images, all accepted office layer pixels, office collision and runtime bytes, plus foreground placement after the player-depth marker. Replacement furniture and its source-derived foreground strips are independent of the ground mask.

## Furniture and access

Two176px curved lounges each have three occupied anchors48px apart. Two64px tables retain the source cups. Four32px bar-side stools use48×64 padded sprites; the last stool was moved16px forward to clear the retained scenic counter collision. The original oversized illustrated counter remains scenic; these are usable native stools beside it, not a newly scaled service-counter model.

The three previous unrelated outdoor sofas are replaced at their existing positions by128px matching benches with two anchors48px apart. Bench and lounge fronts use deliberate lower-edge segmentation. Wokas remain32px at scale1; native R-key rotation establishes facing. The client has no bent-leg sitting animation or automatic seat orientation.

The central/east cafe circulation has96–176px vertical clear spans at the measured4320 route. The west approach has64–80px; the far-left space behind the lounge narrows to48px and is a local seating nook, not the through route. Conservatively traced cliff margins and the foreground lamp obstacle prevent walking onto the pond or through the pillar. Actual path tests cover spawn-to-cafe, portal return, center route and left lounge approach. All71 map anchors are connected:19 interior,10 cafe,6 benches,32 audience and4 west terrace.

## Review evidence

- `cafe-full.png`: actual-client whole cafe, zoomed for context.
- `cafe-native-close.png`, `cafe-occupied-*.png`: normal client zoom and native avatar scale.
- `runtime-campus-cafe-restored.png`: actual full-campus overview.
- `cafe-runtime-checks.json`: native pointer occupancy, measured anchor positions, facing and routes. The harness starts near each seat and emits native movement; it may retry a native click after camera settling, recording click count. No teleport is used for the final occupancy action.
- `geometry.json`, `footprint-audit.json`, `optimizer-equivalence.json`: map checks.

This is a bounded reconstruction for review, not a claim that the new ground candidate was perfectly registered or that every original lounge configuration has been reproduced.
