# Restore reconstructed editable sources

This tree includes selected editable source and tests for these reconstructions. Each reconstructed source is already saved in the authenticated Library artifact pinned by its asset manifest. All members, including omitted assets and larger test evidence, are mapped by exact hash. Restore the full archive with the baseline restore-tool before running a full build or test suite.

- Keeper: restore keeper-r2-reconstructed.json beneath the recovery root. Then use its tools/restore_art.py with the original Keeper runtime Library ZIP pinned in dependencies/keeper-original-runtime.json. All 19 runtime files reproduce exactly; the inherited teleport-race regression remains a known failure. This is newly reconstructed editable authoring, not the unavailable original source archive.
- Studio/Reading: restore studio-reading-reconstructed.json. Its Library archive includes all unchanged PNG inputs. Eleven shipped outputs reproduce byte-for-byte. Live GPU/body/head/touch/multiplayer acceptance remains open.
- Media: restore media-r7c-partial-reconstructed.json and the original r7c source dependency in dependencies/resonance-media-house-r7c-source-replay.json. Supply that restored source to tools/reconstruct.py as --baseline, following the package README. The source-only Library checkpoint requires original artwork, which is mapped separately. Missing r9 and its visual repairs remain unavailable; this package does not claim they were recovered.

No signed download URLs, access credentials, artwork copies, runtime duplicates, merge or deployment are included in the source-tree additions.
