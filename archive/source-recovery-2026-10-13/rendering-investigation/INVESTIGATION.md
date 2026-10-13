# Rendering investigation — isolated, no deployment

12 October 2026. Fresh base: `adc13cffd4e57aca6bc0353ad108bba423c61de1` on `universe-develop`. Phaser: 3.86.0. Local research is isolated on `investigate/render-quality-2026-10-12`. The narrow fix is published as draft [PR #842](https://github.com/BAWES-Universe/workadventure-universe/pull/842), branch `fix/841-camera-zoom-resize`, commit `44dda03e5108b6cd257ce8a3cdeb9630edb8d908`, with [issue #841](https://github.com/BAWES-Universe/workadventure-universe/issues/841). No live app/room/map changes, merge, deployment, authentication changes or paid services were used.

## Bottom line

1. **The chunky map rendering is real, but the main cause is an intentional pixel-art rendering policy.** The application deliberately chooses a small game framebuffer, disables smoothing, then enlarges the composite canvas with pixelated CSS. The current live default-room baseline remains 787×505 bitmap pixels displayed at 1181×758 CSS pixels at DPR 1, using Canvas. This is not evidence of missing source artwork detail or a broken texture loader.
2. **A separate camera-resize defect is reproducible and has a narrow tested fix.** While zoomed out in Explorer, resizing the viewport can leave the previous camera zoom active after the rendering strategy changes. This is not a diagnosis of the original painterly-art complaint. The fix does not change normal framebuffer resolution, texture sampling, art, Woka size or map coordinates.
3. **A higher-quality mode is a larger coordinate-system change, not a safe one-line smoothing switch.** An isolated Phaser comparison fixture and offline before/candidate images are ready. Full application integration is intentionally deferred until genuine browser, input, camera, UI and mobile regression tests can run. No native-quality mode was enabled in application code.

## What was measured or tested

### Live baseline, genuine dot cloud Chromium

A separate browser worker rechecked the default public room, with camera and microphone off. Phaser reports Canvas 3.86.0. The entry asset changed to `index-B91EM-_S.js`; its deployed Git commit is not established. Canvas remains 787×505, CSS 1181×758, DPR 1, `image-rendering: pixelated`. One Zoom In gives 656×421; then one Zoom Out gives 820×526, all at the same CSS dimensions. This is a live baseline, not candidate acceptance, and does not establish the user's device renderer.

### Narrow camera fix: production-source regression tests

At DPR 1, zoom modifier .4, viewport 1280×720:

- Before resize: camera zoom .6; the low-zoom branch renders a screen-sized canvas.
- Resize to 2560×1440: the desired strategy now uses a 2134×1200 game canvas with camera zoom 1.
- **Before:** App's resize callback passes no camera. The camera remains at .6, so visible world width becomes approximately 3556.7 instead of 2134.
- **After:** the manager reuses the last explicitly managed camera only while it still belongs to an active scene and sets zoom to 1. Unrelated login/overlay cameras are not selected. Changing the game clears the reference. Directly destroyed cameras with cleared scene references are rejected even if still present in the camera array.

The same test cases run against the pinned original manager: **10 fail, 16 pass**. Patched source: **26 pass** (22 new manager cases plus four existing HDPI cases). Coverage includes both branch transitions, same-branch low-zoom resizing, DPR 1/1.25/1.5/2/3, focus refresh, saved zoom restoration, explicit overrides, inactive/removed/replaced cameras and unchanged default sizes. Phaser scale/camera boundaries are mocked; these are source-level regression tests, not screenshots or live-device tests.

Independent review repeated the results and added in-memory checks for dynamic DPR 1→2→1, cowebsite-width 1280→640→1280, scene stop/restart and normal camera removal/shutdown. Those extra checks do not substitute for browser integration.

### Offline image comparison: explicitly CPU-only

`render-offline.cjs` calls the real pinned Phaser TilemapLayerCanvasRenderer using `@napi-rs/canvas`, frozen Studio r8 / Reading r4 textures, and a small generated pixel-art control. It reconstructs final nearest enlargement on the CPU. It does not run Chromium's compositor, WebGL, a full WorkAdventure scene, its physics, or its UI.

**36 cases:** three maps × zoom modifiers .5/.75/1/1.25/1.5/2 × simulated DPR 1/2. Logical world width/height remain equal within floating-point tolerance. Source hashes are recorded. The Canvas filter-only route changes zero output pixels, consistent with Phaser's Canvas tile renderer ignoring texture filtering under antialias=false.

At the default 1180×757 CSS viewport and zoom modifier 1:

| Geometry | Legacy framebuffer | Native-framebuffer candidate | Pixel-area multiplier |
|---|---:|---:|---:|
| DPR 1 | 787×505 | 1181×758 | about 2.25× |
| Simulated DPR 2 | 787×505 | 2361×1515 | about 9× |

At simulated DPR 2 and zoom modifier 2, the candidate uses approximately 35.9× the legacy framebuffer pixel area. These are resource calculations, **not measured GPU/frame-time slowdowns**. A shipping option would need a pixel budget/cap and performance measurements on representative devices.

The nearest/native candidate can change pixel placement and fractional-motion sampling. It does not generate additional source detail or automatically make low-resolution art painterly. Many pixels differ because of sampling phase; a changed-pixel count is not a quality score. Woka textures remain nearest in the fixture, but browser motion/appearance acceptance is still required.

## Why the obvious switches are insufficient

- Per-texture linear filtering works in Phaser 3.86 WebGL through `Texture.setFilter`, but Canvas tile layers explicitly disable smoothing when renderer antialias is false. The observed cloud browser uses Canvas.
- Texture filtering happens before final composite-canvas enlargement. It cannot recover framebuffer samples already discarded, and global CSS smoothing would also soften Wokas and canvas UI.
- The commented `resolution` setting in App.svelte is not an implemented GameConfig option in this Phaser version; uncommenting it is not a supported HDPI fix.
- Raising bitmap density and camera zoom together can preserve the logical viewport in a fixture. Full app consumers also use raw camera width, scale.zoom, DOM-container transforms and pointer deltas. Each must be audited before integration.
- Larger source PNGs or tile cells would require an explicit source-pixel-to-world-unit mapping. A new high-resolution environment asset pipeline remains a separate proposal; none was added.

Original black-edge/seam causes and possible atlas bleed remain unverified; neither candidate is claimed to fix them. An independent source audit found complementary binary-alpha base/foreground cutouts: 2,160 Reading texels and 37,755 Studio world pixels. Their native composite is opaque. Separately linearly filtering complementary alpha layers can reduce composited coverage (0.5 over 0.5 gives 0.75). A premultiplied half-pixel CPU model reproduced this risk without atlas effects, including Reading world(462.5,309.5). This is a conditional halo risk for a linear prototype, not an established explanation of the current nearest-render screenshot.

## Other findings kept separate

- HdpiManager's ≤307200-device-pixel early return ignores zoomModifier. A 375×667 DPR 1 viewport returns the same game size for .5, 1 and 2. Characterization tests preserve the current behavior; it is not silently changed here.
- In the low-zoom branch, Phaser ScaleManager.refresh recomputes displaySize, overwriting the manager's manual override. At 1280×720 / zoom .4, the canvas-to-CSS ratio is 1 while the DOM parent receives about .60028 scaling. Real Phaser methods in jsdom reproduce the discrepancy. Speech/emote/embedded-website alignment needs browser checks before a separate fix.
- Explorer dragging uses framebuffer deltas as world scroll deltas without compensating for camera zoom. A native-density feature must address this and camera follow offsets, joystick sizing, DOM scaling and server viewport reporting.
- The noninverse live Zoom In/Out observation matches ExplorerMenu’s 1.2 and .8 factors (product .96), without bundling a new behavior change into this patch.

## Verification limits and next step

The private loopback HTTP fixture server started successfully in the isolated workspace. Dot cloud Chromium is on a separate computer and returned `ERR_CONNECTION_REFUSED` for that exact address. Its supported browser route prohibits file URLs and exposes no file bridge or device-emulation capability. No tunneling, public hosting, security bypass or deployment was attempted.

The fixture is ready to run in a saved coding environment with a browser reachable from that environment. It offers Canvas/WebGL, four quality modes, actual browser DPR reporting, viewport and fractional-scroll controls, animated nearest Woka, click/world coordinates, repeated mode recreation, and JSON measurement export. It has passed JavaScript syntax checks but has **not run in a genuine browser here**.

Full app desktop/mobile, camera follow, touch/joystick, click-to-move, collisions, seats/anchors/spawn, foreground overlap, cross-map cache isolation, dynamic tilesets, resize/context restoration and representative frame-time/GPU acceptance remain open. The application quality feature should not be merged or deployed on the strength of offline images.

## Reproducibility and artifacts

- `candidate.patch`: narrow resize fix plus production-source tests.
- `wa-scale-vitest.config.mts`: focused configuration; the first local dependency installation did not resolve the play workspace’s required svelte-preprocess version correctly, so the minimal runner was used for source regression proof.
- `wa-scale-baseline-vitest.config.mts`: substitutes the pinned original manager in memory for before/after test comparison.
- `evidence/OFFLINE-RESULTS.json`: dimensions, resource ratios, source hashes and caveats for all 36 cases.
- `evidence/*-comparison.png`: clearly labeled offline before/candidate image panels.
- `fixture/`: local-only Phaser comparison harness and source assets, with provenance/licenses and instructions.

Verification snapshot at **2026-10-12 08:15 UTC**, head `44dda03e5108b6cd257ce8a3cdeb9630edb8d908`:

- GitHub CI Play **build, iframe API build, typecheck, Svelte check, lint and formatting passed**. Play unit tests and remaining browser E2E jobs were still running; no failing job was observed at this snapshot.
- All five amd64 Docker builds and desktop build passed. Deployment jobs were explicitly skipped.
- The first local installation incorrectly resolved svelte-preprocess 5.1.4 rather than the play workspace’s pinned 6.0.3; the workspace-scoped retry also omitted that package, and a no-save repair encountered a peer-dependency conflict. Therefore the earlier local named-export/typecheck failure is a **local dependency-resolution limitation, not an established repository baseline source error**. CI’s successful build/typecheck demonstrates the distinction.
- Standard local protobuf/i18n generation succeeded. Full local play lint passed with a 4 GiB Node heap, as did targeted format/lint checks and the focused 26-test regression suite.
- The current CI result is available on [draft PR #842](https://github.com/BAWES-Universe/workadventure-universe/pull/842). This bundle is a frozen snapshot; later CI results are reported there rather than silently changing these bytes.
- None of the existing CI checks constitutes a live acceptance run of the separate native-framebuffer comparison fixture. Its browser, input and mobile acceptance gate remains open.


## Source links

- [Application canvas setup](https://github.com/BAWES-Universe/workadventure-universe/blob/adc13cffd4e57aca6bc0353ad108bba423c61de1/play/src/front/Components/App.svelte)
- [HDPI sizing policy](https://github.com/BAWES-Universe/workadventure-universe/blob/adc13cffd4e57aca6bc0353ad108bba423c61de1/play/src/front/Phaser/Services/HdpiManager.ts)
- [Scale and camera branch](https://github.com/BAWES-Universe/workadventure-universe/blob/adc13cffd4e57aca6bc0353ad108bba423c61de1/play/src/front/Phaser/Services/WaScaleManager.ts)
- [Phaser 3.86 Canvas tile renderer](https://github.com/phaserjs/phaser/blob/v3.86.0/src/tilemaps/TilemapLayerCanvasRenderer.js)
- [Phaser 3.86 texture filtering](https://github.com/phaserjs/phaser/blob/v3.86.0/src/textures/Texture.js)
