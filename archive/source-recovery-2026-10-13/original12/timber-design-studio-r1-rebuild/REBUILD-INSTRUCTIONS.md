# Rebuild timber-design-studio

This lean self-contained archive includes the frozen original environment, native furniture, compiler and unmodified pinned engine fixtures.

1. Install Python3, Pillow and NumPy (requirements.txt), plus Node.js for the movement tests.
2. From this archive root run: python tools/build_environments.py cowork
3. Verify native routes: node tools/verify_native_routes.cjs timber-design-studio
4. The rebuilt runtime is in timber-design-studio/map32. Serve this entire folder together.

Only the selected map source artwork is included; use the named build target above rather than the default all-maps target. No API, generation, network service, secret or paid account is needed to rebuild. Previews are static atlas renders. Live room/media tests remain separate.
