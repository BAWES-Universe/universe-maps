# Moonlit preview repair — 2026-10-16

Repair of `BAWES-Universe/universe-maps`, source commit `37363a42e77e6535791e2ddd171f6d94c48d9f0a`, preview directory `previews/moonlit-conservatory-expanded-2026-10-16`. Map remains 48×64 native 32px tiles (1536×2048), Woka scale1. No expansion, paid service, production game deployment, engine merge, world registration or permission change.

## Repairs

- Moved the fully opaque upper-garden paving/canopy tiles below `floorLayer`; they no longer paint over the avatar.
- Reconciled upper path, under-bed purple paving, planted islands and lamp collisions against the artwork and real player physics. Opened the west paved alcove; blocked the actual plants instead of the path.
- Registered the existing upper furniture groups +16/+8px and lower-right group −12px against native collision cells. Furniture and avatar dimensions are unchanged. All five tables block walking; ten chairs have open approaches and occupancy points.
- **Take nearest seat** in the map commands uses ordinary native movement, approaching from the side so the avatar faces its table. Walk normally to leave. This is native upright occupancy, not a new sitting pose or engine feature.
- Removed all walking-triggered water audio prompts and their anchors. Spawn is silent. **Enable water sound** explicitly opts into the existing native player; native Pause, Mute and Volume retain user choices while walking. **Mute water** removes the map's audio source completely.
- Kept both roof cutaways, the tea ritual and **Walk to fountain**. Visual doorway animation no longer closes a pathfinding barrier across the pavilion entrance.
- Original water tiles were both faint and partly painted over by later artwork. Replaced their active use with transparent flowing highlights on selected cascades and expanding fountain rings, placed above the static scene and below avatars. Continuous real-runtime footage verifies visible motion.
- Revisioned the changed image/script URLs so a new preview load cannot reuse cached pre-repair furniture/controller files. Original art filenames remain available unchanged.

## Acceptance evidence

Accepted for preview publication after the independent review, final route/audio regression and revisioned-URL reload smoke. All revised asset requests returned200; the served TMJ hash matched the release file; fresh spawn was silent and the actual native menu seated the avatar correctly.

Actual local WorkAdventure stack, engine commit `6b551e37c11d0bb344fd8429974cadca80ccedae`, with real native player, pathfinding, keyboard physics, iframe API and audio UI. No engine source modification was required; local frontend setup configuration/dependency recovery was used to run the saved stack.

- 31/31 final route checkpoints reached: upper garden, restored under-bed path, west alcove, both pavilions/counters/exits, all connecting paths, the four sides of the central tree and fountain, and southern connections. Camera zoom and Woka scale stayed1.
- Independent non-author gameplay: all10 chair occupancies, inward facing and unrestricted keyboard exits passed; five tables blocked keyboard attempts; corrected plant boundaries and visible avatar passed.
- Brew → Collect → Serve tea and the actual Walk to fountain button completed in the final route run.
- Native audio opt-in played the real fountain MP3. Pause/Mute persisted through six water crossings. Volume adjustment and Pause persisted during the complete route sweep. A visible-button observer recorded1159 samples with zero walking audio prompts; controller checks also sampled15360 positions without walking audio writes/prompts.
- All668 open tile centers remain connected. This supplements, and does not replace, the real route/physics checks.
- Fresh independent continuous footage: two uninterrupted eight-second water holds and the complete72.4-second capture containing traversal between them. This is the actual game, not the earlier renderer fixture.
- See [evidence gallery](review/index.html), [independent review](review/independent-final-review.md), and machine-readable results in `review/repair-2026-10-16/`.

## Limitations

- Water motion is animated highlights/rings on selected streams over static artwork. Many background waterfalls remain painted/static; this is not whole-scene fluid animation.
- The narrow southwest diagonal shortcut stays closed where the existing lamp and planter leave insufficient native32px clearance. Its paved alcove is accessible, and the restored under-bed path is reached via the east. No complete southwest ring is claimed. Tile-grid collisions are not pixel-perfect leaf contours.
- The tested native engine's **Stop** button clears its property cache, so movement can reapply the still-enabled map audio source. Native Pause/Mute remain effective. Use either, or the map's **Mute water** command for persistent silence. No engine change/deployment was made for this inherited behavior.
- Public GitHub Pages requests return a network-gateway403 in this environment. The pinned published source was retrieved from GitHub and the complete game tested locally. Remote owner-session gameplay and world registration are outside this repair; publication/source verification must not be described as owner-session acceptance.
- Khalid's attachment records/descriptions were retrieved, but their image bytes could not be materialized here. Fresh source/runtime evidence independently reproduced and addressed the reported layer and path defects.

Older screenshots/reports outside `review/repair-2026-10-16/` are historical diagnostics. The final independent review supersedes rejected intermediate candidates.
