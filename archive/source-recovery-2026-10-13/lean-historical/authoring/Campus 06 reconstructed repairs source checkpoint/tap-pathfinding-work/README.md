# StudentHub mobile doorway audit

The restored revision06 entrance is not too narrow for the native avatar body. The supported map-side candidate is the existing binary-roof reconstruction: keep its16px retention band and permanently hide the shared translucent layer. No StudentHub collision cells need to be opened on the evidence here.

This is a source-level map audit and a roof-event regression test. It does **not** reproduce the user's actual northbound mobile tap loop or establish what JavaScript bundle the phone loaded.

## Source and geometry

- Map: `public/butterfly-town/v6/map16/magical-campus.tmj`, SHA-256 `b3b124bd6bbb4ab573eb2848ca4681a58991a3e4a481a7dc1e0f046c62171696`.
- Dimensions:240×216 cells;16×16px cells;3840×3456px world.
- StudentHub is `office` in the roof contract.
- The approach rectangle is x1664..1856, y1488..1616. The interior rectangle is x864..2864, y512..1520. Baseline upper bounds are exclusive. Player feet are y+16.
- The entrance corridor opens columns107..112: x1712..1808, a96px opening. A16px-wide body can occupy center x1720..1800. At y1520..1536 the opening broadens to128px (columns106..113).
- The native body occupies[x−8,x+8]×[y,y+16]. Contact at an edge is allowed.
- `collision-permanent` is visible=true and opacity=0. Native pathfinding sees it; this is not an invisible-layer collision mismatch.
- Only tileset `collision-cell`, GID61154, has a `collides` property. All four adaptive roof layers have zero colliding cells. All16 combinations of roof visibility produce the same authored tile collision grid.

## Verified checks

`audit_studenthub.py` reads the map without changing it. It validates the authored grid and sweeps72 routes between every pair of the six entrance-column centers in both directions, including native first-waypoint and exact-endpoint adjustments. All44,985half-pixel body samples, including a straight joystick-style ingress, are clear of permanent collision. The local A* uses eight neighbors and forbids diagonal corner cutting; it checks geometry and does not substitute for executing EasyStar/Phaser on a phone.

`test_door_roof_feedback.cjs` executes the **actual** baseline and candidate roof scripts against the map in a JavaScript VM. It injects the8px northward first leg found in the native route-restart code:

- At the baseline south interior boundary (origin y1504 / feet1520), five southbound-crossing/northward-kickback cycles cause ten shared-roof transitions.
- At the baseline south approach boundary (origin y1600 / feet1616), five cycles cause ten opaque-roof transitions.
- The existing candidate has zero transitions for both five-cycle sequences.
- At the candidate's retention edge, moving out closes the opaque roof once; an8px kickback does not reopen it.
- Smooth northbound center ingress triggers two baseline visual changes or one candidate visual change. It does not itself produce a loop in this test.

These findings support a roof/replanning feedback mechanism and its bounded mitigation. They do not justify calling that mechanism the proven cause of this particular reported ingress failure. No static collision pushes the tested center ingress back south across either trigger boundary.

## Native source evidence

The separate engine trace checked branch`universe` commit`f00b3482f23c51976b4b339d7a891cad683d6498`. Its`PathfindingManager`, `Player`, and `GameMapFrontWrapper` blobs match the earlier map-audit pin`6accae707e5a26bc56231ef241c64b397a5cea70`.

- Visual show/hide unconditionally updates the collision grid: [GameMapFrontWrapper](https://github.com/BAWES-Universe/workadventure-universe/blob/f00b3482f23c51976b4b339d7a891cad683d6498/play/src/front/Phaser/Game/GameMap/GameMapFrontWrapper.ts#L292-L312).
- An active route is restarted on grid change: [GameScene](https://github.com/BAWES-Universe/workadventure-universe/blob/f00b3482f23c51976b4b339d7a891cad683d6498/play/src/front/Phaser/Game/GameScene.ts#L4091-L4103).
- First waypoint adds8px on a16px map; Player then subtracts16px: [PathfindingManager](https://github.com/BAWES-Universe/workadventure-universe/blob/f00b3482f23c51976b4b339d7a891cad683d6498/play/src/front/Utils/PathfindingManager.ts#L43-L69), [Player](https://github.com/BAWES-Universe/workadventure-universe/blob/f00b3482f23c51976b4b339d7a891cad683d6498/play/src/front/Phaser/Player/Player.ts#L117-L164).
- Joystick input cancels the tap route and uses velocity movement: [Player](https://github.com/BAWES-Universe/workadventure-universe/blob/f00b3482f23c51976b4b339d7a891cad683d6498/play/src/front/Phaser/Player/Player.ts#L88-L101).

Do not describe every replan as a16px destination drift. On this grid, exact-target fitting often preserves the snapped destination. The proven first-leg offset is8px northward.

## Reproduce

From this directory, with the exact restored map and the adjacent`roof-work` candidate:

```sh
python audit_studenthub.py --map /path/to/map16/magical-campus.tmj
node test_door_roof_feedback.cjs /path/to/map16 /path/to/roof-work
```

Outputs are`studenthub-audit.json` and`door-roof-feedback.json`. The baseline map and both tested scripts are read-only. The feedback harness reconstructs only the candidate's relevant map metadata in memory; it does not install a patch.

For an integrated mobile acceptance test, capture the precise avatar start, tap destination, movement direction, roof state, and any repeated route restarts. Test northbound ingress, southbound exit, taps near both doorjambs, repeated taps, and joystick takeover. A successful live result is still required before saying this fixes the reported phone behavior.

## Candidate choice

The existing16px retention band is the smallest currently supported map-side correction that preserves continuous roof adaptivity and static collision. It prevents an8px restart from crossing back into the reveal region after closing. Keep the permanent collision data untouched.

Deferring all roof updates until moving=false is a separate, broader script-only workaround proposed in the engine trace. It would remove mid-route visibility replans, but changes the experience by waiting until the player stops before revealing a roof; it is not required by these doorway geometry findings and has not been implemented here.

PNG crops use world bounds x1568..1920,y1360..1712 at3× size. They are reconstructed source artwork, not runtime screenshots. The collision overlay colors blocked cells pink, interior max boundary cyan, approach boundary yellow. No engine, live map, published site, or restored baseline was edited.
