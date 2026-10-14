# Flagship glass / automatic-door study

Isolated research and review fixture. **No existing Flagship map was edited or published.** The approved stage and liked v09 approach entrance remain preserved. Only the stage is described as approved, not the whole hall.

## Deliverables
- `output/pdf/flagship-glass-design-study.pdf`: three-page visual review; pages 1-2 are design concepts, page 3 describes the implemented fixture.
- `map32/fixture.tmj` + sibling PNGs + `door.js`: small runnable native32 door/tall-glass fixture with original test art. Serve this directory together and use the TMJ as an isolated test entry.
- `tests/results.json`: 53 source-executed cases, 0 unexpected failures, 2 expected far-tap limitations. These are **not authenticated live-browser acceptance**.
- `source/research.md`: exact reference distinctions, source contracts and limitations.

## Replay
Python 3 + Pillow: `python3 source/build_fixture.py` (original tiles, TMJ, decoded state images).
Node: `node tests/run.cjs` (unchanged pinned native methods plus test adapters and actual fixture controller).
Python 3 + ReportLab: `python3 source/make_pdf.py` (uses two unchanged existing v09 visual references, paths recorded in script).

## What works in the source harness
Automatic opening on approach from either side, open-state crossing, retreat closing, repeated approach/retreat, initial inside detection, collidable closed threshold / walkable open threshold. One continuous doorstep covers front, threshold and back; crossing does not trigger a premature close at the seam. Persistent glass/frame never toggles. All fixture art is below `floorLayer`, so no foreground sprite can obscure the avatar head. Door states swap instantly; this is not a multi-frame slide animation.

## Important limits
A tap directly across a closed door from beyond the approach trigger has no route in this pinned fork. Two tests reproduce this rather than pretending it passes. Tap the approach first, then the far destination. Production behavior needs a reviewed choice: retain this two-step behavior, use a permanently walkable visual-only doorway (different semantics), or separately authorize a path-intent engine solution. None of those changes has been made here.
Room-variable state is shared in the prototype, but occupancy arbitration across simultaneous players is not implemented/certified: one player leaving could close another's door. Do not promote this fixture to a production shared entrance without that acceptance. Real iframe timing, multiplayer, failed initialization, server variable state and live deployed-version checks remain pending. Closed-by-default fixture failure blocks the test threshold; it is not an emergency exit design.

The source harness uses pinned engine methods from `60e7afdc3f96ef32525597cd46bd41175d61a2ef`, historically verified served by the existing v09 work. It does not establish what is deployed now. No engine files were changed, no latest Scripting API Extra was imported, and no paid services were used.
