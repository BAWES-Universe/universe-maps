# Native seating and furniture investigation

Engine checkout: `6b551e37c11d0bb344fd8429974cadca80ccedae`.

## Supported behavior evidence

- `docs/map-building/inline-editor/entity-collection-file-format.md` shows chairs with `tags:["seat","basic"]` but explicitly defines tags as filters for Map Editor UI. It describes collisionGrid and depthOffset as physical/draw settings, not sitting actions.
- `play/src/front/Components/MapEditor/EditMode/ObjectsPanel.svelte:107` implements name/tag filtering. A seat tag is not an interaction binding.
- `libs/map-editor/src/types.ts:242` defines the complete entity action discriminated union: Jitsi, playAudio, openWebsite, openFile, description, Livekit. No sit action exists in that union.
- `play/src/front/Phaser/ECS/Entity.ts:371` dispatches supported entity actions; no seat interaction is dispatched.
- `play/src/front/Phaser/Player/Animation.ts:7` defines only Walk and Idle; animation frames are the standard 12-frame four-direction spritesheet. `play/src/front/Phaser/Entity/Character.ts:431` chooses Walk or Idle from direction/moving.
- Character.ts's playEmote renders a DOM text emoji above the avatar. It does not change the avatar into a seated pose.

Conclusion: this checked-out engine provides chair artwork, walkable/collidable entities, and editor seat tags, but no native sitting action or pose was found through its schemas, runtime dispatch and avatar animation code. Making chairs reachable is achievable as a map repair. Claiming an actual native sitting action based on a seat tag would be incorrect. Any runtime-specific extension absent from this checkout must be demonstrated separately.

## Painted furniture inventory

Coordinates below are approximate visible artwork centers, **not proven player destinations**. Player sprite-to-feet offset and actual collision body must be accounted for in gameplay tests.

| Group | Table center | Left chair | Right chair | Table tile |
| --- | --- | --- | --- | --- |
| Upper pavilion west | (225,245) | (200,250) | (252,250) | (7,7), blocked |
| Upper pavilion east | (424,245) | (400,248) | (448,250) | (13,7), blocked |
| Upper terrace | (1204,530) | (1168,530) | (1248,530) | (37,16), blocked |
| Lower pavilion west | (1135,1457) | (1103,1464) | (1166,1464) | (35,45), blocked |
| Lower pavilion east | (1404,1457) | (1372,1464) | (1437,1464) | (43,45), blocked |

Total visible round tables: five. Visible chairs: ten. Tea counters: two, approximately (310,180) and (1255,1350). Lower cutout tiles are offset by **1056 pixels** in world Y.

Most chair-center cells are unblocked. The upper west table and its right chair partly share blocked tile (7,7), so alignment may prevent a natural chair approach even though adjacent row 8 is open. Test entry from the southern open row and account for the Woka's +16px feet offset. Table footprints need tests around their edges, not just center-cell checks. Lower table top is near y=1450 and feet extend below it; collision row 45 blocks the tabletop while row 46 is open. Verify that standing on the lower row does not place the avatar on top of the painted table.

The full map image contains no other obvious benches or seating furniture beyond these ten chairs. This is visual inventory, not a claim of completed gameplay acceptance.

## Clarified acceptance scope

The user subsequently clarified that seating means natural occupancy, facing and chair-back layering through supported native map capabilities, not a new sitting-pose animation. Therefore the missing dedicated sitting action/pose **is not an acceptance blocker**. Native `play/public/collections/FurnitureCollection.json` follows this convention: Basic Chair variants have directional artwork and no collisionGrid, permitting occupancy; tables define physical collision separately. Review must now evaluate reachable chair positions, facing toward tables, visual relationship to chair backs, and blocked tabletop footprints.
