# Azure Pavilion independent review — revised café candidate

Reviewer: non-author agent; actual isolated BAWES v0.3.8 runtime, engine commit 274114560c5ec95fdf8e51e67986a53069f3cf06. No map or engine source edited by reviewer.

Status: bounded furniture/visual/motion checks pass. Full corridor sweep and final popup-anchor reload remain gates pending their results.

Reviewed loaded TMJ SHA256: 7d93cd30ae0d778b66bfa72435a84b33f324c825094f4926c802087105870259. Author subsequently changed popup anchor x coordinates only; current disk TMJ 2e230066591c211bbe13934baff4db6d300e3f0265aaafa51e71aa21faa0fa3d. Controller d4117788765d3d42830c9f2bc492e741ed8186c8d169e6c491ca7a71b1e344df and café art fb117e29927f69e010e1aecc2d29d4e6c041f5bc3c683e631fe0f64407370be0 unchanged.

## Actual independent gameplay

All 13 targets were occupied through the real native Settings → Take nearest seat menu. All arrived at intended coordinates, facing south (native direction2), with camera zoom1 and avatar scale1. Ten chairs exit via ordinary down-key movement. Each settee position moves sideways; supplemental settled test proves full exit from x600,y216 via left to584,216 then down to584,336 around the coffee table. No lock or pose simulation. Evidence: seats.json, seat-0.png through seat-12.png, settee-exit.json/png. Original six chair cushions have a small roughly7px left offset at native grid-fit positions; occupancy is visibly on cushion and acceptable, not exact pixel centering. New café chairs and settee are well aligned. All seat screenshots visually reviewed; avatar remains visible and chair backs remain behind it.

All six tables received settled approaches and actual650ms keyboard pushes from all four sides (24 tests). All blocked the avatar before traversing the tabletop. Repaired lower overlook table now blocks correctly. All24 screenshots visually inspected. Café medallion edge is somewhat conservative north of table but does not eliminate circulation. Coffee table blocks directly in front of settee; leave around either side. Evidence: tables.json, table-0-* through table-5-* screenshots, props.cjs.

## Visual and motion assessment

Revised café art passes direction: substantial lounge seating and café islands address prior empty appearance, while preserving broad marble circulation. Ocean/balcony, cream-and-brass architecture, teal upholstery and planting read coherently at native zoom. Interior roof cutaway leaves the character visible; outside screenshots show glass roof restored. Art has not been rescaled by runtime.

Continuous native runtime capture: fountain-motion-8s.mp4 (139 captured frames across8.4567 seconds; timestamp-preserving encode at15fps). Initial camera finishes its approach before settling. Sequential stationary-view frames60/64/68 visibly show bright droplets moving down side streams and changing ripple rings. This is visible stylized fountain flow, not merely a frame-count claim. The overlay is brighter and simpler than painted art, but visually integrated with its basin and spout. Ocean/background caustics remain static; do not describe the entire water surface as animated.

Author audio evidence separately reviewed: audio-results.json and styled-sound-popup.png. Actual Play click gives nonzero captured master output; actual Stop gives zero output persisting after movement; six crossings do not prompt. This is author-executed runtime evidence, not independent physical-speaker listening. Final anchor placement reload remains author gate.

## Remaining gate

Run the full maximal corridor traversal checks and final popup-anchor reload. Independent sweep52..103 is in progress in routes/results.json, using actual keyboard and native rightclick both directions. Native pathfinding only positions the avatar before each test. Reviewer harness waits for actual settled arrival after roof-induced replan and uses bounded keyboard presses to avoid CDP timing overshoot. Initial overshoot diagnostic is retained separately; it is not counted as a passing traversal.
