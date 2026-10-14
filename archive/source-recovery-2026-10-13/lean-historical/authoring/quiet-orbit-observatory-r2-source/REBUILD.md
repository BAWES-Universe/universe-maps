# Quiet Orbit Observatory r2

Run `python tools/build_observatory.py` (Python 3, Pillow), then `node tools/verify_native_routes.cjs quiet-orbit-observatory` and `python tools/check_head_geometry.py quiet-orbit-observatory` (NumPy). No network or generation required to rebuild.

This revision adds a 384px solid north backdrop. The original 1536×1024 canvas is translated down exactly 384px at 1:1 scale; every original pixel outside the eight old/new seminar-chair footprints remains byte-identical. The eight chairs now form two compact four-seat rows with side access and native chair-back foreground layering. No other architecture, furniture or routes are redesigned. Original r1 is untouched.

The generated master was made using the built-in image tool, then only its north strip was registered to the original north edge. A 24px boundary-color blend is confined to the added strip outside the central arch. The original map is never blended or rescaled.

Native stage and audience areas retain the original speakerMegaphone/listenerMegaphone pairing. Source inspection at commit f00b3482f23c51976b4b339d7a891cad683d6498 confirms role stores derive SPEAKER/LISTENER statuses, which the server treats as silent for proximity grouping. The listener handler contains a stale TODO. No extra silence overlay was added and spawn-only silence remains one tile. No audio was added.

Static/runtime-artifact checks pass: 720 native path legs, 1,047,500 body samples, zero collision hits, zero exhaustive reachable head conflicts, atlas roundtrip/asset closure, and pixel preservation outside the authorized changes. Routes use the existing pinned engine fixture 60e7afdc3f96ef32525597cd46bd41175d61a2ef; the current stage source is pinned separately. These are static proofs and source-contract checks, not live room, microphone, broadcast or multi-user tests.

Deploy the complete map32 folder together and import map.wam for stage semantics. The PNGs are review renders, not functioning rooms. No external service signup, API, engine patch, production publication or paid third-party provider was used.
