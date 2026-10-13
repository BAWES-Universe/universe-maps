# Deterministic map catalogue previews

These previews are assembled from the recovered TMJ layer data and the **existing PNG pixels** referenced by its tilesets. Packed atlases are reconstructed tile by tile. The renderer does not generate or replace artwork, alter the original maps, or run the games.

## Reproduce from a complete repository checkout

Requires Python 3 and Pillow (the checked preview manifest records the version used).

```sh
python tools/map-collection/test_render_previews.py -v
python tools/map-collection/render_previews.py \
  --catalog archive/runtime-recovery-2026-10-13/CATALOG.json \
  --root archive/runtime-recovery-2026-10-13 \
  --output docs/map-collection/previews
```

The renderer supports the finite orthogonal tile/group layers used by all 80 candidates, inline tilesets, layer order, first GID lookup, spacing/margins, offsets, visibility, opacity, tile transformations, transparent pixels, and animation at its first defined frame. Unsupported visual constructs fail clearly. Area, collision, audio, and other non-visual object outlines are not drawn into the scene. Transparent logic tiles contribute no visible pixels. Source maps are read only.

The resulting 480-pixel maximum-dimension thumbnails preserve the full authored world extent and aspect ratio, without cropping or color adjustment. Opaque scenes use JPEG quality 86 with no chroma subsampling; a scene requiring transparency uses PNG. Contact sheets add labels and a neutral presentation background; this is not part of the map artwork. Exact input, render and output hashes, dimensions, skipped layers and per-map warnings are in `docs/map-collection/preview-manifest.json`.

## Interpretation

- These are static source previews using **initial authored visibility**, not live game screenshots or proof of acceptance.
- Runtime scripts, WAM entities, player avatars, audio, interactions and camera-dependent behavior are not executed.
- Keeper's Return and Butterfly Town contain separated spaces in large authored canvases. Their overview thumbnails retain that layout, so individual rooms appear small.
- Gate A v6 and Gate B v4 have pixel-identical initial scenes. Both runtime records retain their own filename and source hashes; the image does not establish runtime equivalence.
- Source artwork is preserved at its original paths; compact JPEGs are review derivatives, not replacement assets.

[Tiled GID specification](https://doc.mapeditor.org/en/stable/reference/global-tile-ids/) and [layer specification](https://doc.mapeditor.org/en/stable/manual/layers/) inform the rendering rules.
