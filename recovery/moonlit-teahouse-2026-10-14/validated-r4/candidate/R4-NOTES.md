# Moonlit r4 tea interaction — additive local candidate

Derived from the preserved validated r3 candidate; r3 backup commit 2846e35fcd38253d01a5dd90e3583a3dd93ba356. No r4 push is authorized yet or performed. Older README, STATUS, REPAIR-NOTES and verification documents in this copy describe historical revisions; this note and the parent REPORT.md describe r4.

Walk to the accessible desk, choose Prepare tea, stay for 1.8 seconds, collect the cup, walk to the moon terrace and choose Serve tea. Leaving the desk region during preparation cancels it. Prepared tea is local to this script instance. Collection and serving are guarded state transitions with once-per-cycle messages; revisiting shows status rather than replaying success. Reset tea ritual is an unobtrusive Settings command. Actual room departure/rejoin starts a fresh ritual. There is no shared/persisted tea state and no sitting mechanic.

runtime/moonlit.js is the authored source and runtime controller; no transpilation. source/add-tea.py reproducibly adds original procedural cup, pot and native animated steam assets plus map layers/anchors to the r3 map. To rebuild all visuals run source/build.py followed by source/add-tea.py. The tea step is idempotent. R3 doors, glass, roof, water, audio and collision data remain unchanged. Tea layers are noncolliding decorations.

All assets are locally generated fixture art, not final artwork. Source/model tests are separate from actual Chromium journeys; see parent REPORT.md and final/evidence. R3-MANIFEST.sha256 is historical only. MANIFEST.sha256 identifies the r4 candidate.
