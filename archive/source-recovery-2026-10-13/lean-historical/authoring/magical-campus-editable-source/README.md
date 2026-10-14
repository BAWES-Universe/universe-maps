# Magical campus: verified native source preview

Use **map16/magical-campus.tmj** as the campus map. It is a finite 3200×3072px world, 200×192 tiles at 16px. The unchanged 32px Greg remains at scale 1 with a 16×16 immovable body. The original giant gate is the separate 960×1440px map in gate/map/gate.tmj.

The complete revision 04 office includes three reception service positions, seven teams and a meeting gallery. Connected exterior paths lead to the classroom, stage/audience, fountain court, arrival avenue, west garden, two display market stalls and four riverside firepit seats. The final garden/foundation joins fill previously blocked internal gaps without changing open paths or original nonvoid artwork.

## Three deliverables

- dist/magical-campus-runnable-preview.zip: self-contained local preview, both maps, scripts, relative assets, sound, representative overview and verification documents. Extract, run `python3 runtime/server.py --port 8850`, then open `http://127.0.0.1:8850/runtime16/?gate=1`. No external service is needed. Start sound explicitly; use arrows/WASD or the proof controls.
- dist/magical-campus-native-maps.zip: native campus and bounded-gate TMJs, referenced atlas pages and native scripts. Real PLAY room URLs remain blank. This payload is for room registration and full-client integration, not a deployed world.
- dist/magical-campus-editable-source.zip: frozen module layers, explicit geometry, masks, effects, connector transforms, compiler inputs and scripts. `tools/rebuild_frozen_layers.py` reconstructs all five layers pixel-identically from the bundled copies; `tools/compile16.py` repacks them. Original high-resolution art masters and earlier generation drafts remain in the sibling authoring packages referenced by source provenance and FINAL-SOURCE-HANDOFF.md.

The full raw WebM, the 8m16s MP4 and the 76s highlight are separate evidence deliveries. Recorder chunk JSONs and decoded analysis WAVs are retained in the workspace but omitted from ZIPs.

## Verified behavior

The final continuous native tile-renderer run visited 28 destinations, with 13,973 checked frames, zero permanent-tile penetration, zero avatar/body-size errors, zero camera-bound errors and no runtime errors. All 96 authored destinations also pass offline 1px body sweeps. The final artifact verifier passes 94 checks. Full evidence and hashes are listed in DELIVERY.json.

Occupied Operations egress/re-entry and grand reception approach have separate native recordings with stationary peers and source-derived social distance checks. Desk start/end facing is set through real blocked contact. This is not a live multiplayer test.

Fountain, river and fire pixels change in the actual tile renderer. The browser captures the real post-mute audio output, with no added soundtrack. Calibrated fountain/fire ambience is localized; sampled office/classroom/stage intervals and stable mute intervals are digitally silent. Audio analysis respects original packet timestamps using silence insertion. No microphone speech was sampled, and no speech-separation or human listening acceptance is claimed.

Both landscape 1024×704 and portrait 512×768 game viewports were checked on the cloud desktop. The original gate reveal, restored follow camera, active gate cue and actual campus scene handoff pass. Reduced motion was checked in the browser after acquiring the reveal: follow/zoom 1 return and five motion layers hide. The native return script offers an explicit action only on its separate pad; leaving removes it, re-entry restores it, and deliberate activation returns to the bounded gate once. Source tests cover 19 lifecycle cases and 858 body origins.

## Source and integration boundaries

Furniture is fixed Tiled artwork with editable authored source layers and explicit footprints. The TMJ does not automatically import movable WAM furniture entities. The personal-area draft describes ownership/configuration, not movable furniture.

Campus foreground, glass and shade are fixed native layers. Adaptive office roof entry/exit behavior is pending. Collisions never change for seating or visibility, and no mask follows the avatar. The 16px derivative conservatively coalesces four 8px physical cells; only two empty garden approach waypoints move 8px. Exact bench anchors remain unchanged.

The current map8 directory is a historical performance candidate, not the default. Earlier Chromium Error9 failures are recorded; the root cause is unproven. The successful final run streams recorder chunks to disk instead of retaining a large browser Blob.

Native production audio routing, actual HTTPS PLAY room URLs, bots, calls, broadcasts, claims, server permissions, full Universe client/server behavior and a physical-device matrix remain unassigned or unverified. No generic `silent` property, production change or fabricated live room link is included.

The original multi-module authoring builder expects its original sibling source trees. The bundled frozen-layer reconstruction needs only the copied sources, Python Pillow and NumPy. The runnable preview uses bundled browser code/assets and Python's standard library.
