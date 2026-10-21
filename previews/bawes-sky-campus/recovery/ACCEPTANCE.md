# Tested playable review package — unpublished

Deliverable: [bawes-sky-campus-native-review.zip](bawes-sky-campus-native-review.zip), 84,143,439 bytes, 109 entries. It contains campus.tmj, runtime, every referenced art dependency, index and PUBLICATION.json. ZIP integrity passed. This is an actual Universe map package, not a static mockup; the index explains how to import the hosted TMJ into Universe.

SHA256 archive: `e852cc683e05ea360ebbf1dd4dcb5817c2e4d3ca784c7c4fa9737b7bf76af529`

SHA256 map: `60ab383c286280f84cf5595cb1e6f445045b180eff1a7e81cc9edf3b6cb7d3c8`

SHA256 runtime: `1dcd3804259fe560238bfdaad7fbff72cf8f170578f5a8115e24fa5b4ca4f70d`

## Result

- **171/171 primary checks passed** in the actual Universe client: all **71 seats** reached and correctly facing; office, both meeting rooms and greenhouse journeys; stage/café keyboard boundary collisions; all 11 animation clocks; desktop and 430×900 touch viewport travel/tap. The source has 71 seats, rather than the approximate 73 in the handoff.
- **12/12 supplemental checks passed**: mobile viewport performance, seating cancellation by keyboard movement, four blocked destinations, clean counter/greenhouse occupancy and entrance captures.
- **Visible motion verified** across five actual-client captures per region: waterfall 2,096 changed pixels, pond 68, lantern 728. This supplements frame-clock checks; it is not inferred solely from TMJ definitions.
- All 71 head boxes clear foreground-mask alpha checks. Representative occupied screenshots were inspected for stage, café, office and greenhouse. This is not an exhaustive pixel-level proof for every avatar costume/animation.
- Static connectivity includes all 71 seats and 12,671 walkable cells. Packaging retains native 16px grids with no art resampling, removes empty/inactive layers and composites compatible backgrounds, reducing 39 layers to 25. Compiler checks preserve interactive layers and prevent overlap with intervening artwork.

## Repairs

Cleared furniture from the greenhouse entrance/stair axis; removed blue ornaments from both side paths; moved two seats into the accessible greenhouse cutaway; lowered the café counter; shaped stage-chair foreground masks around the chair; made seat-facing alignment cancellable; bounded collision repairs; paused gate frame changes during travel to prevent path shifts. Waterfall ribbons, pond ripples and warm lantern pulses use 11 reused, four-frame animation definitions, not hundreds of unique animations. Existing artwork and earlier stage references were inspected before editing. Original source remains preserved in Git history and outside the candidate directory.

## Measured performance and limits

Pinned Universe client: `274114560c5ec95fdf8e51e67986a53069f3cf06`. Cloud headless Chromium, software WebGL (ANGLE/SwiftShader), local HTTP assets; not a physical phone and not a public-network download benchmark.

| Measurement | Result |
| --- | --- |
| Compact client startup | 15,659 ms |
| Desktop 1440×900, 120-frame sample | median 50.46 FPS; minimum 47.62 |
| Touch viewport 430×900, 180-frame sample, DPR1 | median 45.01 FPS; minimum 42.01; maximum 51.32 |
| Observed JS heap during primary traversal | approximately 1.30–1.43 GiB |
| Package download size | 84.14 MB ZIP |

The map remains resource-heavy. Physical-phone memory/performance, production networking, multi-user calls and public hosting were not tested. The local backend reports disabled persistence/permission checks; meeting locks are courtesy controls. No universal device compatibility or flawless operation is claimed.

The primary run completed 165 checks before a harness callback returned the entire Phaser camera to automation, causing scene serialization and heap exhaustion. The callback was corrected to return nothing; the final six checks were resumed on identical map/runtime hashes and recorded in the same 171-record report. This was a test-harness failure, not established evidence of an intrinsic map leak. Earlier interrupted runs remain recorded, with the diagnosis corrected. The earlier optimizer ZIP is superseded and is not the deliverable.

## Evidence and publication

- [Primary checks](evidence/compact-final-checks.json), [supplemental checks](evidence/supplemental-checks.json), [rendered motion](evidence/rendered-motion.json), [motion phases](evidence/motion-capture-phases.json), [head occlusion](evidence/seat-head-occlusion.json), [archive integrity](evidence/native-archive-integrity.json).
- [Occupied café counter](evidence/final-review-counter.png), [clear entrance](evidence/final-review-entrance.png), [occupied greenhouse](evidence/final-review-greenhouse.png), [stage seat](evidence/compact-final-seat-23.png), [mobile viewport](evidence/compact-final-mobile.png).
- [Reproduction](REPRODUCE.md), [recovery provenance](RECOVERY.md), [exact proposed publication action](PUBLICATION-PROPOSAL.md).

No publication, deployment, merge, release publication, permission change or production overwrite was performed. The proposed isolated gh-pages directory still needs the parent's separate publication authority and a post-publication load check. No access denial remains blocking this recovery package.
