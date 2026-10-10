/* Gate B v4: the first IIFE is the byte-preserved portal/audio core.
 * Its camera-free comments apply only to that core. One mobile setup follows.
 */
/* Gate B v2: normal native follow, one static native audio source, reversible portal effects.
 * Map APIs verified at universe-develop d2bc57b63b4abab9303fb3cbcecf1a0450fd15cc.
 * This script never changes camera, movement controls, audio properties or audio playback.
 */
(() => {
  'use strict';
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const subscriptions = [], visibility = new Map(), waits = new Map();
  const veils = ['journey-veil-1', 'journey-veil-2', 'journey-veil-3', 'journey-veil-4'];
  const prop = (object, name) => object.properties?.find(property => property.name === name)?.value;
  const flatten = list => list.flatMap(layer => layer.type === 'group' ? flatten(layer.layers) : [layer]);
  const valid = position => position && Number.isFinite(position.x) && Number.isFinite(position.y);
  const inside = (position, rectangle, margin = 0) => valid(position) &&
    position.x >= rectangle.x - margin && position.x < rectangle.x + rectangle.width + margin &&
    position.y + 16 >= rectangle.y - margin && position.y + 16 < rectangle.y + rectangle.height + margin;
  let disposed = false, sequence = 0, revision = 0, transitioning = false, armed = false;
  let layers = [], threshold = {x:416,y:544,width:128,height:64}, destination = null;

  function show(name, visible) {
    if (!layers.some(layer => layer.name === name) || visibility.get(name) === visible) return;
    visibility.set(name, visible);
    (visible ? WA.room.showLayer : WA.room.hideLayer)(name);
  }
  function curtain(level) { veils.forEach((name, index) => show(name, index === level - 1)); }
  function resetEffects() { curtain(0); show('gate-threshold-charge', false); }
  function visuals() {
    for (const layer of layers) {
      if (['permanent-collisions', 'start', 'campus-audio-control'].includes(layer.name) || veils.includes(layer.name)) continue;
      show(layer.name, prop(layer, 'transitOnly') !== true && !(media.matches && prop(layer, 'reducedMotionHide') === true));
    }
  }
  function sleep(ms) {
    return new Promise(resolve => {
      const id = window.setTimeout(() => { waits.delete(id); resolve(); }, ms);
      waits.set(id, resolve);
    });
  }
  function cancelTransition() {
    ++sequence;
    transitioning = false;
    for (const [id, resolve] of waits) { window.clearTimeout(id); resolve(); }
    waits.clear();
    resetEffects();
  }
  function reconcile(position, allowTravel = true) {
    if (disposed || !valid(position)) return;
    if (transitioning && !inside(position, threshold)) cancelTransition();
    // Re-entry needs a deliberate exit beyond a 16 px band; a tap on the edge cannot retrigger it.
    if (!inside(position, threshold, 16)) armed = true;
    if (allowTravel && !transitioning && destination && armed && inside(position, threshold)) {
      armed = false;
      void travel();
    }
  }
  async function refresh() {
    const at = ++revision;
    try {
      const position = await WA.player.getPosition();
      if (!disposed && at === revision) reconcile(position);
    } catch (error) { if (!disposed) console.warn('Gate position refresh failed.', error); }
  }
  async function travel() {
    if (disposed || transitioning || !destination) return;
    transitioning = true;
    const token = ++sequence;
    ++revision;
    const current = () => !disposed && transitioning && token === sequence;
    try {
      if (!media.matches) {
        show('gate-threshold-charge', true);
        await sleep(260);
        if (!current()) return;
        const position = await WA.player.getPosition();
        if (!current()) return;
        if (!inside(position, threshold)) { cancelTransition(); reconcile(position, false); return; }
        for (let level = 1; level <= 4 && !media.matches; level++) {
          curtain(level);
          await sleep(55);
          if (!current()) return;
        }
      }
      const position = await WA.player.getPosition();
      if (!current()) return;
      if (!inside(position, threshold)) { cancelTransition(); reconcile(position, false); return; }
      await WA.nav.goToRoom(destination);
      // Native navigation normally unloads the script. Otherwise clear effects without auto-retrying.
      if (!current()) return;
      await sleep(800);
      if (current()) cancelTransition();
    } catch (error) {
      if (!current()) return;
      cancelTransition();
      console.warn('Gate room navigation did not complete. Step out before trying again.', error);
    }
  }
  function motionChanged() {
    if (disposed) return;
    visuals();
    if (media.matches) resetEffects();
  }
  function dispose() {
    if (disposed) return;
    disposed = true;
    ++revision;
    cancelTransition();
    subscriptions.splice(0).forEach(subscription => subscription?.unsubscribe?.());
    media.removeEventListener?.('change', motionChanged);
  }
  WA.onInit().then(async () => {
    if (disposed) return;
    const map = await WA.room.getTiledMap();
    if (disposed) return;
    const all = flatten(map.layers);
    layers = all.filter(layer => layer.type === 'tilelayer');
    threshold = all.flatMap(layer => layer.objects ?? []).find(object => object.name === 'gate-threshold') ?? threshold;
    const configured = prop(map, 'campusRoomUrl');
    if (typeof configured === 'string' && configured.trim()) {
      // A room owner supplies the real HTTPS PLAY room URL. An empty target stays inactive.
      try { const url = new URL(configured); if (url.protocol === 'https:') destination = url.href; }
      catch { console.warn('campusRoomUrl must be a verified absolute HTTPS PLAY room URL.'); }
    }
    visuals(); resetEffects();
    media.addEventListener?.('change', motionChanged);
    subscriptions.push(WA.player.onPlayerMove(position => { ++revision; reconcile(position); }));
    for (const edge of ['onEnter', 'onLeave']) subscriptions.push(WA.room.area[edge]('gate-threshold').subscribe(refresh));
    await refresh();
  }).catch(error => { if (!disposed) console.error('Gate initialization failed.', error); });
  window.addEventListener('pagehide', dispose, {once:true});
})();

/* Static mobile arrival only. No cinematic, walking-zoom restore or landing reveal. */
(() => {
/* Gate B v4: one unlocked, immediate arrival setup for a coarse primary pointer.
 * The hidden script iframe is not a game viewport; never use its innerWidth.
 * Native follow resumes on first movement without restoring the old zoom.
 * No later camera calls: movement, pinch, resize and reversal belong to the game.
 */
function installMobileStaticView(WA, host = window) {
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

  let disposed = false, controller;
  window.addEventListener('pagehide', () => { disposed = true; controller?.dispose(); }, {once: true});
  WA.onInit().then(() => {
    if (!disposed) controller = installMobileStaticView(WA, window);
  }).catch(error => console.warn('Gate initial framing unavailable; native camera retained.', error));
})();
