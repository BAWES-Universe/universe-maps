# C south entrance: proportional source prototype

This is a bounded architectural entrance prototype, not a new map, full-building roof, runtime implementation, publication, or authenticated gameplay test. It uses the frozen corrective A as its unchanged interior source. No v06 façade, roof, or side-door raster was reused.

## Review first

- `review/entrance-native-review-sheet.png`: outside, approaching Greg, revealed foyer, and accepted reception/chair/podium comparisons. Every pictured art crop is native 1:1. The surrounding card is layout only.
- `review/outside-occupied-native.png`: the new south entrance with an original 32×32 Greg frame.
- `review/approach-revealed-native.png`: the same position and architecture registration, after the proposed early hide.
- `review/inside-revealed-native.png`: Greg through the door, with reception occupied at A's original anchors.
- `review/full-context-compositing-preview.png`: a labeled half-scale overview and a separate 1:1 foyer detail. Only the south entry module is new; the roof and long wall wings have not been authored.
- `review/entrance-registration-native.png`: diagnostic clear-route and trigger annotation. Use the unmarked art images to judge visual quality.
- `review/entrance-review-sheet-2x-nearest.png`: explicitly labeled 2× nearest diagnostic enlargement; it is not a native asset.

## Proportions and visual design

The new generated 1536×1024 master is preserved intact. Its exact crop `(0,104)-(1536,872)` is 1536×768. A single uniform 5/12 reduction produces a 640×320 native entrance module. Both axes have exactly the same scale; there is no stretch, selective widening, upscale, or v06 source reuse.

The visible wall rises roughly 184px above its footprint, the flush open door is roughly 125px tall, and the finial rises roughly 252px above the threshold. The portal opening is approximately 140px wide, with a conservative 128px clear center band. An original 32px Greg is about one quarter of the door height. Broad stone piers and readable teal/gold ornaments follow the accepted chair and stage material family. The door has a shallow recess instead of a deep invented tunnel; there are no entrance steps, fake upper-floor physics, or raised floating floor patches.

The native assembly is a front/south game façade. It uses parallel horizontal courses, vertical posts, and a modest visible pediment/eave top. It is not a cinematic building illustration. The deliberately shallow eave does not claim to show the final auditorium's roof depth.

The generated master included a diffuse transparent glow. The structural-alpha derivative retains only the largest connected alpha≥128 component before reduction; this removes the exterior glow and isolated specks while preserving original RGB. Original masters remain available for inspection. No corrective recoloring or geometry painting was applied to the generated façade.

## Exact registration

All A assets are translated by `(+128,+256)` into a 2816×2432 prototype canvas. Interior pixels, chairs, stage, meeting bays, reception, and Greg are never resized. The broad source body remains approximately 1536×1728; A's existing arrival opening extends through source y1776. The proof follows that exact threshold instead of contracting the room to a rounded footprint.

- Module origin: `(576,1762)`
- Door threshold: `y2032`, corresponding to A source y1776
- Conservative visual clear portal: `x832..960`, width 128px
- Entire 32px frame center corridor within that band: `x848..944`
- Existing A approach/opening: `x768..1024`, width 256px
- Proposed later expanded landing: `(704,2032)-(1088,2224)`, 384×192px

A's current 256px approach is preserved in every proof. The wider landing is a coordinate proposal only, to be dressed with B's final exterior material family later; no provisional tiled floor or reused indoor material was invented. There is open walking room in front of the door. The garden remains to the right.

## Layer partition and reveal

The 640×320 asset/mask pairs are in `assets/` and `masks/`:

1. Base: only a 128×4px flush threshold floor strip, drawn below actors.
2. Foreground: the tall walls, decorative jambs, door leaves, their lower pedestals, and temporary portal interior.
3. Roof: the local entrance pediment/eave.
4. Shadow: a restrained native footprint contact shadow; 7px offset, low alpha. This hides with the frontage.

The base, foreground, and roof partitions reconstruct the native generated assembly pixel-exactly. Their seams are integer mask boundaries, not resized strips. The shadow is a separate documented derivative. The first split retained awkward cut-off door bases; those were removed from the persistent base. On reveal, all tall architecture, including door bottoms, disappears together and A's original low-wall footprint returns cleanly.

Proposed approach reveal rectangle: `(512,1696)-(1280,2112)`. Hide foreground, roof, and façade shadow immediately upon entry. Do not wait until the player reaches the threshold. At the south trigger y2112, a conservative 32px frame has top y2096. The southernmost opaque façade pixel is y2051; the faint antialiased fringe ends y2054. This leaves 44px to opaque art and 41px even to any nonzero alpha. The rectangle also extends far enough on the sides for that same frame allowance. Use immediate removal for this proof; a fade would need its own speed/timing validation.

A proposed south re-close boundary is y2144, giving 32px hysteresis beyond the entry trigger. Spawning or teleporting into the interior must initialize to revealed. The broad whole-building reveal region and camera framing still need later source/runtime design.

Collision is separate. This prototype neither compiles nor toggles it. A's existing grid is the constant source proposal. The 128px band describes the visible door aperture, not a new invisible collision throat inside A's preserved 256px entrance. New wall art must never create a multi-level floor or new collision automatically. Final collision and click-to-move behavior still require live validation.

## Side-door attachment plan (not generated)

See `side-door-join-plan.json` for exact source and translated coordinates. Future east doors must be side-facing wall bays whose threshold contacts the actual east wall plane, with a shallow porch joined to that same vertical wall. They must not be floor tiles cut into the middle of a large roof plane. A north/south façade cannot simply be rotated, stretched, or pasted onto the roof to stand in for the east-facing asset.

The hall/garden opening translates to `(1536,704)-(1696,800)` and the foyer/terrace opening to `(1600,1568)-(1664,1728)`. The main exterior wall plane is x1664. Preserve those routes and the garden's current position. A later porch can project a small distance east, with its own low roof section physically attached to the wall. Draw its jambs outside the clear north/south route and use a reveal margin derived from the new asset's actual alpha silhouette plus the whole 32px frame. Generate and inspect those modules separately before any whole-building roof.

## Evidence and boundaries

`validation/source-proof.json` establishes exact A translation, exact architecture mask reconstruction, the source-calculated head margin, and 351 sampled conservative frame positions in the clear-route proof. `validation/independent-check.json` additionally verifies the full accepted foyer and hall remain pixel-identical in the empty revealed composition. These are image/geometry checks only.

No TMJ/WAM, audio, engine, controller, collision, deployment, GitHub, or Library state was edited. The known PR799 deployment is not evidence that this entrance was run there. No browser or authenticated gameplay claim is made.

Rebuild locally with `python tools/assemble_entrance.py` using Pillow, NumPy, and SciPy. The script reads frozen A and writes only this prototype directory. The built-in imagegen prompt is saved in `prompts/entrance-01.txt`; the original output is `masters/entrance-generated-master-01.png`. `proportional-scale-manifest.json` records the scale, coordinates, partition, input hashes, and limits.
