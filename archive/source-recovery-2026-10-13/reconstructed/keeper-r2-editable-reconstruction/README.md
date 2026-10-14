# Keeper’s Return r2: editable reconstruction

This is a new source reconstruction made on 13 October 2026 from the retained original r2 runtime. It is not the recovered original authoring project. All 16 texture files and the controller body are original surviving bytes. No scenery or artwork was regenerated.

## Build

Python 3 and Node 24 are sufficient; no network or package installation.

    python3 tools/build.py --report evidence/runtime-comparison.json
    python3 tests/structure.py
    node tests/controller.cjs
    python3 tools/clean_rebuild.py

For a source-only checkpoint that omits PNGs, materialize the existing Library runtime archive using the supported Library workflow, then run `python3 tools/restore_art.py /path/to/lighthouse-keepers-return-r2-runtime.zip`. `source/art-provenance.json` pins the archive and each exact member. The restorer checks every checksum before writing and refuses to overwrite changed artwork.

The default build must match every original runtime file exactly. For intentional later edits, use `--allow-edits` and a new output directory; its result is a new candidate, not original r2. Do not change the immutable `source/runtime-baseline.json` merely to hide a mismatch.

## Editable source

- `source/map.json`: map settings, inline tileset definitions, original layer order and references.
- `source/layers/*.json`: each original layer's settings, objects, properties and order.
- `source/layers/*.csv`: tile GIDs, one map row per line; 128 columns and rows. Layer arrays are reconstructed from these grids.
- `source/anchors.json`: interaction positions, radii, doorway links and labels recovered from the controller's original layout preamble.
- `source/controller.js`: unchanged surviving controller body. The build prepends anchors in the original compact representation.
- `source/room.wam.json`: editable original WAM configuration.
- `source/art/*.png`: the 16 original shipped texture files, with hashes pinned by the runtime baseline.

The compact runtime serialization is intentional to reproduce the shipped JSON/JavaScript bytes, while source JSON is human-readable. No original runtime TMJ or runtime ZIP is needed by the emitter.

## Fidelity and missing originals

The reconstructed emitter can reproduce shipped map/controller/texture bytes. It does not recover high-resolution image-generation masters, original generation prompts, authoring scripts, original geometric masks, original native-fixture test suite or pre-loss proof receipts. The original source ZIP was historically 64,727,545 bytes/122 members; this reconstruction must not be described as that archive.

The delivered script keeps state per visit and preserves it during same-map doors/stairs. It does not provide persistent or shared state, sitting poses or forced facing. Original r2 review remained unpublished, with full-game camera, physics, touch, popup, network and multiplayer checks outstanding.

The new tests establish deterministic emission, structure and controller behavior in mocks. They do not replace original native movement replay or real game/device acceptance. Any defects found in unchanged original behavior are reported without silently altering the byte-identity target.

## Provenance

Runtime: Library `libfile_05a64ebd22288191b9116a05b38ac49b`, `lighthouse-keepers-return-r2-runtime.zip`. Source data extracted locally from this runtime without mutation of the archive or recovered runtime tree. Review contract: `Lighthouse-Keepers-Return-r2-Review.pdf`, Library `libfile_f38fbc2024348191b327456bd209af63`. The user requested preserving the outdoor version while adding enterable buildings as a separate map.

Original textures remain independently preserved in Library. Keep small reconstructed source/tools/tests in source control and verify backup read-back. No deployment, merge or artwork generation is part of this reconstruction.

## Known inherited runtime defect

Independent review found a teleport-rejection recovery race in the unchanged original controller: a delayed `getPosition()` response after a failed teleport can replace a newer movement event with a stale interaction position. The initialization path guards a similar race, but the rejection-recovery path does not. The standalone failing regression is kept under `evidence/known-issues/`; it is deliberately separate from the 19 existing passing mock scenarios. No claim that all controller/gameplay scenarios pass is made.

The original controller is preserved to satisfy byte identity. Fixing this defect must produce a separately labelled revision, with a new runtime hash and independent validation; it must not silently overwrite the retained r2 runtime.
