# Interactive experiences and exact PR dependencies

[All maps](../../MAPS.md) · [Lighthouse checklists](interactive.md) · [Repair checklists](repairs.md) · [Hosted test builds](hosted.md)

Runtime review: 13 October 2026, 12:04 UTC. #842, #815 and both engine branches refreshed at 12:10 UTC; the other PR reads remain the earlier snapshot. Runtime descriptions come from preserved source. No live room, merge, deployment or publication was performed.

**Best actual interaction candidates:** Keeper’s Return r2 and Last Signal r2. Neither has a verified current play-room URL. Last Signal is the strongest demonstrable consumer of the native audio/proximity/pathfinding PRs; Keeper uses existing map APIs for a richer silent indoor puzzle.

**Latest release update:** #842 merged at 12:07:42 UTC as `09b61364b330edb1ece68020daca14c9d9ea2803`. Its merge is a verified ancestor of the current #815 / `universe-develop` head `49c07646b9974ed49131e5dc65bcbcf1eed3c14b` (two commits ahead, none behind). The user reports it is intended for the next release; #815 is still open/unmerged. No deployment or running frontend version was verified.

**Do not equate “merged”, “hosted TMJ” and “playable”.** The engine’s production-source branch `universe` still points to `42ba35bd6eefeb4f74359114904d167cbaecf1ad` (release #800). A running frontend SHA and actual game/device acceptance were not verified. Companion WAM areas require import/configuration; a TMJ link alone does not establish them.

### What can actually be tried once an isolated room is available

#### Lighthouse: Keeper’s Return · r2 retained runtime; reconstructed editable source

Enter the keeper’s house, lighthouse workshop and upstairs lantern room using same-map doors/stairs. Read the chart, collect a brass key, install a fuse, charge the generator, solve the telescope and lens choices, then send the three-note sequence to illuminate the beacon.

- Runtime status: Unpublished candidate; no verified game-room URL.
- Exact PR relationship: [relevant engine fix not proven map pin](https://github.com/BAWES-Universe/workadventure-universe/pull/799): The retained controller toggles decorative layers and uses native floor movement; #799 fixes click/tap destination drift across layer replans. No exact Keeper engine deployment pin was retained. [not used](https://github.com/BAWES-Universe/workadventure-universe/pull/727): Controller has no nativeSoundscape or audio call; the experience is explicitly silent. [not required by map api](https://github.com/BAWES-Universe/workadventure-universe/pull/842): Controller uses existing UI, room visibility and player teleport APIs; no new camera API is requested.
- Remaining limit: Original authoring archive missing; reconstruction preserves runtime bytes. Known inherited teleport-rejection stale-position race; fix would need a new revision. Full-game camera, physics, touch, popup and multiplayer acceptance outstanding.
- [Verified source evidence](https://github.com/BAWES-Universe/universe-maps/blob/f6c4ec62a2023e6f321a63b7db0269ffa0e60822/archive/source-recovery-2026-10-13/reconstructed/keeper-r2-editable-reconstruction/source/controller.js)

#### Lighthouse: The Last Signal · r2

Choose a quiet visit or optional shore signal; walk to three brass floor rings, capture the LOW/MIDDLE/HIGH notes, return to the lighthouse and transmit the sequence. Captured rings turn mint; success adds a warm beacon glow.

- Runtime status: Unpublished candidate; no verified game-room URL.
- Exact PR relationship: [explicit source contract](https://github.com/BAWES-Universe/workadventure-universe/pull/712): Uses native playAudio controls and unload semantics. [explicit source contract and runtime use](https://github.com/BAWES-Universe/workadventure-universe/pull/727): signal.js sets nativeSoundscape descriptor and an exact-zero silent playAudio carrier for one distance-attenuated ambience emitter. [explicit source contract and native fixture pin](https://github.com/BAWES-Universe/workadventure-universe/pull/799): Native floor click/tap movement plus show/hide ring layers; README pins source-native routes to merge 60e7afdc3f96ef32525597cd46bd41175d61a2ef. [production source baseline](https://github.com/BAWES-Universe/workadventure-universe/pull/800): README pins universe to merge 42ba35bd6eefeb4f74359114904d167cbaecf1ad; branch still has that SHA at research time. [no new map api dependency](https://github.com/BAWES-Universe/workadventure-universe/pull/842): No new camera API is used; latest zoom-resize fix is a separate engine change.
- Remaining limit: Needs approved isolated QA room with full runtime assets and supported engine. Source fixtures passed historically; real popup/mobile/audio/multiplayer acceptance not established.
- [Verified source evidence](https://github.com/BAWES-Universe/universe-maps/blob/f6c4ec62a2023e6f321a63b7db0269ffa0e60822/archive/source-recovery-2026-10-13/baselines/lighthouse-last-signal-r2-source/README.md)

#### Timber Studio · continuous-floor r8 retained runtime; reconstructed editable source

Walk through the repaired studio floor and instructor/participant positions. Companion WAM configures an instructor megaphone zone and a linked participant listener zone.

- Runtime status: Retained runtime and rebuilt source; no verified current game-room URL.
- Exact PR relationship: [diagnostic fixture not included fix](https://github.com/BAWES-Universe/workadventure-universe/pull/842): Studio r8 was used in rendering/zoom investigation. #842 changes the engine resize/scene-camera behavior, not these map bytes, source-art resolution or tile-edge rendering. [general platform candidate not map dependency](https://github.com/BAWES-Universe/workadventure-universe/pull/815): No source evidence binds this map to the open v0.3.5 release.
- Remaining limit: Latest original source archive missing; reconstruction preserves runtime. Pixelation/black-edge concerns unresolved. Full-game body/depth/touch/AV acceptance unverified.
- [Verified source evidence](https://github.com/BAWES-Universe/universe-maps/blob/f6c4ec62a2023e6f321a63b7db0269ffa0e60822/archive/source-recovery-2026-10-13/reconstructed/studio-reading-editable-reconstruction/source/studio/areas.wam.json)

#### Reading Conservatory · crossaisle repair r4 retained runtime; reconstructed editable source

Walk the newly cleared crossaisle above the reading groups and use west reading, east reading and mentorship conversation areas when the WAM is imported.

- Runtime status: Unpublished r4 candidate; no verified current game-room URL.
- Exact PR relationship: [diagnostic fixture not included fix](https://github.com/BAWES-Universe/workadventure-universe/pull/842): Reading r4 was a rendering investigation fixture, not a deployment of the zoom-resize fix. The fix does not cure source-art pixelation or thin tile lines. [general platform candidate not map dependency](https://github.com/BAWES-Universe/workadventure-universe/pull/815): No source evidence binds this map to the open v0.3.5 release.
- Remaining limit: Original r4 source archive missing; reconstructed source preserves runtime. Rendering complaints remain open. Media areas and live body/device acceptance unverified.

#### Resonance Media House · r7c survives; r9 unavailable

Explore the media-house garden court and editor, voice, screen and music areas. Those four areas are setup placeholders, with empty property arrays in the surviving WAM.

- Runtime status: r7c restored locally; no verified current game-room URL. r9 cannot be offered as restored.
- Exact PR relationship: [relevant engine fix not verified deployment](https://github.com/BAWES-Universe/workadventure-universe/pull/736): Surviving runtime has a silent-spawn-only layer; #736 fixes initial room-join silence. [no map specific dependency established](https://github.com/BAWES-Universe/workadventure-universe/pull/842): No camera script or feature-specific engine pin found.
- Remaining limit: r9 visual repairs missing. Live playtest and service configuration pending.
- [Verified source evidence](https://github.com/BAWES-Universe/universe-maps/blob/f6c4ec62a2023e6f321a63b7db0269ffa0e60822/archive/source-recovery-2026-10-13/reconstructed/media-house-editable-reconstruction/README.md)

#### Olive Arabic Academy · live-repair r6 preserved package

Walk the classroom and woven lounges; the companion WAM defines a teacher megaphone, linked classroom audience and two LiveKit meeting lounges.

- Runtime status: This is the preserved archive revision, separate from the newer retained hosted repair in [Hosted test builds](hosted.md). No game-room URL is asserted.
- Exact PR relationship: [relevant engine fix not verified deployment](https://github.com/BAWES-Universe/workadventure-universe/pull/736): Runtime has spawn-only-silence layer.
- Remaining limit: A hosted TMJ alone does not import WAM or establish a playable configured room.

#### Lantern Souk Bazaar · fountain-motion r6 preserved package

Explore the bazaar and watch the fountain surface, falling streams and ripples animate: 26 native 32px animated cells, eight frames, 1.12-second loop.

- Runtime status: This is the preserved archive revision, separate from the newer retained hosted repair in [Hosted test builds](hosted.md). No game-room URL is asserted.
- Exact PR relationship: [relevant engine fix not verified deployment](https://github.com/BAWES-Universe/workadventure-universe/pull/736): Runtime has silent-spawn-only layer. [not used](https://github.com/BAWES-Universe/workadventure-universe/pull/727): No map audio descriptor; README states animation needs no script or engine change.
- Remaining limit: Exact r6 revision must be verified; internal filename still says r5. No live browser/device/multiplayer acceptance.

#### Inventor’s Workshop · r2 preserved source/runtime

Walk the creation pads, outdoor test court and courtyard workbench. The companion WAM configures one indoor LiveKit collaboration area; other pads are empty setup zones.

- Runtime status: This is the preserved archive revision, separate from the newer retained hosted repair in [Hosted test builds](hosted.md). No game-room URL is asserted.
- Exact PR relationship: [relevant engine fix not verified deployment](https://github.com/BAWES-Universe/workadventure-universe/pull/736): Runtime has spawn-only-silence layer.
- Remaining limit: A hosted TMJ is not a configured game-room URL; WAM import and live AV/device testing still required.

#### Butterfly Town · v2 integrated review candidate

Explore the animated gate/town scenery, terrace cascades and fountain. Native nearby fountain/cascade audio exists in the source but **is OFF**: `town.js` line 6 sets `ENABLE_NATIVE_AUDIO = false`, and line 4 requires a compatible deployed [PR #712](https://github.com/BAWES-Universe/workadventure-universe/pull/712) build before activation.

- #712 is merged, but the deployed frontend version, device/listening acceptance and explicit activation have not been established. This retained runtime is not a working native-audio demo.
- The supplied native-component QA is pinned to superseded #712 head `93939afff9862c5bf43876288cd5d5bd692b277c`; do not count it as acceptance of final merged head `8380a80f60f3427807257cdaaabd1b11580dadbf`.
- Exact checked source: `Butterfly-Town-v2/candidate/public/butterfly-town/v2/scripts/town.js`, with hashed provenance in the JSON. No current playable-room URL was verified in this research.

### Fresh PR state

| Repository / PR | Current state | Exact head SHA | Meaning for this register |
|---|---|---|---|
| [engine #712](https://github.com/BAWES-Universe/workadventure-universe/pull/712) | Merged 2026-10-09T00:50:44Z | `8380a80f60f3427807257cdaaabd1b11580dadbf` | Native audio controls used by Last Signal. |
| [engine #727](https://github.com/BAWES-Universe/workadventure-universe/pull/727) | Merged 2026-10-10T14:16:47Z | `7f67e56f79816b490f309a83d446de52ba427a0e` | One distance-attenuated ambience emitter used by Last Signal; not used by silent Keeper or Souk animation. |
| [engine #736](https://github.com/BAWES-Universe/workadventure-universe/pull/736) | Merged 2026-10-10T19:58:26Z | `088f19b9c26cbe9968fc4d242765a83d87409cd3` | Initial silent-zone join fix relevant to silent-spawn map layers; deployment not established. |
| [engine #799](https://github.com/BAWES-Universe/workadventure-universe/pull/799) | Merged 2026-10-10T19:37:25Z | `f98f61010733cbc6238ecba747d2f16ff2cdc826` | Native32 click/tap destination preservation across layer changes; explicit Last Signal pin and relevant Keeper behavior. |
| [engine #800](https://github.com/BAWES-Universe/workadventure-universe/pull/800) | Merged 2026-10-10T22:44:28Z | `e04faa3d3a86af6b48227389f89ea4f5bf08f419` | Merged source-release baseline. Does not establish live deployment by itself. |
| [engine #815](https://github.com/BAWES-Universe/workadventure-universe/pull/815) | Open; unmerged | `49c07646b9974ed49131e5dc65bcbcf1eed3c14b` | Open v0.3.5 production-release candidate; source now includes #842; general platform improvements do not establish map-specific interaction dependencies. |
| [engine #842](https://github.com/BAWES-Universe/workadventure-universe/pull/842) | Merged 2026-10-13T12:07:42Z | `d86bbb3437d4d8613e7aef8ffeb3ef8df61c9844` | Merged zoom-resize/scene-camera fix, included in open #815 source. Studio/Reading are diagnostic assets, not proof that their runtime includes this patch. No source-art upscaling or tile-line rendering fix. |
| [maps #18](https://github.com/BAWES-Universe/universe-maps/pull/18) | Open; unmerged | `5c06a65b88c88a8758432a52f378513b49224a7b` | Older twelve-template and three ambient-variant source set; not the latest reconstructed candidates. |
| [maps #19](https://github.com/BAWES-Universe/universe-maps/pull/19) | Open draft; unmerged | `f6c4ec62a2023e6f321a63b7db0269ffa0e60822` | Backup/recovery source only, draft; not a map publication or engine deployment. |

### Corrections to older records

- Engine #842 is now merged as `09b61364b330edb1ece68020daca14c9d9ea2803` from head `d86bbb3437d4d8613e7aef8ffeb3ef8df61c9844`. Both the 12:04 open snapshot and older draft/head `44dda03…` record are superseded. Merged source is not deployment acceptance.
- Some merged PR descriptions quote superseded heads. The table uses returned `head_sha`, not those old body snippets.
- Source register naming historically called Studio r8 a Design Studio. Its actual WAM contains instructor/participant yoga-style megaphone areas; preserve that distinction when describing what the player can do.
- Media House r7c contains four empty setup areas. Do not promise editing, voice, screen or music services until they are configured. Missing r9 remains missing.
- Souk r6 uses existing native tile animation. Its internal TMJ filename still says r5; verify hashes before calling a hosted URL r6.

Evidence: [interactive-experiences.json](data/interactive-experiences.json) contains nine scoped runtime records and hashes for twenty-three inspected files. [github-pr-status.json](data/github-pr-status.json) contains fresh exact PR and branch metadata. No verified play URL was found or invented in this research.

### Zoom-resize, exit and reconnect acceptance after the release

1. Use a build proven to contain #842 merge 09b61364b330edb1ece68020daca14c9d9ea2803, and record the actual frontend version/SHA before testing.
2. Zoom out on a large map, open a website panel, then close it. Map should re-fit immediately, without new black margin space; the next small scroll or pinch should make only a small change.
3. While zoomed out, take an exit to another map. The new scene should start at the retained zoom and the next small scroll/pinch should not jump.
4. Reconnect/recreate the scene while zoomed out, then open/close a panel and resize again. Confirm the new camera owns resizing and the old scene camera cannot receive updates.
5. Repeat on portrait phone with pinch, rotate to landscape, and exercise browser-bar resize. Check ordinary zoom and player-follow behavior remain intact.
6. Record actual game/device results separately from source tests. Source-art pixelation and thin tile lines are outside #842 scope.

[Verified source ancestry](https://github.com/BAWES-Universe/workadventure-universe/compare/09b61364b330edb1ece68020daca14c9d9ea2803...49c07646b9974ed49131e5dc65bcbcf1eed3c14b). No merge, release or deployment was performed by this research.

## Next action to make these playable

Select the exact candidate and an approved isolated test room, serve its complete runtime subtree, import/configure the companion WAM and record the actual frontend commit. Validate the hosted assets and run the map-specific checklist before adding a game-session URL here. This register does not authorize a merge, deployment or publication. Runtime Git uploads remain explicitly pending until their remote receipt is verified.
