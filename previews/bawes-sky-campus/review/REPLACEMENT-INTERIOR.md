# Replacement interior preview — architectural fidelity correction, 2026-10-18

Implemented only in `previews/bawes-sky-campus` on `feat/bawes-sky-campus`. No deployment, Azure operation, engine edit or paid generation. The approved exterior and entrance remain; outdoor restoration has its own unresolved source requirements in OUTDOOR-RESTORATION-AUDIT.md.

## Source and construction

The exact approved concept is preserved under source/approved-interior. New candidates from commit `73b734915f1014e3dbb5c6fda4792742de94dd2d` are preserved under source/interior-candidates with provenance and hashes. These are reconstructed matching candidates, not original registered layers.

Furniture was individually alpha-trimmed and uniformly resized; no nonuniform scaling. Four complete chair views are retained. Calibration dimensions are in interior-asset-calibration.json. The floor repeats a native-detail clean stone region from the matching candidate, with restrained measured inlays. It does not stretch the unregistered plate or copy its opaque gray border. Continuous orthogonal bays now assemble the coordinated sheet’s detailed stone piers, tall inset columns, brass cap rails and textured plinths. Only the translucent pane fill and reflection strokes are renderer-native geometry. The opaque candidate glass and angled partitions are excluded. New room door leaves use the same transparent fill and segmented illustrated rails; the exterior gate remains unchanged.

The layout follows the approved composition: two individual work settings plus a shared four-place table on the left, curved reception near the arrival spine, two south-facing sofas lower left and two complete meeting rooms on the right. Floor, furnishings, foreground masks, glazing and permanent collision are separate. Chair, sofa and counter foregrounds come from those same sprites. There are no borrowed library tiles, colored carpet blocks, invented logo, beverage popup or replacement UI.

## Measured fit

- Native Woka32, scale1; 16px map grid, unchanged engine.
- Bounded floor 2144×592, no overflow or rear exit into sky.
- 192px entrance/spine, 96px front doors and between-room passage.
- Sofa sprite edge is 112px from the front boundary, leaving 96px before the 16px wall.
- 19 indoor occupancy anchors, 48 unchanged outdoor anchors; all 67 connected to spawn.

## Evidence and limits

`replacement-checks.json` records actual right-click anchor occupancy and native R-key direction, with the final runtime lock/exit checks recorded in `replacement-lock-checks.json`. The initial room-test setup omitted a movement event after direct placement; that harness was corrected with native movement, and only the valid 38 seat/facing assertions are retained in the seat report. Navigation setup uses instrumented movement and near-seat placement; the final seat action is native right-click. This verifies achievable facing, not automatic facing. Door state is local per viewer; an occupant keeps their room door open to permit path planning from anywhere inside, while a locked visitor remains blocked. The engine has no public bent-leg sitting pose: these are ordinary Wokas at furniture anchors with segmented foreground occlusion.

`replacement-occupied-*.png` show occupied settings at normal client zoom. `runtime-full-interior.png` is the whole interior; `footprint-interior.png` and `footprint-exterior.png` use the identical camera and avatar position. `geometry.json` and `footprint-audit.json` report connectivity and containment. `optimizer-equivalence.json` compares every used tile pixel/property, layer order, dimensions and runtime bytes after optimization.

The flat beige bars of 82379a5 were rejected and replaced. The revised architecture retains source texture, highlights, plinth depth, individual columns, corner piers, planting and shadows. It is a constructed interpretation of the approved family, not a registered copy of the full concept, and still needs visual acceptance. Shared locks are ephemeral courtesy controls, not private audio or access security. The exterior gate still has the previously documented stepped motion. Outdoor original café/alcove/stage restoration is not included in this interior pass.

## Fidelity correction evidence

`source/architecture.py` records exact source crops and uniform scales for structural detail. No opaque candidate glass or baked pane foliage is used. Pane alpha ranges56–78/255, with separate low-alpha reflections; source rails/posts remain opaque. Six tall inset columns, eight front piers, eight meeting corner piers, five raised planting bands and nine potted plants replace the empty outlined architecture. Source detail is repeated to form continuous orthogonal runs; nothing was generated. The back structural strip is now96px deep, and left work settings/shared table move down32/64px to align with it without adding desk rows.

Sofas are128px wide (formerly176), with approximately96px of inner seating width and two anchors48px apart. Both native32px occupants fit the usable span; no avatar scaling. Sofa fronts remain112px from the footprint edge, leaving96px before the front collision wall. Front-facing chair art shifts8px under the fixed anchor, and its front mask is limited to the lower edge. The saved meeting screenshot has an exact anchor match; test setup now emits real movement before pointer occupancy so a newly opened room does not replan the test click one tile forward. No automatic orientation or bent-leg seated pose is claimed.

The café candidates are preserved and bounded in CAFE-CANDIDATE-ASSESSMENT.md. They are source preparation only; this fidelity correction leaves outdoor pixels unchanged.
