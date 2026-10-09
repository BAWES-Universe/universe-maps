# StudentHub arrival: original art and lighting experiment

Status: archived look-development experiment. The art does not yet meet the owner's v1/giant-gate standard. It is not a playable map, an accepted replacement, a published room, or a catalog-ready template.

The scene studies a connected small-team workplace reached through a planted court, with reception beside arrival, neighboring stations, a glass meeting room, a sofa/rug group, and a fountain. It uses original geometry and original painted material inputs, calibrated to the unchanged32px Woka. This experiment lives separately from all published maps and from the preserved giant-gate journey.

## Review images

- `docs/final-open-native.png`:1536×1152 interior-revealed scene render with one unchanged32px Greg for scale
- `docs/final-covered-native.png`:same scene with the authored rear roof visible
- `docs/final-threshold-native.png`:768×480 native crop of court/entry; no enlargement
- `experiments/brown-maquette/preview.png`:earlier rejected brown material direction

These are offline art renders with a scale sprite, not game screenshots. No continuous playable walkthrough was recorded for this experiment.

## Editable source

`art-source/studenthub-arrival.blend` is the final packed, compressed Blender4.3.2 source. `tools/build_scene.py` rebuilds it and the two draft renders using the original source material images. `art-source/scene-layout.json` stores physical footprints, chair anchors and the exact projection contract. The earlier brown source is `experiments/brown-maquette/scene.blend`.

`art-source/PROVENANCE.md` explains the original material generation. No third-party reference-map art or earlier rejected furniture cutout set was reused.

The render uses Cycles CPU and a restrained compositor pass. A draft rebuild is `blender -b -t 12 --python tools/build_scene.py -- --draft`. It writes new art-source/render outputs locally. Native render dimensions remain1536×1152.

## Verification boundary

The camera's two ground-axis projections are asserted at32 pixels per unit, and both final images are native resolution. Source textures are packed into both Blender files. Shared geometric lighting and contact shadows are visible. This is the extent of the new section's completed validation.

The proposed semantic export/compiler (`tools/compile_map.py`) and actual-Phaser harness (`qa/`) are unfinished/prepared infrastructure. No TMJ, atlas, browser walkthrough, chair/lectern/glass acceptance, mobile test, sound, bot, native meeting or service integration is claimed. Full export was deliberately held after visual review found the current artwork below the requested quality.

Read `docs/LOOK-DEVELOPMENT-STATUS.md` for the diagnosis and `docs/NEXT-ART-STEP.md` for the proposed painted-asset/scene-guide test. Further main-world art work requires a new bounded iteration; it should not be inferred from this archive.


## Archive packaging note

The prepared compiler and Phaser harness described above were not validated and are not included in this archival snapshot. Use the archive README for the exact preserved contents. Packed sources have portability-only path normalization.
