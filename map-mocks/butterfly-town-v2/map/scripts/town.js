/* The Butterfly Gate · local, position-driven experience. No shared state or external services. */
(() => {
  'use strict';
  // Release gate: activate only after the compatible native PR712 build is deployed.
  // There is no reliable runtime feature probe for that behavioral fix.
  const ENABLE_NATIVE_AUDIO = false;
  let audioRuntime=null;
  const GATE = {x:512,y:384,width:1024,height:1536};
  const TOWN = {x:2304,y:512,width:1536,height:1024};
  const APPROACH = {x:832,y:1100,width:384,height:532};
  const THRESHOLD = {x:960,y:880,width:128,height:64};
  const RETURN = {x:3008,y:1424,width:128,height:64};
  const ROOMS = [{"id": "studenthub", "bounds": {"x": 2496, "y": 672, "width": 384, "height": 240}, "camera": [2688, 768, 512, 448]}, {"id": "cafe", "bounds": {"x": 3328, "y": 704, "width": 320, "height": 240}, "camera": [3488, 800, 448, 448]}, {"id": "archive", "bounds": {"x": 3360, "y": 1152, "width": 256, "height": 176}, "camera": [3488, 1216, 384, 384]}];
  const media=window.matchMedia('(prefers-reduced-motion: reduce)');
  const subscriptions=[];const visibility=new Map();
  let disposed=false,initialized=false,revision=0,sequence=0,transition=false;
  let scene=null,room=null,cameraOwner=null,approach=false,lastPosition=null;
  let gateArmed=true,returnArmed=true,aspect=1.5,seenAspect=false;
  const inside=(p,r)=>p.x>=r.x&&p.x<=r.x+r.width&&p.y+16>=r.y&&p.y+16<=r.y+r.height;
  function show(name,on){if(visibility.get(name)===on)return;visibility.set(name,on);(on?WA.room.showLayer:WA.room.hideLayer)(name);}
  function restore(smooth=true){if(cameraOwner===null)return;cameraOwner=null;WA.camera.followPlayer(smooth&&!media.matches,smooth&&!media.matches?650:0);}
  function focus(owner,rect){if(media.matches||cameraOwner===owner)return;restore(false);cameraOwner=owner;WA.camera.set(...rect,true,true,1000);}
  function visuals(){
    show('gate-surroundings',scene==='gate');show('gate-edge-fog',scene==='gate');show('gate-scenery-canopies',scene==='gate');show('gate-ground',scene==='gate');show('gate-front',scene==='gate');
    show('town-scenery-feet',scene==='town');show('town-scenery-canopies',scene==='town');show('town-edge-fog',scene==='town');show('town-surroundings',scene==='town');show('town-ground',scene==='town');show('town-details',scene==='town');show('town-olive-shadow',scene==='town');show('town-olive-feet',scene==='town');show('town-olive-canopies',scene==='town');
    show('gate-steady',scene==='gate');show('town-steady',scene==='town');
    show('gate-water',scene==='gate'&&!media.matches);show('gate-cascades',scene==='gate'&&!media.matches);show('gate-basin-mist',scene==='gate'&&!media.matches);show('town-water',scene==='town'&&!media.matches);
    show('gate-pulse',scene==='gate'&&!media.matches);show('town-pulse',scene==='town'&&!media.matches);
    show('gate-butterflies',scene==='gate'&&approach&&!media.matches);
    for(const r of ROOMS){show(r.id+'-furniture-feet',scene==='town');show(r.id+'-furniture-canopies',scene==='town');show(r.id+'-architecture',scene==='town');show(r.id+'-door-foreground',scene==='town');show(r.id+'-interior',scene==='town');show(r.id+'-roof',scene==='town'&&room!==r.id);show(r.id+'-focus',scene==='town'&&room===r.id);}
  }
  function setScene(next){if(next===scene)return;restore(false);scene=next;room=null;approach=false;visuals();}
  function reconcile(p,allowTransit=true){
    if(disposed||transition)return;lastPosition=p;
    const next=inside(p,TOWN)?'town':inside(p,GATE)?'gate':scene??'gate';
    setScene(next);
    if(scene==='gate'){
      const height=Math.min(1280,2000/aspect);
      const near=inside(p,APPROACH)&&p.y+16<=256+height-32;
      if(near!==approach){approach=near;if(near)focus('gate',[1024,256+height/2,Math.min(800,aspect*height),height]);else restore();visuals();}
      if(!inside(p,THRESHOLD))gateArmed=true;
      if(allowTransit&&gateArmed&&inside(p,THRESHOLD)){gateArmed=false;void travel('town',{x:3072,y:1168});}
    } else {
      const nextRoom=ROOMS.find(r=>inside(p,r.bounds))?.id??null;
      if(nextRoom!==room){restore();room=nextRoom;visuals();if(room){const r=ROOMS.find(r=>r.id===room);focus(room,r.camera);}}
      if(!inside(p,RETURN))returnArmed=true;
      if(allowTransit&&returnArmed&&inside(p,RETURN)){returnArmed=false;void travel('gate',{x:1024,y:1744});}
    }
  }
  async function travel(destination,p){
    if(disposed||transition)return;transition=true;const token=++sequence;++revision;
    restore(false);
    try{
      await WA.player.teleport(p.x,p.y);
      if(disposed||token!==sequence)return;
      transition=false;setScene(destination);reconcile(p,false);
      // Native teleport cancels movement. No input lock is acquired, so failures cannot trap the player.
    } catch(error){
      if(disposed||token!==sequence)return;transition=false;
      console.warn('The doorway did not complete. Step out and enter again.',error);
      try{const at=revision;const current=await WA.player.getPosition();if(!disposed&&token===sequence&&at===revision)reconcile(current,false);}catch(_){}
    }
  }
  function motionChanged(){if(disposed)return;if(media.matches)restore(false);visuals();}
  function observe(p){++revision;if(!transition)reconcile(p);}
  function dispose(){if(disposed)return;disposed=true;++sequence;audioRuntime?.dispose();restore(false);subscriptions.splice(0).forEach(s=>s?.unsubscribe?.());media.removeEventListener?.('change',motionChanged);}
  WA.onInit().then(async()=>{
    if(disposed)return;initialized=true;
    if(ENABLE_NATIVE_AUDIO){
      void import(new URL('scripts/town-audio-runtime.mjs',WA.room.mapURL).href).then(({createTownAudioRuntime})=>{
        if(disposed)return;audioRuntime=createTownAudioRuntime(WA,{enabled:true});return audioRuntime.ready;
      }).catch(error=>console.warn('Local water audio remains unavailable.',error));
    }
    media.addEventListener?.('change',motionChanged);
    const move=WA.player.onPlayerMove(observe);if(move)subscriptions.push(move);
    if(WA.camera.onCameraUpdate)subscriptions.push(WA.camera.onCameraUpdate().subscribe(v=>{if(!v.width||!v.height)return;const next=v.width/v.height;if(seenAspect&&Math.abs(next-aspect)>0.1)restore(false);aspect=next;seenAspect=true;}));
    // Also subscribe to native area edges for prompt visual changes between move samples.
    for(const name of ['gate-approach','gate-threshold','town-return',...ROOMS.map(r=>r.id+'-inside')]){
      for(const edge of ['onEnter','onLeave'])subscriptions.push(WA.room.area[edge](name).subscribe(async()=>{
        const at=++revision;const p=await WA.player.getPosition();if(!disposed&&!transition&&at===revision)reconcile(p);
      }));
    }
    const at=revision;const p=await WA.player.getPosition();if(!disposed&&at===revision)reconcile(p);
  }).catch(error=>console.error('Town experience could not initialize',error));
  window.addEventListener('pagehide',dispose,{once:true});
})();
