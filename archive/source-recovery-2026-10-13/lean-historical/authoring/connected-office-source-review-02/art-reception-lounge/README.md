# Native reception and lounge assets

Original transparent painted furniture for the expanded magical StudentHub office. These are assets and static geometry proofs, not a finished map or live runtime evidence.

- `native/reception.png`: canvas 160×96, actual visible counter 128×64 at (16,16)
- `native/sofa.png`: canvas 160×96, actual visible two-person sofa 128×64 at (16,16)
- `native/coffee-table.png`: canvas 96×64, actual visible table 64×32 at (16,16)
- `native/*-object-alpha.png`: actual full object alpha
- `native/*-occluder.png`: real source pixels selected by traced contours
- `native/sofa-foreground.png`: combined front rail and arm pieces
- `native/*-contact-alpha.png`: actual foot-contact pixels

Use `asset-manifest.json` for final placements, visible bounds, collision parts, contact footprints, exact occupant anchors/directions, foreground traces, and sampled routes. `geometry-plan.json` preserves the original plan. `reduction-manifest.json` records source sizes, measured source crop, transformation, alpha bounds, and hashes.

## Native proof and verification

`proofs/native-empty.png` and `proofs/native-occupied.png` are 768×352 canvases at 1× scale. `proofs/native-occupied-2x.png` is explicitly nearest-neighbor inspection only. The sofa and table have exactly 48px clear floor between their actual visible edges. The reception reserves a 64px north staff pocket and 64px side bypasses. Thirteen entry, exit, bypass, and occupied-neighbor routes pass 1px sampled collision checks with the unchanged 16×16 avatar body. Actual masks change zero protected head pixels; each sofa front masks 34 lower-body pixels.

Greg remains the original 96×128 sprite sheet, cropped to unchanged 32×32 south (index1) and north (index10) cardinal idle frames. The two sofa sprites are spatial occupancy fixtures. They do not imply a sit animation, claim state, or multiple live players. Sofa back and arms collide, but the allocated seat area remains walkable. A full sofa rectangle collider would make the seats unreachable and must not be substituted.

## Source and transformation record

All three masters were generated using built-in `image_gen`, one call per asset, from the exact silhouettes in `guides/`. Every prompt and original master is retained in `source/`. No paid external API or copied third-party artwork was used. The native files contain one premultiplied Lanczos reduction directly from each meaningful alpha>=5 source crop. Final alpha<=4 traces were zeroed; object pixels were not repainted. There is no upscale being presented as new high-resolution detail.

The generator drifted modestly from guide margins and proportions. Each actual source object was measured and fitted once to its requested visible native size. The reception's top is approximately43px deep rather than the planned48; the sofa front begins1px lower than plan; the coffee-table top is approximately25px rather than24. Original anchors were retained and all route/head checks pass. The broad top planes and shallow fronts remain consistent with the validated high-angle orthographic camera. These deviations are explicit in the manifest for visual review.

## Reproduction

`tools/make_geometry.py` generates the guide images and initial geometry plan. `tools/reduce_native.py` derives native assets from preserved masters. `tools/build_proofs.py` derives masks, composites, manifest, and route/head checks. Python and Pillow are required; the font is DejaVu Sans.

Runtime integration, existing claim-contract wiring if desired, in-engine collision/depth verification, and final owner review are outside this asset package and remain required in the full-office build.

## North-facing sofa addition

See `SOFA-NORTH.md` and `sofa-north-manifest.json` for the original opposite-facing sofa, real backrest/arm masks, fixed north-facing seat anchors, and verified static social-pairing proof. Earlier furniture assets remain byte-identical.
