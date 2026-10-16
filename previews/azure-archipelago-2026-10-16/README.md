# Azure Archipelago — unpublished development candidate

Expanded work is isolated on `preview/azure-archipelago-2026-10-16`; compact published checkpoint `7336e66639a1264936a1bda311fcfd76fd0e0e1d` remains preserved. Do not publish or deploy this revision.

The native32px map is5120×5120worldpixels. Four distinct island silhouettes connect to a fountain hub through256px clear bridges with seating bays. North: café service counter and unequal ocean balconies. South: planted garden, beach cove and southern overlook. West: glass lounge with stepped balconies. East: curved gathering terrace and three ocean-view projections. No baked-in labels. Woka scale1 and default camera.

Current candidate has3517 connected walkable cells and55 provisional seat anchors. Those structural checks do not establish gameplay acceptance. New artwork changed all island boundaries and furniture coordinates; a fresh independent route, seat, table and visual review is underway. Continuous water footage and audio persistence verification remain pending. Earlier square-layout review does not certify this revision.

Build order: `node source/silhouette-geometry.cjs`, `node source/water.cjs`, `node source/build-map.cjs` (scripts use this workspace's absolute root). `source/art-geometry.cjs` and `layout.cjs` are retained historical scaffold generators; do not run them over the revised silhouette geometry. Final geometry derives from reviewed artwork, native tile floor masks, manually bounded table footprints and individually measured cushion centers. Non-connected bright fragments such as offshore rocks are excluded.

Sound starts silent and offers deliberate Play sea sound/Stop sea sound commands. The WA.sound fallback uses a separate sound channel not controlled by native master audio controls. No walking-triggered popup code exists. Physical speaker output is unverified.
