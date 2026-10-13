# Campus10 exterior source receiver

Native world: 2944×2624. The eight named owners cover the bounded office edge, northeast woodland, civic receivers, court/garden transition and market/shore landing. The full-scene generated image is a style guide only and is never enlarged into source pixels. Focused generated originals, exact prompts, native downsampled receivers, explicit masks and composition code are preserved.

Review the single integrated composition at `review/campus10-integrated-exterior-native.png`, with the half-size companion for navigation. The review is based on frozen09 and intentionally does not incorporate the independent door, seating or animation workers.

Run the normal isolated10 source assembly and the doorway source corrections first. Then call `apply_exterior.py PROJECT/layers`, or import its `apply(layer_dir)` function, before normal Standard32 compilation. This importer writes only the named static image layers. It does not alter collision, source rooms, anchors, animation, engine code or gate data. Do not apply it twice to the same already-composited layers; run the normal assembly again first.

`exterior-manifest.json` records registration and each owning mask. Source images are full-world transparent canvases and masks are separate. `mode: replace` intentionally clears old alpha where a new finite exterior silhouette removes the old crop/stub. Other owners alpha-composite. Every clearAbove mask describes an actual replacement ground/curb/art object; there are no actor-relative masks.

Current civic clear floor: classroom x608–672,y1472–1600; stage x608–704,y2080–2176. The actual floor mask is `masks/civic-clear-floor-contract.png`. Its 16px low coping outside the north/east edges is separately owned by `31-classroom-bay-edge`. The small bench-toe corner at x672–688,y1456–1472 retains the exact original composed RGBA in the low-foot base owner. No bench position, geometry or visible pixel changes. The parent owns collider and doorway changes. Main threshold remains x1216–1312,y992–1024 and gallery x1824–1888,y992–1024.

No source pixel or file in original09 was modified. No browser, live engine or external publication was used. Live playback and final compiled route acceptance belong to the integrated parent task.
