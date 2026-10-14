# Resonance Media House

Sandbox / media creation — Walnut studio workshop, preview salon and acoustic recording spaces. An additive original native32 map template; all earlier maps preserved.

## Delivered
- Actual orthogonal TMJ, relative PNG atlases and companion WAM in map32/.
- Native occupied/empty/collision previews decoded from the compiled atlas. Greg is a 32px source-authored preview fixture only.
- Original generated environment master, deterministic composition/compiler source, collision/anchor/area contract and reproducible native movement fixture.

## Layout counts
9 visible seats; 18 authored test anchors including the spawn. Counts describe artwork and routes, not supported-user capacity. Willow's gazebo uses two standing conversation anchors rather than chairs. Portal arches are decorative, inactive destination placeholders.

## Status
Static collision, anchor and atlas tests plus pinned native movement replay are supplied in validation/. No live room/browser/keyboard/device/network/multi-user/service test is claimed. No publication, engine edit or merge. Water, foliage and lights are STATIC artwork; no animation is claimed.

## Honest feature scope
Artwork and editor-ready areas only. No AI generation, recording, music service, ecommerce checkout, seller bot or teleport target is operational. Configure appropriate integrations and permissions separately in a new room. Blank portal destinations stay disabled. Decorative counters are fixed background art; public approach anchors are tested, staff access behind counters is not offered.

## Setup
Serve map32/ together and select resonance-media-house.tmj as the custom TMJ. The adjacent WAM is a portable setup candidate: Custom TMJ does NOT automatically import it. Back up any existing room WAM before changes; create a separate test room. See integration/ROOM-SETUP.md.

## Rebuild
Visual boundary sheets are regenerated with python tools/check_spawn_and_boundaries.py resonance-media-house. The source-replay ZIP has tools/, source/ and resonance-media-house/ at its root. With Python3, Pillow and NumPy: python tools/build_maps.py --map resonance-media-house. Then: node tools/native/route-audit.cjs resonance-media-house. No repository, paid API, remote asset download or engine change is needed. Source-extracted engine methods and EasyStar0.4.4 are bundled with source pin metadata.
