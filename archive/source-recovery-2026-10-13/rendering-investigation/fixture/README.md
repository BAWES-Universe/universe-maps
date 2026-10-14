# Isolated Phaser rendering comparison

This is a local-only diagnostic fixture, NOT a deployment, app integration, or browser-accepted fix. It contains Phaser 3.86.0, the HdpiManager compiled from adc13cffd4e57aca6bc0353ad108bba423c61de1, frozen Studio r8 and Reading r4 map/texture assets, and a repository PIPOYA Woka. Licenses accompany the package. The generated two-color pixel-art control is only a control fixture.

In an authorized environment with a browser on the same computer, serve this directory over loopback HTTP and open its URL. Example: `python -m http.server 8765 --bind 127.0.0.1` then `http://127.0.0.1:8765/`. No network service, room, account or application is modified. Stop the server when done. Do not expose publicly without permission.

Compare each of Studio, Reading and pixel-control using baseline, filter-only, native-nearest and native-plus-linear at zoom modifiers 0.5/0.75/1/1.25/1.5/2. Use real DPR 1 and 2 browsers where available; changing CSS viewport fields does NOT emulate a mobile device or DPR. Record the actual renderer; Canvas per-texture tile filtering is expected to have no effect under `antialias:false`.

Capture both the canvas bitmap and browser-displayed result at the same camera center and fractional world offset. Keep the Woka sharp, compare tile edges and alpha foregrounds, click known points, animate/move the Woka, recreate modes repeatedly and return to baseline. Save JSON reports with the measurement button. Test resize, camera-follow and real WorkAdventure UI separately in the full app; this harness does not exercise them.

The fixture uses one renderer at a time and records RAF delta plus render-submission CPU duration after 60 warm-up frames. These are NOT GPU times, full-game frame rates, memory measurements, or mobile performance acceptance. Native-framebuffer pixel-area increase is a resource estimate only.

No higher-resolution art or new detail is generated. Existing map dimensions, tile coordinates, collision data and original assets are preserved. Filtering can blend atlas edges; WebGL visual verification is mandatory before accepting it.

## Current validation status

- JavaScript syntax checks passed.
- Offline CPU reconstruction ran the real Phaser tile-layer Canvas function with native canvas images. See separate evidence; that is not a browser test.
- Dot cloud browser could not reach the workspace loopback server (`ERR_CONNECTION_REFUSED`). File URLs are prohibited by the supported browser route. No tunnel, public host, security bypass or deployment was attempted.
- Therefore this fixture has NOT been executed in a genuine browser in this environment. Full application camera/input/controls, mobile, WebGL, GPU, map transition/context restoration and default-map acceptance remain open.

## Foreground cutout warning

The source maps use complementary binary-alpha holes between base and foreground. Filtering both independently may produce partial coverage at boundaries even with perfect atlas gutters. Source CPU analysis reached 75% coverage at Reading world(462.5,309.5), tile(14,9). Test those contours on multiple backgrounds in WebGL before accepting linear mode. This is a conditional prototype risk, not a diagnosis of current nearest-render black edges.

## Fixture revision 1 — pointer mapping

After setting the canvas CSS dimensions, the fixture now updates both Phaser canvas bounds and `displayScale` (backing-size / actual CSS-size on each axis). It also refreshes bounds when the page or fixture container scrolls, while guarding destroyed canvases. This corrects the fixture's click-to-world measurement initializer; it is unrelated to the application PR. Nine cases run the exact initializer with real Phaser `updateBounds`/`transformX`/`transformY` methods and mocked DOM rectangles: legacy/native/high-DPI geometry and three offsets all map the display center to the bitmap center. This remains source-level checking, not live browser input acceptance.

Mode/map recreation now waits for Phaser's actual DESTROY event instead of a fixed delay. Requests are serialized with latest-request-wins behavior; obsolete callbacks are invalidated immediately. Each run owns its report, sample arrays and game references. Preload/create/runtime errors appear as failures, rather than leaving a misleading running state. If a failed renderer boot cannot reach a destruction frame, recreation deliberately waits and instructs the user to reload; it never starts overlapping games.

The actual bundled fixture passes13 mocked-DOM/Phaser-boundary assertions for delayed destruction, rapid mode/map requests, stale loader/create callbacks, report isolation, listener cleanup and asynchronous/create-error reporting. These are source-level tests only. Real browser scene boot, visuals, movement and pointer behavior remain unaccepted.
