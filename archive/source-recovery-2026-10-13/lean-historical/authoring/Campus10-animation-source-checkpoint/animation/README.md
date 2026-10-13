# Campus10 bounded native motion

The output is ready to integrate from `effects/effects.json`. This replaces the old river, fountain, and fire effects and adds one small ambient-life effect. The untouched Campus09 artwork remains the static baseline. World size 2944 × 2624, Standard32, Woka scale, collision, routes, buildings, basin, banks, and logs are unchanged.

The authoring method is editable SVG geometry rendered at native resolution with sharp. `build_native_motion.cjs` writes each distinct SVG phase and native transparent PNG. It does not translate or recolor a whole existing raster. `prove_motion.py` performs read-only composition and diagnostics. `compile_proof_map.py` compiles ordinary Tiled animations and reconstructs timed views independently from that TMJ. No image-generation service, browser, current-engine change, or publication was used.

## Exact integration specification

| Effect | Native world origin | Size | Frames | Timing | Loop | Layer |
|---|---:|---:|---:|---:|---:|---|
| Fountain | 816, 1344 | 240 × 152 | 16 | 100 ms | 1600 ms | below actors |
| River | 2736, 1248 | 208 × 1024 | 16 | 140 ms | 2240 ms | below actors |
| Fire | 2360, 1720 | 72 × 80 | 12 | 90 ms | 1080 ms | below actors |
| Garden life | 1968, 1400 | 192 × 96 | 16 | 160 ms | 2560 ms | above foliage |

All 60 PNG phases are distinct. Every effect has the same number of distinct visible phases after composition. These are four separate rhythms, not 60 scene-wide phases.

- Fountain: six authored jet trajectories carry three staggered light beads each. A thin constant aqua glaze slightly reduces baked white-jet contrast. Five basin centers emit independently phased expanding lower arcs. The basin/pedestal exclusion remains fixed. The moving details are actual travelling segments and changing-radius arcs, not an alpha change over a copied still image.
- River: 58 staggered ripple groups advect downstream by 27 native pixels through each local cycle. They fade only at the invisible wrap to keep the loop continuous. The water-only fixed pixel mask intersects an authored bank boundary, source blue-water color classification, source opacity, and empty above-layer ownership. Rocks, shore plants, stone, and lamps are excluded. The crop includes the previously frozen easternmost 16px. Flow covers many staggered rows throughout the corridor rather than ten 8px bands.
- Fire: small rear flame tips change shape, lean, and height; three embers rise. Transparent gradients retain the painted texture. Explicit log exclusion paths protect log shapes. A low-opacity local amber response can change their illumination. The broad painted pit and flame mass remain static by design.
- Garden life: two tiny insect loops above the existing flower bed, plus a restrained radial lantern aura. The lamp core remains painted and stationary. All eight occupied Standard32 cells are already permanently blocked planting/lantern cells. Frond animation was omitted because moving duplicated painted leaf tips would require static art removal; this bounded pass preserves that art.

## Ownership and depth

`source/*-pixel-owner-union.png` records every nontransparent effect pixel across the cycle. `source/river-water-owner-mask.png` is the exact fixed river clipping mask; the adjacent SVG records its coarse bank boundary. Fountain and fire SVGs contain their fixed clip paths. Masks are based on native pixels, not actor position.

No below-effect owner pixel has any above-layer opacity in the original09 composition. The exterior owner confirmed river water below y2272 will remain unchanged. The final integrated Campus10 composition still needs the same overlap/mask check after its exterior changes are composed.

## Timed native proof

- `proof/fountain-water-tmj-native-timed.gif`
- `proof/river-water-tmj-native-timed.gif`
- `proof/fire-flame-tmj-native-timed.gif`
- `proof/garden-life-tmj-native-timed.gif`

The same filenames ending `.png` are lossless animated PNGs, preserving native pixels and exact timings. GIFs use one shared palette for the full loop; PNGs are authoritative. Each view is 1:1 native resolution without heatmap or enlargement. Three small native phase sheets and exact PNGs at phases 0/3/7 support static review. `proof-map/magical-campus.tmj` is the actual source of the `tmj` timed proofs and refers to immutable09 static atlases by relative path. It is a bounded offline integration proof, not the final corrected Campus10 TMJ and not a live-browser playback claim.

`proof/tmj-verification.json` records valid ordinary Tiled references and exact selected-frame source-to-TMJ pixel matches. `proof/motion-audit.json` includes timings, distinct phases, placement cells, and visible movement measurements.

## Tile budget and dedup guidance

The proof uses five new atlas pages, each at most 1024 × 1024, totaling 536,753 PNG bytes and 2,046 stored tiles including independent animation roots. Pages: fountain 302 tiles; river 1020 + 537; fire 78; life 109. There are 158 occupied animated cells: fountain22, river121, fire7, life8. These counts include a dedicated animation root per cell; canonical frame tile pixels are deduplicated within each page.

Keep all frames of each cell sequence within its tileset page. Deduplicate identical RGBA frame tiles, skip unchanged cells, and reserve separate animated roots unless two placed cells have identical complete sequences and timings. A shared first/blank frame is not enough to establish animation identity. Adding metadata to a shared first frame can make unrelated cells play the wrong sequence. Separate below and above data layers avoid changing depth semantics. Do not merge independent timing groups into one cell.

## Final acceptance boundary

Reconstruct the final TMJ after the exterior pass, verify these PNGs round-trip at their exact origins, recheck opacity ownership and collision/head clearance at the life bed, and review its native timed clips. Browser playback remains unverified while the browser restriction is active. The proof source map was not modified, and all outputs are confined to this work directory.
