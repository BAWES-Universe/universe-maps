# Moonlit additive r3 repair — completed

Both requested defects are repaired in map scripting and verified in actual Chromium. No engine source was edited. Baseline sealed-r2 remains unchanged; all 47 original manifest entries still pass.

## Deliverables and exact identity

- Candidate directory: `/workspace/scratch/moonlit-repair-r3/candidate/`.
- Authored controller source and runtime: [candidate/runtime/moonlit.js](candidate/runtime/moonlit.js). No JS transpilation is used; source/build.py produces the map, not this controller.
- Map entry: [candidate/runtime/moonlit.tmj](candidate/runtime/moonlit.tmj), unchanged.
- Served runtime: `/workspace/scratch/universe-local/game/maps/moonlit-repair-r3/`.
- [Runtime diff](runtime.patch), [new regression tests](candidate/tests/repair-regression.cjs), [candidate manifest](candidate/MANIFEST.sha256), [repair/provenance notes](candidate/REPAIR-NOTES.md).

| Artifact | SHA-256 |
|---|---|
| runtime/moonlit.js | `1692831cd58e13238c3bb2023119cf4f841120752cfd4e4f3352206ce1c95546` |
| runtime/moonlit.tmj | `3ea059084a3d84352302a8d9d0d139444d4c79622b98b8a8cead5d4903500d7c` |
| tests/controller.cjs | `d01dfbd3f7bee56f550e1d95ae5e546d0e39fde6d654ed994aebb0476360d264` |
| tests/repair-regression.cjs | `314994452cb4fbfd07fccc9bd5ced20c4ba8c7231974ef81fdafcbaff4e5391f` |
| MANIFEST.sha256 | `d2f2f6d1c385daeaf00d8020a20544d3c353e4868245706c81489860c976488a` |

HTTP-served controller bytes match the candidate hash. Full served runtime matches recursively. Historical r2 documents copied into candidate remain identified as historical by REPAIR-NOTES.md; its current manifest replaces the old manifest, retained as BASELINE-MANIFEST.sha256.

Baseline: universe-maps commit `6db977fcb576be429e1c147f59226f62641efae7`, recovery/moonlit-teahouse-2026-10-14/sealed-r2. Engine: `aa3ca1d60801172bfd97b6619bbf351c17eb3dba`. Node 22.22.0 runtime, Playwright 1.56.1, Chromium 154.0.8037.57.

## Fixes and inspected contracts

1. Default timers now wrap `root.setTimeout` and `root.clearTimeout`, preserving the browser-global receiver. Injected clocks still work. Scheduling, cancellation, roof/door transitions and camera return no longer throw Illegal invocation.
2. Menu registration uses supported `{key: label, callback}` options. In this engine, `Api/Iframe/ui.ts:206` defaults to a random UUID key; `Api/IframeListener.ts:535` installs a departure callback that passes the menu *name* to unregister; `Stores/MenuStore.ts:244` removes by *key*. Matching key and label lets the existing iframe-close lifecycle remove commands naturally. `IframeListener.ts:656` executes these callbacks before removing a script iframe. Cleanup no longer depends on pagehide delivery. This compatibility fix should be retested against future engine revisions.

The original controller suite adapter was updated to accept the real API's options form. Runtime changes are limited to timer defaults, menu registration and one explanatory comment. Public closing remains unavailable; demo closing remains single-client only.

## Actual gameplay results

All **28 checks in the seven final browser scripts passed**. These are overlapping journey assertions, not 28 independent features. No final client recorded Illegal invocation or an external request. Existing sandboxed service-worker and unavailable-admin warnings remain environment limitations.

