# Campus09 silent-spawn variant

Use [magical-campus-silent-spawn.tmj](../map32/magical-campus-silent-spawn.tmj) for the native spawn-protected variant. The original `magical-campus.tmj` and all existing artwork, collisions, animations and audio assets remain byte-identical. Both TMJs share the same relative image and audio files.

The only map change is one classified `area` with boolean `silent: true` at `(896, 1536, 96, 96)`, plus the next-object counter. The original start rectangle is unchanged. The native spawn center `(936, 1568)` has area footpoint `(936, 1584)`, inside the quiet landing.

## Behavior and boundary

After the engine applies the area's property, native silence prevents proximity bubbles while the player remains inside. Leaving clears this map's silence flag, so normal proximity eligibility returns unless another user, map or WAM restriction applies. Native `playAudio` is separate: the fountain and fire audio properties, assets and playback settings are unchanged.

The initial room connection happens before the first explicit spawn-area evaluation. This map-only variant cannot guarantee that a player never briefly joins a proximity group during that startup window. [Engine issue #735](https://github.com/BAWES-Universe/workadventure-universe/issues/735) records the source-confirmed ordering gap; a live transient group or media transmission has not been reproduced. No browser or multiplayer test was performed for this patch.

Explicit initial positions, restored/reconnected positions and WAM-defined starts can bypass the TMJ default spawn. Validate them again when configuring a live room.

## Verification

- Every declared TMJ spawn is covered: 1 of 1 possible integer positions.
- Source-derived native movement leaves and re-enters the area across 70 frames with zero body overlaps; silence clears and reactivates.
- Exact native callback audit reports zero audio-manager calls.
- The reusable checker is `tools/spawn_silence.py` at the repository root. From the repository root run:
  `python tools/spawn_silence.py public/butterfly-town/v9/map32/magical-campus-silent-spawn.tmj`
- The checker covers finite orthogonal 32 px maps, classified rectangle starts and uncompressed named start tile layers. It reports unsupported inputs and conflicting silent properties. It does not validate live socket timing or WAM/editor overrides.
- Original TMJ SHA-256: `53eecdd2c8c3362ecdf6ceccab0f4ed01d755adad41f39fcb509ca3e527df42b`.
- Variant TMJ SHA-256: `c1fe4f5a119c5bdfd9c81340e0a420fea146f5bd02902118c20c1867eae0829a`.

Keep the quiet landing small. Check every possible spawn at `(player.x, player.y + 16)`, reject conflicting silence overrides, cross each reachable exit, preserve audio behavior, and retain the startup limitation in future map checks. The original freeze manifests continue to describe the original TMJ; this note describes the additive variant.
