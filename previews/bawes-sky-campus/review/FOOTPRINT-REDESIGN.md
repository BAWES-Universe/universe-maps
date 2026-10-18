> Historical footprint checkpoint. The later [composition pass](COMPOSITION-PASS.md) supersedes its furnishing counts and no-steam statement.

# Footprint correction and furnished interior — 2026-10-18

The previous candidate was rejected for extending interior space outside the building and for a sparse, flat interior. This report supersedes prior visual-readiness reports. Owner acceptance is still required.

## Exact defects and corrections

The previous 2240×1440 floor started above the actual wall body. Its additional 128px service perimeter further occupied outdoor space. The old rear exit led into that artificial perimeter, and plaza sofas stood near the cliff edge. Matching the floor to the whole façade image also incorrectly counted the decorative plant fringe as interior space.

The current floor is **[2944,2448,2144,592]**, ending at x5088/y3040. The unchanged façade artwork uses the aligned **[2896,2128,2240,976]** canvas, including roof and external planting. The floor is inset 48px at either side and stops 64px before the canvas bottom plant fringe. Its back line follows the wings' masonry parapet. There is no service floor outside it. All interior floor, wall, furniture and chair-front tiles are contained within this exact rectangle. The cutaway trigger equals the rectangle. All indoor sofas have at least 64px front clearance. The two plaza sofas moved back from the cliff toward the entrance.

The unsafe rear exit was removed. A 192px front passage crosses the existing entry paving to the town square. New illustrated entrance leaves are tied to the same proximity/collision state: closed at rest outside, open on approach, safely open while an occupant exits. No teleport or remote destination was invented.

## Interior composition and recovered assets

Four native workstation pods provide 16 desks. One larger project room contains two tables/eight seats; two smaller meeting rooms each contain a table/four seats. Reception and two sofa/coffee-table settings sit to the side of the central route. Furniture and Woka dimensions were not rescaled.

The recovered Butterfly Town library artwork supplies stone wall faces, shelving, lamps and teal woven carpet detail at native asset scale. Existing BAWES furniture and amber/red floor branding remain. This reuse adds architectural depth, material detail and warm lighting without paid or new image generation. The source files are preserved under `source/reused/`; original maps were not edited.

Lantern Courtyard and Butterfly Town scripts provide verified proximity-driven glow/butterfly patterns. No reusable smoke asset or verified smoke implementation was found. This candidate reuses the existing proximity glow at reception, suppressed with reduced-motion preference. It is **not smoke**, and is not described as animated smoke or work-activity detection.

## Visual evidence

- [Full campus, actual client](runtime-campus-exterior.png)
- [Roof visible at fixed camera](footprint-exterior.png)
- [Roof hidden at the identical camera](footprint-interior.png)
- [Native desk/chair close view](runtime-native-interior.png)
- [Project room close view](project-room-close.png)
- [Entrance closed](entrance-closed.png) / [entrance open](entrance-open.png)
- [Reception proximity glow](reception-active.png) / [reduced motion](reception-reduced-motion.png)
- [Every furniture extent and measured wall clearance](furniture-clearances.svg)

The roof comparison is a diagnostic pair: a stationary inside player uses map API visibility switches, with identical camera rectangle, zoom and player position. Normal entry/exit is separately exercised. The SVG is a native-pixel plan reconstructed from current TMJ tiles, not a client screenshot; each furniture outline exposes its measured clearance. `footprint-audit.json` records every object and verifies no interior layer spills out.

Remaining visual limitations: the original landscape has softer close-up detail than native interior assets, some decorative vegetation is large relative to Wokas, and the façade's illustrated upper floors do not represent separate navigable storeys. The reused art may still need owner-directed aesthetic refinement. No smoke effect is implemented. These limitations are not substituted with test counts or a claim of visual acceptance.

No engine change, public publication, merge, deployment, paid generation or unrelated work was performed.

## Verification of this correction

The final actual-client captures above were refreshed after the stone-cap and carpet refinements. The roof comparison preserves camera rectangle, zoom and avatar position exactly. Normal entrance approach opens the illustrated leaves and collision gate; leaving restores the façade and closes the entrance. Desktop and mobile chair interactions passed. The two-client room check verified outsider blocking, safe occupant exit and admission after unlock. A separate two-client capture confirms a live occupant remains visible through the glass.

The geometry audit contains one connected campus, all 85 seats reachable and all eight route waypoints reachable. A separate native-client seat sweep exercised all 85 chairs from nearby free positions; it is not an end-to-end route proof. The footprint audit checks full furniture image bounds and every occupied interior tile. Optimized output preserves layer pixels, tile properties and runtime script bytes. These functional results do not establish aesthetic acceptance.
