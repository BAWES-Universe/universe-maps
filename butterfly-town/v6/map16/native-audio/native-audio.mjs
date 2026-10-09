/* Native map audio only. Pinned to Universe fork 6accae707e5a26bc56231ef241c64b397a5cea70. */
export const CAPS = Object.freeze({ fountain: 0.18, fire: 0.18, cascade: 0.15, gate: 0.055 });
const clamp = value => Math.max(0, Math.min(1, value));
const smooth = value => { const x = clamp(value); return x * x * (3 - 2 * x); };
const property = (item, name) => item.properties?.find(p => p.name === name)?.value;
const flat = layers => layers.flatMap(layer => layer.type === 'group' ? flat(layer.layers) : [layer]);
const point = p => p && Number.isFinite(p.x) && Number.isFinite(p.y);
const rect = r => r && [r.x, r.y, r.width, r.height].every(Number.isFinite) && r.width > 0 && r.height > 0;
export const contains = (p, r) => point(p) && rect(r) && p.x >= r.x && p.x <= r.x + r.width && p.y >= r.y && p.y <= r.y + r.height;

export function sourceGain(feet, source) {
  if (!contains(feet, source.bounds)) return 0;
  const r = source.bounds;
  const edge = Math.min(feet.x - r.x, r.x + r.width - feet.x, feet.y - r.y, r.y + r.height - feet.y);
  const distance = Math.hypot(feet.x - source.center.x, feet.y - source.center.y);
  return Math.min(CAPS[source.kind], source.maxGain) *
    (1 - smooth((distance - source.innerRadius) / (source.outerRadius - source.innerRadius))) * smooth(edge / source.edgeFade);
}

export function evaluate(position, config) {
  if (!point(position)) return null;
  const feet = { x: position.x, y: position.y + config.feetOffsetY };
  if (!contains(feet, config.bounds) || config.quietZones.some(zone => contains(feet, zone))) return null;
  return config.sources.map(source => ({ ...source, gain: sourceGain(feet, source), loop: true }))
    .filter(source => source.gain > 0).sort((a, b) => b.gain - a.gain || a.id.localeCompare(b.id))[0] ?? null;
}

export function readConfiguration(map) {
  const fail = reason => { throw Error('Native nearby audio: ' + reason); };
  const raw = property(map, 'nativeNearbyAudio');
  if (typeof raw !== 'string') fail('missing nativeNearbyAudio JSON map property');
  const config = JSON.parse(raw);
  if (config.version !== 1 || !['campus', 'gate'].includes(config.scene) || config.feetOffsetY !== 16 ||
      !rect(config.bounds) || config.startPolicy !== 'explicit-per-map' || config.fadeMs !== 180 ||
      !Array.isArray(config.sources) || !Array.isArray(config.quietZones)) fail('invalid policy');
  const layers = flat(map.layers), objects = layers.flatMap(layer => layer.objects ?? []);
  const carrier = layers.find(layer => layer.name === config.carrierLayer);
  if (!carrier || carrier.type !== 'tilelayer' || carrier.x || carrier.y || carrier.offsetx || carrier.offsety ||
      carrier.width !== map.width || carrier.height !== map.height || !Array.isArray(carrier.data) ||
      carrier.data.length !== map.width * map.height || carrier.data.some(gid => !Number.isInteger(gid) || !gid)) fail('carrier must cover every tile');
  const audioKeys = ['playAudio', 'playAudioLoop', 'audioVolume', 'audioLoop'];
  const holders = [...layers, ...objects, ...map.tilesets.flatMap(set => set.tiles ?? [])];
  if (holders.some(holder => audioKeys.some(name => property(holder, name) !== undefined))) fail('another native audio property already exists');
  const verifyArea = (areaName, expected) => {
    const area = objects.find(object => object.name === areaName && object.class === 'area');
    if (!area || area.rotation || area.ellipse || area.polygon || area.polyline ||
        ['x', 'y', 'width', 'height'].some(key => area[key] !== expected[key])) fail('missing exact boundary area: ' + areaName);
  };
  const ids = new Set();
  for (const source of config.sources) {
    if (ids.has(source.id) || typeof source.id !== 'string' || !['fountain', 'fire', 'cascade'].includes(source.kind) ||
        !point(source.center) || !rect(source.bounds) || !Number.isFinite(source.innerRadius) || source.innerRadius < 0 ||
        !Number.isFinite(source.outerRadius) || !(source.outerRadius > source.innerRadius) || !Number.isFinite(source.edgeFade) || !(source.edgeFade > 0) ||
        !(source.maxGain > 0 && source.maxGain <= CAPS[source.kind]) ||
        typeof source.url !== 'string' || !/^native-audio\/assets\/[a-z0-9-]+\.mp3$/.test(source.url)) fail('invalid localized source');
    ids.add(source.id); verifyArea(source.areaName, source.bounds);
  }
  for (const zone of config.quietZones) { if (!rect(zone)) fail('invalid quiet area'); verifyArea(zone.areaName, zone); }
  if (config.gateCue) {
    if (config.scene !== 'gate' || config.gateCue.maxGain !== CAPS.gate || config.gateCue.durationMs !== 5064 ||
        config.gateCue.debounceMs !== 1200 || config.gateCue.url !== 'native-audio/assets/gate-crossing.mp3') fail('invalid gate cue');
    verifyArea(config.gateCue.areaName, config.gateCue.bounds);
  }
  return config;
}

