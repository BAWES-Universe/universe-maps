# Studio r8 and Reading r4: RECONSTRUCTED editable source

Created 13 October 2026. This is a new authoring workflow reconstructed from exact surviving runtime bytes. It is not the lost original source archive. No artwork has been regenerated, and no deployment is included.

## Build and test

Requires Python 3. Standard library only.

- `python tools/build.py --out /absolute/path/to/new-runtime-directory`
- `python tests/verify.py`

The output directory must not already exist. A clean rebuild uses only `source/` and the new compiler; no runtime fixture or earlier archive is needed. All 11 output files match the frozen delivered fixtures byte for byte (Studio 5, Reading 6, including its README).

## Editing

- `source/<map>/map.recipe.json`: map settings, layer metadata, object areas, tilesets. Layer data points to CSV files.
- `source/<map>/layers/*.csv`: one row per map row, one tile GID per column. Studio is 30 by 27; Reading is 24 by 16. Preserve dimensions unless also updating the map specification.
- `source/<map>/areas.wam.json`: editable audio/conversation areas and map link.
- `source/<map>/art/`: exact recovered runtime PNG tile atlases. These are the surviving editable pixels, not recovered high-resolution or layered masters.
- `source/<map>/extras/`: original non-map runtime files copied unchanged.
- `source/runtime-baseline.json`: immutable acceptance hashes; do not change these to conceal a divergence. New designs should get new revision baselines.

A grid-edit test proves the compiler consumes editable inputs, and an invalid-grid test checks rejection. Structural tests validate GIDs, layer sizes, PNG atlas dimensions, spawn and map references. Fresh grid analysis finds all 177 Studio and 100 Reading unblocked cells connected to their respective spawns. This is only a tile-grid diagnostic, not native physical-body route testing or inherited historical route claims.

## Preservation and provenance

The exact fixture is Rendering-Investigation.zip version 2, Library identity `libfile_9d5b832cfa2481918ac133db5bc17b09`, members under `Rendering-Investigation/fixture/assets/studio/` and `reading/`. Original files are untouched. `source/provenance.json` records the scope and missing items.

Older Studio context/design/movement source and Reading r1/r2/Garden versions remain preserved separately. They are design history, not replacements for these latest frozen runtimes. The reconstruction intentionally does not import older geometry or artwork into the latest maps.

## What remains missing or unverified

- Original r8 and r4 complete source archives, original authoring scripts, unflattened artwork/masks not retained in runtime, and original full validation evidence.
- Pixelation/black-edge complaints are preserved as open issues. Byte-identical reconstruction does not fix them.
- Live GPU/zoom/viewport tests, native avatar/body routes, foreground/head-depth checks, desktop/touch and multiplayer acceptance have not been run here.

The build preserves exactly the surviving experience bytes. It does not establish that missing original editable masters have been restored, or certify the previous unresolved rendering concerns.
