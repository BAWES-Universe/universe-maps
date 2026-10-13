# C: expanded building visual study

This is the full visual-source continuation of the approved south entrance. It is not a compiled or published map. The accepted A hall, stage, meeting bays, foyer and original32px Greg remain exact. Frozen B supplies the finished outdoor stone/timber and pavilion composition, including its four table collision cells and two8px anchor adjustments. The entrance approved in the parent directory is frozen unchanged by `../ENTRANCE-FREEZE.json`.

## Review order

1. `review/full-context-outside-revealed.png`: exterior and interior reveal side by side, clearly labeled50% overview scale.
2. `review/south-approach-sequence-native.png`: new frontage outside, approach reveal, and player inside, all1:1.
3. `review/hall-east-approach-sequence-native.png` and `review/foyer-east-approach-sequence-native.png`: both covered side-wall connections in full-shell context, all1:1.
4. `viewport-audit/source-calculated-recommended-outside-desktop-labeled.png` and the matching portrait file: normal camera at the proposed spawn, not browser screenshots.
5. `viewport-audit/source-calculated-entry-reveal-boundary-*-labeled.png`: the actual revealed composition at the proposed trigger.

Individual native crops and full native outside/revealed images are also in `review/`. No actors are baked into the source layers.

## What changed visually

- A tall main-hall roof has a raised north/south central ridge, separate pitched side fields, restrained brass eaves, coherent shingle directions and directional light.
- A lower, broad foyer roof has a horizontal ridge and four pitched planes. Its initial shallow north slope was re-authored with more original-size shingle rows. A competing front roof gable was then removed so the approved door pediment remains the entrance's single focal point.
- The south façade now continues across the full building with native window/pier modules. The hall front face sits visibly taller behind the lower foyer roof. Windows and piers repeat at original derived sizes, with complete piers covering their integer-aligned seams.
- Both east entrances use one newly authored side-wall/covered-porch module at two translated positions. It is genuinely edge-on in this orthographic projection. No front-facing door has been pasted onto a side wall or into a roof slope; no floor rectangle is inserted beneath a canopy.
- The new world margins use a calm generated ground material and native edge continuations. The garden and terrace inside the translated source rectangle are now pixel-exact frozen B. The new margin material is a source-study extension outside that source rectangle.

The source does not contain v06 stretched roofs, front faces or side entrances.

## Scale and geometry

`geometry-contract.json` is the exact handoff. World size is2816×2432px, or88×76 tiles. All frozen B source art and collision coordinates translate by(+128,+256), exactly(+4,+8) tiles. The accepted body remains approximately1536×1728 before translation; the original arrival opening extends to sourcey1776.

The generated roof masters actually returned1536×1024px. Both final roofs are used at exactly that original size, with alpha extraction only. They are not enlarged to the dimensions requested in the prompt. The hall roof is placed at(128,96), the foyer roof at(128,1072). Their pitched silhouettes and facade overlaps establish building depth without deforming either image.

The south entrance remains640×320 at(576,1762), with exact5/12 uniform reduction from its1536×768 master crop. The south window/pier modules use the same5/12 reduction; the higher hall's window/pier modules use uniform1/2 reduction to create a deliberately taller architectural face. The two side porches remain240×360, exactly15/64 on both axes. No furniture, interior, actor, roof strip, ornament, wall segment or garden asset is anisotropically scaled.

- South threshold: y2032; exterior visual aperture x832..960,128px
- Existing south opening and collision width: x768..1024,256px
- Hall east wall threshold: x1664, y704..800,96px visual span
- Foyer east wall threshold: x1664, y1600..1696,96px visual span
- Foyer's existing source collision opening remains y1568..1728,160px; it is not narrowed to the visual span
- Side-porch origins: hall(1600,488), foyer(1600,1384)
- Proposed spawn center: (896,2176), facing north

The side canopy projects to the east beyond the main wall; its furthest structural pixel is x1775. North support feet are naturally hidden in the closed orthographic projection. Their registration is an explicit source-geometry inference in `side-porch/module-manifest.json`, not a claim of live collision acceptance.

