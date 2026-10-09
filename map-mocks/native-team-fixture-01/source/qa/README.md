# Native workstation runtime proof

This isolated 512 × 384 Phaser 3.86.0 + Arcade harness validates two native workstations. It does not run the complete Universe application and does not demonstrate multiplayer, seat claiming, live audio/video, or a new sit API.

## Final result

The actual cloud-browser run passed all 15 assertions. Both seats were physically approached from the rear, stopped by desk tile collisions at player center y = 192, and exited back to y = 272. Greg retained the unchanged 32 × 32 source frames, scale 1, and the source 16 × 16 body at `(cx − 8, cy)`. The north-facing occupied frame is 10. The left contact x value differed from 192 only by floating-point roundoff (`191.99999999999977`).

The 64 px rear aisle, west bypass, north bypass, and east bypass were traversed. All 635 recorded motion samples were clear of desk overlap. The chair-back image remained at world origin `(0, 0)`, above the player throughout. No runtime errors were recorded.

One stationary native Greg is a scale fixture. It switches seats only between the independent left-seat and right-seat cases. There are two avatars total. Both seats are occupied in the seated captures; aisle traversal uses one stationary occupant and one moving player. A third avatar walking behind two occupied seats and multiplayer collision behavior are not claimed.

## Deliverables

- `results/final-occupied-native-1x.png`: authoritative 512 × 384 actual game canvas
- `results/final-occupied-native-2x.png`: exact nearest-neighbor diagnostic enlargement
- `results/final-occupied-tight-1x.png`: 240 × 160 crop, world rect `(128, 112, 240, 160)`
- `results/final-occupied-tight-2x.png`: exact nearest-neighbor 480 × 320 crop enlargement
- `results/occupied-left-*` and `results/occupied-right-*`: each physical desk-contact checkpoint
- `results/rear-aisle-*` and `results/side-bypass-return-*`: circulation checkpoints
- `results/physical-entry-exit-motion.webm`: 21.095 second actual canvas recording, 512 × 384 VP9, approximately 30 fps
- `results/runtime-verification.json`: assertions, recorded motion, engine coordinates, collision events, fixture changes and scope
- `results/runtime-pixel-audit.json`: protected-head and torso comparison of actual rendered pixels
- `results/source-integrity.json`: SHA-256 evidence that Phaser, source body primitives, Greg, art and licenses are byte-identical copies

## Implementation and reproduction

Start `python3 ../universe-native-team-fixture/qa/server.py --port 8821` and open `http://127.0.0.1:8821/qa/` in the cloud browser. The server binds only to `127.0.0.1`, serves this fixture directory, and accepts bounded PNG, WebM and JSON reports only under `qa/results/`. It was copied from the previous project's loopback server, with only this output directory and default port adapted.

Click **Run physical route + record** with the tab visible. Reload to reset before another full run. Arrow keys or WASD permit manual movement. Captures are taken directly from the game canvas; the 2x outputs only enlarge those pixels with nearest-neighbor sampling.

The desk layer contains eight colliding 32 × 32 tiles: columns 5–6 and 8–9, rows 4–5. This exactly implements desks `(160,128,64,64)` and `(256,128,64,64)`. It uses actual Arcade tile collisions, preserving the source `configureBody` behavior including immovability. The furniture image is below the player; the genuine full shaped back masks are fixed above. No chair blocker or programmable sitting transition is present.

The first local adapter attempt used immovable static zones, which did not separate an already-immovable source player. That failed attempt is preserved in `results/failed-zone-adapter-verification.json` and `results/failed-zone-adapter-motion.webm`. It was replaced by the native tile-collision route; engine code, source body behavior, artwork and prior projects were not modified.

Only files inside this `qa` directory were created or changed for this validation.
