# H025 and H039: art-independent recovery checkpoint

This is a **new, incomplete nonvisual derivation**, dated 13 October 2026. It is
not an original source archive, runnable illustrated map, replacement artwork,
freeze, deployment, or live-acceptance certificate. The original partial recovery
folders were preserved unchanged.

## What this adds

- **H025 Desert Star Caravanserai:** regenerates `design.json`,
  `visible-floor.json`, `layout.json`, and the emitted `caravan.js` wrapper from
  retained literal source. The layout contains 608 admitted cells, four rooms,
  22 anchors and two native-standing seat contacts.
- **H039 Paper Marbling Mill:** regenerates `layout.json` from retained design
  and exact builder statements: 277 admitted cells, two rooms, 16 anchors and two
  native-standing stool contacts. Its emitted interaction script reproduces the
  independently retained final SHA-256
  `96cc654f6a1cbfb83d4c0e14269e11f428912b5029b49f022ab067cf3d15ddf3`.
- No other newly derived file has an independently retained historical per-file
  checksum. Their checksums identify reproducible new derivations only.

## Source and execution provenance

`retained/` holds byte-for-byte copies of the specific recovered inputs.
`retained-inputs.json` pins each copied input and records its recovery source.
Those historical tools are evidence; do not run their complete art builders in
this incomplete package. `tools/recover_nonvisual.py` executes H025's unchanged
layout/floor generators into a new destination, then selects the exact retained
geometry and controller-emission AST statements. H039 uses unchanged retained
design and geometry/controller AST statements.

The only H025 geometry extraction substitution replaces the two uses of
`im.size` with `(1248, 1248)`, the dimensions of the original builder's explicit
image crop. Image loading, composition, atlas packing and TMJ generation are not
executed. This recovers declared collision faithfully without inventing pixels.

## Checks and honest limits

Run `bash tools/check_all.sh` with Python, Pillow, NumPy and Node available.
`REPRODUCIBILITY.json` records two fresh builds and comparison with all nine
shipped source/script outputs. Geometry reports freshly check 16x16 body
clearance, every declared whole hard footprint, room connectivity, and original
floor paths at no more than 0.5-pixel sample spacing. H039's full-width rectangles
are also checked at every integer body origin.

- H025's 19 retained controller cases run unchanged, including all 512
  clue/route/provision configurations and repeated door transitions.
- H039's 14 runnable controller cases retain their original bodies and mocks.
  One additional original case requires actual rendered artwork and is explicitly
  recorded **BLOCKED**. The full-suite `allPass` remains false. No fake pixel
  hashes or fabricated state-layer report are supplied.
- These are source geometry and supported-WA mock checks. They do not test
  actual-engine path following, real spawn randomization, GPU rendering,
  depicted-floor completeness, keyboard, touch, multiplayer or live behavior.
- No PNG, TMJ or WAM is created. The script directories intentionally contain
  only an interaction script, and are not deployable runtime bundles.

## Missing final-build imagery

H025 needs the original `art/masters/courtyard-r3.png`, `rooms-r3.png`, and
`packed-r1.png`. The room masters are asserted 1254x1254, then cropped to
1248x1248. H039 needs `art/masters/mill-r5.png`, `pattern-room-r1.png`,
`stools-r1.png`, and `patterns-r1.png`. The mill is resized to 1152x768 and the
pattern room to 768x768; the two art sheets use fixed whole-object crop boxes.

Those master bytes remain missing. Earlier prompt revisions are historical
evidence, not additional final-build inputs. Freshly generated replacements would
be new artwork requiring geometry re-registration and fresh visual/native/live
checks; they cannot reproduce historical TMJ or manifest hashes by assumption.

The existing partial folders preserve additional tests and dependencies not copied
here. The relevant complete prompt history and original output locators are copied
unchanged under `retained/`; see `ART-RECONSTRUCTION.md` for final-build contracts.
H025's complete final TMJ target remains
`370f6d1ad29138de7c9dc64bc5f8b2636b3c9e17bc2108c478f42da291a4c1a9`;
H039's remains
`25cb99347eb63e8c535215b12c2a01d23784254bf430ff2f4019ec2763d2b240`.
Neither is recovered by this checkpoint.
