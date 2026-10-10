# Gate B v4 static view — local candidate

Desktop with a fine primary pointer keeps native framing and receives no camera commands. Coarse-pointer devices receive one immediate, unlocked wide setup at the player, then no automatic zoom restores, stair pullbacks or waypoint cameras. Portrait uses the same wide scale as v3's opening; landscape swaps the authored frame dimensions. Pointer/orientation changes never reset the view.

Normal native following resumes on the first movement and retains the wide or user-selected zoom. Before that first movement, the native Positioned camera can show a different crop after pinching; walking recenters it. Pre-first-move Look Around can likewise be reclaimed. No engine change or repeated camera workaround is included. Very early interaction before script initialization and native zoom bounds remain platform limits.

Coarse pointer is a device heuristic: a coarse-only desktop/tablet can receive the mobile setup. Hidden iframe dimensions are not used. Short phones retain a smaller avatar until the user zooms in. These are source-class and offline framing checks, not physical touch or live-game verification.

All v3 geometry, balconies, silent spawn, art, animation and native music/waterfall mix are preserved. The onward destination remains blank and owner-configurable. Native Pause/Mute work; Stop may resume audio on a later tile. Water is baked into the mix, not positional. Initial join timing can still expose a brief proximity bubble before the silent tile is applied.

A/Bv1/Bv2/Bv3 are preserved. Publication is held for parent review. The 15 shared v6 PNG source files remain a dependency on [universe-maps PR #4](https://github.com/BAWES-Universe/universe-maps/pull/4); this six-file source package is not a standalone master build. A future master deployment may replace unmerged additive preview files.
