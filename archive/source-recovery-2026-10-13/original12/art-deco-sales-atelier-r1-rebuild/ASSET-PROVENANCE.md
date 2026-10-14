# Asset provenance and build boundaries

Two new local templates. No existing map, engine, service, live integration, or published artifact was changed.

## Original built-in image generation

The architectural artwork was newly generated at 1536×1024 using the built-in image generation tool on 2026-10-10 UTC. No paid external provider, signup, API key, subscription, or runtime service was introduced. These are image sources; the actual playable tilemap, collision, native foreground, spawn and optional WAM areas are separately compiled.

- sales-environment.png: original Art Deco urban atelier. Tool output exec-b23a0ec0-12d2-489a-b799-b5869509c24f.png.
- sales-environment-flat.png: bounded compass edit making the central artwork a clearly flush walkable floor inlay. Tool output exec-d0562df9-5152-426e-ae72-4756ed243779.png. This is the final runtime architectural source, used at its exact original size.
- maker-environment.png: original brick inventor hall with three flat creation pad floor markings. Tool output exec-d854af61-62f1-422c-9012-853dfaaf6a8d.png.
- maker-environment-open.png: bounded edit creating the genuine doorless opening into the southeast collaboration nook. Tool output exec-39fb2079-8531-4059-969c-fe900c7a09d7.png. This is the final runtime architectural source, used at its exact original size.

Generation/edit specs are preserved in GENERATION-PROMPTS.md. Source images are never treated as collision masks. Walkable tile cells were manually fitted to the final art, including room openings, furniture, southern piers, cabinet footprints, and planter bounds. Native32 movement and exhaustive head/body geometry are checked separately. The three creation-pad and two research-wing WAM regions have no activation properties: they are only named editor placeholders.

## Existing approved project assets

- chair-below-safe.png and chair-foreground-safe.png: user's grand-auditorium-01 split-layer native lounge chair. Used without scaling. Teal/brass matches the atelier.
- light-desk.png and light-meeting_table.png: user's social-outdoor-office-01/candidate/source/assets kit. Used at original native dimensions; the wood desk supports laptop research and the table supports workshop collaboration.
- low-lounge-table.png: user's grand-auditorium-03-foyer-terrace native brass/wood low table, used without scaling in each client lounge.
- industrial-chair40-native.png: original generated modern workshop task chair from overnight-events/esports-arena-01, already reduced once from its full master to 40×45 native pixels. The copied industrial-chair-provenance.json preserves its source crop and reduction. We did not upscale a small chair. Its exact lower backrail is split into the foreground; only tangent-head-unsafe pixels are transferred below avatars while retaining a byte-identical composite.
- greg-reference.png: user's grand-auditorium-07-clean native32 reference avatar. Used only for static occupied previews and geometry checks. No avatars are embedded in runtime maps.
- DejaVuSans.ttf and DejaVuSans-Bold.ttf: DejaVu fonts used in review card labels; their license is included. Runtime maps require no fonts.

## Native fixture and compiler

The compiler and validation harness are adapted from the already checked overnight-learning-work pipeline. Native movement fixtures retain unmodified pinned source extraction at engine commit 60e7afdc3f96ef32525597cd46bd41175d61a2ef and the included EasyStar 0.4.4. NATIVE-FIXTURE-HASHES.json freezes every fixture byte. HARNESS-RETURN-FIX.diff documents the sole return-click correction relative to the inherited harness: tile-center +15 selects the last pixel INSIDE the spawn tile; +16 selected the next tile. No engine code changed.

Each rebuild ZIP is self-contained with the selected final environment art, required native furniture, fonts, Python compiler, pinned movement fixture, guide and source layout. Rebuilding needs Python, Pillow, NumPy and Node.js; no network, API or image generation. Static previews are actual compiled-atlas renders. Live browser/device play, WAM editor import, multi-user voice/video and services remain untested.
