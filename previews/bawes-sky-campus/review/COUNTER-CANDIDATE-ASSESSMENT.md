# Counter candidate assessment — rejected, map unchanged

Sources from `cd7223d4dc1f8c675e2f9a543767f6fc30487aa2` were inspected and tried offline. No candidate pixels were integrated into the map, and no counter/stool/collision/runtime/interior/alcove changes were made. No further image generation occurred.

## What was tried

The free-background candidate was fit to the source envelope `(216,676)-(400,746)` / world `(2440,4076,552,210)`. An experimental counter silhouette limited replacement; the whole rectangle was never pasted. First trial: direct envelope fit with an inward1px edge. Second trial: local endpoint alignment (horizontal scale1.04, shift−18 native pixels; vertical shear to correct roughly20px of left/right shelf mismatch), with4px inward feathering. These are diagnostic composites, not approved masks or runtime screenshots.

Both fail visually. The preserved original shelf intersects a different-height wall/support arrangement. Old prop/shelf overlaps make irregular upper joins; aligning left features displaces the right post and return. The candidate adds a new left planted/post shape at that junction. Its sharp, large stone pattern also creates a distinct floor patch. Feathering cannot recover the original structure and would instead blur remnants. The new small counter does not hide those defects. See `counter-registration-comparison.png`, `counter-rejected-removal.png`, and `counter-rejected-local-alignment.png`.

## Counter assembly

Only the upper complete assembly was isolated. Alpha below32 was removed to exclude distant low-opacity noise; the resulting crop is `(130,44)-(1921,531)`,1791×487. Uniform384px calibration produces384×104. The separate apron was not used. Any future foreground mask must be segmented from this same main assembly.

The visible front body is approximately28–36px at that scale, below the40–48px target; the32px stool and32px Woka would not by themselves prove the correct counter proportion. Expanding to obtain a taller body also expands the width. Nonuniform stretching was not used. `counter-native-384-assessment.png` is an offline asset preview, not validated occupancy.

## Exact remaining needs

1. A **registered** clean plate for source `(216,676)-(400,746)`,184×70 source /552×210 world pixels. Keep the original canopy posts, shelf rows, bottles, plants and right return unchanged. Reconstruct only hidden backing, supports and floor behind the original counter and attached props, including the narrow overlaps directly below the shelf. It must meet the original upper/left/right structure and lower floor without requiring those protected pixels to move. A different plausible wall is insufficient.
2. A complete same-camera counter designed for **384px width and40–48px front-body height**, with top depth20–28px and total height at most146px including props. Supply the top, both ends, front apron and props in one coherent transparent assembly. The current main assembly remains useful as a reference, but its body needs the stated proportion at384px; the mismatched separate apron cannot correct it.

No new runtime after image exists because integration was rejected. `counter-runtime-before-unchanged.png` is the actual6b7a519 café view and still represents the current map. Existing native occupancy and96px route evidence remain applicable to that unchanged map; no new counter occupancy claim is made. Accepted interior and outside-mask scenery remain unchanged in the deliverable, byte-for-byte.
