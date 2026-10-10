# Gate B v2 — native follow, standard 32 grid

Separate feedback candidate using the current game APIs. Live-game validation is pending. Gate A, B v1, and all game code remain unchanged.

## What changes

- The map remains 30 × 45 tiles at 32 × 32 pixels (960 × 1440 world pixels). Every artwork tile, animation, object, spawn and collision remains unchanged.
- Native player-follow and normal user zoom own framing throughout the walk. There are no script camera calls, focus areas, movement locks, progressive zoom timers, or camera reset state. Tap and joystick travel therefore cannot trigger B v1's repeated scripted stop-follow cycle.
- The full-map transparent audio layer always references the existing 48-second music + quiet water premix with playAudio, audioLoop=true, audioVolume=1. Native playback, retry, mute, pause and unload own the stream. No custom activation menu, popup or zone-triggered audio writes.
- The portal effects cancel on retreat, clean up on unload or failed navigation, and need a deliberate 16-pixel exit before another entry can trigger travel. Loading directly inside the portal does not auto-travel. The destination remains blank until the room owner supplies a verified HTTPS PLAY room URL in campusRoomUrl.

## Limits

The exact recovered pure music is preserved separately: gate-music.mp3, SHA-256 3f859b065fecd1f09c306db77051efdcba4477cb6f8e49481c225c60c42c76ea. The active premix is the unchanged B v1 asset, SHA-256 449b6c5d32a9a9589d8297676001a19cf92ab86162758a6bdfc8430bdc2207e3: music at 0.5 (−6.02 dB), the existing 16-second cascade repeated three times at 0.2 (−13.98 dB), with 8 ms endpoint ramps. These are existing baked gains, not live positional volume. No audio was regenerated for B v2.

There is no dramatic automatic pullback. Existing camera.set stops native follow; the current public API does not expose a zoom-only operation that preserves follow. The map uses normal native framing instead of a full-map fit. Native scale starts at modifier 1, adapts to viewport/DPI, and respects subsequent manual changes. The whole monument and both outer waterfalls may require the native zoom controls or Look around. Saved or previously changed game zoom can affect arrival framing.

The audio is one premixed stream. Water has a fixed baked balance, not live positional attenuation, independently adjustable volume, or location-based musical transitions. On platforms that ignore HTML media volume, map/user gain can be ineffective; the existing attenuated bytes keep the intended balance. Native Mute and Pause remain available. Browser autoplay can still require the native retry gesture. Native Stop unloads immediately, but crossing the next tile on this full-coverage layer restarts the same source; movement within the same tile does not. Use Mute or Pause to stay silent while walking. This existing behavior is confirmed by a pinned-source fixture; no engine workaround is added. The full source evidence is included in source-audit/audio/AUDIT.md.

Reduced Motion hides moving overlays. The unchanged gate-ground still contains static waterfall and pool scenery; no duplicate fallback artwork is added.

Local validation covers the final TMJ, exact source contracts, default framing calculations, repeated movement-event routes, portal cancellation/re-entry, and mocked native media lifecycle. These are not physical joystick/touch, live tap pathfinding, full HUD, browser audio, or iPhone tests. Live game validation is pending because browser control is blocked by its credential guard. Live tap and joystick behavior remains unverified.

## Package and reproduction

The separate `Gate-B-v2-map-only-review.zip` is supplied privately to the map owner for review. It contains the tests, pinned read-only source snapshots, original audio and shared PNGs. These tools are not included in this five-file repository addition, so the following commands cannot run from a repository checkout alone.

Unpack that review ZIP and run `python tools/verify_candidate.py` with Python 3 and Node 22 or newer. Verification uses the packaged inputs. `tools/build_candidate.py` records reconstruction from the original frozen workspace paths and committed engine blobs; it requires that original workspace and never changes engine files.

`publish/public/butterfly-town/gate-b/v2` is the five-file additive candidate. `dependencies/public` contains exact previously published shared PNGs for offline review only; do not overwrite or republish them. Merge the two public trees into a temporary serving folder to resolve the existing relative image URLs. `originals` preserves the pure music and water input files separately. A browser room must use the hosted TMJ as a Custom map and a real PLAY-room destination, not another asset URL.
