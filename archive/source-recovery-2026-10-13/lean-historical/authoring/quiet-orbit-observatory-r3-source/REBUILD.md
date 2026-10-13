# Quiet Orbit Observatory r3 | 24-seat seminar

Run `python tools/build_observatory.py` (Python3 + Pillow), then `node tools/verify_native_routes.cjs quiet-orbit-observatory` and `python tools/check_head_geometry.py quiet-orbit-observatory` (NumPy). No network or image generation is needed to rebuild.

The approved384px night-sky extension from r2 is byte-identical. This revision changes only seminar chair footprints: three rows, each containing two four-seat blocks, for24 seats. The center aisle is96px wide and side approaches remain clear. All24 anchors stay inside the existing native audience area, linked to the unchanged speaker area. Four research seats remain unchanged. Original architecture, telescope, lighting, floors, furnishings and non-seminar collision are preserved at1:1 scale.

Checks:1,232 native route legs,1,813,409 body samples,zero body collisions; all38 seat/room anchors reached. Exhaustive reachable head tests use the union of all12 frames of nine reference sprite sheets; zero conflicts. Atlas reconstruction, asset closure, native chairback layering, stage containment and exact non-seminar art preservation pass. Movement fixture commit60e7afdc3f96ef32525597cd46bd41175d61a2ef; stage source contract f00b3482f23c51976b4b339d7a891cad683d6498. After successful native stream join, SPEAKER/LISTENER statuses prevent proximity grouping. No extra silence or audio was added. Live AV and multi-user tests remain pending.

## Occupied proof and licensing
All24 seminar seats and4research seats are populated in static proofs by varied actual repository Wokas using native32 idle frames. No invented sitting poses or player actions. Raw Pipoya sheets are intentionally excluded from source archives. To reproduce varied proofs, use the named existing licensed repository sheets in source-assets/WOKA-PROOF.json, as source-assets/woka-proof-0.png through7.png. Without these, previews use the existing reference avatar; the runtime rebuild remains byte-exact. A derived head occupancy mask retains the full multi-sprite geometry test. Do not redistribute standalone Pipoya sheets.

Serve all map32 files together and import map.wam for native stage semantics. Review PNGs are static runtime-atlas renders, not live room screenshots. r1 and r2 are retained unchanged; r3 supersedes r2 seating.
