# Olive Academy live repair r6

Current candidate: maps/olive-academy-live-repair-r6. The final/olive-academy-context-r5b directory and inputs/academy are immutable historical rebuild inputs, not current test recommendations.

## Repairs
- Preserve all 30 approved classroom/cushion seats, seat targets and WAM configuration.
- Separate floor painting from foreground; cap genuine foreground olive foliage at alpha 96/255 so avatars retain at least 62.35% visibility.
- Retain natural underlying trunks, canopies, planters and their solid collision footprints.
- Complete lounge stone corner piers and make low walls start at their native32 blocking boundaries.
- Give the classroom's formerly floor-like blue south boundary a continuous visible stone low wall.
- Open 15 genuinely clear paving cells at the southeast corner and behind the olive trees.

## Rebuild and checks
Python 3, Pillow, NumPy and Node.js are required. No network, credentials or generation calls are used during rebuild.

1. python tools/build_live_repair.py
2. node tools/verify_native_routes.cjs maps/olive-academy-live-repair-r6
3. python tools/check_head_geometry.py maps/olive-academy-live-repair-r6
4. python tools/prove_live_repair.py

check_head_geometry.py reports all reachable alpha>32 overlap including deliberately translucent foliage. DEPTH-REPAIR-CHECK.json additionally measures actual maximum alpha across the complete frozen native head geometry; it must report zero opaque head conflicts and a maximum of 96.

The generated pillar reference is frozen in source-assets/lounge-pillar-generated.png. It was generated with the built-in image tool from the accepted original pillar crop, then integrated only into the corner pier footprint. Its accompanying prompt is in source-assets/PILLAR-PROVENANCE.md. Frozen r6-proof-actors.png is a composed scene of native reference avatar placements; no raw avatar sprite sheet is included or used by the runtime.

Static proof images decode the actual TMJ atlas, insert native32 reference actors, then composite the actual foreground. They are not live browser, keyboard physics, device or multi-user tests. Publication remains gated on independent review.
