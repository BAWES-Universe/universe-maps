# Flagship v05: room setup and acceptance

Roofless Garden, the requested roofless option. The 210 auditorium chairs and 28 social resting places are artwork/geometry counts, not concurrent-capacity claims. This package creates no actual room or media service.

## Safest activation: add areas in the actual room's native editor

1. Create a new, separate room using the versioned v05 Custom TMJ URL. Obtain its real Universe room/share URL. The original v01 remains a separate room option.
2. Open that room using the authorized map-editing account. Back up/export its actual WAM through a permitted supported route before editing. Preserve its absolute external map URL, entities, collections, existing areas, settings and start points.
3. For each lounge rug, create a rectangle using the table below. Choose **Add to this area → Video call**; its detail header is **Meeting Room**. Give each an independent room name exactly as below, or other distinct names. Matching names connect areas in the same map room.
4. Leave start-with-audio-muted and start-with-video-muted off unless you intentionally want those entry defaults; leave chat enabled. These choices do not turn devices on or override permission/user choices.
5. If Stage/Podium and Audience settings are visible, create the podium and audience areas below. Select the actual newly created podium in the audience's Stage dropdown. The link must refer to the podium **area ID**, not its display/broadcast name.
6. Keep all foyer/terrace conversation seating outside the audience and podium. Do not add broad foyer silence. The authored TMJ already contains one non-colliding transparent silent tile layer for spawn/main circulation, deliberately outside every meeting area and casual pair.
7. Verify saved geometry and links in the actual room WAM, then perform the multi-participant checks below before calling any meeting/broadcast active. Keep the actual room's absolute `mapUrl`; do not copy the portable companion's relative map URL over it.

### Four native meeting rectangles

Coordinates are pixels on the native32 map. WAM rectangles include their far edge, so width/height are one pixel less than the corresponding exclusive artwork bounds.

| Rug | x | y | width | height | Independent room name |
|---|---:|---:|---:|---:|---|
| Lounge01, upper-left | 96 | 1072 | 351 | 223 | astral-flagship-v05-lounge-01 |
| Lounge02, upper-middle | 640 | 1072 | 223 | 223 | astral-flagship-v05-lounge-02 |
| Lounge03, upper-right | 1120 | 1072 | 319 | 223 | astral-flagship-v05-lounge-03 |
| Lounge04, lower-left | 96 | 1456 | 351 | 223 | astral-flagship-v05-lounge-04 |

The companion uses `livekitRoomProperty`, the existing native Video call property. Despite that API name, native spaces initially use WebRTC and may transition to LiveKit if configured and needed. This package does not require or create a separate paid service. Entry joins the shared named area space; it does not depend on the distance between occupants within that square. Successful meeting status excludes ordinary proximity bubbles. Join/leave are asynchronous and deployment/media behavior remains untested.

### Auditorium areas

- Podium: x256, y208, width1024, height128. Companion area ID `astral-flagship-v05-podium`; broadcast name `astral-flagship-v05-stage`; chat disabled.
- Audience: x128, y384, width1280, height623. Link to the actual podium area ID; chat disabled. All 210 authored seat feet are inside this audience.
- Default arrival: x736, y1792, width64, height64. The TMJ and portable WAM agree. For an existing room, reconcile its start area rather than blindly duplicating/replacing it.

Stage/Audience editor controls require `FEATURE_FLAG_BROADCAST_AREAS`. The inspected source default is false; the deployment's setting and account permissions are unverified. If the controls are absent, stop this part and ask the authorized administrator for the supported editor/import route. This guide does not authorize changing the flag, accessing credentials or bypassing an access restriction. The Video call meeting option is not gated by that broadcast flag.

## Casual seats and circulation

The six casual pairs deliberately have no WAM meeting, audience, podium or silent property covering them. Resting partners are56px apart, beneath the source default proximity start distance64px. The source default group radius is48px. Deployment overrides, availability, media permissions and participants' choices remain applicable. Physical furniture/railings do not create private audio isolation.

The single native silent tile layer covers the main arrival spine, hall approach branches and the cross-concourse to the terrace. Native tile membership uses player x/y; WAM area membership uses player x/y+16. Do not replace the shaped route with one broad silent rectangle or overlap silence with meeting rugs: silent status takes priority and can mute a joined meeting.

The right doorway is continuous walkable floor on this same map. The north garden is now walkable along the paved route, with a Hall/Garden side door and a north gate from the coffee terrace. Its path terminates at an open-center shaded pergola with two additional casual pairs. Lawn and planting beyond the paving remain scenery. Interior roofs and all camera/visibility scripts are omitted, so this option does not depend on issue798 or an unreleased engine patch. No exterior room link, purchase interaction or background music is configured. The coffee counter is a solid visual service counter with a clear customer approach.

