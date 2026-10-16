# Independent review of first actual local runtime route pass

Reviewed parent-generated runtime screenshots and routes.json without taking over or interrupting the browser. This is independent visual review of actual engine outputs, not an independent traversal yet.

## Positive evidence

- Upper central-bed north/east/south endpoints show a visible Woka on paved paths; prior opaque ground-over-avatar defect is absent there.
- Terrace chair approaches and all four lower pavilion chair approaches show Woka on paving immediately in front of chairs, at consistent native scale. These are standing approaches, not seated poses.
- All four sides of the lower tree loop, fountain cardinal routes, upper/middle/lower connector, southern/southwestern connections and return to spawn show visible avatar placement on natural paving.
- Lower pavilion roof removes inside. Counter screenshot shows retained Brew tea prompt; guide screenshot shows retained Walk to fountain.
- Recorded camera zoom and player scale are consistently 1 at successful checkpoints.

## Failures requiring repair/retest

- Upper pavilion entry, all four upper chair approaches and upper counter reported No path found; their images do not prove successful access.
- Upper pavilion exit and initial terrace approach were cancelled before arrival.
- Lower pavilion exit target reported No path found. Southeast connection cancelled at (1360,1642.9); screenshot places the avatar against the right shrub/stair edge.
- Fountain-north Woka overlaps the top painted fountain ornament slightly, since fountain art is ground depth. This is not the former invisible-avatar defect but remains a minor layering limitation.
- `.popups` DOM count=1 cannot alone prove unwanted audio prompts; viewed water-route screenshots show no audio prompt, while tea and guide prompts are intentional.

## Conservative water-streak coordinates

Pixel bounds measured against the full existing composite, suitable for transparent overlays confined to painted water (world pixels):

- Upper major falls: x1248–1264,y240–298; x1322–1338,y244–303; x1407–1420,y282–339.
- Smaller upper fall: x1114–1133,y288–329.
- Lower central fountain upper spout: x772–784,y1340–1378.
- Lower fountain left spill: x738–752,y1392–1445.
- Lower fountain right spill: x800–815,y1390–1445.
- Lower fountain ripple area: x724–846,y1440–1470, center approximately (780,1454).

Keep streaks off the central stone pedestal. Static screenshots cannot establish visible motion; new continuous actual-runtime footage and visual review are still necessary.

## Replan-aware follow-up and clarified seating

The first-pass cancellation results above are superseded where the follow-up harness waited for eventual arrival. `seats.log` now confirms upper pavilion entry, all four upper chair targets, terrace targets, lower pavilion exit at corrected floor target (1328,1616), and lower stairs (1328,1680) arrive. An initial moveTo cancelled result during roof visibility replanning is not sufficient evidence of failed traversal.

User clarified seating as native occupancy/facing/back layering, not a dedicated seated pose. Detailed visual assessment of closer targets:

- u1 and u3: chair-seat alignment good; facing from path arrival needs normalization toward table.
- u2 at (264,250): clearly to right of painted chair; occupancy fails visual review. Alternative lower-row target(252,264) puts avatar too far in front of chair and is not an improvement.
- u4 at (456,250): right-shifted relative to chair; marginal/fail pending registration/placement review. Lower-row target(448,264) likewise stands in front.
- t1: natural seat overlap. t2: right-edge overlap, prefer a few pixels left if native body fitting permits.
- l1 and l2: seat alignment good; facing should be toward table.
- l3 initially targeted blocked x1376 cell. Adjusted target in left chair tile visibly passes occupancy and facing toward table (`seat-l3-adjust.png`).
- l4 at native-fit x1448: right-edge overlap; suggested target x1432 in the actual chair column before considering artwork changes.

These are screenshot assessments of real local runtime, not this reviewer's own input-driven gameplay pass yet. A command that uses supported moveTo with a short outside approach and final movement toward the table can provide consistent native seating/facing without introducing a pose or movement freeze.
