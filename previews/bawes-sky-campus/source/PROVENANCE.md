# Sources and contracts

Base maps repository: `adabef710832cbb4a1662a8b9f77a493b4e5ecf3`. Runtime: BAWES Universe `274114560c5ec95fdf8e51e67986a53069f3cf06`. Native Woka: 32×32 at scale1; compiler grid:16. This is not a cross-version WorkAdventure certification.

The approved campus concept and office study were recovered unchanged from `BAWES-Universe/universe-maps` transfer commit `96b79b7d3470e526dacdf718c7b72ee638990327`, folder `bawes-build-transfer-2026-10-17`. The Magical Campus geometry/overview and greg sprite were inspected for scale. Magical Campus art was not pasted into this candidate. The approved concept itself supplies the surrounding illustrated islands; native office furniture and gameplay are authored separately.

Built-in image generation produced retained original sky, office shell, floor, furniture and island-plinth PNGs. These are new asset studies guided by the approved concept. No external paid image service or asset purchase was used. The folded amber/red architectural tower is an interpretation of the approved brand direction, not an exact vector-logo tracing. The image originals remain in source/ and in the environment's generated_images folder.

The compiler's separate floor, body, foreground, collision, doors and cover follow the inspected `GameMapFrontWrapper`, `Character`, `Player`, `PathfindingManager` and `CameraManager` contracts at the pinned engine. `floorLayer` is the depth boundary. Collision does not derive from PNG alpha. Layer visibility refreshes collision/pathfinding even for a noncolliding cover, so cover changes and door closing wait for movement to stop. This avoids repeated endpoint shifts observed in the first 16px runtime route test.

Universe Ink was inspected in the saved admin `app/globals.css`: #14121e dark foundation, raised violet-neutral panels, restrained semantic action accents. Those are interface contracts. The owner's approved warm architectural palette governs this map; the shared game/admin interface is unchanged. The creator kit map and validation guides were also inspected for footprint, scale, provenance and evidence requirements.

The wide backdrop is original generated scenery, extended on all four sides. Its small distant islands are decorative and not walkable destinations. Original illustration detail was scaled3× to fit the large campus composition; this enlargement does not create new native detail. Runtime close-ups, not just the overview, are supplied for owner review.

`campus-cleaned-original.png` is a built-in image edit of the approved concept: it removes baked café chairs/tables/stools and the oversized stage microphone, leaving continuous café paving for native separately layered furniture. The source approved image is retained unchanged.
