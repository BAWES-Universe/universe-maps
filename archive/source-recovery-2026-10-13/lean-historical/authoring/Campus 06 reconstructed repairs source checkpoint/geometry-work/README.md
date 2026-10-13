# Revision06 geometry: NEW reconstruction

This patch is freshly derived from the restored native map and atlas pixels. The unavailable lost repair reportedly opened three fountain cells. Its coordinates and hash were not recovered. This reconstruction opens two inspected pavement connector cells and makes no claim of matching that lost patch.

## Changes

- Open collision cells `(101,114)` and `(100,115)`. These are the two connecting cells in the ring's only diagonal-only 2×2 pinch. The diagonal from `(100,114)` to `(101,115)` now accepts a swept 16×16 body in either direction. Adjacent planter/greenery `(100,116)` stays solid. Every other permanent collision GID is unchanged.
- Clear 18 fixed-foreground GIDs: row 189, columns 173–181 and 186–194. Their 2,304 nontransparent pixels are already present identically in the base layer. The native artwork therefore remains unchanged, below the player, with no new artwork or atlas. Only the duplicate foreground strip that overlaps the legal contact position is removed; all side foliage and other foreground GIDs are unchanged.
- No runtime/player-following masks, collision mutation, scaling, service, remote write, or generated art.

## Apply and test

Requires Python 3 and Pillow. Keep `geometry_patch.py` beside `geometry-source-evidence.json`.

    python geometry_patch.py /path/to/copied/native-runtime

The target may be a copied map16 directory or the TMJ itself. The function `apply_geometry_patch(target)` modifies only that TMJ. `apply_to_map(source)` returns a patched deep copy. Both are deterministic and idempotent. The restored baseline path is refused. Independent roof metadata/property changes can be applied before or afterward.

Run tests against the original restored map and optionally verify the integrated output:

    python test_geometry_patch.py --source /path/to/original/map16 --greg /path/to/original/greg.png --patched /path/to/copied/native-runtime

Six tests passed. A 53-segment route winds fully around the fountain; its 16×16 body is swept at half-pixel intervals clockwise and counterclockwise, including diagonal motion. Source/pixel tests verify no other collision changes, native base/foreground pixel equality, static scenery equality, retained foliage, and patch idempotence.

For both central booth interaction fronts, every integer position in each rectangle has a clear full 32×32 sprite envelope. This is stronger than the alpha footprint of any of the 12 restored Greg moving frames:

- Books: player center x=2784–2896, body-top y=3040–3120
- Curios: player center x=2992–3104, body-top y=3040–3120

This head-clear guarantee covers those central interaction fronts. Decorative side foliage and pillars remain foreground; positions under that decoration are not claimed clear. No live Universe or browser physics test is claimed by this package.

## Evidence

- `geometry-source-evidence.json`: baseline SHA-256, exact old/new GIDs and rationale
- `fountain-source-cell-evidence.png`: actual native pixels for opened connectors and retained planter edge
- `fountain-route-evidence.png`, `ring-route.json`: full body-safe ring route
- `books-greg-before-after.png`, `curios-greg-before-after.png`: original 12 moving frames at the same contact position, before/after static layering
- `geometry-verification.json`: bounded verification summary
- `make_geometry_evidence.py`: deterministic source-pixel evidence generation
