# Reproduce this recovery

Map checkout: recovery branch in BAWES-Universe/universe-maps. Pinned Universe client: `274114560c5ec95fdf8e51e67986a53069f3cf06`. Node used for the client: 22.22.0. Browser: installed headless Chromium through Playwright/CDP, not a physical phone.

From `previews/bawes-sky-campus`:

```sh
python3 source/native-cafe-trial/build-candidate.py
python3 source/native-cafe-trial/verify-candidate.py
python3 recovery/package.py
python3 recovery/compact.py
node recovery/compact-final-acceptance.cjs
node recovery/supplemental.cjs
python3 recovery/archive-native.py
```

The root shared 32px optimizer config is unchanged. The delivery package retains native16 assets, removes only empty/inactive unreferenced layers, and composites compatible static background layers. The compiler checks that moved background pixels do not overlap intervening interactive artwork. Interactive layers remain byte-identical. The superseded optimizer experiment passed pixel equivalence. Its runtime run was interrupted by a harness error that tried to serialize the entire Phaser camera/scene; this is not evidence of an intrinsic map memory leak. Publish only the final compact native archive after authorization.

For the client, use a separate pinned worktree with installed workspace dependencies. Fresh setup here required protobuf generation using grpc-tools/ts-proto 2.4.2, `npm run typesafe-i18n`, and `npm run build-iframe-api` in `play`. The recorded `source/runtime/run-local.sh` starts backend, pusher, Vite and CORS map server. Set `BAWES_ENGINE_ROOT` to the pinned worktree and `BAWES_RUN_DIR` to a writable temporary directory. The generated local Vite config needs explicit `server.fs.allow` entries for the worktree and linked dependency directories, so installed fonts are served. No production configuration is required.

Start headless Chromium with CDP port 9222 and a fresh profile, then run `node recovery/compact-final-acceptance.cjs`. It opens the actual packaged TMJ at `http://localhost:8000/_/global/localhost:8090/recovery/compact/campus.tmj`, travels through proximity doors, visits all 71 seats, checks facing and captures occupied screenshots. It also exercises boundary collisions, animation clocks and a 430×900 touch viewport. The local backend disables persistence/permission checks; meeting locks are courtesy controls, not authorization.

The delivered 171-check evidence combines the first 165 checks with finish-acceptance.cjs after correcting a camera-object serialization bug in the harness. A fresh full run uses the corrected compact-final-acceptance.cjs above.

Fresh evidence is under `recovery/evidence`. Earlier evidence elsewhere in the repository is historical and was not reused as current acceptance.
