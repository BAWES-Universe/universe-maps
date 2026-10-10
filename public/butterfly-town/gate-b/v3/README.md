# Gate B v3 experimental map

A separate standard-32 candidate for feedback. Portrait touch devices begin with a wider view of the gate and waterfalls, return gently to normal walking zoom after a short ascent, then get one modest pullback after the first flight of stairs. Desktop arrival keeps normal native framing. The wider walking view is retained on retreat; the cinematic does not re-arm during the same visit.

This also includes revised stair boundaries, accessible balcony floors with foreground tree/lamp silhouettes, and a small native silent spawn zone. Original art, animations and native looping music/waterfall mix are preserved. The onward room URL is blank and must be configured by the room owner.

The initial overview uses a smaller avatar, especially on short phone screens. Manual zoom or Look Around during a transition may be replaced by the current game's native camera completion. A brief normal frame may show before script initialization. Reduced motion skips automatic camera changes. Native movement and manual camera control remain available.

Validation is local source-class simulation, geometry checks and offline compositions. Full live-game HUD, tap/joystick interaction and physical iPhone behavior are unverified. Initial room-join timing can still briefly expose a proximity bubble before the silent tile is applied. Native Pause/Mute remain supported; Stop can resume the static source on the next tile. Water is baked into the music mix, not positional audio.

A, Bv1 and Bv2 are separate preserved versions. No engine changes are required or included. This candidate is unpublished until review and explicit publication.

## Source merge dependency and preview lifetime

The 15 shared v6 PNGs are already served by GitHub Pages, but their source files are in open [universe-maps PR #4](https://github.com/BAWES-Universe/universe-maps/pull/4) and are not yet on master. This six-file source PR depends on those exact assets being merged first or together. It is not a standalone master build. The additive Pages preview can work using the existing served files without merging either PR.

The repository's master workflow builds dist from master and deploys it to gh-pages. A later master deployment can replace unmerged preview files, so this separate preview may need to be restored until its source dependencies and PR are reviewed and merged. No CI settings, existing map assets, or engine code were changed for this preview.
