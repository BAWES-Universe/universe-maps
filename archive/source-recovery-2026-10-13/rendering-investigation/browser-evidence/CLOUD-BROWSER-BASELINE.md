# Cloud browser baseline — 2026-10-12

Observed in dot's dedicated cloud Chromium browser at 07:33–07:37 UTC. This is current live default-room baseline evidence, not before/after candidate acceptance and not the user's device.

## Live route and renderer
- URL: https://dev.bawes.net/@/default/default/default
- Synthetic guest: MapQA; default male1 Woka. No login/account creation, shared-room edits, map URL changes, or admin actions.
- Camera and microphone kept off; no media permission granted. Repeated TURN relay warnings were dismissed without changing network/security settings. Communication was not tested.
- Console startup: WorkAdventure / Phaser v3.86.0 (Canvas | Web Audio), timestamp 2026-10-12T07:33:16.392Z.
- Current source asset: https://dev.bawes.net/assets/index-B91EM-_S.js . Prior report used index-Dp7trYfQ.js. Neither fingerprint proves a Git commit.

## Measured rendering
Baseline: bitmap 787×505; CSS rectangle 1181×758 at x=0,y=0; image-rendering pixelated; viewport 1180×757; DPR 1; visualViewport scale 1. Thus CSS/bitmap ratio is approximately 1.5006×1.5010.

One application Zoom In button click: bitmap 656×421; CSS rectangle still 1181×758, observed y=-5; DPR 1, viewport unchanged. Thus ratio approximately 1.8003×1.8005. Map and Woka visibly enlarge together, with less surrounding map visible. The frame buffer loses dimensions as game zoom rises. The y offset followed focusing the zoom button; no cause is asserted.

The application Zoom Out button was clicked once afterward, but it did not exactly restore the starting dimensions: the resulting bitmap measured 820×526 with the same CSS rectangle 1181×758 at y=-5. Therefore one Zoom In and one Zoom Out are not proven symmetric in this live build. Exact numeric Phaser camera zoom and browser-page zoom were not exposed by inspected DOM. Native browser menu attempts did not expose a zoom value. DPR 1 and visualViewport scale 1 do not independently prove browser zoom 100%.

## Screenshots
- render-baseline-desktop.jpg: settled live default-room baseline, synthetic MapQA Woka near center; silent-zone notification visible. No private chats, other people's account/payment content, or sensitive details visible.
- render-baseline-zoom-in.jpg: same room after one application Zoom In click; Woka/map visibly larger. No private chats, other people's account/payment content, or sensitive details visible.

These are JPEG browser screenshots, not lossless source-art samples. Pixel-art map and Woka both look blocky at the measured enlargement. This does not prove that a candidate HD background will improve, establish source-image quality, or isolate the cause of reported dark edges. No claimed FPS, frame-time, GPU, memory, or input-coordinate performance acceptance was measured.

## Isolated-fixture blocker
Supported browser navigation to a local file was rejected by browser URL policy: allowed protocols are only HTTP and HTTPS. Data URLs are consequently not a permitted fixture route. A loopback-only server started in the isolated workspace, but cloud browser navigation to http://127.0.0.1:8765/ returned net::ERR_CONNECTION_REFUSED. The browser cannot reach that separate workspace loopback server.

No cloud filesystem/HTTP serving bridge, viewport setter, or device-emulation capability was advertised (browser capabilities: none; tab capabilities: browserAuth, botDetection). No browser security changes, socket restriction bypass, public deployment, or tunnel was attempted.

Pending/unverified: true candidate before/after rendering; WebGL; DPR 2; mobile viewport/emulation; candidate input/camera alignment; representative performance; exact deployed Git commit. These require a supported authorized test environment or reachable private HTTP fixture endpoint.
