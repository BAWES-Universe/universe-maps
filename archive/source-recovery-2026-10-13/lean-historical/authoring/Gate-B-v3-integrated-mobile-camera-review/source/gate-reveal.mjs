/* Experimental Gate B v3 reveal, existing public APIs only.
 * One native timed pan/zoom per map visit; widened zoom is retained by native
 * movement-triggered follow. This reveal controller never calls followPlayer: that would restore old zoom.
 */
export function installGateReveal(WA, host = window) {
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
