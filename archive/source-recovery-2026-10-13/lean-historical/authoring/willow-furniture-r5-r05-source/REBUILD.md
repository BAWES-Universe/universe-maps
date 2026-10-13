# Occupied candidate rebuild

Run `python tools/build_candidate.py`, then `node tools/native/route-audit.cjs willow-quay-tea-garden`, then `python tools/check_spawn_and_boundaries.py willow-quay-tea-garden`. Python requires Pillow and NumPy.

This source package intentionally excludes raw character sprite sheets. Obtain the referenced sprites from your authorized existing repository checkout (`play/public/resources/characters/pipoya/`) and place the 12 filenames listed in `woka-source/manifest.json` in local `woka-source/`. The build also expects the existing `source/greg-reference.png` validation fixture from the accepted original Willow source; it is not redistributed here. These are local rendering/test references, never map runtime assets. The compiled runtime has no character assets and uses players' existing avatars.

The receipt freezes this occupied candidate only. Ambient motion integration and independent review remain separate; no release or publication approval is implied.
