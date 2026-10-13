/* Gate B v4: one unlocked, immediate arrival setup for a coarse primary pointer.
 * The hidden script iframe is not a game viewport; never use its innerWidth.
 * Native follow resumes on first movement without restoring the old zoom.
 * No later camera calls: movement, pinch, resize and reversal belong to the game.
 */
export function installMobileStaticView(WA, host = window) {
  const state = {phase: 'skipped', commands: 0};
  let disposed = false, latest = null, subscription;
  const dispose = () => { disposed = true; subscription?.unsubscribe?.(); };
  const empty = () => ({state, ready: Promise.resolve(), dispose});
  const coarse = host.matchMedia?.('(pointer: coarse)')?.matches === true;
  if (!coarse) { state.reason = 'native-fine-pointer-view'; return empty(); }
  const type = host.screen?.orientation?.type;
  const knownType = typeof type === 'string' && /^(portrait|landscape)-(primary|secondary)$/.test(type);
  const legacy = Number.isFinite(host.orientation);
  const screenAspect = Number.isFinite(host.screen?.width) && Number.isFinite(host.screen?.height)
    && host.screen.width > 0 && host.screen.height > 0;
  if (!knownType && !legacy && !screenAspect) { state.reason = 'orientation-unavailable'; return empty(); }
  const portrait = knownType ? type.startsWith('portrait') : legacy
    ? Math.abs(host.orientation) % 180 === 0 : host.screen.width < host.screen.height;
  state.device = {coarse, portrait, orientationSource: knownType ? 'screen.orientation.type'
    : legacy ? 'legacy-window-orientation' : 'screen-aspect-heuristic'};
  if (typeof WA?.camera?.set !== 'function' || typeof WA?.player?.getPosition !== 'function'
    || typeof WA?.player?.onPlayerMove !== 'function') {
    state.reason = 'required-api-unavailable'; return empty();
  }
  state.phase = 'waiting-for-position';
  subscription = WA.player.onPlayerMove(position => {
    if (Number.isFinite(position?.x) && Number.isFinite(position?.y)) latest = {x: position.x, y: position.y};
  });
  const ready = WA.player.getPosition().then(position => {
    if (disposed) return;
    const start = latest ?? position;
    if (!Number.isFinite(start?.x) || !Number.isFinite(start?.y)
      || start.y < 1056 || start.y > 1184 || start.x < 352 || start.x > 608) {
      state.phase = 'skipped'; state.reason = 'already-away-from-arrival'; return;
    }
    // Same wide scale as v3's opening, aligned with the player and native map bounds.
    // Rotate the authored rectangle only at initial setup; orientation changes never reset it.
    const width = portrait ? 640 : 1280, height = portrait ? 1280 : 640;
    WA.camera.set(start.x, start.y, width, height, false, false);
    state.phase = 'applied'; state.commands = 1;
    state.initialFrame = {x: start.x, y: start.y, width, height, lock: false, smooth: false};
  }).catch(() => { state.phase = 'skipped'; state.reason = 'position-unavailable'; })
    .finally(() => subscription?.unsubscribe?.());
  return {state, ready, dispose};
}
