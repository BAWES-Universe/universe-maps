# Bounded acceptance evidence · 2026-10-10

Map SHA-256: e421842c675eecd84cfabf9b0e1dbedb7f1d2268a0396eab48b09f1008734b8e

- PASS8/8 real Phaser3.86 native collision routes: spawn to authored seat and back, with all other seats represented by solid16×16 body fixtures. See occupied-seat-routes.json. No occupant body is crossed on these explicitly chosen clearance routes.
- PASS16/16 original-source tap routes: synthetic100ms touch event → Universe pointer handler → actual EasyStar0.4.4 → source-extracted native Player movement on real Phaser tile/body physics, with Player immovable=false and pinned default speed9 (180px/s). Zero attempted-body overlaps, zero resolved-body overlaps, zero size errors, and every expected destination reached. See native-tap-results.json and native-source-provenance.json.
- PASS16/16 analytical source-path approaches/exits, zero first-leg offset on32px grid.
- PASS exact atlas-to-layer pixel roundtrip and exact original-pixel furniture foreground split. Four near chairs relocate down8px, which is the only furniture-art placement change.
- PASS all720 original permanent collision-grid cells unchanged; both full table blockers remain.
- PASS all authored head top10px clear in masks; moving-avatar browser captures show the heads above table/backrest foreground.

Screenshots are actual standalone browser canvas captures at native scale. native32-eight-seats.png includes seven stationary occupant fixtures and the tested avatar, not a live multiplayer session. native32-source-tap-seat.png shows the source-tap test's single avatar.

## Limits

No full Universe repository build/import, live multiplayer/proximity conversation, physical mobile device, camera or microphone test was run. Normal proximity behavior is not disabled and there is no scripted conversation gate. This does not mean arbitrary taps automatically route around live occupants: the separate conservative occupied-body test establishes available routes, while the native source-tap test is single-player. No sitting animation, pose switch, seat lock or interactive room service is implemented.

## Iteration record

An8px physics-grid experiment was rejected due to native path/body offset concerns. The delivered map is32px. Early test paths grazed exact obstacle boundaries and failed with floating-point drift; final routes add2px clearance and leave each chair via its clear front/back approach, with no map collision deletion. Only final-map results above are acceptance evidence.

## Reproduction scope

The included Python source reproduces the exact TMJ/atlas, pixel-roundtrip checks and conservative occupied-body routes. Full browser harness/source checkpoint is retained in the owner’s Library, separate from this lean Git package. This PR includes exact browser JSON evidence and native-source hashes; it does not vendor another Phaser runtime.

## Superseded evidence

`superseded-native-tap-immovable-true.json` is retained for audit only. Its Character-style immovable=true and fixture speed6 configuration did not match the native Player constructor/default speed. It is replaced for acceptance by the fresh 16/16 immovable=false, speed9 browser run in native-tap-results.json. Occupied-seat evidence already used immovable=false and remains separate.
