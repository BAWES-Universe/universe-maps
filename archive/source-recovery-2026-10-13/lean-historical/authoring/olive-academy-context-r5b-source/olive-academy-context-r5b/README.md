# Olive Academy context r5b

The accepted woven-lounge Academy with 192 px of northern olive-garden context. A visible closed cedar garden gate now ends the northern path. The path opens only eight conservative cells (global columns31-32, rows5-8), fixing the inherited invisible stop. Adjacent walls, pillars and garden remain blocked. A new gate-approach anchor is reachable from spawn.

All accepted interior artwork remains pixel-exact at Y+192. Existing seats, targets and WAM properties are preserved. Intentional courtyard tree-canopy occlusion is unchanged; no new head conflicts. Runtime is48x38 tiles at32px. Host the complete map32 directory. No engine changes, publication or active service integration.

Rebuild: python tools/build_contexts.py academy
Verify: node tools/verify_native_routes.cjs maps/olive-academy-context-r5b
Head geometry: python tools/check_head_geometry.py maps/olive-academy-context-r5b

Python3, Pillow, NumPy and Node.js required. Frozen strips and source layers make the runtime rebuild deterministic with no generation call or network. Raw avatar sheets are excluded; proof images are static composites, not live playtests. Browser/device and multi-user media remain untested.
