# Independent candidate review

Verdict: useful scoped repair candidate; **not accepted for publication**. Reviewed independently from the author through source diffs, original artwork, engine depth implementation, and a separately executed scripting API mock. No live gameplay was performed by this reviewer.

## Verified improvements

- The opaque `Tree canopy above walking loop` layer is now below `floorLayer`, removing its above-avatar draw order over the upper path.
- Both water animation layers now sit above static garden/junction artwork and below avatars, fixing their previous layer occlusion. This does not establish convincing visible water motion.
- Seventeen collision cells changed: north path at x=672–831,y=352–383 opens; planted bed and southwest island receive blockers; the first pavilion table blocker moves from the left chair tile x=192–223 to table tile x=224–255,y=224–255. These changes are consistent with the inspected artwork, but player-body edge handling and full routes still need gameplay testing.
- Walking-triggered water popup code and obsolete popup anchors are removed. The remaining audio action requests `audio/fountain.mp3` using native `playAudio`, with volume 0.22 and looping, only after explicit menu opt-in.
- Native Woka scale and camera settings are unchanged. Roof/door logic and Walk to fountain guidance are retained.

## Independently executed check

Loaded candidate `scene.js` with a mock WA API. Spawned at (623,959), then crossed six water/garden positions five times. The 30 position changes produced zero popups and zero audio property changes. Explicit Enable water sound requested the native audio URL. Entering (576,1264) retained Walk to fountain, and entering (300,260) requested original pavilion roof removal. This is a scripting test, not proof of rendering, collision physics, audio playback or gameplay.

## Publication blockers / remaining requirements

- All chairs remain painted artwork. No supported sitting implementation was found in the local engine; every-seat sitting acceptance is unresolved.
- Every route, connection, central tree perimeter, table footprint, chair approach/exit, and both roof transitions require actual gameplay verification. The candidate's 17 collision edits are not a full-map test.
- Water frame assets are unchanged and their animation remains visually subtle. Layer correction alone is not sufficient to claim visible fountain/waterfall motion. A local renderer fixture can provide limited visual evidence but must not be represented as a live deployed game session.
- Live artifact access is blocked according to the parent agent's 403 fetch result. This reviewer did not independently establish live deployment access.

Do not publish this candidate as accepted until these requirements pass or the user explicitly changes the acceptance scope.

## Fixture evidence assessment

Inspected `upper-candidate.png` and `lower-candidate.png`. The native-size avatar is visibly drawn on top of the upper paved path north of the circular planted bed and on the lower path east of the fountain. Both screenshots clearly label themselves as an unpublished local renderer, not live gameplay. They support the narrow depth-order repair, but not movement, collision, sitting or deployed behavior.

The supplied WebM has a 16.28-second duration at 1100×794, 25 fps. The capture script holds the upper view for six seconds and then moves the camera/avatar directly to the lower view for six seconds; it does not record gameplay traversal. Independently compared decoded frames at 4/5 seconds in the upper-right waterfall region: average channel difference was only 0.007/255, with no pixels changing by more than 10. The lower fountain region at 12/13 seconds did show pixel differences (mean 3.50/255), but numerical change does not demonstrate convincing waterfall/fountain motion. This reviewer does not accept the water-motion requirement from these artifacts. Live gameplay, all-seat behavior and water-motion acceptance remain blocked.

## Subsequent scope and evidence update

The user clarified seating as native natural chair occupancy/facing/back layering, not a dedicated seated animation. Any earlier statement in this report treating missing seated animation as a publication blocker is superseded. Actual local runtime is now available and successful route screenshots support avatar visibility and several full-map connections; see `runtime-route-screenshot-review.md`. Final acceptance remains pending corrected route results, closer chair occupancy review and continuous visible water-motion evidence.