// Capability check only: this element never receives a URL or plays audio. The audited
// native AudioPlayback uses this same volume probe. Do not bypass unsupported gain caps.
export function supportsElementVolume(document) {
  try {
    const probe = document.createElement('audio'); probe.muted = true;
    const original = probe.volume; probe.volume = 0.5;
    const supported = Math.abs(probe.volume - 0.5) < 0.001; probe.volume = original;
    return supported;
  } catch { return false; }
}

export class NearbyAudio {
  constructor(WA, config, { now = () => performance.now(), setTimer = (fn, ms) => setTimeout(fn, ms), clearTimer = id => clearTimeout(id) } = {}) {
    this.WA = WA; this.config = config; this.now = now; this.setTimer = setTimer; this.clearTimer = clearTimer;
    this.enabled = false; this.hidden = false; this.disposed = false; this.position = null;
    this.output = null; this.gain = 0; this.fadeTimer = null; this.gateTimer = null; this.gateId = null;
    this.seenGateIds = new Set(); this.lastGateAt = -Infinity;
  }
  write(name, value) { this.WA.room.setProperty(this.config.carrierLayer, name, value); }
  cancelFade() { if (this.fadeTimer !== null) this.clearTimer(this.fadeTimer); this.fadeTimer = null; }
  clear() {
    this.cancelFade();
    if (this.output) {
      // Removing playAudio synchronously reaches native stop/unload; no lingering fade in quiet rooms.
      this.write('playAudio', undefined); this.write('audioVolume', 0); this.write('audioLoop', false);
    }
    this.output = null; this.gain = 0;
  }
  setEnabled(enabled) {
    if (this.disposed) return;
    this.enabled = Boolean(enabled);
    if (!this.enabled) this.cancelGate();
    this.reconcile();
  }
  setHidden(hidden) {
    if (this.disposed) return;
    this.hidden = Boolean(hidden);
    if (this.hidden) this.cancelGate();
    this.reconcile();
  }
  setPosition(position) {
    if (this.disposed) return;
    this.position = position;
    if (this.gateId !== null && (!point(position) || !contains({x: position.x, y: position.y + this.config.feetOffsetY}, this.config.gateCue.bounds))) this.cancelGate();
    this.reconcile();
  }
  beginGate(id) {
    if (this.disposed || !this.enabled || this.hidden || !this.config.gateCue || this.seenGateIds.has(id) ||
        !point(this.position) || !contains({x: this.position.x, y: this.position.y + this.config.feetOffsetY}, this.config.gateCue.bounds) ||
        this.now() - this.lastGateAt < this.config.gateCue.debounceMs) return false;
    this.cancelGate(); this.gateId = id; this.lastGateAt = this.now(); this.seenGateIds.add(id);
    if (this.seenGateIds.size > 64) this.seenGateIds.delete(this.seenGateIds.values().next().value);
    this.gateTimer = this.setTimer(() => { this.gateTimer = null; this.cancelGate(id); }, this.config.gateCue.durationMs);
    this.reconcile(); return true;
  }
  cancelGate(id) {
    if (id !== undefined && id !== this.gateId) return false;
    if (this.gateTimer !== null) this.clearTimer(this.gateTimer);
    this.gateTimer = null;
    const hadGate = this.gateId !== null; this.gateId = null;
    if (hadGate) { this.clear(); this.reconcile(); }
    return hadGate;
  }
  reconcile() {
    if (this.disposed || !this.enabled || this.hidden) { this.clear(); return; }
    const selected = this.gateId !== null
      ? {id: 'gate-cue', url: this.config.gateCue.url, gain: this.config.gateCue.maxGain, loop: false}
      : evaluate(this.position, this.config);
    if (!selected) { this.clear(); return; }
    if (this.output?.url !== selected.url || this.output?.loop !== selected.loop) {
      // A different asset begins at zero. Unload first so an outgoing source can never
      // inherit the new source's higher cap in the engine's crossfade implementation.
      this.clear(); this.output = selected;
      this.write('audioVolume', 0); this.write('audioLoop', selected.loop); this.write('playAudio', selected.url);
    } else this.output = selected;
    this.targetGain = selected.gain;
    // Movement can arrive faster than a fade tick in source harnesses. Update the
    // target without starving the already scheduled fade by cancelling it each time.
    if (this.fadeTimer !== null) return;
    const from = this.gain, start = this.now();
    if (Math.abs(from - this.targetGain) < 0.00001) return;
    const step = () => {
      this.fadeTimer = null;
      if (this.disposed || !this.enabled || this.hidden || !this.output) return;
      const progress = clamp((this.now() - start) / this.config.fadeMs);
      this.gain = from + (this.targetGain - from) * smooth(progress);
      this.write('audioVolume', this.gain);
      if (progress < 1) this.fadeTimer = this.setTimer(step, 30);
    };
    step();
  }
  dispose() {
    if (this.disposed) return;
    this.disposed = true; this.enabled = false;
    if (this.gateTimer !== null) this.clearTimer(this.gateTimer);
    this.gateTimer = null; this.gateId = null; this.clear();
  }
}

