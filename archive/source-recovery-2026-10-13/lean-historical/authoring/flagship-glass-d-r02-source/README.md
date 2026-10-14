# Flagship Glass D r02 - isolated native32 candidate

**Compiled implementation, awaiting independent source QA and final visual review. Not live validated or published.** A/B/C originals are unchanged. The earlier Glass D r01 is visually blocked and is not this candidate.

## What changed
- Lower foyer/terrace use warm pale limestone, restrained perimeter bronze inlay, a compass inset and small seating pads. No raised obstacles are added by these floor decorations.
- Three terrace pairs now use original east/west-facing chair assets, facing one another across small tables. Anchors remain 56px apart. Nine collision cells change for their tables; other geometry stays unchanged.
- Reception uses its original unlettered source counter; coffee uses a generated unlettered sprite. The old TERRACE text becomes a small unlettered inset panel. No newly baked text labels.
- South garden is one generated curved planting composition, split only to preserve the original straight approach. It is not a repeated texture. Northern garden/pavilion remain predecessor composition.
- New see-through glass has alpha18/255 pane fill and low-alpha reflections. A separate alpha18/28 layer above avatars demonstrates real compositing through the panes. Opaque slim front piers/cornice cut away on entry, while the rear clear architectural frame remains. This is a bounded height/cutaway improvement, not proof that all building-design goals are solved.
- Liked portal uses exact original foreground/roof sprites, original placement and scale. Its outside approach stays pixel-exact. The hall/stage base and foreground remain exact through world y1264.

## Doors
The candidate retains open doorways. It does not install the earlier custom shared-state auto-close prototype. That prototype's simultaneous occupancy failures and a static-open fallback are documented separately in `flagship-glass-door-study/shared-occupancy-r2`. Those findings do not assess official Scripting API Extra doors, which were not tested. No Extra package or engine modification is introduced here.

## Verification status
Author static scan: 2,173 connected walkable cells; all262 anchors body/head-clear and reachable; all4,356 conservative spawn placements safe/silent. Every1,881,142 reachable body-clear integer placement passes upper14px head masks for all12 frames of Greg and eight varied original32px Woka sheets. These are deterministic source/static checks, not browser/device acceptance. The low-alpha glass pane overlay's maximum alpha is28; it intentionally tints, rather than hides, pixels behind it.

`validation/chair-depth-conservation.json` proves every nontransparent chair source pixel and all alpha are preserved across below/above depth partitions. Foreground safety was obtained by assigning depth, not erasing chair backs or rails. No stage furniture or meeting-room seat orientation changed.

Independent route/reveal/collision/touch audit remains pending. Native camera limitations inherited from v09 still apply; no new camera behavior is claimed. No live media, multiplayer, deployment or capacity validation was done.

## Entry and rebuild
Serve all siblings in `map32/` together and use `grand-auditorium.tmj` for an isolated test. Companion WAM is unchanged from C; importing Custom TMJ does not automatically apply its meeting/podium/audience setup.

Python3 dependencies: Pillow, NumPy.

1. `python3 tools/assemble_glass_r02.py`
2. `python3 tools/compile_runtime_c.py`
3. `python3 tools/verify_runtime_geometry.py`
4. `python3 tools/verify_varied_geometry.py`
5. `python3 tools/render_varied_preview.py`

All consumed source inputs are bundled. The original source path is consulted only if a required frozen JSON is missing; a complete bundle does not require that path. No code files from the engine are part of this rebuild.

Compiled previews are decoded tilemap compositions with exact native32 Woka sprites, not generated approximations or live screenshots. Concept source `source/masters/direction-r02.png` is separately labeled and is not the compiled map.

## Distribution and optional character fixtures
Eight raw Pipoya sheets are intentionally excluded. Their local provenance remains in source/wokas/WOKA-PROOF.json. The compiled runtime rebuild needs none of them. The existing Greg fixture remains for standard static geometry checks. Composed character proofs are included. To regenerate varied-character previews/checks, obtain the eight named sheets from an authorized WorkAdventure repository at the recorded commit and place them under the recorded woka-proof names. Optional preview/check tools fail clearly until they exist. These two defensive guards are packaging-only changes; the runtime compiler/assembly code is unchanged. FREEZE.json describes the complete local QA freeze; PACKAGING.json lists the distribution exclusions/diffs.
