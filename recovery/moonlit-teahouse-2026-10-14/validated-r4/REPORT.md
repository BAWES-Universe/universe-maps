# Moonlit r4 — local tea journey

**Completed: all 33 final Chromium journey checks passed.** Additive technical fixture derived from validated r3. Nothing has been pushed, deployed or coordinated for backup. Validated r3 and sealed r2 remain unchanged; their original manifests verify.

## Deliverables

- Authored controller source/runtime: [candidate/runtime/moonlit.js](candidate/runtime/moonlit.js).
- Map entry: [candidate/runtime/moonlit.tmj](candidate/runtime/moonlit.tmj).
- Procedural asset builder: [candidate/source/add-tea.py](candidate/source/add-tea.py).
- Original cup/pot/steam sprite: [candidate/runtime/tea-ritual.png](candidate/runtime/tea-ritual.png).
- New state-machine regressions: [candidate/tests/tea.cjs](candidate/tests/tea.cjs).
- Served local copy: `/workspace/scratch/universe-local/game/maps/moonlit-r4/`.
- Candidate identity: [candidate/MANIFEST.sha256](candidate/MANIFEST.sha256).

| File | SHA-256 |
|---|---|
| runtime/moonlit.js | `1360a94a10f4228f9c1f3fb66f02d3975684166ee6fe61736ddfb31e8489bb81` |
| runtime/moonlit.tmj | `41ae5ef40dd4dffdfb88f24e3f35fe56b8921dcc2e1c2d79824b4917803f5921` |
| runtime/tea-ritual.png | `d7e0cb63aa0e984bbce5ab77a01e8d7a53cd6b4bdf3b17401fe609193b5f427f` |
| source/add-tea.py | `3ab0613e7b89821ce19d79b3fd26897a933f4c8ad987e21c71b6f54398c6aa03` |
| tests/tea.cjs | `0e0fa3576361c7894d786124dbf764d61bd83a3148205a29819e2c6b1d42dc29` |
| MANIFEST.sha256 | `96ebe51e0202c407d8eafc95ea8474a2e581627aa6f3ad796ffd709b6182b624` |

## Interaction

Walk to the pavilion desk. Choose **Prepare tea**, remain there for 1.8 seconds, then **Collect tea**. Walk through the connected map to the moon terrace and choose **Serve tea**. A procedural pot/steam marks brewing, a cup/steam marks ready tea, collection clears the desk, and serving reveals a cup with animated steam on the terrace. There is no attached carried-cup sprite; carrying is local controller state and the handoff instruction.

Leaving the desk region while brewing cancels its timer and clears visuals. Epoch guards prevent a late callback from finishing cancelled preparation. Collection/serving validate both state and location; repeated/stale callbacks cannot repeat a transition. Once-per-cycle success notices are not replayed on revisits. **Reset tea ritual** is a Settings command; it clears the timer, cup/steam and notices. Actual room departure destroys the local instance; rejoining starts idle.

The existing `WA.ui.openPopup` API supplies map-anchored labeled buttons; `WA.player.onPlayerMove` supplies local position. Existing layer visibility and native Tiled tile animation provide visuals. Menu keys retain the r3 label/key lifecycle compatibility fix. No tea state is written to WA.state, storage, accounts or shared services. Public doors remain fail-open; the existing closing demo is still explicitly single-client only.

## Verification approach and source checks

Engine `aa3ca1d60801172bfd97b6619bbf351c17eb3dba`, Chromium 154.0.8037.57, Playwright 1.56.1, isolated Node 22.22.0. Runtime remains loopback-only with synthetic guests and fake media. No new external service or paid generation was used.

Source/model checks: **23 passed** (17 original controller, 2 r3 regressions, 4 tea state-machine tests); **26 structure checks passed**; **41 native/adaptor route cases passed**, zero sampled model collisions. The tea builder is idempotent. Existing r3 tile-layer contents, including collisions, are unchanged apart from sequential layer IDs. These are source/model checks, not substitutes for gameplay.

Final live results are recorded in [final/suite-results.json](final/suite-results.json), with detailed logs, screenshots, sampled states and Playwright traces in final/evidence/. The final runner executes sessions sequentially. Keyboard actions use native Enter on a focused popup button and actual Arrow-key movement; test focus is assigned with Playwright, so automatic Tab ordering/accessibility is not claimed. The mobile journey uses actual touchscreen taps for every walking leg and tea action, with no WA movement/teleport helper. Reset/departure checks also use the real game APIs/UI.

## Final live results

