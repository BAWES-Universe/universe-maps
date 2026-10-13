# The Butterfly Gate · StudentHub Town

A single finite 144 × 96 TMJ, 32 px tiles, with an original monumental gate and a separate living town scene. Crossing the magical threshold teleports only the local player to town. The gate's visual layers disappear locally. StudentHub, Lantern Café and Atlas Archive reveal their interiors at the same physical location when entered; stepping out restores each roof and surrounding light.

## Install in universe-maps

Copy this complete folder to `public/butterfly-town/` and keep the relative structure. Map entry: `butterfly-town.tmj`. Script: `scripts/town.js`. No WAM, service, secret, backend change or external paid dependency is required. Existing maps are unaffected.

## Native behavior

- `start` marker begins on the lower gate approach.
- One guarded `WA.player.teleport()` moves between spatially separated scenes, landing outside return triggers.
- Room entry is position-driven, using native Tiled area feet coordinates (`y + 16`, inclusive edges).
- Visual visibility is local to the map script; there are no shared-state writes.
- Permanent collisions never hide. All roof, furniture canopy, focus, fog and effect layers are non-colliding.
- Furniture uses actual alpha cutouts, feet below `floorLayer`, canopies above. Pots alone block the two promenade olives. Perimeter cliff/garden scenery is outside the walkable area.
- The gate camera pulls back once on approach. Focus ownership is restored before another focus, preventing the fork's one-slot saved-zoom overwrite. Aspect-ratio changes and reduced-motion changes restore player follow.
- No control lock is acquired, including on teleport failure.
- Water, butterfly flow and lantern spill use native Tiled animations. Reduced motion retains steady illumination and hides loops.

## Validation status

Local release candidate. The repository TypeScript/Vite build, unmodified pinned Universe map validator, deterministic lifecycle tests, and focused Phaser/source-primitive browser checks are included in the source package. This is not a live Universe multiplayer session. Before deployment signoff, test the hosted map in the actual fork with two players, reconnect inside each interior, device orientation changes and room-map-editor permissions.

No push, merge, deployment or public hosting was performed for this package.
