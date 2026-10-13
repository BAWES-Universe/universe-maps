# Social Room / Outdoor Office 01

Separate unpublished review candidate copied from the approved roofless StudentHub mock. This is not the magical main map.

Open `map/studenthub-outdoor-office.tmj` with its relative tileset intact. The original artwork, native32 tile geometry and static furniture are unchanged. Three area objects now explicitly specify visible=true; rebuild source has the same correction. The stale roof-return waypoint label is corrected.

## Functional limits

- Static seating artwork; no sitting, seat reservation, movable furniture or work-app integrations are implemented. Seat-approach movement and return routes will be tested independently.
- No scripts, forced proximity interaction, silent property, paid generation, live room links or automatic meeting behavior. Actual multiplayer conversation behavior requires the target Universe runtime and a second client.
- Coarse32px permanent collision grid is unchanged. Furniture is below the player; glass and structural art are fixed foreground above the player. This is not per-object dynamic depth.
- No full Universe import, multiplayer or physical-device acceptance is claimed. Do not promote this candidate based on an offline render alone.
- `screenshot.png` is the archived composition with repeated avatars for scale, not a fresh browser screenshot or multiplayer session.

## Reproduction

From `source/`, run `python3 tools/build_template.py` with Pillow installed. It writes source/map and source/docs; it does not overwrite the candidate map. Preserve ART-PROVENANCE.md. This package does not grant new asset rights.

Parent source: https://github.com/BAWES-Universe/universe-maps/tree/03d83f2dd74108a6f75847bd2f7d03c5d619c950/map-mocks/studenthub-roofless-outdoor-office
