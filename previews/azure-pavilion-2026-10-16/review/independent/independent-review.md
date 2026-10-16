# Azure Pavilion independent review — revised café candidate

Reviewer: non-author agent; actual isolated BAWES v0.3.8 runtime, engine commit 274114560c5ec95fdf8e51e67986a53069f3cf06. No map or engine source edited by reviewer.

Status: independent furniture, visual, motion and assigned corridor checks PASS. Final audio fallback author runtime evidence independently reviewed and accepted. Earlier audio/static-ocean details below are historical and superseded by the final-pass section.

Reviewed loaded TMJ SHA256: 7d93cd30ae0d778b66bfa72435a84b33f324c825094f4926c802087105870259. Author subsequently changed popup anchor x coordinates only; current disk TMJ 2e230066591c211bbe13934baff4db6d300e3f0265aaafa51e71aa21faa0fa3d. Controller d4117788765d3d42830c9f2bc492e741ed8186c8d169e6c491ca7a71b1e344df and café art fb117e29927f69e010e1aecc2d29d4e6c041f5bc3c683e631fe0f64407370be0 unchanged.

## Actual independent gameplay

All 13 targets were occupied through the real native Settings → Take nearest seat menu. All arrived at intended coordinates, facing south (native direction2), with camera zoom1 and avatar scale1. Ten chairs exit via ordinary down-key movement. Each settee position moves sideways; supplemental settled test proves full exit from x600,y216 via left to584,216 then down to584,336 around the coffee table. No lock or pose simulation. Evidence: seats.json, seat-0.png through seat-12.png, settee-exit.json/png. Original six chair cushions have a small roughly7px left offset at native grid-fit positions; occupancy is visibly on cushion and acceptable, not exact pixel centering. New café chairs and settee are well aligned. All seat screenshots visually reviewed; avatar remains visible and chair backs remain behind it.

All six tables received settled approaches and actual650ms keyboard pushes from all four sides (24 tests). All blocked the avatar before traversing the tabletop. Repaired lower overlook table now blocks correctly. All24 screenshots visually inspected. Café medallion edge is somewhat conservative north of table but does not eliminate circulation. Coffee table blocks directly in front of settee; leave around either side. Evidence: tables.json, table-0-* through table-5-* screenshots, props.cjs.

## Visual and motion assessment

Revised café art passes direction: substantial lounge seating and café islands address prior empty appearance, while preserving broad marble circulation. Ocean/balcony, cream-and-brass architecture, teal upholstery and planting read coherently at native zoom. Interior roof cutaway leaves the character visible; outside screenshots show glass roof restored. Art has not been rescaled by runtime.

Continuous native runtime capture: fountain-motion-8s.mp4 (139 captured frames across8.4567 seconds; timestamp-preserving encode at15fps). Initial camera finishes its approach before settling. Sequential stationary-view frames60/64/68 visibly show bright droplets moving down side streams and changing ripple rings. This is visible stylized fountain flow, not merely a frame-count claim. The overlay is brighter and simpler than painted art, but visually integrated with its basin and spout. Ocean/background caustics remain static; do not describe the entire water surface as animated.

Author audio evidence separately reviewed: audio-results.json and styled-sound-popup.png. Actual Play click gives nonzero captured master output; actual Stop gives zero output persisting after movement; six crossings do not prompt. This is author-executed runtime evidence, not independent physical-speaker listening. Final anchor placement reload remains author gate.

## Remaining gate

Run the full maximal corridor traversal checks and final popup-anchor reload. Independent sweep52..103 is in progress in routes/results.json, using actual keyboard and native rightclick both directions. Native pathfinding only positions the avatar before each test. Reviewer harness waits for actual settled arrival after roof-induced replan and uses bounded keyboard presses to avoid CDP timing overshoot. For a one-tile northward click, it selects the north portion of the same destination tile: release engine GameSceneUserInputHandler ignores right clicks intersecting the Player sprite. The engine still chooses the same native destination tile center; no synthetic movement is used for traversals. Initial overshoot diagnostic is retained separately; it is not counted as a passing traversal.


## Final pass — text-free art, ocean overlay, corridor completion

Final loaded map SHA256 0ad78bfdb4ec625291b5a43692da2f693aed81a249f1a9810e9f9a85583e4a8a, artwork coastal-unlabeled.png SHA256 7497e143fa5410fb5696f13f32b33dc99a6fe8cb1205b72e0bd1fb22b9d6236d. Final fallback controller reviewed from source: b1b4e1fd6ff126b43fa668ca11d38fa919438e2ecbab87a804b63bc398224881. Loaded visual pass preceded this audio-only controller update; seating and roof code are unchanged.

