# Riverside garden module · frozen review candidate

Original magical garden artwork, a public river-edge hangout and a low firepit, built for the expanded magicalUniverse campus. This is a local candidate, not a deployed map or a claim of live ownership, private conversations or physical-device acceptance.

## What is ready

- `docs/riverside-native-greg.png`: first native composition, unchanged 32×32 Greg.
- `docs/four-cardinal-seats-native.png`: exact north/south/east/west bench positions with full head visibility and lower-body rim occlusion. These are **bench positions using the existing standing frames, not a new sitting animation**.
- `layers/garden-base.png`: 1024×1024 native map receiver. Original imagegen source was 1254×1254 and was uniformly reduced by the renderer; Greg is never scaled.
- Separate foliage and bench foregrounds, water/fire overlays and masks, an avatar shade-receiver mask, and a contact-shadow asset.
- `garden-geometry.mjs`: authoritative walkable polygon, solid footprints, continuous 16×16-body sweeps, 8px-lattice route search and exact cardinal bench positions.
- `garden-audio.mjs`: one original procedural crackle loop, explicit user gesture and mute, bounded proximity gain.
- `garden-integration.mjs`: explicit scene/position/mute handler. It changes this garden's SFX only. The default adapter installs no hidden-tab listener and changes no game-wide background audio behavior. Only the standalone demo opts into hidden-tab suppression for its local map SFX.
- `preview/index.html`: standalone native-scale walking/bench/motion/audio implementation.
- `riverside-garden.tmj`: editor-ready artwork layers, native collision objects, bench-position objects and connection metadata. Native object collision/bench behavior needs the supplied adapter or equivalent host implementation; stock Universe/Tiled collision support is **not asserted**.

## Campus transform

Native receiver: 1024×1024, world origin `(2176,1920)`. Local coordinates add that origin. Native tiles are 32px; avatar frame is 32×32 at scale1, body offset `(-8,0)` with size16×16 relative to sprite center.

- West commons connection: local `(0,288)`, world `(2176,2208)`, 96px receiver centered at y288. Entry sprite center is `(16,272)`, so feet land at y288.
- As-built fire center: local `(492,520)`, world `(2668,2440)`. This is an 8px north / 4px west art drift from the planning center; collision and audio follow the actual artwork.
- Bench sprite centers: north `(492,392)` facing down; south `(492,623)` facing up; west `(378,520)` facing right; east `(606,520)` facing left.
- Public route reaches the garden without any office desk traversal. Water, planted borders and fire are solid.
- Northern/southern river continuation remains a host-campus connection. The south path edge is closed until a host path is deliberately connected. The western clear entrance joins the commons; the rest of the western landscape edge requires the host's normal terrain overlap/blend.

## Layer order and head safety

Base artwork retains baked lighting and fixed scenery. Extracted foregrounds duplicate only pixels needed to occlude a moving avatar; they are not a new opaque full-canvas foreground. Draw base, subtle masked water/fire motion, avatar contact shadow, original Greg, projecting foliage, then the active bench's foreground rim.

The active bench foreground must protect the avatar's top19px. `preview/preview.mjs` contains the exact head-safe draw pass. Do not draw the combined bench foreground blindly over all characters. Every cardinal proof preserves all head pixels and demonstrably covers some opaque lower-body pixels with its real painted bench rim.

The shade mask is for avatar light receiving, not an additional global darkening layer over the already lit base. Reduced motion disables moving water/fire overlays and keeps the complete static composition.

## Local sound

`audio/fire-gentle-original.mp3` is the existing original16-second mathematical synthesis, copied byte-for-byte. No third-party samples, Conference assets, paid services or new license assumptions. MP3 container duration is16.056s because of codec framing; source PCM loop is16.000s. SHA256: `ea9a73835ea6c8a1700810ed8f69a1301dd242cd45e8cecc0f4564e00a767012`.

Fire presence is full within160px, fades to zero by384px, and is bounded to the garden. Maximum gain is0.06. World-space StudentHub and meeting-gallery exclusions remain quiet. No generic native `silent` property is used. Volume still needs real browser/device listening acceptance; the prepared asset is intentionally quiet.

Host usage: createGardenAudio with default options; createGardenIntegration(adapter,{sceneId:'magicalUniverse'}); feed handleRouteTransition with the new scene and world sprite-center position; feed handleWorldPosition, handleUserMute and explicit optional handleMapSfxSuppression. Start only through startFromUserGesture. The bridge suppresses this source while changing scene/position, never unmutes a user after a route change, and disposes only its own nodes.

## Verification and remaining gate

Passed offline:
- Four west-entry→approach routes, continuous native-body clearance, deliberate bench entry and reverse exit.
- All four complete head masks and nonzero correct lower-body foreground occlusion.
- Water/fire blocking; work/meeting coordinate samples at zero local gain; mute/optional map-SFX suppression.
- Eleven explicit integration state checks including scene departure/return and mute persistence.
- Twelve adapter lifecycle checks including recoverable fetch retry, repeated starts using one context/loop, disposal and no default visibility listener.
- Original audio hash, codec, stereo channels and duration; module syntax.

Browser walking, live motion and live audio capture are **not yet verified here**. Shell Chromium was blocked by sandbox socket creation; reviewed escalation failed at an environment mount. The supported visible cloud-terminal route then encountered ambiguous terminal-window identity. No restrictions were bypassed. The campus compiler owns the next integrated browser walking capture. No phone/speaker/headphone test has been performed.

## Reproduce

Run `python tools/build_native.py`, `python tools/build_layers.py`, then `python tools/render_seat_proofs.py` for the native artwork/occlusion proofs. Run Node tests in `tests/verify-geometry.mjs`, `tests/verify-integration.mjs` and `tests/verify-audio-adapter.mjs`. The browser test script is preserved but has not passed in this environment.

Serve this directory through an authorized local preview host and open `/preview/`. UI supports click-to-walk, WASD/arrows, explicit cardinal bench buttons, E to use/leave a nearby spot, native1×, reduced motion and opt-in local sound.

All three original imagegen prompts and outputs, including the two superseded placement attempts, remain in `art-source/`. No giant gate, office topology, live configuration, repository remote or production site was changed.
