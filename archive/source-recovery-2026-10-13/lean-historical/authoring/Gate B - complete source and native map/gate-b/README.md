# Gate B · detail to monumental scale

This is the self-contained source backup of the separate Gate B candidate. The complete map is `gate/map/gate.tmj`; all original 15 image atlases are included locally. The published A map and its artwork have not been changed.

B begins at native center (496,1136). Walking north progressively widens the camera and holds the achieved scale. Desktop makes a bounded upward framing move at the door; retreat restores native follow without zooming in. Use **Use my camera** in the map menu to opt out. Reduced motion uses ordinary native framing and hides the existing declared animation overlays. Furniture and character scale are unchanged; the character is 32px.

Select **Play gate music and waterfalls** from the map menu for the recovered original music with a much softer fixed waterfall bed. It is one preattenuated 48-second loop, not positional audio. There are no edge action popups. Native mute/pause/stop are respected. iOS can require the native retry button after browser autoplay rejection. On browsers without element-volume support, the slider cannot attenuate; use speaker mute or pause. The fixed asset itself limits the level. No physical iPhone test is claimed.

## Portal setup

`campusRoomUrl` remains blank. Add the destination yourself with the in-game area/portal editor at the doorway. This script never calls navigation while that field is blank. If using its optional scripted transition later, supply a verified absolute HTTPS PLAY room URL, not a relative TMJ asset path.

## Rebuild and tests

Python3, Node24 with transform-types support, NumPy and FFmpeg/libmp3lame were used. No paid generation/service is required.

1. `python3 source/restore_baseline.py /tmp/gate-a-restored` reconstructs the exact 24-file source A baseline from bundled files and verifies every hash.
2. `python3 source/build_gate_b.py /tmp/gate-a-restored /tmp/gate-b-rebuilt` reconstructs B into a fresh directory. The 27 output file hashes match the bundled candidate.
3. `python3 source/build_audio.py` reproduces the fixed mix from bundled original music/cascade. It asserts the exact tested output hash; a different codec build may need remeasurement.
4. `node --experimental-transform-types --test tests/*.mjs` runs 24 camera/audio/native-source tests. The copied AudioPlayback fixture is from the user's fork at f00b3482f23c51976b4b339d7a891cad683d6498.

`source/finalize_package.py` is the saved local packaging recipe and refers to the separate local browser harness results directory. It is provenance, not a requirement for playing or rebuilding B. Publication files are already included in `publish/`.

## What was checked

Visible cloud Chromium ran the actual TMJ through Phaser3.86 Canvas with the unchanged 32px Greg and the fork's 16×16 feet-body contract. Portrait and desktop walked the approach, reached the upper/side collision boundaries and retreated. Desktop retreat retained exactly the held zoom. The explicit manual escape walked in Follow at unchanged zoom. Reduced motion made zero camera commands during the route. Native AudioPlayback with real HTML media passed start, mute, pause, resume, one complete loop, stop and unload; only one media source was active. Compact reports are in `docs/evidence/`.

These are standalone renderer/API-adapter checks. They do not prove the full deployed Universe iframe, physical mobile controls/HDPI, or an editor portal destination that has not yet been configured. Manual gesture detection is conservative because the public camera API has no input-origin event; the menu opt-out is deterministic. Desktop final framing has narrow finite dark side margins. B is ready for the requested live A/B test, not a claim of universal device acceptance.

Original gate art, animation definitions, collision grid and all atlas bytes are unchanged. The original A map/entry script and SHA256 inventory are in `originals/`. Music provenance and conservative levels are recorded in `docs/audio-*`. No new redistribution license is assigned here.
