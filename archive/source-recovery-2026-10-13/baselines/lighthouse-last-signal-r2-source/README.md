# Lighthouse: The Last Signal · interactive map candidate r2

An additive, private-to-each-visitor signal-restoration experience on N35-r3 Lighthouse Festival Island. **Not published. Independent review and isolated in-game acceptance are required.**

## Play loop

1. Arrive at the south dock and choose **Begin quietly** (default) or the optional shore signal.
2. Tap the brass floor rings on a phone, or right-click their floor on desktop, to use native movement. Keyboard/joystick movement also reaches the proximity trigger. Tap the real popup buttons to act. These are floor-arrival targets plus UI actions, not invented clickable-entity APIs.
3. Capture the three notes: sunset deck / LOW first; north terrace / MIDDLE second; east cottage / HIGH last. Each captured ring turns mint. Visit them in any order.
4. Return to the lighthouse approach and transmit LOW → MIDDLE → HIGH. Wrong input resets only that sequence, preserving exploration. The beacon gains a warm optical glow on completion, and optional map audio is unloaded.
5. The global **Signal journal** uses screen-space UI and gives progress anywhere. **Inspect nearby ring** opens controls only at a nearby ring; away from rings it gives screen-space directions. **Shore signal off** is available anywhere. **Restart signal** shows a screen-space question and temporarily adds **Confirm signal restart** to the menu; Close, moving or opening the journal cancels it. Local ring journals also provide sound on/off and restart. Walking away closes a popup. No forced movement, timer, traps, combat, account data or persistence. Reloading starts a new visit.

This is a small complete interaction loop, not an event broadcasting/stage system or multiplayer-cooperative quest. Other visitors' state is intentionally unaffected. The broad lawn, routes, entrances, collision and original depth layers are preserved exactly. Existing N35 seating/art does not gain a new sit mechanic.

## Runtime

Serve `runtime/` together at one HTTPS origin. Entry files:
- `lighthouse-last-signal.wam` references `lighthouse-last-signal.tmj`.
- The TMJ root `script` property selects `signal.js`; its WA iframe API is provided by the game.
- All image and audio URLs are relative and included. No CDN, npm, paid service or runtime dependency is requested by the script.

Do not use a guest-only `/global` URL as evidence of playability if that frontend does not permit arbitrary TMJ loads. Do not change any live room to test this. An owner/admin-approved isolated QA room remains the in-game acceptance gate.

## Audio behavior and provenance

The experience starts with no `playAudio` property and makes no sound unless selected. Optional shoreline signal uses the native audio controls, with source gain **0.09** and a smooth proximity falloff from 16px to 160px around the west sunset deck `(272,672)`. The gathering lawn has **exactly zero** proximity gain everywhere, proven geometrically. There is no music bed; a zero-valued PCM carrier meets the engine's opt-in contract. Native mute/master/pause/Stop remain authoritative. The script never uses WA.sound or bypass audio, never retries against the user's controls, and unsets `playAudio` using `undefined` on off/reset/completion/exit.

`audio/tide-signal.wav`: original deterministic additive sine/bell synthesis (220/330/440 Hz, eight-second loop, mono PCM16 at 22,050 Hz), authored by `tools/build.py`. `silent-carrier.wav` is exact zero PCM. No third-party audio sample, artist imitation, recording or paid generation service. The sequence provides an optional audible reinforcement of the same written notes; sound is never required. Test actual loudness on physical hardware before acceptance. A browser gesture/retry may be required by the existing native controls.

The original image atlases and map geometry are reused unchanged from the user's N35-r3 authored map assets. New transparent brass/mint ring tiles and the completion glow are original procedural art from `tools/build.py`. No new outside asset license is introduced. Source-native test methods/EasyStar are inherited from the existing approved N35 native test package, attributed in its retained manifest; they are evidence tooling, not shipped runtime code.

## Exact source contract

Repository: https://github.com/BAWES-Universe/workadventure-universe

