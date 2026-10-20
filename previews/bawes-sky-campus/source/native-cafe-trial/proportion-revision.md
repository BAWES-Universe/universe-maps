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

The first runtime attempt failed to initialize seat behavior because a relative JSON fetch resolved against the client script iframe. The fix embeds seat coordinates in the generated candidate runtime. The next run passed70/71 checks; the side-chair56 arrival landed16px from its nominal anchor and escaped the initial12px facing trigger. The revised side-chair trigger accounts for that offset and uses a32px lateral approach. The final run writes `proportion-final/`. Sofa masks were also lowered to keep heads and torsos visible; older `proportion-review/` captures show the superseded masks.

Implementation/source milestone584c781 was pushed to the existing draft branch.

## Follow-up registration correction

The `proportion-final` run passed69/71 checks: stool57 and nook63 were captured at intermediate approach positions with incorrect facing. These failures are retained. Subsequent `sofa-final` waits longer for chained public moveTo calls before capture and repeats affected interactions.

Café sofa anchors moved from4336 to4320; nook anchors moved from3248 to3232. Low cushion masks begin10px below sprite center, preserving head/upper torso and concealing lower legs. The80px nook sofa now has two anchors32px apart; the third overlapping capacity claim was removed. No sprite scaling or artificial screenshot pose was applied.

Independent review confirms smaller theater seating with rear-facing occupants and clearer west-bridge balusters. The façade review found no remaining registration tear, floating occupant or cutout gap; material contrast with the accepted interior is stylistic, not an established geometry defect. Sofa/stool visual acceptance remains pending.
