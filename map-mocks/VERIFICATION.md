# Archive verification · 2026-10-09

- 13 design folders, with 12 canonical TMJ files across 10 Tiled candidates and 3 visual-only designs.
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
