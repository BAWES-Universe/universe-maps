# Cardinal meeting furniture

Original furniture authored with the built-in `image_gen.imagegen` tool, then mechanically registered at native scale. No paid API/CLI fallback, reference-pixel copying, source engine changes, publishing, bots, live meeting wiring, or avatar enlargement was used.

Start with `proofs/meeting-furniture-review-sheet.png`. The authoritative empty and occupied native proofs are `proofs/small-four-cardinal-{empty,occupied}-native.png` (256×192) and `proofs/conference-six-{empty,occupied}-native.png` (256×384). Diagnostic 3× images use nearest-neighbor scaling. The review sheet presents 2× copies and crops only the conference proof's unused vertical margins.

## Delivered original assets

`source/` contains all six full-resolution, original alpha masters, each exact generation prompt, and `generation-record.json` with the built-in tool's returned file paths. `guides/` contains the technical source-coordinate silhouettes used as edit targets. The guides were created before generation; their reproducible geometric construction is in `tools/make_guides.py`. The workstation source and its actual Phaser proof were inspected for camera, palette, and scale only; no furniture reference pixels were copied into these assets.

The generated images retained approximate object proportions but drifted in transparent padding. `tools/package_assets.py` therefore trims the largest alpha≥32 connected object's bounding box and resizes it in premultiplied RGBA to the required native visible dimensions. The original alpha masters remain unchanged. This is recorded explicitly as registration, not a claim that the generator obeyed every source pixel. No sprite is rotated or reflected. East and west are separate purpose-authored views with upper-left light.

| Native sprite | Canvas | Measured visible bounds, half-open | Visible size |
| --- | --- | --- | --- |
| Each N/S/E/W chair | 48×64 | (9,8)–(39,44) | 30×36 |
| Small table | 128×96 | (16,16)–(112,80) | 96×64 |
| Conference table | 224×128 | (16,16)–(208,112) | 192×96 |

Alpha bounds are measured at thresholds 1, 16, 64, 128, and 240 in `asset-manifest.json`. The manifest also contains source canvas dimensions, exact crop rectangles, SHA-256 hashes, native/source-coordinate foreground polygons, and measured foot/contact-band bounds.

## Small room geometry

The four-cardinal layout fits the 256×192 interior. Coordinates below are room-local. The west doorway occupies y64–160. The table's collision envelope is (80,64,96,64), matching the registered visible extent; the tabletop is (80,64,96,48). The chair itself is a walkable seat allocation, as in the validated workstation calibration.

| Place | Avatar center | Avatar faces | Original Greg frame | Chair origin |
| --- | --- | --- | --- | --- |
| North | (128,48) | South | 1 | (104,16) |
| South | (128,128) | North | 10 | (104,112) |
| West | (72,88) | East | 7 | (46,56) |
| East | (184,88) | West | 4 | (162,56) |

All avatar frames remain 32×32 at scale 1. The collision body remains x=center−8, y=center, width=16, height=16. At each seat the body is tangent to the correct table edge. The two quiet-room world origins are (2144,480) and (2144,704).

## Conference geometry

The 256×384 room contains a 192×96 visible table/collision envelope at (32,128). Three south-facing seats at (64,112), (128,112), and (192,112) face three north-facing seats at (64,224), (128,224), and (192,224). Every chair is the same 30×36 native sprite used in the small room. No enlarged conference chair or diagonal facing is used. The doorway is west, y160–256; a 32 px west side lane connects its interior center to the north and south seat approaches. World origin: (2144,928).

## Rendering and occlusion

For integration use each `assets/{layout}-empty-native.png` as transparent below-player furniture, then unchanged directional avatar frames, then `assets/{layout}-foreground-native.png`. Individual original sprites and component masks are also available. The aggregate foreground is specific to this furniture arrangement; retain correct scene depth logic when integrating moving avatars.

- North-facing chair: substantial, traced upholstered back above the torso, native measured bounds (11,19)–(39,39). It is not reduced to a narrow strip.
- South-facing chair: near ends of both armrests and the seat lip are foreground; rear arm sections remain behind the head. The initial incorrect whole-arm mask is archived.
- East/west chairs: the actual near horizontal armrest is foreground. These are original lateral sprites, not rotated north sprites.
- Small table: two disjoint source-pixel edge contact pieces at the side occupants' hand/lower-body height. No table foreground covers protected head pixels.

Every visible foreground pixel is an unchanged RGBA pixel from its registered native source asset. Masks select source contours; they do not paint cover-up shapes. Contact layers preserve source foot and small shadow pixels within the documented contact band. They are not new collision obstacles.

## Checks and limitations

`proofs/route-checks.json`: all 10 seat entry paths and their exact reverses pass 2,594 1 px body samples with the table and every other occupied seat body blocked. `geometry-plan.json` contains every waypoint, full sprite/body bounds, chair origin, facing, and frame index. The small room does not need enlargement under these dimensions. This is an offline geometric check, not an engine collision or multiplayer test.

`proofs/pixel-checks.json`: all 10 occupied fixtures preserve every opaque/nonzero pixel in the protected top 14 avatar rows; foreground covers 106–233 torso pixels per fixture. The unchanged Greg sheet hash is included. These repeated Greg sprites are explicitly scale fixtures, not live multiplayer users, and use existing standing directional frames; no seated animation is claimed.

`archive/attempt-01-initial-layering/` preserves the first empty/occupied/geometry proofs, manifest, and compositor before the south arm layer partition was corrected. It records the initial 13 protected hair pixels covered per south-facing fixture. All six generation attempts and full prompts remain in `source/`; nothing was discarded.

Reproduce the offline check and proof with:

1. `python tools/build_geometry.py`
2. `python tools/package_assets.py`
3. `python tools/make_review_sheet.py`

Runtime integration, actual seat interaction/claims, avatar animation, multiplayer, audio, and meeting behavior remain outside this art deliverable.
