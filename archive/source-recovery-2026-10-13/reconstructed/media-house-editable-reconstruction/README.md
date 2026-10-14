# Media House: editable reconstruction checkpoint

This is a NEW partial reconstruction, dated 13 October 2026. It is not the missing r9 and not an exact restoration of r9. Original r7c source and artwork survive; this package rebuilds their five runtime files byte-for-byte, supplies editable layout and a small source-plane compiler wrapper, and adds two bench-front route-test landmarks in a separately named candidate. No new artwork, no pixel edits, no deployment, no automatic facing or sitting animation.

## What is usable now

- After rebuilding, candidate/resonance-media-house/map32 contains the TMJ, WAM and three original image atlases for an authorized test room. This source checkpoint omits duplicate PNG assets; obtain the original Library source archive and rebuild before import. No hosted test room was created by this work.
- source/layout.json is the new editable collision, quiet-zone, area, anchor and fixture source.
- The compiler uses the ORIGINAL source artwork via the original Library source ZIP identified in evidence/original-library-references.json. The original source archive must be extracted locally and supplied as --baseline. Do not substitute a catalogue screenshot or regenerate imagery.
- The r7c map is a creation/listening-space template. Editor, recording, screen playback and synthesis services remain unconfigured, as in its original source. This package does not turn those areas into working integrations.

## Rebuild

Requires Python 3 with Pillow and NumPy, plus Node.js for movement checks. Extract the original resonance-media-house-r7c-source-replay.zip from Library. From this package root:

    python3 tools/reconstruct.py --baseline /absolute/path/to/extracted/r7c --original
    python3 tools/reconstruct.py --baseline /absolute/path/to/extracted/r7c
    node tools/native/route-audit.cjs baseline-rebuild/resonance-media-house
    node tools/native/route-audit.cjs candidate/resonance-media-house

The original reconstruction asserts SHA-256 equality for all five runtime files. Candidate texture and WAM bytes must also remain equal. Its TMJ title deliberately labels the new candidate. Its two additional source/test landmarks are (240,800) and (784,800), closer to the garden bench fronts than old approach anchors at y=815. They do not appear as interactable entities in TMJ/WAM. Collision is unchanged. The route tests establish reachable standing positions, not recovered r9 bench changes.

## Evidence and fidelity

User defect report Sentinel_ce59181f97408191b4e0584746282aed, 11 October 2026 22:47 UTC: reachable benches; remove top-right plant/wall obstruction; continuous entrance without cropped glow; repair blurred bottom-right carpet. Prior delivery Sentinel_e4290e4b50bc8191bf2445f052354e33, 23:06:46 UTC, claimed those repairs and explicitly withheld live rendering validation. The comparison attachments have not yielded source pixels or r9 bytes.

The recorded missing source package media-r9-source.zip was 36,289,906 bytes, 86 members. Full r9 source/TMJ SHA-256 is unknown. No claim of exact r9 recovery can be supported. r7c original artwork is retained exactly; the entrance, lower-right rug and top-right plant/wall remain r7c and require supported original pixels or a separately approved design decision. We did not remove art obstacles by silently opening collisions through them.

## Verified before and after

Fresh execution, not inherited historical PASS:
- Original: 5/5 runtime files byte-exact; 31 anchors; 1,722 source-extracted native desktop/touch route legs, 2,626,367 collision samples; zero failed legs.
- Candidate: original image atlases/WAM byte-exact; same 272 floor cells, all reachable; 33 anchors; 1,864 route legs, 2,860,552 collision samples; zero failed legs.
- Both: 188,123 safe integer body placements, zero head conflicts, zero unreachable admitted cells; collision extracted from TMJ agrees with source.
- Native methods are surviving source-extracted methods pinned to 60e7afdc3f96ef32525597cd46bd41175d61a2ef. These are offline movement replays, not live device/GPU/Phaser/browser or current-engine certification.

## Acceptance checklist still open

1. Recover exact r9 source/runtime or original repair comparison pixels and compare full hashes if available.
2. Entrance: inspect both sides of threshold at native zoom; continuous floor/glow, no rectangular crop seam. NOT FIXED here.
3. Lower-right carpet: inspect native pixels and zoom/pan for repeated/blurred patches. NOT FIXED here.
4. Top-right recording-room passage: visually identify intended continuous path and measure full body routes around plant/wall; do not open depicted solid fixture. r9 repair NOT RECOVERED.
5. Benches: click/touch each front and depart both directions; verify standing body/feet and depth in live room. Offline front-target routes pass; live result OPEN. Sitting and automatic facing are not implemented.
6. Validate desktop keyboard, touch, repeated destinations, interrupted route, viewport/zoom, multiplayer and rendering. NOT RUN.
7. Verify configured services only after explicit integration authorization. UNCONFIGURED.

Original archives were not changed. No remote GitHub writes, merges, permission changes, publishing, paid tools or image generation were used.
