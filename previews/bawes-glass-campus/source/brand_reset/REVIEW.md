# Illustrated brand reset — representative alternative

Owner rejected `0d835f4` as off-brand: wood/gold/Art Deco and realistic furniture. Do not propagate that aesthetic. Both that checkpoint and earlier rejected `579875d` remain in GitHub history. This alternative is confined to the same lower tower/arrival section and tower shell; the wider campus is not being extended before review.

## Verified sources versus interpretation

- Current `BAWES-Universe/workadventure-universe-admin/app/globals.css` (fetched from default branch; blob `11b9d7713df1d914bdfa8afa125651bbeac54b8e`) explicitly specifies neutral dark surfaces, selective Universe violet/blue gradient `#8629fc` → `#4156f6`, and distinct semantic accents. Ink `#14121e` is the product foundation. These are product/UI rules, not an approved furniture or architectural material specification.
- Current game `docs/brand/README.md`, `bawes-lettermark-white.svg`, and `bawes-universe-white.svg`: identity assets and their intended dark-background use. The geometric tower identity is retained without baked text/signage.
- Archived `origin/archive/map-mock-library-2026-10-09:map-mocks/butterfly-campus-v3-dark/screenshot.png` was visually inspected. Early office artwork `map-mocks/expanded-office-01/screenshot.png` was inspected for readable upholstery/table silhouettes and orthogonal surfaces with raised fronts. Its historical colors, text and wood are not a mandate to reuse them.
- Named Magical Campus source README in `archive/source-recovery-2026-10-13/lean-historical/authoring/magical-campus-editable-source/` and later `docs/map-collection/previews/campus-v11.jpg` were inspected. The exact 'initial' revision is not uniquely established. Campus04/Butterfly Campus lineage was independently reviewed by the parent; the retrieved connected-campus 'early' images are planning diagrams and were NOT misrepresented as finished art.
- The owner rejected realistic rendering. The required craft is richly illustrated stylized scenery, expressive compact furniture and readable floors, not photographic surfaces or flat low-detail icons. Tea Garden remains a craft benchmark, Volcanic Observatory a spatial reference; neither sets brand materials.
- `Universe-Custom-SVGs-and-Design-Kit.zip` is an assistant-generated proposal according to the parent's provenance review, not an approved map-art bible. Library search succeeded; signed image transfers returned proxy403. Git/GitHub source reads and local image inspection work.

Design interpretation for this study: pale painted stone and cool ink structure, curved geometric floor mosaics, broad violet/blue upholstery, compact tables, illustrated planted glass partitions and localized cyan fixtures. These choices are proposed, not claimed as owner-approved brand details. No recoloring of the rejected wood/Art Deco scene was used: new retained image-tool originals were authored against the original geometry guide and early art references.

## Implementation and validation scope

`assemble.py` registers the new art to existing native door/seat coordinates. `section-original.png` and `tower-original.png` retain image-generation sources. Chair fronts use only a low foreground strip rather than the previous torso-obscuring band. Camera and Woka remain native scale. Actual desktop right-click and touch input is exercised in `source/validation/brand-seating.cjs`.

The existing map has no native sitting-pose mechanic: movement places the Woka at the authored chair anchor. These tests assess approach, exit, avatar visibility and layer overlap, not a newly implemented seated animation.

No new collision or runtime logic changes relative to `0d835f4`; the old whiteboard removal and two desk extents remain as that checkpoint. The tower retains full-footprint cutaway and approach doors; meeting lock behavior remains the same. Portal destinations remain unbound. Other campus artwork remains historical/rejected until this alternative is reviewed.

## Input test correction

The first desktop test used left-click and did not move. Inspection of `play/src/front/Phaser/UserInput/GameSceneUserInputHandler.ts:107` showed that this pinned Universe build uses right-click for desktop walking and a short tap on touch. The test was corrected to those existing controls; no engine changes were made. `brand-pointer-failure.png` records the invalid left-click attempt, not a passing test or visual deliverable.

## Current actual-game evidence

Normal-scale captures show the occupant head and torso at the lower meeting-chair anchor and visible through the exterior frontage. Desktop right-click approach/exit and short touch-tap approach/exit are tested. Keyboard movement is measured after bringing the game canvas into focus, with a 96px horizontal change in the final run. The separate final JSON records the tested positions and native scale. Static validation passes 6,396 connected walkable cells and 88 reachable seats; four mocked reveal handlers pass; repository build succeeds for 11/11 maps. These results do not imply visual acceptance or campus-wide polish.

## Owner consistency feedback — focused follow-up

Tea Garden, Sky Village and the earlier Butterfly/Magical Campus lineage were visually rechecked. Their useful common quality is coordinated projection, compact furnishing, material continuity and readable routes; their wood/gold themes are not copied. This pass reuses the current registered furniture/planting/wall kit across the existing tower upper rooms, arrival terraces and bordering paths. `empty-material-original.png` is a single image-tool edit of `review/brand-section-native.png`, with furniture removed to restore empty rugs. It supports native assembly without duplicate chairs. No external paid generation, new theme or broad campus expansion.

The lower reviewed seating section and tower shell remain intact. Existing work/meeting/social anchors and collision cells remain unchanged; new chair foreground strips cover only the feet. Other districts beyond surrounding street junctions remain unfinished, and repetition in the shared furniture/material kit is a remaining limitation rather than a claim of Tea Garden-equivalent finish.

A bounded second finishing edit, `consistency-finish-original.png`, uses `consistency-guide.png` (the compiled existing section) to repair repeated paving spots and clipped planter joins. It is composited at the same world bounds, without collision or runtime changes. This is retained separately from the empty-material source for reproducibility.
