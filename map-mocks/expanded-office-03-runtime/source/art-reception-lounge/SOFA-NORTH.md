# North-facing sofa counterpart

Original rear-view painted counterpart to the existing south-facing teal two-person sofa. The artwork was generated as a new view, never rotated or reflected. Existing reception, south-facing sofa, and coffee-table assets remain unchanged.

## Integration

- Full art: `native/sofa-north.png`
- Combined real back/arm foreground: `native/sofa-north-foreground.png`
- Detailed geometry and results: `sofa-north-manifest.json`
- Native empty/occupied pairing: `proofs/sofa-north-pair-empty.png`, `proofs/sofa-north-pair-occupied.png`
- Route diagnostic: `proofs/sofa-north-routes.png`

The canvas is 160×96 and measured object bounds are (16,16,128,64). Preserve local seats (52,32) and (108,32), facing north. Use unchanged Greg index 10, 32×32. Draw the full sofa below actors and the combined foreground at the same origin above them. Its genuine backrest top is local y33 and it extends through about y74; the side arm pieces are separately available.

Physical floor blockers are local [16,48,128,32], [16,16,12,32], and[132,16,12,32]. The elevated visible back projects above its floor footprint. Each 16×16 actor body at the intended seat spans y32..47, stopping precisely before the back's floor blocker at 48. Approach and exit from the north. Do not block the whole 128×64 visible rectangle.

## Validation

Both north-facing occupants retain all 248 opaque pixels in their protected first 14 sprite rows. The actual full backrest occludes 289 of 362 lower-body pixels per occupant. Seven sampled entry, exit, cross-lane, and side-bypass routes pass, including an occupied neighboring seat. The diagnostic pairing leaves 48px clear floor on both sides of the 64×32 coffee table and 64px side lanes.

This is a static asset-scale proof, not live runtime, claim, or sit-animation evidence. Runtime integration and collision/depth checks remain the parent's task.

## Preserved work

`source/sofa-north-prompt.txt` records the new-view generation; `source/sofa-north-correction-prompt.txt` records the targeted backrest correction. The first attempt placed the top edge about 3px too high and is retained as `source/sofa-north-attempt-01-high-back.png`. The accepted original source is `source/sofa-north-master.png` (1619×971).

`tools/build_north_sofa.py` derives the accepted native asset with one premultiplied reduction directly from its measured source alpha crop, traces the actual masks, and runs the occupied and route checks. It does not modify the earlier furniture assets. There is no paid external API use or artificial high-resolution upscale.