| Journey | Actual result and evidence |
|---|---|
| Roof transitions/reversal | Visible stages `4,3,2,1,2,3,4,3,2,1,0,1,2,3,2,1,0`, never skipping a stage during reversal. Glass remains visible. Controlled position changes test reversal timing; ordinary outdoor-to-indoor walking also succeeds in route tests. [results](evidence/roof-camera-results.json), [cutaway](evidence/RoofCamera-cutaway-glass.png). |
| Indoor initialization | Held the real script response while the real player walked indoors, then released candidate bytes. 62 samples, no visible roof. This is controlled integration setup, not an authored indoor spawn. |
| Timed camera | Actual zoom modifier `1 → 1.171875 → 1`, logical viewport `720×450 → 615×384 → 720×450`, mode returns Positioned→Follow. Movement interruption also restores Follow/zoom. [measurements](evidence/camera-scale-observation.json). |
| Demo visual/collision sync | Closing `4→3→2→1→0`, collision only at 0; opening `0→1→2→3→4`, collision retained until 4. [results](evidence/door-demo-retest-results.json), [closed screenshot](evidence/SingleClientDemoRetest-closed.png). |
| Closed passage and bypass | Direct keyboard approach stops at y448. Real path goes around the east opening (max x816) and reaches (456,288). 126 sampled frames, zero blocked-cell overlaps. No teleport for route. |
| Physical doorway occupancy | Real move reaches (456,416), body top416/bottom432; close is refused, frame4/grid0 remain. [results](evidence/demo-physical-results.json). |
| Natural departure/rejoin | Two public-map exits reach the actual empty.json GameScene with zero scripting menus and zero audio; real rejoin restores exactly four usable commands. Camera/audio/open callbacks function after rejoin. [results](evidence/departure-rejoin-retest-results.json), [rejoin screenshot](evidence/DepartureRejoinRetest-rejoined.png). |
| Closed demo departure | Exit from a verified closed demo removes all five commands; rejoin starts frame4 with collision off. [results](evidence/demo-physical-results.json). |
| Prior routes | Garden→pavilion→desk→chair standing approach→terrace→garden all physically reached. 500 sampled actual body/grid frames, zero overlaps. [results](evidence/desktop-retest-results.json). |
| Water/glass/public passage | All four native tile frames 9363–9366 observed in 75 samples. Wall collision stops at y448, glass remains visible. Two synthetic clients observe each other and cross the public open passage; no public close menu. [results](evidence/public-mobile-retest-results.json). |
| Audio | Two local media elements play and advance time; Silence removes both. Native Stop, re-enable, then Silence pass. Natural departure also clears both. [desktop results](evidence/desktop-retest-results.json), [Stop results](evidence/audio-stop-results.json). |
| Phone emulation | Chromium 428×926 touch-to-walk and enable/Silence commands pass. Physical phone/Safari not tested. |

Per-client Playwright trace ZIPs, screenshots, frame samples, errors and request records are retained in evidence/. EVIDENCE.sha256 hashes the deliverable evidence and scripts.

## Source/adapter results — separate from live gameplay

- 17 existing controller tests pass: [log](controller.log).
- 2 new receiver and lifecycle-contract regressions pass: [log](regression.log).
- The same 2 regressions fail against unchanged r2: [negative control](baseline-regression-control.log). The timer fails on receiver identity; menu cleanup leaves four entries.
- 25 map structure checks pass: candidate/tests/structure-results.json.
- 41 native/adaptor route cases pass with zero sampled collisions: [log](routes.log).

The regression clock/store are contract models. The Chromium results above independently establish browser behavior.

## Harness corrections and retained failures

Initial repaired-map runs exposed test assumptions, retained without deletion:

- Roof visibility changes emit map-change notifications. `GameScene.ts:4088` replans an active path, so the original WA.player.moveTo promise can resolve cancelled while the player continues to its destination. Final route scripts preserve that original result and await physical arrival within 25px (native tile/body alignment); they issue no replacement movement. This behavior is observable in the result JSON, not hidden as a successful original promise.
- The first departure script queried getCurrentGameScene during the temporary transition scene and threw immediately. The corrected poll tolerates that transient absence and still requires the actual destination map. Its final two-cycle run passes.
- Controlled teleport occupancy and injected pagehide results are retained separately. Additional demo-physical.cjs uses real walking and actual departure, so acceptance does not depend on those controls.

No product assertion was changed to ignore a remaining mechanics failure. Original logs/results remain alongside explicitly named retests.

## Preview, reproduction and limits

Verified local candidate preview:
http://localhost:8000/_/r3-moonlit-r2-validation/localhost:8081/moonlit-repair-r3/moonlit.tmj

Verified isolated single-client demo:
http://localhost:8000/_/r3-demo-physical/localhost:8081/moonlit-repair-r3/moonlit.tmj#doorDemo=single-client

These are environment-local URLs; no public forwarding/deployment was created. All six existing services remain running.

Commands (from /workspace/scratch/moonlit-repair-r3):

```sh
node candidate/tests/controller.cjs
node --test candidate/tests/repair-regression.cjs
python candidate/tests/structure.py
node candidate/tests/native-routes.cjs
/workspace/scratch/universe-local/local-env.sh node roof-camera.cjs
/workspace/scratch/universe-local/local-env.sh node desktop-retest.cjs
/workspace/scratch/universe-local/local-env.sh node door-demo-retest.cjs
/workspace/scratch/universe-local/local-env.sh node departure-rejoin-retest.cjs
/workspace/scratch/universe-local/local-env.sh node public-mobile-retest.cjs
/workspace/scratch/universe-local/local-env.sh node audio-stop.cjs
/workspace/scratch/universe-local/local-env.sh node demo-physical.cjs
```

Runtime uses existing local-only Node/browser guards and synthetic guests. Original game/admin and fetched map checkouts remain clean; disposable engine's only tracked change is its pre-existing test isolation fixture. No production engine edit, deploy, merge, push, credential/permission change, shared-service change or paid service occurred.

No remaining blocker for the two requested repairs. Multiplayer-safe closing, physical devices/speaker listening, polished artwork and final visual acceptance remain unverified. This fixture does not implement sitting or companions.
