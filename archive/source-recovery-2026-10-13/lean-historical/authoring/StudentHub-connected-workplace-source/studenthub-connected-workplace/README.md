# StudentHub: one connected workplace

This is a construction and visibility proof for review, not a finished replacement campus. It is a separate 960 × 768 world with a 32px avatar and tile grid.

Two neighboring workstations, a four-person shared table, a compact sofa/rug corner, and an adjoining four-person glass meeting room share one floor and planted perimeter. The meeting room is reached through the opening in its west glass wall. No departmental buildings or transport links divide the team.

## What the method changes

The previous campus expanded isolated destinations and placed furniture from whole-image bounds. That produced distant chairs and inconsistent material scale. This proof instead assembles original material patches, separately authored architectural pieces, furniture grouped by visible seat/tabletop edges, and planting that follows the foundation.

The original architecture, planting and material masters are independently downsampled once to their authored world footprint. The generator then packs unchanged native 32px cells into one 1024px atlas. Source resolution is not a claim of high-DPI gameplay support.

The glass, wall base, permanent collision, furniture and removable cover are independent. Entry hides only the cover; the glazed rear shell, perimeter and meeting partition remain. Glass is visually transparent while its physical footprint remains solid. The doorway is excluded from that footprint.

The two tabletop groups use opposing chair artwork. Chair legs tuck beneath the table and seat faces approach the tabletop. These are standing approaches in the current engine, not sitting animations.

## Files and use

- `map/studenthub-proof.tmj`: importable finite map; its images and script are relative
- `map/scripts/studenthub.js`: roof-only entry/exit behavior and initial-position catch-up
- `tools/build_proof.py`: deterministic assembly from original sources and reusable props
- `art-source/`: original generated material, planting and architecture masters
- `assets/`: native pieces and semantic layer renders
- `layout.json`: proof bounds, spawn and continuous walking checkpoints
- `qa/`: independent Phaser 3.86/Arcade browser harness, unchanged Greg and pinned fork primitives

Run `python3 qa/server.py --port 8816` and open `http://127.0.0.1:8816/qa/` in a local browser. Controls support keyboard, tap-to-walk, touch movement, 1×/2× review, a narrow portrait viewport and reduced motion. The recorded walk is continuous movement, including entrance, commons, adjoining room, visible glass, rear approach and exit restoration.

The static composition in `docs/interior-native.png` includes repeated unchanged avatar sprites only to illustrate simultaneous scale. Browser captures contain one actual moving avatar. All preview pixels come from the authored map; they are not generated concept art.

## Scope and limits

The existing giant magical gate, v1, v2 and v3 artifacts are untouched. The gate's scale/reveal remains the baseline for a later integrated campus. This small proof does not claim that the complete magical art direction has been accepted.

The preview uses actual Phaser rendering and Arcade physics with a local WA message adapter. It is not the full Universe application or a physical-phone test. Static TMJ furniture cannot dynamically sort around a player from every side. No bots, CRM, meeting service, stage broadcast, permissions or new sitting behavior are configured. Functional interiors are silent; no audio source is started.

Reference images and third-party map artwork informed construction only. They are not included or copied into the authored map. The conference-campus stage reference uses compact chair banks, clear aligned aisles, a split lectern and roof/facade reveal; its inspected script does not configure a live broadcast stage.
