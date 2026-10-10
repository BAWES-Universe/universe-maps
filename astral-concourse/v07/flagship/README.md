# Astral Concourse: corrective A / v07

A separate corrected same-layout baseline for comparison with earlier versions. Native 32px tiles; 2560×1920 map. The 210 auditorium chairs, 16 meeting chairs and 12 casual chairs are artwork/geometry counts, not concurrent-user capacity.

## Changes

- Preserve the accepted stage, auditorium and meeting-chair/table art.
- Replace the 12 casual stools with accepted north-facing lounge chairs at native scale, with close low tables and clear approaches.
- Add a wider marked reception counter, staff access, a 64px side return and a 96px customer apron.
- Widen the middle lounge side clearance to 64px while retaining its single entrance and communication rectangle.
- Restrict silence to the 16-cell spawn receiver, down from 333 circulation cells.
- Use native whole-hall focus on entry and restore following on exit. No scripts, roof switching or dynamic collision.

The existing garden layout remains. Material redesign/animation and the enclosing-building variation are separate candidates.

## Use safely

Serve all nine files in `map32/` together. The entry point is [grand-auditorium.tmj](map32/grand-auditorium.tmj); the adjacent [portable WAM](map32/grand-auditorium.wam) is a setup candidate. Custom TMJ does not import it automatically.

Create a separate room and follow [the room setup guide](integration/ROOM-SETUP.md). Back up the actual room WAM before any configuration change: supplying a map URL to the inspected admin update handler can regenerate the WAM and reset areas/entities. This package creates no room or media service.

## Verification and remaining limits

The frozen package passed 29 schema/zone checks and 30 repair/preservation checks. All 2,110 open cells connect and 259 seat/landmark anchors are clear. Native-source replay passes 11,802 normal commands on the unpatched source, with 16 known same-cell baseline exceptions; merged source passes all 11,818 commands. See [acceptance scope](validation/ACCEPTANCE.md), [zone checks](validation/v07-zone-verification.json), [repair checks](validation/v07-repair-verification.json), and [runtime hashes](RUNTIME-MANIFEST.json).

Initial native whole-hall focus is source-tested. Resizing/rotating while focused has a known stale-zoom/padding limitation; leaving and re-entering recalculates the fit. Full rotation acceptance is not claimed. Portrait whole-hall fit makes avatars small; manual zoom remains available. Live browser, device, media, multiplayer, capacity and PR799 deployment behavior are unverified.

## Standalone source backup

This Git folder contains the compact runtime and review evidence. The full rebuildable source, generation inputs, previews and detailed replay fixtures were delivered separately as `astral-flagship-a-v07-standalone-source.zip` (96,526,396 bytes; SHA256 `3c29f241cd1f9712ecb86b26e64db14d0fa15c3d758a6c537d1f6d25bada5627`). ZIP integrity and a clean isolated rebuild were checked before publication; the rebuild reproduced all nine runtime files and final previews exactly. Source paths mentioned in the review JSON refer to that archive, not this compact folder.

The separate runtime backup is `astral-flagship-a-v07-runtime.zip` (6,602,575 bytes; SHA256 `b3518c0a91b80ffda137cb43629ed6d33c4228fa1e1b495d02168ea391beeb61`). See [artwork provenance](PROVENANCE.md). Reference actors are review overlays and are not runtime dependencies.
