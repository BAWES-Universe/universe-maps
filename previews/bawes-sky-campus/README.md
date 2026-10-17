# BAWES sky campus — isolated review candidate

This candidate follows the approved sky-island concept retrieved from backup/bawes-build-transfer-2026-10-17 (96b79b7). It is a new map on feat/bawes-sky-campus; existing maps and the older rejected glass-campus preview are unchanged. No Azure resources or production deployment are involved.

The 8192×7168 world uses a 16px tile grid with native 32px Wokas at scale 1. The central office has a 2240×1440 full floor, 16 desks, two review tables, four enclosed meeting rooms, two lounges, a wide central aisle, and separate 192px front/rear entrances. The right wing accommodates shared StudentHub use. The surrounding campus retains the café, stage with 32 audience places, portal garden, bridges and outdoor arrival square. Portal scenery has no invented destination.

Furniture, chair fronts, walls, permanent collision, proximity doors and office cover are distinct layers. The cover hides locally inside when movement stops; nearby doors open during approach and close at rest. This avoids the pinned client replanning an active 16px-grid path for every visibility change. Its lower window band is translucent outside; this is a visibility treatment, not a multi-floor building. Shared meeting locks are courtesy controls in the apps menu, expire after 15 minutes, and always permit an inside occupant to exit. They are not access security or private audio rooms. No spawn audio, quests, unsolicited popups or baked navigation labels are added.

The standalone ZIP is a runtime review bundle. The editable source, original art, compiler and complete evidence live on `feat/bawes-sky-campus`; authoring commands below refer to that checkout. The repository optimizer rejects native16 tiles, so the direct map bundle bypasses it.

## Reproduce

Run `python3 source/build.py` (Pillow and NumPy), then `python3 source/validation/geometry.py` from this directory. The compiler retains source art and editable pixel geometry. Source concept scenery remains decorative outside the separately authored office, chairs and café tables; it is not a complete editable tile-by-tile conversion of every decorative plant.

For the recorded local engine at `274114560c5ec95fdf8e51e67986a53069f3cf06`, run `bash source/runtime/run-local.sh`. Open `http://localhost:8000/_/global/localhost:8090/campus.tmj`. This uses the environment's installed Node22 and dependencies, local backend/pusher/Vite and a CORS map server. Stop with Ctrl-C. Desktop movement uses arrow keys or right-click; touch uses short tap. No special engine patch is included.

`campus.tmj`, `runtime.js` and the complete `assets/` folder must stay together when hosted. Source art, compiler and review evidence are not runtime requirements.

## Review limits

The script uses local map variables; the local development server explicitly disables server-side persistence and variable permission checks. Meeting locks are ephemeral. Separate audio/video room properties and a StudentHub destination require real destination/configuration details.

Scenery extends beyond all walkable sides. The engine's unrestricted Explore camera can pan outside any finite map; padding cannot guarantee scenery for arbitrary pan or zoom. Measured supported-view results are recorded separately under `review/` rather than claiming an engine-wide guarantee.
