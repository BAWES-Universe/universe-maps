# Seven missing final masters: exact contracts and usable prompt history

No art was generated. All exact prompt texts and original output locators are
copied unchanged under `retained/H025/art/` and `retained/H039/art/prompts/`.
Their copied hashes are in `retained-inputs.json`. File references below are
relative to `retained/`. The saved output UUIDs are identification evidence, not
downloadable Library IDs or recovered image bytes.

## H025 Desert Star Caravanserai

The world is 1248x2496 (39x78 native 32px tiles). Final build inputs:

| Master | Exact prompt | Final build contract |
|---|---|---|
| `art/masters/courtyard-r3.png` | `H025/art/courtyard-r3-prompt.txt` | Assert 1254x1254; crop top-left 1248x1248; place at (0,0) |
| `art/masters/rooms-r3.png` | `H025/art/rooms-r3-prompt.txt` | Assert 1254x1254; crop top-left 1248x1248; place at (0,1248); all three interiors |
| `art/masters/packed-r1.png` | `H025/art/packed-r1-prompt.txt` | Full size not asserted; use source crop (1066,451,1169,537), 103x86, at the same courtyard coordinates |

The final room/courtyard dimensions are corroborated by the retained historical
README and builder assertion, not current image headers. The initial courtyard
prompt asks for 1536x1536; that request does not override the final 1254-square
contract. Packed-r1's original full dimensions are not independently established.

### What the final edit prompts actually contain

- **Courtyard r3:** preserve architecture, cistern, seats, empty packing bay and
  three doors. Edit only the south arrival into a broad clear sandy apron and
  continuous U-shaped sandstone/boulder boundary. This presupposes a missing
  courtyard image; it is not a whole-scene specification.
- **Rooms r3:** preserve all interiors except the right-room stair. Shorten the
  stair toes to y596, use 80px clear treads x1098..1178, keep top landing
  x1058..1178/y375..416, and clear floor y604..695. It presupposes missing prior
  room art.
- **Packed r1:** preserve all courtyard pixels outside the east packing bay;
  fill two baskets near (1090,490)/(1140,490), add star/arch/crescent seals, keep
  contents no more than 24px above the rim. It requires an accurately registered
  courtyard reference; a standalone basket sheet is not equivalent.

### Foundational descriptions and superseded changes

`courtyard-r1-prompt.txt` gives the complete scene: pale amber desert continuing
to all edges, irregular adobe court, broad south gate, three north buildings,
center-left covered cistern, east packing bay and two woven benches. Exact style:
“Whole coherent finely detailed pixel-art orthographic top-down 3/4 overhead view,
north-up, no isometric diagonal axes.” Sandstone, woven textiles, warm dusk light
and short shadows are explicit. `courtyard-r2-prompt.txt` removes the exterior
stair and lowers south walls to 12px adobe curbs. These raster iterations are not
final build dependencies, but their subject/edits are part of the final intent.

`rooms-r1-prompt.txt` describes three cutaway guest/work rooms: blue-bedding and
wind ribbon at west, red bedding and landmark at center, chart table and east
stairs at right. It references the missing caravanserai's materials/style.
`rooms-r2-prompt.txt` reduces furniture and widens three door thresholds to
160px. Its 64px stair is superseded by r3's 80px stair.

Important divergence: final `author-layout.py` traces arrival-floor polygons down
to y1138, while the r3 prompt describes an apron down to y1000. Exact final
polygons, hard-footprint contours, door anchors, seat contacts and foreground
masks must govern reconstruction alignment. Prompt compliance alone does not
reproduce those traced boundaries.

Final original output filenames, from `H025/evidence/original-art-locators.json`:

- Courtyard: `exec-64e11af3-4c88-497b-be88-c55ad61cfb48.png`
- Rooms: `exec-91489d41-b5ac-4c51-aed1-a6607a8dc3cf.png`
- Packed state: `exec-dc256464-021b-4faf-a56c-0da4b217996f.png`

The locators do not prove the exact attached-reference arguments of each old
image edit, even though the text describes an apparent r1/r2/r3 sequence.

## H039 Paper Marbling Mill

Native world is 1920x768. Input dimensions below are prompt requests only;
the builder does not assert the original image dimensions.

| Master | Exact prompt | Final build contract |
|---|---|---|
| `art/masters/mill-r5.png` | `H039/art/prompts/mill-r5.txt` | Requested 1536x1024; resize entire scene to 1152x768; place at (0,0) |
| `art/masters/pattern-room-r1.png` | `H039/art/prompts/pattern-room-r1.txt` | Requested 1024x1024; resize to 768x768; place at (1152,0) |
| `art/masters/stools-r1.png` | `H039/art/prompts/stools-r1.txt` | Requested transparent 1536x1024; crop two complete stools; resize each to 38x20 |
| `art/masters/patterns-r1.png` | `H039/art/prompts/patterns-r1.txt` | Requested transparent 1536x1024; eight fixed complete-sheet crop boxes |

