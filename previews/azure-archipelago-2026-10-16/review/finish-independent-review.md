# Independent final Azure polish review

**Result: PASS for a usable, polished local preview within the tested scope. No remaining material visual or gameplay blocker was found after the final repairs. This is not publication approval, and nothing was published by this reviewer.**

I independently operated the actual BAWES release game in the isolated CDP9222 room, inspected native screenshots, and reviewed ordered frames from actual-game motion recordings. I did not author or modify the map, artwork, controller, or engine. The reviewer browser was navigated to `about:blank` and released for the author's controlled performance run after the final lounge check.

## Exact reviewed state

Final reload TMJ SHA256: `d5c0e46f269e364538784d2b200545b3ebb4650b0ee70083be4198279968bb62`.

Controller SHA256: `dffafcf1646d6e9c8f11e882b259138ecd74bdf83f89a1ca38066eb718e8a804`.

Geometry SHA256: `952ba5ffb6ba202b514d7d9c542ca0ba1cdbd29a1f148791e3a700b0b495f4c3`.

`final-hashes.json` records the exact hashes of all reviewed island, bridge, bay, hub, sea, and animation assets. Earlier incremental snapshots are clearly named `initial-hashes.json` and `final-reload-hashes.json`; they are not the final candidate identifier. `final-equivalence.json` confirms all55 final seat definitions and all17 table footprints match the tested targets/footprints. Later repairs were confined to the documented landing/shoreline regions and were retested below.

## Actual gameplay results

| Check | Result and evidence |
|---|---|
| All55 seats | Actual Settings → Take nearest seat, exact target occupancy, intended native facing, ordinary keyboard exit.47 non-hub plus8 hub passed; all8 bays repeated after final bay artwork. `seat-retests.json`, `hub-seats.json`, `bay-seats.json`; full `retest-<seat>.png` screenshots. |
| Seat appearance | Reviewed cushion/body alignment and visibility. All11 lounge seats, including the3 moved rear chairs, clear the console/shelf. Café round-table chairs, garden seats, gathering armchairs and side-table pair, hub and rotated bay seats remain visibly usable. No offset exception is needed for the final anchors. |
| All17 table footprints |68 cardinal-side setup attempts:50 accessible approaches received actual keyboard pushes and screenshot review;18 setup tiles were blocked by neighboring props/rails/footprints, so no contact pass is claimed for those sides.34 actual non-hub contacts plus16 hub contacts showed no standing on tabletops. `table-retests.json`, `hub-tables.json`, full contact screenshots and diagnostic sheets. |
| Lounge console |3 north pushes stopped at feetY2352, with body below the shelf.3 west pushes stopped atx456 on the timber strip beside the console, without walking through books/maps/wall. `console.json`, six `console-*.png` screenshots. |
| Roof cutaway | Actual keyboard entry and exit through both east and southeast openings:4 crossings, correct cutaway/restoration, visible Woka. `roof.json`, `roof-*.png`. |
| Garden connectors | Actual right-click out/return for all3 western overlooks and beach connection:8/8 unique traversals, repeated8/8 after garden edge repairs. Endpoint feet are on paving/sand, not planting. `native-connectors.json`, `final-garden-connectors.json`, `final-click-*.png`. |
| Beach boundary | Actual east push against the changed outer beach cell stops atx3128,y4400, on the foamy shoreline rather than deep sea. `final-beach-cell.json/png`. The nearby beach out/return and separate shoreline push also passed. |
| Bridge mouths | Both edge lanes at all8 bridge mouths:16/16 click traversals. Initial straight keyboard returns were15/16: lounge upper lane2448 was genuinely blocked by its landing post. The post/art/collision were repaired. Final café and lounge retests passed both edge lanes with click and straight keyboard movement in both directions. Latest lounge art was reloaded and retested again. Final coverage is all16 unique edge-lane routes passing click and keyboard return after the repair. `mouths.json`, `final-mouths.json`, `last-lounge-mouths.json`. |
| Scale and visibility | Native camera zoom1 and Woka scale1 throughout recorded checks. No floor-over-avatar disappearance observed. No walking-triggered popup observed; mouth records explicitly report0 popups. No new scripted speed or camera override was introduced by this review. |

