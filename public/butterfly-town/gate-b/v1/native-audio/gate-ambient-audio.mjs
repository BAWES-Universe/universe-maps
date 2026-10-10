/* One preattenuated gate loop through the existing native map audio channel.
 * Native API contract reviewed at f00b3482f23c51976b4b339d7a891cad683d6498.
 * No Audio/WebAudio player, volume-support probe, persisted setting, or engine patch.
 */
const property = (holder, name) => holder.properties?.find(item => item.name === name)?.value;
const flatten = layers => layers.flatMap(layer => layer.type === 'group' ? flatten(layer.layers) : [layer]);
const AUDIO_PROPERTIES = ['playAudio', 'playAudioLoop', 'audioVolume', 'audioLoop'];

export function readConfiguration(map) {
  const fail = message => { throw new Error('Gate ambient audio: ' + message); };
  const raw = property(map, 'gateAmbientAudio');
  if (typeof raw !== 'string') fail('missing gateAmbientAudio configuration');
  const config = JSON.parse(raw);
  if (config.version !== 1 || config.scene !== 'gate' || config.startPolicy !== 'explicit-per-map' ||
      config.carrierLayer !== 'campus-audio-control' || config.sourceVolume !== 1 ||
      config.url !== 'native-audio/assets/gate-music-waterfalls-loop.mp3') fail('invalid configuration');
  const layers = flatten(map.layers);
  const carrier = layers.find(layer => layer.name === config.carrierLayer);
  if (!carrier || carrier.type !== 'tilelayer' || carrier.x || carrier.y || carrier.offsetx || carrier.offsety ||
      carrier.width !== map.width || carrier.height !== map.height || !Array.isArray(carrier.data) ||
      carrier.data.length !== map.width * map.height ||
      carrier.data.some(gid => !Number.isInteger(gid) || gid <= 0)) fail('carrier must cover the map');
  const holders = [map, ...layers, ...layers.flatMap(layer => layer.objects ?? []),
    ...map.tilesets.flatMap(set => set.tiles ?? [])];
  if (holders.some(holder => AUDIO_PROPERTIES.some(name => property(holder, name) !== undefined))) {
    fail('another native audio source is configured');
  }
  return Object.freeze(config);
}

export class GateAmbientAudio {
  constructor(WA, config) {
    this.WA = WA;
    this.config = config;
    this.enabled = false;
    this.loaded = false;
    this.navigating = false;
    this.disposed = false;
  }
  write(name, value) { this.WA.room.setProperty(this.config.carrierLayer, name, value); }
  setEnabled(enabled) {
    if (this.disposed || this.navigating) return false;
    if (!enabled) { this.clear(); this.enabled = false; return true; }
    if (this.loaded) return true;
    // The asset itself contains its maximum intended level. Source volume 1 adds
    // no amplification, even when a browser ignores HTMLMediaElement.volume.
    this.write('audioVolume', 1);
    this.write('audioLoop', true);
    this.loaded = true;
    this.write('playAudio', this.config.url);
    this.enabled = true;
    return true;
  }
  clear() {
    if (!this.loaded) return;
    // Removing the one source invokes native stop/unload, with no outgoing fade.
    this.write('playAudio', undefined);
    this.write('audioLoop', undefined);
    this.write('audioVolume', undefined);
    this.loaded = false;
  }
  // Keep the original gate journey's hook contract; the fixed ambient loop does
  // not introduce a cue, restart, source switch, or timing change at the portal.
  beginGate() { return false; }
  cancelGate() { return false; }
  pauseForTransition() {
    if (this.disposed) return;
    this.navigating = true;
    this.enabled = false;
    this.clear();
  }
  resumeAfterTransition() {
    if (this.disposed) return;
    this.navigating = false;
    // A cancelled/failed navigation only offers explicit Play again. A new
    // native source would clear native Stop, so never reinstall it automatically.
  }
  dispose() {
    if (this.disposed) return;
    this.enabled = false;
    this.clear();
    this.disposed = true;
  }
}

export function installGateAmbientAudio(WA = globalThis.WA, host = globalThis.window, doc = globalThis.document) {
  let controller = null, disposed = false, navigating = false, menu = null;
  const refreshMenu = () => {
    menu?.remove(); menu = null;
    if (disposed || !controller || navigating) return;
    menu = WA.ui.registerMenuCommand(controller.enabled ? 'Stop gate music and waterfalls' : 'Play gate music and waterfalls', {
      key: 'gate-ambient-audio',
      callback: () => {
        if (disposed || navigating || doc.hidden) return;
        controller.setEnabled(!controller.enabled);
        refreshMenu();
      }
    });
  };
  // No edge observers or on-screen action messages. Playback/background behavior
  // remains governed by native Pause/Stop/Mute and the browser, without reloads.
  const dispose = () => {
    if (disposed) return;
    disposed = true;
    controller?.dispose(); menu?.remove(); menu = null;
    host.removeEventListener('pagehide', dispose);
  };
  const ready = WA.onInit().then(async () => {
    if (disposed) return;
    const map = await WA.room.getTiledMap();
    if (disposed) return;
    controller = new GateAmbientAudio(WA, readConfiguration(map));
    if (navigating) controller.pauseForTransition();
    refreshMenu();
  }).catch(error => { dispose(); console.error('Gate ambient audio initialization failed.', error); });
  host.addEventListener('pagehide', dispose, { once: true });
  return {
    ready,
    beginGate: id => controller?.beginGate(id) ?? false,
    cancelGate: id => controller?.cancelGate(id) ?? false,
    pauseForTransition: () => {
      navigating = true; controller?.pauseForTransition(); refreshMenu();
    },
    resumeAfterTransition: () => {
      if (disposed) return;
      navigating = false; controller?.resumeAfterTransition(); refreshMenu();
    },
    dispose
  };
}
