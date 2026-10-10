# Astral Concourse: garden B / v08

A separate garden and coffee variation built on the frozen corrected A core. Native 32px tiles; 2560×1920 map. The accepted hall, foyer, reception, 210 auditorium chairs, 16 meeting chairs and four meeting rectangles remain intact. Twelve casual seats use accepted native chair artwork. These are artwork and geometry counts, not concurrent-user capacity claims.

## What changes

- Coherent outdoor timber and limestone replace the repeated indoor/stage-light floor bands, with a continuous garden gate landing.
- Two native low tables give the pavilion a coffee destination. Its four north-facing chairs form pairs 48px apart around a clear 128px central passage; other casual pairs remain 56px apart.
- Exactly three small rooted leaf accents use the existing native animated-tile system, with four 32px frames and restrained movement. Native Disable animations pauses them. No map audio, water, fountain, fire, script-driven replacement or new paid dependency is configured.
- The 16-cell quiet spawn receiver and native whole-hall entry focus carry over from A. Manual zoom remains available; the known native resize/rotation limitation remains.

## Use safely

Serve all ten files in `map32/` together. Use [grand-auditorium.tmj](map32/grand-auditorium.tmj) for Custom TMJ. The adjacent [portable WAM](map32/grand-auditorium.wam) is a configuration candidate: Custom TMJ does not import its meeting and broadcast areas automatically.

Create a separate room and follow [ROOM-SETUP.md](integration/ROOM-SETUP.md). Back up and reconcile the actual room WAM before any configuration change, and preserve its absolute `mapUrl`. Resubmitting a map URL to the inspected admin update handler can regenerate its WAM and reset areas/entities. This static package creates no room or media service.

## Verification and limits

Independent frozen review passes 70/70 checks: 29 schema/zone, 30 garden/preservation and 11 native animation-isolation checks. See [garden evidence](validation/independent/v08-garden-verification.json), [merged-source route results](validation/route-results.json), [acceptance scope](validation/ACCEPTANCE.md), and [exact runtime hashes](RUNTIME-MANIFEST.json).

All 2,106 open cells connect; 259 seat/landmark anchors are clear. Exactly four pavilion table cells change from A. Testing covers 1,813,584 reachable integer body positions without upper-head conflicts. Native-source replay on merged `60e7afd` passes 11,818/11,818 commands and 32,352,365 swept samples. The actual pinned animated-tile plugin ticks alongside 5,302,552 movement frames, emitting 194,589 render-only events with no mapChanged event or raw-map/property mutation.

The public dev build was verified as `60e7afd`, containing PR799, on 2026-10-10 at 20:04 UTC. This is served-version evidence only. Map tests use source/fixtures with stub scene, renderer, DOM and camera integration; they do not establish live gameplay, keyboard/renderer integration, device performance, media, multiplayer, network isolation or load.

Fresh native whole-hall focus is source-tested. Resizing/rotating while focused can lose padding or retain stale zoom; leaving and re-entering recalculates fit. Full rotation acceptance is not claimed. The frozen TMJ's historical local-candidate status string is retained to preserve its reviewed hash; publication and verification scope are recorded here.

## Full standalone source backup

This Git folder is the compact 17-file runtime and review package. Source inputs, generation masters/prompts, rebuild tools, masks, full independent reports, camera proofs and detailed replay fixtures are in the separately delivered `astral-flagship-b-v08-standalone-source.zip` (121,947,566 bytes; SHA256 `ca2e99d0e9e6fb5dfd30ca1309d4d54183cff2f3b5d4eab37bd25055d8a3cb10`). Source-only paths and historical local paths in reports refer to that archive and its recorded validation environment, not files included in this lean folder. A clean isolated rebuild reproduced all ten runtime files and final previews exactly.

The separate `astral-flagship-b-v08-runtime.zip` backup is 7,792,216 bytes; SHA256 `e28c4cfe9ae7304d32db5e32de521f57131e8a44b4052ca247b46dd4a0a33cdb`. The Library backups were confirmed before Git publication. See [artwork provenance](PROVENANCE.md). Greg is a reference-only review overlay, not a runtime dependency. A/v07 and all earlier versions remain separate for comparison.
