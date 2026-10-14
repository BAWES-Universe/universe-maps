# Rebuild olive-arabic-academy-woven-lounges-r4

Requires Python3 with Pillow and numpy, plus Node.js. Run:

python tools/build_environments.py academy
node tools/verify_native_routes.cjs olive-arabic-academy-woven-lounges-r4
python tools/check_head_geometry.py olive-arabic-academy-woven-lounges-r4

For the exact native property schema validation install Zod from the standard npm registry, then run node tools/verify_meetings.cjs olive-arabic-academy-woven-lounges-r4. Alternatively set ZOD_MODULE to an existing installed Zod module path. The pinned schema source is tools/native-fixture/map-editor-types.ts. No map engine change, network service, secret or image generation is required. Runtime output is olive-arabic-academy-woven-lounges-r4/map32.

The cushions and table are detailed original built-in generated transparent sprites, prepared by tools/prepare_lounge_assets.py and placed at native32 scale by tools/build_environments.py. No stand-in chair backs or foreground head cutouts are used. Live multiplayer and conferencing need separate deployment testing.
