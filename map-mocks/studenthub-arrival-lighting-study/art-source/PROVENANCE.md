# Original art provenance

All architecture, plants, furniture, fountain and lighting are authored as original geometry by `tools/build_scene.py`. No third-party reference map artwork and no earlier rejected furniture sprites are imported.

The four material channels are cut from `original-material-sheet.png`, created through the built-in image generation tool. It returned1254×1254 pixels; each source quadrant is627×627, used as a surface material on calibrated geometry, never enlarged into a campus background. Prompt requested warm fine limestone, teal ceramic, straight oak grain and cream linen with diffuse albedo and no baked directional lighting.

The camera is orthographic and mathematically calibrated:32 world pixels per logical ground unit in both axes. Native exports are1536×1152. Blender is offline authoring; the game remains a2D tilemap.

Greg is the unchanged user-approved32px avatar, used only in preview/harness evidence and never baked into the map.

`painted-water.png` is a separate original1254×1254 surface made with the same built-in tool. Its prompt requested jewel teal water, sparse broken caustic glints and diffuse painted detail without a basin, objects or concentric rings. It is applied to the two independent3D fountain water surfaces; the basin geometry remains original and separately authored.
