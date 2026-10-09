# Campus 06 native meeting-room companion

This is an offline companion WAM draft for the connected campus. Nothing has been uploaded, registered, or changed in a live room. The three rooms use the current fork's native `livekitRoomProperty`; there is no external call website or map-script replacement.

The source audit is pinned to `6accae707e5a26bc56231ef241c64b397a5cea70`. The JSON Schema and original Zod schema declarations both accept the draft. Revision03 as-built geometry is confirmed and applied. Local checks passed against the compiled 3840×3456 native map: all 14 seats, room arrivals, public-gallery exclusion, relative TMJ binding, and both blank gate room-URL fields. `validation-report.json` and `final-validation-summary.json` identify the exact checked files. **The actual deployment and room registration still need separate verification.** Revalidate if the geometry or compiled map changes.

## What is configured

| Room | Area ID and native room name | World rectangle x, y, width, height | Physical seats |
|---|---|---|---|
| Meeting A | campus06-office-meeting-a | 1904, 1072, 272, 272 | 4 |
| Meeting B | campus06-office-meeting-b | 2224, 1072, 256, 272 | 4 |
| Conference | campus06-office-conference | 2528, 1072, 320, 272 | 6 |

These rectangles are the final as-built Revision03 interior geometry plus office origin `(800,448)`, with no scaling and no extra offset. `geometry-contract.json` records the source fingerprint and confirmed bounds. The office envelope is `(800,448,2112,1088)`. The public gallery is `(864,1424,1984,64)` and is outside all three meeting areas.

The native detector tests `(avatar.x, avatar.y + 16)` using inclusive rectangle edges. For final bounds, the southernmost in-area avatar anchor is world Y=1328; Y=1329 is outside. The door threshold anchor at world Y=1368 is outside and the interior public-arrival anchor at Y=1328 is inside, exactly on the inclusive edge. The arrivals intentionally enter their room's native conversation area. This boundary covers every seated avatar and stops before the gallery. It does not redefine collision geometry.

Each room has a different native room name. Entry joins that room's shared media/chat space with `ALL_USERS`; leaving exits it. Distances between chairs do not determine who participates in this meeting space. Physical chair counts are not a tested connection-capacity promise. The 64 px capture / 48 px centroid rules for ordinary proximity bubbles do not establish these room calls.

The draft uses the fork's normal defaults: `startWithAudioMuted=false`, `startWithVideoMuted=false`, `disableChat=false`. The entry handler does not force a user's disabled microphone/camera on; these values simply avoid forcibly muting an already active device. Browser media permissions and each participant's controls still apply.

The property is called `livekitRoomProperty`, but the backend initially selects WebRTC for media spaces and can switch to LiveKit according to participant count and availability. The source default threshold is four users. This draft does not force a transport or change the engine's media settings. Verify the actual deployed settings and LiveKit service before promising six-person operation.

## Ownership and rights

These are shared meeting areas for users admitted to the parent campus room. No private owner ID, personal-claim behavior, member tags, or admin identity has been invented. The schema does not require an owner for a normal meeting area. `ownerId` is required only if a separate `personalAreaPropertyData` is added; this draft does not add that property. Creating/updating areas through the editor requires the existing room's `canEdit` authorization; ordinary personal-area ownership is not enough for those area commands.

Map-storage upload authentication and room membership/editor authorization are separate prerequisites. No credentials are included. The server scopes native area spaces to the player's room, but this fork explicitly documents that member-only area enforcement within a room is browser-side. Do not describe geometry alone as a confidential-access boundary. No area-based security policy is claimed here.

## Files

- `native-meetings.wam`: portable local draft, version 2.0.0.
- `geometry-contract.json`: room rectangles, all 14 avatar anchors, public gallery and revision confirmation.
- `fork-wam-2.0.0.schema.json`: unchanged exported schema from the audited fork.
- `validation-report.json`, `source-schema-validation.json`: executed offline results and their limits.
- `final-validation-summary.json`: final artifact hashes and completed local checks.
- `source-audit.json`: exact source paths, line references and SHA-256 fingerprints.
- `stage-audience-plan.json`: source-supported optional plan only; no stage/audience areas are inserted into the WAM.
- `build_companion.py`, `validate_companion.py`, `verify_source_schema.cjs`, `bind_map_url.py`: local generation/binding/checks. They do not upload or register anything.

