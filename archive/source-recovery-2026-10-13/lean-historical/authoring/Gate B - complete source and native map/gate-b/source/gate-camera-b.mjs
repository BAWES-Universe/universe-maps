/* Gate B: one-way detail-to-monument reveal using supported native map APIs.
 * Source contract: Universe f00b3482f23c51976b4b339d7a891cad683d6498.
 * No zoom-back-in on arrival or retreat. No movement controls are disabled.
 */
export const CAMERA_B = Object.freeze({startY:1136,endY:624,startWidth:416,startHeight:480,portraitEndWidth:704,landscapeEndHeight:736,intervalMs:60});
const clamp = (n,a,b) => Math.min(b,Math.max(a,n));
export function framing(aspect, progress, initialWidth) {
  const p=clamp(progress,0,1), eased=p*p*(3-2*p);
  const endWidth=Math.max(initialWidth,aspect>=1?CAMERA_B.landscapeEndHeight*aspect:Math.min(944,1360*aspect,aspect<0.8?CAMERA_B.portraitEndWidth:944));
  const width=initialWidth+(endWidth-initialWidth)*eased;
  return {width,height:width/aspect};
}
export function releaseAtCurrentZoom(WA, view, position) {
  // Both set forms save the current native zoom. No dimensions means no zoom
  // change, so followPlayer restores THIS zoom instead of an earlier step.
  const x=view?view.x+view.width/2:position.x, y=view?view.y+view.height/2:position.y;
  WA.camera.set(x,y,undefined,undefined,true,false,0);
  WA.camera.followPlayer(false,0);
}
export function installGateCameraB(WA=globalThis.WA, host=globalThis.window, clock=()=>performance.now()) {
  const media=host.matchMedia('(prefers-reduced-motion: reduce)');
  let disposed=false, started=false, active=!media.matches, everChanged=false, view=null, position=null;
  let maxProgress=0, initialWidth=0, aspect=0, displayedWidth=0, requestedWidth=0, initialAt=0, monumentFocus=false;
  let timer=null, subscription=null, menu=null, lastWidth=0, released=false, reason=media.matches?'reduced-motion':'awaiting-spawn';
  const clearTimer=()=>{if(timer!==null){host.clearTimeout(timer);timer=null;}};
  const stop=(why,release=true)=>{
    if(disposed)return;
    active=false;reason=why;clearTimer();
    if(release&&everChanged&&position&&!released){released=true;releaseAtCurrentZoom(WA,view,position);}
  };
  const issue=(width,height)=>{
    if(disposed||!active||!position)return;
    requestedWidth=width;everChanged=true;
    // Positioned mode yields to native player-follow on their next movement.
    // Immediate small size steps avoid overlapping engine pan/zoom tweens.
    WA.camera.set(position.x,position.y,width,height,false,false,0);
  };
  function tick(){
    timer=null;
    if(disposed||!active||!view||!initialWidth||!position)return;
    const target=framing(aspect,maxProgress,initialWidth);
    const remaining=target.width-displayedWidth;
    if(remaining>0.2){
      displayedWidth += Math.min(remaining,Math.max(0.5,remaining*0.28));
      issue(displayedWidth,displayedWidth/aspect);
      timer=host.setTimeout(tick,CAMERA_B.intervalMs);
    }else {
      reason=maxProgress>=1?'monument-hold':'waiting-for-progress';
      if(aspect>=1&&maxProgress>=1&&position.y<=576&&!monumentFocus){
        monumentFocus=true;
        // A landscape screen needs a small upward framing pan to see the crown.
        // Missing dimensions preserve the already-reached zoom exactly.
        const from={x:view.x+view.width/2,y:view.y+view.height/2},began=clock();
        const pan=()=>{
          timer=null;if(disposed||!active||!monumentFocus)return;
          const t=clamp((clock()-began)/700,0,1),e=1-Math.cos(t*Math.PI/2);
          WA.camera.set(from.x+(480-from.x)*e,from.y+(CAMERA_B.landscapeEndHeight/2-from.y)*e,undefined,undefined,true,false,0);
          if(t<1)timer=host.setTimeout(pan,40);
        };
        pan();
      }
    }
  }
  function update(p){
    if(disposed)return;position={x:p.x,y:p.y};
    if(!active)return;
    if(monumentFocus){
      if(p.y>624||Math.abs(p.x-480)>320)stop('retreat-native-follow');
      return;
    }
    if(!started){
      started=true;initialAt=clock();reason='close-start';
      issue(CAMERA_B.startWidth,CAMERA_B.startHeight);
      const settle=()=>{
        timer=null;if(disposed||!active)return;
        if(!view){timer=host.setTimeout(settle,160);return;}
        initialWidth=view.width;displayedWidth=view.width;lastWidth=view.width;aspect=view.width/view.height;tick();
      };
      timer=host.setTimeout(settle,160);
      return;
    }
    maxProgress=Math.max(maxProgress,clamp((CAMERA_B.startY-p.y)/(CAMERA_B.startY-CAMERA_B.endY),0,1));
    if(initialWidth&&timer===null)tick();
  }
  function cameraUpdated(v){
    if(disposed||!(v.width>0&&v.height>0))return;
    const previous=view;view={x:v.x,y:v.y,width:v.width,height:v.height,zoom:v.zoom};
    if(!active||!started)return;
    const nextAspect=v.width/v.height;
    if(!initialWidth)return; // Await the settled initial viewport, not a stale pre-command event.
    if(Math.abs(nextAspect/aspect-1)>0.08){stop('viewport-changed');return;}
    // The API has no gesture-origin flag. These conservative checks yield on
    // a clear unexpected zoom-in or a jump beyond the requested pullback.
    // A menu command is the deterministic opt-out for subtle gesture changes.
    if(clock()-initialAt>700&&previous){
      if(v.width<lastWidth*0.94 || v.width>Math.max(requestedWidth,lastWidth)*1.13){stop('manual-or-external-camera');return;}
    }
    lastWidth=v.width;
  }
  function motionChanged(){if(media.matches)stop('reduced-motion');}
  const ready=WA.onInit().then(()=>{
    if(disposed)return;
    subscription=WA.camera.onCameraUpdate().subscribe(cameraUpdated);
    menu=WA.ui.registerMenuCommand('Use my camera', {key:'gate-camera-manual',callback:()=>stop('manual-menu')});
    media.addEventListener?.('change',motionChanged);
  });
  function dispose(){
    if(disposed)return;if(monumentFocus&&everChanged&&position&&!released){released=true;releaseAtCurrentZoom(WA,view,position);}clearTimer();subscription?.unsubscribe?.();menu?.remove?.();
    media.removeEventListener?.('change',motionChanged);disposed=true;active=false;reason='disposed';
  }
  return {ready,update,release:()=>stop('navigation'),dispose,snapshot:()=>({active,started,maxProgress,displayedWidth,requestedWidth,aspect,reason,view})};
}
