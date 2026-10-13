# H039 recovery boundary after two new-art attempts

## Result

Both newly generated mill exteriors fail registration to the retained original
geometry. Neither is an exact restoration. Keep them as preserved reconstruction
experiments, not accepted map runtime assets.

The second image changes 99.972598% of pixels, but its important surfaces remain
near the first image's positions. Approximate r1-to-r2 center changes are only
0–2px for tray papers, bridge and hanging papers; the doorway sill changes about
12px down. The remaining required corrections are roughly 82–113px south for
most surfaces, with separate horizontal and size errors. Exact target bounds and
manual measured bounds are in `comparison.json`.

The retained walkable band still crosses drawn trays; wet-paper overlays land on
aprons/ground; the expected deck reaches rail/support and river; the expected door
remains in the courtyard; stool contacts and floor corridors cross plants.
Repeated coordinate-edit generation has been ineffective in these two attempts.
This is evidence about these attempts, not proof that all future methods must fail.

## Exact restoration is still blocked by original assets

The user's requirement is to rebuild exactly what existed. An art-aligned changed
layout cannot satisfy that requirement by itself, even if its gameplay is similar.

The four original H039 final masters are still missing:

1. `art/masters/mill-r5.png`
2. `art/masters/pattern-room-r1.png`
3. `art/masters/stools-r1.png`
4. `art/masters/patterns-r1.png`

Original controller mechanics and declared geometry survive; the final controller
runtime matches its historical hash. Preserved prompts and output UUIDs do not
recover those four PNGs. The two new exterior candidates do not change the count
of missing original artwork. Exact restoration still requires those bytes, an
authentic equivalent final raster/runtime source, or supported recovery that
provides enough original information to reproduce and verify the old output.

The historical TMJ target remains
`25cb99347eb63e8c535215b12c2a01d23784254bf430ff2f4019ec2763d2b240`.
No new-art rebuild can be assumed to match it.

## Alternative requiring an explicit decision

**Proposal only:** build a separately named, newly authored functional
reconstruction around one chosen new exterior image, while preserving all
original files, geometry, scripts, hashes and failed candidates unchanged.
This trades exact visual/layout restoration for the same core interaction
mechanics. Do not implement this alternative without an explicit decision to
accept that changed scope.

### Concrete work if that alternative is chosen

1. Pick the candidate and native rendering scale explicitly. Record its exact
   bytes and transform in a new design package; never relabel it `mill-r5`.
2. Trace its actual visible floor, complete tray bases/feet, bridge rails/posts,
   walls, vegetation frontiers and rack supports. Build a new declared geometry
   contract from those traced pixels. Do not reuse the old collision blindly or
   put generic blocking margins over clear floor.
3. Move exterior interaction anchors and door approaches to actual clear body
   origins beside the pictured fixtures. Preserve semantic IDs: `journal`,
   `swirl`, `rake`, `rack`, `enter`; keep the interior `comb`, `inspect`, `exit`
   contract. Route-only anchors and seat contacts also need new measured positions.
4. Re-register wet-paper overlays to both actual tray interiors and printed-sheet
   overlays to the actual hanging papers, using complete transparent sprites.
   Recompute fixed-solid containment, rather than pasting rectangles over legs.
5. Supply a coherent entered pattern-room master, two complete low stool sprites,
   and eight genuinely distinct marbling samples. These three new master groups
   do not currently exist. Preserve the two-region door contract and stool contact
   capability; do not replace the room with a generic placeholder or silently
   relocate Comb to an outdoor station.
6. Reuse the retained controller source body unchanged if possible. Build a new
   layout prefix and runtime under a new reconstruction identity. Changed anchors
   necessarily change the whole emitted script hash; that is expected and must
   not be described as the historical `96cc...` runtime.
7. Verify the entire new source-only build, real TMJ/atlas decoding, all displayed
   pattern states, native routes and live input/rendering before acceptance.

### First feasibility gate: physical scale and clear floor

At the former 0.75 scale, r2's observed clear bridge deck is approximately
54px deep. It therefore cannot honestly inherit the original 64px clear-deck
claim; strict 32px collision cells may retain only one completely clear row.
Other narrow floor strips need actual tracing and click-fit tests before a
functional-grid claim is possible.

Using the full 1536x1024 image at native scale instead of downsampling gives an
approximately 72px-deep bridge deck, potentially enough for a 64px corridor after
grid registration. This is a proposal to change scene scale/world dimensions,
not an implemented fix or a proven connected layout. Actor scale, fixture size,
room size and global tile alignment would all need review. Neither scaling choice
may silently waive the original movement/visual requirements.

### Required gameplay parity

- Three explicit tools remain: Swirl bit 1, Rake bit 2, Comb bit 4. Each pass may
  be added only once per wet sheet; order deliberately commutes.
- Every wet subset 0–7 and independently copied print subset 0–7 remains
  reachable: 64 combined logical/display states.
- Both outdoor trays and the interior table show the same current wet pattern.
  Both rack papers show the copied printed pattern.
- A nonblank print is created/completed only by explicit Lift and hang. Later
  passes change only the wet sheet. Fresh wet sheet preserves the hanging print.
- Door travel both ways preserves both patterns. Reload starts a fresh visit;
  state remains local per visitor, without invented shared persistence or audio.
- Reset requires confirmation and clears both patterns. Close, guide, proximity
  and pause do not mutate the work. Stale callbacks cannot supersede newer intent.
- Layer changes wait for actual idle and settled doorway travel. Preserve late
  initialization, failed/retried transitions, movement supersession and disposal
  safeguards in the existing controller.
- Keep native 32px actors/16x16 bodies and explicit honest standing stool contact.
  No automatic sitting/facing claim may be introduced.
- Arrival silence remains tightly scoped to the true new arrival; it must not
  silently cover the workspace or seats.

### Acceptance checklist for an approved functional reconstruction

- Original evidence immutable; new identity and old/new comparison explicit
- Missing room/stool/pattern assets supplied and provenance recorded
- Whole visible-floor inventory and grounded-fixture masks independently reviewed
- Every admitted cell and fitting extreme routed with full-body continuous checks
- Real doorway/spawn/return targets, failed transitions and stale interactions tested
- All 64 physical visual states distinct where intended; alpha and overlay bounds valid
- No head/foreground clipping; complete opaque ground beneath foreground pixels
- Deterministic clean build plus TMJ/atlas round-trip equality
- Actual keyboard, pointer/touch, rendering-scale and multiplayer-local-state review

The retained 14 passing controller checks can be reused, but the missing physical
state test remains blocked until real replacement assets and runtime are built.
Historical PASS never transfers to new art or changed geometry.

## What this assessment changed

Only small evidence files were created. No original or candidate image, geometry,
controller or runtime was modified. No new image generation or paid call occurred.
No functional reconstruction implementation started.
