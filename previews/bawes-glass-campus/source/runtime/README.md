# Local reproduction

Engine: `BAWES-Universe/workadventure-universe` at `274114560c5ec95fdf8e51e67986a53069f3cf06`. Tested with Node 22.22.0, installed frontend Vite 5.4.21, system Chromium and the engine's installed Playwright. The engine's own README documents Docker development and anonymous access via `docker-compose-no-oidc.yaml`. This run used the equivalent existing Node services, without production configuration or an admin API.

The saved environment initially lacked generated protocol files. From `ENGINE/messages`, these commands succeeded:

```sh
npm ci --cache /workspace/onboarding/npm-cache --no-audit --no-fund
mkdir -p ../libs/messages/src/ts-proto-generated
npm run ts-proto
```

From `ENGINE/play`, build the official iframe API:

```sh
/workspace/onboarding/toolchain/node_modules/node/bin/node node_modules/vite/bin/vite.js build --config iframe-api.vite.config.mts
```

The installed root Vite was version 3; use **play/node_modules/vite**, version 5.4.21. The installed `svelte-preprocess` exposes a default import; the local derived Vite configuration changes only that import and the HMR port. Sass is already installed in `play/node_modules`; an ignored root dependency symlink makes it resolvable by the root preprocessor. No tracked engine source is patched.

With ports 8000, 8001, 8080, 8082, 8090 and 50051 free, run `bash source/runtime/run-local.sh` from this candidate. Override `BAWES_ENGINE_ROOT`, `BAWES_NODE_BIN` and `BAWES_RUN_DIR` if needed. Stop only these processes after testing. The generated `ENGINE/play/bawes-local.vite.mts` is a temporary local configuration and can then be removed.

Redis, Matrix, map-storage, production authentication and production media services are not needed for these geometry/visibility checks. LocalAdmin reports that no admin backoffice is configured; Matrix logs an invalid unset endpoint at startup. This does not block the tested local room, but chat/account/catalog integrations and audio communication are not established by this run. No production service was configured to work around those messages.

Start a separate synthetic browser:

```sh
chromium --headless --no-sandbox --disable-dev-shm-usage \
  --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --remote-debugging-port=9222 --user-data-dir=/workspace/bawes-runtime/browser about:blank
```

Open the local game, choose a synthetic name/Woka, and continue without webcam. Tests in `source/validation/` connect to this browser. For the current town use `town.cjs`, `town-doors.cjs` and `town-crossing.cjs`; the other drivers retain earlier prototype coordinates. `routes.cjs` and `capture.cjs` use the existing first tab; `tables.cjs` and `two-clients.cjs` create independent anonymous browser contexts. Do not run two tests that control the same tab simultaneously. No real identity, camera, microphone or login token is checked into the repository.

`capture.cjs` writes timestamped JPEG frames to `/workspace/bawes-runtime/motion-frames`. The reviewed movie was encoded with:

```sh
ffmpeg -f concat -safe 0 -i /workspace/bawes-runtime/motion-frames/frames.txt \
  -vf 'fps=25,format=yuv420p' -c:v libx264 -crf 20 -movflags +faststart \
  review/client-motion.mp4
```

Keep the native screenshot's camera state separate from the overview. Default 1440×900 desktop gameplay uses a 720×450 game canvas upscaled 2×, zoom modifier 1, Phaser camera zoom 1 and Woka scale 1. The overview was obtained by five normal Zoom Out button clicks (modifier 0.32768); it is not evidence of default-camera tower visibility.

## Map packaging check

In the separate universe-maps checkout, `npm ci` rejected the inherited lockfile because optional fsevents/esbuild platform entries were missing. The documented install route succeeded with `npm install --package-lock=false --cache /workspace/onboarding/npm-cache --no-audit --no-fund`; package.json and package-lock.json remained unchanged. `npm run build` then optimized 11/11 maps, including `dist/previews/bawes-glass-campus/campus.tmj` and its bundled runtime script. This packaging check used Node 24.19.0 / npm 11.9.0. The built output was not deployed. Actual-client movement evidence targets the source candidate, not a released optimized world.
