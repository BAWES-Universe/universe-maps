# C entrance viewport audit

## Evidence and scope

This is a source-calculated architectural preview audit. It is not a browser screenshot, live engine test, verified camera session, or publication. No runtime, engine, collision or camera behavior was changed. Only files within this audit directory were created.

The exact pinned `HdpiManager.ts` in `/workspace/shared/flagship-v06-viewport-audit/source` is transpiled and executed by `calculate-viewports.cjs`. The settled follow rectangle is then calculated from `CameraManager.ts`'s centered player-follow and map-bounds contract. Source file hashes are in `source-calculated-viewports.json`.

Pinned repository commit: `90a148c03e03401e26d236eaac9bea4123b42c57`.

- [HDPI sizing source](https://github.com/BAWES-Universe/workadventure-universe/blob/90a148c03e03401e26d236eaac9bea4123b42c57/play/src/front/Phaser/Services/HdpiManager.ts#L6-L108)
- [DPR and CSS canvas source](https://github.com/BAWES-Universe/workadventure-universe/blob/90a148c03e03401e26d236eaac9bea4123b42c57/play/src/front/Phaser/Services/WaScaleManager.ts#L32-L87)
- [Default player follow](https://github.com/BAWES-Universe/workadventure-universe/blob/90a148c03e03401e26d236eaac9bea4123b42c57/play/src/front/Phaser/Game/CameraManager.ts#L327-L341)
- [Map bounds](https://github.com/BAWES-Universe/workadventure-universe/blob/90a148c03e03401e26d236eaac9bea4123b42c57/play/src/front/Phaser/Game/CameraManager.ts#L571-L615)

Assumptions: fresh zoom modifier 1, unobstructed game canvas, no co-website, no screen blocker, no room focus, no prior user zoom, settled player-follow. DPR 1, 2 and 3 were executed separately and agree for these two CSS viewport sizes. Other fractional DPR values are not covered by that equivalence claim. No phone safe area or browser address-bar geometry is fabricated.

## Fixed world and entrance

- World: 2816 by 2432 pixels.
- A source translation: +128 x, +256 y.
- Entrance threshold: y2032; center x896.
- A approach: x768 to1024, unchanged width256.
- Entrance module: origin(576,1762), size640 by320.
- Measured alpha bbox in the approved PNG: local(13,16,626,293), half-open.
- Alpha bbox in world: (589,1778,1202,2055), half-open. Last occupied row is2054. Height277, width613.
- Proposed reveal boundary: y2112 while approaching north.
- Proposed exterior restoration boundary: y2144 while moving south.

All rectangles here use half-open crop coordinates. Alpha-envelope counts describe the occupied vertical extent, not the proportion of opaque architectural surface.

## Camera math

For a CSS viewport W by H and device pixel ratio D, the source receives physical dimensions W*D by H*D. Its default budget is640*480=307200 pixels. Physical zoom is floor(sqrt(physical area/307200)), except a permitted1.5 step. The executed source also applies its complete clamping and rounding logic. CSS scale is real canvas width/game width/D.

For the tested DPR values:

| CSS viewport | Physical zoom at DPR1/2/3 | CSS scale | World view | Greg CSS frame |
|---|---|---|---|---|
| Portrait390x844 | 1 /2 /3 | 1 | 390x844 | 32x32 |
| Desktop1440x900 | 2 /4 /6 | 2 | 720x450 | 64x64 |

Default settled follow: cameraX=clamp(playerX-viewWidth/2,0,worldWidth-viewWidth); cameraY=clamp(playerY-viewHeight/2,0,worldHeight-viewHeight).

At center x896:

- Portrait x701 to1091. For every outside center y>=2010, vertical map bounds clamp the view at y1588 to2432.
- Desktop x536 to1256. Its vertical view is y(playerY-225) to(playerY+225) until the southern clamp at playerY2207, after which it stays y1982 to2432.

## Default-follow findings

| Player center y | Purpose | Portrait y bounds | Desktop y bounds | Desktop upper alpha rows clipped | Desktop alpha-envelope rows visible |
|---:|---|---|---|---:|---:|
| 2336 | Southern reference | 1588..2432 | 1982..2432 | 204 | 73 |
| 2208 | Southern approach | 1588..2432 | 1982..2432 | 204 | 73 |
| 2176 | Recommended outside spawn | 1588..2432 | 1951..2401 | 173 | 104 |
| 2160 | Closer outside alternative | 1588..2432 | 1935..2385 | 157 | 120 |
| 2144 | Restoration boundary | 1588..2432 | 1919..2369 | 141 | 136 |
| 2128 | Close spawn inside hysteresis band | 1588..2432 | 1903..2353 | 125 | 152 |
| 2113 | Last whole-pixel center before reveal | 1588..2432 | 1888..2338 | 110 | 167 |
| 2112 | Reveal boundary, immediately pre-hide | 1588..2432 | 1887..2337 | 109 | 168 |
| 2003 | Full alpha height fits, already inside | 1581..2425 | 1778..2228 | 0 | 277 |
| 1987 | Full module height fits, already inside | 1565..2409 | 1762..2212 | 0 | 277 |

Portrait contains the complete entrance alpha height at every tested outside center, but only a central390px horizontal slice of the640px module. Its alpha extent is613px wide, also wider than the portrait world view. Moving only the spawn cannot make the whole module fit horizontally at default portrait scale.

Desktop contains the entire entrance module width, but clips its upper elevation even immediately before the reveal. To show the first occupied upper row1778 under ordinary centered follow, the player would need y<=2003. That is29px north of threshold2032 and109px north of the reveal. Therefore there is no exterior default-follow spawn that displays the full entrance height while retaining the proposed reveal behavior.

At y2112 the proposed facade hides; the numeric facade projection at that coordinate is a pre-hide geometric reference, not a claim that the opaque building should persist after the transition. At y2144 it restores.

## Spawn recommendation

Use(896,2176) as a useful outside approach position if normal camera behavior is retained. It gives64px to the reveal boundary and32px beyond restoration. The unchanged32px Greg frame occupies world x880..912,y2160..2192, inside the256px approach and proposed landing extent. Its portrait CSS frame is x179..211,y572..604. Its desktop CSS frame is x688..752,y418..482.

A closer alternative(896,2160) gives48px to reveal and16px beyond restoration, with16 more northern world pixels visible on desktop. It still clips157 upper alpha rows. A y2128 spawn gets closer framing but lies inside the hysteresis band, so its initial exterior visibility depends on explicit controller initialization; it is not the preferred robust spawn.

Do not push spawn farther south to try to show more building. It makes northern framing worse until the bottom clamp, and then changes only the avatar's on-screen position.

## Mathematical framing tradeoff, notes only

The project decision is to retain ordinary outdoor follow and manual zoom. No extra exterior framing state is recommended or implemented. For mathematical comparison only, a temporary desktop entrance framing could retain the same2x CSS scale and use world rectangle x536..1256,y1762..2212, centered on(896,1987), while the player starts at(896,2176). This is a189px northward look offset. It includes the full640x320 entrance module and puts Greg's CSS frame at x688..752,y796..860, leaving40 CSS pixels below the frame. The source alpha starts32 CSS pixels below the viewport top.

This trades the usual centered avatar for an avatar near the bottom and shows less path ahead to the south. It also needs an explicit, tested transition back to normal follow at the entrance. It cannot show an entire broader shell that rises above y1762, and does not solve portrait horizontal clipping. It is a geometric design option only; no camera behavior, focus rectangle or zoom override was implemented.

## Door and route readability under ordinary follow

The approved decision is to judge the doorway and route rather than require the whole facade to fit. Main proofs use ordinary follow at player y2176, y2160 and y2112 on both viewport sizes. Optional framing is excluded from the main PNGs.

- The full approach x768..1024 fits horizontally in both views. Portrait has67px side margins around it; desktop has232 world pixels on each side.
- The full clear portal x832..960 also fits horizontally. Its128 native pixels display as128 CSS pixels in portrait and256 CSS pixels on desktop. Greg remains32 world pixels wide, leaving48 world pixels to each side in the portal.
- At desktop spawn y2176, the visible northern edge y1951 is81px north of the y2032 threshold. The southern288px-long clear route y1936..2224 loses only its northern15px; the threshold, approach and all route to the south remain in view.
- At desktop approach y2160, the visible edge y1935 is97px north of threshold and includes the full manifest clear-route rectangle beginning y1936.
- The alpha upper elevation is clipped as reported above. The actual door graphic and broader shell must still be inspected in the final image; numeric route inclusion is not by itself a usability or live-runtime proof.
- At reveal y2112, use the approved empty revealed composite if supplied. Otherwise label the static exterior crop as the immediately pre-hide reference, never as a post-transition exterior state.

## Completed image evidence

Final inputs received and used without retouching:

- `../review/full-outside-empty-native.png`, native2816 by2432.
- `../review/foyer-revealed-empty-native.png`, native2816 by2432.
- `../masks/full-shell-occlusion-alpha.png`, measured half-open bbox(128,112,1776,2055).
- Original A Greg reference, unchanged native32 by32 north-facing frame.

The parent confirmed a path addition x768..1024,y2176..2432. The source-calculated examples use the final outside composite containing that addition; no ground or collision was changed by this audit.

Six labeled main PNGs are complete, each with a separate exact-sized viewport PNG:

- `source-calculated-recommended-outside-portrait-labeled.png`
- `source-calculated-recommended-outside-desktop-labeled.png`
- `source-calculated-closer-outside-portrait-labeled.png`
- `source-calculated-closer-outside-desktop-labeled.png`
- `source-calculated-entry-reveal-boundary-portrait-labeled.png`
- `source-calculated-entry-reveal-boundary-desktop-labeled.png`

All main PNGs use ordinary settled player-follow. No optional camera state was rendered or implemented. At y2112 the images use the actual revealed source composite, so they do not misrepresent the facade as remaining opaque after reveal.

Visual review confirms the open doorway, threshold, full approach width, and Greg are clearly readable at both exterior positions and both viewport sizes. Desktop crops the upper entrance but leaves a large, high-contrast opening and the uninterrupted approach. Portrait shows the entrance from finial to threshold while clipping the module's outer125px on each side. The unchanged256px A opening is visible after reveal. These are static visual and source-geometry findings, not live gameplay acceptance.

The broader shell is intentionally outside the viewport: its mask begins y112. Portrait top1588 clips1476px of that overall vertical envelope, with573px left and685px right of its overall width outside view. Desktop spawn top1951 clips1839px of the shell envelope, with408px left and520px right outside view. Desktop approach top1935 clips1823px. These envelope measurements are not a fraction of visible roof area; the building is much larger than the close entrance view.

`rendered-inputs-and-outputs.json` records input hashes, exact crop bounds, avatar frame, and viewport location inside each labeled image. `final-viewport-proof.json` records successful pixel-equality checks for source crop + nearest canvas scale and labeled viewport regions, output hashes, tested DPR equivalence, full approach width inclusion, and zero shell alpha intersection with every32px Greg frame.

Rebuild with `calculate-viewports.cjs`, then `render-source-calculated.py` using the three input paths above, then `verify-rendered.py`. The label bars lie outside the exact390 by844 or1440 by900 viewport rectangle. No browser screenshots, runtime edits or publication were performed.

The final y2112 boundary input is the semantic foyer-only revealed composition; the hall shell remains closed. Camera bounds are unchanged. See the current rendered-inputs-and-outputs.json hashes.