## Added exterior floor and unchanged collision

Neither A nor B's collision grid is edited or saved as a new runtime grid. The geometry validator copies frozen B in memory with the same(+4,+8)-tile translation and checks source identity. Relative to A, it retains only B's four approved pavilion table cells; the two changed social anchors are documented in the geometry contract. The spawn16px body uses x±8 and y..y+16, with exact box[888,2176,904,2192].

The only proposed additional walkable region is the south path `(768,2176)-(1024,2432)`:256×256px, exactly64 new32px cells, tile rectangle `(24,68)-(32,76)`. The native A path material continues into this region without changing width. The actual spawn's16×16 body and entire32×32 frame have clear floor across the old/new boundary. Other added world cells are blocked by default until separately designed and tested.

The three entrance aprons and safe source routes are explicit in the geometry contract. In-memory checks sampled39 south and45 points for each east route; both16px bodies and32px frame rectangles were clear at all samples. This is source geometry only. Runtime key movement, click-to-move and route perception still need validation.

The128px front portal and96px side visual spans do not create new invisible collision throats. After reveal, A's original openings remain exactly as broad as they were.

## Reveal, restoration and ownership

`layer-ownership.json` and `semantic-shell-contract.json` define independent hall and foyer owners and six world-sized decorative exports:

1. `assets/hall-shadow.png`: below actors; hidden by hall-open
2. `assets/foyer-shadow.png`: below actors; hidden by foyer-open
3. `assets/hall-shell.png`: above actors; hall front face, roof and east porch; hidden by hall-open
4. `assets/foyer-wings.png`: above hall-shell but below foyer-roof; hidden by foyer-open
5. `assets/foyer-roof.png`: above wings and below front; hidden when either hall or foyer is open
6. `assets/foyer-front.png`: approved entrance/pediment and foyer porch, last draw slot; hidden by foyer-open

The six-group recomposition is pixel-exact with the approved full shell. South wings and entry cannot be flattened into the same draw slot: wings overlap the roof at28,740 native alpha pixels and must precede it, while the entry follows it. No arbitrary world-coordinate slice is used. Original semantic modules determine ownership.

The entire foyer roof, beginning at worldy1154, overlaps28,781 alpha pixels of the accepted hall floor within[170,1154,1625,1200]. Thus hall-open hides that complete roof module too, even if the foyer façade has restored. Both shadow groups are only ground/contact shadows and have no foreign-roof dependency. Base, B interior-above, collision and the eventual quiet receiver remain permanent. The4px flush threshold strip is below actors and is not collision.

Hall entry core is[128,256,1664,1344], with hold[96,224,1696,1376], plus its east apron. The hall front's last alpha row is1290; hall entryy1344 puts the full32px frame top aty1328, leaving37px margin. Hall shadow endsy1304 and is below actors. Foyer core is[128,1280,1664,2032], plus the south and foyer-east aprons; each hold is expanded32px. The overlapping cores support stable foyer/hall transitions.

The agreed outside triggers are unchanged:
- South entry center y2112,80px before its threshold;41px full-frame margin to all façade alpha
- Both east entries center x1832;40px full-frame margin beyond porch alpha
- Reverse restoration immediately beyond y2144 south or x1864 east, after leaving the relevant hold union

Boundaries are inclusive. Initialize each owner independently from its entry regions before the first visible frame. Visibility is instant; no partial-alpha fade is asserted head-safe. `validation/semantic-reveal-proof.json` tests1px entry/reverse-exit sweeps and a foyer-to-hall round trip, with zero visible-shell/full32px-frame intersections.

Shell owners and hall camera focus are independent. The accepted native hall focus translates with the interior. Outdoor behavior remains ordinary follow/manual zoom; no exterior camera state is introduced.

## Default-camera evidence and accepted limit

The pinned source camera/scale fixture was executed in `viewport-audit/`. Desktop1440×900 uses2 CSS px/world px, while portrait390×844 uses1. At spawn(896,2176), desktop crops173px from the entrance's upper alpha envelope. Portrait fits the full entrance height but crops the outer wings. At the closer outside pointy2160, desktop still crops157px from the top.

