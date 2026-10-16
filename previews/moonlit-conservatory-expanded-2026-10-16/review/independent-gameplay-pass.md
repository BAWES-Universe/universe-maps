# Independent actual local gameplay pass

Non-author reviewer controlled the real local game through CDP at `localhost:8000/_/global/localhost:8766/moonlit.tmj`. Used engine pathfinding and actual keyboard events; no teleportation, mocked renderer or collision bypass. Map was not edited by reviewer.

Evidence directory: `/workspace/moonlit-runtime/independent/`.

- `independent-runtime-water-and-routes.mp4`: approximately 58.6 seconds, continuous CDP capture, 863 timestamped frames. Includes traversal and holds on lower fountain and upper terrace.
- `results.json`: successful fountain, upper terrace and upper bed-north arrival; native zoom=1 and scale=1.
- `collisions.json`: keyboard attempts into planter and five tables, then repeated water crossings and return near spawn.
- `fountain-0.png` through `fountain-5.png`, `terrace-0.png` through `terrace-5.png`: successive real-runtime frames at approximately 700ms intervals.

## Findings

New water highlights are materially more visible than original artifact: successive fountain views show changing bright cascade streaks and pool rings, and successive terrace views show changing bright streaks over selected upper waterfalls. The effect is an animated transparent highlight overlay on static artwork, not animation of every water pixel or every waterfall. Reviewer inspected successive native-view frames; supplied continuous footage allows full-motion playback. No claim that all painted waterways animate.

Five table centers resisted 1.5-second ArrowUp movement from south approaches. Upper tables stopped at sprite y256/feet272, terrace at y544/feet560, lower tables at y1472/feet1488. Avatar did not enter the blocked tabletop cells. No Enable water sound/Mute water prompts appeared through the checked route crossings. Camera zoom and avatar scale remained1.

The upper planted bed still had a visible north-edge problem in this candidate: ArrowDown from (752,368) stopped at sprite(752,400), feet416, placing avatar over painted flowers. This was reported immediately; author queued blockers on row12 while preserving row11 upper path. Requires final reload/retest on north and other edges.

Final seating was deliberately excluded while author adjusted chair registration offline. Final candidate acceptance remains pending these final changes and retest. Fake-camera preview appeared on first keyboard interaction; diagnostic collision screenshots retain it. Reviewer switched it off using native camera control before releasing browser; clean video was captured before that preview appeared.
