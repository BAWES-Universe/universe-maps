# Butterfly Gate: experiential revision

A separate local review candidate built on the completed light-interior Butterfly Campus. The original gate painting, Greg avatar, campus rooms, furniture, collision footprints and destinations remain intact. No published map or engine was edited.

## What changed

- The approach now pulls out once to reveal the full monumental gate and a tiny Greg, then eases back into the player's original zoom for the close approach.
- Seven gold/aqua butterflies follow staggered 7.2-second flights up the long staircase, with flutter, trails and brighter convergence near the portal. New restrained aperture shimmer/ripples and amber lantern pulses accompany the waterfalls.
- The threshold briefly gathers light, fades through midnight blue, and reveals the town. Stepping away during the charge cancels entry. These are native map layers, not an engine fade API.
- Town arrival is on the existing clear paving south of the fountain, bringing water, greenery and the surrounding campus into the initial view.
- The same-map return arch still leads back to the gate. Campus interiors remain light and all previously built activity zones remain available.

## Usability

Player controls remain active. The script owns exactly one camera focus per approach; it restores the saved zoom on close approach, retreat, transit, reduced-motion change or cleanup. Reduced motion skips the cinematic camera/fade and hides moving effects while preserving the painted gate and static water. No audio or soundtrack is activated.

The map content is translated exactly 1,024 world pixels right, with finite midnight-blue camera space around the gate. World dimensions are now 5,120 × 3,328, still a 32px grid. Geometry within every room is unchanged; this is presentation padding, not an extra district. Authoritative areas, audio geometry and staged integration coordinates follow the translation.

## Review evidence

The 25.4-second clip is actual cloud Chromium running Phaser 3.86, the real TMJ tiles/animations/collisions and the map script through a source-verified WA adapter. The camera adapter models contain fitting, map-edge bounds, the single saved zoom slot and focus/follow release. It is not a full Universe session, physical-phone acceptance or proof of live conferencing/bots. Cloud capture averaged approximately 10.8 distinct rendered frames/sec; the MP4 is normalized to30fps, not a claim of deployed performance.

The recorded approach passed reveal, original zoom restoration, transit, cleared departure/transition layers and unchanged collision checks. Portrait390×844, landscape844×390 and live reduced-motion release were checked. See qa/results for the exact scoped reports, including retreat and re-entry at a non-default1.6× zoom.

## Files and use

- map/butterfly-campus.tmj is the complete runtime map. Host the map folder intact only after publication is authorized.
- integration contains translated proposals; native meeting/stage configuration, bots/services, booth links and external portals are still disabled/pending live room setup.
- tools/build_gate_effects.py rebuilds original procedural effects from source-inputs/map/butterfly-campus.tmj.
- tools/compose_stage.py then translates the generated map, prepares finite camera space and veil layers, and updates layout/audio source coordinates.
- node qa/audio-sync-geometry.mjs regenerates the disabled audio geometry and manifest after those two steps.
- map/scripts/campus.js is the editable authored runtime, and qa/harness.js + qa/gate-journey.js are review sources.
- source-inputs preserves the immutable previous map, layout, original gate master and audio policy required for that rebuild.

No new publication or live integration is implied. Audio remains explicitly OFF; the earlier full-campus integration and audio activation notes remain applicable, using this revision's translated areas rather than older coordinates.