## Finish the local package

Revision03 is confirmed at `../sources/office-geometry/source-coordinate-geometry.json`, copied from the office's `03-as-built-registration` contract. To reproduce, run from this directory:

```sh
python build_companion.py --geometry ../sources/office-geometry/source-coordinate-geometry.json --geometry-revision 03-as-built-registration --geometry-final
python validate_companion.py --geometry ../sources/office-geometry/source-coordinate-geometry.json --require-final --require-map
node verify_source_schema.cjs /path/to/fork-checkout
```

The Python validator needs `jsonschema`. The source-schema validator needs existing `typescript` and Zod 3 packages; it transpiles the original schema declarations through `WAMFileFormat`, excluding an unrelated enum import. This is a narrow schema check, not a full frontend/backend build. In the preparation environment these were available through `NODE_PATH=/workspace/shared/universe-audio-fix/node_modules` (TypeScript 5.8.3, Zod 3.25.76). No dependency installation or engine modification was needed.

`native-meetings.wam` contains `mapUrl: "../map16/magical-campus.tmj"`. The exact frontend resolves this with `new URL(wam.mapUrl, absoluteWamFileUrl)`. Therefore this layout is valid when both paths are hosted with their relationship preserved:

```text
<campus package>/companion-wam/native-meetings.wam
<campus package>/map16/magical-campus.tmj
<campus package>/<the TMJ's actual referenced assets>
```

If the WAM and map will live in different directories/hosts, use `bind_map_url.py --map-url '<confirmed public HTTPS TMJ URL>' --output native-meetings-bound.wam` to prepare a separate local bound draft. The placeholder is an instruction, not a real or registered URL. The utility does not verify the URL remotely and does not upload. Confirm the hosted TMJ and every referenced resource before deployment.

## Practical activation, once deployment is authorized

1. Obtain the actual target deployment, existing owner/editor authorization, unused WAM storage path, final map/asset URL, and chosen room's existing verified play URL. Preserve any existing room configuration and read its WAM first if integration is into an existing room. This companion is a full minimal WAM, so replacing an existing WAM blindly would discard that room's other areas/entities/settings. Merge the three uniquely named areas into an existing WAM only after reviewing conflicts; do not overwrite unrelated fields.
2. Publish the complete campus map and assets by the deployment's approved process. Either preserve the relative directory layout above or bind a copy to the confirmed public map URL. Hosting the `.wam` next to a TMJ does not activate it by itself.
3. The audited map-storage supports authenticated `PUT` to the selected new `.wam` path with the WAM as `application/json`, or multipart field `file`. It validates WAM content, stores it, refreshes it and updates its map list. Use the deployment's already-authorized authentication flow. The basic map-storage "Add a map" UI creates an empty WAM; it does not import this companion's three configured areas. If using the ZIP upload UI, use a new dedicated directory: the audited `/upload` path deletes other files in the selected directory. Uploading a TMJ can also generate an empty WAM automatically; choose the explicit `native-meetings.wam`, not that generated empty one.
4. Register/select the WAM through the target deployment's actual room-management process. For an Admin API deployment, the fork delegates `GET /map?playUri=...` to the configured Admin API's `GET /api/map`. The verified room must resolve to the new WAM URL. The creation/update interface for that external Admin API is not in this fork, so no guessed mutation endpoint or room URL is supplied here. For a deployment that truly uses `LocalAdmin` instead, the audited play-path pattern `/~/<verified storage-relative WAM path>` resolves against `PUBLIC_MAP_STORAGE_URL`; this is a route pattern, not evidence that a live room exists. The direct `/_/<instance>/<host>/<map>` route produces plain `mapUrl` and does not activate this companion.
5. Inspect the actual map-details response. It must have the intended `wamUrl` and no truthy plain `mapUrl`: the frontend prioritizes `mapUrl` when both are present. Then check that the returned WAM's relative `mapUrl` resolves to the final TMJ. The fork also expects universe/world/room structure in WAM storage paths for custom collections. Preserve the deployment's existing verified namespace; a local package filename does not establish namespace ownership.
6. Verify authorized users can load the WAM/TMJ/assets and the room's websocket/media services. LiveKit availability is provided either by Admin API capability `api/livekit/credentials` version `v1` or the configured `LIVEKIT_HOST`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`. Credentials remain server-side and are not part of a WAM. Check availability without disclosing or embedding secrets.
7. Run the runtime acceptance checks below in the authorized test room. Only then report which behaviors are working. Registration, startup and multiplayer operation have not been performed for this draft.

