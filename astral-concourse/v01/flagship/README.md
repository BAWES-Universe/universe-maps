# Astral Concourse · Flagship Hall v01

A separate 210-seat conference or esports hall prototype. This additive preview does not replace any existing campus map. The proposed shared hub and other halls are not implemented here.

## Files and setup

This folder contains the six-file runtime in `map32/` plus concise validation and provenance documentation. Design source artwork and build tools are maintained separately and are not included in this runtime snapshot.

- `map32/grand-auditorium.tmj`: native 32px Tiled map, 48 × 40 cells (1536 × 1280px)
- `map32/grand-auditorium.wam`: companion native Podium/Audience configuration
- Four `map32/*.png` files: complete local runtime texture closure

Keep all six runtime files in the same directory. Open the TMJ in Tiled for map inspection. For native presenter/listener roles, a compatible WorkAdventure room must load the companion WAM as its room map/configuration. Its `mapUrl` resolves `./grand-auditorium.tmj`. Importing only the TMJ does not activate the complete Podium/Audience pair.

Published asset paths:

- [TMJ](https://bawes-universe.github.io/universe-maps/astral-concourse/v01/flagship/map32/grand-auditorium.tmj)
- [Companion WAM](https://bawes-universe.github.io/universe-maps/astral-concourse/v01/flagship/map32/grand-auditorium.wam)

These are static map assets, not an active room or verified live broadcast. Room creation, WAM activation and live acceptance remain separate steps.

## Layout and audio intent

Three banks × ten chairs × seven rows give 210 visible seats, at 32px horizontal and 64px row pitch. Native Woka sprites remain 32 × 32 at scale 1. Two blue aisles connect to the rear portals; both side stairs reach the stage. Chair backs and lectern use ordinary above/below-actor layers with collision. There is no custom seating controller or engine patch.

The podium area ID is `astral-flagship-podium`; its broadcast name is `astral-flagship-stage`. The audience references the podium area ID through `speakerZoneName`; audience chat is disabled. All default spawn placements are inside the quiet arrival vestibule. No music, ambience, iframe or legacy Jitsi audio is added. The south doorway has no bound exit URL.

At the reviewed engine source commit `75666c0ccae779515b6fcbd83446ebd1eee29d1b`, native Podium/Audience schema and runtime support are present. Editor controls are gated by `FEATURE_FLAG_BROADCAST_AREAS`, whose source default is false. The deployed flag and available WAM import route are unverified. Successful role joins are excluded from proximity groups in source; that does not establish successful media joins or zero transition bubbles.

## Validation and limits

The frozen candidate passed 210/210 reachable, body-clear and head-clear seat anchors; 3,800 source-matched movement legs; all 716 walkable cells connected; no furniture/head conflicts across 554,924 reachable integer body-clear placements; 1,089 safe and silent default spawn placements; 26 current-engine WAM checks; and 18 package checks. See [validation summary](docs/VALIDATION-SUMMARY.json) and [runtime hashes](docs/RUNTIME-SHA256.json).

These are offline/source-level checks. No live browser playthrough, keyboard/touch/mobile acceptance, multiplayer rendering, media join, transient-bubble check, cross-hall audio isolation or concurrent-capacity/load test has been completed. The movement model uses source-default speed 9, which deployment may override. The seat count is not a concurrent-user guarantee.

## Publication safety

Source is proposed in a regular pull request without merging. The Pages preview is added independently to the existing `gh-pages` tree, preserving existing served paths. Do not run a clean deployment from `master` merely to publish this preview: the existing deployment workflow can replace Pages content and remove previews absent from `master`.

No engine changes, workflow changes, production-room updates or media-service creation are part of this preview. See [provenance](docs/PROVENANCE.md).
