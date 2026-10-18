# Replacement interior preview — 2026-10-18

Implemented only in `previews/bawes-sky-campus` on `feat/bawes-sky-campus`. No deployment, Azure operation, engine edit or paid generation. The approved exterior and entrance remain; outdoor restoration has its own unresolved source requirements in OUTDOOR-RESTORATION-AUDIT.md.

## Source and construction

The exact approved concept is preserved under source/approved-interior. New candidates from commit `73b734915f1014e3dbb5c6fda4792742de94dd2d` are preserved under source/interior-candidates with provenance and hashes. These are reconstructed matching candidates, not original registered layers.

Furniture was individually alpha-trimmed and uniformly resized; no nonuniform scaling. Four complete chair views are retained. Calibration dimensions are in interior-asset-calibration.json. The floor repeats a native-detail clean stone region from the matching candidate, with restrained measured inlays. It does not stretch the unregistered plate or copy its opaque gray border. Continuous orthogonal stone and transparent amber glazing are renderer-native geometry. The opaque candidate glass and angled partitions are excluded. New room door leaves use the same transparent fill and brass line treatment; the exterior gate remains unchanged.

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

The furniture is illustrated; the continuous architectural runs are simpler measured construction and still need visual acceptance. Shared locks are ephemeral courtesy controls, not private audio or access security. The exterior gate still has the previously documented stepped motion. Outdoor original café/alcove/stage restoration is not included in this interior pass.
