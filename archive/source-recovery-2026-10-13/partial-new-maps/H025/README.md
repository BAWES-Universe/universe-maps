# H025 — Desert Star Caravanserai

An original irregular adobe caravan courtyard, covered cistern, woven saddle benches and provision packing bay stand inside a continuous desert scene. The south gate leads to a usable sandstone-rimmed arrival apron. Three north doorways enter two distinct guest cells and a roof-stair chart room in the same map. Every doorway has an explicit return action. The stair flight leads to an actual usable upper landing and returns to a broad lower landing.

## Local visit experience

Record three fictional clues at the cistern, wind-ribbon guest cell and landmark guest cell. Their combined answer is the star → arch → crescent itinerary, exactly two flasks, dates and a cloth sunshade. Choose an itinerary at the chart table or packing bay; cycle the flask count and toggle the two other provisions, then explicitly Pack panniers. Incorrect choices retain all clues and selections. Success visibly fills the two panniers and places three gold route seals on their table. Editing a selection explicitly empties the packed result so it can be packed again. Repeated recording and repeated completed packing are harmless.

All progress survives each same-map room transition. Close is nondestructive. Inspect nearby reopens prompts; prompts can be paused. Reset requires a separate confirmation. Full map reload starts a fresh local visit. No online account, shared multiplayer state, timer, audio, real travel advice or avatar riding is implemented. Only the two native32 tiles containing every actual initial full-body landing are socially silent; all ordinary destinations remain outside the silent area.

## Art, geometry and native scale

Seven fresh built-in imagegen masters, their exact prompts and provenance are preserved under art/. Runtime uses the final courtyard-r3 and rooms-r3 original whole scenes at a1:1 pixel scale. Each1254×1254 master contributes its1248×1248 top-left viewport, omitting only six scenic edge pixels; there is no enlargement, repeated texture construction, floor repainting, padding or prior-map scene reuse. The three distinct interiors are drawn once in their original companion scene. The successful packed-r1 table crop is the single initially hidden state layer. Its8,849 changed pixels lie entirely in blocked packing-fixture cells; collision never changes.

The world is39×78 native32 tiles. Main courtyard lanes, gate, room aisles and lower stair landing have wide physical routes. The narrow stair flight and north-of-cistern shortcut use tighter incidentals with exact native-body fitting proofs, not a64px claim. Coarse cells containing real wall, curb, planter, bench-foot or stair-edge fragments remain blocked, including thin floor fringes. Entire covered-cistern architecture is inaccessible, including its roof projection; actors cannot walk on its painted canopy. No tall swinging doors overlap usable approaches. All three exterior thresholds enter real rooms, and all three interior thresholds return.

Both theme-specific woven saddle benches have exact native contacts at(344,719) and(936,719), independently recorded using actual final-direction frames4 and7. All103 and101 lower-body alpha pixels respectively contact their cushion regions. Genuine low front furniture strips are the only foreground masks; the complete opaque ground remains underneath. These are unchanged native standing/perch-contact proofs, not automatic sitting or facing.

## Rebuild

Entry: map32/map.tmj loads local caravan.js. Optional map32/map.wam references that map and defines no separate conversation areas.

Run sh tools/rebuild.sh with existing Python3, Pillow, NumPy and Node24. No network, install, paid API, browser, server or socket is needed. All dependencies used by the native fixture are vendored. source/ contains authoritative controller, art-selected geometry/floor data, actor sheets and provenance, historical source/API pins. tools/author-layout.py and tools/author-floor.py preserve editable authoring recipes. Rebuild generates source/design.json, source/layout.json, source/visible-floor.json, NATIVE-SPAWN-CHECKS.json and the map32/, review/ and validation/ outputs.

## Author evidence and limitations

Current author gates cover608 admitted cells;40,650 native out/back legs and45,990,559 full-body samples at≤0.5px spacing; every admitted center and four exact fitting extrema; all256 actual start outcomes; every ordered anchor pair;43 whole declared physical/architectural regions;55 art-selected continuous floor-width paths; all250 blocked-frontier cells; both actual seat contacts; and zero foreground/native-head-union conflicts.

The emitted controller passes19 authored cases including every one of512 clue/route/provision configurations. All three door pairs pass213 unchanged baseline transition cases:180 supported native-schema cases and33 explicitly synthetic robustness cases. Tests include busy, reject/retry, recovery, stale callbacks, movement supersession, initial position races, nondestructive Close, reset/cancel, disposal, local isolation and replay. Only a real moving:false event releases deferred changed layers; promise settlement and an x/y-only snapshot cannot invent idle.

Both reachable raster states are decoded from actual TMJ/atlas bytes and tested at six rational static fixed-origin scales. Opaque static rasters do not establish live GPU texture filtering, fractional camera behavior or the reported black-edge issue. Historical pinned movement code in a stub scene is not a real desktop, touchscreen, keyboard, browser, mobile, engine-dispatch, AV, social or multiplayer test. Independent exact-freeze review, live acceptance, publishing, source-hosting and spreadsheet links remain separate and pending. Nothing is deployed or published.

Exploratory failures remain under evidence/: initial tile+16 endpoint expectations were corrected to exact native-fit targets without calling that a collision repair; initial broad floor probes were reconciled with physical mixed-edge cells; an early miswired state layer was corrected after the decoded empty/packed crops exposed it. No failed candidate is counted as accepted.
