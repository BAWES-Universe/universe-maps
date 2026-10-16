# Azure Pavilion — review candidate

A separate compact coastal Art Deco social map with reusable, text-free artwork. Public Pages preview publication was authorized2026-10-16. Runtime assets match tested commit0992485c4b48d0846aaf4ab00e17f8d2d3d92dc7. Moonlit and all unrelated maps are unchanged.

Open `azure.tmj` with its adjacent assets in WorkAdventure. The map uses a native32px grid, Woka scale1 and camera zoom1. It contains a glass lounge, two café groups, connected promenade, animated fountain, ocean caustic highlights and overlook. See [exact interactions](INTERACTIONS.md).

Spawn is silent. Profile → All settings → **Play sea sound** starts the optional quiet loop; the same action becomes **Stop sea sound**. No audio popup appears when walking. **Take nearest seat** positions Woka on a nearby cushion; ordinary movement exits. There are13 occupancy positions and6 blocked tables. Woka remains in its native upright pose.

## Validation

Actual game runtime: BAWES Universe v0.3.8, exact engine commit `274114560c5ec95fdf8e51e67986a53069f3cf06`, isolated local checkout. No engine merge or production deployment.

- All510 walkable cells form one connected component.
-404 actual traversals passed:101 maximal continuous horizontal/vertical runs × keyboard/right-click × both directions.The original416-traversal sweep included208 independent traversals; unchanged routes retain those results, with all four changed rear-wall runs retested.
- All13 seat approaches/occupancy/exits and all6 tables from4 sides passed independent review.
- Floor visibility, text-free art, roof enter/leave and native camera/Woka scale passed.
- Ocean/fountain motion recorded across repeated loops. Independent review inspected ordered rendered frames, not continuous audiovisual playback. The footage is provided for human review.
- Actual Phaser output capture passed: silent spawn; audible output after Play; Stop silence persists through walking and four further crossings. Six crossings while playing and four after Stop produced zero popups.

[Evidence gallery](review/index.html) · [Independent report](review/independent/independent-review.md) · [Route results](review/full-route-results.json) · [Audio evidence](review/final-audio-results.json)

## Limits

Ocean motion is restrained animated caustic highlights over static painted water, not physical surface displacement. Captured cadence is limited by the software-rendered browser; no claim of perfect60fps or physical-speaker/mobile validation. The rear wall is blocked to prevent façade overlap. Seat occupancy uses a bounded final native position adjustment to center Woka on the cushion; Woka retains its native upright pose.

The released native audio Stop action restarts full-map audio on the next tile movement. The tested map-only Play/Stop fallback avoids that defect; native audio master controls do not govern this separate channel. See [diagnostic](review/native-audio-limitation.md). No private/acoustic rooms or multi-user communication behavior is claimed.

## Source and publication

Final artwork: `coastal-unlabeled.png`, generated with the built-in image tool and downsampled to1280×1024; original retained in `source/unlabeled-artwork-original.png`. No external paid service. `source/build-layout.cjs` is an earlier geometry scaffold, not a final-map rebuild script; final TMJ/geometry are authoritative. `source/build-ocean.cjs` generates the ocean overlay. Fountain and synthetic sea-breeze were authored locally. Superseded labeled artwork remains only in earlier Git history; historical review screenshots are explicitly marked.

Publication is limited to this preview directory and its assets. No world registration, production deployment, permission changes or spending.
