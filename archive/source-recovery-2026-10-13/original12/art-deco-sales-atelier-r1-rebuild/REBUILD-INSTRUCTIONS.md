# Rebuild Art Deco Sales Atelier

This archive is self-contained. Install Python3, Pillow and NumPy (requirements.txt), plus Node.js for native route tests.

1. From this archive root: python tools/build_environments.py sales
2. node tools/verify_native_routes.cjs art-deco-sales-atelier
3. python tools/check_head_geometry.py art-deco-sales-atelier

The rebuilt runtime is art-deco-sales-atelier/map32. Compare it with reference/map32. Host the complete runtime folder together. Use this named target; the other template's art is intentionally omitted. All original required art, fonts and pinned unmodified native movement fixtures are included. No API, network, paid account, credential or generation is needed. Reviews are static compiled-atlas renders; live room and media behavior has not been tested.
