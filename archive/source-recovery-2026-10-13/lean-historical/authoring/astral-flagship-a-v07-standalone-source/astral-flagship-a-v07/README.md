# Astral Concourse: corrective A / v07

A separate corrected baseline for comparison with the preserved earlier maps. Native32; 2560×1920; 210 auditorium chairs, 16 meeting chairs and 12 casual chairs. These are artwork/geometry counts, not supported-user capacity.

## Improvements

- Accepted stage and auditorium art remain exact. Meeting chair/table art is preserved.
- Twelve weak stools replaced by accepted north-facing lounge chairs at their original native scale; close low tables and clear approaches.
- Wider, clearly marked reception with staff access,64px return and96px customer apron. Old cramped booth and invisible collision padding removed.
- Middle lounge side clearance widened to64px, keeping its single entrance and unchanged communication rectangle.
- Silence restricted to the16-cell spawn receiver, down from333 circulation cells.
- Native whole-hall focus on entry; following restores on exit. No scripts or layer/collision switching.
- Existing top-down garden doors, paths and pavilion remain connected. Exterior material redesign/animation belongs to separate version B.

## Use

Serve every file in `map32/` together with relative paths intact. `grand-auditorium.tmj` is the Custom TMJ entry. The adjacent portable WAM is a setup candidate, not something Custom TMJ automatically imports. Follow [the safe room setup guide](integration/ROOM-SETUP.md) before configuring media areas. Create a separate room; do not replace an existing room map URL without backing up its actual WAM.

## Validation and limits

The final frozen artifact passed independent29 zone/schema checks and30 repair/preservation checks. All2,110 open cells connect,259 seat/landmark anchors are clear, and1,821,010 reachable integer body placements have no tested head/foreground conflict.

The source-extracted native movement replay covers11,818 commands per source pin. Unpatched90a148c passes11,802 normal movements;16 known same-cell fallback probes remain explicitly recorded. Merged60e7afd passes all11,818 commands. Both have zero body/head collisions, unintended meeting entries, trapped routes or mapChanged events. Camera-only focus was separately executed against native camera/scale classes and real Phaser camera math. This is source/fixture validation, not a live network/browser/keyboard/device/load test.

Fresh whole-hall framing passes the tested initial portrait/landscape/desktop cases. Native orientation-change behavior has a known stale-zoom/padding limitation; full rotation acceptance is not claimed. Portrait whole-hall fit makes avatars small; manual zoom remains available. Merged PR799 deployment and all actual media operation remain unverified.

## Rebuild

Use Python3 with Pillow and NumPy. From this package root run, in order:

```sh
python3 tools/integrate_cleanup.py
python3 tools/compile_runtime.py
python3 tools/verify_runtime_geometry.py
python3 tools/render_reviews.py
```

All assembly inputs are bundled under `source/`; no external working directory is required. Earlier `*prototype*` tools preserve experiments and are not part of the final rebuild. Portable route replays are in `validation/native-routes/{current90a,merged60e}` and use Node.js plus bundled EasyStar0.4.4; run `node validation/native-routes/merged60e/route-audit.cjs .`. No engine code was changed by this map package.

See [provenance](PROVENANCE.md), [validation summary](validation/ACCEPTANCE.md), and `RUNTIME-MANIFEST.json` for exact runtime hashes. Preview actors are reference overlays only; the Greg sheet is not a runtime dependency.
