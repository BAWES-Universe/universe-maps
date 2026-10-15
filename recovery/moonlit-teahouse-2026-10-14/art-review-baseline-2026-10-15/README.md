# Moonlit visual candidate — unpublished

Open `comparison.html` for the before/after gameplay images. The PNGs in `deliverables/` are unedited browser screenshots, not rendered mockups. The before image is the saved r4 arrival; the after images were captured in this local game session at the same 1440×900 viewport with the normal Woka.

## What changed

The candidate restores a copy of the original N41 Moonlit Ruin Courtyard, at its native 48×32 tiles / 1536×1024 pixels. Artwork, collision, foreground, spawn and map-area layers are unchanged. `runtime/moonlit-review.tmj` adds only a local script and a transparent native-audio control layer. `scene.js` adapts optional camera and explicit audio controls from r4. The full r4 controller is preserved unchanged in `preserved/r4-controller.js` for future structural integration.

This is a demonstrably different visual result from r4, but it is restoration of existing art, not a newly authored teahouse. No pixels were edited, generated, stretched, recolored or pasted from another style. Tea Garden informed the desired distinction between preparation and serving destinations; its daylight architecture was not pasted into Moonlit. No additional districts were added.

## Visual assessment from actual gameplay

- **Woka scale:** same normal character scale as r4. Stairs and route edges now supply recognizable spatial references. The monumental architecture is still large relative to the character; it is the original scene's scale, not evidence that realistic furnishing or seating has been resolved.
- **Lighting:** warm lantern pools contrast with cool blue water, foliage and stone. This is baked artwork, not dynamic light simulation.
- **Route density:** open space is concentrated into medallion courts and connected by narrower stone approaches. Planting frames the route instead of occupying it as isolated placeholder circles.
- **Depth:** cliffs, waterfalls, balustrades, planted edges and the recovered foreground layer establish depth. Art is richly illustrated while the Woka is a simpler pixel sprite; this stylistic difference remains visible.
- **Navigation:** native `WA.player.moveTo` carried the character from the entry through the lower garden, mosaic court, upper ruins and gazebo approach. No teleports were used. The evidence records final coordinates and screenshots. This establishes those traversals, not exhaustive collision-edge coverage or multiplayer readiness.

The final optional-control observation shows a real overview camera transition and automatic return to the original walking zoom. Explicit audio enable created two playing audio elements (spatial bell plus silent carrier), and silence removed both. This verifies browser playback state, not subjective sound quality. The whole-scene capture shows thin horizontal tile seams at fractional zoom; this remains a rendering issue for the optional overview, and the normal walking screenshots are the primary art comparison.

## Exact asset gap — structural work stopped

The upper-left gazebo contains a statue and functions visually as a shrine. The recovered Moonlit runtime consists of assembled ground/object atlases and a small foreground atlas. It does not provide a separate matching glass facade, door animation sequence, removable opaque roof and complete furnished interior beneath it. Neither does the inspected Tea Garden runtime establish a compatible Moonlit glass-teahouse assembly. Exposing a roof fade over this baked scene would not reveal a legitimate interior.

Therefore roof/glass/animated-door/interior and tea-counter/table integration are not enabled in this candidate. Water retains its detailed original appearance; no new water animation is claimed. Required next asset: one stylistically compatible local teahouse assembly with separately usable roof, revealed interior, glazing/frames, door frames and counter/table surfaces. No crude replacement polygons were drawn. Original N41 and current r4 remain untouched.

## Review links and isolation

Local game URL (only in this executor while its stack is running):
`http://localhost:8000/_/moonlit-art-review-local/localhost:8081/moonlit-art-candidate/moonlit-review.tmj`

This is not a public preview URL. Browser requests and WebSockets were restricted to localhost; captured blocked-external lists are empty. The synthetic character is `Moonlit Art Review`. No shared world was registered or modified and nothing was published, pushed or deployed.

The executor briefly disconnected, then a new tool call confirmed recovery at 08:06:53 UTC. Candidate files and screenshots survived. Library saving of the four deliverable screenshots failed with `hosted apps tools/list request failed: network`; no Library IDs or successful upload are claimed. All screenshots remain available locally.

## Files

- `comparison.html`: side-by-side review, loading unmodified PNGs from `deliverables/`.
- `runtime/`: standalone local candidate plus untouched copies of original runtime files.
- `preserved/original-sha256.json`: hashes of original files, verified byte-identical in the copied runtime.
- `preserved/r4-controller.js`: original useful interaction implementation retained for later integration.
- `evidence/navigation.json`: actual native pathfinding destinations.
- `evidence/review-results.json`: browser observations, including expected isolated-stack media/service-worker/admin warnings.
- `evidence/controls.json`: measured optional-control observations; assess these independently of visual quality.
- `review.cjs`, `controls.cjs`, `harness.cjs`: reproducible local capture scripts.

No screenshot or source assertion here establishes final visual approval. These artifacts are for review.
