# NEW restored06 binary roof reconstruction

This is newly implemented source derived from the exact restored06 map and script. It is **not** the unavailable lost07repair, and no equivalence with that lost artifact is claimed.

## Integration

Use Python 3.9+ and Node.js 18+; no package install or network access is needed.

1. Make a fresh copy of the restored native runtime.
2. Run `python apply_roof_patch.py /absolute/path/to/copied/map16` (or the copied directory containing `map16`, or the repository root).
3. Apply any separately reviewed geometry patches before or after this patch. This patch preserves all collision, tilesets, objects, artwork data, and unrelated metadata already present.

The callable packaging entry point is `apply_roof_patch.apply_roof_patch(directory)`. It writes exactly `magical-campus.tmj` and `scripts/adaptive-roofs.js`, and returns their relative paths and SHA-256 hashes. The exact restored input is protected against accidental in-place patching.

The pure map entry point is `patch_roof_map.patch_roof_map(map_dict)`. It returns a deep copy and changes only:

- `roof-translucent-shared.visible` to `false`, hiding the old shared 50% roof before script initialization.
- `campusRoofContract` JSON: adds `retainMargin: 16`.

The standalone map command is `python patch_roof_map.py SOURCE.tmj NEW.tmj`. It rejects identical input/output paths. Without an output argument it writes deterministic JSON to stdout.

## Behavior

- Native origin remains `(x, y)`; roof membership uses feet `(x, y + 16)`, with inclusive minimum **and maximum** rectangle boundaries.
- Each building hides its opaque roof upon entering its existing interior or approach rectangle.
- A revealed building stays revealed while feet remain within either of those rectangles expanded by one native tile (16 pixels). It restores only after leaving their expanded union. A fresh entry into only the expanded margin does not reveal the roof.
- Retention expands each actual rectangle separately; it does not create a large enclosing rectangle over unrelated exterior space. Building state is independent, including transitions between buildings.
- The shared translucent roof is never shown. Fixed foreground, shell/glass, posts, and permanent collision are never runtime visibility targets.
- Existing tileset metadata indexing, flipped-GID masking, interactive-tile rejection, movement revision guards, subscriptions, and reduced-motion effects behavior remain in place.
- The script and map contract must ship together. A missing/non-16 retain margin rejects initialization instead of silently using an incompatible map.

## Verification

Run in this directory:

```
node --test test-roofs.cjs
python -m unittest -v test_package.py
```

Tests use the immutable restored06 map at `/workspace/shared/recovered-campus06/public/butterfly-town/v6/map16/magical-campus.tmj`. To replay elsewhere, set `ROOF_BASE_MAP` to a read-only copy with SHA-256 `b3b124bd6bbb4ab573eb2848ca4681a58991a3e4a481a7dc1e0f046c62171696`. The baseline hash assertion deliberately prevents claiming tests against a different map are the same baseline verification.

Native body contract: parent-provided source audit of fork `6accae707e5a26bc56231ef241c64b397a5cea70` confirms container origin `(x,y)`, body `[x−8,x+8] × [y,y+16]`, and feet/depth `y+16`; `configureBody` uses container size 16×16, body size 16×16, body offset `(0,8)`. Archived source reference: `map-mocks/civic-rooms-01/source/qa/fork-primitives.js` at `03d83f2dd74108a6f75847bd2f7d03c5d619c950`.

South-contact regressions assert the full native body is clear immediately above the actual permanent collision row and contacts a solid row across its width, then initialize directly at that contact:

| Building | Origin | Feet / body bottom |
| --- | --- | --- |
| Classroom | `(544, 2064)` | `(544, 2080)` |
| Event | `(544, 2800)` | `(544, 2816)` |
| Office west | `(1200, 1504)` | `(1200, 1520)` |
| Office east | `(2400, 1472)` | `(2400, 1488)` |

The regression suite also covers all maximum edges, doorway jitter and re-entry, retention-only spawn, unrelated exterior corners, initial indoor spawn, several building transitions, stale initial/area position responses versus newer movement, reversed async refresh order, disposal during initialization/map loading/position fetch, reduced motion, collision-bearing flipped GIDs, untouched collision data and metadata, pure/deterministic/idempotent map patching, supported packaging directory shapes, composition, and rejection of incomplete/ambiguous trees.

These are source/map and mocked native-API tests. No browser run, heavy capture, engine edit, or publication was performed by this work package.
