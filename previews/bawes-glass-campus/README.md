# BAWES campus — illustrated brand-reset alternative

This isolated candidate preserves the BAWES folded-glass tower, outdoor spawn, full-footprint interiors, shared campus uses and door/meeting-lock behavior. The owner rejected the atlas-heavy artwork at `579875d` and the wood/gold/realistic-furniture section at `0d835f4`. Both remain recoverable in Git history.

The current work is a **representative alternative**, confined to the tower shell and lower interior/arrival section at world x320–1088, y1280–1856. It uses newly authored illustrated stone/glass scenery, broad violet/blue seats, compact tables, curved floor mosaics and planted edges. It is not a completed or owner-approved campus. The surrounding old artwork and study boundaries remain visible; campus-wide propagation is paused for visual review.

## Sources and interpretation

[source/brand_reset/REVIEW.md](source/brand_reset/REVIEW.md) distinguishes verified product colors/logo guidance, inspected early-campus artwork, the owner's constraints and proposed design interpretation. Current Universe/Orbit code specifies neutral ink surfaces and selective violet–blue accents; it does not prescribe wood, gold, realistic furniture or a map-material bible. The assistant-generated UI design-kit ZIP is not treated as approved map art.

Retained generation sources and native registration code are in `source/brand_reset/`. Earlier sources and provenance remain as history. Selected WA Village atlases still exist in the unreworked portions under the previously reported project-specific partnership permission; they do not set this alternative's art direction.

## Functional scope and evidence

- Persistent collision cells and the runtime door/lock script are identical to `0d835f4`; six-tile entrances and four full-footprint cutaways remain intact.
- Static checks: 6,396 connected walkable cells and 88 reachable seat cells. This does not visually certify every seat.
- `source/validation/brand-seating.cjs` exercises actual desktop **right-click** and touch-tap approach/exit. This pinned Universe build uses right-click to walk; the first invalid left-click attempt is documented. Final run: 6/6 checks pass, including measured keyboard movement and the inside cutaway. Screenshots and results are in `review/brand-*`.
- Chair foreground strips were reduced to preserve torso visibility. No new sitting-pose engine mechanic is claimed: the Woka stands at the authored chair anchor with controlled visual overlap.
- The prior 10-check shared-door suite belongs to `0d835f4`; unchanged collision/script hashes are recorded in `review/brand-inputs.json`. It is not represented as a fresh full-suite run on this artwork.
- Repository build passes 11/11 maps. Static and mocked reveal checks remain separate from visual acceptance.

`review/brand-seat-desktop.png`, `brand-team-interior.png` and `brand-outside-occupied.png` are actual normal-scale local-game captures. `brand-section-native.png` is an offline art-layer export. Historical `redesign-*`, `polished-*` and `town-*` evidence describes previous iterations and cannot establish acceptance of this one.

Build here with `python3 source/build.py`; validate with `python3 source/validate.py` and `node source/test-reveal.cjs`. Run repository `npm run build` without deployment. Local engine setup is in `source/runtime/README.md`, pinned to `274114560c5ec95fdf8e51e67986a53069f3cf06`.

Six portal destinations remain unbound. No walking popups, quests, background audio or baked text/signage. Work remains under `previews/bawes-glass-campus/` on draft PR #21. No existing-map, Azure or tracked-engine changes, merge, deployment or world registration.
