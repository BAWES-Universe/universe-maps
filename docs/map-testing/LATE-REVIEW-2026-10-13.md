# Later quality and gameplay review · 13 October 2026

[Testing register](README.md) · [Common acceptance checks](COMMON-CHECKS.md) · [Earlier quality review](QUALITY-REVIEW-2026-10-13.md)

This record consolidates the later user decisions and source findings from 13 October. It supplements the preserved cards and earlier review. Later explicit decisions below govern current review status even where an imported historical field still says Pending or Current candidate. This documentation changes no map assets, runtime, collision or engine code.

Collection IDs and hashes identify preserved artifacts, not independently captured user sessions or deployed-engine builds. User reports, source inspection, approach-only tests, file availability and full live acceptance remain separate. No new independent live-engine PASS is claimed here.

<a id="future-standards"></a>
## Latest direction: quality over quantity

**Fewer high-quality, polished maps take priority over the earlier 100-map quantity ambition.** New maps must actually **function, react and animate**: intended spaces and activities must work, interactions must provide meaningful feedback, and appropriate motion must be planned into the initial build and verified in-engine. Attractive previews and complete file packages cannot establish a working experience.

Keep varied art styles. Tea Garden and Art Deco set references for detail, clarity, cohesion and polish at playing scale; they are not a shared visual template. The earlier source-pixel, scale, seam and circulation checks remain applicable.

- Make every intended seating area approachable, including rear and side routes where the scene implies them. Use real ground-contact collision rather than artwork-sized exclusion rectangles; preserve walls, water edges and genuine solids.
- For seating advertised as usable, prove **approach → actual sit behavior → exit** on the exact runtime and engine, including benches. A scenic chair, standing anchor or route endpoint is not sitting. Disclose unsupported or absent sitting rather than labeling it implemented.
- Test the native avatar footprint, access and exit, and tabletop/canopy/light foreground ordering. Do not trap the player, obscure the head incorrectly or allow walking over solid object bases.
- Verify suitable water, smoke, fire or lighting motion in-engine where the theme calls for it. Do not advertise static art as animation.
- Before requesting more manual review, supply exact-build evidence of the intended functions and list unresolved limitations. The user stopped manual testing after basic requirements were missed; admitted-cell route counts or approach sweeps alone do not satisfy this gate.

**Preserved current versions:** N39 stays unchanged for the demo, with no iteration or smoke retrofit; N40 keeps its current demo URL/runtime; N41 retains its approved art/layout/collision; N48 stays as-is as a scale/quality/flow reference. Future standards do not revoke these specific decisions or authorize immediate redesigns.

<a id="n21"></a>
## N21-r2 · Vienna Pattern Atelier

