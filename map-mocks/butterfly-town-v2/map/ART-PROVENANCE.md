# Artwork and runtime provenance

Original gate, cliff vista, town ground, building exterior/interior and furniture alpha assets were generated for this project with OpenAI's built-in image tool on 2026-10-08. The inspiration is the monumental scale/reveal of a fantasy gate; no 33 Immortals screenshot, character, logo or copied game asset is included.

Town olive artwork is original AI-assisted art from the user's previously accepted Lantern Courtyard work. Source prompts and generation notes are retained in the source package's `art-source/` directory.

The art build performs tile-aligned crop/scale, source alpha reuse for cleaned architecture, and feet/canopy separation. Illumination, water ripples, butterfly frames, atmosphere, terrain, labels and collision masks are authored in code.

The unmodified Greg Woka appears only in the QA harness. It is not packaged in the runtime TMJ. The map adds no avatar or identity asset.

QA engine: Phaser3.86.0 and the Universe-pinned AnimatedTiles plugin, with extracted depth/body/layer-visibility primitives. Transport, camera focus and player event wiring are harness adapters; they are not the full Universe application.

Fork compatibility was checked against `BAWES-Universe/workadventure-universe` commit `b214491999a37b087930f984a547b4dc5b428fa0` and relevant methods found unchanged from earlier validated snapshots. Relevant sources include `CameraManager.ts`, `GameMapFrontWrapper.ts`, `Player.ts`, `GameScene.ts`, `WaScaleManager.ts`, and `MathUtils.ts`.


## V2 separation (2026-10-08)
Built-in image generation edited the original plaza into two registered 1536×1024 assets: an empty paving plate and a transparent scenery extraction. These preserve the original layout closely; they are not pixel-identical redraws. Source files live under art-source/v2. Foreground/feet tiles are deterministic, complementary masks of the alpha scenery with explicit flower-arch overrides. No opaque crop is layered over a duplicate baked town object. Generation used the built-in image tool, with no external paid-credit service. Collision supports were visually traced and rasterized to the engine’s 32 px grid; tree canopies are not treated as solid footprints.
