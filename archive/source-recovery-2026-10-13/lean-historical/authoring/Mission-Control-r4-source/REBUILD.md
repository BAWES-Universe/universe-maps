# Mission Control r4: operator backrest correction

Run `python tools/build_mission.py`, then `python tools/check_head_geometry.py mission-control-center`. Python3, Pillow and NumPy are required. Runtime rebuild uses frozen assets, no network or new image generation.

The six operator chairs move15px south to the bottom of their existing native floor cells, with full rear chair widths protected. Upper desks move15px south; lower desks12px so their complete feet stay above the walkable row. All six exact native authored tap arrivals match the new anchors. Cushion remains below the Woka; a low lumbar rail is above the lower torso. No sprite pixels are erased. The original wheel/base pixels are retained. Approved sky, architecture, briefing and room properties are unchanged.

`tools/prepare_lowback.py` reproduces native chair ownership from the frozen imagegen master. `tools/shift_consoles.py` reproduces bounded console composition from the r3 source and frozen generated clean floor. Existing console pixels are translated, not redrawn.

Proofs show existing standing idle sprites, not new seated animation. Full upper14 head union passes across admitted body positions. At exact arrivals the upper18 rows are clear; at the last southern1px the rail can meet one shoulder/back-edge row. This is separately rendered and reviewed rather than hidden by moving the rail behind every character.

Source-native routes were independently tested using the pinned extracted engine fixture. That optional third-party engine fixture is not redistributed in this source ZIP; the test receipt and exact provenance are retained in verification/. No live multiplayer, browser, AV or deployment claim. No engine changes. The separate local/remote entity-depth issue draft is unrelated to this static map-only workaround.

## Preview licenses
Raw Pipoya sheets are excluded from this source package. Their repository provenance is in source-assets/WOKA-PROOF.json. Optional varied preview tools reference those licensed assets. Runtime rebuild and derived head-mask tests do not require redistribution of raw sheets.
