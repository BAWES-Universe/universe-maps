# Celestial Garden - calmer native32 draft

Separate unpublished draft. Original expanded r4 and the earlier color proposal are preserved. This is new artwork and new map geometry, not a color-only patch and not a reuse of r4 collision certification.

## Changes
- Quieter midnight-indigo sky, restrained waterfall glow, warm cream paving, and concentrated gold/blue portal accents.
- Upper curved walkways and remaining pond-edge bottlenecks widened in the artwork. The lower conifers are kept inside planted beds so their foliage no longer intrudes into traversal.
- Fresh collision grid, physical portal-foot exclusions, five destination areas, natural native standing targets, and safe arrival domain.
- Native 32 px tiles and 32 px avatar frames; 16 x 16 body; scale 1. No engine changes. No furniture or artificial seating was added.
- Foreground contains only fresh foliage-only conifer-crown pixels over genuine paving. No paving is above players. Every admitted body position is checked against the union of the 12 native head silhouettes; dedicated native crossings cover both lower loops in both directions.

## Files and rebuild

`source/calm-master-native.png` is the frozen 2048 x 1536 artwork normalized from the saved generated 4:3 input. Image generation is not required to rebuild.

Python dependencies: Pillow, NumPy, SciPy. Node uses the bundled source-extracted methods and EasyStar 0.4.4. The supplied 96 x 128 Greg test sheet is a QA-only fixture reused unchanged from the user's existing map source; it is not a runtime dependency.

Run from the source package root:

    python tools/explore_floor.py
    python tools/build_calm.py
    node tools/native/route-audit.cjs celestial-transit-garden-calm-draft
    python tools/check_spawn_and_boundaries.py celestial-transit-garden-calm-draft
    python tools/final_proofs.py
    node tools/native/detour-audit.cjs celestial-transit-garden-calm-draft
    python tools/render_crossings.py
    python tools/verify_proof_actors.py

The color-segmented floor mask is an authoring aid only. The final collision grid combines it with explicitly reviewed physical-foot exclusions and boundary corrections. Mathematical route clearance alone is not evidence of actual-art safety; see the independent review bound to the frozen hashes.

`celestial-transit-garden-calm-draft/map32` is the runtime. Copy that complete directory when testing. The five portal destinations remain intentionally unconfigured, matching the template status; no external site, teleport, live meeting service or new publication is enabled.

## Verification scope

Source-native replay uses unchanged pinned methods at 60e7afdc3f96ef32525597cd46bd41175d61a2ef. Tests cover desktop/touch pointers, ordered anchor pairs, destination edge clicks, every traversable tile center and return, 60 Hz movement sampled at intervals no greater than 0.5 px, fixture exclusion, spawn domains, atlas decoding, avatar visibility, and actual portal trigger arrivals.

This is not a live browser/Phaser renderer, keyboard or joystick, real-device, networking, AV, service-integration, or publication acceptance test. Independent actual-art review and source/native tests support the draft; a live-room test is still required before release.

## Intentional world scale

The original r4 runtime is 64 by 48 tiles at 32 px per tile: 2048 by 1536 world pixels, with wokaScale 1. This draft retains those exact world, tile, body and avatar dimensions. The generated 4:3 image was normalized to that established canvas; its 1448 by 1086 storage resolution was not adopted as world units. The ornamental portal structures remain intentionally monumental. User-facing occupied proofs use eight distinct, unmodified repository Wokas recovered byte-exactly from accepted Reading provenance; consistent single-actor boundary/crossing diagnostics are kept separately. Runtime atlases contain no avatars.

## Engine fixture provenance

The pinned TypeScript files and source-extracted JavaScript are copied unchanged from the accepted r4 source package and checked against its manifest. The pin is inherited provenance; no fresh public fetch or authenticated repository checkout was used in this build.
