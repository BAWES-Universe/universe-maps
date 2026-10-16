# Focused consistency pass after 205b881

The owner found the representative section inconsistent with the earlier Tea Garden/Sky Village work. Those actual references and the early Butterfly Campus image were reviewed again. This pass reuses the existing illustrated furniture, glass, planting and cool stone treatment across the tower upper rooms, side paths and two arrival terraces. It does not introduce another theme or expand the campus program.

The old wooden upper floor, mixed terrace chairs and coarse side-bed art no longer adjoin the review section. One empty-material repair image restores rugs beneath removed furniture; furniture is then placed at the existing native anchors with silhouette masks and low foreground strips. Duplicate furniture and copied rectangular rug backgrounds caught in intermediate assembly were removed before final capture. Planting is reused at native scale. A second bounded image-tool finishing edit of the assembled guide repairs repeated paving blotches and clipped planting edges while preserving the furniture/layout; both its guide and original are retained.

## Actual gameplay comparison

All captures use the local pinned Universe engine, synthetic users and normal camera/Woka scale. No screenshot is a presentation render.

| View | Before (205b881 retained capture) | After |
| --- | --- | --- |
| Occupied interior | [Before](before-interior.png) | [After](after-interior.png) |
| Glass frontage and arrival | [Before](before-frontage.png) | [After](after-frontage.png) |

Additional affected-seat evidence: [upper room](after-upper-seat.png), [arrival terrace](after-terrace-seat.png), [touch](after-touch.png). The before images are the exact retained checkpoint captures, not reconstructed scenes.

## Validation scope

**Final run: 10/10 checks pass.** `checks.json` records the final actual-client run: desktop lower-chair approach/exit, upper-chair approach/exit, terrace-chair approach/exit, keyboard displacement, touch approach/exit, and interior cutaway. `inputs.json` records the runtime, collision and art hashes. Only the seat-backs tile layer changes in the map JSON; persistent collision, full-footprint interiors, doors, shared lock script and seat coordinates are unchanged from 205b881. Shared lock concurrency was not redundantly retested for this art-only pass; prior evidence remains historical.

Static checks retain 6,396 connected walkable cells, 88 reachable seats, the connected StudentHub reserve and 192px entrances. Four mocked reveal checks and the repository 11-map packaging build are separate from visual acceptance.

## Remaining limits

This is a focused consistency improvement, not a claim of Tea Garden-equivalent finish or owner acceptance. Furniture motifs and paving repeat; bespoke variation and broader composition still need review. Other campus districts retain the old art beyond the surrounding street junctions. No new seated animation, bound portal destinations or production chat/media integration. No existing maps/Azure/engine changes, merge or deployment.
