# Campus11: campfire access and junction arrival

A focused, separately versioned repair of the user-tested Campus10 map. The four fire-court bench positions, the northeast planter escape and both clockwise/counterclockwise loops are reachable on the existing32px native grid. Two small bench receivers were authored to match their fixed physical footprints; the fire, original water/lighting effects and surrounding scenery remain registered. Low rail/plant ownership is fixed per object; there are no player-following masks or conditional collision changes.

The arrival and its single silent area move together to the east diamond junction. A physical directional board sits beside the route with paths toward Student Hub, reception/meetings, classroom, stage, campfire and market. The fountain social area is outside the relocated silence. Native silence prevents ordinary proximity initiation while retaining ambience; it does not fix the game's separate initial-connection grouping race (#735).

## Use

Import map32/magical-campus.tmj. Its relative dependencies reuse hash-recorded, preserved Campus09/10 assets. Keep those served paths. This preview does not replace Campus10 or any gate. The giant gate remains a separate map that the owner can connect using the existing room editor.

map32/magical-campus.wam is an OPTIONAL fresh-room stage/audience template. A TMJ URL alone does not install it. Do not overwrite an existing room's WAM with this minimal file. Preserve unrelated areas/entities when merging. Native podium/audience controls depend on the deployment's broadcast-area feature flag; successful role/space connection is not verified here.

## Verified and remaining limits

748 tap-route legs and20 directional journeys pass against the pinned native32 path/body contract. Both full loops, the screenshot escape points and all four bench returns connect. The compiled foreground has zero opaque head cuts across72,539 valid fire-court positions and12 cardinal frames. Fourteen arrival/return legs and6,901 walking frames pass. All60 animation frames, positions and timing,24 event seats and native audio remain unchanged. The23-file standalone runtime rebuilds byte-identically.

These are source-model and compiled-pixel checks, not a live-room or physical-phone playtest. Bench positions use the ordinary Woka standing frames, with a static south backrest overlap; there is no animated sit pose or autosnap. Native paths ignore other people. Some fire-court gaps remain32px wide rather than a broad promenade.

## Provenance and preservation

The bounded bench repair was authored with the built-in image tool from the project's own garden artwork. Only registered bench receivers are adopted; the original and intermediate masters remain in the separately preserved source checkpoint. The board is project-authored SVG. No Conference Campus or other third-party artwork was copied. Original asset rights and attribution are unchanged; no new blanket license is assigned.

The publication is additive and references preservedv9/v10 image/audio assets. The defined decoded texture footprint is49,811,456RGBA bytes; this avoids re-uploading the existing23.87MB of dependencies. The new TMJ plus atlas is393,757bytes. No engine change, deployment of game code, or PR merge is part of this update.
