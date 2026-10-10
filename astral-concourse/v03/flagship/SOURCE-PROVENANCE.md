# Flagship v03 source, provenance and rebuild

This intentionally small repository package contains the complete nine-file runtime and its setup/validation documentation. The full editable source and forensic movement evidence are preserved in the owner-held archive delivered with the map:

- Filename: `astral-flagship-v03-complete-source.zip`
- Exact size: 229,106,239 bytes
- SHA-256: `936f74a8b145c0e137d4fd7621619d415aae94922a376be6786aacd7c587cb89`
- Runtime-and-setup ZIP: `astral-flagship-v03-runtime-and-setup.zip`, 6,800,685 bytes, SHA-256 `e076e97d4163095787cb70a27e6674dc1133497c44efd02d5222153e0b19edb5`

These archive filenames identify the separately delivered backups, not public repository download links. Their original documentation records the pre-publication local freeze; the nine runtime bytes are identical to this package. The complete-source ZIP is deliberately not committed. Its raw 297,464,656-byte route sample stream is stored gzip-compressed in the archive and is not a runtime dependency.

## Source contents

The complete-source archive includes `source/` generated masters, exact generation prompts, explicit layout and collision/quiet grids, preserved v01 input pixels, furniture and divider components; `assets/` authored compositions; `tools/` build/render/verification scripts; `review/` native-scale visual evidence; `validation/` engine-source audit, current schema/zone checks, source-matched movement model and independent replay evidence; `ART-SOURCE-FREEZE.json` and `SOURCE-FREEZE.json` inventories. The original portrait inputs are excluded.

## Rebuild from the complete-source backup

Verify the archive SHA-256, extract it into a separate directory and use its package root. Python with Pillow and NumPy plus Node.js are required. Preserve a copy of the frozen runtime before rebuilding.

1. `python tools/build_runtime.py`
2. `python tools/verify_runtime_geometry.py`
3. `FINAL_ROUTE_AUDIT=1 node tools/test_native_routes.mjs`
4. `python tools/render_runtime_reviews.py`
5. `python tools/verify_runtime_package.py`

The archive's `tools/rebuild_art_portable.py` uses included input copies to reproduce the initial art checkpoint; `tools/assemble_art.py` preserves the original assembly. Runtime registration and later low planted bay-edge refinements are applied by `build_runtime.py`. Compare rebuilt outputs with this package's `RUNTIME-MANIFEST.json`. Do not silently replace frozen published assets if dependency or encoding changes produce a different hash. The standalone `tools/verify_runtime_manifest.py` in this repository requires only Python and does not rebuild or mutate runtime files.

## Provenance

New lounge furniture, rugs, plants, welcome desk, garden scenery, pergola, railings and low planted dividers were generated for this project with the image tool, then registered to native scale. Hall/chair/podium and cafe components are reused project-authored assets. No Conference Campus pixels are redistributed. This package does not invent a new licence or claim third-party assets are CC0.

- [Original civic furniture provenance](https://github.com/BAWES-Universe/universe-maps/blob/03d83f2/map-mocks/civic-rooms-01/source/provenance.json)
- [Original chair generation record](https://github.com/BAWES-Universe/universe-maps/blob/03d83f2/map-mocks/expanded-office-02/source/frozen-review-package/art-meeting/source/generation-record.json)
- [Greg native-scale reference provenance](https://github.com/BAWES-Universe/universe-ai-creator-kit/blob/67382dc97f494c230e93f0cf67e478df6e5b6d17/docs/catalogue/wokas.md#reference-greg32-map-fixture)

Greg Gulf-outfit v3 is the unchanged project-authored review fixture, SHA-256 `e88ba016c58f6bc7616c831c3c56a4656e66772794940af93c0c0835e85a987d`. It is not an upstream WorkAdventure sprite and is excluded from the runtime closure.

The offline movement/schema inspection is pinned to engine commit `b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af`. It is not live renderer, media, deployment-override or load verification. The setup guide records the source limitations and acceptance tests still needed for an actual room.
