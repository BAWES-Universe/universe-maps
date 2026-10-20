# Seam correction and interior composition — 2026-10-18

This review supersedes the rendering-line and interior observations in `COMPOSITING.md`. Source/assets were preserved in commit `536006c`; current client evidence accompanies the final review commit.

## Scenery

The mobile north line lay at the scenery texture-page boundary y=1024. Source pixels were continuous and opaque there. At the reproduced camera (x=3368,y=272,zoom=.32768), screenshot pixel (200,246) was RGB(62,136,252) between neighboring pixels approximately (100,164,253). Extending each texture page with a one-pixel duplicate border and setting Tiled `margin:1` removed the anomalous row: the same pixel became (100,164,253). Logical tile pixels, coordinates and collision dimensions are unchanged. This is a map asset fix; no engine change is involved. The isolated optimizer also reapplies page padding, and pixel/property/script equivalence still passes.

The larger rectangular sharpness boundary came from retaining the source concept's sky rectangle over a different backdrop. The current site uses an alpha cutout of the connected islands (`source/campus-site-cutout.png`) against one continuous original sky. The approved arrangement and footprint remain; no new island, building or destination was introduced. The generated original is retained at `/workspace/generated_images/exec-1266f23d-92e4-482e-b7c0-100254a29aec.png`. This removes the rectangular source-sky patch rather than covering its edge with another frame.

## Interior

Native32 Wokas and existing furniture sizes remain unchanged. Work rugs now fit the two workstation groups; the review tables have a defined rug and glass-screen edge. The existing meeting footprints now accommodate four places per table with native glass panels and planter ends. A reception desk sits beside the arrival route, the arrival lounges have coffee tables, and a rear conversation bench area supports the review wing. An amber/red inlaid motif marks the central route. Front/rear entrances and the central spine remain clear. The full floor remains cutaway-only; no exterior slab has been restored.

There are 99 reachable seats and 23,569 connected walkable cells. Native seat pointer sweeps, route and lock regressions, and both source/optimized boundary captures are recorded in adjacent JSON files. Camera-only boundary placements are coverage tests, not entrance-event simulations. Full glass/cutaway behavior is checked separately through normal movement.

## Current real-client images

- [Campus exterior](runtime-campus-exterior.png)
- [Complete interior](runtime-full-interior.png)
- [Native desk and chair](runtime-native-interior.png)
- [Indoor occupant seen through glass](runtime-registered-glass.png)
- [Mobile north edge](mobile-edge-north.png)
- [Optimized mobile north edge](optimized-mobile-edge-north.png)
- [Old seam reproduction](north-seam-baseline.png)
- [Same camera after page padding](north-seam-padded.png)

This is for visual acceptance, not a claim of perfection. The illustration retains softer close-up scenery and larger decorative plants than the native furniture. The accessible service perimeter and wide central circulation remain intentionally open. There is one navigable office floor. No StudentHub integration, engine patch, hosting change, public publication or deployment was added.

Final current-build verification: 99/99 seat pointer interactions, 23 route/input/camera checks, 8 compositing checks, 6 two-client lock/visibility checks, and 8 boundary assertions each for source and optimized maps passed. The pixel regression confirms the original seam delta of 38 channel levels is now zero in source and optimized captures. Native16 pixel/property equivalence and runtime script identity pass. The route suite was rerun after a concurrent lock test correctly prevented entry; the final run is clean.
