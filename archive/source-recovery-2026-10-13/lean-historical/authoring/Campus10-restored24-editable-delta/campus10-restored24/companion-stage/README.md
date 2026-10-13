# Native stage and audience configuration

The corrected campus keeps 24 auditorium seats: two banks of three chairs across four rows. Dense event seating is intentional. This separate configuration uses the existing native podium/audience feature; it is not active merely because the TMJ calls the room an event hall.

## Existing room: safest setup

Use the in-game area editor without replacing the room's WAM file:

The Podium and Audience controls are shown only when FEATURE_FLAG_BROADCAST_AREAS is enabled. Its source default is false, and the deployed setting has not been verified. If these controls are absent, this editor procedure is not currently available in that deployment. No feature flag or application setting has been changed. The existing WAM schema and runtime handlers are separately present.

1. Create a podium area named Campus stage at world rectangle x=96, y=1760, width=448, height=112. Give its native podium property the broadcast name campus-stage.
2. Create an audience area named Campus audience at x=64, y=1888, width=512, height=384. Select the Campus stage podium as its speaker source.
3. Leave the room's unrelated areas, entities, collections, settings and global megaphone configuration intact. Do not add a whole-hall silent property as a substitute for broadcasting.
4. Test with a real speaker and listener. Confirm the speaker broadcasts, the audience receives the stage stream, entering these configured roles excludes ordinary proximity groups, and leaving restores normal behavior. Also test reconnect and a failed media/space join. These connection and physical-device checks have not been performed here.

The membership coordinates use each avatar's feet at x, centerY+16. The two rectangles do not overlap or share an inclusive edge. Their 16px separation avoids overlapping speaker/listener flags. Audience coverage includes every seat and the broad internal circulation. The source treats speaker/listener membership as simple flags, so do not build overlapping or duplicate audience areas as a workaround.

## Files and portability

stage-areas.merge.json contains only the two native area records. The audience's speakerZoneName is the podium AREA ID, not its visible name. Preserve that reference when importing or recreating the records.

magical-campus.wam is a fresh-room configuration template with no pre-existing entities or other editor areas. Place it beside magical-campus.tmj only for a NEW map-storage import. The existing importer and relative mapUrl resolution are source-verified; no upload was performed here. Never upload this minimal WAM over an established room: map-storage can replace a same-named existing WAM. For an established room, use the editor steps above or merge the two areas into a copy of its actual WAM while preserving all other data.

A hosted TMJ URL alone does not install WAM properties or activate native broadcasting. This file is not a configured live room, and the native role is entered only after a successful space join. No automatic click-to-sit, player-aware routing, or seating animation is added.

## Pinned source

- Native feature guide: https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/docs/map-building/inline-editor/area-editor/broadcast.md
- WAM schema: https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/libs/map-editor/src/types.ts

Validation: the exact pinned native WAM schema parses this file; audience linkage and non-overlap pass; all 24 seats and 240 feet-position samples fall in the audience only; the speaker falls in the podium only. Relative mapUrl resolution and the paired map-storage import are verified from source. Live media connection, upload, reconnect and physical-device acceptance remain untested. No live configuration has been changed.

- Relative mapUrl client resolution: https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/play/src/front/Phaser/Game/GameScene.ts#L720-L739

- Editor control feature gate: https://github.com/BAWES-Universe/workadventure-universe/blob/75666c0ccae779515b6fcbd83446ebd1eee29d1b/play/src/front/Components/MapEditor/EditMode/areaProperties.ts#L86-L120
