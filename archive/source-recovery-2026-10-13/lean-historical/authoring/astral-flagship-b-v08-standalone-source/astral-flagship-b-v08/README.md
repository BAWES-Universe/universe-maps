# Astral Concourse: garden B / v08

A separate garden/coffee variation built on the frozen corrected A core. Native32;2560×1920. The210 auditorium chairs,16 meeting chairs, corrected reception, four lounge areas and indoor foyer remain intact. Twelve casual seats use accepted native chair art. Seat counts are geometry, not concurrent-capacity claims.

## What changes

- Coherent outdoor timber removes the repeated stage-light bands from the coffee deck. Outdoor limestone replaces the repeated indoor garden tile; the gate landing is continuous.
- Two native low tables give the pavilion a coffee destination. Four north-facing chairs remain reachable around a128px central passage. Pavilion partners are48px apart; other casual pairs remain56px apart.
- Three small rooted leaf accents use the existing native animated-tile system, with four32px frames and gentle1–2px per-axis movement. No flashing, script-driven tile replacement or map audio. The native Disable animations setting pauses them.
- Spawn-only16-cell silence and native whole-hall entry focus carry over from A. Manual zoom remains available; the documented native rotation/resize limitation remains.

## Files and setup

Serve all ten files in `map32/` together. Use `grand-auditorium.tmj` for Custom TMJ. The adjacent portable WAM is a configuration candidate; Custom TMJ does not automatically import its meeting and broadcast areas. Follow [ROOM-SETUP.md](integration/ROOM-SETUP.md), back up actual room configuration and preserve its absolute mapUrl. No actual Universe room or media service was created by this package.

## Validation

Only four collision cells are added for the pavilion tables. All2,106 open cells connect,259 seat/landmark anchors are clear, and1,813,584 reachable integer body placements have zero tested head conflicts. Full native-source replay on merged60e7afd passes11,818/11,818 commands and32,352,365 swept samples, with no collision, unintended meeting entry, loop or mapChanged event. The actual pinned animated-tile plugin runs alongside5,302,552 movement frames in the fixture, emitting194,589 render-only events without changing raw map data or native properties.

The public dev build was verified as60e7afd, containing PR799, at20:04 UTC on2026-10-10. This is served-version evidence; these map checks are source/fixture tests, not authenticated gameplay, device performance, keyboard/renderer integration, live calls or concurrency testing. Fresh camera fit is checked separately; rotation does not fully pass. See `validation/ACCEPTANCE.md` for exact scope.

## Standalone rebuild

Python3 requires Pillow, NumPy and SciPy. All consumed inputs are bundled. Run in order:

```sh
python3 tools/rebuild_material_proposal.py
python3 tools/integrate_pavilion_composition.py
python3 tools/build_leaf_animation.py
python3 tools/integrate_pavilion_geometry.py
python3 tools/compile_runtime_b.py
python3 tools/verify_runtime_geometry.py
python3 tools/render_compiled_b.py
```

The historical extraction/optional-sketch tools are not rebuild steps. `source/frozen-a` holds the accepted predecessor raster/geometry inputs; `source/overlays` preserves original raw alpha/shadow ownership; the new material and leaf masters/prompts are included. The original A source also remains independently backed up and published for comparison.

Final independent review:29 schema/zone checks,30 garden/preservation checks and11 actual-candidate animation checks,70/70 passing against the frozen TMJ/WAM/grid/layout hashes. This is independent static/source acceptance, not live media/device acceptance.
