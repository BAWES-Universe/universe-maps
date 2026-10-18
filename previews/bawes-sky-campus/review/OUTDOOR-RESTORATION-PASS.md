# Conservatory, stage and cafe correction pass

This candidate continues from `6a7caef` without generation, deployment or accepted-interior changes. It remains subject to visual review; the cafe is not marked finished.

## Conservatory alcove

The prior flattened lower west table is replaced by a bounded stone conversation bowl within reference `(60,366)-(182,444)`. Source coordinates remain `world=(1792+3*x,2048+3*y)`. The aligned native patch is `(1968,3136,384,256)`; the actual clear-floor trace excludes the current northern planters, left pillar, front lamps/railing and southeast flower bed. Existing pixels outside that trace are preserved.

The construction has individually jointed curved cap stones, a textured outer side face, a darker18px inner wall, a lowered illustrated inner floor, and three shaded eastern treads. Near cap/face and retained foreground objects are separate from the floor and render above players. Collision closes the bowl perimeter and allows entry through the64px eastern stair opening. This is illustrated depth in the existing2D engine, not a new elevation mechanic.

A144px matching curve has three native anchors32px apart on its cushions; a uniformly scaled48px table sits inside the bowl. The northern landing setting and its existing stair connection remain. See `alcove-registration.json`, `alcove-ground.png`, `conservatory-restored.png` and `district-occupied-conservatory-lounge.png`.

## Stage audience

Complete front/rear timber armchair views from the coordinated cafe sheet were material-adapted to a walnut/tobacco palette. Alpha, frames, slats, joints, full legs and luminance detail are preserved; red/cream upholstery and bright brass no longer form the banks. This is an adaptation, not a claim of exact extraction of the tiny reference chairs. No cream bench or small red-dot substitute is used.

Two4×4 banks use48px chair artwork at64px pitch. The left bank begins5504, the right5856; the clear central aisle is112px. The left bank moved32px inward to keep the narrowing western edge clear. Contact shadows sit beneath chairs; lower timber backs render above occupants. All32 anchors face the stage at Woka32 scale1. The existing warm stage floor, steps, canopy and planted boundary are retained as source pixels. `stage-restored.png` and `district-occupied-audience.png` show actual client views.

The original small microphone has not been restored. The existing stage desk remains at its prior checkpoint; a matched independently placed microphone/podium prop would be needed if that original detail is required. It is outside the audience-bank restoration performed here.

## Cafe corrections and remaining blocker

Two compact table groups replace the widely separated outward lounges: each has a144px curve with two cushion anchors, a nearby64px cup table and an inward-facing matching armchair. Curves moved toward the planted/back edge; their anchors move from48px down the old sprite to32px down the new sprite. Source-derived lower edges provide occupancy overlap. The standing-sprite engine limitation remains; these are not bent-leg seated animations.

The former narrow western strip is no longer designated as a circulation route. Access is east of the left group and west of the right group. Measured clear vertical spans at y4352 are144px at x2504/2568/2600 and160–176px at x2760/2888. A six-cell (96px) swept-square connectivity check also passes from (2848,4320) to (2560,4352). Lantern collision now follows its physical stone pedestal at y4416; its raised head remains foreground artwork, allowing walkers behind it. The pedestal foot remains blocked. Pond, railing and cliff boundaries were not removed to gain that space. See `cafe-clearance.json`. Native pointer/facing checks and approach tests are recorded in `cafe-runtime-checks.json`.

Board joints are less contrasty and staggered; native material has small per-board variation. Contact shading is confined to the trace boundary, and upper foreground floor fringes are trimmed further. No blanket blur was applied. The inherited blurred scenery still differs in sharpness from native furniture/boards, and the upper bar-to-deck joins remain a visual review item.

The oversized counter is **not fixed**. Its countertop/body/props are baked into the scene above and outside the approved deck mask. A smaller counter would reveal unknown background; the alternate cafe candidate still contains its own large counter and shifted perspective, so it is not a clean removal plate. Exact bounded needs are in `source/cafe-candidates/counter-adaptation-blocker.json`: a registered clean background for current source `(198,688)-(390,744)` (world2386,4112,576,168), preserving canopy supports/shelves, plus a separate matching counter assembly that can be calibrated to320–384px width,40–48px body height and native32 occupants. These are target calibration dimensions, not generated or validated assets. No source was invented to conceal the blocker.

## Checks

`geometry.json` covers all72 connected anchors. `district-runtime-checks.json` covers changed audience/conservatory seats, facing, stairs and district/aisle routes. `cafe-runtime-checks.json` covers the regrouped cafe. `cafe-preservation.json` verifies unchanged accepted interior pixels/collision/runtime and scenic source images. `optimizer-equivalence.json` compares the final optimized map with source. Full-campus evidence is `runtime-campus-outdoor-restored.png`.

The stage route harness initially stopped short during long cross-campus navigation. Reissuing the same route after settling reached the stage apron and floor, then all three audience aisles. The harness now allows two settled retries; this is not reported as a single uninterrupted traversal. All 35 new seat clicks passed independently, with exact anchors and native facing.
