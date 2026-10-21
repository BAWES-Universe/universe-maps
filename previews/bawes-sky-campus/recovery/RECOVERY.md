# Sky campus recovery — 2026-10-21

Recovered source: 08485166c2f9dfb208318ef862a46a031cbfdb8a from draft PR #22. Branch: recovery/bawes-sky-campus-20261021.
The unuploaded e3f3514/5b6542f commits remain unavailable. No old executor or desktop was accessed. No publication, deployment, merge or permission change occurred.

Backup verified through both routes: local blob hash matched connector create_blob(base64), followed by create_tree/create_commit/update_ref(force:false, expected_sha). Ref deb7f676e38cfa18e7fa8f0fcdcfff9ab070e760 was verified by git ls-remote. Git CLI pushes subsequently backed up art/source/runtime/tests to 29c8a770430fe571205e4a32aec2960bc3b3850f and 1be728a.

Fresh baseline: 36/36 café path/seat-position checks passed in actual pinned Universe 274114560c5ec95fdf8e51e67986a53069f3cf06. Baseline did not test facing. A single preliminary headless Chromium FPS sample was 34.2, not a benchmark or a physical-phone result. Historical results are not current evidence.

Recovery changes under test: bounded registered entrance/bridge art repairs; two entrance seats moved into new greenhouse cutaway; shaped stage-chair masks; cancellable facing for all seats; eleven reused water/lantern animation definitions. Static geometry connects all 71 seats and all 12,671 walkable cells.

Initial all-seat test reached seats 0–10 with correct facing, then stopped at a closed meeting-room door. The harness now explicitly approaches each proximity door before entry. Full acceptance remains in progress; this checkpoint is NOT ready for publication.

The fresh runtime uses a separate pinned worktree and regenerated protobuf, i18n and iframe API assets. Vite explicitly serves installed dependency paths for fonts. npm ci found the source lock incomplete for optional platform packages; npm install --package-lock=false installed build dependencies without changing the source lock.

## Later runtime findings

The optimizer archive at a3ad353 is NOT ready: its renderer exhausted the ~4GB JavaScript heap after ~405 seconds. The first native retry also exposed a gate-animation path shift (stage target y3248 ended at y3280). These failures are preserved under evidence/optimized-* and native-final-*.

The candidate-local gate animation now pauses frame changes while moving. Runtime packaging removes six empty layers and three invisible, unreferenced steam layers, then composites six compatible background layers. The compiler verifies that these layers do not overlap intervening interactive artwork. This reduces 39 layers to 25 without resampling or altering interactive layers. Editable sources remain intact. The compact runtime is undergoing fresh all-seat/viewport/collision/motion checks; do not publish either archive yet.
