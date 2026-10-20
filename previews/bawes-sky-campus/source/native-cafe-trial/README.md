> Status: cc62f45 failed independent visual review. The proportion/facing correction is documented in `proportion-revision.md`; latest evidence is under `sofa-final/`; `proportion-final/` retains the previous failed run. Earlier `whole-map/` screenshots are historical. No final visual acceptance is claimed.

# Native outdoor campus candidate

This isolated playable candidate restores the whole outdoor campus at native world-pixel resolution. It preserves the approved island arrangement, accepted office interior, gate, spawn and original runtime. The primary campus map and separate tower worktree are unchanged. No deployment or merge has occurred.

Open `review.html` for the map overview and normal-scale gameplay evidence. Load `playable/campus.tmj` in the pinned local Universe runtime; the local URL is `http://localhost:8000/_/global/localhost:8090/source/native-cafe-trial/playable/campus.tmj`. Keep the candidate inside this repository because it references original assets and runtime by relative paths.

## Artwork and registration

`panels.json` contains 18 generated landscape panels and their world coordinates. Each source is 1536×1024 and integrated at 1:1 scale. `generation-provenance.json` records source files, hashes, dimensions and integration status. The rejected square output returned 1254×1254 instead of 1024×1024; it is retained as evidence and never resized or integrated.

The café has a compact horizontal counter, four registered stools and a continuous wood floor. The conservatory has an integrated stone recess, low sofa and clear eastern entry. Native stone, foliage, cliffs, roofs and bridge surfaces now extend through the front plaza, central square, stage and portal garden. The stage retains all 32 seats.

Generated overlaps are not pixel-identical to their references. Hard native joins are used inside overlaps. The initial full assembly showed sky seams; the final integration clips panel backgrounds to the existing registered island alpha and retains the original continuous sky. Only this legacy alpha mask is resized to its existing world registration; generated artwork is not enlarged, blurred or feathered. Distant background islands remain the original softer scenery.

Opaque exterior artwork is restored while every original exterior alpha value is retained, including occupant apertures and translucent panes. Interior and gate layers remain byte-for-byte identical as map layer objects.

## Validation and limits

`static-checks.json` verifies local asset references, tileset dimensions, valid tile IDs, unchanged original layers and bounded collision changes. The 564 changed collision cells are within the counter approach, conservatory recess/entry and two upper bridge railing strips and eastern lamp plinth, plus corrected furniture footprints. The bridge strips previously allowed the avatar onto painted balustrades; the clear floor route now passes above them.

`whole-map/` contains ten gameplay region captures at camera zoom 1 and avatar scale 1. Those initial captures established reachability of all regions and office entry. The subsequent interaction run checks selected right-click seats, exits, corrected bridge routes, gate entry and two-client occupant visibility. It passed 32/32 checks before the final façade-strip/lamp-depth correction. The shorter final join run rechecks those affected routes, gate and two-client visibility. Results are recorded separately.

Earlier café records are retained: `bar-corrected-checks.json` passed 18/18 after the counter/mask correction; `runtime-checks.json` passed 36/36 on an intermediate café build. These do not establish whole-map acceptance. No sitting animation was added. The later candidate-only seating runtime adds a directional approach using public movement events/moveTo.

Rebuild with `python build-candidate.py`, verify with `python verify-candidate.py`, and capture the assembled native map with `python export-candidate.py gameplay-map-native.png 1664 2048 4864 3712`. Overview images are downscaled for review only. Gameplay scripts use the local pinned Universe client and Chromium CDP on port 9222.

Current review: independent reviewer confirms improved theater occupants, café sofa registration, west-bridge structure and continuous façade transition. Latest stool/conservatory captures are pending. Historical `whole-map/final-summary.json` describes the earlier candidate, not current acceptance. No user approval or deployment is claimed.

The existing draft PR branch received the implementation milestone `efcfcc8`. GitHub GraphQL and REST metadata lookups returned Forbidden in this environment; branch pushes succeeded. No PR title/body update was attempted after those lookup failures.
