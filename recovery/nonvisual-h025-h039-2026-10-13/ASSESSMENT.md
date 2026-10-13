# Recovery boundaries and concrete next steps

13 October 2026. Based on the retained files inspected for this checkpoint.

## Which missing maps have enough surviving implementation evidence?

- **H025-r2:** saved layout/floor generators, builder and controller can reproduce
  the authored nonvisual design, collision and puzzle behavior. This checkpoint
  implements that derivation. The illustrated map still needs its three final
  raster masters and a complete fresh source/native/render/live test run.
- **H039-r1:** saved design, builder and final controller reproduce authored
  geometry and marbling behavior. Re-emitted JavaScript matches the retained
  original final checksum. The illustrated map still needs four raster masters.
- **H009:** the preserved material represents an earlier deliberately unfrozen
  Mechanical Orchard candidate, not H009-r3. `advance`, `fresh`, `phases` and
  `visible` define the three-cam/four-beat local state machine, and
  `define-layout.py` specifies orchard/cam-house geometry. Both 64-pixel
  inter-island aisle gates fail in the historical candidate; `freeze.py`
  deliberately refuses to freeze it. Re-emitting this earlier controller/grid
  would not recover the missing final r3 geometry. Its current builder requires
  `orchard-master-r5.png`, `cam-house-master-r1.png`,
  `orchard-phase2-master.png` and `orchard-phase3-master.png`.
- **Other 30 missing H identities:** the inspected evidence ledger establishes
  names, versions, some target hashes and historical review summaries. It does
  not contain the actual source, authored coordinates or raster masters required
  for faithful reconstruction. Names and historical PASS labels are insufficient
  to recreate their maps without new design decisions.

No embedded image bytes or complete deterministic pixel-generation recipe were
found in the H009/H025/H039 retained text. Their image-generation prompts and
UUID filenames are references, not raster assets. Builders crop, scale and pack
the absent raster masters; those operations cannot synthesize their contents.

## Media House r9 boundary

The restored original/r6/r7c sources are useful and should remain immutable. The
existing partial reconstruction changes two bench-front source/test landmarks to
`(240,800)` and `(784,800)` and changes the TMJ title. Its PNGs and WAM remain
byte-identical to r7c, and its TMJ is semantically identical after removing the
name property. These landmarks are not exported as interactable entities by the
compiler. They prove closer standing-floor targets; they do not change gameplay
geometry or implement sitting/facing.

### Benches

Protected bench/planter rectangles remain `[112,704,384,800]` and
`[640,704,912,800]`. Current route evidence reaches floor clicks `(240,816)` and
`(784,816)`. Useful next verification is clicks on the actual bench artwork and
departure in both directions. Moving farther north needs defensible collision
changes or re-authored depicted solids; more metadata landmarks do not fix it.

### Top-right plant/wall

The `voice-planter` fixture remains `[688,336,720,368]` and the horizontal wall
remains visible. World region `[663,329,834,379]` is pixel-identical to the original
master after its recorded half-scale transform and offset `[128,192]`. The
original contains the same obstruction; no clean original donor under it was
found. Opening collision through that depicted wall/plant is not a valid repair.
Cloning neighboring floor would constitute newly authored scene content.

### Entrance and glow

Historical `expand_r7.py` pastes r6 rectangle `[0,80,768,608]` at `[128,176]`,
ending at world y=704. Region `[408,572,618,704]` is entirely pixel-identical to the
half-scaled master, which ends at that lower edge. The separately retained
`r7b-preserved-south-entry-strip.png` is a 128x96 donor for world
`[448,800,576,896]`; it does not repair the building-threshold boundary near
y=704. A new blend/registration using exterior art would be a new design choice,
not an established recovery of r9.

### Lower-right rug

Most rug pixels already match the registered original clean-seat master. Current
differences largely contain intended chairs/table and narrow floor strips made
by historical `rebuild.py`, stretching local y=270..274 into y=256..270 while
compacting keyboard cabinets. A narrowly masked restoration of demonstrably
damaged rug-border pixels from that same master is technically possible. It must
preserve current furniture and be labelled a new source-derived correction.
There is insufficient evidence that this explains or resolves the complete r9
blur complaint; wholesale rug replacement may undo established furniture work.

### Exact implementation surfaces for a new, separately labelled Media repair

- Keep `tools/reconstruct.py --original` byte-exact. A new visual derivative
  needs an explicit patch stage with per-region donor provenance and a guarantee
  of zero pixel changes outside named repair masks.
- Change `source/layout.json` fixture/grid data only when verified art edits make
  genuinely clear floor. Keep historical r7c and existing bench test anchors.
- Reuse `tools/build_maps.py`'s `Map.compile()`, `validate()` and `render()`;
  no replacement compiler or generic map template is needed.
- Decode emitted atlas/TMJ and compare with authored planes, run exhaustive
  physical-body/head and protected-fixture checks, then native routes. Add actual
  artwork bench clicks, departures and recording-passage targets.
- Review the rug border and y=704 seam at native scale, followed by real
  keyboard/touch/GPU rendering. Offline composites cannot certify live results.

The retained Media delivery evidence contains the prior assistant's repair claim
and inaccessible comparison-attachment references. It does not supply actual r9
pixels or an exact r9 build recipe. This assessment made no Media edits.
