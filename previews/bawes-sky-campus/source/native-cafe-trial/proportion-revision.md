# Response to independent visual review of cc62f45

This revision is not visually accepted yet. All corrections remain isolated here; primary campus and engine source are unchanged.

## Measured scale

`native-measurements.json` records a live Woka frame of32×32, origin0.5/0.5, scale1, and16×16 collision body offset(0,8), camera zoom1. Source theater canvases were48×64 with approximately48×48 visible chairs. Actual native artwork bounds, not2× browser screenshot dimensions, guide corrections. Approximate hand-inspected bounds are labeled as such.

## Raster iterations

Only built-in image editing produced revised artwork. All images remain1536×1024 with no whole-image resampling. References are direct TMJ exports. Sources and rejected/intermediate outcomes are retained.

- Café pass1 reduced lounges but left stools too tall and added two chairs. Pass2 explicitly halved stool legs, lowered the counter and removed those extra chairs. Integrated source: `cafe-proportion-2.png`.
- Theater pass1 reduced all32 chair backs while retaining banks and aisles. Integrated source: `stage-proportion-1.png`. Returned chair positions differ slightly from requested coordinates; depth masks and anchors follow actual art.
- Conservatory pass1 centered the table and refined muddy west-bridge stone. Pass2 barely reduced the sofa despite exact dimensions. Pass3 used an explicit half-size instruction; returned a substantially smaller sofa/table. Integrated source: `nook-proportion-3.png`.

## Seating capabilities

The pinned client exposes32px standing/idle/walk sprites, native R-key rotation and public map movement events/moveTo. Its public player API does not expose a seated pose or direct facing setter. Candidate-local `seat-runtime.js` uses a short directional approach via public moveTo after arrival, with cancellation respected; no engine source or avatar scale changes. Original cutaway/door runtime is copied unchanged, then the candidate-only seating behavior is appended.

New foreground masks place upper bodies above the smaller rear theater backs and align low cushion/stool edges to actual artwork. Tests record final native direction, seat positions and screenshots; passing those checks does not establish a physically bent sitting animation.

## Validation in progress

`proportion-review/` holds new captures and checks. Prior `whole-map/` results belong to cc62f45 and must not be substituted for this revision. Independent screenshot review is required after the run.
