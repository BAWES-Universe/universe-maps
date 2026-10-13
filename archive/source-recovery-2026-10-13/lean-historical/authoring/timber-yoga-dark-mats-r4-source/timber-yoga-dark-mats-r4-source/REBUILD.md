# Self-contained reconstruction

Requirements: Python3, Pillow and NumPy. Tested with Python3.12.14, Pillow12.3.0 and NumPy2.3.5 in the task environment. No network, generation, credentials, raw sprite sheets or external source directory is needed.

Run `python tools/rebuild.py` from any working directory. It rebuilds `timber-yoga-dark-mats-r4/`, independently decodes TMJ to check art/geometry/depth/roles/mats, verifies captured native evidence against exact rebuilt inputs, and compares every output file with EXPECTED-OUTPUTS.json.

The compiler uses full-resolution baseline native layers, the retained Movement border master and explicit native32 geometry. It never halves the previous collision grid. It regenerates packed atlases, WAM, layout, native32 static proof and diagnostics. Base/foreground split uses the original scaled foreground mask plus explicit head-safe elevated architecture; empty composition stays pixel-exact.

## Native replay boundary

The included evidence was freshly produced on these exact inputs with the unchanged pinned native movement fixtures. Optional raw engine source, EasyStar bundle and private test runner are intentionally omitted from compact distribution while redistribution closure is uncertain. Rebuilding attaches the recorded evidence only after its input SHA-256 matches; it does not claim to rerun the engine. Exact fixture/runner hashes, commits and full routes remain in evidence/NATIVE-ROUTES.json. Independent verification with separately available pinned fixtures can rerun those methods.

Original accepted1536×1216 runtime atlases, layers, assets and layout are retained in baseline. Original source and runtime archive identity is in source-assets/BASELINE-PROVENANCE.json. Baseline hashes are checked before compilation. No original files are overwritten.
