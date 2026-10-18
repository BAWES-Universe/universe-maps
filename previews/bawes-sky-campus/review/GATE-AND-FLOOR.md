# Gate capability review and restrained floor — 2026-10-18

**Smooth gate motion remains unresolved.** No replacement stepped animation is claimed as a fix. This pass removes the invented central geometric mark and continues the existing stone floor through the arrival route. Furniture, layout, exterior shell, proximity thresholds and collision timing are unchanged.

## Exact native-animation limitation

The pinned engine is `274114560c5ec95fdf8e51e67986a53069f3cf06`, with `phaser-animated-tiles` 2.0.2 loaded from its `src/plugin/main.js` (the package's actual main entry, not the obsolete dist bundle).

- Native Tiled animation is driven by Phaser `postUpdate`, so it avoids hidden-iframe timer stepping. It is suitable for continuously looping decoration.
- `postUpdate` advances to frame zero after the final frame, unconditionally. The animation clock advances independently of whether a particular gate is being approached.
- `GameScene.ts` handles `WA.room.setTiles` by calling `putTile` and then `animatedTiles.updateAnimatedTiles(x,y)`. The latter assigns the animation's **existing current frame**, rather than restarting at frame zero.
- The public iframe `room.ts` exposes tile replacement and layer visibility, but no animation restart, one-shot play, reversal, per-instance phase, or completion callback. Internal plugin pause/rate controls are not exposed through that map API.
- `loadTileset` rebuilds tilemap layers and colliders; it is not a supported gate playback/restart command and does not initialize a new controlled animation instance. Rebuilding the map on every entrance event would also disturb unrelated map state.

The [installed-plugin harness result](native-animation-capability.json) demonstrates the sequence `1 → 2 → 3 → 1 → 2`. Replacing the displayed tile with frame 1 followed by the same `updateAnimatedTiles` call used by the engine immediately assigns frame 2. This is a source-level harness using the installed implementation, **not a fabricated browser capture**. Reproduce with `node source/validation/native-animation-capability.cjs` in this environment.

Consequently, native tiles do not provide a reliable event-started, one-shot opening/closing sequence with completion-synchronized collision through the current supported map API. Hiding a looping animation or assigning a long last-frame duration does not supply the missing restart/completion controls. Directly touching the parent game's Phaser objects from the map would bypass the supported API; no such workaround was added.

## Other existing mechanism inspected

`WA.room.website.create` supports embedded HTML/CSS, but the `EmbeddedWebsiteEvent` schema has no pointer-pass-through option. `EmbeddedWebsiteManager` creates a DOM iframe at the supplied rectangle, above the canvas. A visual gate iframe would intercept movement clicks at the entrance; CSS inside the iframe does not make its parent iframe pass pointer events through. The overlay also sits outside native sprite depth ordering. No webpage overlay or custom movement forwarding was added.

## What remains in the candidate

The earlier map-local stepped gate remains explicitly unfinished. It opens collision early on approach, cancels a stale closing sequence when direction reverses, and closes collision only at the last closing frame. The previous [gate clip](gate-interaction.mp4) documents its stepping; it is from commit `74c7a1e`, before this floor-only correction, and is **not new evidence of smooth motion**. Smooth gate motion needs a supported event-controlled animation mechanism beyond what this pinned map API exposes, or a different approved non-animated interaction design.

## Current floor evidence

- [Actual-client interior with continuous stone arrival floor](runtime-full-interior.png)
- Same-camera [roof-visible exterior](footprint-exterior.png) / [interior](footprint-interior.png)
- [Full campus](runtime-campus-exterior.png)

The crude polygon is removed, not rebranded. No new logo is invented. Existing desk, meeting, lounge and reception arrangements remain untouched. No paid assets, image generation, engine changes, deployment or publishing were performed. Overall visual acceptance remains pending.

Verification: actual-client roof comparison retained identical camera/zoom/avatar coordinates; the native chair check passed. Footprint containment and optimized pixel/property/runtime equivalence passed. Git confirms no change to layout coordinates, runtime script or tracked engine files in this pass.
