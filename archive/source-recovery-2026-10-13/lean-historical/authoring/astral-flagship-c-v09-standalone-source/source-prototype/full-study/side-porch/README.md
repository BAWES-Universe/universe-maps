# C: native east side porch

This is a small native side-entry module for the parent's full-shell visual study. It is not a runtime or collision change. All files are confined to this directory, and no rejected v06 architecture was reused.

## Review

- `review/east-side-native-review-sheet.png`: original 32px Greg in the hall exterior, early reveal, and inside; the identical translated module at the foyer door; native comparison with approved A chairs.
- `review/hall-outside-occupied-native.png` and `review/foyer-outside-occupied-native.png`: unmarked 1:1 local crops.
- `review/hall-registration-native.png` and foyer equivalent: separate diagnostic overlays.
- `assets/east-side-complete-native.png`:240×360 native transparent asset.

Only local 512×512 context crops were assembled here. Whole-world placement is the parent's task.

## Shape and source

The first two generated masters are retained but rejected: they portrayed a south-facing arch beside a continuous sidewall. The third master follows an explicit code-native geometric guide and produces an attached axis-aligned side canopy. It does not invent a frontal doorway to make an edge-on east wall easier to see.

The original 1024×1536 master is intact. It is reduced once by exactly 15/64 in BOTH axes to 240×360. There is no crop, rotation, stretch, selective rescale or texture tiling. Original prompts and all masters are retained. The structural derivative removes disconnected or diffuse alpha outside the largest alpha≥128 component. Visible RGB is unchanged; only RGB of fully transparent native pixels is normalized to zero.

The canopy's west edge overlaps the same tall wall band containing the doorway. The roof projects east from the wall. It is not a hole in the roof, a raised landing or a separate floor rectangle. There is no floor art in this module: the persistent base layer is genuinely transparent, so A's unchanged paving remains beneath it.

## Registration

- Native canvas: 240×360
- Local threshold: x64, y216..312; 96px clear north/south walking interval
- Hall origin:(1600,488), giving threshold x1664, y704..800
- Foyer origin:(1600,1384), giving threshold x1664, y1600..1696
- Main door/post vertical rise: approximately 104px; original 32px Greg is unchanged
- South ground jamb footprints:(49,312)..(82,342) and(140,312)..(175,342), entirely outside the 96px route
- North ground jamb footprints inferred from the guide/elevation:(49,183)..(82,215) and(140,183)..(175,215); the canopy hides them naturally in the closed image
- Any-alpha native bounds:[24,3,176,343), so the easternmost world art pixel is x1775,15px beyond the initial approximate 1760 porch limit
- Opaque structural bounds:[27,5,173,341)

North ground footprint positions are a source-geometry registration, not a collision claim. The canopy is about 166px north/south in projected roof depth and its supports stand roughly 104px. Mainwall art naturally extends screen-up above the footprint. Parent integration must join that wall band into the full shell.

## Projection and reveal

The floor axes are horizontal/vertical. Vertical elevation projects straight up. Therefore the east wall is viewed edge-on, and the southern jamb and porch supports naturally project over the ground doorway in the closed view. That is correct occlusion for this projection. A south-facing fake arch is deliberately absent.

An early reveal is required before walking under that closed silhouette. Suggested east approach trigger: center x1832 while moving west, with re-close x1864. At the trigger the original full 32×32 Greg frame has its west edge at 1816. Every nonzero new structure pixel ends by 1775, leaving 40 clear pixels. Hide foreground, porch roof and contact shadow immediately. Keep it revealed while inside, on the approach, or if spawned/teleported inside. Parent should union this with the whole-building reveal region; side-specific illustrative y ranges are hall 432..880 and foyer 1328..1776. These are source proposals, not a runtime implementation or speed-validated fade.

## Layers and validation

`assets/` and `masks/` contain matching base, foreground, porch-roof and shadow files. The base is fully transparent. Foreground and canopy exactly partition the generated native assembly. Contact shadow is a restrained derivative from the actual southern feet, offset 2px with low opacity; it hides together with the structure.

`validation/source-proof.json` verifies byte-exact RGBA reconstruction, a zero-opaque-pixel base, and the 40px east trigger margin. It also records sampled revealed 32px-frame route checks against the new above-actor art. Revealed local floors and furnishings are the exact A source layers. None of this substitutes for collision, player-controller, camera, audio or live-gameplay validation.

Rebuild: `python tools/assemble_side_porch.py` with Pillow, NumPy and SciPy. Read `module-manifest.json` for full registration, source hashes, evidence and limits.
