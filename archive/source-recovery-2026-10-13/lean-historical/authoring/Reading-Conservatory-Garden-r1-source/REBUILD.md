# Rebuild the Fountain Garden variant

Python 3 with Pillow and NumPy rebuilds the retained source inputs without image generation or network access:

python tools/prepare_garden.py
python tools/build_garden.py
python tools/restore_evidence.py
python tools/render_proofs.py
python tools/check_release.py

The first two commands reconstruct the artwork, tilesets, eight water-animation frames, collision grid, native WAM areas and static checks. The next command restores frozen, hash-bound native replay evidence. It does not rerun the engine or claim a new live test. The last two commands recreate actual-arrival/route illustrations and verify every expected generated output hash.

## Optional fresh native replay

Provide the separately authorized, pinned portable native fixture through NATIVE_FIXTURE_DIR. Its three file hashes are in NATIVE-FIXTURE-PINS.json. Engine source and raw character sheets are deliberately excluded from this compact source package.

node tools/verify_native_routes.cjs candidate
node tools/trace_seat_routes.cjs candidate
node tools/trace_garden_routes.cjs candidate
node tools/check_native_spawn.cjs candidate /path/to/pinned/start-and-math-typescript

The spawn command requires Node 24 and the exact StartPositionCalculator.ts and MathUtils.ts pins documented in ASSET-PROVENANCE.md. Repeat the route command with READING_SPAWN set to [400,464], [400,465], [401,464] and [401,465] to reproduce all four real startup outcomes. Both clockwise and counterclockwise full fountain circuits are part of every route run.

Fresh evidence can differ in environment metadata such as the Node version. The default offline source rebuild uses the captured evidence exactly. Do not represent source-level replay as a live-browser or multi-user result.
