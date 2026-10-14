# Scoped native spawn silence — unpublished map candidates

The delivered Campus09 and Social/Outdoor Office01 maps have no native silent spawn protection. These separate candidates add one small classified `area` with boolean `silent:true` around each original spawn. Original start rectangles, random position selection, rendering, collisions, tiles, animation, audio properties and assets are unchanged. Gate maps are handled separately.

- Campus09 v9.1 proposal: quiet landing rectangle `(896,1536,96,96)`. Original spawn `(920,1552,32,32)` has one possible center `(936,1568)`, whose area footpoint is `(936,1584)`.
- Social/Outdoor Office02 proposal: quiet landing rectangle `(416,672,160,96)`. Original spawn `(448,672,96,64)` has2145 possible integer centers. All2145 footpoints are covered.

The32px padding around the native footpoint envelope keeps protection active through a small first step. Both original start areas remain exactly as delivered. Each map changes only its TMJ: one added object and the next-object counter. The other runtime files are byte-identical. Inherited manifest/audio notes describe the original baseline; this README and the patch audit describe the new spawn-only exception.

Existing native semantics suppress proximity participation while `silent:true` is active. Map music is independent: this property does not call the audio manager, alter `playAudio`, reset mute or stop an ambient track. The campus retains its fountain/fire native areas; this outdoor-office template has no music configured to begin with. After leaving the quiet landing, the absent silent property clears the map's silence flag and normal proximity eligibility resumes, subject to any other active user/WAM restrictions.

## Important validation boundary

The engine connects the room socket before its first explicit evaluation of the spawn area's properties. The map activates silence during startup without needing the player to walk, but this map-only change cannot guarantee zero transient server grouping during that initial window. No engine change, multiplayer/browser test or publication is included.

Explicit initial positions, restored/reconnected positions and WAM-defined starts can bypass these TMJ default spawn rectangles. The checker covers every declared supported TMJ spawn in these files; room-editor changes need the same validation again.

## Files

- `candidates/`: complete local runtime copies with relative assets intact. Neither existing published map was modified.
- `tools/spawn_silence.py`: reusable finite32 TMJ coverage audit and opt-in patch builder. Run with a map path to validate; `--output` creates a new derivative.
- `tools/test_spawn_silence.py`: targeted coverage/edge/exit/audio invariance tests.
- `verification/map-change-audit.json`: exact old/new hashes, added rectangles and all-spawn coverage.
- `AUTHORING-CHECKLIST.md`: local checklist addition for future map builds.

Proposed destinations are review names only. No branch, PR, Pages file, production room or gate was changed.
