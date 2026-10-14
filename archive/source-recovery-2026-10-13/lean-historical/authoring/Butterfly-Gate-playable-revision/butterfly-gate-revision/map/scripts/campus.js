/* Butterfly Campus. Position-driven, player-local layers and same-map doorways. */
(() => {
  'use strict';
  const GATE = { x: 32, y: 1664, width: 960, height: 1440 };
  const CAMPUS = { x: 1120, y: 128, width: 2944, height: 3104 };
  const GATE_SPAWN = { x: 512, y: 3000 };
  const CAMPUS_SPAWN = { x: 2624, y: 2080 };
  const GATE_THRESHOLD = { x: 448, y: 2208, width: 128, height: 64 };
  const CAMPUS_RETURN = { x: 2496, y: 3104, width: 128, height: 64 };
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const subscriptions = [];
  const visibility = new Map();
  let disposed = false;
  let revision = 0;
  let sequence = 0;
  let transitioning = false;
  let scene = null;
  let room = null;
  let gateArmed = true;
  let returnArmed = true;
  let layers = [];
  let rooms = [];
  let gateBounds = GATE;
  let campusBounds = CAMPUS;
  let gateSpawn = GATE_SPAWN;
  let campusSpawn = CAMPUS_SPAWN;
  let threshold = GATE_THRESHOLD;
  let returnArea = CAMPUS_RETURN;
  let nativeAudioRuntime = null;
  let ownsCamera = false;
  let revealSeen = false;
  let revealAt = 0;
  let lastPosition = null;
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
  const now = () => Date.now();
  const veils = ['journey-veil-1', 'journey-veil-2', 'journey-veil-3', 'journey-veil-4'];

  function curtain(level) {
    veils.forEach((name, index) => show(name, index === level - 1));
  }
  function releaseCamera(duration = 900) {
    if (!ownsCamera) return;
    ownsCamera = false;
    // A positive duration also cancels any in-flight native pan.
    WA.camera.followPlayer(true, media.matches ? 1 : duration);
  }
  function gateCamera(position) {
    lastPosition = position;
    if (scene !== 'gate' || media.matches) { releaseCamera(1); return; }
    if (position.y >= gateSpawn.y - 16 && !ownsCamera) revealSeen = false;
    if (!revealSeen && position.y < gateSpawn.y - 64 && position.y > gateSpawn.y - 500) {
      revealSeen = true;
      revealAt = now();
      ownsCamera = true;
      // Exactly ONE native focus acquisition preserves the player's original zoom slot.
      WA.camera.set(gateBounds.x + gateBounds.width / 2, gateBounds.y + 672,
        960, 1344, true, true, 1600);
    }
    if (ownsCamera && ((position.y < gateSpawn.y - 424 && now() - revealAt > 2400) || position.y > gateSpawn.y - 16)) {
      releaseCamera(1400);
    }
  }

  // Character origins are not feet. This matches the map's source-pinned y+16 depth/area convention.
  const inside = (p, r) => p.x >= r.x && p.x <= r.x + r.width &&
    p.y + 16 >= r.y && p.y + 16 <= r.y + r.height;
  const flatten = list => list.flatMap(layer => layer.type === 'group' ? flatten(layer.layers) : [layer]);
  const property = (layer, name) => layer.properties?.find(p => p.name === name)?.value;

  function show(name, value) {
    if (visibility.get(name) === value) return;
    visibility.set(name, value);
    (value ? WA.room.showLayer : WA.room.hideLayer)(name);
  }

  function visuals() {
    for (const layer of layers) {
      // This layer owns physics permanently, independently of every visual reveal.
      if (layer.name === 'permanent-collisions') continue;
      // Control layers must remain enabled across scene visibility changes.
      if (layer.name === 'campus-audio-control') { show(layer.name, true); continue; }
      const owner = rooms.find(r => layer.name.startsWith(r.id + '-'));
      let visible;
      if (owner) {
        visible = scene === 'campus';
        if (layer.name === owner.id + '-roof') visible = visible && room !== owner.id;
        else if (owner.hasRoof) visible = visible && room === owner.id;
      } else if (layer.name.startsWith('gate-')) {
        visible = scene === 'gate';
      } else if (layer.name.startsWith('campus-')) {
        visible = scene === 'campus';
      } else continue;
      if (property(layer, 'transitOnly') === true) visible = false;
      if (media.matches && property(layer, 'reducedMotionHide') === true) visible = false;
      show(layer.name, visible);
    }
  }

  function setScene(next) {
    if (next === scene) return;
    scene = next;
    room = null;
    releaseCamera(1);
    if (next === 'gate') revealSeen = false;
    visuals();
  }

  function reconcile(position, allowTransit = true) {
    if (disposed || transitioning) return;
    setScene(inside(position, campusBounds) ? 'campus' : inside(position, gateBounds) ? 'gate' : scene ?? 'gate');
    gateCamera(position);
    const nextRoom = scene === 'campus' ? rooms.find(r => inside(position, r.bounds))?.id ?? null : null;
    if (nextRoom !== room) {
      room = nextRoom;
      visuals();
    }
    // Re-arm only after physically leaving a doorway. A failed teleport cannot create a retry loop.
    if (!inside(position, threshold)) gateArmed = true;
    if (!inside(position, returnArea)) returnArmed = true;
    if (allowTransit && scene === 'gate' && gateArmed && inside(position, threshold)) {
      gateArmed = false;
      void travel('campus', campusSpawn);
    } else if (allowTransit && scene === 'campus' && returnArmed && inside(position, returnArea)) {
      returnArmed = false;
      void travel('gate', gateSpawn);
    }
  }

  async function travel(destination, position) {
    if (disposed || transitioning) return;
    transitioning = true;
    const token = ++sequence;
    ++revision;
    try {
      if (!media.matches) {
        if (destination === 'campus' && layers.some(layer => layer.name === 'gate-threshold-charge')) show('gate-threshold-charge', true);
        await sleep(260);
        if (disposed || token !== sequence) return;
        const current = await WA.player.getPosition();
        const portal = destination === 'campus' ? threshold : returnArea;
        if (!inside(current, portal)) {
          transitioning = false;
          show('gate-threshold-charge', false);
          reconcile(current, false);
          return;
        }
        for (let level = 1; level <= 4; level++) {
          if (disposed || token !== sequence) return;
          if (media.matches) break;
          curtain(level); await sleep(55);
        }
      }
      releaseCamera(1);
      await WA.player.teleport(position.x, position.y);
      if (disposed || token !== sequence) return;
      transitioning = false;
      setScene(destination);
      reconcile(position, false);
      if (!media.matches) {
        await sleep(80);
        for (let level = 3; level >= 0; level--) {
          if (disposed || token !== sequence) return;
          curtain(media.matches ? 0 : level); await sleep(75);
        }
      }
      curtain(0);
    } catch (error) {
      if (disposed || token !== sequence) return;
      transitioning = false;
      curtain(0);
      show('gate-threshold-charge', false);
      console.warn('The doorway did not complete. Step out and enter again.', error);
      const at = revision;
      try {
        const current = await WA.player.getPosition();
        if (!disposed && token === sequence && at === revision) reconcile(current, false);
      } catch (positionError) {
        console.warn('The current position could not be refreshed.', positionError);
      }
    }
  }

  function observe(position) {
    ++revision;
    reconcile(position);
  }

  async function refresh() {
    const at = ++revision;
    try {
      const position = await WA.player.getPosition();
      if (!disposed && !transitioning && at === revision) reconcile(position);
    } catch (error) {
      if (!disposed) console.warn('The doorway position could not be refreshed.', error);
    }
  }

  const motionChanged = () => { if (!disposed) { visuals(); if (media.matches) { releaseCamera(1); curtain(0); } } };
  function dispose() {
    if (disposed) return;
    disposed = true;
    ++sequence;
    subscriptions.splice(0).forEach(s => s?.unsubscribe?.());
    media.removeEventListener?.('change', motionChanged);
    nativeAudioRuntime?.dispose();
    releaseCamera(1);
    curtain(0);
  }

  WA.onInit().then(async () => {
    const map = await WA.room.getTiledMap();
    if (disposed) return;
    // The optional native bridge has one deployment flag, defaulting to disabled.
    // Importing its policy does not fetch audio or create playback state.
    if (typeof WA.room.mapURL === 'string') {
      void import(new URL('scripts/campus-audio-runtime.mjs', WA.room.mapURL).href)
        .then(module => {
          if (disposed) return;
          nativeAudioRuntime = module.createCampusAudioRuntime(WA, { enabled: module.ENABLE_NATIVE_AUDIO });
          return nativeAudioRuntime.ready;
        })
        .catch(error => { if (!disposed) console.warn('Optional campus audio could not initialize.', error); });
    }

    const all = flatten(map.layers);
    layers = all.filter(l => l.type === 'tilelayer');
    const objects = all.flatMap(l => l.objects ?? []);
    const areas = objects.filter(o => o.width > 0 && o.height > 0);
    gateBounds = areas.find(o => o.name === 'gate-bounds') ?? GATE;
    campusBounds = areas.find(o => o.name === 'campus-bounds') ?? CAMPUS;
    gateSpawn = objects.find(o => o.name === 'gate-spawn') ?? GATE_SPAWN;
    campusSpawn = objects.find(o => o.name === 'campus-spawn') ?? CAMPUS_SPAWN;
    rooms = areas.filter(o => o.name.endsWith('-inside')).map(o => ({ id: o.name.slice(0, -7), bounds: o, hasRoof: layers.some(layer => layer.name === o.name.slice(0, -7) + '-roof') }));
    threshold = areas.find(o => o.name === 'gate-threshold') ?? GATE_THRESHOLD;
    returnArea = areas.find(o => o.name === 'campus-return') ?? CAMPUS_RETURN;
    media.addEventListener?.('change', motionChanged);
    const move = WA.player.onPlayerMove(observe);
    if (move) subscriptions.push(move);
    for (const name of ['gate-threshold', 'campus-return', ...rooms.map(r => r.id + '-inside')]) {
      for (const edge of ['onEnter', 'onLeave']) {
        const subscription = WA.room.area[edge](name).subscribe(refresh);
        if (subscription) subscriptions.push(subscription);
      }
    }
    await refresh();
  }).catch(error => console.error('The campus experience could not initialize.', error));
  window.addEventListener('pagehide', dispose, { once: true });
})();
