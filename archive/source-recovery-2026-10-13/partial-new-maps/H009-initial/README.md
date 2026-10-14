# Mechanical Orchard — H009 author checkpoint

A new complete walled orchard with three individually cam-driven tree sculptures and a matching enterable cam house. Copper petal vanes, verdigris leaves and brass fruit lamps visibly change in four untimed, explicitly advanced beats. Three cam profiles can be selected independently at the outdoor cranks or interior mechanisms. A completed performance may be copied to one temporary preset for this visitor only; loading restores draft cams, while a performance keeps its original snapshot. Full reload or confirmed reset clears the visit. Doors and Close preserve it. No audio, accounts, persistent saving, networked state or avatar vehicle physics.

## Status: unfrozen, author geometry gate blocked

This is runnable source, not source acceptance, live acceptance, publication or a completed delivery. Both main inter-island aisles have attractive clear paving but their complete-base 32px collision quantization leaves only one admitted tile at the narrowest points. `evidence/full-floor.json` intentionally fails those two whole-width bands. The original art, complete supports and failure evidence are preserved. See `AUTHOR-CHECKPOINT.md` for a precise repair handoff. No READY or freeze is issued.

## Build and inspect

Requires Python 3 with Pillow and NumPy, and Node with built-in `stripTypeScriptTypes` support. Native route methods are source-pinned and bundled under `tests/native`; this project changes no engine source.

Run `bash tools/rebuild.sh`. It rebuilds from original artwork and author sources, executes all other offline suites, then deliberately exits nonzero at the still-red full-floor width test. All test outputs are under `evidence/`. A clean copy has not been run; coordinate storage with the parent before creating one.

Main map: `runtime/mechanical-orchard.tmj`, WAM: `runtime/mechanical-orchard.wam`, controller: `runtime/mechanical-orchard.js`. Source controller and layout generator live under `source/` and `tools/`. The complete original imagegen art and exact prompts are in `art/`, with generation provenance. `CANDIDATE.json` records exact current source/runtime hashes without claiming readiness.

## Geometry and visible-state design

The three low tree sculptures remain wholly inside planted islands rather than overhanging pedestrian paving. Every complete island/rim, crank base, bench apron/foot, open door face, room cabinet and relevant garden frontier is traced as a solid. Phase patches are registered generated-art selections inside permanently blocked planted areas; all 27 independent pose combinations have the same collision. Original opaque whole-scene art remains under the semantic lower branch-back pixels.

Two bent-branch benches are genuine contact locations. Proofs use the real unchanged 32px standing Woka and its 16px body, native arrivals, directions and central lower torso contact. They do not implement sitting, autosit, forced facing or a new avatar animation.

Only the true exterior startup rectangle is quiet; neither room as a whole nor either same-map doorway is silent. The whole orchard and interior have coherent scenery extending to their own image boundaries. This does not establish live camera bounds or renderer behavior.

## Offline evidence and limits

The fixture executes all ordered native desktop/touch anchor pairs, every admitted floor cell's fit extrema and center, all 256 real random-start outcomes, and continuous body sampling at no more than 0.5px. Controller tests exhaust all 27 cam choices across four beats and probe invalid actions, repeated callbacks, replay, preset independence, state retention, disposal, and async transition/recovery order. Static scale tests compare emitted tile decoding against whole-scene rational-nearest composition at six scales.

Source/static plates are not game screenshots. Numeric raster equality does not establish GPU filtering, fractional camera positions, zoom/resizing, live desktop/mobile/touch interaction, networking, AV or independent semantic artwork acceptance. GitHub source, spreadsheet row and preview links are pending, not invented.
