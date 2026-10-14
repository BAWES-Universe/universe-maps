# Re-verification after controller repairs

The findings below are retained as the initial-review record. The two concrete defects (cleanup exception coupling and fixed-sequence roof reversal) were repaired during this review and are no longer outstanding in the revised controller.

Independently read the revised implementation and added tests, then reran syntax check, 16 controller tests, 25 structure checks and 41 native-route cases: all pass, with zero sampled body collisions. Revised runtime SHA-256: 91e587675b26e2b6a4c98ce891f0a7cd2cea693ceedd00ec70de3a9d6dc42e94. Revised controller-test SHA-256: 06486fbd2bd0e6d0452ef623462744aca30a3b0de84d1d3d5f4590f33e61ed0f.

Verified changes:
- Disposal attempts collision release first and independently attempts every cleanup operation. Collision errors leave recovery-needed status and repeated disposal can retry. Audio, menu or unsubscribe exceptions no longer suppress camera restoration or passage opening. Failed visibility writes no longer poison the visibility cache.
- Roof reversal proceeds one stage from the displayed stage instead of restarting a fixed sequence. Initial spawn inside remains fully cut away rather than briefly showing the roof.
- Explicit doorDemo=single-client controls demonstrate a complete 4→3→2→1→0→1→2→3→4 panel cycle with collision toggling. tests/door-demo-trace.json is an adapter event trace, not live footage. Public mode still intentionally has no closing.

Current verdict: controller-level fixes are accepted on source/mock evidence. Real renderer/physics, multiplayer, camera zoom restoration, native audio controls/devices, companion navigation, touch, performance and polished-art acceptance remain open. The new report supersedes the initial report's recommendation to repair these two concrete defects; it does not waive the real-game gates. Final package manifest regeneration is owned by the author after this report is saved.

---

# Independent verification: Moonlit technical slice

## Verdict
Suitable as a local mechanics fixture and source-level route demonstration. Not ready for production, multiplayer door closing, polished-art acceptance, or a claim that the requested interactive map is finished. Final art can be explored, but should not conceal the remaining behavioral gates.

## Checks independently performed
- Read README, STATUS, contract, build source, controller, controller tests, structure tests, native-route tests, source-method manifest and retained engine camera/room/audio configuration implementations.
- Ran JavaScript syntax check, all 8 controller tests, all 25 structure checks, all 41 native-route cases. All passed; route harness reported zero sampled body collisions.
- Checked MANIFEST.sha256 after the test run: all listed files verify. The test runners regenerate their result JSON files; those contents still match the original manifest. No runtime/source files were edited or rebuilt.
- Viewed decoded open-cutaway and roof-exterior images. These are sparse, flat procedural fixture renders, clearly not final Moonlit-quality art and not live game screenshots.
- Fault-injected a synchronous property-transport error during disposal with an in-memory mock, without changing files.

## Findings
### Error cleanup can strand the QA collision state
In runtime/moonlit.js, dispose marks disposed=true before calling subscriptions, menu removals, audio(false), camera restoration and failOpen sequentially. An exception in any earlier cleanup step prevents later steps. Reproduction: initialize in QA mode, close the door to completion, make room.setProperty throw, call dispose. Result: disposed=true, door=closed, collision still visible, camera restoration not called. A second dispose returns immediately. This is a demonstrated error-path defect under fault injection, not evidence of an observed live transport fault. Use individually guarded best-effort cleanup, attempt passage opening and camera restoration even after other errors, and test failures at each cleanup stage. visible() also updates its cache before issuing the visibility command, making a failed write look successful locally.

### Roof reversal is not continuous
roof() always uses [3,2,1,0] on entry and [1,2,3,4] on exit, without remembering the currently displayed alpha. For example, leave while the entry fade is still at 75% and it restarts at 25% before increasing again. Epoch cancellation prevents stale callbacks but does not prevent this discontinuity. Hysteresis reduces accidental toggling; it does not eliminate rapid movement across both thresholds. Test reversal at every step and derive the next sequence from actual current alpha. Initial spawn inside also briefly schedules 75% after roofs start hidden. Live quality and grid-rebuild cost remain untested.

### Default door behavior is deliberately limited
Public mode starts open and has no close path. Open pavilion door therefore does not normally demonstrate any panel movement. QA mode has five authored states and keeps collision during opening until the final frame; during closing it checks local occupancy before each frame and enables collision only at completion. This is internally consistent for a single-client fixture. There is no multiplayer occupancy arbitration, close synchronization or late-join acceptance; do not enable public closing. Body/position correctness still requires live game QA.

### Camera restoration needs real-engine acceptance
Controller sends followPlayer on timer completion, movement cancellation and normal disposal. The retained API and GameScene accept these calls, but CameraManager itself is not included/tested, so actual restored zoom, viewport state, resize and pinch behavior are not established. Tests only check that a follow call occurred. Failure cleanup can skip that call as described above.

### Audio is an opt-in test signal
The map starts silent. Explicit enable writes a native soundscape descriptor plus silent carrier, and disable removes both properties. The descriptor matches the retained parser's field/range constraints. No actual audio pipeline, autoplay recovery, native controls, voice coexistence or device listening test was performed. Bell test audio is not final ambience/music/waterfall sound.

### Native water and geometry
TMJ contains four 180 ms water frames on 24 cells, a 720 ms native animation loop. No live playback/performance check was performed. Routes use extracted pinned pathfinding/player/collision methods plus adapter bodies and renderer, covering ordered route pairs among five positions and one close/reveal replan. This is useful evidence for continuous garden–pavilion–terrace connectivity and side-passage bypass, not full physics, companions, touch, furniture depth or exhaustive reachable-area proof. Decorative shrubs/seat art are not all modeled as blocking bodies; final art/collision alignment needs an explicit pass.

## Gates before declaring the map usable and polished
1. Repair and test best-effort disposal/failed initialization, roof reversal and cancelled/interrupted actions.
2. Load on a verified isolated frontend and exercise actual renderer, avatar dimensions, physics and iframe messages; confirm panel/collision timing, furniture approaches and transparent-glass readability.
3. Validate camera restoration/zoom, native audio controls and water animation on desktop and touch devices.
4. Keep public doors open until multiplayer occupancy and shared state are designed and verified, or explicitly accept always-open public doors as the product behavior.
5. Art direction and detailed material/foliage/lighting/animation pass, followed by visual/collision/depth re-verification with actual avatars.

No external write, deployment, paid call or original-map modification was performed. This report is the sole new authored file.
