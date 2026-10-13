# Gate B v3 geometry review

Local, unpublished map-only candidate for integration with the separate camera work. The current game source is pinned read-only at universe-develop commit 75666c0ccae779515b6fcbd83446ebd1eee29d1b. This is a source reference, not a verified deployed-game revision.

## Result

- Retains the exact 960×1440 world, standard 32px grid, original 32px Woka dimensions, all old art/animation layers, objects, spawn coordinates, audio bytes and script bytes.
- Realigns central walkability with the stairs and landings. The right lamp, planter, tree, edge and water regions marked red are blocked using the full native 16×16 body.
- Opens the two existing balcony floors with connected stone approaches. Existing tree and lamp silhouettes are copied, without changing their pixels, into a foreground layer above the native floor marker. Their physical trunks, planters and pedestal bases remain blocked. These are separate from the upper silhouette through which the player can pass behind.
- Adds a small transparent native silent=true layer at x448–544, y1088–1184. It contains the full declared start area, the single native start tile and the explicit spawn point, with a margin for body/feet. This only controls proximity conversations; map music remains unchanged. Leaving the zone releases its contribution to silence, without overriding other native silence sources.

The user annotation was registered to the actual native atlas composition. Measured screen scale is approximately 0.9359 with cropped offsets, not one screenshot pixel per world pixel. The registration and exact red/green world rectangles are in results/annotation-registration.json.

## Source/model verification

- 16/16 explicit balcony-candidate routes pass full ascent, descent, green stair/landing visits, both balcony visits and returns. The stairs-only fallback passes its 12 central routes; its four balcony routes are intentionally inaccessible. Baseline Bv2 passed 4/16.
- 536 every-open-cell out-and-back model cases pass, including two native same-tile no-ops. Native PathfindingManager and Player methods are source-extracted unchanged and use the actual EasyStar0.4.4 implementation. Frame stepping is 60Hz at native speed9, with an additional half-pixel body sweep.
- 135 distinct fractional clicks across the six green regions, each from three spawn offsets and back, pass405/405. Fifteen of150 coarse region samples land in conservative32px pool, railing, lamp or vegetation edge cells and remain blocked. These are explicitly excluded and listed, not reported as successful green clicks. No nearest-tile fallback is used.
- Every one of31,314 sampled actor origins across the four red rectangles is body-blocked. Physical balcony base footprints are separately swept in physical-base-verification.json, while four behind-canopy/pole positions are verified body-clear.
- Five complete scene comparisons at animation times0,600,1800,3600 and5400ms are pixel-identical to Bv2 when no actor is present. Native32 Woka composites show the actor correctly behind each foreground tree/lamp and unobscured on the balcony floors.
- 16 native silent-store/property checks pass, including2145 points covering the entire declared start rectangle, start-tile center, repeated exits/returns and unchanged music.

These are exact-source model, geometry and offline atlas-composition tests. Browser control remains blocked; no recovery or alternate-browser attempt was made. Live game physics, actual touch/joystick dispatch, device graphics, iPhone behavior and network proximity grouping have not been tested.

## Important initial-join limit

The current client registers the silent callback before connecting, but sends its existing availability status in the room-join handshake before evaluating the initial spawn tile. The explicit spawn setPosition is after the room-joined response. The silent layer therefore cannot guarantee zero transient proximity bubble during the initial handshake. Source-order evidence and an executable property-store fixture are in source-audit and results/silent-zone-verification.json. No game-engine change or script workaround is included.

## Integration

GEOMETRY-INTEGRATION-MANIFEST.json pins the exact candidate TMJ and new foreground PNG, names the only owned map edits, and hashes unchanged payload files. The camera worker owns any later script changes and the final combined validation. Do not publish this candidate separately.

The main candidate is publish/public/butterfly-town/gate-b/v3/gate.tmj. stairs-only/gate.tmj is a replacement-map fallback for that same destination directory; it references the original shared assets and includes spawn silence but no balconies or foreground tileset. dependencies contains exact old shared PNGs for offline review only, not republishing.

Useful visual review:
- results/annotation-boundary-comparison.png
- results/native32-occlusion-contact-sheet.png
- results/candidate-grid.png

Reproduction from this review workspace: run python tools/build_candidate.py, node tools/build_native_model.cjs, node tools/verify_routes.mjs, node tools/verify_tolerant_taps.mjs, node tools/verify_silent.cjs, python tools/verify_art.py, python tools/assemble_review_images.py and python tools/finalize_geometry.py. Build inputs reference the frozen local Bv2 package. The silent fixture uses the existing Svelte dependency from the source-audit checkout; no dependencies or software were installed.
