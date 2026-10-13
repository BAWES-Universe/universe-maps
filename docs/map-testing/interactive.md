# Interactive story experiences

[All maps](../../MAPS.md) · [How to test and record feedback](README.md) · [Common acceptance checks](COMMON-CHECKS.md)

Start with the [interactive experience and engine-PR guide](EXPERIENCE-GUIDE.md). Neither archived puzzle candidate has a verified current game-session link.

## Jump to a map

- [Lighthouse: The Last Signal · r2](#lighthouse-last-signal-r2)
- [Lighthouse: The Keeper’s Return · r2](#lighthouse-keepers-return-r2)

<a id="lighthouse-last-signal-r2"></a>
## Lighthouse: The Last Signal

- Map ID: `lighthouse-last-signal-r2`
- Exact review revision: **r2**
- Purpose/category: Events / Exploration
- Record role: Current candidate
- Current state: Original r2 source and runtime recovered; unpublished; live acceptance open
- Source/evidence: [Original r2 source](../../archive/source-recovery-2026-10-13/baselines/lighthouse-last-signal-r2-source/)
- Recovered runtime revision: **lighthouse-last-signal-r2-runtime** · [Entire runtime folder](../../archive/runtime-recovery-2026-10-13/lighthouse-last-signal-r2-runtime/)
- Runtime Git upload: **pending verification**; runtime links are planned destinations and may not open yet.
- Runtime entry: [TMJ](../../archive/runtime-recovery-2026-10-13/lighthouse-last-signal-r2-runtime/lighthouse-last-signal.tmj) · [WAM](../../archive/runtime-recovery-2026-10-13/lighthouse-last-signal-r2-runtime/lighthouse-last-signal.wam)
- TMJ SHA-256: `3f0da81589faee13032922a438cdac5d3fa33ed87f22752c1b826abbde993b0e`
- Play/session URL: **not verified**. Archive/GitHub file links are not deployment URLs.
- Retained historical evidence (not a new test result): PASS_SCOPED: 18 interaction tests, 800 native route legs; independent replay

### Test next

- [ ] Inspect the rings and collect LOW, MIDDLE and HIGH notes; restore the beacon and check the visible completion feedback.
- [ ] Test out-of-order actions, repeat clicks, close/reopen and restart; verify progress is private to this visit and another player is unaffected.
- [ ] Enable optional shore audio with an intentional gesture; leave/re-enter its zone, reconnect and verify mute/cleanup behavior.
- [ ] Run the applicable [common acceptance checks](COMMON-CHECKS.md) on this exact map and engine revision; record N/A with a reason for absent features.

### Feedback and decision

Imported verbatim from workbook v22, `Map review index!P82:W82`. Blank fields are intentionally blank. Historical wording is preserved even when it mentions an older attachment.

- Design review: Pending
- Desktop test: Not tested
- Phone / touch test: Not tested
- Media / multi-user test: Not tested
- Tester: 
- Test date: 
- Decision: Pending
- Feedback / next change: 

Add a dated result below; keep prior feedback and identify the exact map/engine build.

- New test date / tester:
- Map revision / engine commit / deployment URL:
- Device / viewport / zoom:
- Result / reproduction / evidence link:
- Decision / next change:

<a id="lighthouse-keepers-return-r2"></a>
## Lighthouse: The Keeper’s Return

- Map ID: `lighthouse-keepers-return-r2`
- Exact review revision: **r2**
- Purpose/category: Events / Exploration
- Record role: Current candidate
- Current state: Original r2 runtime recovered; full original authoring missing; reconstructed authoring is separate; known teleport-race failure
- Source/evidence: [Reconstructed authoring (not original)](../../archive/source-recovery-2026-10-13/reconstructed/keeper-r2-editable-reconstruction/)
- Recovered runtime revision: **lighthouse-keepers-return-r2-runtime** · [Entire runtime folder](../../archive/runtime-recovery-2026-10-13/lighthouse-keepers-return-r2-runtime/)
- Runtime Git upload: **pending verification**; runtime links are planned destinations and may not open yet.
- Runtime entry: [TMJ](../../archive/runtime-recovery-2026-10-13/lighthouse-keepers-return-r2-runtime/enterable-lighthouse-r2/runtime/keepers-return.tmj) · [WAM](../../archive/runtime-recovery-2026-10-13/lighthouse-keepers-return-r2-runtime/enterable-lighthouse-r2/runtime/keepers-return.wam)
- TMJ SHA-256: `94bdc3c6dbd4ccf9a096b828016795083497f39da6f5f4c2ab2b8080b48634aa`
- Play/session URL: **not verified**. Archive/GitHub file links are not deployment URLs.
- Retained historical evidence (not a new test result): PASS_SCOPED: 13 interaction tests, 228 native route legs; 19 runtime files exact

### Test next

- [ ] Enter and leave the house, workshop and lantern room; collect chart/key/fuse and complete power, telescope, lens and signal steps in order.
- [ ] Reproduce the inherited teleport-recovery race: interrupt/overlap room transitions, reconnect during a pending transition and verify no stale completion relocates the player.
- [ ] Repeat, cancel and restart puzzle actions; verify private visit progress, no duplicate UI/listeners and correct room recovery. The known race is not fixed by backup.
- [ ] Run the applicable [common acceptance checks](COMMON-CHECKS.md) on this exact map and engine revision; record N/A with a reason for absent features.

### Feedback and decision

Imported verbatim from workbook v22, `Map review index!P83:W83`. Blank fields are intentionally blank. Historical wording is preserved even when it mentions an older attachment.

- Design review: Pending
- Desktop test: Not tested
- Phone / touch test: Not tested
- Media / multi-user test: Not tested
- Tester: 
- Test date: 
- Decision: Pending
- Feedback / next change: 

Add a dated result below; keep prior feedback and identify the exact map/engine build.

- New test date / tester:
- Map revision / engine commit / deployment URL:
- Device / viewport / zoom:
- Result / reproduction / evidence link:
- Decision / next change:

