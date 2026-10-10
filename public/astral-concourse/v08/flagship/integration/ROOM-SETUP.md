# Flagship garden B (v08): room setup and acceptance

Garden/coffee variation: coherent exterior materials, purposeful pavilion tables and restrained native leaf animation, retaining corrected reception/chairs, spawn-only silence and native whole-hall focus. The 210 auditorium chairs and 28 social resting places are artwork/geometry counts, not concurrent-capacity claims. This package creates no actual room or media service.

## Safest activation: add areas in the actual room's native editor

1. Create a new, separate room using the versioned v08 Custom TMJ URL. Obtain its real Universe room/share URL. The original v01 remains a separate room option.
2. Open that room using the authorized map-editing account. Back up/export its actual WAM through a permitted supported route before editing. Preserve its absolute external map URL, entities, collections, existing areas, settings and start points.
3. For each lounge rug, create a rectangle using the table below. Choose **Add to this area → Video call**; its detail header is **Meeting Room**. Give each an independent room name exactly as below, or other distinct names. Matching names connect areas in the same map room.
4. Leave start-with-audio-muted and start-with-video-muted off unless you intentionally want those entry defaults; leave chat enabled. These choices do not turn devices on or override permission/user choices.
5. If Stage/Podium and Audience settings are visible, create the podium and audience areas below. Select the actual newly created podium in the audience's Stage dropdown. The link must refer to the podium **area ID**, not its display/broadcast name.
6. Keep all foyer/terrace conversation seating outside the audience and podium. Do not add broad foyer silence. The authored TMJ already contains one non-colliding transparent silent tile layer for the 128×128 spawn receiver only, deliberately outside every meeting area and casual pair.
7. Verify saved geometry and links in the actual room WAM, then perform the multi-participant checks below before calling any meeting/broadcast active. Keep the actual room's absolute `mapUrl`; do not copy the portable companion's relative map URL over it.

### Four native meeting rectangles

Coordinates are pixels on the native32 map. WAM rectangles include their far edge, so width/height are one pixel less than the corresponding exclusive artwork bounds.

| Rug | x | y | width | height | Independent room name |
|---|---:|---:|---:|---:|---|
| Lounge01, upper-left | 96 | 1072 | 351 | 223 | astral-flagship-v08-lounge-01 |
| Lounge02, upper-middle | 640 | 1072 | 223 | 223 | astral-flagship-v08-lounge-02 |
| Lounge03, upper-right | 1120 | 1072 | 319 | 223 | astral-flagship-v08-lounge-03 |
| Lounge04, lower-left | 96 | 1456 | 351 | 223 | astral-flagship-v08-lounge-04 |

The companion uses `livekitRoomProperty`, the existing native Video call property. Despite that API name, native spaces initially use WebRTC and may transition to LiveKit if configured and needed. This package does not require or create a separate paid service. Entry joins the shared named area space; it does not depend on the distance between occupants within that square. Successful meeting status excludes ordinary proximity bubbles. Join/leave are asynchronous and deployment/media behavior remains untested.

### Auditorium areas

- Podium: x256, y208, width1024, height128. Companion area ID `astral-flagship-v08-podium`; broadcast name `astral-flagship-v08-stage`; chat disabled.
- Audience: x128, y384, width1280, height623. Link to the actual podium area ID; chat disabled. All 210 authored seat feet are inside this audience.
- Default arrival: x736, y1792, width64, height64. The TMJ and portable WAM agree. For an existing room, reconcile its start area rather than blindly duplicating/replacing it.

Stage/Audience editor controls require `FEATURE_FLAG_BROADCAST_AREAS`. The inspected source default is false; the deployment's setting and account permissions are unverified. If the controls are absent, stop this part and ask the authorized administrator for the supported editor/import route. This guide does not authorize changing the flag, accessing credentials or bypassing an access restriction. The Video call meeting option is not gated by that broadcast flag.

## Casual seats and circulation

The six casual pairs deliberately have no WAM meeting, audience, podium or silent property covering them. Pavilion resting partners are48px apart; the other casual pairs are56px apart, beneath the source default proximity start distance64px. The source default group radius is48px. Deployment overrides, availability, media permissions and participants' choices remain applicable. Physical furniture/railings do not create private audio isolation.

The single native silent tile layer covers exactly 16 native32 cells at x704, y1760, width128, height128. The former 333-cell circulation silence is removed. All other ordinary circulation is eligible for proximity, subject to active role/status and participant settings. Native tile membership uses player x/y; WAM area membership uses player x/y+16. Do not replace the shaped route with one broad silent rectangle or overlap silence with meeting rugs: silent status takes priority and can mute a joined meeting.

The right doorway is continuous walkable floor on this same map. The north garden is now walkable along the paved route, with a Hall/Garden side door and a north gate from the coffee terrace. Its path terminates at an open-center shaded pergola with two additional casual pairs. Lawn and planting beyond the paving remain scenery. Interior roofs and camera/visibility scripts are omitted. A native focusable map area frames the whole hall on entry and restores following on exit; it does not change collision or layers. This option does not require PR799 to perform ordinary movement or native camera focus. No exterior room link, purchase interaction or background music is configured. The coffee counter is a solid visual service counter with a clear customer approach.

## Custom TMJ does not import the companion WAM

The inspected admin flow saves the external TMJ URL and creates a separate room-specific WAM with empty areas/entities when map storage is available. It does not discover the adjacent portable `grand-auditorium.wam`. Without map storage initialization it falls back to the TMJ alone. The native silent spawn receiver and camera focus remain map content, but authored meeting/podium/audience areas require actual room setup.

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
- Check native local and remote avatar depth, chair approaches, every stage stair, collision around the coffee counter and the garden doors, paved path, pavilion posts/chairs and planted perimeter.
- Test realistic multi-user load independently. Seat counts do not establish supported concurrent users.

Current area/schema/quiet behavior was checked against merged engine `60e7afdc3f96ef32525597cd46bd41175d61a2ef` and matched the earlier `90a148c03e03401e26d236eaac9bea4123b42c57` contract; this is not a claim that the deployment matches either head. [Meeting editor option](https://github.com/BAWES-Universe/workadventure-universe/blob/60e7afdc3f96ef32525597cd46bd41175d61a2ef/play/src/front/Components/MapEditor/EditMode/areaProperties.ts), [native area handlers](https://github.com/BAWES-Universe/workadventure-universe/blob/60e7afdc3f96ef32525597cd46bd41175d61a2ef/play/src/front/Phaser/Game/MapEditor/AreasPropertiesListener.ts), [WAM schema](https://github.com/BAWES-Universe/workadventure-universe/blob/60e7afdc3f96ef32525597cd46bd41175d61a2ef/libs/map-editor/src/types.ts).

## Garden anchors and boundaries

Hall-side opening: x1408–1567, y448–543. Terrace north opening: x2144–2271, y1024–1087. Pavilion paving: x1920–2399, y64–383; four solid posts, four north-facing lounge chairs and two low tables have explicit32px collision cells. Outdoor resting pairs are (2040,231)/(2088,231) and (2264,231)/(2312,231), each48px apart. A128px central passage remains clear. Tables are at x2048/y160/64×32 and x2240/y160/64×32 in collision geometry. They remain outside all authored WAM communication roles and the quiet route. These are resting art anchors, not an automated native sit action.

Paving controls where avatars can walk; the garden is not a second physics height. The open pergola, column faces and cast shadows are visual depth. The map uses a single permanent collision layer and no script. Entering/leaving the hall changes native camera framing only; layer visibility remains unchanged.

## Unpatched native pointer limit

The current game source has an independent same-cell fallback: clicking within the tile already occupied can settle in a neighbouring tile. This occurs without map scripts and is documented in [issue798](https://github.com/BAWES-Universe/workadventure-universe/issues/798). [PR799](https://github.com/BAWES-Universe/workadventure-universe/pull/799) was merged into universe-develop at `60e7afdc3f96ef32525597cd46bd41175d61a2ef`; the public dev gameplay build was verified as universe-develop@60e7afd on2026-10-10 at20:04 UTC. The B replay passes all11,818 commands on that merged source, with the native animation plugin ticking in parallel. This is not a live-device test or evidence that every other deployment uses that build. On an older unpatched deployment, the known same-cell issue can remain; animation support itself predates PR799.

## Whole-hall camera focus and its limits

The native TMJ area is x0, y0, width1536, height1008, `focusable:true`, `zoomMargin:0.15`. This uses the same native focus mechanism as the Conference Campus reference, without its decorative hide/show scripts. The podium, speakers, audience and tested exit landings fit on fresh entry in source-executed portrait390×844, landscape844×390 and desktop1440×900 camera cases at DPR1/3. Native manual zoom remains available. Fitting this entire hall on portrait produces approximately7px-high avatar frames; users can zoom in for detail.

A known existing camera-resize limitation remains: rotating/resizing while focused can lose the entry padding or retain stale zoom. Initial-entry fit is tested separately from rotation, which does not fully pass. Leaving and re-entering the focus area recalculates the fit. No reapplying script fights manual zoom. Camera math and map source were tested offline; no live rendering, browser interaction or device-session acceptance is claimed.

## Reception and corrected casual furniture

The reception counter uses a new proportionate192×51 asset with a readable RECEPTION marker. Its solid footprint is x960, y1568, width192, height32, without the old invisible north padding. The staff/customer anchors are (1048,1551) and (1048,1600), with a64px side return and96px customer apron. It is ordinary proximity space, not a configured meeting or purchasing interaction. Twelve casual seats reuse the accepted north-facing chair artwork at native scale. Four close low tables serve the indoor/terrace pairs; two more low tables now serve the pavilion pairs, with a clear central approach. No rejected tall stool/table assembly returns.

The middle lounge keeps its original chairs, table, rug and meeting bounds. Low side dividers move outward32px for64px lateral clearance. The north cap is composed at native scale and overlaps only the top16px of the artwork rectangle; no chair pixels are replaced. Native route checks confirm the single entrance does not create a through-shortcut.

## Native garden animation

Three blocked-planting placements use a four-frame32px tile animation at350/450/350/650ms. The layer sits below avatars and carries no collision, silence, media, script or other behavioral properties. Frame changes update only render indices. Native Disable animations pauses the effect; every frame is complete on its own. No background music, audio service or paid dependency is added.

Verify in the actual room that animation is restrained, the pause setting works, garden paths/doorways remain clear, all four pavilion chairs can be reached and exited, and media behavior remains unchanged. Source fixtures do not establish mobile performance or visual rendering on a real device.
