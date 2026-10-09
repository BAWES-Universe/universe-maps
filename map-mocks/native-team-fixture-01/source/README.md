# Native StudentHub workstation calibration

A bounded 512×384 native geometry proof for the larger connected team office. This is a two-person module, not a claim about the size of the StudentHub team or a finished interior design.

The new transparent workstation preserves a 64×64 desk and a 30×36 chair at the unchanged 32×32 Woka scale. Two real full chair backs cover the torso while keeping the protected head pixels clear. The neutral receiver is deliberately for visual/physics calibration; coherent flooring, planting, architecture and shared lighting belong to the next composition pass.

## Preserved sources

- `fixture-plan.json`: proposed exact geometry, seat anchors, head region, collision and entry/bypass routes
- `applied-art-manifest.json`: actual measured art extents, alpha thresholds and the accepted 2 px back-top variance
- `art-source/single-station-master.png`: original image-generation output, 1086×1448
- `art-source/single-station-native.png`: one controlled premultiplied downsample to 96×128, containing the visible64×64/30×36 objects
- `art-source/fixture-chair-backs-native.png`: semantic source-pixel assignment to above-player backs
- `assets/greg-reference.png`: unchanged scale-reference avatar sheet, not an account-avatar change
- `tools/compose_native_proof.py`: reproducible static assembly
- `qa/`: actual Phaser/Arcade inspection harness and evidence, with explicit source-harness limitations

`art-source/attempt-01-failed-registration.png` preserves the first attempt. It made the desks too wide and used the wrong projection despite a whole-scene guide. It was rejected internally. The second method authored a single station against a silhouette guide; repeating that measured module at known coordinates kept native scale under direct control. Exact generation prompts and guides are saved.

The original generated asset is `authoring-session/generated_images/exec-ba7658f0-68b2-4559-9ef8-723d8eec84f6.png`; its copied master is preserved here. The failed whole-module generation was `exec-0e1324ea-f10c-4342-a8ea-9b06739c1805.png`. Generated furniture is original. No new public license is assigned by this experiment; bundled third-party runtime files retain their existing notices.

## Evidence and limits

Independent static review found zero changed pixels in each avatar's protected14px head strip, while the meaningful chair back changed389/544 pixels in the torso-region rectangle. Both are unchanged32px Greg scale fixtures. They are not two live users or a multiplayer test. Runtime evidence is separate under `qa/results/`.

The actual back begins worldy193, 2 px below the proposed191; this variance is recorded rather than changing the avatar anchor. Alpha1–4 source fringes extend beyond solid art, so collision is never derived from a raw nonzero-alpha bounding box.

Personal-area claiming requires real WAM area configuration and the relevant room/editor permissions. Candidate footprints in the plan are geometry guides only. No users, owner UUIDs, claim policies, live services or permissions were configured. Baked map furniture is not automatically editable through claiming.

No existing map, published asset, engine source or prior experiment was modified. The larger campus plan is separately proposed in the expanded-office/riverside study.
