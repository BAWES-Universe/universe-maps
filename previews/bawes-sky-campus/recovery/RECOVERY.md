# Sky-campus recovery — 2026-10-21

The compact native package is the current deliverable. See ACCEPTANCE.md for current test evidence and PUBLICATION-PROPOSAL.md for the isolated, unexecuted hosting action. Draft recovery PR: https://github.com/BAWES-Universe/universe-maps/pull/23.

Source was recovered from GitHub commit 08485166c2f9dfb208318ef862a46a031cbfdb8a (draft PR #22). The unuploaded e3f3514/5b6542f commits remain unavailable. No old executor or desktop was accessed. No publication, deployment, merge or permission change occurred.

Backup was proven before substantial edits: a local base64 blob matched the connector's returned Git hash, followed by create_tree/create_commit/update_ref with expected SHA and force:false. The resulting deb7f676e38cfa18e7fa8f0fcdcfff9ab070e760 ref was verified with git ls-remote. Subsequent CLI pushes checkpointed source, artwork, runtime, tests and archives on recovery/bawes-sky-campus-20261021. Both backup routes worked.

Repairs include bounded entrance/bridge artwork, two entrance seats moved into a functioning greenhouse cutaway, chair-shaped stage foreground masks, a lower café counter, cancellable seat-facing adjustment, bounded collision corrections and eleven reused water/lantern animation definitions. The compiler retains native 16px artwork and avatar scale 1. The final package composites compatible static backgrounds and omits empty/unreferenced inactive layers, reducing 39 layers to 25 with no resampling; interactive layers are identical and the compiler checks intervening artwork for overlap.

A real gate timing defect was found during the raw-package run: a late closing frame shifted a stage path by 32px. The candidate-local runtime now postpones gate frame changes while moving. The subsequent compact all-seat run passed the affected path and all 71 positions/facings.

Two late automation crashes were initially misattributed to map memory exhaustion. The harness returned the Phaser camera object from startFollow, causing automation to serialize the entire scene and exhaust the heap. The corrected callback returns nothing. Valid 165 completed checks were retained, and finish-acceptance.cjs resumed the remaining checks on exactly the same map/runtime hashes, yielding 171 passing records. No earlier run's performance values were substituted. The earlier optimizer archive is superseded, not the publication target.

Runtime setup used a separate Universe worktree pinned to 274114560c5ec95fdf8e51e67986a53069f3cf06, regenerated protobuf/i18n/iframe assets, and Vite dependency-directory permissions. npm ci encountered an incomplete optional-platform lock; npm install --package-lock=false installed dependencies without changing that lock. No gameplay engine patch was used. Local backend persistence/authorization checks are disabled by the existing local-development mode.
