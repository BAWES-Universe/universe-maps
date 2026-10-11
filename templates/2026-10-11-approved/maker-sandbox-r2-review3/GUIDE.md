# Inventor’s Workshop r2

A native32 brick, brass, green and oak workshop with three open creation pads, six indoor workbench places, a four-place collaboration nook and a two-place outdoor workbench. South testing court, west doorway, north terrace and garden landing are connected usable destinations. Side garden paths connect via the visible doors/courtyard; planted bases stay solid. 48×36 tiles /1536×1152 pixels.

## Runtime
Host map32 together and import map.wam/map.tmj in the Universe editor. No engine changes, scripts, new audio, integrations or service activations. Native bounded LiveKit meeting-area metadata is supplied for the collaboration nook; live multi-user, AV and editor import are untested. Spawn silence is confined to the one start tile. Screens, tools and creation pads are decorative/editor-ready placeholders, not running tools.

## Seats and proof
All12 authored taps were replayed through pinned source-derived native pathfinding/movement and land exactly at stool/body anchors. Existing native standing idle frames illustrate occupancy; there is no new seated animation. The primary occupied proof is reconstructed from runtime atlases at actual tested arrival endpoints, not a live game screenshot. Furniture silhouettes are inside their solid tile cells; stools are walkable visual destinations. Every walkable cell is connected; exhaustive head tests cover nine local reference sheets /108 frames.

## Rebuild
Python3 + Pillow + NumPy and Node.js. Run python tools/build_workshop.py, node tools/verify_native_routes.cjs inventors-sandbox-workshop, python tools/check_head_geometry.py inventors-sandbox-workshop. Generation is not needed for rebuilding. Frozen source masters are included. Build and checks are local; no API, credential or purchase required. Raw Pipoya sheets are deliberately excluded; standard proof falls back to the existing reference avatar, and the derived head-union mask preserves runtime safety. Supply your licensed repository Woka sheets locally for varied preview rebuilding.

## Review limits
Routing uses pinned unmodified source extracts in a stub scene, not browser/network/physics gameplay. The regular replay return targets the nearest native floor-fit point (spawn Y minus1); independent QA separately verifies true-spawn return behavior. No publication or deployment has occurred.
