# Lantern Congress — safe room setup

## Activate native areas in a new, separate room

1. Create a separate room with the eventual versioned Custom TMJ URL, or use an authorized isolated map-storage import. This local package has not created a room or a live link.
2. Before editing an actual room, export/back up its WAM through a supported permitted route. Preserve its actual absolute mapUrl, entities, collections, areas, start points and unrelated settings.
3. In the room editor create each networking rectangle below, choose **Add to this area → Video call** (detail heading **Meeting Room**) and assign its distinct room name. Identical names connect areas inside the same map room, so do not reuse one name accidentally.
4. If Podium/Stage and Audience controls are visible, create each talk pair and select the actual newly created podium in that hall's Audience dropdown. The link is to the podium area ID, not its label. Never link Forum or Lab to Summit.
5. Do not add broad silence. The TMJ already owns the eight-cell quiet arrival. All ordinary circulation and casual pairs are otherwise eligible for native proximity, subject to successful role/status, permissions and participant settings.
6. Verify saved geometry/IDs in the actual WAM, then perform the live acceptance checklist. Do not overwrite the real room's absolute mapUrl with the portable companion's relative path.

Default audio/video mute options in the companion are false: they do not force devices off, turn devices on, or bypass permission/user choices. Native meeting spaces begin through existing WebRTC behavior and may transition to LiveKit when configured/needed. This map does not create or require a separate paid media service.

## Exact authored rectangles

Coordinates are native pixels. WAM uses player (x, y + 16) and inclusive far edges. The meeting rectangles mark the inner lounge floor, excluding divider/threshold trim; all four intended seat feet are inside each one.

| Area | x | y | width | height | Link or room name |
|---|---:|---:|---:|---:|---|
| Summit Podium | 192 | 320 | 1023 | 127 | lantern-summit |
| Summit Audience | 160 | 448 | 1087 | 383 | lantern-summit-podium |
| Forum Podium | 1664 | 320 | 1023 | 95 | lantern-forum |
| Forum Audience | 1632 | 432 | 1087 | 335 | lantern-forum-podium |
| Lab Podium | 1664 | 1344 | 1023 | 95 | lantern-lab |
| Lab Audience | 1632 | 1456 | 1087 | 383 | lantern-lab-podium |
| Congress Lounge 1 | 224 | 1312 | 319 | 223 | congress-lounge-1 |
| Congress Lounge 2 | 736 | 1312 | 319 | 223 | congress-lounge-2 |

Three Podium/Audience pairs and two Video call rooms are authored candidates. Successful joined speaker/listener/meeting status suppresses ordinary proximity. This schema/geometry does not prove media joins, isolation between live participants or failure/reconnection behavior.

Stage/Audience editor controls require FEATURE_FLAG_BROADCAST_AREAS, whose inspected source default is false. The actual deployment setting and editing permissions are unverified. If absent, stop that setup step and ask the authorized administrator for a supported route. Do not change settings or bypass an access restriction. The Video call option is not gated by that broadcast flag.

## Arrival and circulation

Tiled start rectangle: x 1408, y 1888, width 64, height 32. The actual native random start applies a 16px margin. The sole transparent noncolliding silent tile layer covers x 1376, y 1856, width 128, height 64, exactly eight 32px cells. WAM contains no duplicate default start or silence. An existing room may have a separate stored start; reconcile it rather than blindly overwriting it. Tile-layer silence uses player x/y without the 16px feet offset.

Three casual pairs rest 56px apart, below the source default 64px proximity-start threshold. Furniture and room walls do not guarantee private audio isolation; deployment overrides and participant settings may differ. Group bays have low three-sided dividers and front wings to stop automatic through-shortcuts, while every intended seat remains reachable.

Summit and Forum secondary exits enter rear aisles outside their audience rectangles. This prevents unrelated tested click journeys from briefly joining a talk on the way to another destination. Individual users can still deliberately enter any open talk room.

The stages use walkable single-level floor and shallow tread artwork. No true multilevel physics or automatic sitting is implemented. Stair endcaps were cropped away so no visible solid-looking post has a walk-through body footprint. Coffee and registration have a defined service front, staff entry/return and customer approach. The espresso machine occupies one explicit native cell on the counter's right section. No purchasing interaction is configured.

## Custom TMJ and reset warning

The inspected admin Custom TMJ flow creates a separate room-specific WAM with empty areas/entities when storage is available. It does not discover or import the neighboring conference.wam. Native map collision, silence and focus work as TMJ content; communication areas require actual room setup.

Pinned admin source:
- [Room creation](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/admin/rooms/route.ts#L390-L399)
- [WAM resolution](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/map/route.ts#L186-L265)
- [Empty WAM creation](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/lib/map-storage.ts#L152-L200)

Explicitly sending mapUrl in the inspected room update handler can regenerate/reset stored WAM configuration even when the URL value is unchanged. [Reset handler](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/admin/rooms/%5Bid%5D/route.ts#L503-L540).

ZIP import is a replacement route, not a safe append-only area merge. It can replace destination files and supplied WAMs. Never upload this package blindly into a live room/root directory. Download/back up the exact isolated destination and preserve unrelated data first. [Replacement source](https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/map-storage/src/Upload/UploadController.ts#L199-L224).

## Focus and live acceptance

Each hall has its own native focusable area with zoomMargin 0.15. The full stage, speaker, audience and rear exit fit on fresh desktop 1440×900, portrait 390×844 and landscape 844×390 entry at DPR 1/2/3 in source-executed camera math. Portrait whole-room fit produces approximately 9.4 CSS-pixel avatars; native manual zoom remains available. Existing focus rotation/resize does not fully pass. Leaving/re-entering recalculates the initial fit. No script repeatedly reapplies zoom or changes collisions/layers.

Required live checks after authorized setup:
- Fresh spawn lands safely inside quiet arrival; keyboard/tap movement and chair/stair/door access work.
- Each hall's presenter reaches only its intended audience; simultaneous other halls stay independent.
- Two participants in each lounge communicate across the whole intended inner rectangle; other lounges remain separate.
- Casual pairs can form bubbles; leaving a meeting returns to ordinary eligibility.
- Permissions, mute/video state, reconnection and failed joins behave as expected.
- Local/remote avatar depth, initial camera fit, manual zoom and portrait/rotation are checked on actual clients.
- Capacity is load-tested separately; 110 drawn/resting seats do not establish concurrency.

Local proofs use source pin 60e7afdc3f96ef32525597cd46bd41175d61a2ef, including the merged native32 replan fix. Public dev served that build when verified earlier in this work, but this package has no authenticated live room/session validation. No browser renderer, phone, network-media or multi-user acceptance is claimed.
