# Forum Hall · Local Concept 01

One provisional second hall for parallel conference talks and panels. This is a design review and reusable art/source checkpoint, not an implemented or live room.

## The design

- **48 visible audience chairs** in three stepped fan-shaped arcs: 12 + 16 + 20. This is a count of drawn chairs, not concurrent-attendee capacity.
- **Three illustrated panel places** at one compact curved table. The small speaker figures are separated clearly. They are anonymous review-only scale references, not an event lineup. All panel, audience and visitor figures must be excluded from any future runtime art.
- **1024 × 896 native world pixels**, a 32 × 28 world on a 32px grid.
- **Unchanged 32 × 32 Greg Woka frames.** All audience chairs use the existing project's original north-facing art at its native 32 × 48 asset size. No chairs or avatars are rotated, enlarged or redrawn.
- A shallow low panel platform, chamfered room silhouette, continuous teal perimeter circulation and open southern arrival distinguish the Forum from the 210-seat flagship.
- The outer path and both side-stage approaches remain visually clear. They are intended circulation, not tested collision geometry or a verified accessible route.

## Review files

- `review/forum-overview.png`: whole-room design review, map rendered at native 1:1 scale within the page.
- `review/native-scale-composition.png`: four native 1:1 crops showing the panel, stepped arcs, entry/perimeter and empty chair layout.
- `assets/forum-occupied-native.png`: clean 1024 × 896 static composition with illustrative occupants.
- `assets/forum-empty-native.png`: same room without the illustrative audience or panel figures.
- `assets/forum-architecture-native.png`: normalized architecture only.

## Reusable source

- `source/forum-architecture-master.png`: original built-in imagegen result, retained non-destructively.
- `source/generation-prompt.txt`: exact generation prompt. The attached lobby and flagship are style references only; the Forum has a new floor plan.
- `source/seats.json`: all 48 exact chair anchors and illustrative occupancy choices.
- `source/scale-reference-positions.json`: native world dimensions, count and speaker/visitor frame positions.
- `source/*.svg`: self-contained deterministic source compositions.
- `references/`: unchanged Greg sprite sheet, original chair layers and style references.
- `tools/build-concept.mjs`: reproducible native SVG and PNG render, using Node.js and Sharp.
- `source/provenance.json` and `SOURCE-CHECKPOINT.json`: source origin, hashes and checkpoint inventory.

From this directory, run `node tools/build-concept.mjs`. This regenerates the PNG and SVG compositions from the retained master and the unchanged sprite assets. No model call is required to rebuild the review images.

## Honest limits

There is deliberately no TMJ, WAM, collision map, audio configuration, browser preview, live room, media stream, room link, portal destination or public deployment in this checkpoint. Runtime actor depth, walkability, each arc’s seat-entry/body/head geometry, seat reachability, spawn safety, silence, multi-user behavior and presenter/audience media remain unverified until a separate authorized implementation pass. The temporary table-front clipping used to demonstrate visual depth is a static composition technique, not an implemented game layer.

A subsequent authorized implementation should preserve this reviewed character, author the actual collision/foreground split, verify access to every chair and the panel, configure distinct Forum media identifiers, and validate live behavior before connecting it to the shared lobby. No feature flags, engine behavior, existing flagship/lobby/campus files or Arena assets were changed here.

“Forum Hall” is a provisional name. There are no real speakers, schedules, sponsor claims or event-capacity claims.
