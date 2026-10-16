# Independent real-gameplay review

Final targeted collision review: PASS. Seating and selected water highlights also pass the independent review described below. The author’s final regression and packaging reload evidence have now closed the remaining local acceptance gates, as recorded below.

Final reviewed candidate SHA-256:

- moonlit.tmj: `c776df59952a83a843ad9f49ee262f1975110be93de18d28ea0c6e53d56e1815`
- scene.js: `66198fe5316a5a6a36907e6eb55ad24163c67970dde77452e3006502dc1fcd2b`

Reviewer was not a map author and made no map changes. Controlled the real local WorkAdventure game through CDP, invoking the same iframe `takeSeat()` callback registered by the native menu and using actual ArrowDown/ArrowUp/ArrowLeft/ArrowRight keyboard events. No teleports, custom avatar pose or collision bypass. Evidence: `/workspace/moonlit-runtime/independent-final/`.

## Ten-seat assessment: PASS

All ten seat actions returned true. Every left chair ended facing right toward its table; every right chair ended facing left. Each seat allowed an ordinary ArrowDown exit of more than60px without a freeze or special exit control. All screenshots independently inspected. Native zoom and Woka scale remained1.

| Chair | Occupied feet | Visual judgment |
|---|---|---|
| Upper west left |216,250|Natural chair overlap, inward facing; pass|
| Upper west right |268,250|Corrected registration resolves previous rightward offset; pass|
| Upper east left |408,250|Natural chair overlap, inward facing; pass|
| Upper east right |456,250|Corrected registration resolves previous edge alignment; pass|
| Terrace left |1168,536|Aligned with cushion, inward facing; pass|
| Terrace right |1240,536|Adjusted target aligns with cushion; pass|
| Lower west left |1104,1464|Aligned with chair, inward facing; pass|
| Lower west right |1168,1464|Aligned with chair, inward facing; pass|
| Lower east left |1360,1464|Repaired group registration aligns chair, inward facing; pass|
| Lower east right |1424,1464|Repaired group registration aligns chair, inward facing; pass|

This accepts the user's clarified native occupancy convention, not a dedicated sitting animation. Existing avatar remains upright as supported by the engine.

## Water evidence: PASS for selected animated highlights

Captured fresh continuous actual-runtime video with camera off, timestamp-preserving CDP frames, native zoom/scale1. Files:

- `fountain-motion-8s.mp4`: uninterrupted eight-second hold.
- `upper-waterfall-motion-8s.mp4`: uninterrupted eight-second hold.
- `water-and-traversal.mp4`: full continuous capture including paths between viewpoints, encoded15fps H264 CRF25.

Successive independently inspected native-view frames show bright changing stream streaks on fountain cascades/selected upper falls and changing fountain pool rings. Motion is materially visible compared with the original faint ripple tiles. Limitation: these are transparent animated highlights/rings over existing static art. Not every painted waterfall or water pixel animates. No claim of full fluid or scene animation. Camera preview is off throughout these captures.

## Final bed edges and restored paving: PASS

After the final collision candidate was reloaded, independently walked to both restored purple paving cells below the bed: feet (752,528) and (784,528). Both arrived through ordinary engine pathfinding. Their screenshots show the Woka visible on the paving in front of the bed, rather than on plants. The west path (560,464) and southwest paved alcove (560,560) also arrived successfully and show feet on paving.

Actual 1.2-second keyboard pushes tested the final boundaries. From the west path, ArrowRight stopped at feet (568,464), before the lamp/plant obstacle. From the east, ArrowLeft stopped at (872,464), outside the foliage. From restored under-bed paving, ArrowLeft stopped at (744,528), before the southwest planted island. All three boundary screenshots were independently visually inspected. All seven targeted checks retained native Woka scale 1 and camera zoom 1, with no audio popup detected. Earlier north/northwest/northeast and south boundary checks passed; these final changes addressed the remaining west/east and southwest mismatches.

Evidence: `final-collision-review.json`, `final-bed.cjs`, and seven `final-*.png` screenshots in `/workspace/moonlit-runtime/independent-final/`. The TMJ and controller hashes above were checked again after these tests and matched the tested candidate.

The narrow southwest diagonal shortcut remains closed where the existing lamp/planter does not provide a native 32px passage. The paved alcove is reachable from the west/north, and the purple path under the bed is restored and reachable via the east. This is acceptable for this repair, but is not a complete walkable southwest ring. Tile-grid borders do not promise pixel-perfect collision against every decorative leaf.

