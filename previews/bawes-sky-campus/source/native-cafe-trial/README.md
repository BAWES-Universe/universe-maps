# Registered native café / bridge pilot — unfinished visual candidate

This controlled candidate is separate from the primary `campus.tmj`. It proves that 1536×1024 native panels can be generated and assembled without enlargement. It does **not** finish the whole-map request or meet final café visual acceptance.

## Sources and registration

- `registered-reference.png`: direct native-pixel export from playable base `851a243`, at world [1984,3712,1536,1024]. No resampling.
- `restored-native.png`: built-in image edit of that reference; returned 1536×1024. Prompt fixed camera, silhouette, bridge edges and 32px Woka furniture dimensions (144px sofa, 64px table, 48px armchair, 32px stool).
- `east-reference.png`: adjoining map export at [3264,3712,1536,1024], with the completed café panel's 256px overlap supplied at the left. `east-restored-native.png` returned 1536×1024.
- `south-reference.png`: adjoining export at [1984,4480,1536,1024], with the café panel's 256px overlap at the top. `south-restored-native.png` returned 1536×1024.

Shared specification: same orthographic game camera, cream stone, gold/glass framing, turquoise water, illustrated foliage, warm upper-left daylight, fixed routes and silhouettes. Prompts requested identical overlap pixels. The generator did not satisfy exact pixel retention: east overlap mean absolute RGB difference 5.47/255, 98.86% of pixels changed. Inspection of `bridge-join-detail.png` and `south-join-detail.png` found the principal contours continuous enough for this isolated gameplay trial. This is a visual judgement, not exact pixel equivalence.

`build-candidate.py` joins at world x3392 and y4608 using hard cuts in the overlaps, with no enlargement, feathering or blur. It writes only `playable/` and trial artifacts. The original map, source builder, assets and runtime remain untouched. Foreground masks are reused provisionally against the new scenery; their final accuracy still needs review. The generated TMJ references the original assets and runtime by relative paths; keep this folder inside its repository for reproduction.

## Actual gameplay evidence

The local pinned Universe client loaded `playable/campus.tmj`. The completed `runtime-checks.json` contains 36/36 successful checks: square and bridge approach, café circulation, ten café seat right-click approaches and exits, and return to the front plaza. Camera zoom and avatar scale remained 1. Captures include `runtime-cafe.png`, `runtime-bridge-join.png`, `runtime-square.png` and `runtime-seat-51.png` through `runtime-seat-60.png`.

The first click test failed because the leftmost seat was outside the viewport, not because movement had been established to fail. Its evidence remains `runtime-first-checks.json` and `runtime-failure.png`. The corrected test approaches within the viewport before clicking; it completed before the environment restart. Those saved results survived, but the temporary console log and local runtime processes did not. Do not describe them as a new post-restart run.

## Remaining visual work — do not propagate as accepted

The main scene is visibly clearer at normal gameplay scale, and both inspected internal joins are continuous. However, the inherited counter remains too large relative to a 32px Woka and the stools remain separated from it. Rectangular timber variations/ghost contours are still visible in the floor. Furniture/foreground registration is provisional, including seat facing on arrival. The outer edges still meet unreworked scenery; upper-left conservatory and other campus regions are not corrected. No whole-map visual acceptance is claimed from the 36 functional checks.

Next: correct the counter and stool relationship and floor artifacts within this complete native region, then inspect actual seated/standing views and masks. Extend only after that visual proof, using the same fixed shared coordinates and native panel approach. Preserve accepted office, gate, island arrangement and clear routes. No paid services, engine changes, merge or deployment.

## Counter/floor correction milestone

The candidate now uses `counter-floor-edit-2.png`: a compact horizontal bar, four stools close to its front and a continuous timber deck without the former rectangular ghost patches. The first edit reduced the bar but moved stools unevenly; the second used a horizontal counter and evenly spaced row. The generator did not obey every requested coordinate, so actual painted anchors were measured and registered instead of claiming exact prompt compliance.

The four bar anchors are now in `candidate-layout.json`. Only the front-of-counter collision strip [2512,4192,416,80] is released to match visible floor; all other original collision cells, accepted interior, gate and spawn remain unchanged. A first foreground placement hid too much of the Woka. The final mask/anchor adjustment keeps the head and upper torso visible, demonstrated by `runtime-seat-57.png` through `runtime-seat-60.png`. It does not add a sitting animation or automatic facing.

The corrected counter passed a fresh 18/18 approach, right-click seating, exit and return-route check in `bar-corrected-checks.json`. The earlier 36-check record belongs to the intermediate correction before the final mask adjustment, and is not final visual acceptance. `runtime-cafe.png` and the final bar captures were inspected. The primary campus map is still untouched.

Two native conservatory panels have also been generated and inspected as sources. They replace the pasted oval with a continuous stone recess and restore the roof at native resolution. They are not yet integrated or gameplay-validated at this milestone. Broader front-plaza, stage and portal correction work is in progress.
