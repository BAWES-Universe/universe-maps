# Azure Pavilion — final independent review

PASS for the reviewed preview candidate. No unresolved seating, rear-wall, table, route, visibility, animation-integration, or audio-control blocker was found. Publication/package smoke remains the author's responsibility. This report describes the final state; prior findings are archived separately in independent-review-historical.md.

## Exact candidate

Actual runtime: isolated BAWES v0.3.8, engine commit274114560c5ec95fdf8e51e67986a53069f3cf06. Reviewer did not edit map or engine source, or unrelated Moonlit files.

SHA256:
- azure.tmj: 04e276eee6a0808937a554fe2ea141c048badf8a079c72ce481965bfc1bd35ba
- scene.js: 355006deffaa7bf75cb4567e7183419fbd9b7b01960ce7a0e34a372cf06b7f33
- coastal-unlabeled.png: 7497e143fa5410fb5696f13f32b33dc99a6fe8cb1205b72e0bd1fb22b9d6236d

## Fresh independent seating and rear-wall tests

All13 seats were retested after the final correction through the actual Settings → Take nearest seat menu. All reached their updated exact targets, faced south, remained visible, and retained camera zoom1/avatar scale1. All13 occupancy screenshots were visually inspected: bodies occupy the intended cushions; the six original chairs now align centrally, and all three settee positions occupy separate cushions. Ordinary keyboard movement exits every position. The settee exit was additionally tested fully around the coffee table:600,216 →584,216 →584,336. No lock or hidden avatar.

The map uses native pathfinding for approach and a bounded final seat-centering teleport (maximum12px) after successful arrival. This is position/facing occupancy with the normal native avatar, not a new sitting pose.

Rear-wall northward keyboard pushes at x592,624,656,688 all stop at feetY208. All four screenshots were inspected: avatar bodies remain below the façade beam and fully visible, with no wall penetration. The blocked rear strip does not depict a usable full-avatar-width passage.

Fresh evidence: /workspace/coastal-runtime/independent-seat-fix/seats.json; seat-0.png through seat-12.png; wall.json; wall-592.png through wall-688.png; settee-exit.json/png. These replace the previous seating-offset and rear-wall-overlap findings.

## Tables, connections, roof, and scale

All six unchanged tables previously passed24 independent actual keyboard pushes, one from every side, with settled approach positions. All24 screenshots were inspected; no avatar crossed onto a tabletop. Evidence: independent-cafe/tables.json and table-0-* through table-5-* PNGs. Final changes affect seat centering and the rear wall, not table footprints.

Final combined route evidence contains404 passing traversals across101 maximal runs and510 connected walkable cells:388 results retained only for exactly unchanged run geometry, plus16 author reruns covering every shortened rear-wall run. Reviewer checked the combined records' arrival, zoom1, scale1 and zero-popup fields. The original sweep was split between author and independent reviewer; the reviewer independently executed208 keyboard/right-click traversals before the final wall shortening. Do not describe all404 as independently executed. Final aggregate: /workspace/coastal-pavilion/review/full-route-results.json.

Actual independent keyboard roof tests confirmed hidden canopy inside at648,316 and restored canopy outside at648,469; avatar stays visible. Evidence: independent-cafe/final/roof-enter.png and roof-leave-clear.png. Roof code/art are unchanged by final seating/wall correction. Text-free façade and café/lounge/overlook art were visually reviewed at native scale.

## Water evidence and boundaries

Continuous independent capture: independent-cafe/final-ocean-fountain-12s.mp4,12.34seconds/156captured frames, covering more than three ocean cycles. Ordered frames show descending fountain droplets/ripples and shifting ocean caustic highlights. No obvious shoreline spill onto marble, tile seams, vanished patches, or avatar occlusion were seen. Ocean motion is animated highlights over painted water; fountain streams are stylized overlays.

Author final-gameplay-motion.mp4 was independently checked as a valid26.633second recording and reviewed through extracted ordered frames. It corroborates stationary water motion and walking through roof transitions. Review used sequential frames from continuous recordings, not continuous human playback. Maximum independent capture gap158ms limits any frame-perfect smoothness claim. Final wall/seat edits do not change animation or art.

## Audio

Final-audio-results.json and final-audio.cjs were independently reviewed; final-rendered-audio.webm decoded successfully (51.68seconds). Author used real menu clicks, with a passive Phaser-master-output analyser/recorder; no playback or context-resume call was injected by the test. Evidence confirms silent spawn (RMS0), actual playback (RMS0.0126437, HTTP200asset, looptrue, volume0.45), six playing movement checkpoints without prompts, then Stop/RMS0 and four further movement checkpoints plus keyboard movement remaining silent and prompt-free.

This is independently reviewed author runtime evidence, not a second independent audio run or physical-speaker listening. The final explicit menu toggles Play sea sound / Stop sea sound without an audio popup. It is a map-only fallback because native media Stop reapplies playAudio after movement in this engine. Audio code is unchanged by the final seat/wall correction.

CDP9222 released. No further map edits requested by reviewer.
