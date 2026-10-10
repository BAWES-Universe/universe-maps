# Corrective A acceptance scope

Frozen map SHA256: `50c07de93567b15d7b5170bca02a4fe2b43dd5865fe02f6b90d06605947e2b85`. WAM SHA256: `2504f5871750964aa6972f88bb4071ccbca73aa74847d84398637d18838954c2`.

- Native32 lossless atlas reconstruction: byte-exact.
- Independent final schema/role/quiet checks:29/29 pass. Repair/preservation checks:30/30 pass.
-2,110 open native cells, all connected.259 clear anchors. Exactly16 silent cells at spawn.
-1,821,010 reachable integer body placements: zero tested head conflicts.4,356 conservative spawn samples: body/head safe and quiet.
- Full unpatched-source90a148c route replay:11,818 commands,11,802 normal movements pass,16 separately classified existing same-cell exceptions,32,353,173 swept samples.
- Full merged-source60e7afd replay:11,818/11,818 commands pass,32,351,804 swept samples.
- Both route replays: zero collisions, head conflicts, unintended meeting entries, loops or mapChanged events. Accepted desktop/touch-pointer pathways and explicit directional boundary vectors are tested; this does not execute real Phaser keyboard integration.
- Whole-hall native focus is camera-only. Source-executed fresh-focus cases contain the hall/stage/speakers and tested exit landings. Native resize/rotation has a documented stale-zoom/padding limitation.

No live rendering, browser session, device interaction, media join, network isolation, production release parity or concurrent capacity is established by these checks. The movement harness uses a camera stub; native camera class/math verification is a separate fixture. `staticOnly:true` in the route reports means no dynamic tile/layer mechanism exercised by that replay; the real TMJ still contains a native focusable area.

Hall base/foreground pixels are exact. The four meeting rugs are unchanged outside2,986 base pixels in lounge02’s top16px strip belonging to its declared wider north divider; all16 group-chair and four group-table artwork rectangles are exact. This is an intentional divider ownership change, not a blanket claim of unchanged full rug bounding rectangles.

PR799 is merged into universe-develop but deployment was not verified at freeze. Runtime focus does not require decorative layer changes or PR799. Known same-cell behavior on an unpatched deployment remains recorded rather than hidden.
