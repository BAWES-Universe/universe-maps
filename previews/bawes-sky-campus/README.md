# BAWES sky campus — replacement interior preview

The interior candidate now uses matching furniture and detailed source columns, piers, rails, plinths and planting around genuinely transparent amber panes. The earlier flat-wall version was rejected; this is its architectural correction. See [replacement implementation and evidence](review/REPLACEMENT-INTERIOR.md). This is an isolated review candidate; visual acceptance remains with the user.

This candidate follows the approved sky-island concept retrieved from backup/bawes-build-transfer-2026-10-17 (96b79b7). It is a new map on feat/bawes-sky-campus; existing maps and the older rejected glass-campus preview are unchanged. No Azure resources or production deployment are involved.

The 8192×7168 world uses a 16px tile grid with native 32px Wokas at scale 1. The 2144×592 interior now has two individual work settings, one four-place shared project table, curved reception, two outward-facing sofas with four occupied anchors, and two enclosed four-place meeting rooms. There are 19 indoor anchors and 52 outdoor anchors. A 192px arrival spine and entrance, 96px meeting doors and 96px between-room route support circulation. The open shared campus leaves room for StudentHub use without inventing a destination. The café now has a registered timber surface, matching curved lounges and bar-side stools, plus matching benches at the existing outdoor locations. Stage and conservatory restoration remain separate; portal garden and square geometry are unchanged.

Furniture, segmented chair/sofa/reception fronts, transparent orthogonal glazing, walls, permanent collision, proximity doors and office cover are distinct layers. The cover hides locally inside when movement stops; nearby doors open during approach and close at rest. This avoids the pinned client replanning an active 16px-grid path for every visibility change. Outside, opaque structural artwork surrounds transparent window apertures showing clipped native interior art and live occupants. The interior floor appears only within its masonry boundary in the local cutaway; upper façades do not add navigable storeys. Shared meeting locks are courtesy controls in the apps menu, expire after 15 minutes, and always permit an inside occupant to exit. They are not access security or private audio rooms. No spawn audio, quests, unsolicited popups or baked navigation labels are added.

The standalone ZIP is a runtime review bundle. The editable source, original art, compiler and complete evidence live on `feat/bawes-sky-campus`; authoring commands below refer to that checkout. The isolated Vite configuration explicitly sets the optimizer to 16px and preserves the current Universe client API. The shared root configuration still defaults to 32px; it is unchanged.

## Reproduce

Run `python3 source/build.py` (Pillow and NumPy), then `python3 source/validation/geometry.py` from this directory. The compiler retains source art and editable pixel geometry. Source concept scenery remains decorative outside the separately authored office, chairs and café tables; it is not a complete editable tile-by-tile conversion of every decorative plant.

For the recorded local engine at `274114560c5ec95fdf8e51e67986a53069f3cf06`, run `bash source/runtime/run-local.sh`. Open `http://localhost:8000/_/global/localhost:8090/campus.tmj`. This uses the environment's installed Node22 and dependencies, local backend/pusher/Vite and a CORS map server. Stop with Ctrl-C. Desktop movement uses arrow keys or right-click; touch uses short tap. No special engine patch is included.

`campus.tmj`, `runtime.js` and the complete `assets/` folder must stay together when hosted. Source art, compiler and review evidence are not runtime requirements.

## Isolated optimized build

From this candidate directory, run `node ../../node_modules/vite/bin/vite.js build --config vite.config.ts`, then `python3 source/validation/optimization.py`. Use the saved Node22 binary if the shell Node version differs. The output is `dist/`; the equivalence check compares every used tile pixel and tile property, layer order and map dimensions. The candidate config changes no engine code or shared tooling. It retains `runtime.js` instead of the optimizer's generic remote-API HTML wrapper.

See `review/GATE-AND-FLOOR.md` for the current floor and unresolved smooth-gate limitation; `COMPOSITION-PASS.md` records the preceding furnishing pass; `FOOTPRINT-REDESIGN.md`, `SEAMS-AND-COMPOSITION.md`, `COMPOSITING.md`, `REFINEMENT.md` and `COMPOSITING-CHECKPOINT.md` describe earlier checkpoints.

## Review limits

The script uses local map variables; the local development server explicitly disables server-side persistence and variable permission checks. Meeting locks are ephemeral. Separate audio/video room properties and a StudentHub destination require real destination/configuration details.

Scenery extends beyond all walkable sides. The engine's unrestricted Explore camera can pan outside any finite map; padding cannot guarantee scenery for arbitrary pan or zoom. Measured supported-view results are recorded separately under `review/` rather than claiming an engine-wide guarantee.

The rear exit and external service floor were removed because they extended into sky behind the building. Existing plaza paving connects the front threshold to outdoor spawn. The beverage prompt and its prompt-dependent steam trigger are removed, with no replacement popup or control. Existing native movement and courtesy-lock controls remain. Gate appearance and behavior are unchanged; its stepped motion remains a known limitation.

Outdoor restoration is now tied to the exact original attachment: see [source comparison, native audit and bounded restoration needs](review/OUTDOOR-RESTORATION-AUDIT.md). The bounded café reconstruction is documented in [café restoration](review/CAFE-RESTORATION.md), with [remaining stage and conservatory scope](review/REMAINING-DISTRICTS.md). The earlier candidate assessment records source QA before integration.
