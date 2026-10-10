# Outdoor Office silent-spawn variant

Use [studenthub-outdoor-office-silent-spawn.tmj](map/studenthub-outdoor-office-silent-spawn.tmj) for the native spawn-protected variant. The original `studenthub-outdoor-office.tmj` and all existing files remain byte-identical. The two TMJs share `map/tilesets/native32.png`; no artwork is duplicated.

The only map change is one classified `area` with boolean `silent: true` at `(416, 672, 160, 96)`, plus the next-object counter. The original random start rectangle `(448, 672, 96, 64)` is unchanged. All 2,145 possible native integer spawn positions have their `(player.x, player.y + 16)` footpoint inside the quiet landing.

## Behavior and boundary

After the engine applies the area's property, native silence prevents proximity bubbles while the player remains inside. Leaving clears this map's silence flag, so normal proximity eligibility returns unless another user, map or WAM restriction applies. Native map music is independent; this template has no configured music, and its audio properties remain unchanged.

The initial room connection happens before the first explicit spawn-area evaluation. This map-only variant cannot guarantee that a player never briefly joins a proximity group during that startup window. [Engine issue #735](https://github.com/BAWES-Universe/workadventure-universe/issues/735) records the source-confirmed ordering gap; a live transient group or media transmission has not been reproduced. No browser or multiplayer test was performed for this patch.

Explicit initial positions, restored/reconnected positions and WAM-defined starts can bypass the TMJ default spawn. Validate them again when configuring a live room. This is a source-only template in PR #6, stacked on archive PR #3. It is not published to Pages or a live room.

## Verification

- Every declared TMJ spawn is covered: 2,145 of 2,145 possible integer positions.
- Source-derived native movement leaves and re-enters the area across 44 frames with zero body overlaps; silence clears and reactivates.
- Exact native callback audit reports zero audio-manager calls.
- The reusable checker is `tools/spawn_silence.py` at the repository root. From the repository root run:
  `python tools/spawn_silence.py map-mocks/social-outdoor-office-01/map/studenthub-outdoor-office-silent-spawn.tmj`
- The checker covers finite orthogonal 32 px maps, classified rectangle starts and uncompressed named start tile layers. It reports unsupported inputs and conflicting silent properties. It does not validate live socket timing or WAM/editor overrides.
- Original TMJ SHA-256: `e421842c675eecd84cfabf9b0e1dbedb7f1d2268a0396eab48b09f1008734b8e`.
- Variant TMJ SHA-256: `0e1d34ac9094a1d882e7145009679dec39d9fa8de963a83b76e3a0a8c9f9f618`.

Keep the quiet landing small. Check every possible spawn footpoint, reject conflicting silence overrides, cross each reachable exit, preserve audio behavior, and retain the startup limitation in future map checks. The original manifests continue to describe the original TMJ; this note describes the additive variant.
