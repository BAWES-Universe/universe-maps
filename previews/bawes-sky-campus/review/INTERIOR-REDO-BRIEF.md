# Fresh whole-interior proposal — review checkpoint, not implementation

The rejected interior is frozen. Only the unsolicited beverage prompt and its prompt-dependent steam trigger have been removed. No replacement dialog, button, keyboard hook or other interface was added. Existing native movement, chair-position access, R rotation, meeting courtesy-lock controls and gate behavior remain available. No art or layout has been changed in this pass.

## Recoverable snapshot

- Full source/map checkpoint: `2a1adb9fc75ecfcafabba91a9eb4bdcbfc68afae`.
- Local branch: `backup/bawes-interior-before-redo-20261018`.
- Runtime review archive: `/workspace/bawes-sky-campus-before-interior-redo.zip`.

The approved keeper is the **lower-left outward-facing lounge idea**, not the current upper-right couch placement. The fresh proposal restores that idea. The exterior layout and gate appearance are keepers. Nothing in this proposal has been integrated into the map.

## Why the current map is inconsistent

| Source/use | Actual source → world placement | Consequence |
|---|---|---|
| Campus ground, edges and vegetation | `campus-site-cutout.png`, 1536×1024 → 4608×3072, Lanczos 3× | Foreground paving and plants are enlarged painted detail, not native-size modular assets. |
| Building shell and its planting | 1536×1024 source, alpha crop 1509×652 → 2240×968, approximately 1.484× | Sharper plant silhouettes sit over the much softer campus plants. Both images contain vegetation. |
| Desk | Cropped 313×281 → 64×64, Lanczos | Detail is reduced to about 20–23%; unequal axis ratios also change its aspect. |
| Red chair | Cropped 218×272 → 32×40 | About 14.7%; the retained outlines and lighting differ from the room crops. |
| Freestanding planter | Cropped 392×268 → 80×64 | About 20–24%, with unequal axis scaling; distinct from the enlarged baked plants. |
| Stone floor | 64×64 crop from `floor-original.png` repeated at 1× | Small repeated masonry detail, with no common authored density/light treatment with the furniture. |
| Walls and rugs | Separate 448×288 Butterfly Town room; 48×48 textile repeated/recolored, 12×80 wall strip repeated | Different asset family, repeated fragment edges, code-drawn rug borders and chopped architectural motifs. |
| Reception glow | Separate 128×96 Lantern Courtyard glow → 128×128 | Another family and nonuniform scaling near the criticized reception/coffee area. This should be omitted from the fresh design. |

The engine sets `pixelArt: false`, `roundPixels: false`, `antialias: false`, `antialiasGL: false`. The map does not apply different renderer filters to individual families. Normal-camera captures use zoom 1 and Woka scale 1; in this client a 1440px screenshot spans 720 world pixels, exposing each native texel at roughly two screen pixels. A uniform blur or renderer change cannot reconstruct missing source detail or make the different lighting/outlines agree.

The old central geometric mark was already removed in `2a1adb9`. The current reception floor is plain stone; historical clips can still show the old mark. The adjacent red carpet is a recolored, repeated sample from the unrelated library room. No such carpet, emblem or glow is carried into the fresh proposal.

### Duplicate plants are baked, not just a filter setting

The [normal-scale composite](normal-transition-composite.png) and [same-camera base-only diagnostic](normal-transition-base-only.png) show the soft planter cluster still present in the campus plate after the sharper façade layer is hidden. The diagnostic changes visibility only for capture; it is not a proposed fix. This is a real compositing overlap. The current campus PNG has no independent plant masks or hidden clean paving beneath those clusters. The façade PNG also includes flowers, pots, vines and their shadows in its building artwork.

The two small interior overlay planters sit over the authored indoor floor, not over a second plant sprite. They still belong to a different detail treatment. Removing those alone would not resolve the exterior duplicate planting. No plant was blurred, painted over, upscaled, or concealed with another sticker in this pass.

### Seats and room fragments

The BAWES furniture sheet has front-view red and amber chairs, not a coordinated set of rear/profile views. `chair(..., facing)` currently chooses chair artwork and records metadata; it does **not** command the Woka to turn. The engine has native R rotation, but the public map API has no seating pose or automatic chair-facing command. Prior chair reachability checks must not be described as proof of correct seated poses. Current occupied diagnostics show ordinary native Wokas at chair anchors, not invented seated animations.

