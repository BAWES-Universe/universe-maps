# Rebuild and verify

Dependencies: Python 3, Pillow, NumPy and SciPy. The compact source archive is self-contained for art construction, native32 compilation, varied occupied proof reconstruction, authored geometry and scenery checks. No network, paid generation or engine changes are needed.

From the extracted source root:

1. python tools/reorient_source_mats.py
2. python tools/repair_runtime_doorways.py
3. python tools/build_native32.py
4. python tools/check_geometry.py timber-mixed-six-mat-instructor-facing-r2
5. python tools/check_scenery.py
6. python tools/check_spawn_outcomes.py
7. python tools/check_room_floors.py
8. Copy geometry-checks/timber-mixed-six-mat-instructor-facing-r2/independent-checks.json to timber-mixed-six-mat-instructor-facing-r2/HEAD-GEOMETRY.json if packaging the generated evidence.
9. python tools/verify_expected.py

EXPECTED-OUTPUTS.json pins the runtime, atlas, layer sources, layout, empty/occupied images and authored evidence. The geometry checker writes to geometry-checks/ rather than silently replacing a frozen evidence file. evidence/ contains the separately retained final run reports.

## Native route replay boundary

NATIVE-ROUTES.json records replay with the pinned, unmodified extracted PathfindingManager, Player and GameScene.moveTo at engine commit 60e7afdc3f96ef32525597cd46bd41175d61a2ef and EasyStar 0.4.4. This optional extracted engine fixture and runner are deliberately omitted from the compact source archive. Repeating native engine replay requires that separately licensed, pinned fixture. This does not limit self-contained map rebuilding, atlas decoding, pixel geometry or scenery checks.

## Character proofs

Frozen occupied-proof-overlay.png and native-head-union.json are the reproducible proof inputs. WOKA-PROOF.json records the eleven source sheets, hashes, frame numbers and positions. Raw character sheets and the local-only proof preparation helper are not distributed. Runtime atlases contain no characters. See ASSET-PROVENANCE.md and licenses/.

## Actual startup rounding gate

source-assets/native-spawn-outcomes.json records the actual repository StartPositionCalculator and MathUtils execution at zero, midpoint and the two nearest-one random values. The four observed positions are checked against current collision and the quiet layer by check_spawn_outcomes.py. Native route evidence also replays every target, every walkable cell, both full nook traversals and quiet returns from all four positions. Re-capturing these engine outcomes requires the separately licensed pinned repository; the compact source rebuild uses the frozen, source-hashed capture and asserts its start rectangle still matches exactly.
