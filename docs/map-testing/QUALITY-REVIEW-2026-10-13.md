# Quality standard and reported findings · 13 October 2026

[Testing register](README.md) · [Common acceptance checks](COMMON-CHECKS.md) · [Whole collection](../../COLLECTION.md)

This dated record supplements the earlier feedback without overwriting it. No artwork, collision, map script or engine fix is made by this documentation update. Original versions remain preserved. Source inspection, mocked API tests, user-observed loading and full live acceptance are different evidence levels.

## Visual quality requirement

The user’s new minimum is **every new map should reach at least the Tea Garden’s visual quality and continue improving**. The user also singled out **Art Deco’s beautiful detail quality** as a benchmark and asked for continuous improvement with no regression to pixelated, stitched cutouts. Use both Tea Garden and Art Deco as visual references at actual playing scale; Mission Control’s art/layout is also user-approved. **These are quality benchmarks, not visual templates:** different styles are welcome. Match detail, clarity, cohesion and polish at playing scale; do not make every map look like Tea Garden or Art Deco. Visual approval is separate from functional acceptance. Willow Quay remains a visual reference, not a blanket gameplay approval: its circulation, seams and motion limitations below remain open.

Compare the actual in-game views at matched viewport, camera zoom and projected player/tile scale, with source-pixel / artwork detail visible. An enlarged thumbnail, filtered/upscaled export or larger pixel dimensions alone cannot earn a quality PASS. Require coherent art, clean joins, readable objects and intended motion, as well as footprint-aware movement and clear audio where designed. Record the exact baseline and candidate revisions before approval.

## Standing map-design rule: chairs, desks and tables

Across all maps, **do not draw artificial collision boundaries behind chairs**. Allow approach from the rear and intended circulation around seating with the native avatar footprint. This also applies to desks and tables: allow approach to the real ground-contact base without a large empty-floor gap; keep collision separate from tabletop overhang, and let the tabletop appropriately cover the avatar through foreground/depth ordering. Preserve real furniture contact footprints, walls, water edges and other intentionally solid geometry; visual furniture bounds are not automatically ground-contact bounds.

