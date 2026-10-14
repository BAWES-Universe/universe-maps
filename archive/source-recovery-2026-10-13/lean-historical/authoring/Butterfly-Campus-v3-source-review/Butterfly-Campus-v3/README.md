# Butterfly Campus v3 · local candidate

A new StudentHub workplace and public student campus: quiet monumental Butterfly Gate, central fountain and couch/carpet commons, StudentHub reception/teamwork/three meeting rooms, Learning Hall, Lantern Stage and audience, Media + Design, R&D, Operations + Sales, and four public market booths.

## Open locally

Serve this folder with Python and open `/qa/` in a local browser. The review harness uses real Phaser3.86, the accepted32px Greg avatar and source-pinned depth/physics primitives. It is a reproducible source harness; it is not the complete Universe client.

The import entry is `map/butterfly-campus.tmj`. Keep its `tilesets/`, `scripts/` and `audio/` folders beside it. All map assets are self-contained relative references. No publication is included in this deliverable.

## Implemented

- Same-map gate/campus travel and return, with player-local layer reconciliation.
- Local interior reveal: each building's roof gives way to its own floor, walls and independently placed furniture.
- Permanent collision independent of roof, scene and reduced-motion visibility.
- Purposeful larger room plans at unchanged Woka/furniture scale.
- Reachable table, desk, stage, classroom and market approaches.
- Native tile water/butterfly animation; reduced-motion fallback retains static water art.
- Deliberate finite island boundaries, connected promenades and directional signs.
- Bounded fountain/cascade audio is implemented through native map properties, with quiet functional interiors. The deployment flag remains off until the compatible engine is deployed and listening/device acceptance is complete.

## Prepared integrations

`integration/interaction-hooks.json` names editable activity areas for later approved guides, bots, Linear, Attio, image/music/design workflows and market interactions. These definitions do not impersonate or claim connected bots.

`integration/native-areas-proposal.wam` is a schema-verified native meeting/stage configuration proposal covering the three meeting rooms, full teacher/student classroom, design-review area and stage/audience. It is outside the importable TMJ package and has not been activated. Universe must load it through its supported WAM/map-storage room route, or an operator can reproduce the areas in the native area editor. Hosting it beside a TMJ alone does not activate native rooms. See `docs/NATIVE-AREA-SETUP.md`.

Furniture supports approachable standing positions. The current fork exposes no verified sitting animation API. Privacy, native media permissions, LiveKit sessions and bot/account bindings require deployment-specific acceptance.

## Review and rebuild

- `evidence/` contains overview and layout review images, geometry and source checks.
- `qa/results/` contains actual rendered/physics evidence with its execution scope stated.
- `docs/ASSET-CONTRACT.md` and `docs/ART-PROVENANCE.md` explain world scale, ownership and rendering decisions.
- `tools/build_campus.py` rebuilds the map from the included prepared assets and original light-room masters. For complete material regeneration, run `tools/prepare_assets.py`, `art-source/landscape-build-assets.py`, `tools/prepare_ground_variants.py`, and `tools/light_room_materials.py` first. After building, run `node qa/audio-sync-geometry.mjs`, `tools/prepare_integration.py`, and `node tools/validate-contract.cjs`. Tested build dependencies are in `requirements-build.txt`; the Linux renderer uses DejaVu Sans fonts.

The prior map versions, user avatar, native application and engine work are untouched. The candidate adds a versioned map folder only.

## Audio activation dependency

The included native water integration was tested against immutable engine head `3fccc2890dbd30ed48bdefe79b00be0e0c915af8`. That is source/component compatibility, not evidence the intended Universe environment has deployed it. Keep `ENABLE_NATIVE_AUDIO=false` until deployment, real-client and physical-device listening checks are complete. See `docs/AUDIO-ACTIVATION.md`. The silent walkthrough uses the deployment-default setting.
