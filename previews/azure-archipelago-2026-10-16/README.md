# Azure Archipelago — unpublished development candidate

Expanded work is isolated on `preview/azure-archipelago-2026-10-16`; compact published checkpoint `7336e66639a1264936a1bda311fcfd76fd0e0e1d` remains preserved. Do not publish or deploy this revision.

The native 32px map is 5120×5120 world pixels. Four distinct island silhouettes connect to a fountain hub through 256px clear bridges with seating bays. North: café service counter and unequal ocean balconies. South: planted garden, beach cove and southern overlook. West: glass lounge with stepped balconies. East: curved gathering terrace and three ocean-view projections. No baked-in labels. Woka scale1 and default camera.

The final geometry has 3,613 connected walkable cells, 55 seats and 17 blocked table footprints. Fresh independent gameplay review passes within the documented scope: every seat was exercised, 21 changed seats retested, table contacts inspected, garden routes/right-click connectors and roof cutaways verified. Author testing passed all 24 bridge-mouth crossings across three lanes per bridge. Native Woka scale and camera remain 1. See review/independent-review.md for exact coverage and limitations.

Continuous 12.8–13.5 second actual-runtime videos show fountain droplets and expanding rings. Independent review inspected ordered timestamped frames. Ocean shimmer is subtler; painted shoreline foam is static. Silent spawn and deliberate Play/Stop were measured at browser output, with six playing and six stopped crossings and zero audio popups. This is not a physical-speaker listening test.

Build order: `node source/silhouette-geometry.cjs`, `node source/water.cjs`, `node source/build-map.cjs` (scripts use this workspace's absolute root). `source/art-geometry.cjs` and `layout.cjs` are retained historical scaffold generators; do not run them over the revised silhouette geometry. Final geometry derives from reviewed artwork, native tile floor masks, manually bounded table footprints and individually measured cushion centers. Non-connected bright fragments such as offshore rocks are excluded.

Sound starts silent and offers deliberate Play sea sound/Stop sea sound commands. The WA.sound fallback uses a separate sound channel not controlled by native master audio controls. No walking-triggered popup code exists. Physical speaker output is unverified.


Performance: controlled full-redraw testing at 1366×768 measured about 29–31 FPS expanded versus 40 FPS compact; ordinary expanded idle scheduling with water enabled measured about 53 FPS. No 60 FPS guarantee. See review/performance-report.md. The structural generator deliberately leaves gameplayAccepted false; separate review/acceptance.json and independent-review.md record actual gameplay acceptance.
