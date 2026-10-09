# South arrival garden

Frozen local module for the magical campus. Native footprint **1472×576**, tile size32, world origin **(704,2480)**. Original raster art was generated with the built-in image generator; no paid API, deployment, or remote edits were used. The scene contains warm honey stone, teal mosaic accents, dense original planting, amber contact light and a finite low south border. There is no water, market, new gate, stair flight or claimed seating here. The original giant gate remains a separate host asset.

## Files to integrate

- `layers/avenue-base.png`: full native painted ground, plants, light and stonework.
- `layers/avenue-foliage-foreground.png`: native RGBA extraction of the painting's original path-facing leaf pixels. Draw above the avatar. No replacement props were generated for this layer.
- `layers/avenue-walkable-mask.png`: white is the exact nominal public corridor; black is blocked garden.
- `layers/avenue-collision-mask.png`: inverse of the walkable mask.
- `avenue-manifest.json`, `avenue-geometry.mjs`: native/world coordinates and continuous 16×16 lower-body collision beneath a unchanged32×32 avatar frame.
- `arrival-avenue.tmj`: Tiled image layers, collision rectangles and receiver/start objects. It does not configure a live portal or host-specific feature.
- `collision-grid-8px.json`: body-aware native samples, derived from the same geometry.
- `index.html`: local keyboard walking preview. Serve this directory over HTTP; it uses the exact supplied Greg spritesheet at32×32.

## Fixed registration

| Connection | Local center | World center | Nominal width |
| --- | --- | --- | --- |
| North to courtyard | (800,0) | (1504,2480) | 128px, x736..864 |
| West to stage cloister | (0,304) | (704,2784) | 96px, y256..352 |
| South arrival approach | (800,576) | (1504,3056) | 128px, x736..864 |
| Arrival spawn | (800,432) | (1504,2912) | Native32px avatar |

The host supplies the96×96 west cloister at world x608..704, y2736..2832, joining the civic stage door at(608,2784). There is no right branch. The host controls the original gate/portal transition; this module supplies the receiving garden and arrival point only.

The full north/south corridor has a nominal128px width including the low stone/teal paving shoulders. The central tessellated field is approximately96px wide at the north seam, matching the courtyard's visual use of shoulders. Collision treats those low shoulders as walkable; garden foliage stays outside this corridor. The left corridor is registered at96px total width. Decorative painted inlays are not interaction targets.

## Source and quality evidence

`art-source/avenue-master-03-layout.png` is the preserved2004×785 generated master used by the module. `art-source/AVENUE-STRICT-GEOMETRY-PROMPT.txt` and `avenue-layout-guide-no-water.png` preserve its prompt and guide. `art-source/registration.json` records source/destination rectangles. `package_avenue.py` downsamples nine source regions once directly into native coordinates. Every region is reduced: the largest scale is0.9231. No source region or completed painting is enlarged. This production registration corrects generator layout drift without repainting the artwork. Earlier source candidates are preserved locally for review, but are not integration assets.

`docs/avenue-native-greg.png` shows the final composition with the actual Greg frame at native32×32. `docs/avenue-native-geometry.png` shows the exact lane outlines and several native avatar placements. `docs/courtyard-avenue-seam-native.png` shows the north join using the supplied courtyard pixels.

`docs/geometry-verification.json` confirms continuous body traversal from arrival to each receiver, correct world coordinates, blocked gardens, and the absent right branch. Raster dimensions, mask polarity and source downsampling were checked. The optional browser smoke test is supplied as `docs/verify-preview.cjs`; its local launch was blocked by this execution environment's Chromium socket restriction, so no browser-run success is claimed. The host should perform its normal runtime integration checks.
