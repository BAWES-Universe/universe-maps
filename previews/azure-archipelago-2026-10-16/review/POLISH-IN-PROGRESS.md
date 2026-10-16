# Unpublished finish pass — in progress

Owner clarified publication only when finished. Prior gameplay acceptance does not certify the new finish pass. Do not deploy.

Benchmarks inspected: actual recovered Tea Garden, Volcanic Observatory, Sky Village Airship Terminal and Lantern Souk Bazaar previews. Preserve Azure's ocean, four distinct islands, balconies, beach and native player/camera scale. Aim for richer material/planting detail, stronger use of space and integrated bridges rather than copying the reference themes.

Map-local render optimization removes only tiles completely covered by higher opaque artwork and disables drawing of fully transparent collision/start layers while retaining all their data. Sea animation128px patches are repacked into64px quadrants so the engine's default one-cell culling margin includes every partly visible patch. Same frame timing and motion pixels. No engine edits. Full-map raster comparison against prior source:14909pixels differ by at most1channel unit from atlas rounding; mean absolute channel difference0.000142.

First controlled1366×768 forced-redraw sample: old29.26FPS, optimized57.40FPS. Repeated measurements, other views and water-edge footage pending. This is not a final performance claim.

A revised fountain-court artwork has been generated but is not installed. Wider finish and independent review remain open. Prior independent-review.md describes its explicitly identified earlier map hash only.