All 8 sequential scripts exited 0; **33 checks passed, 0 failed**. These are overlapping journey assertions, not 33 independent features. No nonlocal runtime requests or Illegal invocation errors were recorded. The existing sandboxed service-worker warning is the only recorded page error in these final sessions.

| Journey | Actual result |
|---|---|
| Keyboard tea journey | Arrow-key approach from garden to desk and desk to terrace; native Enter activation on focused popup buttons. Leaving cancels brewing. Ready cup and steam appear; collection clears desk; serving reveals terrace cup and both steam animation frames (9368/9369). Reset and real departure during brewing/rejoin pass. |
| Touch tea journey | All 25 recorded walking taps, including cancellation and revisits, use the actual touchscreen; no WA move/teleport helper. Prepare, collect and serve use tap buttons. Revisiting desk/terrace shows status with no repeated collection/serving notice. Mobile reset and real departure remove tea prompts. |
| Roof/camera | Reversal stages `4,3,2,3,4,3,2,1,0,1,2,1,0`; no skipped stage in sampled sequence. Controlled indoor initialization: 79 samples, no visible roof. Camera zoom modifier `1→1.171875→1`; timed and movement-triggered return restore Follow. |
| Demo door | Close frames `4→3→2→1→0`, collision only after closing; open frames `0→1→2→3→4`, collision held until frame4. Direct approach blocked; side passage route reaches pavilion, max x816, 380 samples without blocked-cell overlaps. Closing remains single-client demonstration only. |
| Routes | Five connected legs through pavilion, desk, chair standing approach, terrace and garden. 1,033 actual body/grid samples, zero overlaps. Native replanning can cancel the original promise while physical movement continues; arrival is verified without reissuing a move. |
| Natural menu/audio cleanup | Two real public-map departures leave zero scripting commands and zero audio. Rejoin restores exactly five commands, including Reset tea ritual. Tea-specific departure during brewing also leaves zero popup buttons and fresh idle state after rejoin. |
| Water/glass/public passage | All four native water frames observed; permanent glass stays visible and wall collision holds. Two synthetic clients can use the open public passage. No shared tea-state claim is made. |
| Audio | Explicit play advances both local media clocks; Silence, native Stop, re-enable and subsequent Silence all pass. Physical listening is unverified. |

Selected live images: [desktop ready cup](final/evidence/TeaKeyboardAccepted-ready-cup.png), [desktop served cup/steam](final/evidence/TeaKeyboardAccepted-served-steam.png), [touch ready cup](final/evidence/TeaTouch-ready.png), [touch served cup/steam](final/evidence/TeaTouch-served.png). [Full final suite results](final/suite-results.json) identify the authoritative result files and accompanying traces. HTTP-served controller, map and sprite bytes match the listed SHA-256 values; the served runtime directory matches candidate/runtime recursively.

## Evidence interpretation

Earlier exploratory runs remain in evidence/ and top-level logs. They include an initial cup placement obscured by the avatar, corrected by moving the props beside the standing positions. An early keyboard harness attempted Tab navigation and later sent an extra unfocused Enter after collecting; the engine's `GameSceneUserInputHandler.ts` maps unfocused Enter to Express, which captures movement input. The corrected journey activates once and physically walks using Arrow keys. Initial concurrent roof/door sampling missed intermediate rendered states; those results are retained, and final sequential regression results are authoritative only where their assertions pass.

The pre-final `final/tea-live-final` run also retains its failed extra-Enter keyboard check; `final/tea-keyboard-retest` is the corrected final journey. Do not combine earlier runs into an acceptance count. Generic sandboxed service-worker and missing-admin Explore warnings are environment limitations; tea runtime errors are inspected separately.

## Reproduction and limits

Local preview: `http://localhost:8000/_/r4-tea-keyboard-final/localhost:8081/moonlit-r4/moonlit.tmj`.
This is available inside the environment, not a public deployment or forwarded URL.

From `/workspace/scratch/moonlit-r4`:

```sh
node --test candidate/tests/controller.cjs candidate/tests/repair-regression.cjs candidate/tests/tea.cjs
python candidate/tests/structure.py
node candidate/tests/native-routes.cjs
python final/run.py
```

To regenerate the full map from its source, run `python candidate/source/build.py` followed by `python candidate/source/add-tea.py`. The runtime JavaScript is authored directly.

No production engine edits, pushes, merges, deployments, shared-room changes or permission changes occurred. Tea is a local interaction, not shared multiplayer inventory. No seating, physical-phone/Safari behavior, physical speaker listening or polished-art acceptance is claimed. This remains procedural technical fixture art.