The actual rendered default views show Greg, the full256px approach, the clear128px door route, threshold and lower jambs legibly in both sizes. That supports retaining ordinary follow. The tall building is not expected to fit completely at default zoom. The y2112 boundary proofs use the fully revealed composition and show A's unchanged broad passage. These are source-calculated previews with explicit labels, not browser screenshots, phone testing, or authenticated gameplay evidence.

## Sole spawn quiet receiver proposal

No audio configuration is edited. The parent runtime plan should replace A's old quiet receiver with exactly one16-cell receiver centered on the actual new spawn: pixel rectangle `(832,2112)-(960,2240)`, tile rectangle `(26,66)-(30,70)`. Do not retain the translated old receiver and add another. Exact old and new receiver bounds are in `geometry-contract.json`. Hall, foyer, terrace and routes remain outside any additional quiet zone.

## Evidence, provenance and remaining work

- `validation/source-invariants.json`: hall, full accepted foyer and garden are pixel-identical in the revealed composition.
- `validation/geometry-proof.json`: exact translated frozen B grid, explicit64-cell extension, body/frame routes and all three head margins.
- `validation/semantic-reveal-proof.json`: pure independent-owner coordinate model; no controller is installed. The prior single-shell proof files are explicitly superseded.
- `viewport-audit/`: pinned camera math, actual input hashes and labeled source views.
- `geometry-contract.json`: full module crops, ratios, origins, source hashes, walkability and future quiet receiver proposal.
- `layer-ownership.json`: exact assets, masks and visibility ownership.
- `masters/`, `prompts/`, and `side-porch/masters/`: original built-in imagegen outputs and prompts, including rejected/iterated studies.

Rebuild with `python tools/assemble_full_shell.py`, `python tools/validate_geometry.py`, `python tools/export_semantic_groups.py`, then `python tools/render_review_cards.py`. Dependencies are Pillow, NumPy and SciPy. The scripts prefer the bundled `../../source/frozen-b` flat inputs, falling back to the existing `source-b-frozen` snapshot, and verify each input against its frozen hash. They read the approved entrance assets/masters in this same C tree and write only this full-study directory. No sibling A/B project or old v06 viewport fixture is required. The original A comparison and A-to-B deltas are archived in `tools/historical-a-comparison.json`; regeneration carries them forward only after the new base/above bytes match the exact frozen outputs covered by that historical proof. It does not perform a fresh A comparison. The exact DejaVu Sans review fonts and installed license are bundled under `tools/fonts/` as build-only resources, not generated artwork or runtime dependencies. `source-b-frozen/SNAPSHOT.json` records verified B source hashes; `b-animation-placement-translated.json` and the native leaf atlas preserve B's animation source for the parent's compiler. No TMJ/WAM compile, collision/audio/controller change, engine edit, authenticated room test, GitHub publication, Library publication or B file change was performed.

Final source-only update: finished B materials and pavilion are integrated; six semantic shell exports are ready. No A/B files, runtime grid, quiet configuration, controller, camera implementation or publication was changed.

## Portable regeneration and camera evidence

Run the four art commands above from `C/source-prototype/full-study`. All project inputs and review fonts are inside the bundled C tree; Python, Pillow, NumPy and SciPy remain toolchain prerequisites. `STANDALONE-SOURCE-NOTES.json` lists the input resolution and evidence boundary. Art generation never invokes the viewport scripts.

`viewport-audit/` remains historical, labeled source-calculated study evidence. Its original rebuild scripts are outside this portable command set. The bundled final source-camera proof is `../../validation/focus/` (source files, audit script, source manifest and results), owned by the runtime compilation workflow. That proof replaces any need for the old v06 fixture in final validation. Neither proof is an authenticated gameplay test.

`tools/PORTABILITY-REGENERATION-PROOF.json` records the isolated clean-output run: all four commands passed, all 80 regenerated PNGs match the original freeze byte-for-byte, and the geometry contract matches byte-for-byte. The live art and geometry were not regenerated. The archived `review/hall-roof-inspection.png` is outside this four-command output set.
