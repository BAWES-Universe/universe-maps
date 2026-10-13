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
