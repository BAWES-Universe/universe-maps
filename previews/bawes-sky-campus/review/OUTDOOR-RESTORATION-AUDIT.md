# Outdoor restoration against the exact owner reference

Reference verified: commit `532e7da29f5c3122974e3be7ac2a9552df5c0a27`, Git blob `7856a83ee3fd1c36fb5ebc6b6fa30cc32f8b7802`, SHA256 `96c20e6ad1e1e0944cf9712eb3f39a00b26bdb9ff6eaebbc12f62668ef5e67c8`. It is pixel-identical to this checkout's `approved-campus-concept.png` despite different PNG file bytes. This establishes the actual matching reference rather than guessing from an intermediate revision.

[Paired source comparison](OUTDOOR-REFERENCE-COMPARISON.svg) compares identical source coordinates at identical display scale. These are source-art diagnostic crops, not gameplay or a proposed replacement.

## Confirmed losses and current causes

- **Café:** the exact reference has a warm timber deck, counter stools and two substantial curved seating groups. The current cleaned plate substitutes pale masonry where the deck and lounges were, then the compiler adds three small café tables and six chairs. The pond and waterfall remain in the plate, but their deliberate relationship to the timber deck is lost.
- **Left conservatory:** the curved/sunken conversation alcove and entrance furnishing are removed from the cleaned plate. Two separate café-table pairs were added on the emptied paving. They do not restore the alcove's shape, enclosure or gathering purpose.
- **Stage:** the reference combines warm stage material, a strong stepped edge and substantial dark audience banks. The cleaned plate removes the audience while the compiler supplies 32 red chairs at 56×64 pitch. The original visual rhythm and floor/seat contrast were not preserved. Adding more of those chairs would not recover them.
- **Benches:** the compiler substitutes three 128×80 indoor-style sofas for outdoor planted-edge benches/curved seating. These are different objects with different silhouettes and placement, not faithful replacements of the reference benches.

This is an art/composition regression, not evidence that the Wokas should be smaller. The current foreground plate is 1536×1024 enlarged to 4608×3072. Current chair content is 32×40 (48×64 padded atlas), café tables 64×64 and sofas 128×80 at Woka scale 1. The relationship between small sharp interaction furniture and large soft painted scenery causes the tiny-dot impression. Restoring the old flattened image at 3× would bring back the appearance at overview scale while also bringing back enlarged baked furniture and missing foreground layers; that is not a clean native-scale fix.

## Actual-client native-scale audit

- [Café](outdoor-normal-cafe.png)
- [Left conservatory](outdoor-normal-west-review.png)
- [Stage audience](outdoor-normal-audience.png)
- [Terrace sofa substituted for a bench](outdoor-normal-outdoor-lounge.png)

Each capture has an actual native Woka at an existing interaction anchor, normal zoom 1 and character scale 1. Representative right-click approaches succeeded. The static collision audit finds all 48 outdoor seat anchors connected to spawn (32 audience, 6 café, 4 west, 6 terrace/portal lounge). These checks prove current reachability only, not seated animation, correct facing or visual acceptance. In the captured approaches, actual last direction was not necessarily the metadata's declared facing; metadata does not turn the player. Preserve native R rotation and require matching chair views/occupied validation for the replacement.

## Restorations possible from the supplied source

The exact visual composition and district positions can be recovered, and have been preserved in the reference archive and paired comparison. A clean playable art restoration cannot yet be extracted from this single flattened 1536×1024 PNG under the requested constraints. The deck is interleaved with stools, curved furniture, plants, shadows and pond edges; stage chairs and ground are likewise painted together. No clean background under the baked furniture or complete independent seat/front/back views is supplied. Cropping those regions into the existing expanded world would still enlarge their pixels 3× or paste floor-containing rectangles over the current plate. Neither is being presented as a solution.

No outdoor map pixels, furniture placements, avatar sizes or collision have been changed in this audit. No sticker overlay, destructive smearing, landscape stretching or generation call was made. The approved interior source and its pending plate work remain untouched.

## Bounded source work needed next

[Machine-readable district scope](../source/outdoor-reference/restoration-scope.json) records approximate reference envelopes and their existing world destinations. The factor of three there identifies current spatial placement only; it is **not** an instruction to enlarge source pixels.

Prepare three coordinated district restorations in the same illustrated family, retaining the expanded world arrangement:

1. **Café deck/bar/lounge/pond district:** ground and architectural plate at its intended world-pixel detail, with timber boards, curved deck/pond rim, existing lily pond and waterfall relationship. Export complete stools, tables, curved seating and their shadows separately. Preserve the stone bridge connection; provide no extra baked chairs under interactive ones.
2. **Conservatory social district:** restore the curved alcove, stepped/enclosed edges and furnished entrance as one coherent group with a clear approach. Export the curved seating and foreground fronts independently, rather than scattering generic café furniture over an empty floor.
3. **Stage/audience district:** retain the warm stage floor and steps, distinct audience surface, two purposeful chair banks and central aisle. Provide matching native-detail chair front/back views and masks. Calibrate seat width/depth and pitch against 32px occupants and a minimum 96px clear aisle; do not choose a count by copying painted chair dots.

Include a small matching outdoor-bench/curved-seat component set for the office terrace and lower arrival edges, with actual anchors, facing and clean underlying paving where baked seats are removed. Existing scenery outside those districts, the exterior building and the liked gate remain keepers. Complete seat bounds and collision/pond-edge margins must be measured after these exports, then tested in normal-scale occupied captures. No paid service or new asset-production cycle has been initiated here.
