# Archive verification · 2026-10-09

- Original archive baseline: 14 design folders, with 12 canonical TMJ files across 10 Tiled candidates, 3 visual-only designs, and 1 offline art/lighting study.
- 217 local runtime/asset references checked, including PNG dimensions, TMJ/script links, dynamic map-relative imports, prefab image paths and audio paths.
- Original canonical TMJ hashes and per-folder checksums pass. Frozen v1 and the aligned Lantern canonical TMJs match the existing published repository snapshots.
- All four included compositors/builders run from isolated copies and reproduce their archived screenshot bytes exactly.
- The two archived Lantern validators pass 2,251 and 2,254 offline checks after their hosting-URL assertion is adapted to the local archive.
- Both baseline and archive-branch `npm run build` pass. The exact same 10 published map inputs are discovered, and no archive content appears in `dist/`. A separate read-only review confirmed the discovery helper does not traverse the archive.
- Existing published files, application source, dependencies, pipeline configuration and template list are unchanged. Only map discovery gains an archive-directory exclusion.

## Explicit gaps

The two StudentHub maps retain historical area objects lacking required `visible` booleans. Their pinned build-schema rejection is documented, rather than silently changing original TMJ bytes. The connected-glass proof also retains its known proximity-conversation `silent` bug.

The pre-water v2 fragment lacks a complete independently frozen historical asset set and is not validated as a standalone map. Static proposals have no TMJ. Source-harness screenshots are not a new full-client, multiplayer, device, native-room or audio-listening acceptance.

No candidate is merged, deployed, or added to the live template catalog by this archive. See `validation-summary.json` for the concise machine-readable results.

## Arrival art study addition

The final open/covered/threshold renders retain their original bytes and native dimensions. The final Blender scene and earlier brown maquette were reopened in Blender 4.3.2 after portability-only path cleanup. All packed image hashes and object/mesh/material counts match their source snapshots. Decoded archive files contain no environment-specific paths, external libraries or embedded scripts. The earlier 13 candidate folders remain byte-for-byte unchanged.

No Cycles rerender or gameplay export was performed during archiving. The included scene builder produces draft authoring renders, not an exact recreation of the final avatar-composited review images. There is no TMJ or play link, and the unvalidated compiler/harness, backup `.blend1` files, logs and intermediate renders are excluded.

## Latest source and draft preservation

- 26 top-level design snapshots are now indexed: 10 original Tiled candidates, 10 visual proposals, 5 source-review modules, and 1 Blender art study. Subordinate attempts include layout02, failed fixture registration, rejected garden and avenue masters, and historical office inputs.
- All original 14 candidate folders remain byte-for-byte unchanged from PR3 head d818e6c4c001e5fa7ba76e02663a1fb9ce9460fd. All live/published paths remain unchanged by this update.
- Latest candidate checksums, source-copy hashes and local Markdown links are checked. Text-only machine-path normalization is listed per new folder. Source-review bundles retain historical implementation artifacts; the archive validator does not assert runtime portability or playability for them.
- The canonical-map validator still checks 12 original TMJs and 217 local references; new source-review TMJs are preserved as historical inputs, not promoted into that acceptance count.
- The office02 exact immutable review package is included. Runtime03 is independent: its reported wall overlap and top-left-chair exit through a neighboring conversation bubble remain known issues despite historical physics checks.
- Liked office/garden visual direction is distinguished from unverified live behavior. River root demo is superseded; native static integration is preserved with final readiness unconfirmed. No merge, deployment, new live template, service configuration or broad licensing change.

### Latest execution checks

TypeScript `tsc --noEmit` passes, and direct execution of the unchanged discovery helper returns exactly the same 10 published map inputs as the saved baseline, excluding the archive. A fresh full build was attempted but the process was killed during existing tileset rendering; it is not recorded as passing. Earlier baseline build results above are historical. Independent archive-only review passed checksum completeness, all added Markdown links, 16 local source-TMJ asset references, provenance and privacy checks. Original vendor whitespace and historical trailing blank lines are preserved rather than rewriting source bytes.
