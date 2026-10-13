# Event camera and broadcast source check

Checked repository: BAWES-Universe/workadventure-universe, commit `4d0b3a83f9e75e94ab55765247f26c83a2bc8974`. This is implementation verification, not a live multi-user test. No conference fixture was located during this targeted check.

## Safe native TMJ camera focus

Use a rectangular object in an objectgroup. Coordinates and width/height below are illustrative pixel dimensions, not measured N43/N44 bounds. Replace them with the complete stage rectangle from the generated map.

```json
{"id":101,"name":"stage-focus","class":"area","type":"area","x":320,"y":160,"width":640,"height":256,"rotation":0,"visible":true,"properties":[{"name":"focusable","type":"bool","value":true},{"name":"zoomMargin","type":"float","value":0.1}]}
```

The current wrapper recognizes `class` of `area` or legacy `zone`. Entry focuses the entering player's camera on the rectangle's center, with its complete width/height. It does not remotely move audience cameras when a speaker enters. The area itself is both trigger and framing target. A focus area covering only the audience frames only the audience. If a single whole-event frame is desired for everybody, use one focus rectangle enclosing stage and audience, and recognize that entry anywhere in it activates focus. Separate stage-only trigger and larger remote framing require a separately verified scripting approach; this is not provided by the focusable property alone.

Default margin is 0. A margin of 0.1 fits width × 1.1 and height × 1.1, yielding padding around the whole rectangle, not 10% on every side. Fit selects the smaller of available viewport width/target width and viewport height/target height. Default entry transition is 1000 ms. Leaving focus restores player follow and saved zoom over 1000 ms. Do not layer overlapping focus rectangles: leave handler exits focus without an overlap stack check.

Native dynamic TMJ area containment samples player y + 16, so use the visible walkable floor bounds and confirm edge behavior in play. Positive rectangle dimensions are required by the focus entry handler. Keep bounds inside the map and match native pixel scale.

## WAM speaker/listener companion

Minimal companion example; illustrative 640 × 256 stage and 640 × 384 audience. There is deliberately no silent area. Do not duplicate the same camera focus in TMJ and WAM when both load.

```json
{
  "version":"2.0.0",
  "mapUrl":"./map.tmj",
  "entities":{},
  "entityCollections":[],
  "areas":[
    {"id":"stage-area","name":"Stage","x":320,"y":160,"width":640,"height":256,"visible":true,"properties":[
      {"id":"stage-speaker","type":"speakerMegaphone","name":"N43 Main Stage","chatEnabled":false},
      {"id":"stage-focus","type":"focusable","zoom_margin":0.1}
    ]},
    {"id":"audience-area","name":"Audience","x":320,"y":448,"width":640,"height":384,"visible":true,"properties":[
      {"id":"audience-listener","type":"listenerMegaphone","speakerZoneName":"stage-area","chatEnabled":false}
    ]}
  ]
}
```

`speakerZoneName` references the speaker area's `id`, NOT its display name and NOT its speaker property's id. The helper resolves that area id to the speaker property's name. WAM speaker entry joins its named room and calls `startStreaming`; listener entry joins the matching room and sets listener state. `chatEnabled` defaults false in the schema; explicit false is clearer. Optional listener `waitingLink` is a string. Avoid overlapping speaker and listener areas so a player is not in both roles. Speaker entry is automatic, so the entry boundary should be an intentional on-stage transition.

WAM focus schema uses `{id,type:"focusable",zoom_margin}`. TMJ uses named properties `focusable` and `zoomMargin` (listener also accepts legacy `zoom_margin`). WAM area fields require id, name, x, y, width, height, visible and properties. Root requires version, mapUrl, entities, areas and entityCollections.

## Delivery limitation

An adjacent WAM is not automatically imported with a custom TMJ. GameScene sets mapUrlFile when the room has mapUrl; only the alternate room.wamUrl branch loads and parses WAM, resolves WAM.mapUrl relative to the WAM URL, then loads the TMJ. Therefore label speaker/listener as a supplied WAM configuration until room setup explicitly loads it and a real multi-user test passes.

Do not advertise a standalone TMJ speaker/listener pair as working. The inspected TMJ listener property resolves its string through WAM speaker areas; with no matching WAM area it returns undefined and does not join. WAM-to-Tiled conversion also builds a speaker string differently from the WAM handler, so mixing formats should not be treated as equivalent or tested.

## Pinned sources

- [WAM schemas and TMJ property names](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/libs/map-editor/src/types.ts)
- [Speaker area-id lookup](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/libs/map-editor/src/Utils.ts)
- [TMJ handlers, lines 729–841 and 935–943](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/play/src/front/Phaser/Game/GameMapPropertiesListener.ts#L729)
- [WAM handlers, focus at 652–668 and broadcast at 1368–1463](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/play/src/front/Phaser/Game/MapEditor/AreasPropertiesListener.ts#L1368)
- [Camera focus default and multiplier](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/play/src/front/Phaser/Game/CameraManager.ts)
- [Viewport fit calculation](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/play/src/front/Phaser/Services/WaScaleManager.ts)
- [Area recognition, containment and WAM property conversion](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/play/src/front/Phaser/Game/GameMap/GameMapFrontWrapper.ts)
- [TMJ versus WAM load branch, lines 446–450 and 727–760](https://github.com/BAWES-Universe/workadventure-universe/blob/4d0b3a83f9e75e94ab55765247f26c83a2bc8974/play/src/front/Phaser/Game/GameScene.ts#L727)