## Custom TMJ does not import the companion WAM

The inspected admin flow saves the external TMJ URL and creates a separate room-specific WAM with empty areas/entities when map storage is available. It does not discover the adjacent portable `grand-auditorium.wam`. Without map storage initialization it falls back to the TMJ alone. The native silent TMJ path remains map content, but authored meeting/podium/audience areas require actual room setup.

Sources, pinned to admin develop inspection `e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1`:
- [Room creation](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/admin/rooms/route.ts#L390-L399)
- [Room WAM resolution](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/map/route.ts#L186-L265)
- [Empty WAM construction](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/lib/map-storage.ts#L152-L200)

## Important warning: map URL updates and replacement imports

The inspected admin update handler regenerates the WAM whenever an explicit `mapUrl` field is supplied, even if the value is unchanged. This can reset areas and entities. Back up and reconcile the actual room WAM before any source change; preserve the existing configuration and verify it afterward. [Reset handler](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/admin/rooms/%5Bid%5D/route.ts#L503-L540).

Map storage also has a separate ZIP download/upload UI. Upload replaces destination-directory contents and overwrites supplied WAM files. Never upload this standalone package blindly into a live room or root directory. It is not a safe append-only area import. Download and back up the exact isolated destination and reconcile all unrelated files/fields first, through an authorized supported interface.

An existing authenticated WAM JSON Patch route validates/migrates before saving. Any such merge must start with the actual room WAM obtained through an allowed route, detect drift with a test operation, preserve unrelated areas and resolve IDs. This source capability is not evidence that the UI/API is reachable, nor permission to bypass the current access restriction.

Historical inspected import source: [ZIP UI](https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/map-storage/src-ui/App.svelte), [replacement behavior](https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/map-storage/src/Upload/UploadController.ts#L199-L224), [validated PATCH](https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/map-storage/src/Upload/UploadController.ts#L406-L478).

## Required live acceptance

- Fresh entry lands in the intended quiet receiver; test keyboard and click movement.
- Two or more participants join one lounge, communicate while at opposite seats, leave/re-enter, and retain expected mute/camera behavior.
- Simultaneous different lounges do not share media. Do not infer this solely from distinct names.
- Casual partners can form an ordinary bubble; leaving a lounge restores normal eligibility. Test transitions and failure/reconnection conditions.
- Presenter/listener roles operate correctly, ordinary proximity is suppressed while those roles are successfully joined, and separate rooms/halls do not leak audio.
- Check native local and remote avatar depth, chair approaches, every stage stair, collision around the coffee counter and the garden doors, paved path, pavilion posts/tables and planted perimeter.
- Test realistic multi-user load independently. Seat counts do not establish supported concurrent users.

Current source behavior was checked against engine `b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af`; this is not a claim that the deployment matches that head. [Meeting editor option](https://github.com/BAWES-Universe/workadventure-universe/blob/b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af/play/src/front/Components/MapEditor/EditMode/areaProperties.ts), [native area handlers](https://github.com/BAWES-Universe/workadventure-universe/blob/b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af/play/src/front/Phaser/Game/MapEditor/AreasPropertiesListener.ts), [WAM schema](https://github.com/BAWES-Universe/workadventure-universe/blob/b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af/libs/map-editor/src/types.ts).

## Garden anchors and boundaries

Hall-side opening: x1408–1567, y448–543. Terrace north opening: x2144–2271, y1024–1087. Pavilion paving: x1920–2399, y64–383; four solid posts, two tables and four stool bases have explicit32px collision cells. Outdoor resting pairs are (2036,224)/(2092,224) and (2260,224)/(2316,224), each56px apart. They remain outside all authored WAM communication roles and the quiet route. These are resting art anchors, not an automated native sit action.

Paving controls where avatars can walk; the garden is not a second physics height. The open pergola, column faces and cast shadows are visual depth. The map uses a single permanent collision layer and no script. Entering/leaving the hall does not change zoom or layer visibility in this roofless option.

## Unpatched native pointer limit

The current game source has an independent same-cell fallback: clicking within the tile already occupied can settle in a neighbouring tile. This occurs without map scripts and is documented in [issue798](https://github.com/BAWES-Universe/workadventure-universe/issues/798). The proposed [PR799](https://github.com/BAWES-Universe/workadventure-universe/pull/799) was opened separately; it is not a runtime dependency of this roofless map and must not be treated as deployed. Normal movement regression results and explicitly classified same-cell probes are recorded separately.
