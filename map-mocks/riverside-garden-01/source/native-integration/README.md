# Static native integration variant

This bounded variant supersedes the older demo as the candidate for native collision and foreground integration. The original generated artwork, demo runtime/audio/tests and archive remain unchanged.

## What changed

- All physics is permanent. Back/arm/plant footprints remain solid while the four bench cushion/position corridors are always open. There is no `benchId` mode or collision switching.
- The conservative physical mask is an8px grid: an8×8 cell becomes solid if any sampled pixel intersects a physical obstacle or leaves the approved walk surface. Continuous16×16 native-body sweeps verify entry, approach and reverse exit.
- Every foreground is a fixed world-space architectural mask. No mask depends on avatar position, alpha, head box, interaction mode or facing.
- Fixed masks trace the actual painted backs/arms. The north backrail remains behind its occupant in the base; its low front fascia is not incorrectly treated as head-height foreground. The south near backrail and arms are above-character. Side benches retain their outside painted back and end arms as fixed foreground. No head-shaped structure was removed.

## Exact support status

All four bench-position fixtures pass permanent-grid reachability, approach→position→reverse-exit, and fixed-mask head checks for all3 frames of their prescribed facing. The south rail properly occludes63 lower-body pixels in the idle frame. The other three positions are in front of or clear of their real rails, so no extra lower-body coverage is claimed or fabricated.

These are positions on/at the bench surfaces using the existing unchanged standing Woka frames. They are not a new sitting animation. Native Universe/Phaser rendering and physics are still pending the compiler's live check. No multiplayer occupancy or ownership is claimed.

Native sprite-center coordinates:
- North `(496,392)`, face down; approach `(496,432)`
- South `(496,624)`, face up; approach `(496,584)`
- West `(384,520)`, face right; approach `(416,520)`
- East `(608,520)`, face left; approach `(568,520)`

World origin remains `(2176,1920)`. Add it once to all positions and rectangles. West entry center is `(16,272)` with feet `(16,288)`. Frame32×32 at scale1; body offset(-8,0), size16×16.

## Compiler inputs

- `native-manifest.json`: exact coordinates, geometry, fixed mask semantics and per-position support.
- `riverside-native-static-8px.tmj`: ordinary orthogonal8px tile map; transparent collision tile has `collides:true`; ground is below `floorLayer`, fixed foreground above. No dynamic properties or custom sit API.
- `collision-grid-8px.json`: permanent physical cells, not a position-conditioned standability grid.
- `collision-rectangles.json`: merged equivalent native-pixel rectangles for a32px host map that accepts fixed rectangle colliders. The art/Woka are not resized when using these.
- `masks/permanent-physical-mask.png`: white=solid, black=walkable.
- `masks/bench-and-foliage-fixed-foreground.png`: single static above-character layer.
- `masks/bench-*-fixed-foreground.png`: individual structural parts for audit.
- `docs/four-static-bench-positions-native.png`: unaltered32px sprites under the same fixed foreground.
- `docs/permanent-grid-verification.json` and `docs/fixed-mask-verification.json`: exact evidence, including route coordinates and all-frame head coverage counts.

The standalone8px TMJ is structurally ordinary Tiled; successful loading, layer ordering and movement in the actual host remain an acceptance gate. Do not silently substitute32px tile rounding for this8px physical mask. The merged rectangle file is the exact option for a host with a32px art grid.

Water, fire and planted regions remain solid. The module does not change the giant gate, office topology, global audio/background behavior or live configuration.
