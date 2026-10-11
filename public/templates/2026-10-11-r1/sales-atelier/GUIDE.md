# Art Deco Sales Atelier

A brass, teal and walnut urban sales atelier with two private client bays, eight research desks, and an intimate briefing alcove.

Category: Work. 48×32 tiles at native32 scale (1536×1024 pixels). 14 walk-to visual seats.

## Using this template
Host the complete map32 folder together. map.tmj contains the architecture, furniture, collision, safe spawn, and spawn-only silent layer. map.wam adds native editor-ready room-area semantics; its mapUrl is relative. Import or review these areas in your Universe editor before deployment. No service was activated.

The central compass is a flush floor inlay. Client bays each have two native lounge seats and a low brass table. Eight laptop desks support research work; the northern board and two briefing seats form a small presentation destination. Broad central circulation remains social and nonsilent.

## What is functional
- Tile collision, connected circulation, random spawn containment, and local spawn-only silence are authored in the TMJ.
- Seats use the current native32 reference body and walk-to floor-click positions. No invented seated animation, sprite scale change, custom engine behavior, or player is baked into the map.
- Meeting areas use current native WAM room definitions. Media, multi-user audio/video, and editor import have not been tested live.
- Screens, research desks, creation pads and tool areas are editor-ready decorative destinations. No CRM connection, AI bot, research service, external tool, or data feed is active. Add only your own approved links and services.

## Verification
VALIDATION.json reports the source/atlas round trip and authored anchor checks. NATIVE-ROUTES.json replays actual pinned source-derived native moveTo, path fitting, return, same-cell and sequential routes at 60 Hz with body samples at ≤0.5 pixels. HEAD-GEOMETRY.json decodes the actual TMJ and checks exhaustive integer native-body placements against all 12 reference avatar head frames. Static occupied images are compiled-atlas renders, not live room screenshots. See each check's exact scope.

## Rebuild
The self-contained rebuild ZIP contains frozen original art, compiler, avatar review fixture and pinned native movement fixtures. Install Python3, Pillow and NumPy, plus Node.js for native route tests. From its root run python tools/build_environments.py sales, then node tools/verify_native_routes.cjs art-deco-sales-atelier, then python tools/check_head_geometry.py art-deco-sales-atelier. This rebuild requires no API, credential, paid provider, network request, engine patch or generation call.

Original architectural art was generated with the built-in image tool; existing approved native furniture is documented in ASSET-PROVENANCE.md. No publication or existing project overwrite occurred.
