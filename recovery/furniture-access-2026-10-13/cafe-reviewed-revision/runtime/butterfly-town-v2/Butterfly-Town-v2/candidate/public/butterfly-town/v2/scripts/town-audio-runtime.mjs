/* Native-only environmental audio bridge. No independent audio player.
 * Requires the reviewed PR712 native audio behavior before activation.
 * All playback uses existing active-layer playAudio/audioVolume/audioLoop.
 */
import {TownAudioDirector, FUNCTIONAL_SILENT_ZONES} from './town-audio.mjs';

export const AUDIO_LAYER = 'midnight-surroundings';
export function createNativeAudioAdapter(WA, {layer = AUDIO_LAYER} = {}) {
  let active = false;
  const property = (name, value) => WA.room.setProperty(layer, name, value);
  const silence = () => {
    // undefined is the actual WA unsetting contract. Null/empty URL is unsafe.
    // Unload first, immediately releasing BOTH native crossfade slots.
    property('playAudio', undefined);
    property('audioVolume', undefined);
    property('audioLoop', undefined);
    active = false;
  };
  return {
    setSource(url, {volume, loop}) {
      if (!Number.isFinite(volume) || volume <= 0 || volume > .35) throw new Error('Invalid local audio gain');
      // Gain/loop precede the URL so a new source never starts at default gain.
      property('audioVolume', volume);
      property('audioLoop', loop === true);
      property('playAudio', url);
      active = true;
    },
    setVolume(volume) {if (active) property('audioVolume', volume);},
    silence,
    stop: silence,
    // Gate cue is deliberately unavailable in this release candidate.
    playCue() {throw new Error('Gate cue is disabled in this candidate');},
  };
}

export function createTownAudioRuntime(WA, {enabled = false, eventTarget = globalThis.window, adapter, onState} = {}) {
  let disposed = false, revision = 0, director;
  const subscriptions = [];
  const dispose = () => {
    if (disposed) return;
    disposed = true; ++revision;
    subscriptions.splice(0).forEach(s => s?.unsubscribe?.());
    eventTarget?.removeEventListener?.('pagehide', dispose);
    director?.dispose();
  };
  const observe = position => {
    if (disposed || !director) return;
    ++revision;
    const state = director.observe(position);
    onState?.(state);
    return state;
  };
  // Do not change visibility behavior: native background playback is retained.
  // pagehide is actual navigation/disposal, not an ordinary hidden tab.
  if (enabled) eventTarget?.addEventListener?.('pagehide', dispose, {once:true});
  const ready = enabled ? WA.onInit().then(async () => {
    if (disposed) return;
    if (typeof WA.room.setProperty !== 'function') throw new Error('Native map property API unavailable');
    director = new TownAudioDirector(adapter ?? createNativeAudioAdapter(WA), {enableGateCue:false});
    subscriptions.push(WA.player.onPlayerMove(observe));
    // Native room edges are also sampled, guarded against stale async reads.
    for (const zone of FUNCTIONAL_SILENT_ZONES) {
      for (const edge of ['onEnter', 'onLeave']) {
        const source = WA.room.area?.[edge]?.(zone.id + '-inside');
        if (source) subscriptions.push(source.subscribe(async () => {
          const at = ++revision;
          const position = await WA.player.getPosition();
          if (!disposed && at === revision) observe(position);
        }));
      }
    }
    const at = revision;
    const position = await WA.player.getPosition();
    if (!disposed && at === revision) observe(position);
  }).catch(error => {
    dispose();
    throw error;
  }) : Promise.resolve();
  return {ready, dispose, observe, get enabled() {return enabled && !disposed;}};
}