Read on 2026-10-11 UTC:
- `universe`: **42ba35bd6eefeb4f74359114904d167cbaecf1ad**.
- `universe-develop`: **50a980e984aa61146a472ccbc025f2ea17350d5d**.
- Original audio-controls PR [#712](https://github.com/BAWES-Universe/workadventure-universe/pull/712): merged 2026-10-09, merge `4f0b17849499ae604cc4963e6f292c1e9fee4911`.
- Native click/tap PR [#799](https://github.com/BAWES-Universe/workadventure-universe/pull/799): merged 2026-10-10, merge `60e7afdc3f96ef32525597cd46bd41175d61a2ef`.
- Additional proximity extension [#727](https://github.com/BAWES-Universe/workadventure-universe/pull/727): merged 2026-10-10, merge `b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af`.
- Release [#800](https://github.com/BAWES-Universe/workadventure-universe/pull/800) merged into `universe` on 2026-10-10. Source release is verified; deployment/device acceptance is not inferred from that merge.

`evidence/api/` retains the actual pinned production iframe contracts for onInit/player position/movement, popup buttons, menu, show/hide layer and setProperty, plus the proximity fixture. One distance-attenuated emitter is supported, not binaural positioning or a multi-emitter mixer. Native path fixture source is pinned at `60e7afdc…`; `evidence/native-production-diff.json` shows no changes to the exercised path/player/pointer/collision/visibility methods at the production pin. The later wrapper/scene changes concern spawn silence.

## Reproduce

Used: Node **24.19.0**, Python **3.12.14**, Pillow **12.3.0**, included EasyStar **0.4.4**. No npm install is necessary.

From this directory:

```
python tools/build.py
node --check runtime/signal.js
node --test tests/interaction.cjs
python tests/structure.py
node tests/native/routes.cjs
python tools/render.py
```

The source bundle includes its base TMJ/WAM and runtime atlases, so rebuild does not rely on an absolute workspace path. Build does not modify the original frozen candidate. Compare the file hashes in `MANIFEST.sha256` before acceptance. The manifest excludes itself and outer ZIPs.

## Checked versus not checked

- PASS: script syntax; 18 isolated interaction/lifecycle tests, including off-station (1050,320) journal/control access, non-destructive native Close, temporary confirmation cancellation, all sequence phases, wrong answer, premature activation, quiet default, audio off and ordering, stale callbacks, movement during initial-position query, close/reopen, reset, unload and two isolated visitors.
- PASS: original map layers unchanged; asset references; full-coverage transparent native-audio carrier; all state tiles are non-colliding; written/audio parity and quiet lawn.
- PASS: **800** source-native desktop/touch route legs, all ordered station pairs including same-cell, all **16** light states, **2,624** active visibility rebuild/replans, **1,118,624** sampled positions. **0 collisions, 0 endpoint drift**. These execute actual extracted engine methods and real EasyStar; browser/renderer/body services are fixture adapters.
- Static review renders are rebuilt from actual TMJ tiles. They are **not in-game screenshots**.
- NOT RUN: isolated full game, real browser popup layout/autoplay/controller behavior, multiplayer networking, real Woka rendering/seating, physical Android/iPhone/Safari audio or microphone coexistence. Two visitor fixtures prove local script isolation only.

## In-game review checklist

Fresh session: start quietly, use touch/right-click and keyboard, collect out of order, make a wrong final choice, finish, close/reopen from journal, reset, repeatedly cross station thresholds, leave the map and reload. Check rings are reachable without touching walls and that character depth remains natural. Confirm final glow is visible without covering walkable surfaces. Phone viewport: every popup button remains tappable and no dialog traps movement. Enable optional shoreline signal, use native mute/master/pause/Stop, walk to the lawn, return, disable sound, finish/reset/unload; no preference override or residual sound. Reload after testing both engine and map versions. Check a second visitor remains independent.

## r2 independent-review correction

The r1 global journal incorrectly fell back to the dock’s world-anchored popup when away from every station. r1 remains unchanged. r2 removes that fallback: the global journal always calls the verified `WA.ui.displayActionMessage` screen-space API; nearby ring popups are used only when `current` identifies a ring. Both sound-off and confirmed restart work from any map position.

The pinned production `PopUpTriggerActionMessage.svelte` renders a native button literally labeled **Close** (also triggered by SPACE). r2 never makes that button accept a destructive restart or open an unrelated popup: it only dismisses/cancels. Confirmation is an explicitly named temporary menu command. Generation tokens invalidate that command on movement, Close, another message or disposal. Production component snapshots are included under evidence/api. A dynamic confirmation menu must still be checked in the actual game UI for visibility/usability.

Browser acceptance was attempted by the independent r1 reviewer but blocked before launch by Chromium process-singleton socket restrictions. r2 does not bypass this restriction or claim a browser, mobile-layout or audio-hardware pass. Review renders and native-route checks are unchanged in scope. Real popup dimensions, screen-message wrapping and menu behavior remain isolated-game acceptance gates.
