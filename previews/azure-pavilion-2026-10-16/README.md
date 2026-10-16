# Azure Pavilion — work in progress

A separate compact coastal Art Deco map. This branch is a source/artwork backup, not an accepted or published preview. Moonlit is unchanged.

Open `azure.tmj` in WorkAdventure. Native 32px grid, Woka scale1. The map contains a furnished glass lounge, two café groups, broad promenade, animated fountain and overlook. Spawn is silent. Use the profile's All settings menu, then Pavilion sound or Take nearest seat; sound never starts from walking. Interactions, all route edges, regenerated furniture alignment and rendered audio are still undergoing actual-game validation.

Artwork: original vector geometry authored for this map, then refined with the built-in image-generation tool. Original1402x1122 raster retained in source; runtime image downsampled to1280x1024. No external paid service. Generated imagery is not proof of collision correctness. Fountain animation and synthetic sea-breeze audio authored locally. Source build-layout.cjs recreates the geometry scaffold and animation; it does not recreate the generated final art. Final map references coastal-cafe.png. Current candidate has13 chair/settee occupancy positions and6 table footprints.

Test runtime: exact BAWES Universe v0.3.8 commit274114560c5ec95fdf8e51e67986a53069f3cf06 in an isolated checkout. No engine merges or production deployment.

Publication requires separate authorization; no public Pages preview has been created for this new map.
