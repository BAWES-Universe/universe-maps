# Rebuild and verify r3

Dependencies: Python 3, Pillow, NumPy and SciPy. The compact source is self-contained for art construction, native32 compilation, occupied proof reconstruction and the fresh r3 checks. No network, paid generation, raw engine code or raw character sheets are needed.

From the extracted source root, run:

python tools/rebuild.py

This rebuilds the six straight mats from the unchanged retained concept, reapplies the unchanged bounded nook-door repair, compiles and decodes the native map, checks geometry/scenery/startup/nook coverage, reconstructs the hash-pinned r2 baseline, verifies the exact r3 mat-only delta, and checks EXPECTED-OUTPUTS.json. Generated runtime files appear in timber-mixed-six-mat-instructor-facing-r3/.

## Individual steps

1. python tools/reorient_source_mats.py
2. python tools/repair_runtime_doorways.py
3. python tools/build_native32.py
4. python tools/check_geometry.py timber-mixed-six-mat-instructor-facing-r3
5. python tools/check_scenery.py
6. python tools/check_spawn_outcomes.py
7. python tools/check_room_floors.py
8. python tools/check_r3_correction.py
9. Copy geometry-checks/timber-mixed-six-mat-instructor-facing-r3/independent-checks.json to timber-mixed-six-mat-instructor-facing-r3/HEAD-GEOMETRY.json.
10. Copy evidence/r2-accepted/NATIVE-ROUTES.json to timber-mixed-six-mat-instructor-facing-r3/NATIVE-ROUTES.json.
11. python tools/verify_expected.py

## What is fresh and what is inherited

Fresh r3 checks cover exact source-to-atlas reconstruction, zero changes outside the six mat neighborhoods, all twelve unchanged prop sprites/positions, straight parallel edges, 102-cell connectivity, all 22 anchors, exhaustive body/head geometry, the four recorded startup outcomes, and six existing actual native arrival bodies fully contained on the new mat surfaces.

The full TMJ, WAM, layout, foreground and spawn inputs remain byte-for-byte identical to r2. R3-MAT-CORRECTION.json verifies this against the accepted r2 hashes. Stable r2 media-role IDs in WAM are intentional.

NATIVE-ROUTES.json is inherited r2 evidence from the pinned, unmodified extracted PathfindingManager, Player and GameScene.moveTo at engine commit 60e7afdc3f96ef32525597cd46bd41175d61a2ef with EasyStar 0.4.4. Its original TMJ and layout hashes still match the r3 files exactly. It records 3,810 routes, 2,898,558 body samples and no body-collision samples. The engine was not re-executed for r3. Repeating the native engine replay requires the separately licensed pinned fixture, which is deliberately omitted from this compact source. No browser, keyboard, touch, live media or deployment test is claimed.

## Accepted r2 baseline

check_r3_correction.py uses the same transformer with --orientation r2 in a temporary directory, then compiles it and requires 18 accepted r2 output hashes to match before making any preservation claims. It compares the full-resolution mat surface/contact-shadow alpha support, the exact native resampling support, six separate native neighborhood rectangles, and the existing native arrival records. This avoids distributing a second flattened room or an engine fixture.

## Character and startup proof inputs

source-assets/occupied-proof-overlay.png and native-head-union.json are frozen reproducible proof inputs. WOKA-PROOF.json records the eleven original source sheets, hashes, frame numbers and positions. Raw character sheets and preparation code are not distributed. Runtime atlases contain no characters. See ASSET-PROVENANCE.md and licenses/.

source-assets/native-spawn-outcomes.json records the actual r2 StartPositionCalculator and MathUtils execution at zero, midpoint and the two nearest-one random values. Its four distinct observed positions are checked against the current unchanged collision and quiet layer. The fresh check asserts that the start rectangle still matches this capture exactly; it does not claim a new JavaScript execution.
