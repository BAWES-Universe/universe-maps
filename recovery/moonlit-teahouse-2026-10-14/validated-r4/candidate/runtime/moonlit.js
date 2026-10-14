/* Moonlit tea-house technical slice. Original maps unchanged. No runtime dependencies.
 * Production-safe default: open passage, shared opening, no automatic or public closing.
 * doorDemo=single-client (legacy qaDoorClose=1) is SINGLE-CLIENT TEST MODE, never multiplayer-safe occupancy arbitration.
 */
(function(root){'use strict';
// The ritual is local to this script instance: no shared or persisted tea state.
function createTeaExperience(WA,clock){
 let state='idle',position={x:0,y:0},timer=null,epoch=0,disposed=false,popup=null,promptKey='',cancelled=false;
 const shown=new Map(),notified={collected:false,served:false};
 const zone=()=>position.x>=176&&position.x<=320&&position.y>=272&&position.y<=352?'desk':position.x>=864&&position.x<=1024&&position.y>=384&&position.y<=480?'terrace':'away';
 function layer(name,on){if(shown.get(name)===on)return;WA.room[on?'showLayer':'hideLayer'](name);shown.set(name,on)}
 function close(){popup?.close();popup=null}
 function refresh(){
  layer('tea-preparing',state==='preparing');layer('tea-desk-cup',state==='ready');layer('tea-desk-steam',state==='preparing'||state==='ready');layer('tea-served-cup',state==='served');layer('tea-served-steam',state==='served');
  const z=zone(),key=state+':'+z;if(key===promptKey)return;promptKey=key;close();if(disposed||z==='away')return;
  let message='',label='',action;
  if(z==='desk'){
   if(state==='idle'){message=cancelled?'Preparation cancelled. Stay here while brewing.':'Prepare tea, then take it to the moon terrace.';label='Prepare tea';action=prepare}
   if(state==='preparing')message='Brewing tea… stay by the desk.';
   if(state==='ready'){message='Your tea is ready.';label='Collect tea';action=collect}
   if(state==='carrying'){message=notified.collected?'Carry your tea to the moon terrace.':'Tea collected. Walk to the moon terrace.';notified.collected=true;}
   if(state==='served')message='Tea is served on the terrace. Reset in Settings to brew again.';
  }else{
   if(state==='carrying'){message='Enjoy the view with your tea.';label='Serve tea';action=serve}
   else if(state==='served'){message=notified.served?'Your cup is waiting by the moonlit water.':'Tea served. Enjoy the moonlit water.';notified.served=true;}
   else message='Bring tea from the pavilion desk.';
  }
  popup=WA.ui.openPopup(z==='desk'?'tea-desk-prompt':'tea-terrace-prompt',message,label?[{label,callback:action}]:[{label:'Close',callback:close}]);
 }
 function cancel(){epoch++;if(timer!==null){clock.clearTimeout(timer);timer=null}}
 function prepare(){if(disposed||state!=='idle'||zone()!=='desk')return false;cancel();cancelled=false;state='preparing';refresh();const token=epoch;timer=clock.setTimeout(()=>{timer=null;if(disposed||token!==epoch||state!=='preparing')return;if(zone()!=='desk'){state='idle';cancelled=true}else state='ready';refresh()},1800);return true}
 function collect(){if(disposed||state!=='ready'||zone()!=='desk')return false;state='carrying';refresh();return true}
 function serve(){if(disposed||state!=='carrying'||zone()!=='terrace')return false;state='served';refresh();return true}
 function move(p){if(disposed)return;position=p;if(state==='preparing'&&zone()!=='desk'){cancel();state='idle';cancelled=true}refresh()}
 function reset(){if(disposed)return;cancel();state='idle';cancelled=false;notified.collected=false;notified.served=false;promptKey='';refresh()}
 function dispose(){disposed=true;cancel();close();for(const name of ['tea-preparing','tea-desk-cup','tea-desk-steam','tea-served-cup','tea-served-steam'])layer(name,false)}
 return{move,prepare,collect,serve,reset,dispose,status:()=>({state,zone:zone(),cancelled,disposed})};
}

function createExperience(WA,clock={setTimeout:(fn,ms)=>root.setTimeout(fn,ms),clearTimeout:id=>root.clearTimeout(id)}){
 let door='open',frame=4,doorEpoch=0,roofEpoch=0,roofInside=false,roofStage=0,disposed=false,position={x:448,y:704},moveCount=0,cameraTimer;
 const tea=createTeaExperience(WA,clock);
 const timers=new Set(),menus=[],subs=[],visibility=new Map(),cleanupErrors=[];
 const demo=()=>WA.room.hashParameters.doorDemo==='single-client'||WA.room.hashParameters.qaDoorClose==='1';
 function later(f,ms){const id=clock.setTimeout(()=>{timers.delete(id);if(!disposed)f()},ms);timers.add(id);return id}
 function visible(name,on){if(visibility.get(name)===on)return;WA.room[on?'showLayer':'hideLayer'](name);visibility.set(name,on)}
 function doorFrame(f){for(let i=0;i<=4;i++)visible('door-frame-'+i,i===f);frame=f}
 function occupied(){return position.x>=400&&position.x<=496&&position.y+16>=400&&position.y+16<=464}
 function failOpen(){doorEpoch++;door='open';doorFrame(4);visible('door-collision',false)}
 function animate(open){const token=++doorEpoch;door=open?'opening':'closing';let step=frame;
  function tick(){if(token!==doorEpoch)return;if(!open&&occupied()){openDoor();return}step+=open?1:-1;step=Math.max(0,Math.min(4,step));doorFrame(step);
   if(step===(open?4:0)){door=open?'open':'closed';visible('door-collision',!open);return}later(tick,80)}
  if(frame===(open?4:0)){door=open?'open':'closed';visible('door-collision',!open)}else later(tick,80);
 }
 function openDoor(){if(disposed)return;WA.state.doorOpen=true;animate(true)}
 async function closeForQA(){if(disposed||!demo())return false;
  const count=moveCount,p=await WA.player.getPosition();if(disposed)return false;if(count===moveCount)position=p;
  if(occupied())return false;animate(false);return true; // Local QA only: never writes a shared closed state.
 }
 function roofFrame(stage){for(let j=1;j<=4;j++)visible('roof-alpha-'+j,j===stage);roofStage=stage}
 function roof(inRoom){if(inRoom===roofInside)return;roofInside=inRoom;const token=++roofEpoch,target=inRoom?0:4;
  function tick(){if(token!==roofEpoch||roofStage===target)return;roofFrame(roofStage+Math.sign(target-roofStage));if(roofStage!==target)later(tick,70)}
  if(roofStage!==target)later(tick,70);
 }
 function move(p){moveCount++;position=p;tea.move(p);const x=p.x,y=p.y+16;
  const within=roofInside?x>=96&&x<=800&&y>=208&&y<=464:x>=128&&x<=768&&y>=240&&y<=432;
  roof(within);if(door==='closing'&&occupied())openDoor();
  // A player's new movement takes control back from the optional scenic view.
  if(cameraTimer){clock.clearTimeout(cameraTimer);timers.delete(cameraTimer);cameraTimer=null;WA.camera.followPlayer(true,250)}
 }
 function audio(on){if(!on){WA.room.setProperty('native-audio','playAudio',undefined);WA.room.setProperty('native-audio','nativeSoundscape',undefined);return}
  WA.room.setProperty('native-audio','nativeSoundscape',JSON.stringify({url:'audio/tide-signal.wav',volume:0.09,x:976,y:176,innerRadius:32,outerRadius:224}));
  WA.room.setProperty('native-audio','audioVolume',0);WA.room.setProperty('native-audio','audioLoop',true);WA.room.setProperty('native-audio','playAudio','audio/silent-carrier.wav');
 }
 function viewTerrace(){if(disposed)return;if(cameraTimer){clock.clearTimeout(cameraTimer);timers.delete(cameraTimer)}WA.camera.set(944,400,448,384,false,true,650);cameraTimer=later(()=>{cameraTimer=null;WA.camera.followPlayer(true,500)},1500)}
 // This engine removes script menus by label on iframe close; use the same supported key.
 function menu(label,fn){menus.push(WA.ui.registerMenuCommand(label,{key:label,callback:()=>{if(!disposed)fn()}}))}
 async function init(){failOpen();for(let j=1;j<=4;j++)visible('roof-alpha-'+j,false);
  subs.push(WA.state.onVariableChange('doorOpen').subscribe(value=>{if(value===true&&!disposed)animate(true)}));
  const subscription=WA.player.onPlayerMove(move);if(subscription)subs.push(subscription);
  menu(demo()?'DEMO (single client): open door':'Open pavilion door',openDoor);menu('View moon terrace',viewTerrace);menu('Enable test bell ambience',()=>audio(true));menu('Silence test ambience',()=>audio(false));
  menu('Reset tea ritual',()=>tea.reset());
  if(demo())menu('DEMO (single client): close door',closeForQA);
  const count=moveCount,p=await WA.player.getPosition();if(disposed)return;if(count===moveCount)move(p);
  // Outside initially: show a roof only after successful position initialization.
  if(!roofInside)roofFrame(4)
 }
 function dispose(){
  // Repeatable recovery: a previous failed cleanup must never suppress the next attempt.
  disposed=true;doorEpoch++;roofEpoch++;cleanupErrors.length=0;
  function attempt(label,fn){try{const result=fn();if(result&&typeof result.then==='function')result.catch(error=>cleanupErrors.push({label,error:String(error)}))}catch(error){cleanupErrors.push({label,error:String(error)})}}
  // Collision release comes first, independently of presentation, audio and menu failures.
  door='recovery-needed';
  attempt('open passage',()=>{WA.room.hideLayer('door-collision');visibility.set('door-collision',false);door='open'});
  for(let i=0;i<=4;i++)attempt('door frame '+i,()=>visible('door-frame-'+i,i===4));frame=4;
  for(const t of [...timers])attempt('cancel timer',()=>{clock.clearTimeout(t);timers.delete(t)});
  for(const s of subs)attempt('unsubscribe',()=>s?.unsubscribe?.());
  for(const m of menus)attempt('remove menu',()=>m?.remove?.());
  attempt('stop tea',()=>tea.dispose());
  attempt('stop audio',()=>WA.room.setProperty('native-audio','playAudio',undefined));
  attempt('remove ambience',()=>WA.room.setProperty('native-audio','nativeSoundscape',undefined));
  attempt('restore camera',()=>WA.camera.followPlayer(false));
  return cleanupErrors.slice();
 }

 return{init,tea,open:openDoor,closeForQA,audio,viewTerrace,dispose,status:()=>({door,frame,roofInside,roofStage,disposed,cleanupErrors:cleanupErrors.slice()})};
}
if(typeof module!=='undefined'&&module.exports)module.exports={createExperience,createTeaExperience};
else if(root.WA){let app;root.WA.onInit().then(async()=>{app=createExperience(root.WA);await app.init()}).catch(e=>{console.error('Moonlit initialization failed; authored doorway remains open',e);app?.dispose()});root.addEventListener?.('pagehide',()=>app?.dispose())}
})(typeof globalThis!=='undefined'?globalThis:this);