export function installNativeAudio(WA = globalThis.WA, host = globalThis.window, doc = globalThis.document) {
  let controller = null, disposed = false, revision = 0, prompt = null, menu = null, navigating = false;
  const subscriptions = [];
  const removePrompt = () => { const prior = prompt; prompt = null; if (prior) void prior.remove().catch(error => console.warn('Nearby audio prompt removal failed.', error)); };
  const updatePrompt = () => {
    if (disposed || !controller || controller.enabled || controller.hidden || !evaluate(controller.position, controller.config)) { removePrompt(); return; }
    if (!prompt) prompt = WA.ui.displayActionMessage({message: 'Enable nearby water and fire sounds', callback: () => {
      if (disposed || !controller || controller.hidden) return;
      controller.setEnabled(true); removePrompt(); refreshMenu();
    }});
  };
  const refreshMenu = () => {
    menu?.remove(); menu = null;
    if (disposed || !controller) return;
    menu = WA.ui.registerMenuCommand(controller.enabled ? 'Turn off nearby sounds' : 'Enable nearby sounds', {
      key: 'campus-native-nearby-audio', callback: () => { if (!disposed) { controller.setEnabled(!controller.enabled); updatePrompt(); refreshMenu(); } }
    });
  };
  const refresh = async () => {
    const at = ++revision;
    try { const position = await WA.player.getPosition(); if (!disposed && controller && at === revision) { controller.setPosition(position); updatePrompt(); } }
    catch (error) { if (!disposed && at === revision) { controller?.clear(); console.warn('Nearby audio position unavailable.', error); } }
  };
  const visibilityChanged = () => { controller?.setHidden(doc.hidden || navigating); updatePrompt(); if (!doc.hidden && !navigating) void refresh(); };
  const dispose = () => {
    if (disposed) return; disposed = true; ++revision;
    subscriptions.splice(0).forEach(subscription => subscription.unsubscribe());
    removePrompt(); menu?.remove(); menu = null; controller?.dispose();
    doc.removeEventListener('visibilitychange', visibilityChanged); host.removeEventListener('pagehide', dispose);
  };
  const ready = WA.onInit().then(async () => {
    if (disposed) return;
    const map = await WA.room.getTiledMap(); if (disposed) return;
    const config = readConfiguration(map);
    if (!supportsElementVolume(doc)) { console.warn('Nearby audio remains off: browser element-volume support is required for the approved gain caps.'); return; }
    controller = new NearbyAudio(WA, config); controller.setHidden(doc.hidden || navigating);
    subscriptions.push(WA.player.onPlayerMove(position => { ++revision; controller.setPosition(position); updatePrompt(); }));
    for (const source of config.sources) {
      subscriptions.push(WA.room.area.onEnter(source.areaName).subscribe(refresh));
      subscriptions.push(WA.room.area.onLeave(source.areaName).subscribe(() => { if (controller.output?.id === source.id) controller.clear(); void refresh(); }));
    }
    for (const zone of config.quietZones) {
      subscriptions.push(WA.room.area.onEnter(zone.areaName).subscribe(() => { controller.clear(); removePrompt(); void refresh(); }));
      subscriptions.push(WA.room.area.onLeave(zone.areaName).subscribe(refresh));
    }
    if (config.gateCue) subscriptions.push(WA.room.area.onLeave(config.gateCue.areaName).subscribe(() => { controller.cancelGate(); void refresh(); }));
    doc.addEventListener('visibilitychange', visibilityChanged); refreshMenu(); await refresh();
  }).catch(error => { controller?.dispose(); console.error('Native nearby audio initialization failed.', error); });
  host.addEventListener('pagehide', dispose, {once: true});
  return {
    ready, beginGate: id => controller?.beginGate(id) ?? false, cancelGate: id => controller?.cancelGate(id) ?? false, dispose,
    pauseForTransition: () => { navigating = true; controller?.setHidden(true); removePrompt(); },
    resumeAfterTransition: () => { navigating = false; if (!disposed) { controller?.setHidden(doc.hidden); void refresh(); } }
  };
}
