# Rendering: what changed, what still needs testing

**Nothing was deployed.** The higher-quality rendering experiment is isolated from the application. A separate resize bug has a small regression-tested fix.

## Actual live baseline

The default room in the cloud browser uses Phaser 3.86 Canvas: **787×505 bitmap pixels enlarged to 1181×758 CSS pixels**, with `image-rendering: pixelated`, at DPR 1. That deliberate nearest-neighbor enlargement explains chunky pixels. It is not a measurement of your device or the Studio/Reading candidate maps.

## Before / candidate comparison

See `RENDERING-COMPARISON.png`:

- **Source art:** original map tiles reconstructed at their native world-pixel size; no Woka in this reference panel.
- **Before:** small framebuffer, then nearest enlargement.
- **Filter only:** no difference on the observed Canvas path. Phaser's Canvas tile renderer ignores per-texture linear filtering when global antialias is false.
- **Native framebuffer:** more framebuffer samples, with Woka still nearest. Fractional pixel placement changes. It does not create missing artwork detail; it is not automatically a visual improvement.

These panels are **offline CPU reconstructions using Phaser's tile renderer**, not screenshots of an accepted browser fix. Original black edges, seams and possible atlas bleed remain unresolved here; no claim is made that either candidate fixes them. WebGL filtering could soften environment textures but requires edge/halo and shared-cache tests. A source-level check found another risk: these maps use complementary transparent cutouts in the floor/base and foreground. Linear sampling of those layers separately can create partial-coverage halos even when the source composite is opaque. A CPU half-pixel model reaches 75% coverage at some edges; that is a conditional risk, not a diagnosis of the current nearest-render screenshot.

At the same view and default zoom, the native candidate uses about **2.25× framebuffer pixels at DPR 1**, or **9× at simulated DPR 2**. Those are pixel-count estimates, not measured GPU costs. A shipping mode needs a sensible cap and desktop/mobile performance tests.

## Separate confirmed resize bug

When Explorer is zoomed out, resizing can leave the old camera zoom active after the app changes its canvas scaling strategy. In one reproducible case the camera stays at .6 instead of returning to1, showing too much world. The patch retains only the active, still-valid camera already managed by the scale service. It does not change default art or texture settings.

Final source regression suite: **26 pass after;10 fail /16 pass before**. These mock the Phaser boundary and are not live pointer/pan/zoom-anchor validation. Independent review passed for this narrow source-level scope. [Issue #841](https://github.com/BAWES-Universe/workadventure-universe/issues/841) and [draft PR #842](https://github.com/BAWES-Universe/workadventure-universe/pull/842) are open; no merge or deployment. Full local lint passes after standard code generation. In GitHub CI on the exact PR commit, Play build, iframe API build, typecheck, Svelte check, lint and formatting have passed; unit tests and remaining browser E2E jobs were still running at08:15 UTC. The earlier local Svelte export failure came from an incomplete/incompatible local dependency installation, not an established repository source defect.

## Remaining gate

The cloud browser cannot reach this workspace's private loopback server; file URLs are also unsupported. The prepared local Phaser fixture must run in a connected/saved coding environment before accepting a quality mode. Still open: real browser before/after, Canvas/WebGL, camera follow, controls and pointer alignment, mobile/touch, map transitions, Woka motion, UI, collision/seat/foreground behavior, and representative performance.

Existing zoom-control behavior: Zoom In multiplies by1.2 and Zoom Out by0.8. Their product is0.96, so one pair reduces zoom4%; this explains the live bitmap width787→656→820 sequence. Making the controls reciprocal is a separate UX choice, excluded from PR842.