[Revision card](n-learning.md#n21)

**User decision:** design liked; quality and functional completeness fail review. Pixelation, scale, excessive boundaries and an incomplete experience remain concerns.

**Source inspection:** runtime atlas pixels exactly match the generated master plus specified chair composites, so packing introduces no pixel loss. This does not dismiss source-art detail or live presentation complaints. Native 32-pixel tiles, a 1536 × 1024 world and wokaScale=1 do not prove appropriate perceived scale. Only 319 of 1,536 cells are open; this is not a defect percentage because the remainder includes intended scenery. Collision uses whole-cell 62% floor coverage plus explicit blocks, so intended visible floor still needs independent comparison. Both WAM zones have empty properties and no services are configured. The separate furniture-approach candidate changes only four cells, (10–13, 16); remaining desk geometry and the broader complaints are outside that change.

Preserve the liked design and original artifact. Validate source detail and in-game scale, visible floor versus collision, usable spaces and actual purpose before closing the findings. Collection identity: **N21-r2-runtime**, `map32/map.tmj`, SHA-256 `d157119f542265ca0d74a2cf913ee53011af125ad61e8e2321f7cb7ba72d54a5`.

<a id="n34"></a>
## N34-r2 · Harbour Language Exchange Lab

[Revision card](n-learning.md#n34)

**User decision:** direction liked; the map is “pretty cool.” Animated water and an explorable continuation beyond the top are future ideas. Preserve the current artifact; any later expansion should be separately identified, actually accessible and motion-tested. This is not full gameplay acceptance or authorization for an immediate expansion.

Collection identity: **N34-r2-runtime**, `map32/map.tmj`, SHA-256 `2273fef40efbcc3c323305067bc32e1c832fb307c32d058470d36444ec699bcc`. Harbor Tongues Exchange (N07) is a different map.

<a id="n38"></a>
## N38-r2 · Rainforest Canopy Forum

[Revision card](n-exploration.md#n38)

**User decision:** liked direction with a failed functional review: unusable benches, missing animation, usability and scale problems. Keep the original and liked concept. A furniture approach alone does not establish sitting, exit behavior or completed functionality.

Collection identity: `rainforest-canopy-forum.tmj`, SHA-256 `24920afcf88375c0340a09740400a7cc023a66375b66ed7fe93c301f4d7d269a`. This lookup does not establish the exact user-tested session/engine or a completed source inspection. Those remain unresolved; no source fix or live retest is claimed.

<a id="n39"></a>
## N39-r3 · Volcanic Observatory Lodge

[Revision card](n-exploration.md#n39) · [Preserved demo map file](https://bawes-universe.github.io/universe-maps/recovered/2026-10-13-collection-v1/N39-r3-runtime/volcanic-observatory-lodge.tmj)

**Explicit user decision: perfect; no change, no iteration; keep as-is for the demo.** Preserve the current runtime and URL. Do not retrofit smoke or other motion into this version. This approval is the user's review decision, not an independently observed technical sweep.

A larger, separate same-theme map with different spaces and animated fire, smoke and lights is a future concept only. Accessible seating and verified approach/sit/exit apply to future usable benches; they do not reverse the current no-change decision.

Collection identity: **N39-r3-runtime**, `volcanic-observatory-lodge.tmj`, SHA-256 `ac6f097436f2106cd70cf6375f1f22e5422dac279d07ae3b753a21586340f5eb`.

<a id="n40"></a>
## N40-r3 · Coral Research Pier

[Revision card](n-exploration.md#n40) · [Preserved demo map file](https://bawes-universe.github.io/universe-maps/recovered/2026-10-13-collection-v1/N40-r3-runtime/coral-research-pier.tmj)

**Explicit user decision: keep the current map where it is for the demo.** Preserve its URL and runtime unchanged. The concept is liked, while odd scale and tiny unusable benches remain reported limitations; demo preservation is not full gameplay acceptance.

A future, separate version may retain the concept while improving scale, animated water and functional spaces. Do not replace the current demo with that revision implicitly. Collection identity: **N40-r3-runtime**, `coral-research-pier.tmj`, SHA-256 `e3b5e44c8b43bf8e5b3f66dce642eade6738dfe78a296ff2df24d2a89fbdb1d9`.

<a id="n41"></a>
## N41-r3 · Moonlit Ruin Courtyard

[Revision card](n-exploration.md#n41)

**User approval: appearance and usability.** The user called the map perfect, beautiful and functional. Preserve its approved artwork, layout and collision. Only subtle waterfall/water motion was identified as a future improvement; any such change needs exact-build motion and nonregression checks and must remain narrowly scoped.

This user approval does not prove every common or multiplayer check, and it cannot transfer to a different revision. Collection identity: **N41-r3-runtime**, `moonlit-ruin-courtyard.tmj`, SHA-256 `933915f23172c9bebcf4f962e32e32e356ea974edd4202d1b849cb7ef9d9d168`.

<a id="n42"></a>
## N42-r4 · Sky Village Airship Terminal

[Revision card](n-exploration.md#n42)

**User report:** beautiful artwork, but benches are not sittable, the left-side approach is blocked, the avatar appears over trees and lights appear beneath the avatar. Three user screenshots show canopy/lamp overlap. Preserve the liked art and layout while recording the function/depth failures.

**Completed source inspection:** no authored seat/sit behavior; four solid bench rectangles. Canopies and lamp artwork are ground-layer content. The remaining 22 foreground tiles cover three building details, and the compiler strips foreground at reachable avatar-head positions, explaining the overhead-depth problem. These are source/runtime findings, not a new live retest. The separate furniture-approach pass leaves N42 unchanged and does not establish sitting or repaired depth.

Collection identity: `sky-village-airship-terminal.tmj`, SHA-256 `f5250de920da2f87bdda475018e261380558d8dfe619c456ef02104eb7d1da5e`. Skylot Garden Commons (N14) is a different map.

<a id="n43"></a>
## N43-r1 · Glass Hall Conference Campus

[Revision card](n-exploration.md#n43)

**User report:** overall design and bottom-right VIP area liked; stage seats face right instead of up, an apparent bridge destination has no entrance, seats are unusable, VIP access is unclear, a top bridge allows walking over trees, and fountains/water are static.

**Source inspection:** 18 anchors reuse Reading chairs, but the runtime has no seat/sit/facing behavior and source records explicitly say no sitting. The long bridge ends at a blocked VIP west wall; the actual southern entry at (1280, 752) is reached through the bottom loop. Connectivity of all 453 walkable cells does not establish clear access. Foliage is ground-only without foreground occlusion. The far-right waterfall bridge at (1456, 336) is blocked; the exact tiny bridge reported by the user remains uncertain and must not be equated with it. Water is static.

The separate rear-chair patch passes 18 approach sweeps only; it does not resolve sitting/orientation, VIP legibility, bridge/tree depth or motion. Prove those functions on an exact revised build before requesting another manual review. Collection TMJ: `glass-hall-conference-campus.tmj`, SHA-256 `48886ff4aa1541910a61a26c6636474c1fe468a414c8d11aaacbf41472608dba`.

<a id="n45"></a>
## N45-r2 · Desert Esports Pavilion

[Revision card](n-exploration.md#n45)

**User report: failed gameplay.** The player walks over objects; scale, positioning, furniture and layout do not fit or function as intended. The inspected current candidate is N45-r2, while the exact user-tested session/build remains unresolved.

**Source inspection:** 967 blocked and 569 walkable cells; bleacher collision ends at y=608 while visible seating extends below it. Three reachable 16 × 16 avatar-foot rectangles on the seating have no blocking collision, supporting the report. Native 32-pixel tiles and wokaScale=1 do not establish correct proportions. Chairs/consoles are scenic, without individual seat anchors; eight general approach anchors do not make each fixture functional.

Preserve the artifact and failure report. Verify object-base collision, foreground depth, scale, useful approaches and the intended activities on an identified build. No collision fix, redesign or live acceptance is established by this inspection.

<a id="n47"></a>
## N47-r3 · Winter Lantern Festival

[Revision card](n-exploration.md#n47)

**Authoritative later user decision: REJECT.** The user describes the map as terrible, isometric, nonfunctional and inconsistent with the guidelines. This supersedes the historical Current candidate role as a review decision. Do not recommend or promote this version as accepted.

Retain the original source/runtime and prior feedback as historical evidence; rejection is not a deletion request. Source-defined spatial layout and a quiet-zone property do not prove a functioning experience. Named areas are empty setup placeholders, and no quest script is supplied. These source facts are separate from the user's quality/function rejection and are not independent live testing.

Collection identity: **N47-r3-runtime**, `winter-lantern-festival.tmj`, SHA-256 `6f93d4f1b1f5d32d922c2e0bf57a8f13149b18f9acea084463da129aab2f7700`. Its recovered artifact remains part of the 80 file packages previously checked for static availability/integrity; the rejection changes no recovery count. N47 is outside the separate 28-map furniture proposal. The governing future direction is [quality over quantity](#future-standards).

<a id="n48"></a>
## N48-r1 · Acoustic Cave Hall

[Revision card](n-exploration.md#n48) · [Preserved reference map file](https://bawes-universe.github.io/universe-maps/recovered/2026-10-13-collection-v1/N48-r1-runtime/acoustic-cave-hall.tmj)

**Explicit user decision: keep as-is as a reference for future work.** Scale, quality and seamless flow are user-approved and described as mostly perfect. Preserve the current URL/runtime; do not retrofit animation or sittable benches as part of a generic improvement pass. Their absence remains an acknowledged limitation.

N48 is absent from the reviewed 22-map manifest, additional five-map manifest and separate café candidate, so it is outside the assembled 28-map furniture proposal. Keep it excluded unless the user explicitly changes the preservation decision. It can inform quality/scale/flow without imposing the same art style on future maps. This user approval does not invent independent live QA, actual sitting or animated scenery.

Collection identity: **N48-r1-runtime**, `acoustic-cave-hall.tmj`, SHA-256 `73f18ebf500aef88826eb06f59c2b374ff3765af5993dce60ac7684ffb4fd579`.
