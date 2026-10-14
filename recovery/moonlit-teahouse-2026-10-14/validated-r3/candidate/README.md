# Moonlit Tea House: isolated technical slice

**This is a local mechanics prototype with deliberately provisional procedural fixture artwork. It is not the finished Moonlit design, a polished visual proposal, a deployed map, or live-game acceptance.** Existing Moonlit and all original/protected maps remain unchanged.

## Runnable entry
Serve the entire `runtime/` directory together through an authorized isolated map service. Load `moonlit.tmj` in a compatible WorkAdventure/Universe QA frontend. It uses the frontend-provided WA iframe API. Opening TMJ or JavaScript directly in a browser is not a game playtest. No npm package, CDN, login, paid service, or external runtime dependency is added.

Continuous native32 geography: garden approach → glass pavilion → open side passage → waterside terrace. All walking occurs within this one map. There are no teleports or fake cross-map transitions.

## Included behavior
- Five authored sliding-door states at 80 ms per step. Dynamic collision is separate from decorative panels. Opening a closed QA door retains collision until the panels finish opening; closing only enables collision after the final closed state and another local occupancy check.
- Default passage is OPEN, including before script initialization. No automatic closing, timer trap, or public close action. Shared `doorOpen=true` is observed; normal visitors can request opening.
- Add `doorDemo=single-client` to the map hash (legacy alias: `qaDoorClose=1`) only in an explicitly single-client QA session to expose the clearly labeled QA close command. This tests actual collision changes; it is not safe multiplayer closing. No shared closed state is written. Do not distribute that mode as a multi-user entrance.
- Roof cutaway uses per-player geometric hysteresis and authored alpha layers. Reversal advances from the currently displayed alpha stage, and starting inside remains cut away without a flash. It is a stepped opacity transition, not a native smooth-alpha API. Glass and the permanent building frame never disappear. Decorative roof layers have no collision.
- Native four-frame water-tile animation, 720 ms loop, 24 animated cells.
- Optional short terrace camera pan/zoom, then follow restoration; new player movement cancels the scenic view. No doorway camera takeover.
- Audio is silent by default. Explicit menu enables a quiet original local bell-loop test emitter and native zero-valued audio carrier. Native controls remain responsible for mute/pause/Stop/autoplay recovery. This is NOT waterfall audio or final music. No music bed is included.
- Reachable desk and chair approaches. A shallow desk-front lip provides the intended lower-body depth fixture. There is no sitting mechanic and no claimed live avatar/depth acceptance.

## Controls
Use the native menu commands: Open pavilion door; View moon terrace; Enable test bell ambience; Silence test ambience. The close command exists only in single-client demo mode, where both controls are labeled DEMO (single client). `tests/door-demo-trace.json` records the complete five-frame close/open cycle in the controller adapter; this is not live footage. No popup, reciprocal-door trigger, or inventory is used.

## Rebuild and checks
From this directory:

    python source/build.py
    node tests/extract-native.cjs
    node --check runtime/moonlit.js
    node --test tests/controller.cjs
    python tests/structure.py
    node tests/native-routes.cjs

Python requires existing Pillow. Node 24's built-in TypeScript transformer is used only to refresh the test harness. It reports its experimental status. No dependency installation is needed.

Current source baseline: `BAWES-Universe/workadventure-universe@aa3ca1d60801172bfd97b6619bbf351c17eb3dba`. The exact inspected engine files are retained under `source/engine-pin/`, with source/method hashes in `tests/source-method-manifest.json`. Tests transpile extracted unchanged methods from that pin. The full game, renderer, physics service and networking are replaced by explicitly scoped adapters in those tests.

Checked: 17 controller lifecycle/door/roof/audio/camera/fault-injection tests; 25 structure checks; 41 native route cases covering all ordered garden/pavilion/terrace/desk/seat route pairs with door open and closed, plus closing/reveal during an existing route. Native pathfinder replans through the open side passage when the front door closes. Zero sampled body collisions. The test harness is evidence for these methods, not a substitute for full-game QA.

Static renders in `renders/` are decoded from the actual TMJ and inspected. They are not screenshots of the game. The simple fixture artwork is not intended to meet the user's final visual-quality bar.

## Explicit outstanding gates
- Real isolated browser session on a verified frontend build, plus desktop/touch interaction.
- Multiplayer state, late joins, occupancy arbitration, interrupted initialization/network state. Public closing remains disabled until these are solved and accepted.
- Companion routing/door behavior; player-path success does not establish companion success.
- Live roof transition quality, no flicker, glass readability, depth and desk approach with actual Woka sprites.
- Performance: stepped reveal uses show/hide and therefore native grid rebuild/replans; duplicate visibility writes are suppressed, but full-game cost remains unmeasured. A true continuous fade would require a supported renderer API or separately authorized engine work.
- Audio device/autoplay/native controls/voice coexistence and suitable final music/audio art.
- Camera resize/pinch, interruption and real-device usability. Controller tests assert that followPlayer is called; they do not measure restored zoom, viewport, or actual camera state.
- Artistic direction, material details, foliage, lighting and final animation polish.

No GitHub mutation, upload, publish, deployment, paid call, or original-map edit was performed.

## Revision after independent review
Cleanup now attempts collision release first, independently attempts every remaining cleanup action, records failures, and allows repeat attempts. Failed layer calls are not cached as successful. Fault injection covers audio, camera, collision, frame, subscription and menu failures. Roof reversal is tested in both directions from all intermediate alpha stages. Public always-open mode is not advertised as an opening/closing demonstration; explicit single-client mode demonstrates that cycle. Shared safe closing remains unimplemented.
