# Gate B v3 integrated experimental candidate

This is a local, unpublished map-only candidate for parent review. The selected version is `integrated/public/butterfly-town/gate-b/v3/gate.tmj`. It combines the reviewed balcony/stair boundaries and native spawn silence with a portrait-mobile establishing view, ordinary walking zoom, and one modest first-landing pullback. Desktop arrival keeps the current native framing.

## Camera sequence

- On a portrait device with a coarse primary pointer, the script asks the existing player-position API for the current location. Newer movement events take precedence. The overview is skipped if loading finishes after the player has left the arrival area or if they join in an upper zone.
- Near spawn, one unlocked native camera set establishes the view at world centre (480,800), authored rectangle 640×1280. It stays there while stationary; there is no timer-driven zoom carousel or input lock.
- After 128 world pixels of deliberate ascent, one native followPlayer call restores the saved ordinary walking zoom over 400ms.
- At the first landing, one existing camera.set widens the current native frame by up to 12%, subject to avatar and map-edge budgets. Its native pan lasts 200ms, followed by the engine's movement-triggered follow glide. That automatic follow retains the new zoom. An explicit followPlayer after this reveal would restore the old zoom, so the script never makes that call.
- The wider zoom is held through retreat and later visits to the stairs. This deliberately does not re-arm the cinematic within the same map visit. The earlier request for a repeatedly re-armed reveal is not solved.
- Reduced-motion preference disables the automatic camera sequence. Audio and static waterfall art remain available.

## Mobile detection and viewport data

Map JavaScript runs in an iframe that the pinned IframeListener sets to `display:none` (line 690). The candidate never reads iframe innerWidth/innerHeight or width media queries. It checks `matchMedia('(pointer: coarse)')` plus `screen.orientation.type` when available, then the legacy numeric window.orientation, then screen width/height as a last heuristic. The screen orientation check prevents fixed portrait screen dimensions from classifying a rotated phone as portrait. This is a device heuristic, not a measurement of the game canvas; a portrait touch tablet can qualify.

The initial overview uses authored world dimensions and does not pretend a current viewport snapshot exists. The landing reveal uses only finite native onCameraUpdate data received within 96ms: world x/y/width/height and native zoom. It defers when no fresh snapshot is available or when the frame/scale budget is unsuitable. GameScene's subscription does not immediately send a snapshot and filters duplicate events; the fixture models both facts. There is no unsupported camera API, engine adapter or PR 727 dependency.

## What the checks establish

- The integrated map is deep-equal to the reviewed geometry candidate except for two camera/version metadata properties. Its new foreground PNG, silent layer 55, foreground layer 56, collision data, layer order, and tilesets are unchanged from the geometry manifest.
- The full Bv2 portal/audio script is a byte-identical embedded block of the integrated script. Music bytes, all 15 shared PNG hashes, all old art/animation layers, the 32px grid, and the blank editor-configurable onward destination are preserved.
- The complete unchanged current CameraManager, WaScaleManager and HdpiManager run with the actual pinned Phaser 3.86 Camera/Pan/Tween classes. DOM, GPU rendering, scheduling, game layout and player-position events are adapters. No movement/pathfinding or real joystick driver is simulated by the camera fixture.
- 20 route scenarios, 5 arrival compositions, 18 reversal scenarios and 18 loading/transition edge cases were executed. The edge report explicitly records manual-ownership failures instead of counting those as preserved gestures. Six device-classification branches pass independently of hidden iframe dimensions. The integrated portal suite passes 10 tests, including 7820 bidirectional movement events, cancellation, re-entry and early unload.
- Five calibrated composition routes contain 2315 frames with no avatar overlap of the estimated bottom HUD reserve. The reference case was calibrated against three fixed map landmarks in the supplied phone images: the tight image is approximately 1.66 image pixels per world pixel and a 427×802 world viewport. A 430×809 native model matches that crop closely. Exact device CSS dimensions/DPR were not observed; 430px CSS width/DPR 3 is the matching model, not a claimed device reading.
- The reference phone's overview avatar frame is about 20.2 CSS px, then 32px at walking scale. The smaller modeled phone's overview can be 14.5px. The alternative readability crop shows less of the upper gate; it is in the review images but is not the selected candidate.
- Geometry's independent exact-source tests remain applicable because its data is unchanged: 16 explicit routes, 536 open-cell out-and-back cases, 405 fractional-click cases, full body/blocking sweeps, 16 native silence checks, and five pixel-identical static/animated scene comparisons.

## Remaining limits

This has not been validated in the full live game, actual game HUD, browser graphics, tap pathfinding, native joystick dispatch, or on a physical iPhone. The filmstrips are native-camera class compositions with estimated UI masks, not live screenshots. They are useful for review, not proof that touch play feels seamless.

The existing native camera may replace manual zoom/Look Around during a scripted pan or zoom restoration. After the sequence completes, the script makes no later camera reset and manual exploration survives repeated travel. A local defect draft identifies the existing native listener-ownership problem separately from a future follow-preserving zoom API enhancement. No engine changes are included.

Native mode changes can reapply map bounds at follow handoff. Conservative framing budgets reduce this in the tested routes; arbitrary sideways movement, changed layout, frame timing and mobile gestures are not guaranteed seamless. A brief ordinary frame can appear before the map script initializes. Orientation is handled by native resizing without repeated scripted reframing.

The silent spawn zone cannot guarantee zero transient proximity bubble during the room-join handshake; the current engine evaluates the initial silent tile after joining. Native audio autoplay/retry, saved Pause/Mute, platform volume limits and the existing Stop-on-next-tile behavior are unchanged. Waterfall sound is baked into the same music mix, not live positional audio.

## Review and reproduction

Start with `filmstrips/reference-phone-arrival-options.png`, `filmstrips/reference-phone-journey.png`, `INTEGRATED-MANIFEST.json`, `CALIBRATION.md`, and `CAMERA-ISSUE-DRAFTS.md`.

Use Node 24+ and Phaser 3.86.0. The fixture currently finds the already-installed source package in the review workspace; `PHASER_SOURCE_ROOT` can point to the `src` directory of an independently installed phaser@3.86.0 package. Run the five `tests/verify-*.mjs`/capture scripts and `node --test tests/integrated-portal.test.mjs`. Geometry reports are copied under `geometry-evidence`; their original durable checkpoint remains separate.

Only `integrated/public/butterfly-town/gate-b/v3` is proposed for later additive publication. `candidates` contains earlier review controls and is excluded from the final checkpoint. There is no publication, source PR or deployment in this task. A, Bv1 and Bv2 remain unchanged.

## Source publication dependency

The 15 shared v6 PNGs exist on Pages but their source is in open universe-maps PR #4, not master. The six-file v3 PR depends on those assets being merged first or together. A later master build may replace unmerged preview files; no CI changes or duplicate shared assets are proposed. The preview and a standalone source build must not be conflated.