## Scope and evidence provenance

The ten-chair and continuous water recordings were made on TMJ hash `8a359738c24b89e1abe665f72698c6a85dc064637c1404559e359c54593be67a`; the controller hash was identical. Subsequent changes were bed/plant collision corrections, tested in the final targeted pass above. No furniture art, seating controller, water layer or scale changed between these passes. Earlier reports document rejected intermediate candidates and are superseded by this final targeted result.

Independent visual/gameplay review now accepts the tested seat occupancy, selected visible water highlights, avatar visibility and corrected central garden routes/boundaries. The author still owns the final full-map route and native-audio regression before publishing. This review is of the actual local game runtime, not a claim that the published remote preview has already been revalidated. CDP control was released to the author after completion.

## Packaging equivalence review

Final packaged TMJ SHA-256: `186e0d0c427f8be503597cecfc258385eedf880528f878607b024b7fca68f237`.

Independently compared the packaged map with `/workspace/moonlit-runtime/reviewed-before-versioning.tmj`. Reversing only the three revisioned asset references makes the parsed JSON exactly equal. Compact serialization plus a trailing newline reproduces the reviewed TMJ hash `c776df59952a83a843ad9f49ee262f1975110be93de18d28ea0c6e53d56e1815`; the snapshot's different raw hash was whitespace only. Collision data, layers, properties other than the script path, and gameplay content are unchanged.

Verified actual packaged asset hashes against the copy manifest:

- `interior-repair-20261016.png`: `73c40e6abcab454ba4b494bcec9acbfaea67f245e3ddb6387ad95c20c63a8aeb`
- `furniture-repair-20261016.png`: `525e4455324f98e5015da9a34ccdb7ffde944a754aea27cbb11975e1a9074be0`
- `scene-repair-20261016.js`: `66198fe5316a5a6a36907e6eb55ad24163c67970dde77452e3006502dc1fcd2b`, also identical to the independently recorded reviewed controller hash.

The packaging script copies the reviewed assets before restoring original artwork filenames; it does not transform their pixels or controller code. Packaging equivalence is accepted, conditional on the author's reload smoke confirming that the new URLs load successfully. No CDP control or gameplay changes were made during this packaging review.

## Author regression and native Stop limitation assessment

The author reports 31/31 final route goals passed, actual Brew/Collect/Serve and Walk to fountain button interactions passed, and native audio was enabled through the actual settings menu. Reported checks found native Pause/Mute persisted over six water-region crossings, volume 0.925 persisted at 31 route checkpoints, and an audio-popup observer recorded zero hits across 1,159 samples. These are author regression results, not additional independent browser tests.

The author also found an existing native-engine Stop behavior: it clears the remembered properties, then movement can reapply the persistent playAudio source. The paused setting still holds; the map's explicit Mute water action clears playAudio completely and remains silent during later walking.

Independent assessment: this is an acceptable disclosed engine limitation for the preview repair, provided the described behavior is accurate and the reload smoke passes. Silent spawn, explicit audio opt-in, absence of walking-triggered prompts, and persistent native Pause/Mute satisfy the requested audio behavior. Do not claim every native control is correct: document that native Stop can have its source reapplied on movement, and direct persistent-silence users to native Pause/Mute or the map's Mute water action. An engine repair is outside this map-preview scope. If audible playback were to resume despite prior Pause/Mute, that would be a material blocker; the reported tests did not show that behavior.

## Final local acceptance gates closed

Independently inspected the author's `/workspace/moonlit-runtime/packaged-smoke.json`. It records `passed: true`, silent fresh spawn, HTTP 200 for the map, all three revisioned assets and water-flow.png, and actual native-menu seating at sprite (268,234), equivalent to feet (268,250), with zoom/scale 1. Its served map SHA-256 is `186e0d0c427f8be503597cecfc258385eedf880528f878607b024b7fca68f237`, matching an independent current-disk hash check; the versioned controller still matches the reviewed controller hash. This closes the packaging reload condition. The JSON does not separately enumerate the author's reported upper-path/under-bed traversal, so those remain covered by the earlier independent gameplay evidence and attributed author report.

Together with the reported final route/audio regression above, there are no remaining local acceptance blockers from this review. Accept the corrected preview for publication with the documented limited water animation, narrow southwest shortcut, native upright seat occupancy, and native Stop caveat. This is not a claim of post-publication remote testing; publication status and exact commit are to be supplied by the author.