Independent assigned maximal runs52..103: all208 native traversals PASS (keyboard and right-click, both directions). Each recorded zoom1, avatar scale1, zero visible popups. routes/results.json contains exactly208 results; diagnostic failures are separately named and not counted. Author reports complementary runs0..51 passed208; combined416 is author-aggregated evidence, not416 independently executed tests. Keyboard timing overshoot and near-avatar click handling were harness corrections only. Paths beside café tables, both sides of planters, lounge thresholds and overlook connections are represented by these maximal corridor runs.

Final art reload: final/lounge.png, cafe.png, overlook.png and shore.png inspected. Façade lettering removed; furniture remains aligned with tested occupancy and obstruction positions. No visible shoreline overlay spills onto marble or occludes avatar. A minor existing visual limitation remains at rear lounge row5: the avatar can overlap the façade beam vertically in the narrow strip behind settee; it stays visible, but this is not pixel-perfect wall occlusion.

Actual keyboard roof entry reached648,316 with canopy hidden; outward movement to648,469 restores canopy. Evidence final/roof-enter.png and final/roof-leave-clear.png. The intermediate y403 frame was before the clear outside point and is retained as diagnostic. Both final states visually inspected; no avatar hiding.

Final continuous capture final-ocean-fountain-12s.mp4 contains12.34s,156 frames across more than3 ocean animation periods. Ordered native screenshots and final/ocean-sequence.jpg show broad caustic highlights shifting and pulsing on existing ocean art, with fountain droplets/ripples also continuing. No obvious shoreline seams, vanished patches, or water overlay over floor/avatar were seen. This is animated caustic highlighting over painted water, not a fully simulated moving ocean. Native screenshots show motion integrated without camera/avatar scaling. Review used ordered frames from the continuous clip, not physical continuous-video playback. Maximum capture gap158ms limits certification of frame-perfect smoothness; no multi-second capture stall. MP4 retains actual timestamp ordering and is available for human playback.

Audio supersession: native Stop was reported by author to restart after walking because engine property caching reapplies playAudio. Do not claim that native control works reliably. The final source uses one explicit native menu command toggling Play sea sound / Stop sea sound, backed by WA.sound, and does not register audio in movement callbacks or show an audio popup. Spawn does not play sound. This source design addresses the defect without engine edits, but final actual audible-output, Stop-persistence and crossing tests belong to author evidence and remain the remaining gate at this report's completion. No independent physical-speaker listening is claimed.

Independent browser CDP9222 released. No map, engine source, or unrelated Moonlit files modified by reviewer. Preview visual/gameplay acceptance passes within the limitations stated; final audio runtime evidence was subsequently reviewed and accepted below; publication/package smoke remains an author gate.


## Final audio gate closed

Independently reviewed /workspace/coastal-runtime/final-audio-results.json and final-audio.cjs, and decoded final-rendered-audio.webm successfully (51.68seconds). Harness uses real native menu clicks for Play sea sound and Stop sea sound. Its WebAudio analyser/MediaRecorder taps Phaser master output without calling play or resuming the context. Evidence supports silent spawn (RMS0), actual rendered playback (RMS0.0126437, HTTP200asset, looptrue, volume0.45), six playing movement checkpoints with nonzero output and zero popups, then Stop with RMS0 and four further movement checkpoints plus keyboard movement remaining silent and prompt-free. Audio gate PASS on author-executed evidence independently reviewed. This is not a second independently executed runtime test or physical-speaker listening. Dynamic explicit Play/Stop menu is the documented fallback for unreliable native media Stop, not a custom popup.

Final author gameplay recording also reviewed after successful finalization: /workspace/coastal-runtime/final-gameplay-motion.mp4, duration26.633s, size5,325,529bytes. Extracted ordered frames every3seconds corroborate the initial stationary water view, changing fountain/caustic phases, visible avatar walking into the lounge with canopy hidden, and walking back outside. No popup obscures those sampled frames. Contact sheet is author-video-frames/sequence.jpg. This is review of extracted frames and file integrity, not a claim to continuous human playback. Existing independent12.34s recording and direct keyboard roof tests remain complementary evidence.

All requested independent review gates are now closed except publication/package smoke, which remains the author's responsibility. No further map edits are requested by this reviewer.
