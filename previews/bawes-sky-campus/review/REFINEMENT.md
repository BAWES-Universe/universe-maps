# Isolated refinement review

Environment availability was confirmed with local files, a clean baseline checkout and the saved commit. Work stays in `previews/bawes-sky-campus/` on `feat/bawes-sky-campus`. No engine, shared Vite config, hosting configuration, public publishing, deployment or StudentHub integration is changed.

## Exact baseline images at 2b1e3423adc74c91e7384067215a815c7b848d2d

- Full-map **offline composition**, not a runtime screenshot: `previews/bawes-sky-campus/review/campus-exterior.png`.
- Native-Woka desktop interior **actual-client screenshot**: `previews/bawes-sky-campus/review/desktop-chair.png`.
- Native-Woka touch interior **actual-client screenshot**: `previews/bawes-sky-campus/review/mobile-chair.png`.
- Other inside/outside actual-client views: `review/inside-front-room.png` and `review/outside-visible-occupant.png` under the same candidate directory.

The baseline does not contain a full-world runtime screenshot. Its `desktop-explore.png` and `mobile-explore.png` cover only their measured camera views. The desktop chair screenshot also predates the removal of the stretched side foliage visible at its far left; its furniture/character evidence remains valid, but it is not a final exterior-art image.

## Optimizer correction

The previous statement that the optimizer only supports 32px was too broad. Its default is 32px; the installed optimizer exposes `options.tile.size`. The new candidate-local `vite.config.ts` passes 16. No map rescaling, collision coarsening, avatar rescaling or dependency patch is used. The shared repository-root build remains unchanged and still uses its default 32; use the isolated candidate command.

The generic optimizer also rewrites the map script to an HTML wrapper that loads `https://play.workadventu.re/iframe_api.js`. That wrapper did not initialize this map's controls in the local Universe test. The map-local post-build hook restores the map's self-contained JS script property and copies the exact source script. Universe then injects its own API, as it does for the tested raw map. The hook runs after the optimizer's asynchronous post-processing; no remote API endpoint is substituted.

`optimizer-equivalence.json` compares every used tile's RGBA pixels and tile properties, all layers in order, object data and native map dimensions. Script identity is retained separately. This establishes that optimization does not alter 16px collision precision or artwork. It does not establish visual acceptance. The optimizer emits fewer larger textures, but a larger PNG payload in this configuration; no download-size improvement is claimed.

## Visual inspection against the approved concept

- **Native furniture scale:** office desks are 64×64 against 32×32 Wokas; chair painted width is 32px, with transparent padding. The actual desktop/touch views support those proportions. Enlarging avatars or shrinking the world to compensate would break the native contract.
- **Art degradation:** the surrounding 1536×1024 concept is enlarged 3×. Its bar, stairs, plants and architecture are substantially softer and larger in apparent detail than the native furniture. Optimization is pixel-identical and cannot recover that source detail. This remains a visual acceptance issue.
- **Floor patches:** the small café patches were already removed by the whole-scene café cleanup in the baseline. Café paving is continuous. The stage has a distinct, rectangular light-paving audience area. The large office terrace and its straight front/side edges remain more rectangular and prominent than the approved concept. Those material/shape transitions still need owner judgment; they are not claimed to be visually seamless.
- **Baked furniture interference:** the western conservatory's curved lounge, table and entrance dining set were painted into the floor image and partly walkable. This refinement makes that decorative lounge region and dining set impassable while retaining the clear eastern promenade and stair landing. It does not pretend that those oversized painted seats are native usable chairs. The main office, café and audience retain all 74 reachable native seat anchors.
- **Building comparison:** the full usable office footprint is much larger than the concept's shallow illustrated office. It preserves the folded warm-glass direction but is not an exact BAWES vector silhouette or exact reconstruction of the approved façade. No claim of visual acceptance is made.

The collision refinement leaves 22,374 connected walkable cells; all nine destinations and 74 seat anchors remain connected. The old western camera anchor is now deliberately decorative/blocked. The current western walkable bound moves inward from 1952 to 2112; the unchanged backdrop therefore has more margin there. Baseline camera results are conservative for this inward boundary change, not a fresh walk test of the old anchor.

## Remaining limits

Review the new optimized-client screenshots separately from the offline full-map composition. Standard repository-wide building still needs per-map tile-size selection if this candidate is ever promoted; changing shared tooling is outside this task. Source artwork softness, the enlarged office's rectangular footprint and remaining decorative conservatory furniture are the main visual issues. No public review URL or deployment is created.

## Follow-up verification

The isolated build passes: one map processed, one succeeded. The pixel/property equivalence check and byte-identical runtime check pass. Nine optimized-map real-client checks pass: native outdoor spawn, chair entry/exit, meeting entrance, actual lock-menu interaction, safe locked-room exit, rear exit, clear western promenade and keyboard collision against the decorative western lounge. Evidence is in `optimized-runtime-checks.json`, `optimized-native-interior.png`, `optimized-rear.png` and `optimized-west-obstacle.png`. `optimizer-initial-api-failure.png` records the earlier failed wrapper run, not the final result.
