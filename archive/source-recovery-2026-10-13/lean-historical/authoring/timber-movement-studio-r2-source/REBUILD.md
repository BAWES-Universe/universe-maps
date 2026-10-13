# Rebuild Movement Studio r2

Requirements: Python 3 with Pillow and NumPy; Node.js.

From the extracted package root:
1. python tools/build_expansion.py
2. node tools/verify_native_routes.cjs timber-movement-studio-r2
3. python tools/check_head_geometry.py timber-movement-studio-r2

The fixed generated border and frozen accepted r1 layers/layout are included. All original r1 base/foreground pixels and collision are restored exactly at +96,+96, without rescaling. The border master alone is resampled to the 960×864 canvas. The build writes native TMJ/WAM/atlases, layout, preservation proof and review images. Source rebuilding needs no image generation, API key, internet fetch or paid service.

Native route replay uses unchanged pinned engine methods with test doubles and EasyStar, covering every walkable floor cell, participant/dais/outdoor target, endpoint offsets, returns and sequences. Actual source geometry is a separate gate from live browser, keyboard/joystick/mobile physics, concurrency and AV.

Review overlays contain genuine unchanged native32 Woka idle frames. The frozen composed overlays and derived head-union mask are enough to reconstruct the fixed review; no raw sprite sheet is distributed. Independently recomputing pose/union provenance requires the original local repository sprites named in source-assets/WOKA-PROOF.json and OUTDOOR-WOKA-PROOF.json. Runtime contains no avatars.

The r1 baseline is from the independently accepted r1 source/runtime freeze. Its original Library source is libfile_ad4d2230533c8191af8d0dfe55f7a39f; the r1 map TMJ SHA256 is 300aa37abc7408c3104a50ff486326ca0c21d49606b194ac861a37fc2b1e3ec7. R1 itself is not edited or replaced by this build. The r2 spawn location is an intentional semantic change; old spawn quiet coverage is removed and exactly one new outdoor spawn cell is quiet.

Preserve ASSET-PROVENANCE.md and licenses/. No public URL or deployment is created.
