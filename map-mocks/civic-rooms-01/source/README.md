# Civic pavilion: classroom and great hall

Original coherent native-scale classroom/event module for Universe's public-left campus branch. Start with `docs/civic-occupied-native.png` (640×1152). The repeated characters are unchanged 32×32 Greg scale fixtures, not live attendees. Room/seat counts are provisional examples, not a known class or event headcount.

## Campus attachment

Place the module's top-left at world **(0,1792)**, native 32 px tiles. East public entrances are local **(608,384)** and **(608,992)**, hence global **(608,2176)** and **(608,2784)**. Door gaps are y344–424 and y952–1032 locally. They meet the lead's outside public cloister without crossing HQ desks. Keep this module's 640×1152 scale; do not enlarge furniture or Greg to fill the room.

- Classroom: six distinct north-facing desk/chair stations, clear teacher front, side/rear approaches, solid northern teaching board and built-in bookshelves.
- Event hall: 24 north-facing example audience chairs in two banks. The nearest chair silhouettes leave a 98 px central aisle. Four 64 px row pitches preserve circulation behind occupied seats.
- Stage: both side approaches remain open. Main front fascia is blocked. Speaker stands at (320,688), body tangent to the podium collider at (288,704,64,32). The actual top/rim redraws over the torso while the head stays clear.
- Walls, planters, desks, podium and stage fascia have independent exact rectangular collision data in `module.json`.

## Layers and editable sources

Place these equal-size transparent layers in the given order:

1. `assets/architecture-native.png`
2. `assets/furniture-native.png`
3. Native players (Universe's `floorLayer` boundary)
4. `assets/foreground-native.png`
5. `assets/glass-native.png`
6. `assets/shadow-native.png`

The two above-player environmental masks are original code-native tints. They demonstrate source-style partial glass/shadow overlap without changing physical collision. They are not a full exterior roof-reveal system. Architecture is the interior-revealed state; a separate coherent exterior roof is still a campus integration task.

`art-source/` retains both built-in imagegen masters, exact prompts, editable geometry SVGs, and the generated layer SVGs. `tools/render-native.js` mechanically composes original assets; no Python image editing or third-party reference art is used. Chair and classroom station source pixels are unchanged original art from the validated shared modules. `provenance.json` records source hashes. `asset-manifest.json` records native/source dimensions, hashes, alpha bounds, entrances and mask origins. Original generator alpha1–4 fringes are recorded separately from meaningful solid silhouettes.

## Verification

`docs/offline-verification.json` passes 33 entry routes and their exact reverses, through 19,285 one-pixel swept-body positions. Every other fixture body is treated as occupied. Both stage stair routes, teacher access, all six desks and all 24 audience places are included.

All 32 fixture masks preserve every nonzero Greg pixel in the protected top 14 rows. They cover 281 torso pixels per classroom fixture, 233 per audience fixture and 190 for the podium speaker. The teacher intentionally has no foreground occlusion. These are source-pixel checks and static compositions.

`qa/` contains a separate genuine Phaser 3.86 Arcade harness, using the source-extracted native body/depth primitives. It supports physical keyboard movement and a route runner. Exact rectangle collisions remain an integration representation, not an assertion that a Tiled 32 px collider grid or current deployed Universe has been configured. The current browser result is tracked separately; never describe offline results as an actual runtime walkthrough.

No live broadcast, meeting/audio configuration, live multiplayer, audience access control, WAM service regions, seat interaction, claim ownership, sitting animation, or deployment is included. No repository or hosted map changed.

## Reproduce

From this folder:

- `node tools/build-module.js`
- `node tools/render-native.js`
- `node tools/check-module.js`
- `node tools/freeze-manifest.js`

For manual runtime QA, serve this folder using `python qa/server.py --port 8837` in the supported cloud desktop terminal, then open `http://127.0.0.1:8837/qa/` in the cloud browser. The shell-executor loopback is isolated from the browser; its server is not proof of browser reachability. Do not launch shell Chromium to work around socket restrictions.