The original `mouths.json` failure remains in evidence. A preliminary message incorrectly summarized all16 keyboard returns as passing before inspecting every field; the correct initial15/16 result and successful repair are recorded above. Blocked table setup sides likewise remain excluded rather than silently counted as passes.

Independent final graph validation found3589 free native-grid cells, all connected; all55 seat and approach targets free; every cell in all17 table footprints blocked (`final-structure.json`). This graph check supports, but does not replace, the actual gameplay checks. I did not walk every individual free tile or test arbitrary multiplayer crowding.

## Visual judgment against the references

The final candidate passes my practical visual-polish gate. The earlier plain rooms and repeated marble furniture islands have been replaced by distinct, coherent destinations: a café with service counter and varied seating zones; a timber/chart reading lounge with built-in shelving; a botanical garden with differentiated beds and rocky beach; a gathering terrace with a flush shell inlay and open social center; and a mosaic fountain court with legible axes and seating insets. The quieter sea supports these landmarks instead of competing with them. Limestone bridge coping, piers, clean bays, and finished landing returns give the connections an architectural purpose.

This applies the useful lessons from Tea Garden, Volcanic Observatory, Sky Village, and Bazaar—environmental framing, material hierarchy, grouped activity, clear circulation, and memorable destinations—without importing their themes. The normal-scale Woka remains readable within the richer surroundings. Broad gathering space and bridge clearance are intentional, not missing decoration.

I accept it as polished and usable. I cannot objectively guarantee the subjective ranking “better than Tea Garden.” Tea Garden's reference has denser organic environmental framing, while Azure has stronger differentiated interior functions and a deliberately more formal coastal layout. The references are small whole-scene illustrations, whereas these checks use actual native-scale gameplay crops. That comparison is an editorial judgment, not a measurable technical pass.

The actual visual defects found during this pass were repaired and checked: embedded blue bay rectangles; excessively bright/wire-like sea highlights; clipped beach surf; clipped northern palm canopy; unfinished café landing corners; and the lounge post intrusion plus temporary rectangular paving splice. Final screenshots show clean bay exteriors, curved surf, complete palm crowns, finished café returns, and continuous lounge paving. Ordinary material changes at bridge/island joins remain visible but now read as construction transitions rather than broken cutouts.

## Motion evidence and limits

Reviewed ordered native crops from actual-game hub-fountain, garden-fountain, and beach-ocean recordings at approximately0–1.25s,4–5.25s, and8–9.25s. Fountain highlight beads visibly progress along the jets, and rings expand/reset across repeated cycles. The ocean shows restrained moving highlights over a static painted base; the beach foam itself is not animated surf. The lower opacity is visually better integrated. See `*-ordered-review.png` and `*-selected-frames.json` in this directory, and the author's continuous `*-motion.mp4` files in the parent directory.

The supplied continuous recordings are actual-game captures. My inspection method was ordered timestamped frames, not physical continuous video playback. I therefore do not claim to have ruled out every between-frame stall or flicker, nor do frame counts alone establish visible motion. The visible jet/ring changes do establish localized fountain motion; ocean motion is subtler. Final shoreline/landing art was separately verified by the fresh native screenshots above; the animation controller and water behavior were unchanged by those edge-only repairs.

I also inspected ordered camera-traversal frames from `bridge-camera-motion.mp4`. A first multi-image interpretation wrongly suggested missing bridge floor. Reopening the exact JPEGs individually showed complete floor and visible Woka, with hashes00114=`178807bd53fd8f3534e5664e554375186fdc8471a4bdb0459dd0aa49508b2643` and00216=`c6b6be75cfdca10ec3c0d6bb479ccbfc35d5f0ebe9052c0b8c1dda197922ceb0`; direct pixel checks also confirmed beige floor. That unsupported rendering-blocker claim was explicitly withdrawn. It is not an outstanding issue.

## Scope and remaining limits

No material blocker remains in this bounded local review. Final performance measurements are the author's separate controlled evidence; this report does not independently certify their FPS figures. Audio output/control testing was not repeated by this reviewer in this pass; the checks here establish silent fresh entry/no walking prompts and preserve the author's separate audio gate. Native occupancy does not add a new sitting animation. No production deployment, world registration, paid service, permission change, or engine merge was performed or approved here.
