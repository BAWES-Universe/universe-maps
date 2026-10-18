# Current compositing review — 2026-10-18

Recovered the saved workspace rather than rebuilding the concept. Recovery commit: `9c9f38ac5a5bf69005cef051db05adec34bfd860`. The earlier checkpoint and refinement reports are historical.

The exterior floor slab and duplicate baked office are removed. The cleaned façade retains its aspect ratio (1509×652 source crop →2240×968), anchored at the front threshold y=3104. Structural pixels are opaque; actual pane apertures reveal clipped native interior imagery and live occupants. The complete 2240×1440 floor and 128px service perimeter appear only in the client-local cutaway. Registration is recorded in `source/registration.json`.

Background audience seats, oversized terrace benches and café furniture were removed from the retained island arrangement. Native furniture supplies those usable spaces, including conservatory tables and plaza/pergola sofas. Woka scale remains 1 with native32 frames; accepted desk/chair sizes are unchanged.

Actual client evidence:
- [Exterior campus](runtime-campus-exterior.png)
- [Full local cutaway](runtime-full-interior.png)
- [Native desk and chair](runtime-native-interior.png)
- [Indoor occupant through glass](runtime-registered-glass.png)
- [Conservatory seating](runtime-native-west-terrace.png)
- [Plaza sofa](runtime-native-plaza-lounge.png)

Geometry confirms 23,834 connected walkable cells, all nine waypoints and all 84 seat anchors reachable. The isolated native16 optimizer passes pixel/property equivalence, layer-order/dimension checks and runtime script byte equality. Client checks and their precise scopes are recorded in the adjacent JSON files. The all-seat interaction sweep uses camera/player placement near each seat, then real pointer input; end-to-end campus routes are checked separately. Camera checks use supported zoom controls and explicit boundary placements, not a claim about unrestricted Explore panning.

Visual review: the single façade, warm amber/red identity, conservatory/stage arrangement, lower café and portal garden remain recognizable against the approved source. Window evidence now visibly includes an indoor avatar; the old planter-obscured capture was insufficient. The complete cutaway is visible in its current capture.

Remaining limitations: landscape artwork is softer than the native furniture at close zoom, some decorative plants are oversized relative to Wokas, and the intentionally exposed cutaway/service perimeter still reads as a large rectangle. This is a review candidate, not visual acceptance or a production-ready claim. The building has one navigable floor; upper façade imagery is not another storey. Courtesy locks are ephemeral and do not establish private audio or access security. No StudentHub integration, destination, engine change, paid service, public preview publication or deployment was added.

The mobile north-edge capture has a thin horizontal rendering line that remains a visual review issue. Camera-only placements bypass movement events, so their cover state is not an entrance/cutaway test; normal entry and exit are checked separately. The old cliff assertion used y=3232; current map collision begins at y=3312 at x=3096, and a longer keyboard approach stops at y=3296.
