# Rebuild Reading Conservatory r2

Python 3 with Pillow and NumPy is sufficient for the deterministic map and review rebuild. Run from this extracted directory:

python tools/prepare_art.py
python tools/build_map.py
python tools/render_seat_proofs.py
python tools/check_release.py

The original approved artwork and every used generation output are retained in source-assets. Image generation is not rerun: the retained source images are the immutable inputs. Compiler placement, selective foreground splitting, proof overlays and all generated files rebuild deterministically. Raw character sheets and game-engine files are not included. The four full-scene character overlays are compiled review inputs with pinned per-frame provenance; they never appear in runtime maps.

## Optional fresh native replay

Use the authorized pinned native fixture described in ASSET-PROVENANCE.md. Put its three files in tools/native-fixture, or provide that path through NATIVE_FIXTURE_DIR. No engine code is edited.

node tools/verify_native_routes.cjs candidate
node tools/trace_seat_routes.cjs candidate
node tools/check_native_spawn.cjs candidate /path/to/pinned/start-and-math-typescript

The last command uses Node 24's built-in TypeScript transformation and the exact StartPositionCalculator.ts and MathUtils.ts source hashes documented in the capture. To replay a particular actual spawn outcome, set READING_SPAWN to a JSON pair such as [400,465]. The four captured positions are [400,464], [400,465], [401,464] and [401,465]. Source evidence includes the four-run summary and the full baseline route report.

Native proofs are tied to both map and layout hashes. The offline rebuild verifies these bindings; it does not rerun the engine fixture or represent frozen proof evidence as a new live test.

## Original source art

The approved concept stays unchanged. Runtime repair is confined to the documented two-desk nook, the two reading-rug furniture areas and the small mentorship-rug arrangement. Matching original chairs and tables are extracted by explicit masks, scaled and repositioned. The original architecture/scenery outside the bounded repairs is retained. Perimeter comparison is checked in SOURCE-PRESERVATION.json.
