import { installNativeAudio } from './native-audio.mjs';
const nativeNearbyAudio = installNativeAudio();
/* Bounded Universe gate. Native map APIs only; the destination is a real PLAY room URL. */
(() => {
  'use strict';
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const subscriptions = [], visibility = new Map();
  const veils = ['journey-veil-1', 'journey-veil-2', 'journey-veil-3', 'journey-veil-4'];
  const prop = (o, name) => o.properties?.find(p => p.name === name)?.value;
  const flatten = list => list.flatMap(l => l.type === 'group' ? flatten(l.layers) : [l]);
  const inside = (p, r) => p.x >= r.x && p.x <= r.x + r.width && p.y + 16 >= r.y && p.y + 16 <= r.y + r.height;
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
  let disposed = false, sequence = 0, revision = 0, transitioning = false, armed = true;
  let layers = [], bounds = {x:0,y:0,width:960,height:1440}, spawn = {x:480,y:1336};
  let threshold = {x:416,y:544,width:128,height:64}, destination = null;
  let ownsCamera = false, revealSeen = false, revealAt = 0;
  function show(name, value) {
    if (!layers.some(l => l.name === name) || visibility.get(name) === value) return;
    visibility.set(name, value);
    (value ? WA.room.showLayer : WA.room.hideLayer)(name);
  }
  function curtain(level) { veils.forEach((name, index) => show(name, index === level - 1)); }
  function releaseCamera(duration = 900) {
    if (!ownsCamera) return;
    ownsCamera = false;
    WA.camera.followPlayer(true, media.matches ? 1 : duration);
  }
  function visuals() {
    for (const layer of layers) {
      if (layer.name === 'permanent-collisions' || layer.name === 'start') continue;
      if (veils.includes(layer.name)) continue;
      show(layer.name, prop(layer, 'transitOnly') !== true && !(media.matches && prop(layer, 'reducedMotionHide') === true));
    }
  }
  function camera(position) {
    if (media.matches) { releaseCamera(1); return; }
    if (position.y >= spawn.y - 16 && !ownsCamera) revealSeen = false;
    if (!revealSeen && position.y < spawn.y - 64 && position.y > spawn.y - 500) {
      revealSeen = true; revealAt = Date.now(); ownsCamera = true;
      // One focus acquisition keeps the engine's one saved player-zoom slot intact.
      WA.camera.set(bounds.x + bounds.width / 2, bounds.y + 672, 960, 1344, true, true, 1600);
    }
    if (ownsCamera && ((position.y < spawn.y - 424 && Date.now() - revealAt > 2400) || position.y > spawn.y - 16)) releaseCamera(1400);
  }
  function reconcile(position, allowTravel = true) {
    if (disposed || transitioning) return;
    camera(position);
    if (!inside(position, threshold)) armed = true;
    // An unregistered destination remains an inactive portal, never a guessed or broken URL.
    if (allowTravel && destination && armed && inside(position, threshold)) {
      armed = false; void travel();
    }
  }
  async function refresh() {
    const at = ++revision;
    try { const p = await WA.player.getPosition(); if (!disposed && !transitioning && at === revision) reconcile(p); }
    catch (error) { if (!disposed) console.warn('Gate position refresh failed.', error); }
  }
  async function travel() {
    if (disposed || transitioning || !destination) return;
    transitioning = true; const token = ++sequence; ++revision;
    try {
      if (!media.matches) {
        show('gate-threshold-charge', true); nativeNearbyAudio.beginGate(token); await sleep(260);
        if (disposed || token !== sequence) return;
        const current = await WA.player.getPosition();
        if (!inside(current, threshold)) {
          transitioning = false; show('gate-threshold-charge', false); nativeNearbyAudio.cancelGate(token); reconcile(current, false); return;
        }
        for (let level = 1; level <= 4 && !media.matches; level++) {
          if (disposed || token !== sequence) return;
          curtain(level); await sleep(55);
        }
      }
      releaseCamera(1);
      // The fork resolves this against the PLAY URL. Supply a verified room URL, not a sibling asset path.
      nativeNearbyAudio.pauseForTransition();
      await WA.nav.goToRoom(destination);
      // Native navigation normally unloads this iframe. If it does not, never leave a persistent veil/lock.
      await sleep(800);
      if (!disposed && token === sequence) { nativeNearbyAudio.resumeAfterTransition(); transitioning = false; curtain(0); show('gate-threshold-charge', false); nativeNearbyAudio.cancelGate(token); }
    } catch (error) {
      if (disposed || token !== sequence) return;
      transitioning = false; nativeNearbyAudio.resumeAfterTransition(); curtain(0); show('gate-threshold-charge', false); nativeNearbyAudio.cancelGate(token); releaseCamera(1);
      console.warn('Gate room navigation did not complete. Step out before trying again.', error);
    }
  }
  function motionChanged() {
    if (disposed) return;
    visuals();
    if (media.matches) { nativeNearbyAudio.cancelGate(); releaseCamera(1); curtain(0); }
  }
  function dispose() {
    if (disposed) return;
    disposed = true; ++sequence; ++revision; nativeNearbyAudio.dispose();
    subscriptions.splice(0).forEach(s => s?.unsubscribe?.());
    media.removeEventListener?.('change', motionChanged); releaseCamera(1); curtain(0);
  }
  WA.onInit().then(async () => {
    const map = await WA.room.getTiledMap(); if (disposed) return;
    const all = flatten(map.layers); layers = all.filter(l => l.type === 'tilelayer');
    const objects = all.flatMap(l => l.objects ?? []);
    bounds = objects.find(o => o.name === 'gate-bounds') ?? bounds;
    spawn = objects.find(o => o.name === 'gate-spawn') ?? spawn;
    threshold = objects.find(o => o.name === 'gate-threshold') ?? threshold;
    const configured = prop(map, 'campusRoomUrl');
    if (typeof configured === 'string' && configured.trim()) {
      // Absolute HTTPS PLAY URLs only: this avoids asset-relative navigation surprises on /@ routes.
      try { const url = new URL(configured); if (url.protocol === 'https:') destination = url.href; }
      catch { console.warn('campusRoomUrl must be a verified absolute HTTPS PLAY room URL.'); }
    }
    visuals(); curtain(0); media.addEventListener?.('change', motionChanged);
    subscriptions.push(WA.player.onPlayerMove(p => { ++revision; reconcile(p); }));
    for (const edge of ['onEnter', 'onLeave']) subscriptions.push(WA.room.area[edge]('gate-threshold').subscribe(refresh));
    await refresh();
  }).catch(error => console.error('Bounded gate initialization failed.', error));
  window.addEventListener('pagehide', dispose, {once:true});
})();
