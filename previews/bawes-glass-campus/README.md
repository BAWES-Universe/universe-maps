# BAWES glass campus — playable review candidate

A new, isolated campus with an outdoor town-square spawn, a folded glass tower, shared daily work and meeting tables, outdoor social seating, and a connected study court reserved for the future StudentHub wing. The tower art follows the modern four-part BAWES mark; Universe Ink and violet/blue glass replace the historical red/orange/brown identity. No labels or wordmarks are baked into the map.

**Actual-client checks have run; owner visual acceptance remains open.** This is a draft review candidate, not a deployed world. Existing maps, Azure, engine source and deployment configuration are unchanged.

## Explore and inspect

- `campus.tmj`: orthogonal **64×34**, native **32px** cells. Outdoor spawn at cell **(22,22)**. Six-cell / **192px** entrance spine and cross-campus promenade.
- **28 reachable chair positions**, **10 blocked table footprints**, **1,846 connected walkable cells**. The eastern study court is usable now and reserves space for StudentHub on this same map.
- Daily work/social groups face the square. Rear shared project/meeting tables and outside café tables provide other uses without inter-map portals. Furniture has reachable occupied positions, separate near backrests, and clear exits. Wokas retain their native upright animation; there is no custom sitting pose.
- Local facade/roof cutaway is initialized correctly both outside and inside. Permanent walls/collision stay separate from the removable cover. Outside observers retain the glass facade while an inside observer sees the cutaway.
- A reflecting basin uses **48 frames × 40ms**, a continuous 1.92-second loop. Spawn and walking have no map audio, popups, quests, notifications or teleport gimmicks. The conversation-disabling `silent` property is absent.

[Outside with a real second occupant](review/client-outside-occupied.png) · [Inside with cutaway and occupied chair](review/client-inside-occupied.png) · [Normal-camera arrival](review/client-spawn-final.png) · [Whole campus, zoomed out in the actual client](review/client-overview.png) · [Actual-client motion movie](review/client-motion.mp4)

The overview uses five normal Zoom Out button clicks; it is **not** a default-camera view. At 1440×900, normal gameplay uses a 720×450 game canvas displayed at 2×, zoom modifier 1, Phaser camera zoom 1, and Woka scale 1. The outside/inside/arrival screenshots use that normal state. Offline `layout.png`, `outside.png` and `inside.png` remain explicitly separate from the client captures.

## Verified in the local client, 16 October 2026

Target: BAWES Universe engine **274114560c5ec95fdf8e51e67986a53069f3cf06**. Node 22.22.0, frontend Vite 5.4.21, system Chromium, software WebGL, isolated local back/pusher/map host and anonymous synthetic users. No production auth, admin, media service or live room was used.

| Check | Observed result | Evidence |
| --- | --- | --- |
| Final campus routes and seats | **91/91 passed**, including all 28 seat approaches, occupied positions and exits, arrival, central aisle, study court, pond and return | `review/client-routes-final.json` |
| Keyboard table boundaries | **40/40 passed**: all ten tables approached and pressed against from four sides, no body intersection | `review/table-boundaries.json` |
| Doorway across its full width | **6/6 enter/leave cycles passed**; cover hides inside, restores outside, permanent wall stays solid | `review/door-wall-checks.json` |
| Interior perimeter walls | **4/4 keyboard checks passed** with cover hidden | `review/door-wall-checks.json` |
| Two independent users | Outside user sees a real second Woka through the ground-floor glass; inside user has local cutaway, outside cover remains visible | `review/two-client-result.json` and paired screenshots |
| Basin animation | 144 actual captured browser frames over 6.24 seconds, with changing native tile IDs across multiple loops | `review/motion-final.json`, `review/client-motion.mp4` |
| Source loop seam | Last→first pixel change is within the range of ordinary adjacent frame changes | `review/animation-source-check.json` |
| Repository build | **11/11 maps optimized**, including this campus and bundled reveal script; no deployment | `review/build-report.txt` |
| Static connectivity/assets | All 1,846 walkable cells in one component; all seats and exits reachable; assets and layers intact | `review/static-validation.json` |

