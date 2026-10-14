# Gate B v4 static-view candidate

LOCAL REVIEW ONLY. This separate standard-32 map removes every v3 cinematic controller. On a fine-primary-pointer desktop, the complete script sends zero camera commands. A coarse-primary-pointer device gets one immediate, unlocked wide setup at the current player position, then no further scripted camera commands. The portrait 640×1280 world rectangle preserves v3's opening zoom; landscape initial setup uses 1280×640. Native follow resumes on the first movement without restoring the old zoom. User-selected zoom stays in effect during tested subsequent movement, reversals and ordinary resizes.

The v3 boundaries, balconies, foreground, silent spawn, art, animation definitions and native music/waterfall premix are unchanged. Only two version metadata values change inside the TMJ; all other map bytes are preserved. The original portal/audio script is retained byte-for-byte as its own IIFE. The onward destination remains blank and owner-configurable.

## Important native limits

- Before the first movement, the existing camera API leaves the camera in Positioned mode. Pinching then retains the selected zoom but can change the crop away from the player; the first walk recenters normally. The reference source test measured a 134×502 world-pixel recenter after zooming in before moving. A pre-first-move Look Around request is also reclaimed by the existing one-shot follow listener. These are reproduced limitations, not passing ownership checks.
- Calling followPlayer to resume immediately would restore the pre-wide zoom. The supported map API exposes no zoom-only, follow-preserving operation. This candidate uses one set call; it does not prime saved zoom, lock input, inject movement, or repeatedly reset the camera.
- After the first movement, the tested native pinch choices and Look Around remain user-controlled. Native maximum zoom bounds can still clamp pathological zoom/resizing. Full preservation at arbitrary dimensions is not claimed.
- The first ordinary native frame can appear before map-script initialization. Very early zoom made before the one initial setup can be replaced by that setup. Late loading already away from the arrival area skips setup entirely.
- Coarse primary pointer is an input-device heuristic. A coarse-only desktop or tablet receives the mobile setup; a phone reporting a fine primary pointer retains native framing. No actual handset classification was observed. Screen Orientation is preferred, then legacy numeric orientation, then screen aspect. Hidden iframe dimensions are never used. Pointer/orientation changes do not rerun setup.
- On short portrait screens the retained wide view can make the Woka about 14.5 CSS px in the calibrated model; the reference phone model is about 20.2 CSS px. Users may pinch in. Landscape uses the same logical scale, not a whole-map panorama.
- Native audio and initial room status limits remain: Pause/Mute work; Stop can resume the static source on a later tile; water is baked into the music mix rather than spatial. Silent tiles cannot guarantee suppressing the initial room-join proximity bubble.

## Evidence and scope

CAMERA-VERIFICATION.json contains 31 source-class cases: 29 passing checks and two explicitly reproduced native limitations. The harness executes unchanged CameraManager, WaScaleManager, HdpiManager and PinchManager source pinned to universe-develop 75666c0ccae779515b6fcbd83446ebd1eee29d1b; it also executes the exact GameScene zoomByFactor body and actual Phaser 3.86 Camera/Pan/Tween classes. Player-position events, Rex gesture events, DOM, clock and viewport are adapters. This does not constitute native pathfinding/joystick input, live HUD, browser GPU or physical iPhone verification.

The integrated script also passes 12 portal/lifecycle tests, including 7,820 bidirectional movement events, one mobile setup, zero desktop camera actions, clean unload, reduced motion and blank destinations. Geometry/asset preservation is checked independently; the accepted v3 geometry route evidence is included without relabeling it as a new live test.

framing/arrival-comparison.png and the four journey strips use actual source-camera outputs over the exact map art with the player drawn at floorLayer depth. Gray UI reserves come from the earlier calibrated user screenshots. They are offline compositions, not live screenshots. Native zoom and user-selected zoom are labeled separately.

## Review and possible later publication

Runtime: publish/public/butterfly-town/gate-b/v4/gate.tmj and native-audio/gate-with-native-audio.js. Inspect V3-TO-V4-SCRIPT.patch and CANDIDATE-MANIFEST.json. No external publication or engine edits are included in this task. The pinned engine files are unmodified test inputs, not an engine patch.

A future additive six-file source PR/Pages preview must preserve all current paths. Like v3, the 15 shared v6 PNG source files depend on universe-maps PR #4; the six-file candidate is not a standalone master build. A later master build can replace unmerged additive previews. Existing A, Bv1, Bv2 and Bv3 remain separate.
