# BAWES glass campus — first architectural blockout

**Experimental, not a finished map or a gameplay-tested tower.** This starts the separately authorized BAWES build; no existing map was edited. No deployment or live world registration is part of this branch.

The four exact folded paths from the modern white mark define the glass elevation. This initial geometry study establishes their proportions, a continuous outdoor arrival and a shared workspace. It still needs architectural depth, finished materials, useful landscape boundaries and actual-client evidence before expansion. The transparent silhouette currently reads as an elevation study, not a finished volumetric tower.

## Current deliverables

- `campus.tmj`: orthogonal 64×48 map, native 32px cells; outdoor spawn at cell (22,34).
- `ground.png`, `seat-backs.png`, `tower-glass.png`, `logic.png`: independent image-backed layers. Collision is authored explicitly, never inferred from artwork.
- `runtime.js`: local facade/roof-cover reveal, including initial inside state. Permanent collision remains on its own layer. No ambient audio, `silent`, walking popups, portals or notification engine.
- `source/build.py`, `source/lettermark.svg`, `source/layout.json`: reproducible original blockout and exact folded source geometry.
- `review/layout.png`, `outside.png`, `inside.png`: **offline blockout exports without avatars**, not client screenshots. No people are baked into art.
- `source/validate.py`, `source/test-reveal.cjs`: static geometry and mocked reveal checks; see results in `review/`.

## Campus plan

The main arrival spine and transverse promenade are six cells / 192px wide. A six-cell entrance opens directly toward the town square. Daily work/social seats sit along the entry frontage, with a central unobstructed aisle and rear shared project/meeting tables. Outdoor café groups flank the square. The eastern 17×14-cell plot reserves StudentHub facing the same square; it is currently an open placeholder, not an implemented service or another map.

This version has 20 reachable chair positions and six blocked table footprints. Chairs have separate foreground backrests, but seating appearance and body alignment remain unverified. No sitting pose or seat interaction is claimed. No acoustic isolation, video meeting integration, lead notifications or guaranteed arrival awareness is claimed. A connected room can improve sightlines; it cannot ensure that a team elsewhere notices a visitor.

The next layout pass must remove unassigned empty perimeter area or give it a useful garden/meeting purpose. Do not enlarge the campus before validating the entrance and one daily workspace group at normal camera scale.

## Reproduce

From the repository root, with Python 3 + Pillow and Node installed:

```sh
python3 previews/bawes-glass-campus/source/build.py
python3 previews/bawes-glass-campus/source/validate.py
node previews/bawes-glass-campus/source/test-reveal.cjs
```

Open `campus.tmj` with its adjacent files in the pinned Universe client. A static file server or offline PNG is not that client. No public play URL exists.

## Source and design contract

- New branch based on `universe-maps` master `adabef710832cbb4a1662a8b9f77a493b4e5ecf3`; root README, folder READMEs, package/build configuration and deployment workflow inspected. No AGENTS.md exists in that revision.
- Game `274114560c5ec95fdf8e51e67986a53069f3cf06`: `play/index.html`, `docs/brand/README.md`, `docs/brand/bawes-lettermark-white.svg`. Ink `#14121E`, purple `#8629FC`, blue `#4156F6`; exact four paths retained in `source/lettermark.svg`. The supplied brand asset remains BAWES's; no third-party reference art was copied.
- Orbit is the admin application: `workadventure-universe-admin` `83b5e70715322a4d45cb1b292723b6e39315f08b`, `app/globals.css`. Soft violet `#C4B5FD`, star gold `#E9C74C`, neutral raised planes, selective accents. Supplied modern direction takes precedence over historical red/orange/brown identity.
- Same game revision: `GameMapFrontWrapper.ts` draws layers after `floorLayer` above players; `setLayerVisibility` also changes collision. Cover contains no permanent blockers. `Api/Iframe/room.ts` and `player.ts` provide reveal events and initial position.
- Universe Creator skill and handbook inspected: [skill](https://github.com/BAWES-Universe/universe-ai-creator-kit/blob/main/skills/universe-creator/SKILL.md), map guide, experiment history and validation. Skill blob `cbc1cf7b5d196c760e1d8832f800fe637f4e9c2d`; map guide blob `e0d1947e91600e642eed60ac3fa80340cab8fa11`.
- Supplied historical Library IDs could not be resolved in this delegated session. Their pixels have **not** been inspected. Historical themes are reported brief context only.

## Required next proof

1. Restore a separate local full-client stack at the pinned game revision; the saved environment currently has source/dependencies but no running play/back/pusher stack. Do not reuse or interrupt Azure's runtime.
2. Capture actual desktop gameplay at normal camera/Woka scale: outdoor spawn, approach, doorway, occupied seat and return. The full tower should be legible without requiring an overview camera; its current height needs this check.
3. Use two real clients, one inside and one outside, to test actual occupants through the glass. Tune pane alpha and mullions against real face/body visibility; a transparent PNG alone does not pass.
4. Walk all visible routes with keyboard and click movement; approach every table on four sides, enter/exit each seat, and repeat collision checks after roof/facade enter/leave transitions and reload inside.
5. Replace the flat elevation/blockout with coherent tower depth and native-scale material detail only after the threshold proof. Add restrained continuous motion only after a real-client seam/cadence check; current candidate contains no animation.
6. Inspect full-client screenshots and movement footage before calling the result usable or visually accepted. Preserve source, tests and evidence on this draft branch. No merge, public deployment or spending.
