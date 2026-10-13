# Lantern Souk Bazaar - fountain motion r6

Based on the approved r5 panorama/seating map, which remains untouched. Native Tiled animation now moves the basin surface, falling streams and spreading ripples: 26 animated 32px cells, 8 frames at 140ms, 1.12-second repeating loop. Approximately 13,600 basin pixels move in each frame. Every pixel outside the water mask, the central stone bowl, lantern, outer rim and market artwork are preserved.

## Runtime
Serve the complete map32 folder together. The TMJ remains named lantern-souk-bazaar-r5.tmj and its companion WAM is unchanged; use this variant in a separate review room. Custom TMJ does not automatically import WAM. Native Tiled animation needs no map script or engine change. Collision, anchors, quiet/spawn, areas, map properties and existing layers are unchanged. No audio/media/bot/payment/service configuration is added.

## Validation
Actual pinned phaser-animated-tiles 2.0.2 with Phaser3.86 Tiled parser sees all eight frames on every animated cell. Its Phaser scene is a test double, not a live browser. The unchanged native movement methods replay all 1,318 source routes while animation runs, checking collisions and area membership. Zero mapChanged events. Atlas-rendered review frames use actual plugin-selected IDs, and all pixels outside the water mask compare byte-exact. The GIF uses a common palette to avoid background flicker.

## Rebuild
Extract source ZIP, then run from its root:
python motion-tools/build_fountain.py
node motion-tools/validate_native_motion.cjs lantern-souk-bazaar-r5-fountain-motion
python motion-tools/render_fountain.py
python motion-tools/package_motion.py
Requires Python3/Pillow/NumPy and Node, no network or paid service. Source bundles approved static runtime/geometry/composited review input plus reproducible native frame code. The full original art source remains in the separately delivered static r5 source ZIP. Raw third-party Woka sheets are not included; the approved occupied game-scene proof is reused.

No live room, browser renderer, keyboard/device, audio or real multi-user test is claimed. Nothing is published or installed. Static r5 remains the fallback.
