/* Native-only, local-property bridge. Production must remain disabled until native/device acceptance. */
import { AUDIO_ASSETS, CampusAudioDirector, FUNCTIONAL_SILENT_ZONES } from './campus-audio.mjs';

export const AUDIO_LAYER = 'campus-audio-control';
export const ENABLE_NATIVE_AUDIO = false;
const MAX_GAIN = 0.06;
const validGain = volume => Number.isFinite(volume) && volume > 0 && volume <= MAX_GAIN;
export function createNativeAudioAdapter(WA, { layer = AUDIO_LAYER } = {}) {
  let active = false, currentUrl;
  const property = (name, value) => WA.room.setProperty(layer, name, value);
  const silence = () => {
    if (!active) return;
    // undefined removes a property. Never pass null or an empty URL to native playback.
    property('playAudio', undefined);
    active = false;
    currentUrl = undefined;
    property('audioVolume', undefined);
    property('audioLoop', undefined);
  };
  return {
    setSource(url, { volume, loop = true }) {
      if (!Object.values(AUDIO_ASSETS).includes(url) || !validGain(volume) ||
          (url === AUDIO_ASSETS.cascade && volume > 0.05)) throw Error('Invalid campus water source or gain');
      // Native gain changes update the current slot immediately. Release a DIFFERENT
      // feature first so its outgoing slot cannot inherit this source's gain or
      // remain audible after a teleport. Same-URL local movement never unloads.
      if (active && currentUrl !== url) silence();
      // Authored gain precedes source: a newly allocated native slot cannot start at 1.
      property('audioVolume', volume);
      property('audioLoop', loop === true);
      active = true;
      currentUrl = url;
      property('playAudio', url);
    },
    setVolume(volume) {
      if (!validGain(volume) || (currentUrl === AUDIO_ASSETS.cascade && volume > 0.05)) throw Error('Invalid local water gain');
      if (active) property('audioVolume', volume);
    },
    silence,
    stop: silence,
  };
}

export function createCampusAudioRuntime(WA, { enabled = false, eventTarget = globalThis.window, adapter, onState, onError, policy = {} } = {}) {
  let disposed = false, revision = 0, director;
  const subscriptions = [];
  const dispose = () => {
    if (disposed) return;
    disposed = true; ++revision;
    subscriptions.splice(0).forEach(subscription => subscription?.unsubscribe?.());
    eventTarget?.removeEventListener?.('pagehide', dispose);
    director?.dispose();
  };
  const fail = error => { dispose(); onError?.(error); };
  const observe = position => {
    if (disposed || !director) return;
    ++revision;
    const state = director.observe(position);
    onState?.(state);
    return state;
  };
  const refresh = async () => {
    if (enabled !== true || disposed || !director) return;
    const at = ++revision;
    try {
      const position = await WA.player.getPosition();
      if (!disposed && at === revision) return observe(position);
    } catch (error) { if (!disposed && at === revision) fail(error); }
  };
  // pagehide during slow initialization must also invalidate the pending setup.
  if (enabled === true) eventTarget?.addEventListener?.('pagehide', dispose, { once: true });
  // Disabled means NO initialization, subscriptions, properties, fetches, or media.
  const ready = enabled === true ? Promise.resolve().then(() => WA.onInit()).then(async () => {
    if (disposed) return;
    if (typeof WA.room?.setProperty !== 'function') throw Error('Native room property API unavailable');
    if (typeof WA.player?.onPlayerMove !== 'function' || typeof WA.player?.getPosition !== 'function') throw Error('Native player position API unavailable');
    director = new CampusAudioDirector(adapter ?? createNativeAudioAdapter(WA), policy);
    subscriptions.push(WA.player.onPlayerMove(position => { try { observe(position); } catch (error) { fail(error); } }));
    for (const zone of policy.geometry?.silentZones ?? FUNCTIONAL_SILENT_ZONES) {
      for (const edge of ['onEnter', 'onLeave']) {
        const source = WA.room.area?.[edge]?.(zone.id + '-inside');
        if (source?.subscribe) subscriptions.push(source.subscribe(refresh));
      }
    }
    // An already-moving player outranks this asynchronous initial position read.
    await refresh();
  }).catch(error => { fail(error); throw error; }) : Promise.resolve();
  return { ready, dispose, observe, refresh, get enabled() { return enabled === true && !disposed; } };
}
