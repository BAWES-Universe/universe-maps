# Mission Control Center

Category: Work. Native32 candidate: 48×32 tiles, 8 usable visual seats.

## Files and setup
- Host the complete map32 directory together; use map.wam for an editor-managed room, or map.tmj for base map rendering. Do not move atlases individually.
- Spawn, collision and single-cell spawn silence are built into TMJ. Seating is walk-to visual seating; no invented sitting animation or custom engine changes.
- Companion WAM defines bounded presentation and meeting areas using current native properties. Review/import in the Universe editor; conferencing and broadcasts require deployment permissions/services and are not live-tested.
- Screens are artwork only. Add your own document links, lesson materials or media destinations in the editor. No AI teacher, research integration or command data feed is implemented.

## Checks
All 15 seat/room anchors reached from spawn through collision-free tile cells. Base and foreground atlases round-trip exactly; floorLayer separates avatars from chair backrails. Occupied proofs insert a reference avatar at native scale. These are static compiled-map renders, not live room screenshots.

## Rebuild
Run python tools/build_environments.py from the parent source bundle (Python 3 + Pillow). The source-assets folder contains frozen reused native artwork. Source paths and provenance are listed in ASSET-PROVENANCE.md. No paid generation or new dependencies/services were used.

## Mission-control program
Six compact operator consoles use the modern native40px task-chair kit; two matching chairs sit at the briefing table. The bottom-right space is intentionally a flexible editor-ready bay with wall records cabinetry. It does not implement an incident-review workflow. Wall screens and console displays are decorative static artwork: there is no live telemetry, AI agent, bot, incident feed or external system integration.

Open room thresholds were cleared in the original artwork, and the octagonal command-floor collision follows a conservative interior polygon, excluding diagonal wall shoulders and peripheral equipment/grates. The main arrival grate is an intentional entrance floor surface, not an exterior equipment zone.

Modern-chair foreground was checked against every body-clear integer placement and all12 reference head poses. Unsafe edge pixels were moved below avatars without changing the combined empty-map artwork; safe lower-back occlusion remains. Exhaustive head conflicts0. All480 native route legs passed with683,618 subpixel body samples. No live browser/keyboard/media/device acceptance is claimed.