Source tests are in `source/validation/`. The earlier 67-check sweep is retained under `review/historical-first-sweep/` and must not be presented as final-coordinate evidence. These tests cover the named routes and objects, not exhaustive traversal of every possible path or physical-device performance.

## Visual findings still open

- The tall folded crown is cropped above the **normal arrival camera**. The broad illuminated entrance and front seated occupants are visible. The separate zoomed-out client view shows the full silhouette; do not use it to claim full default-camera visibility.
- The facade is substantially more detailed than the interior furniture and landscape. The interior remains spare; visual cohesion needs owner review and likely another art pass.
- Upper tower storeys are an architectural facade, **not additional explorable floors**. Actual occupant visibility has been demonstrated in the ground-floor frontage, not in every upper pane or every interior position.
- Chair overlap is real layering, not a new seated animation. Fine facade frames can cover a Woka directly behind them, as expected for opaque mullions.
- The recorded motion is actual software-rendered Chromium output. The source loop is continuous; no perfect-60fps, physical-device or audio-communication claim is made.
- A shared map and sightlines do not guarantee arrival awareness. There is no notification engine, lead routing, acoustic isolation, meeting service, or completed StudentHub product integration.

## Reproduce

With Python 3 + Pillow and Node:

```sh
python3 previews/bawes-glass-campus/source/build.py
python3 previews/bawes-glass-campus/source/validate.py
node previews/bawes-glass-campus/source/test-reveal.cjs
```

The compiler preserves separate ground/furniture, backrest, glass-cover, animated-water and invisible collision layers. It authors collision explicitly rather than inferring it from image colors. See [local runtime setup and exact commands](source/runtime/README.md). A static host or offline composition is not the game client. No public play URL is deployed.

## Sources and rights

- New branch based on `universe-maps` master **adabef710832cbb4a1662a8b9f77a493b4e5ecf3**. Root/folder READMEs, package/build configuration and deployment workflow inspected; no AGENTS.md exists at that revision.
- Game **274114560c5ec95fdf8e51e67986a53069f3cf06**: `play/index.html`, `docs/brand/README.md`, `docs/brand/bawes-lettermark-white.svg`. Ink **#14121E**, purple **#8629FC**, blue **#4156F6**. The exact supplied source mark is retained in `source/lettermark.svg` as the architectural reference; the generated facade is an interpretation, not a mathematically exact retrace.
- Orbit is the admin application: `workadventure-universe-admin` **83b5e70715322a4d45cb1b292723b6e39315f08b**, `app/globals.css`. Soft violet **#C4B5FD**, star gold **#E9C74C**, neutral raised planes and selective accents.
- Same game revision: `GameMapFrontWrapper.ts` draws layers after `floorLayer` above players and changes collision when hiding layers. `Api/Iframe/room.ts` and `player.ts` provide local reveal events and initial position. The cover contains no permanent blockers.
- Tower study and transparent foreground cutout were generated with the built-in image tool, using this candidate's original mark-derived blockout as reference. Full outputs remain in `source/tower-study-original.png` and `source/tower-cutout-original.png`; prompts and compilation anchors are in `source/ART-PROVENANCE.md`. Ground, furniture, water and gameplay masks are original procedural assets. No people are baked into artwork. No third-party historical reference art was copied.
- [Universe Creator skill](https://github.com/BAWES-Universe/universe-ai-creator-kit/blob/main/skills/universe-creator/SKILL.md), map guide, experiment history and validation were inspected. Skill blob `cbc1cf7b5d196c760e1d8832f800fe637f4e9c2d`; map-guide blob `e0d1947e91600e642eed60ac3fa80340cab8fa11`.
- The historical Library references could not be resolved in this delegated session. Their pixels were not inspected; supplied descriptions were used only as background context, with the modern direction taking precedence.

Source, art, runtime scripts and tests are backed up in draft PR #21. No merge, public deployment or new external paid service is part of this work.