### Prompt dependencies and intended style

**Mill r5 is a local edit.** Preserve every structure and fixture; clear west-tray
side paving x170..247/y385..650 and lower crosswalk x170..850/y575..685 in a
1536-wide scene. It needs a prior scene. `mill-r1.txt` is the whole-scene basis:
cream limestone mill, terracotta roof, right-attached waterwheel, vertical
millrace, two shallow marbling trays, left-to-right drying bridge, right-bank
rack, woods, restrained sunlight. Its exact style is “crisp detailed painterly
pixel art for a native 32px tall walking character, orthogonal top-down oblique
view (not isometric).”

`mill-r2.txt` corrects bridge width but contains abandoned contradictory
x-coordinate phrases before its explicit final correction. It must not be used
as a standalone clean geometry plan. `mill-r3.txt` straightens the southern
entrance and closes obsolete trails; r4 restores the right-bank landing; r5
clears the final side and lower-yard floor. Their final intent matters, but r1–r4
are not separate current build inputs.

**Pattern-room r1** is a full original-scene description with a missing stylistic
reference: warm cream limestone, honey wood, restrained painterly pixel texture,
complete enclosure, broad gold plank floor, south door, north specimen cabinets,
low beech viewing table and clear circulation on four sides. It is more usable
than a local edit, but exact style equivalence cannot be checked without the old
image. The final measured table and cabinet bounds override a loose assumption
that generated prompt coordinates will match their old counterparts.

**Stools r1** is standalone: two separate low/wide beech stools, transparent
canvas, overhead oblique view, one oval and one subtly rectangular, whole feet
preserved, no outside shadows. Prompt says eventual 38x18; actual final build
uses **38x20**. Exact source crops are (92,330,668,707) and
(923,350,1457,707), placed at native (245,465) and (533,465).

**Patterns r1** is standalone and semantically detailed: rigid 4x2 sheet grid,
transparent padding, cream deckled paper, indigo/ochre/white/teal mineral palette.
Samples are blank; swirl; horizontal rake; swirl+rake; vertical comb;
swirl+comb; rake+comb herringbone; all-three peacock. These distinct physical
forms support the retained three-bit gameplay. Correct generation does not
guarantee historical sample placement inside the fixed crop boxes.

### Exact pattern registration

Source boxes, as (left,top,right,bottom):

- (30,128,373,474), (405,128,750,474), (783,128,1129,474), (1162,129,1510,474)
- (30,536,373,907), (405,536,750,907), (783,536,1129,907), (1162,536,1510,907)

Each wet sample is resized to destination rectangles (x,y,width,height):
(200,339,111,60), (487,339,110,60), (1428,311,212,99).
Each hanging print is placed at (976,243,54,64) and (1040,243,54,64).
Complete paper silhouettes and real alpha are necessary; large enough canvas
dimensions alone would not prove correct crop registration.

Final native geometry includes west tray (184,324,327,429), east tray upper
(471,325,610,416), north bridge rail (688,332,1019,369), south rail
(688,455,1024,499), pattern table (1380,291,1695,473), cabinet
(1228,189,1840,218). Stool actor anchors are (264,463)/(552,463); above-floor
strips are y477..479, x250..277/x538..565. Retained design has the full inventory.

Final output filenames, from
`H039/receipts/original-image-artifact-references.json`:

- Mill: `exec-d7cbe82f-e59b-41aa-ab8b-14c98c8c265b.png`
- Room: `exec-54bc3486-f127-44c2-bbcd-e93c3ed19b58.png`
- Stools: `exec-304cca3f-e05c-412c-b3c9-4cf4db79e9cf.png`
- Patterns: `exec-6600176f-dd1d-4b82-acee-fe9ff85c582a.png`

## Honest reconstruction path

The descriptions plus final design are enough for a **new thematic and structural
reconstruction** preserving the intended subjects and interaction mechanics.
They do not establish original pixels or automatically aligned furniture.

First secure this deterministic checkpoint. Any later artwork pass should use
the complete foundational descriptions and final geometry as explicit constraints,
keep all old evidence, and carry a new reconstruction identity. Verify actual
pixels, crop bounds, alpha, furniture silhouettes and clear floor before reusing
collision. Re-measure mismatched source contours instead of presenting invisible
walls or walk-through furniture as faithful recovery. Rebuild actual TMJ/atlases,
verify unique physical state displays and round-trip decoding, then perform
native full-body routes, spawn/transition checks and live rendering/input review.
No historical visual, map hash or acceptance status transfers to newly generated
artwork.
