# Representative tower section — owner review required

The owner rejected the entire visual quality of `579875d`. That commit remains on GitHub and on local branch `checkpoint/bawes-rejected-art-579875d`. This revision is a representative section, not completed campus artwork. It replaces tower architecture and the lower tower interior/arrival area (world x320–1088, y1280–1856); other districts remain the rejected artwork. Abrupt study boundaries are expected pending an accepted campus-wide treatment.

## References actually inspected

All retrieved from `origin/backup/moonlit-art-review-2026-10-15` (`f8d196cb`), except Butterfly Campus from `origin/archive/map-mock-library-2026-10-09` (`03d83f2`). Runtime TMJ atlases were decoded to full native-resolution images for inspection, not merely read as metadata.

- **Willow Quay Tea Garden**: `recovery/furniture-access-2026-10-13/reviewed-revision/runtime/willow-furniture-r5-r05-runtime/map32/`. Benchmark for tactile material detail, planting, coherent light, edges and small props. Its named README identifies the garden unambiguously; owner can correct the exact revision if needed.
- **Volcanic Observatory Lodge**: `archive/runtime-recovery-2026-10-13/N39-r3-runtime/`. Setting, purposeful bridge connection, usable paving and spatial composition.
- **Sky Village Airship Terminal**: `archive/runtime-recovery-2026-10-13/N42-r4-runtime/`. Distinct linked destinations, edge planting and architectural layers.
- **Lantern Souk Bazaar**: `archive/runtime-recovery-2026-10-13/lantern-souk-bazaar-r6-fountain-runtime/`. Prop specificity, warm local lighting, patterned walkable surfaces and destination character.
- Moonlit arrival and earlier Butterfly Campus were inspected for context; neither is the requested quality ceiling.
- Universe Ink palette read in the saved admin `app/globals.css`: #14121e foundation with violet raised surfaces and restrained accents.

Reference artwork is studied, not pasted into this section. Retained image-generation originals are `section-original.png`, `section-registered-original.png` and `tower-original.png`. Built-in image generation was used, with no external paid service. The first, more ornamental section study remains in the saved environment at `generated_images/exec-0386f55d-ddfc-460c-9548-0c61c49dbaf3.png`; it was revised toward modern task furniture, geometric textiles and integrated lights.

## Implementation and limits

`registration-study.py` retains the measured initial registration; the final image-tool cleanup retains those anchors without stretched rug artifacts. `assemble.py` places the registered section at native room and door anchors, replaces its old foreground props, and splits chair fronts for avatar overlap. Camera zoom and Woka scale remain unchanged. Furniture positions are measured in pixels in `layout.json`; chair groups were corrected to the native tile-centred movement grid. Two desk collision extents expand to match the artwork, and the obsolete standing-whiteboard blocker is removed. Door artwork is reduced to subtle smoked glass with thin warm-metal edges; its tile collision properties are unchanged. Main routes, entrances, meeting room bounds, shared-lock script and full building reveal masks remain intact.

Actual screenshots are `review/redesign-*.png`. These must be visually reviewed separately from gameplay checks. The partial section is not claimed to exceed Tea Garden without owner review. Current section tests do not recertify all other campus art, and older polished/town suites are historical evidence.

## Current review evidence

Final section run: 5/5 actual-client checks (native tile-centred seat approach, independent outside/inside cover, lounge seat and exit). Door run: 10/10 passed before the final artwork-only chair cleanup and door sprite change; collision and lock logic are unchanged. Build: 11/11 maps. Static: 6,396 walkable cells and 88 reachable seat cells. Screenshots were inspected visually at normal 1440×900 client scale.

The new interior and outside captures show the actual local game. Old art at the top/bottom is the explicit section boundary. Remaining work is owner review followed by coherent campus-wide spatial/art redesign, including garden edges and secondary districts; current gameplay checks are not visual acceptance.
