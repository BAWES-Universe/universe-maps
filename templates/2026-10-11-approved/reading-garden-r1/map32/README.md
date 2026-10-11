# Reading Conservatory: Fountain Garden

A separate garden variant of the approved Reading Conservatory. The entire original 768×512 functional interior remains pixel-exact, with its original collision rows and furniture anchors. The map extends to 768×832 at native 32px Woka scale.

## Features

- Ten walk-to reading/conversation chair anchors, two standing study desks and three distinct native conversation areas
- Seventy new connected garden-floor cells: full fountain circuit, two-tile-wide side approaches to both image edges, and a south approach reaching the bottom edge
- Eight real basin-water animation frames, 140ms each, encoded as native Tiled tile animations
- Water refraction/ripples confined to a 2,125-pixel basin-water ownership mask; stone, flowers, statue, floor and avatar imagery do not animate
- Matching original interior foreground rails; no garden ground or water layer draws over avatars

## Verified source-level behavior

All 6,248 native route legs passed across the four actual spawn outcomes, with 4,750,935 body samples and zero collision/endpoint failures. Tests include both full-circuit directions, every open floor cell, exact authored anchors, same-cell moves, returns and tile-edge click extrema. There are 157 connected open cells and 114,688 checked integer 16×16-body positions. The upper-head foreground check has zero intersections.

The 70 new garden cells have a separate hash-bound visual art/geometry acceptance. All eight animation frames are decoded from the actual emitted runtime atlas and compared pixel-for-pixel; each frame changes only owned water pixels. Original interior pixels and collision rows are exact.

## Native controls and limits

Avatars retain ordinary standing-idle movement and facing controls. Chairs do not automatically sit, snap or turn characters. Main-group arrivals retain east/west facings; other approaches can face differently. Review PNGs and route GIFs show actual captured native positions/facings with authentic static idle sprites; they are rendered illustrations, not live browser footage or walking animation.

This package does not claim live-browser, keyboard/joystick, mobile, networking, LiveKit service or multi-user acceptance. Side and south paths reach the map boundary; no unconfigured cross-map portal or teleport is implied. Conservatively blocked margins around furniture and planting remain; physical silhouettes are not pixel-perfect polygons.

## Loading

Keep all runtime files together. Serve the folder over an authorized HTTP(S) host. map.wam references ./map.tmj; the map references its sibling PNG atlases. The map uses native Tiled animation and ordinary map layers; no custom script or engine patch is required.