The alternative Butterfly Town furniture-foot/canopy sheets do contain other chair/table arrangements, but they are small bundled compositions matching that separate room family. Combining them with the current façade/furniture would introduce another style instead of solving the whole-map problem.

Right-room upper wall panels are cropped from a 408×48 library strip into 288px room spans. Short side returns and unrelated glass pieces complete the collision geometry but read as disconnected fragments. Roof-on views additionally clip interior imagery to façade window apertures. Complete collision boundaries do not make these fragmented visuals legible; the new design requires complete matching wall modules and an explicit whole-room cutaway rule.

## Fresh spatial proposal

[Full footprint and occupied scale study](FRESH-INTERIOR-SPATIAL-STUDY.svg)

This is a **spatial schematic, not finished art or an in-game preview**. Furniture rectangles are placeholders. Woka markers are 32×32 at map scale; they check relative occupancy/clearance and do not claim a seated animation. The current assets cannot honestly supply a coherent beautiful final-art preview, so none is presented as approved.

- Keep the verified 2144×592 interior and 192px central arrival spine.
- Restore a lower-left window lounge with two outward-facing sofas and low side tables, away from the entrance.
- Replace desk rows with two separated individual work settings and one shared project table. Use open space between purposes, not repeated carpet boxes.
- Put reception beside the arrival route, with a quiet refreshment surface nearby. No coffee prompt, new interaction widget, carpet patch or glowing marker.
- Two right-side four-place meeting rooms have continuous perimeters, clear 96px entrances, a 96px inter-room route and approximately 112px clear front circulation. The schematic shows the full walls, not cropped decorative slivers.
- Use one continuous floor material. Seating upholstery and the furniture itself establish zones; omit rugs for this proposal.

Proposed art direction: warm ivory stone, restrained amber/brass edges, muted terracotta upholstery and natural green foliage, with the gate's existing material/light treatment as reference. One light direction and one native outline/detail budget across all foreground assets. No teal library motifs, repeated lamps, pasted bookcases or standalone glow.

## Smallest coherent asset-production scope

Production has **not** begun. No paid generation is requested or initiated by this document.

1. **One coordinated native-scale interior kit:** seamless stone floor variants; continuous wall runs, corners, ends and door reveals; front/rear/profile chair views with declared seat anchors and foreground masks; a work surface, shared table, reception counter, outward-facing sofa and small side table. Existing approved furniture/gate art can serve as reference and be retained where it passes the same occupied-scale check. Export at intended world-pixel sizes without per-item aspect stretching. This replaces the borrowed library kit as a whole.
2. **One clean campus ground/edge plate at its intended 4608×3072 foreground scale**, preserving the approved layout, with the duplicated plant clusters actually removed and underlying paving/edge/shadow areas reconstructed. Separate vegetation/shadows from the plate. Enlarging the existing 1536×1024 image is not this deliverable.
3. **One matching façade/ground-transition vegetation pass**, preserving the building silhouette and liked gate: plant-free architectural/threshold pixels where needed, plus a small shared set of shrub/planter/tall-plant modules and shadows. Replace underlying duplicate vegetation, not only its cover layer. Distant sky islands may remain deliberately softer; walkable foreground must share the native treatment.

These are bounded art deliverables, not a new map layout or an engine project. The first review should show one complete whole-interior composition using that kit, with real native Wokas occupying a desk, both sides of a meeting table and the outward lounge, plus the entrance transition at normal camera scale. Review it together before integration. If true bent-leg seated Woka animation is required rather than convincing occupied placement, that needs a separately supported avatar/engine capability and is outside this map-only scope.

## Evidence and implementation boundary

- [Normal-scale interior at beverage/reception, no popup](normal-interior-no-popup.png)
- [Normal-scale work area](normal-interior-team.png)
- [Native Woka at a reachable chair position](normal-interior-seat.png)
- [Popup check](consistency-checks.json): no map popup API calls during approach, dwell and Space; no beverage prompt text.
- [Occupied meeting diagnostic](normal-occupied-meeting-0.png) / [second anchor](normal-occupied-meeting-1.png)
- Right-side [cutaway](normal-meeting-cutaway.png) / [roof-on](normal-meeting-roof-on.png), identical normal camera.

These captures document the rejected map and its defects after popup removal. They are not a claim that its art, seats or room treatment are fixed. The new proposal is pending review and coherent assets. No incremental layout/art changes, deployment, public publication, paid generation or engine changes were performed.
