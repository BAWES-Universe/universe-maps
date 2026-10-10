/* Gate B v3: the FIRST IIFE below is the preserved Bv2 portal/audio core.
 * Its camera-free comments apply only to that core. Separate v3 camera controllers follow.
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

/* Separate camera-only v3 experiment; v2 portal/audio core above is byte-preserved. */
(()=>{
/* Experimental Gate B v3 reveal, existing public APIs only.
 * One native timed pan/zoom per map visit; widened zoom is retained by native
 * movement-triggered follow. This reveal controller never calls followPlayer: that would restore old zoom.
 */
function installGateReveal(WA, host = window) {
  const state = {phase:'waiting', reason:null, commands:0};
  const api=WA?.camera;
  if (typeof api?.set!=='function' || typeof api?.onCameraUpdate!=='function' || typeof WA?.player?.onPlayerMove!=='function') {
    state.phase='disabled';state.reason='camera-api-unavailable';return {state,dispose(){}};
  }
  const media=host.matchMedia('(prefers-reduced-motion: reduce)');
  const now=()=>host.performance.now();
  let disposed=false,view=null,viewAt=-Infinity,approached=false,lastY=null;
  const subscriptions=[];
  const finite=(...values)=>values.every(Number.isFinite);
  subscriptions.push(api.onCameraUpdate().subscribe(next=>{
    if(disposed || !next || !finite(next.x,next.y,next.width,next.height,next.zoom) || next.width<64 || next.height<64 || next.width>4096 || next.height>4096 || next.zoom<=0 || next.zoom>16)return;
    view={...next};viewAt=now();
  }));
  subscriptions.push(WA.player.onPlayerMove(position=>{
    if(disposed || state.phase==='revealed' || state.phase==='disabled' || !position || !finite(position.x,position.y))return;
    const previousY=lastY;lastY=position.y;
    // A real approach from the lower flight, with separate arm and trigger lines.
    // A spawn/teleport already above the landing does not trigger a reveal.
    if(position.y>=896)approached=true;
    if(!approached || previousY===null || position.y>=previousY || position.y>816 || position.y<752 || position.x<416 || position.x>576)return;
    if(media.matches){state.phase='disabled';state.reason='reduced-motion';return;}
    if(!view || now()-viewAt>96){state.reason='no-fresh-native-viewport';return;}
    // Keep a small native Woka readable. zoom is native CSS scale in normal Follow.
    // Already very wide/exploration views are left alone.
    const duration=200;
    // Native follow glide temporarily relaxes map bounds. Reserve travel at
    // 360 world px/s through both 200ms phases, plus one sprite half-width.
    // Skip a reveal that would need a later map-edge correction.
    const reserve=360*(duration*2/1000)+16;
    const safeWidth=2*Math.min(position.x-16,960-position.x-16);
    const safeHeight=2*Math.min(position.y-reserve,1440-position.y-reserve);
    const factor=Math.min(1.12,(32*view.zoom)/20,safeWidth/view.width,safeHeight/view.height);
    if(factor<1.025 || view.width>960 || view.height>1440){state.reason='deferred-for-frame-or-avatar-budget';return;}
    state.phase='revealed';state.reason=null;state.commands++;
    state.before={...view};state.factor=factor;state.duration=duration;
    // Preserve the actual viewport centre, including native bounds/HUD offset.
    // One call only; native pan and native movement-follow glide own every frame.
    api.set(view.x+view.width/2,view.y+view.height/2,view.width*factor,view.height*factor,false,true,duration);
  }));
  return {state,dispose(){if(disposed)return;disposed=true;subscriptions.forEach(s=>s?.unsubscribe?.());state.phase='disposed';}};
}

/* Experimental portrait arrival using existing APIs only.
 * The script iframe is hidden: never use its innerWidth or width media queries.
 * Device classification uses coarse pointer and Screen Orientation when available.
 * Authored overview dimensions are world coordinates, not a claimed viewport query.
 */
function installMobileArrivalExperiment(WA,host=window,overview={width:640,height:1280}){
 const state={phase:'skipped',commands:0};
 const coarse=host.matchMedia('(pointer: coarse)').matches;
 const orientationType=host.screen?.orientation?.type;
 const portrait=typeof orientationType==='string' ? orientationType.startsWith('portrait') :
   Number.isFinite(host.orientation) ? Math.abs(host.orientation)%180===0 : host.screen.width<host.screen.height;
 state.device={coarse,portrait,orientationSource:typeof orientationType==='string'?'screen.orientation.type':Number.isFinite(host.orientation)?'legacy-window-orientation':'screen-aspect-heuristic'};
 const portraitCoarse=coarse && portrait;
 const empty=()=>({state,ready:Promise.resolve(),dispose(){}});
 if(!portraitCoarse||host.matchMedia('(prefers-reduced-motion: reduce)').matches||typeof WA?.camera?.set!=='function'||typeof WA?.camera?.followPlayer!=='function'||typeof WA?.player?.getPosition!=='function')return empty();
 let disposed=false,origin=null,latest=null;
 state.phase='waiting-for-position';
 const subscription=WA.player.onPlayerMove(position=>{
   if(disposed||!Number.isFinite(position?.x)||!Number.isFinite(position?.y))return;
   latest={x:position.x,y:position.y};
   if(state.phase!=='establishing')return;
   if(host.matchMedia('(prefers-reduced-motion: reduce)').matches){state.phase='motion-disabled';return;}
   if(position.y>origin.y-128)return;
   state.phase='walking';state.commands++;
   WA.camera.followPlayer(true,400);
 });
 const ready=WA.player.getPosition().then(position=>{
   if(disposed)return;
   if(host.matchMedia('(prefers-reduced-motion: reduce)').matches){state.phase='skipped';state.reason='reduced-motion';return;}
   const start=latest??position;
   // Late loading or joining at the gate must not drag the camera back to spawn.
   if(!Number.isFinite(start?.x)||!Number.isFinite(start?.y)||start.y<1056||start.x<352||start.x>608){state.phase='skipped';state.reason='already-away-from-arrival';return;}
   origin={...start};state.phase='establishing';state.commands++;
   WA.camera.set(480,800,overview.width,overview.height,false,false);
 }).catch(()=>{state.phase='skipped';state.reason='position-unavailable';});
 return{state,ready,dispose(){disposed=true;subscription.unsubscribe?.();}};
}

let disposed=false,revealController,arrivalController;
window.addEventListener('pagehide',()=>{disposed=true;revealController?.dispose();arrivalController?.dispose();},{once:true});
WA.onInit().then(()=>{if(disposed)return;
arrivalController=installMobileArrivalExperiment(WA,window);
revealController=installGateReveal(WA,window);
}).catch(error=>console.warn('Gate camera experiment unavailable; native camera retained.',error));
})();
