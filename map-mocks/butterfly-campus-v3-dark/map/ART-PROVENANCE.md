# Original art and native-resolution contract

All new raster art was generated for this candidate with OpenAI's built-in image generation. No third-party paid image provider, copied commercial sprite pack, reference-image extraction or external API key was used.

The supplied architectural images were inspected as layout and mood references only. No pixels from them ship in the map.

## Original sources

- furniture-original.png: independently isolated tables, individual desks, four chair facings, four couch facings, rug, coffee table, lamp and olive pot.
- architecture-original.png: independent bookcase, window, doorway, workbench, podium, planter and lamp.
- room-shell-original.png: empty architectural master. Real limestone/walnut wall strips were extracted as structural components. Furniture is never baked into that master.
- parquet-original.png and ground-original.png: original material textures, separately tiled for floor surfaces. Material repetition represents actual paving/wood/grass and never extends scenery beyond the deliberate island boundary.
- hq-roof-original.png, creative-roof-original.png, learning-roof-original.png, operations-roof-original.png and research-roof-original.png: independent, distinct building roof/exterior sprites.
- stage-original.png: independent original proscenium/backdrop sprite.
- landscape-original.png and landscape-alpha-extraction.png: original foliage, garden, fountain and market sprites, with true generated alpha. See assets/outdoor-provenance.json.
- gate-original.png and gate-arch-original.png: reused original project-owned artwork from the earlier Butterfly Gate, now placed at or below its original native dimensions rather than expanded.

## World scale

World tiles and the user's unchanged Greg Woka are32px. Most furniture renders24–128worldpixels across. A larger room means additional floor and circulation; furniture is not inflated to fill it. Source artwork is downsampled once for its chosen native world dimensions. Atlas padding does not change visible object dimensions.

This fork currently samples map tiles at their authored world dimensions. This candidate does not claim extra Retina texture density, arbitrary-zoom sharpness, a new sitting animation, or dynamic Y-sorting for static TMJ furniture. Only true alpha wall/tree/furniture overhangs render over the character; floor/rug/threshold pixels remain below.

## Runtime assets

PNG atlases use32px tiles. No Tiled image-layer or resized-object workaround is required. Atlas generation deduplicates identical material cells and packs only occupied cells. All references are local to this candidate folder. Audio is absent from the executable candidate.

## QA-only assets

qa/greg.png is the previously accepted avatar sheet, byte-for-byte copied for testing. It is not a replacement Woka and is not installed or published to a user account. Phaser and AnimatedTiles are existing source-harness dependencies, retained under their original licensing.
