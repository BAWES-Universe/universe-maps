# Controlled performance comparison

Same local BAWES v0.3.8 engine, Chromium CDP9223, 1366×768 viewport, camera1/Woka1, one rendering game tab, stationary hub/spawn views, sound stopped. Reviewer browser was navigated to about:blank. Each sample warmed for3s and collected15s of requestAnimationFrame timing, Chrome Performance metrics and V8 sampling profiles. No engine source changes. Test-only animation pause and forced post-update dirty flag were cleared by navigation.

| Diagnostic | Expanded animation on | Expanded paused | Compact on | Compact paused |
|---|---:|---:|---:|---:|
| Forced redraw every frame, mean RAF FPS |30.64|28.73|40.16|39.92|
| Main-thread TaskDuration /15s |15.05s|15.08s|15.00s|15.06s|
| ScriptDuration /15s |0.61s|0.46s|0.51s|0.47s|

All forced-redraw samples record actual viewport1366×768, native camera/scale1, same engine/browser. Expanded is slower than compact in this controlled rendering workload. Pausing animation does not improve either map's forced-redraw rate materially; the expanded on/off difference is within the variation of these single samples, not a claimed animation speedup.

Ordinary idle scheduling samples for expanded were52.73FPS on,60.02 paused,52.73 on. TaskDuration fell from8.98–9.23s to1.08s when paused. Engine GameScene.ts:1049 marks the scene dirty on tileanimationupdate; pausing therefore also skips idle rendering. This is not evidence that tile-index updates consume that whole difference. Preliminary compact idle samples were57.28–59.00FPS on and59.90 paused; a second diagnostic CDP connection may have affected their viewport, so the forced-redraw table is the authoritative equal-viewport comparison.

Expanded animation plugin self samples totalled only0.019–0.027s per ordinary15–16s sample and0.008s in forced-redraw mode. Most forced-redraw samples were attributed to native `(program)` rather than JS. These data support redraw/native rendering work as the dominant observed cost, but do not isolate GPU versus browser/driver internals. Software rendering and concurrent browsers are environment facts, not a proven exclusive cause. Earlier simultaneous-review recordings measured roughly11–25FPS and remain honest evidence of that loaded environment.

Map-local optimization already applied: sea motion uses1,600 native128×128 animated patches instead of roughly20,000 individual32px instances. It retains24frames/100ms and continuous visible shimmer. Two fountains retain72native32px tiles with24frames/70ms, for73animation groups total. Compact has592groups. No frame reduction, disabled motion, camera zoom, avatar scaling, engine changes or paid services were used. Current measurements do not justify further reducing visible animation quality to chase the small bookkeeping cost.

Limitations: stationary views, one15s sample per forced condition, synthetic redraw diagnostic rather than a hardware benchmark, shared hosted execution environment. No60FPS guarantee, especially at1920×1080 or under concurrent browser load. Actual gameplay and water clips are separate evidence. A user's GPU/device/network performance remains unverified.
