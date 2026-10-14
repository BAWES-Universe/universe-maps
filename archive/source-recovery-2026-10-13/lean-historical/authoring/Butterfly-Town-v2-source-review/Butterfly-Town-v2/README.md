# Butterfly Town v2 integrated review candidate

Local candidate only. V1 remains frozen and published separately; this task has not pushed, merged, or deployed v2.

## What changed

- Removed repeated off-map filler and blended the gate/world edges into the room backdrop. User zoom and Places controls remain unchanged.
- Traced both entrance paving edges against the expanded artwork, with solid lamp/planted supports and genuine-alpha foreground foliage. The lower paved approach now reaches a deliberate faded boundary instead of an early invisible wall.
- Animated eight actual terrace cascades with masked down-flow and light basin mist. Preserved the corrected, visibly animated fountain below the player/foliage layers.
- Cleared opaque doorway floor from above-player architecture for all three interiors.
- Added ONE separate walnut/brass study desk and teal parked-chair proposal with a reachable north-side standing workspace. This is not a sitting interaction or a promise of independently Y-sorted furniture. The east-side approach and south aisle are usable; the parked chair meets the west fixtures, so there is no outer-left loop. Other arrangements remain for user feedback.
- Integrated very quiet, nearby-only fountain/cascade audio through native map properties. Arrival, the central gate path and functional interiors stay silent. There is no town score or gate cue. Runtime activation remains OFF until the compatible native audio fix and device/listening acceptance are complete.

## Source sharpness diagnosis

The town uses native 1536×1024 source plates and already reads clearly at 1×. The expanded gate source is 1254×1254 enlarged to 2048×2048, so some softness is in the artwork itself. No destructive sharpening, additional upscaling, camera restriction, or claimed lossless detail recovery was applied. Desktop and mobile-sized source renders plus actual scale/filter metadata are under evidence/boundary-audit. Real high-DPI phone acceptance is still outstanding.

## Review/run

1. Python 3 + Pillow: `python tools/build_map.py`
2. Run `node tests/run-state-tests.cjs`, `node tests/run-audio-tests.mjs`, `node tests/run-audio-integration-tests.mjs`, `python tests/check-scenery-assets.py`, and `python tests/check-water-order.py`.
3. `node tools/validate-engine.cjs` uses the supplied bundled native map validator.
4. Run `python qa/server.py`; open `http://127.0.0.1:8812/qa/integrated-review.html`.
5. Use explicit visual, gate-edge, cascade-pixel, native-audio, and recording buttons. Audio review is opt-in and QA-only. Pure native audio checks run without the optional recording tap.
6. For an exhaustive collision sweep, open `/evidence/boundary-audit/` and click “Audit every collision face”. It fingerprints the loaded TMJ and rejects a stale map.

The supplied native-audio review bundle is ready to use. Rebuilding it requires the separate Universe checkout at PR712 commit 93939afff9862c5bf43876288cd5d5bd692b277c and its dependencies; set NATIVE_AUDIO_ROOT and run `node qa/build-native-audio.cjs`. Exact component hashes are recorded in evidence/native-audio-source-pin.json.

## Candidate addition

`candidate/public/butterfly-town/v2/` is a self-contained runtime folder with relative assets/scripts/audio. `candidate/INDEX-PROPOSAL.md` describes the small optional version entry. Keep v1 as the current/default map until owner approval. No WAM import, backend, paid service or engine change belongs to this map addition.

AUDIO-INTEGRATION.md documents supported APIs, default-off activation, intrinsic audio levels and the unsupported-volume mobile limitation. CLAUDE-REVIEW.md is the independent-review prompt.

## Verification boundaries

See RELEASE-V2.json and the named evidence reports for exact current stages, hashes and counts. Historical checks remain labeled as historical. The earlier 213/213 scenery run preceded the original water-only correction; its later full rerun stalled and is not presented as a final integrated pass.

The harness uses actual Phaser 3.86, AnimatedTiles and pinned native movement/depth primitives. The native audio review uses the actual patched Svelte component/store/controller. Scene transport, camera and map property dispatch are documented adapters. Neither is a full hosted Universe/two-client acceptance session. Desktop mobile-sized viewports are not physical iOS/Android or Retina-device acceptance. Listening calibration and actual host MIME/CORS remain release gates.

Frozen v1 source hashes are retained in evidence/frozen-v1-sha256.json. Original generated artwork and historical audio design work remain preserved in the source archive; superseded music is excluded from the versioned runtime folder.

The supplied visual walkthrough has audio omitted because cloud capture synchronization did not validate. Separate fountain/cascade MP3s are source previews only. The 16-check native component evidence remains independent of recording. Native QA is now guarded by immutable bundled source snapshots from93939aff; later native revisions are outside this test claim.
