# Rebuild Art Deco r2
Requires Python3, Pillow, NumPy and Node.js. No network or generation call is needed.

python tools/build_art_deco.py
node tools/verify_native_routes.cjs art-deco-sales-atelier-r2
python tools/check_head_geometry.py art-deco-sales-atelier-r2

The 60×40 native32 map occupies1920×1280pixels. The original interior remains1536×1024 at offset192,160. Host the whole map32 folder. map.wam offers optional native meeting areas; conferencing, editor import, browser/device and multi-user runtime were not live-tested. No integrations are active.

Source distribution intentionally omits raw avatar sheets. The exact map and all geometry can rebuild without them; fresh occupied preview generation is skipped unless authorized native Woka sheets are provided. Included occupied composites are frozen proofs from all14 real native32 actors. Runtime never includes avatar pixels.
