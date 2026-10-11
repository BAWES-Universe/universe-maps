# Olive Arabic Academy

Category: Knowledge. Native32 candidate: 48×32 tiles, 22 usable visual seats.

## Files and setup
- Host the complete map32 directory together; use map.wam for an editor-managed room, or map.tmj for base map rendering. Do not move atlases individually.
- Spawn, collision and single-cell spawn silence are built into TMJ. Seating is walk-to visual seating; no invented sitting animation or custom engine changes.
- Companion WAM defines bounded presentation and meeting areas using current native properties. Review/import in the Universe editor; conferencing and broadcasts require deployment permissions/services and are not live-tested.
- Screens are artwork only. Add your own document links, lesson materials or media destinations in the editor. No AI teacher, research integration or command data feed is implemented.

## Checks
All 32 seat/room anchors reached from spawn through collision-free tile cells. Base and foreground atlases round-trip exactly; floorLayer separates avatars from chair backrails. Occupied proofs insert a reference avatar at native scale. These are static compiled-map renders, not live room screenshots.

## Rebuild
Run python tools/build_environments.py from the parent source bundle (Python 3 + Pillow). The source-assets folder contains frozen reused native artwork. Source paths and provenance are listed in ASSET-PROVENANCE.md. No paid generation or new dependencies/services were used.

## Revision2 geometry notes
- North-facing chairs have solid rear clearance cells, so a player can enter/leave the seat laterally while the backrail cannot swallow a head from the south.
- The left arrival door leaf is solid; the central64px entrance stays open. Study entrances are flat96px doorless limestone thresholds, deliberately opened in the source artwork.
- Exhaustive integer-position check found zero head/foreground conflicts above courtyard y512. Remaining38,924 positions are intentional olive-canopy occlusion, not hidden chair or wall defects.
- Native source replay:1,024 legs with1,866,085 <=0.5px body samples, including edge clicks and same-cell targets; zero failures. Live browser/keyboard/network/media acceptance is still pending.
