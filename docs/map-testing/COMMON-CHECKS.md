# Common acceptance checks

[All maps](../../MAPS.md) · [Register](README.md)

Use these once per tested map/revision, alongside its map-specific checks. Record a failure or N/A honestly; a checked box needs dated evidence. Backup completeness, historical source QA and HTTP 200 are separate from live acceptance.

## Identify the build first
- [ ] Record exact map ID/revision and TMJ SHA-256; include companion WAM, scripts, images/audio and full relative directory layout.
- [ ] Record the actual deployed engine commit, test environment/session URL and relevant PRs. Merged code does not prove a deployment contains it.
- [ ] Load a clean session; verify all local assets load, relative paths resolve and no blocking console/runtime errors occur. Do not expose secrets in evidence.

## Native movement, furniture and art
- [ ] On desktop, use keyboard and click-to-move through every meaningful branch, entrance, stair, cross-aisle and furniture approach. Check the full native player body/head footprint and real collision, not only a point-path overlay.
- [ ] Make rapid repeated destination clicks, reverse a route and click close to obstacles/same-tile positions. The latest valid destination wins; no stale route or teleport may override it.
- [ ] Visible empty floor is reachable where intended; walls, water edges, rails, equipment and actual furniture feet remain solid. A standing approach is not proof of sitting animation.
- [ ] At the real viewport/zoom, inspect player scale, foreground/lower-back depth, head visibility, glass transparency, cropped glows, stretched rugs, repeated art bands, black edges and seams. Record screenshots of unresolved rendering issues.

## Phone and touch
- [ ] Test actual touch input on a phone-sized viewport: tap targets, dialogue/menus, camera bounds, portrait/landscape and dismiss/reopen. State whether it was a real phone or only emulation.
- [ ] Test gestures after orientation/viewport changes; controls should stay reachable, readable and avoid unintended movement behind UI.
- [ ] For the #842 engine fix, test zoom before/after resize, orientation change, scene exit/re-entry and reconnect; confirm the deployed engine actually contains the merged fix. This does not by itself fix source-art pixelation or tile seams.

## Player names and DOM overlays

These checks cover [#916](https://github.com/BAWES-Universe/workadventure-universe/pull/916) (zoomed-out DOM alignment) and [#918](https://github.com/BAWES-Universe/workadventure-universe/pull/918) (remove hover enlargement). Both are merged source changes; first record a deployed engine build that contains them. Release availability and these live checks remain unverified. They are separate from #842 camera refit and do not close map-art pixelation, black-edge or seam complaints.

- [ ] Zoom out fully with the desktop wheel, use Look around on a large map, and pinch out on a phone. Player name pills stay centred above their players at the intended head gap; return to default and zoom in to check ordinary placement/size.
- [ ] While zoomed out, resize the window, open/close a side panel and rotate the phone. Names remain aligned; repeat after scene exit/re-entry and reconnect without stale DOM positioning.
- [ ] Hover or walk up to another player at default, far-out and close-in zoom: the pill becomes lighter and comes in front of other names, with **no extra 6% scale enlargement**. Text size/height remain at the resting scale. A long name may legitimately widen its pill when the full text is revealed.
- [ ] Test a long name and overlapping players: highlight reveals the full name and correct front ordering; removing highlight restores the dark/truncated name and normal depth ordering. Check the name stays centred throughout.
- [ ] While zoomed out, trigger a speech bubble, map popup and embedded website where configured; compare their alignment with default zoom and after panel/window resize. Record unsupported features as N/A. The source fix affects their shared DOM layer, but their live behavior has not been accepted by this register.

## Interaction, audio and multi-user
- [ ] For configured interactions, test happy path plus out-of-order/repeated actions, close/cancel/reopen and restart. No duplicate handlers, stuck panels or invented success.
- [ ] For audio/media, start from a fresh session and a deliberate user gesture; test mute, zone enter/exit, overlapping cues and cleanup. Confirm intended per-user versus shared behavior with two users.
- [ ] Where roles or speaker/listener zones exist, verify actual two-user boundaries, voice/media state and camera behavior; source configuration alone is insufficient.

## Interrupted sessions
- [ ] Leave/re-enter, reload and reconnect during movement and interactions. Restore only the intended state; avoid stale async completions, duplicated audio/listeners, cross-user progress or unintended teleportation.
- [ ] For puzzle/private-visit progress, verify visit scope and reset explicitly. For Keeper r2, retain the known teleport-recovery race as open until a reproduced test passes against a specific fix.

## Close the review
- [ ] Record date/tester, map and engine revision, device/viewport, observed result, reproduction steps and evidence URL on the map card.
- [ ] Keep design approval, source/native checks, hosted verification and live acceptance separate. A failure stays visible until a later exact-build retest closes it.
