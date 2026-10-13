# Social Room / Outdoor Office 01

Separate unpublished derivative of the approved roofless StudentHub mock. It does not replace the magical main map.

Open `map/studenthub-outdoor-office.tmj` with its relative tileset. The world remains960×768 pixels, with native32 map cells and unchanged32×32 Greg. The full original permanent collision grid, including both solid tables, is preserved.

## Concrete changes

- Three area objects explicitly declare visible=true.
- Four near-side table chairs move down8px into reachable floor. Exact original backrest pixels are separated into foreground; no chair or table is repainted.
- Original tabletop pixels sit above far-side occupants. Foreground leaves each authored head's top10px clear.
- Eight table positions and clear egress routes are authored in source/seat-contract.json. No sitting animation, interaction lock, reservation or additional game feature is introduced.
- Original artwork and the parent map are retained. Recombined furniture layers exactly reproduce the furniture composition with the four documented relocations.

## Rebuild and check

Run `python3 revision-tools/build_native_seats.py`, then `python3 revision-tools/verify_art_and_schema.py` and `python3 revision-tools/verify_geometry.py`. Pillow is required. The older source/tools/build_template.py reproduces the historical base, not this derivative; run the revision compiler afterward.

## Functional limits

- Static authored table positions support the normal avatar. Desk and lounge furniture are decorative and are not advertised as authored seats.
- No script, generic silent property, forced conversation, ambient audio, external destination, WAM meeting configuration, or movable editor entity is included.
- Standalone Phaser movement, original-source touch-path behavior, and analytical clearance have separate evidence. These do not establish full Universe import, live multiplayer/proximity conversation, or physical-device acceptance.
- Full target repository schema/build and live client import have not been run. Local structure and asset roundtrip validation are included.
- The archived screenshot.png is historical. Current browser captures, when present, live under evidence/. Occupants in test captures are fixtures, not live multiplayer.

## Source

Parent: https://github.com/BAWES-Universe/universe-maps/tree/03d83f2dd74108a6f75847bd2f7d03c5d619c950/map-mocks/studenthub-roofless-outdoor-office

Preserve ART-PROVENANCE.md. No new paid art or generation was used. This package grants no additional asset rights. An abandoned8px collision-grid experiment was rejected because of native pathfinding/body compatibility; the deliverable uses native32.

Final fidelity correction: actual native tap rerun passed16/16 with Player immovable=false and pinned WOKA_SPEED9 (180px/s). See evidence/native32-source-tap-immovable-false-results.json; prior true/speed6 evidence is superseded. Launch validation/tap/tap-browser-immovable-false.html for this final configuration.
