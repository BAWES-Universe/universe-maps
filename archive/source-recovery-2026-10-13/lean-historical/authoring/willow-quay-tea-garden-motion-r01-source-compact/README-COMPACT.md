# willow-quay-tea-garden: compact motion r01 replay source

This is a separate companion to the unchanged frozen full motion-r01 candidate. No runtime, static map, ZIP or manifest was replaced.

Rebuild using Python3 + Pillow and Node.js, with no network or package install:

1. Extract this ZIP to any folder.
2. Run: python motion-tools/rebuild.py --output-dir /path/to/empty-output
3. The new willow-quay-tea-garden-motion-r01/map32/ folder contains the rebuilt runtime closure. Validation, native occupied frames, contact sheets and diagnostic GIF are regenerated as well.

Frozen full MANIFEST SHA256: 62981bc24d6f6f08e0054efdc60d5d3b7d0aca3069ca7f43993f0907c5a5e234
Frozen full source ZIP SHA256: 61d9b3ff03899bb9c3eacdbfb81a0162ebcec0407c7c9be0af813c508efabb22
Frozen runtime ZIP SHA256: b25c9fd7f3d83cbfea52dc85197d1a5ac344ead4123463c67afc3f7121356dd2
Engine pin: 60e7afdc3f96ef32525597cd46bd41175d61a2ef
Actual native animation plugin git blob: 69d1046e62a6c60577d4591f3fac145f3a733f8b

COMPACT-COMPANION.json records exact input files, hashes and source provenance. All original art is recovered from the byte-exact static source input ZIP. Eight-frame alpha overlays are rebuilt from source. Review rendering is an atlas decode driven by native-plugin replay states, not a live browser screenshot.
