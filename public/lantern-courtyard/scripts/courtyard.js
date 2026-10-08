/* Original Lantern Courtyard. Local visual layers only; no services or player-control lock. */
(() => {
  'use strict';
  const gathering = {name:'butterfly-gathering',x:480,y:288,width:160,height:160};
  const alcove = {name:'covered-alcove',x:128,y:144,width:96,height:80};
  const subscriptions=[];
  const media=window.matchMedia('(prefers-reduced-motion: reduce)');
  let active=false, sheltered=false, disposed=false, cameraChanged=false, eventVersion=0, viewport;
  const inside=(p,z)=>p.x>=z.x&&p.x<z.x+z.width&&p.y>=z.y&&p.y<z.y+z.height;
  const visible=(name,on)=>WA.room[on?'showLayer':'hideLayer'](name);
  function restoreCamera(){
    if(!cameraChanged)return;
    cameraChanged=false;
    WA.camera.followPlayer(!media.matches,media.matches?0:650);
  }
  function ambient(){
    visible('lantern-steady',media.matches);
    visible('lantern-flicker',!media.matches);
    visible('pool-ripples',!media.matches);
    visible('gathering-butterflies',active&&!media.matches);
    if(media.matches)restoreCamera();
  }
  function enter(){
    eventVersion++;
    if(active||disposed)return;
    active=true;visible('gathering-glow',true);visible('gathering-butterflies',!media.matches);
    // Keep the user's zoom. A small pan is allowed only with a confirmed wide world viewport.
    // No initial viewport event or a narrow/mobile view means normal player-follow throughout.
    if(!media.matches&&viewport&&viewport.width>=384&&viewport.height>=288){
      WA.camera.set(552,352,undefined,undefined,true,true,800);cameraChanged=true;
    }
  }
  function leave(){
    eventVersion++;
    if(!active)return;
    active=false;visible('gathering-glow',false);visible('gathering-butterflies',false);restoreCamera();
  }
  function roofEnter(){eventVersion++;if(disposed)return;sheltered=true;visible('alcove-roof',false);}
  function roofLeave(){eventVersion++;sheltered=false;visible('alcove-roof',true);}
  function motionChanged(){if(!disposed)ambient();}
  function dispose(){
    if(disposed)return;
    leave();if(sheltered)roofLeave();disposed=true;
    subscriptions.splice(0).forEach(s=>s.unsubscribe());
    media.removeEventListener?.('change',motionChanged);
  }
  WA.onInit().then(async()=>{
    if(disposed)return;
    visible('gathering-glow',false);visible('gathering-butterflies',false);visible('alcove-roof',true);ambient();
    subscriptions.push(WA.room.area.onEnter(gathering.name).subscribe(enter));
    subscriptions.push(WA.room.area.onLeave(gathering.name).subscribe(leave));
    subscriptions.push(WA.room.area.onEnter(alcove.name).subscribe(roofEnter));
    subscriptions.push(WA.room.area.onLeave(alcove.name).subscribe(roofLeave));
    subscriptions.push(WA.camera.onCameraUpdate().subscribe(v=>{viewport=v;if(cameraChanged&&(v.width<384||v.height<288))restoreCamera();}));
    media.addEventListener?.('change',motionChanged);
    const version=eventVersion;const p=await WA.player.getPosition();
    // Fork subscriptions do not replay initial membership. Avoid overwriting a newer movement event.
    if(!disposed&&version===eventVersion){if(inside(p,gathering))enter();if(inside(p,alcove))roofEnter();}
  }).catch(error=>console.error('Courtyard visual initialization failed',error));
  window.addEventListener('pagehide',dispose,{once:true});
})();
