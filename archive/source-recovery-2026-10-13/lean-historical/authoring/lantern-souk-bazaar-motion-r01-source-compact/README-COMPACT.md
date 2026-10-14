# lantern-souk-bazaar: compact motion r01 replay source

This is a separate companion to the unchanged frozen full motion-r01 candidate. No runtime, static map, ZIP or manifest was replaced.

Rebuild using Python3 + Pillow and Node.js, with no network or package install:

1. Extract this ZIP to any folder.
2. Run: python motion-tools/rebuild.py --output-dir /path/to/empty-output
3. The new lantern-souk-bazaar-motion-r01/map32/ folder contains the rebuilt runtime closure. Validation, native occupied frames, contact sheets and diagnostic GIF are regenerated as well.

Frozen full MANIFEST SHA256: 2ea8f2b354ee3f75c45b85d2b921be464fd586c3199c153a6b95434a1f46a7b6
Frozen full source ZIP SHA256: 76a807a032f83db804d368fab614ee2fe7d8dd599955f040cddc3a73cdd322ac
Frozen runtime ZIP SHA256: ad9d38018f57ba42c678fa59b0a498a074115bda12a2f7c70ee0c3f2b4ef7e48
Engine pin: 60e7afdc3f96ef32525597cd46bd41175d61a2ef
Actual native animation plugin git blob: 69d1046e62a6c60577d4591f3fac145f3a733f8b

COMPACT-COMPANION.json records exact input files, hashes and source provenance. All original art is recovered from the byte-exact static source input ZIP. Eight-frame alpha overlays are rebuilt from source. Review rendering is an atlas decode driven by native-plugin replay states, not a live browser screenshot.
