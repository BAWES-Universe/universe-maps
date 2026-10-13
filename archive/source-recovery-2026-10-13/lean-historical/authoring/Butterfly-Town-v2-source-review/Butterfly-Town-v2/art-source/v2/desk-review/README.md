# One StudentHub desk review

Review-only replacement for the **left StudentHub table group (index 0)**.
No other room or furniture group is redesigned. The map generator is owned by
the integration worker; this helper does not write the map or its atlases.

## What this demonstrates

- A separate walnut/brass desk and teal chair at the existing room scale.
- One reachable **standing work position north of the desk**, facing down.
- Clear eastern approach and a newly freed southern passing aisle.
- The chair is parked alongside and has a blocking footprint. This is **not
  sitting behavior** and is not a claim of four-sided seating or object Y-sort.
- `standing-workspace-review.png` uses the unchanged project's `qa/greg.png`
  as a 32px scale reference. It is not the owner's customized avatar.

## Reproduction and integration

Run `python3 tools/desk_preview.py`. The helper writes only this review folder.

Import `arrangement` from `desk_preview`. Its `feet` and `canopy` outputs are
full-room 448×288 alpha images. Skip StudentHub furniture index 0 in the old
generator loop, composite these replacements, and use their two collision
rectangles instead of the original (64,192,96,32) rectangle. All other indices
remain unchanged. See `manifest.json` for exact local/world coordinates.

The standing center is local (128,136), world (2592,744), accounting for the
existing test body's x=-8..7 and y=+8..23 footprint. A north-side work position
at y144 would penetrate the solid table row; do not use that earlier sketch.

## Checks completed

- Visual inspection of generated source, packed sprites, native room, and
  three 3× nearest-neighbor screenshots.
- Reachability from the room entrance on the current map collision grid.
- Every 1px sample along the proposed approach path, checking nine points
  across the existing collision-body footprint.
- Correct table support cells, clear standing/approach cells, and release of
  the old south-chair blocking strip.
- Feet and canopy alpha have no overlap.

These are deterministic static checks. The integrated result still needs a
real Phaser walk from the doorway to the work position, collision contact,
front passing, and full-fork verification. The table uses the existing fixed
TMJ depth split, not per-object dynamic depth. Entrance-crop fixes are separate.

## Asset provenance

`generated-source.png` was made with the built-in image-generation tool on
2026-10-08, using `art-source/town/interiors-furniture-alpha.png` as a style
reference, with `transparent_background=true`. The source alpha is retained.
Sprite packing uses cropped source object bounds and proportional Lanczos
downsampling, followed by a deterministic depth split; no character changes.

Final prompt:

Use case: stylized-concept. Asset type: one transparent 2D game furniture sprite
sheet for a charming magical university, matching the reference's rich
hand-painted warm walnut wood, tiny brass gold trim, teal velvet, warm book
pages and carefully shaded outline. The reference is style reference only.
Produce exactly TWO fully isolated objects on a TRUE transparent background,
generous transparent separation, no floor, no rug, no room, no text, no people,
no ground glow. LEFT two-thirds: one practical straight-on rectangular writing
desk, facing south/down, camera tilted down 35 degrees as in a top-down 2D
WorkAdventure game, symmetrical flat horizontal front edge, NOT isometric
diagonal. Clearly readable small tabletop with ONE open book, ONE small warm
brass lamp at back-left, a small closed teal book at back-right, generous clear
workspace; four short visible slender wooden feet. No chair attached or behind
it. Compact overall width-to-height 1.35:1; tabletop occupies upper 55% of
silhouette, short feet below. Do not make it a giant counter. RIGHT one-third:
one separate small chair, straight-on facing south/down, matching the desk,
rounded teal upholstered backrest, clearly visible comfortable seat cushion,
walnut slender legs with brass details, entire chair including feet. Chair
silhouette height approximately same as desk's height; chair width approximately
45% of desk width. Its seat center and feet must be especially legible. Match
the original cozy detailed game-art aesthetic without noisy texture,
photorealism, generic flat pixel art, modern furniture, heavy carved throne
proportions or angular camera perspective. Keep both objects unoccluded and
independent so they can be placed and collision-tested separately in the game.
Background must be alpha transparency, not a checkerboard illustration.
