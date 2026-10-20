# Focused composition pass — 2026-10-18

This pass preserves the corrected 2144×592 masonry footprint, exterior campus arrangement and native Woka/furniture scale. It addresses the rejected repeated desk grid and generic library treatment. Visual acceptance remains pending.

## Purposeful areas and circulation

- Two team neighborhoods each have three individual desks and one shared four-place project table. Their rugs group related work, and a 128px clear cross-route separates the teams.
- The upper-right area is an **open shared lounge**, with two sofa/coffee settings. It has no privacy or lock claim.
- Only the two lower meeting rooms are enclosed, each with four places and a courtesy lock. These are not private audio rooms or security boundaries.
- Reception sits beside the 192px entrance spine, with the beverage table toward the lounge. Neither occupies the arrival route.
- Red/amber woven rugs echo the tower palette. Repeated shelf bands are reduced to one lounge bookcase and the existing small room panels. The original illuminated stone accents remain reused artwork; this is not a new bespoke interior art set.

## Interaction mechanisms

The pinned client's existing `WA.room.showLayer` / `hideLayer` and `WA.ui.displayActionMessage` support the interactions. No engine change is involved. The map-source search found no reusable smoke/steam sprite or behavior. The beverage effect therefore uses three tiny procedural translucent stroke frames, created in the compiler, rather than paid assets or an image-generation service. It runs only after an explicit “Brew a warm drink” action, lasts five seconds and hides on movement/departure. Reduced-motion disables it. This is a local visual effect, not a shared drinks service or work-activity detector.

Entrance leaves reuse the existing glass sprite at closed, three intermediate and fully open positions. The first time-series test caught iframe timers batching and skipping a frame. The corrected implementation schedules each step only after the previous step, with cancellation on reversal. Browser timer throttling can make the effect stepped/slow; no claim of a smooth engine animation is made. Collision opens immediately for approach and only closes when the last closing frame is reached; reversal cancels the older sequence. This preserves safe approach and exit.

## Actual-client visual evidence

- [Current interior](runtime-full-interior.png)
- Identical camera: [exterior](footprint-exterior.png) / [interior](footprint-interior.png)
- [Native workstation close-up](runtime-native-interior.png)
- [Enclosed meeting close-up](project-room-close.png)
- [Full campus](runtime-campus-exterior.png)
- [Entrance interaction capture](gate-interaction.mp4)
- [Beverage interaction capture](beverage-interaction.mp4)
- [Furniture bounds and clearances](furniture-clearances.svg)

The clips are timed sequences of actual-client screenshots. The gate time-series JSON separately records visible states sampled in the client. Captures do not establish aesthetic acceptance. Landscape softness, oversized decorative plants and non-navigable illustrated upper storeys remain unchanged limitations.

No deployment, merge, paid generation, Azure work or modification of existing maps.

## Functional evidence

The actual-client gate timeline observes all three intermediate positions before fully open. Normal exit restores the façade and completes closure. The beverage action observes all three steam frames, then stops; a separate reduced-motion check suppresses the effect. Desktop and touch chair interaction pass in the revised layout. Two-client checks cover the enclosed room lock, outsider blocking, safe occupant exit and admission after unlock. The fixed-camera roof pair preserves camera and avatar coordinates.

A final clearance review removed two planters from the route between team areas, leaving its full 128px width unobstructed. The static footprint audit finds no interior furniture or layer spill. The 27 recomposed interior seats passed actual-client interaction checks; the final planter removal changes no seat position or interaction. All 75 campus seats and eight route waypoints remain connected. Optimizer equivalence preserves pixels, tile properties, layer order and runtime bytes. These checks support the supplied visual evidence; aesthetic acceptance is still open.