## Runtime acceptance still required

Use two independent authenticated or permitted guest browser sessions, each with its own identity. Confirm both loaded the same verified play room and exact WAM revision.

- Walk into Meeting A from the gallery and sit at separated chairs. Confirm the named native meeting row/participants, bidirectional microphone/audio, camera as allowed, and one sent chat message each. Then leave via the door: the departing session must leave the call and stop receiving that room's media.
- Put one session in A and one in B; confirm the rooms remain separate. Repeat in Conference, including quick leave/re-entry and a reconnect. Test every seated anchor and all door boundaries without changing geometry.
- Keep one session in a meeting and the other in the public gallery; the gallery session must not enter that meeting. Repeat after crossing between rooms.
- If four/six simultaneous users are required, test those actual counts and the transport transition on the deployment. A two-user result does not prove six-user operation.

The fork has native meeting-area Playwright tests for two-user chat, reconnect, and rapid entry/exit. They were inspected as source, not executed here. No live two-user or broadcast evidence is claimed by any offline report.

## Source references at the pinned commit

- `libs/map-editor/src/types.ts:18-24,44-50,193-240,375-385`: IDs, LiveKit configuration, rectangle-area shape and WAM root schema.
- `libs/map-editor/src/Migrations/WamFileMigration.ts:16-45`: version 2.0.0 and schema parsing.
- `libs/map-editor/src/GameMap/GameMap.ts:43-50`: WAM supplies map-editor areas; a TMJ alone does not.
- `libs/map-editor/src/GameMap/GameMapAreas.ts:28,41-46,318-327`; `libs/math-utils/src/MathUtils.ts:8-13,29-30`: point offset and inclusive bounds.
- `play/src/front/Phaser/Game/MapEditor/AreasPropertiesListener.ts:237-242,875-946,1200-1229`: automatic native media/chat entry and leave.
- `libs/shared-utils/src/Space/areaSpaceName.ts:1-18`; `play/src/pusher/services/SpaceJoinPolicy.ts:8-19,39-51`: room-scoped native names and enforcement limits.
- `play/src/front/Phaser/Game/GameScene.ts:437-442,699-718,791-806`: WAM selection, relative map URL resolution and namespace parsing.
- `map-storage/src/Upload/UploadController.ts:195-221,254-264,330-391`; `map-storage/src/Services/Authentication.ts:40-136`: import and authentication.
- `play/src/pusher/controllers/MapController.ts:55-82`; `play/src/pusher/services/AdminApi.ts:218-246,295-303`; `play/src/pusher/services/AdminService.ts:1-5`; `play/src/pusher/services/LocalAdmin.ts:74-85,251-284`: resolution/registration contract and editor authorization.
- `libs/map-editor/src/types.ts:160-173`; `map-storage/src/MapStorageServer.ts:50-58,168-189`: optional rights/ownership and editor requirements.
- `back/src/Model/CommunicationManager.ts:31-46,94-99`; `back/src/Model/Policies/TransitionPolicy.ts:29-44`; `back/src/Model/Services/LivekitAvailabilityService.ts:1-23`; `back/src/Model/States/StateFactory.ts:47-71`; `back/src/Enum/EnvironmentVariableValidator.ts:155-161`: transport policy and configuration.
- `tests/tests/map_editor/map_editor_livekit.spec.ts:32-65,67-111,113-171`: existing source tests, not a result for this campus.
