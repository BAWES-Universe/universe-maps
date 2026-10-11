# Quiet Orbit Observatory

Category: Knowledge. Native32 candidate: 48×32 tiles, 12 usable visual seats.

## Files and setup
- Host the complete map32 directory together; use map.wam for an editor-managed room, or map.tmj for base map rendering. Do not move atlases individually.
- Spawn, collision and single-cell spawn silence are built into TMJ. Seating is walk-to visual seating; no invented sitting animation or custom engine changes.
- Companion WAM defines bounded presentation and meeting areas using current native properties. Review/import in the Universe editor; conferencing and broadcasts require deployment permissions/services and are not live-tested.
- Screens are artwork only. Add your own document links, lesson materials or media destinations in the editor. No AI teacher, research integration or command data feed is implemented.

## Checks
All 22 seat/room anchors reached from spawn through collision-free tile cells. Base and foreground atlases round-trip exactly; floorLayer separates avatars from chair backrails. Occupied proofs insert a reference avatar at native scale. These are static compiled-map renders, not live room screenshots.

## Rebuild
Run python tools/build_environments.py from the parent source bundle (Python 3 + Pillow). The source-assets folder contains frozen reused native artwork. Source paths and provenance are listed in ASSET-PROVENANCE.md. No paid generation or new dependencies/services were used.

## Observatory program
Four research stations, an eight-seat seminar bay and a complete clockwise/counterclockwise route around the telescope. Telescope barrel and plinth, outside mountain art and curved rails are solid exclusions. The instrument was moved south in the original source artwork to make the north route genuinely open; no route runs through the instrument. The telescope and display panels are decorative. There is no research-data feed or telescope-control integration; attach your own documents/media in the editor.

Verification includes720 native route legs with1,048,314 body samples, including the whole telescope ring in both directions, and zero exhaustive reachable foreground-head conflicts. Live room/media/device verification remains pending.
