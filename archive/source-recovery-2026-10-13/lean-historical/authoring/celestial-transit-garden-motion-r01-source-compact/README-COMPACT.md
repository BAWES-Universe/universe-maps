# celestial-transit-garden: compact motion r01 replay source

This is a separate companion to the unchanged frozen full motion-r01 candidate. No runtime, static map, ZIP or manifest was replaced.

Rebuild using Python3 + Pillow and Node.js, with no network or package install:

1. Extract this ZIP to any folder.
2. Run: python motion-tools/rebuild.py --output-dir /path/to/empty-output
3. The new celestial-transit-garden-motion-r01/map32/ folder contains the rebuilt runtime closure. Validation, native occupied frames, contact sheets and diagnostic GIF are regenerated as well.

Frozen full MANIFEST SHA256: 92aba812e5f3ab7012b68ec58bd180079d0ea0df690a548c50e1a0891bc25051
Frozen full source ZIP SHA256: e0c1742eadbfd3ffbb6eac245cfab6bd57a552310a020e2dd1c43e1522aff389
Frozen runtime ZIP SHA256: 56e84e042bbe5aa6f67290b7241c8088579894f5631eb28128683ac964955c87
Engine pin: 60e7afdc3f96ef32525597cd46bd41175d61a2ef
Actual native animation plugin git blob: 69d1046e62a6c60577d4591f3fac145f3a733f8b

COMPACT-COMPANION.json records exact input files, hashes and source provenance. All original art is recovered from the byte-exact static source input ZIP. Eight-frame alpha overlays are rebuilt from source. Review rendering is an atlas decode driven by native-plugin replay states, not a live browser screenshot.
