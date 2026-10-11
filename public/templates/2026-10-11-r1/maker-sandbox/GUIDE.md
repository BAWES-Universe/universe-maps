# Inventor’s Sandbox Workshop

A bright brick inventor workshop with three flexible creation pads, six native tool-bench seats, an idea-board bay, and a two-seat collaboration corner.

Category: Sandbox. 48×32 tiles at native32 scale (1536×1024 pixels). 8 walk-to visual seats.

## Using this template
Host the complete map32 folder together. map.tmj contains the architecture, furniture, collision, safe spawn, and spawn-only silent layer. map.wam adds native editor-ready room-area semantics; its mapUrl is relative. Import or review these areas in your Universe editor before deployment. No service was activated.

Coral, mint and ochre creation circles are flat walkable floor paint. Built-in north and west tools/benches remain solid and reachable from the hall. The southeast wood nook has a real broad doorless opening on its left. The idea board, workbench tools and creation pads are decorative editor-ready placeholders; no tools, bots or services run automatically.

## What is functional
- Tile collision, connected circulation, random spawn containment, and local spawn-only silence are authored in the TMJ.
- Seats use the current native32 reference body and walk-to floor-click positions. No invented seated animation, sprite scale change, custom engine behavior, or player is baked into the map.
- Meeting areas use current native WAM room definitions. Media, multi-user audio/video, and editor import have not been tested live.
- Screens, research desks, creation pads and tool areas are editor-ready decorative destinations. No CRM connection, AI bot, research service, external tool, or data feed is active. Add only your own approved links and services.

## Verification
VALIDATION.json reports the source/atlas round trip and authored anchor checks. NATIVE-ROUTES.json replays actual pinned source-derived native moveTo, path fitting, return, same-cell and sequential routes at 60 Hz with body samples at ≤0.5 pixels. HEAD-GEOMETRY.json decodes the actual TMJ and checks exhaustive integer native-body placements against all 12 reference avatar head frames. Static occupied images are compiled-atlas renders, not live room screenshots. See each check's exact scope.

## Rebuild
The self-contained rebuild ZIP contains frozen original art, compiler, avatar review fixture and pinned native movement fixtures. Install Python3, Pillow and NumPy, plus Node.js for native route tests. From its root run python tools/build_environments.py maker, then node tools/verify_native_routes.cjs inventors-sandbox-workshop, then python tools/check_head_geometry.py inventors-sandbox-workshop. This rebuild requires no API, credential, paid provider, network request, engine patch or generation call.

Original architectural art was generated with the built-in image tool; existing approved native furniture is documented in ASSET-PROVENANCE.md. No publication or existing project overwrite occurred.
