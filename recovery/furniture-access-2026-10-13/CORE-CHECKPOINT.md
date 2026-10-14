# Furniture access: first runtime checkpoint

This first checkpoint contains exactly **317 payload files**: 311 dependency-complete runtime files, three manifest.json files and three restore_revision.py scripts. They restore **28 maps**: 22 reviewed revisions, five additional revisions and one partial Butterfly café revision.

The descriptor was prepared and all payload paths, sizes, SHA-256 values and Git blob SHA-1 values were verified locally against initial-manifest.json. It does not by itself confirm a remote upload or commit. CORE-BACKUP-MANIFEST.json lists the exact expected Git paths and all 28 map IDs. These two checkpoint descriptors are outside the 317-file payload count.

## Restore

For each of reviewed-revision, additional-reviewed-revision and cafe-reviewed-revision, run its restore_revision.py with --bundle pointing to that bundle directory and --output pointing to a new, nonexistent destination. For example:

    python recovery/furniture-access-2026-10-13/reviewed-revision/restore_revision.py --bundle recovery/furniture-access-2026-10-13/reviewed-revision --output /new/reviewed-runtime

The restore scripts verify every source file before copying and each destination hash after copying, and refuse an existing output directory. Use separate new destinations for the three bundles.

## What follows separately

This is a complete runtime-recovery checkpoint. It is **not yet the complete sealed source/proof bundle**. A subsequent checkpoint will expand coverage to all 433 sealed-snapshot paths, including QA/proof records and historical integrity seals, plus the bounded source/fixture supplement and prerequisite/portability ledger. The complete snapshot includes these runtime paths; it is not 433 additional runtime files. Sanitized metadata copies are accounted for with original/published hashes and an explicit redaction ledger.

## Preservation and limits

- All 596 original collection files were independently rehashed and remain unchanged. Original paths and public URLs are preserved.
- N39 Volcanic Observatory Lodge, N40 Coral Research Pier, N41 Moonlit Ruin Courtyard and N48 Acoustic Cave Hall are excluded from the runtime revisions and unchanged.
- Exact frozen checkpoint scope: 28 maps and 1,364 removed collision cells. All 28 empty-scene RGBA comparisons match the originals.
- Butterfly changes only its two accepted café cells and the associated isolated depth repartition. Three larger-loss openings and real/shared supports remain.
- No live Phaser or authenticated WorkAdventure PASS is claimed. Static/native-avatar composites and limited source replay do not establish live gameplay acceptance.
- No deployment, publication, release publishing, merge, sitting animation or interactive-seat behavior is included.
- Later Mission Control and Tea floor candidates are separate and excluded from these checkpoint files and counts.
- This checkpoint guarantees exact runtime restoration when its manifest hashes verify. It does not claim a complete portable source rebuild.
