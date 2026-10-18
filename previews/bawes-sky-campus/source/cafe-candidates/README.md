# Cafe matching-source candidates

Source: exact owner attachment Library libfile_920640f873608191b578224ecf765372, archived at commit532e7da29f5c3122974e3be7ac2a9552df5c0a27. Input crop is original coordinates(90,625)-(480,930),390x305. Existing world destination from restoration-scope.json at82379a56399f7fdec32a7435616477018896ba2b is x2062,y3923,width1170,height915. Mapping describes location only; does not establish usable geometry.

Exactly two targeted built-in image edits, no other districts or implementation. Original preserved.

## Ground candidate
cafe-ground-candidate.png:1419x1109 RGB,2789877 bytes,SHA25626060f7ddbbc4f84a1cd21fbaad303c205a79e4c4c1ab13f6a2f2a8a00320bb4,Library libfile_d81c44ed5d8c8191b5cf34ba3e039bb9.
Restores warm timber deck and glass-roof bar, cups/shelves, pond/lilies/waterfall, lush planted rim, right stone connection. All loose seating/tables/stools removed; clean deck available. Aspect1.2795 nearly matches1170/915=1.2787; uniform downscale~0.824 can fit overall envelope, not registration.
IMPORTANT: exact boundary geometry was NOT preserved. Pond rock positions, deck curvature, railing/lamps, bridge stair geometry and waterfall exit drift. Perspective is more facade-dominant than desired orthogonal map art. Sky and cliff background are opaque. This is NOT a drop-in registered replacement or clean alpha island plate. Pixel-perfect boundary replacement would produce visible seams. Need deliberate boundary registration/masking and native-detail inspection before integration; do not stretch landscape nonuniformly to force a match. Bar is still large relative to native32px characters at full district scale; aspect fit does not prove object scale. No claim all geometry is suitable.

## Furniture candidate
cafe-furniture-candidate.png:1536x1024 RGBA,2128792 bytes,SHA256b06e6488219eede6d6e2e579884cd13647ef9678485c6c67131736cacd66b85f,Library libfile_f079ec82ebd4819192c8384e9907a7cb.
Transparent background verified(alpha0..254), inspected composited on white. Separate complete cream/red curved lounge front/rear, armchair four views, round tables with/without cups, two stools, straight stone-end timber bench front/rear. Matching warm illustrated family; no pasted floor rectangles. Atlas positions/relative sizes are arbitrary, not world coordinates. Stool views nearly identical, and side chair views slightly oblique; not complete validated cardinal sprites. Complete silhouettes help extraction but no foreground masks/shadows/anchors supplied. Bench is a new matching interpretation, not exact original bench extraction.

## Native-scale calibration proposals, NOT tested dimensions
Keep actual Woka32px atscale1. First compare uniformly resized armchair seat cushion width32-40worldpx to a native occupant; derive whole-chair size from that ratio, never resize avatar. Start stools with24-32px seat diameter; tables64-80px diameter; bench2seats96-128px long; curved3seat lounge144-176px long, then evaluate cushion capacity and perspective at native zoom. These are starting bounds rather than measured approvals. Full asset scaling must be uniform; don't give every asset one common atlas-to-world multiplier. Maintain at least96px clear access routes,64px seat approach targets, and explicit pond/cliff collision margins; verify actual usable bounds after art calibration. Separate foreground arms/backrests for correct Woka overlap. No sitting-pose API is supplied by these assets.

## Prompts summarized
1.Edit exact cafe crop: maintain framing/boundaries/bridge/pond/waterfall, restore crisp illustrated1170x915detail, remove all loose furniture/shadows, keep bar/canopy/perimeter planting. Actual boundary drift documented above.
2.Transparent complete matching cream/red timber cafe furniture and outdoor benches, front/rear/cardinal views, isolated no background/shadows/avatars. Actual view limitations documented above.