The user specifically called Art Deco beautiful and requested these boundary repairs across the collection, then reported a large empty-floor gap above an Art Deco desk and asked to approach beneath its tabletop overhang. Preserve the liked art. [Art Deco revision card](work-gardens.md#art-deco-sales-atelier-r2b). Additive collision revisions are being handled separately; this rule and review record do not mark any map fixed.

## Willow Quay Tea Garden · r5 / r05

[Revision card](work-gardens.md#willow-quay-tea-garden-furniture-r05) · [Preserved exact runtime](../../archive/runtime-recovery-2026-10-13/willow-furniture-r5-r05-runtime/)

**Evidence:** user-reported circulation / visual problems, with source inspection confirming the retained r5 layout and collision behavior. These are open defects, not fixed or newly live-tested.

- Collision rounding creates an invisible barrier extending about **31 pixels above tables**.
- The entrance is only one tile wide. Chair approaches / full circulation loops and the stair landing are blocked or constrained.
- Old foliage covers paving. A baked **north 160-pixel strip** contains a visible seam / tree mismatch.
- This preserved revision has **no animation**; do not advertise it as a motion-enabled build.

**Next acceptance:** walk completely around each chair/table with the real avatar footprint; approach every chair from both sides; traverse the entrance and stairs in both directions; compare visible paving with collision boundaries. Inspect the north join and foliage at matched in-game scales. Any proposed art or motion revision remains separate from the preserved original.

## Celestial Transit Garden · tested revision not yet identified

[Expanded r4 history](work-gardens.md#celestial-transit-garden-expanded-r4) · [Calmer Draft card](work-gardens.md#celestial-calmer-draft)

**User report:** the Transit Garden looks pixelated. A matched-scale comparison against the Tea Garden is pending. The report does not identify which Transit revision was tested, so it is not assigned as a proven defect of one specific variant.

**Source comparison (specific to the current Calmer Draft):** its original 1448 × 1086 artwork was enlarged about 1.414× to 2048 × 1536. Tea Garden’s main artwork is native 1536 × 1024 plus a north strip. Both packed atlases reconstruct their original masters pixel-for-pixel; the measured difference is source-art detail rather than damaged tile slicing. Matched 512-world-pixel crops show the Calmer Draft blurrier. This does not identify the user’s tested variant or generalize the finding to every Transit version.

**Next acceptance:** capture the actual TMJ/hash, engine build, viewport and zoom; record the source-to-world sampling ratio and compare equal-world-scale crops and native source detail and in-game views against the Tea Garden benchmark. Separate low-detail artwork, scaling behavior and visible art joins before deciding the repair. No upscale-only quality PASS.

## Mission Control · design approved, boundaries need inspection

[Revision card](work-gardens.md#mission-control-center-r4-paired-shift) · [Preserved r4 runtime](../../archive/runtime-recovery-2026-10-13/Mission-Control-r4-runtime/)

**User feedback:** the design is “perfect”; preserve the artwork. The user reports floor barriers left and right of the entrance and substantial visibly walkable floor being blocked, including the floor by the main screen at the top and the upper room’s left/right edges. The exact version the user viewed is still unconfirmed. Source inspection of the current published r4 candidate does independently confirm these false-blocked floor regions, plus upper-room south floor and console fronts. Its TMJ is `mission-control-center/map32/map.tmj`, SHA-256 `ecba8068ca83077a051dbd68fdf4af956e4b5271688bae15ebece7ea9a4cab08`; all seven runtime files match their publication-manifest hashes.

**Source finding:** `build_environments.py` / `command()` admits a 32-pixel tile only if the whole tile fits a hand-drawn polygon, uses coarse console rectangles, and admits the lower room through narrow rectangles. Artwork/collision overlays show fully blocked 16 × 16 avatar-body footprints on visibly clear floor at the main-screen approach, upper edge aisles, upper south floor, both entrance sides and console fronts. The prior 495 route passes tested only already-admitted targets, so they did not measure missing-floor coverage. No runtime change or live retest is recorded.

**Next acceptance:** compare an explicitly marked intended-walkable-floor mask with the actual collision mask, using the real avatar footprint. Count and visualize falsely blocked floor, including the main-screen approach, entrance sides and upper-room edges. Connectivity of cells already admitted by the collision mask cannot detect excluded-but-intended floor. Improve boundaries while preserving the liked art; identify the exact revision before attributing the result.

## Resonance Media House · art rejected, tested revision unresolved

[Media review and missing r9](repairs.md#media-r9) · [Surviving r7c runtime](../../archive/runtime-recovery-2026-10-13/resonance-media-house-r7c-runtime/)

**New user decision: reject the current viewed artwork / needs a coherent art pass.** The concept and layout are liked. The user described the art as “pixelated junk stitched together” and said its quality was not up to par.

The exact version viewed was not supplied. The published collection entry is the surviving **r7c** fallback; this does not prove the user viewed r7c. Requested **r9 remains missing**, and the rejection must not be attributed to r9 or treated as evidence its repairs were recovered. Preserve the current artifact and the earlier imported review fields.

**Next acceptance:** first identify the tested URL/hash. Keep the liked concept/layout as review intent, then require a coherent art treatment, consistent source-pixel detail and seamless joins at matched in-game scales, at least the Tea Garden visual benchmark. A polish revision is not approved or implemented by this record.

## Lighthouse: The Keeper’s Return · r2

[Revision card](interactive.md#lighthouse-keepers-return-r2) · [Preserved exact runtime](../../archive/runtime-recovery-2026-10-13/lighthouse-keepers-return-r2-runtime/)

**Map-script findings:** user-reported reverse-exit popup on arrival, pickup interaction reopening, and journal-footer behavior were reproduced in mocked WorkAdventure API checks. Mocked reproduction is not a live-engine retest. These defects remain open alongside the previously recorded teleport-recovery race.

**Separate engine gaps:** source inspection confirms gaps in companion teleport handling and cross-room walk-to / bot summoning. There is no portal graph to route across the separated rooms. These are not established as map-art fixes or covered by a newly approved engine issue; no additional engine issue or implementation is authorized by this record.

**Next acceptance:** arrive in each room without an immediate reverse-exit prompt; collect an item once without reopening it; check journal footer actions after close/reopen. Interrupt/reconnect during room transitions and test stale completion recovery. Where companions or bots are intended, test their placement and cross-room destinations separately on a specific engine build; record unsupported behavior instead of claiming success.

## Lighthouse: The Last Signal · r2

[Revision card](interactive.md#lighthouse-last-signal-r2) · [Preserved exact runtime](../../archive/runtime-recovery-2026-10-13/lighthouse-last-signal-r2-runtime/)

**User-observed entry evidence:** the 13 Oct screenshot shows the map loaded in Universe and its starting popup visible, with Begin quietly / Begin + shore signal / Close. The room URL and exact deployed engine build were not shown. This establishes observed loading and entry UI only, not full puzzle, audio, multiplayer or acceptance PASS.

**Audio evidence:** the published runtime contains a real approximately eight-second WAV. Source configuration uses volume **0.09** and a **160-pixel radius**; the dock emitter is approximately **528 pixels from the start**. The start is outside that emitter radius, so the clip is not expected to be audible there under the configured proximity behavior. A file upload or source calculation does not prove audible playback on the user’s device; actual playback remains unverified.

**Next acceptance:** after an intentional audio gesture, test at the start and within the dock zone; verify clear audibility at the intended location, mute/exit/re-entry and cleanup. Make the quiet-start / proximity expectation clear, or review it as a design change. Do not claim an audio fix from asset availability alone.

## Shared popup styling

The starting popup does not match the intended Universe design system. The shared engine issue is [#932: map-script popup surfaces, buttons and Close styling](https://github.com/BAWES-Universe/workadventure-universe/issues/932), **open** when checked on 13 Oct. This is separate from Keeper’s map-script interaction bugs.

**Next acceptance:** compare hierarchy, surfaces, button sizing/wrapping, spacing and Close treatment with the current design system; test ordinary desktop and phone-width popups, long actions, close/reopen, focus and interaction isolation. Filing the issue does not mean a fix is merged, released or live-tested.

## Evidence and release discipline

- Preserve all existing source/runtime versions and imported feedback. Add any approved future repair as its own revision.
- Public availability was checked for all 80 packages / 596 original files; [publication receipt](../map-collection/publication-status.json). It does not close these quality or behavior findings.
- The 33 H originals, Media r9 and full-original-authoring gaps remain unresolved. This record changes no recovery count.
- This update is to the backup-branch testing register only. It does not modify the public directory or publish a map/engine revision.
