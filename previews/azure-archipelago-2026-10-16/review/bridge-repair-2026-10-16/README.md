> Bridge paving in this revision was rejected in visual review. See [revision2](../bridge-repair-v2-2026-10-16/README.md). The canopy change is retained.

# Azure bridge and canopy repair — 2026-10-16

Base: `d0d9a80b4fbbbeac83e431493914524abc5fb424`. Saved only on `preview/azure-archipelago-2026-10-16`; no deployment or merge. No Moonlit edits.

## Change

Bridges and viewing bays now use the same world-aligned128px limestone slabs. The bridge atlas supplies outer rails only; the bay atlas supplies its rails and chairs over the shared floor. This removes the competing floor scales, rotated floor patterns and discontinuous baked shadows at bridge/bay joints. Thin inlays define transitions to the preserved island paving. Hub landings stop at the existing mosaic border. Island materials remain visibly distinct; this does not claim identical stone artwork across every island.

Removed the lounge canopy's interior lattice and full-area tint. A muted perimeter remains, with the existing entry/exit cutaway. Canopy draw tiles fell from320 to68.

All four canonical island PNGs, hub and bridge PNGs, geometry,55 seat definitions,17 table definitions, controller,water atlases,sea texture and sound remain byte-identical to the base. See preservation.json. Collision remains3589 connected cells. No changes to engine, camera, Woka scale or audio behavior.

## Actual-game validation

Used the running WorkAdventure stack in the selected cloud workspace, via native browser UI, right-click navigation and keyboard physics. This is author validation, not a new independent review or live owner-session test. No additional agents or broad map audit were used.

- All16 edge-lane crossings at eight mouths passed native right-click approach/crossing and keyboard return. First sweep navigated between mouths; final targeted sweep positioned the player near each test start and used real mouse/keyboard crossings.
- All eight bay seats and three representative lounge seats passed the actual native Take nearest seat menu, exact target occupancy and keyboard exit. Eleven seat screenshots are included. The rear lounge chair has only19px of backward travel before its existing wall; its forward keyboard exit was separately checked in lounge-forward-exit.json. Geometry and all other seat/table definitions are unchanged; no new all55-seat/all17-table test is claimed.
- Eight bridge/bay outward keyboard pushes stopped at existing rail boundaries.
- Both lounge openings retained outside/inside/outside canopy visibility true/false/true.
- Eleven matched before/after views show the avatar visible with native scale/zoom1 and zero sampled map popups.
- Final hub inlay refinement only shortened four visual strips by32px, preserving the mosaic border. Final captures and performance samples use that refinement; hub-final.json records its targeted crossing recheck. No collision/controller/seat changes followed gameplay tests.

## Performance

Matched1366×768 viewport, animated water enabled, forced continuous rendering; one six-second sample per view/version. These are short environment-specific regression samples, not a universal FPS guarantee.

| View | Before FPS | After FPS |
|---|---:|---:|
| Bridge/bay |57.2|57.0|
| Lounge outside |41.8|46.5|
| Lounge inside |40.7|41.1|

p95 frame intervals remained approximately33.3–33.4ms. Existing opaque-tile pruning and cull-safe sea atlas are retained.

## Evidence and limitations

[Before/after captures](captures.md). Raw checks and scripts are in this directory. Runtime SHA-256 manifest identifies the exact tested assets. The final tested Git commit is the commit containing this report and manifest.

The three supplied Library references resolved but their supported downloads failed with `library file transfer failed: download failed`; no image bytes were saved or visually inspected: `libfile_bdf5bbcdf2f88191a845743da0cb671b`, `libfile_f3980f1fb1f48191893ba669a403bb23`, `libfile_229b1347e2d481919eb8b21951dc467a`. Work proceeded from independently captured base gameplay, with its saved baseline verified against d0d9a80.

Preview-branch candidate only. Existing published preview is unchanged. Native upright seat occupancy and existing water/audio limitations remain as documented in the prior acceptance report.
