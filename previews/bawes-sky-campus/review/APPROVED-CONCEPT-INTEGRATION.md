# Approved concept received — integration blocked on matching source plates

The exact approved visual direction is saved unchanged at `source/approved-interior/concept.png`. It replaces the earlier schematic as the design reference. The owner approval remains valid; this is a source-production requirement, not a request to redesign the approved composition.

Transfer: commit `f33898d626b146aec02671e3f0339dabd808230d`, Git blob `bf4c8924632219be1c6747169cbbce8f626fc596`, SHA256 `113568cb5cfc93911a9a3d48485c2810aac94d32081695cd0a4ef16139f2f29e`. Verification passed. The file is **2172×724 RGB**, fully opaque; there are no hidden transparent object layers.

## Scale findings

The canvas includes considerable empty margin. Visual inspection places the complete illustrated envelope approximately at source `(32,52)–(2142,632)`, about 2110×580. This is an estimate, not a segmentation mask or collision boundary. A uniform scale of approximately 1.016 would place that envelope within the verified 2144×592 footprint; the visible composition's aspect ratio is therefore promising. Fitting the full 2172×724 canvas would be the wrong calculation.

[Native-scale study](APPROVED-CONCEPT-SCALE-STUDY.svg) shows the unmodified source and representative 32-world-pixel avatar extents. It is not an in-game capture. No Woka is resized, no nonuniform image stretch is proposed, and no gate or collision geometry is changed. Clearances must be measured against the eventual *usable floor and furniture bounds*, not this outer envelope. In particular, the existing 192px entrance and at least 96px clear internal routes cannot be inferred from the painted openings.

## Why a clean functional decomposition is not available from this PNG

- The curved reception, tables, chairs, sofas, plants and their shadows cover floor pixels that are absent from the file. Cropping objects does not reveal those pixels. Moving a crop would leave a duplicate or a hole unless replacement floor is painted.
- Several chairs are partly hidden by tabletops. Their complete silhouettes and table/seat foreground pieces are absent. A rectangular crop includes nearby floor, shadow or table pixels, repeating the previous sticker/occlusion problem.
- Amber glass is already composited with the floor and objects behind it. Treating those opaque painted pixels as a transparent gameplay panel would either cover an avatar or erase the intended scene beneath it.
- Wall/column joins, planting and floor shadows are merged. They are not independent complete wall runs, door leaves or foreground masks.
- The concept paints its own open entry doors. Keeping those in a backdrop underneath the liked existing gate would duplicate the gate. A clean matching threshold without the concept leaves is needed.

Using the image as a single floor backdrop would draw players on top of desks and wall fronts. Using it above players would hide them. Polygon cutouts alone cannot recover the missing pixels or chair views. Filling those gaps with prior library tiles, blur, unrelated furniture or generated patches would violate the approved single-family direction. No such patch was made.

## Exact minimum source changes to unlock implementation

Export these from the same approved composition, in its original coordinate system, with no art-style change and no baked Wokas:

1. **Clean floor/threshold plate:** complete floor under every furniture item and plant; no chairs, desks, tables, sofas, reception counter, object shadows or painted entry door leaves. Preserve the ivory pattern, integrated linework and approved lighting. Keep a clean central 192-world-pixel route after calibration.
2. **Complete object plates:** isolated curved reception, the two individual work settings, shared table, meeting tables, sofas, side tables and plants. Separate their cast shadows. Complete the portions currently hidden by adjacent objects. Do not export rectangular crops containing floor. Use uniform scale and preserve native aspect ratios.
3. **Architecture/glazing plates:** complete wall runs, columns, corners, door surrounds, removable door leaves and glass with meaningful alpha. Include the floor hidden behind translucent glass in plate 1. Room boundaries must remain continuous except at the declared entrances; no chopped wall fragments.
4. **Occupancy/foreground exports:** complete chair views matching each table-facing position; separate desk/table front edges, reception front, couch arms and chair fronts needed to overlap Wokas correctly. Declare each seat anchor, intended cardinal facing, approach side and object footprint in the same coordinates. Provide the opposite sofa view only if the approved outward orientation actually requires it.

A layered source document containing those exports is equivalent. This is a bounded preparation of the **approved image**, not a new unrelated kit, new layout, or paid generation request. No production service or generation tool has been called.

## Specific gameplay checks still pending

- **Sofas:** the visible cushion openings appear toward the image's lower boundary, while the transfer README calls them inward-facing. Do not silently rotate the painting: that would invert its perspective and lighting. Resolve the intended seat-facing declaration in the source export, then show native Wokas facing the town square. Orientation is not yet signed off.
- **Chair facing:** use the engine's existing approach movement and R rotation for actual cardinal directions. There is no supported map API for a true seated-pose animation or automatic chair-facing command. Every chair must be checked with an occupied native Woka; a metadata field is not proof of orientation.
- **Meeting rooms:** measure both complete boundaries and door apertures from calibrated plates; assign collision independently; verify 96px routes, shared courtesy locks, outsider blocking, occupant safe exit and reversal. The concept does not establish those measurements.
- **Occlusion:** place floor/base below the player layer and only appropriate foreground pieces above it. Check every seat, counter edge and glass wall at normal game zoom, including both sides of tables.
- **Exterior transition:** retain the existing exterior and gate. Register the new interior and window composite to the same footprint; verify roof-on/roof-hidden at identical camera positions. No new duplicate vegetation or second painted gate.
- **No popups:** retain the already verified prompt removal. Do not reintroduce coffee prompts, glow markers or new UI controls.

## Saved work and boundary

The approved original, provenance, source metadata and scale study are saved on the existing draft branch. The playable map remains at the popup-free checkpoint. Art, layout, runtime, gate and engine code are unchanged in this source-review pass. There is intentionally no claimed in-game replacement capture: no functional replacement has been integrated yet. Supplying the four matching source exports above is the specific remaining blocker before clean implementation can proceed.
