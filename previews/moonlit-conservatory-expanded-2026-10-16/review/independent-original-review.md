# Independent review of original Moonlit artifact

Reviewed by a non-author agent through map, script, engine depth code, and image inspection. No gameplay claim is made here. Candidate repair acceptance remains pending.

## Confirmed original defects

- `Tree canopy above walking loop` is an overlay above `floorLayer`, containing 18 opaque artwork tiles over x=672–864, y=352–448. These include paved ground north of the central planted bed and can cover the Woka entirely. The engine switches depth to 1,000,000 after the `floorLayer` object group.
- `scene.js` creates water audio popups on entering any water-source radius, and derives many lower map popup anchors from the player position. Walking between anchor regions can reopen popups. This directly conflicts with the requested popup-free water crossings.
- Painted left pavilion table center (224,240) is walkable. Other table centers (424,240) and (1200,528) are blocked, showing inconsistent furniture collision.
- There are no seat properties or objects in the original TMJ. Painted chairs alone do not establish a sitting interaction.
- Seven of fifteen upper animation placements are beneath later connector/junction artwork. All three lower fountain animated tiles at (768,1344), (768,1376), (800,1376) are beneath opaque `Continuous lower garden` artwork.
- Every upper animation placement uses the same 32×32 tile-0 ripple. The maximum average per-channel difference from frame zero across its 24 frames is only 1.69/255. The original animated placement covers small patches, not the major painted waterfall streams. Eight upper placements have no later covering layer, so their weak motion cannot be explained solely by depth.

## Acceptance requirements still pending

Actual engine gameplay must cover the upper path, all loops/connections, central tree, both pavilion roof transitions, each seat approach and sit/exit, blocked table footprints, stable native avatar/camera scale, silent spawn, repeated water-region crossings without prompts, and preserved Walk to fountain guidance. Continuous footage must visibly establish water/fountain motion. Source frame counts, static screenshots, and coordinate-only assertions cannot substitute for this.
