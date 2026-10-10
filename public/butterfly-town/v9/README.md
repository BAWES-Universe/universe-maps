# Lush magical campus 09 — standard32 candidate

This is an unpublished map-only candidate built from the recovered lush pre-island source. It uses the existing engine and ordinary32px tiles, with unchanged32px avatars and furniture scale. No engine PR, custom entity setup, or patched pathfinding is required.

## Contents and entry

`map32/magical-campus.tmj` is the complete campus runtime map. Keep all PNGs and the `audio/` subfolder beside it. Its default spawn is in front of the fountain. The perfected gate is a separate preserved map; a gate-to-campus room portal must be configured through the existing world editor. No destination URL is invented here, and this campus file alone does not include the gate journey.

The map includes eight ordinary work seats split left/right, two reception positions, a separate meeting area, classroom, event hall, fountain, riverside garden and two market booths. Floor labels are absent. Classified named areas remain available for later editor configuration. Bots, ownership, conferencing, stage broadcast and commerce links are not configured by this TMJ.

## Changes in09

- Native32px runtime grid. Art is packed1:1 into atlases; no source or Woka scaling.
- The baked light reception floor strip is locally repaired to match its surrounding limestone; all furnishings, foreground and collision are preserved.
- Office chair registration and floor targets allow standard native taps. Desk/table geometry remains solid, with practical floor target regions rather than a single precise click.
- Fountain paving and obstructing small furniture are locally re-authored for a continuous loop. The protected fountain bowl/spout and existing water animation pixels are preserved exactly.
- Garden source is translated16px left/up as a whole, keeping its bench/fire/tree proportions. All four bench pockets remain unavailable as promised native32 seating positions; outer circulation is available.
- A bounded shore paving repair connects the market to the garden. Its lower material seam is repaired with continuous paving and a curved waterfront edge.
- Civic chair backs render below actors for safe walking. This reduces the seated illusion: Greg visibly stands in front of those backs. Original foreground assets remain preserved separately for later editor-based depth work. The lectern rim remains above actors, but its required south registration leaves the speaker standing visibly behind it.
- Low paving/hedge/pot fragments erroneously above actors are assigned below. Real canopy, translucent shade and glass remain above. Two northern fountain canopy fringes still brush1–8 opaque head pixels across three traced frames; they are recorded, not hidden by dynamic masks.
- Interiors are roofless in this candidate. No dynamic roof visibility changes can restart a native tap path.

## Evidence and limits

The actual compiled TMJ passes42 office and102 public-route legs against unmodified source-derived native path methods at the source default180px/s,16×16 physics body, EasyStar0.4.4 and60Hz interpolation. Separate office/civic module tests exercise wider floor-click regions. These are source/geometry tests, not a live Universe session, browser playback or physical-phone acceptance.

The finite map is2944×2624 world pixels,92×82 tiles. Four tile layers allocate30,176 Phaser tile objects,75% fewer than the equivalent16px build. Thirteen Tiled objects and13 atlas pages are present. Runtime files total about19.9MB; atlas RGBA is about36.8MiB. Browser stability is unverified for this revision; previous cloud Error9 events are not claimed resolved.

All source animation frames reconstruct exactly from the32px atlases. Final foreground still exposes4,372 changing river pixels,1,615 fire pixels and8,112 fountain pixels. This verifies pixel visibility, not frame pacing on a device.

## Existing native audio

Two preattenuated files are activated by six classified native area rectangles: fountain and fire each have three gain bands. Playback follows native autoplay/retry, saved mute/pause and block-audio controls. There is no custom enable menu or `silent` property. Work, meeting, class and event areas have no ambient overlap.

The bands approximate distance on browsers with element volume support. Phones without element volume control play the fixed, already softened file level; this is not continuous spatial mixing or stereo panning. Native speaker-icon mute remains the appropriate mute control. Audible playback, native same-source transitions and background behavior still need live-client validation.

## Rebuild

Python3 with Pillow/NumPy and Node are sufficient for source assembly and route checks. FFmpeg is required only to rebuild the preattenuated audio bytes if missing.

Run `python3 tools/build09.py`, `python3 tools/compile32.py`, `python3 tools/install_native_audio09.py`, then the verification tools in `tools/`. Original generator studies are provenance, not mandatory compile inputs. The source-derived movement model is bundled under `validation/` and pinned in reports.

No part of this package grants a new license to owner-created art or audio. Third-party source code used for verification retains its upstream terms; reference artwork was not copied into this candidate.
