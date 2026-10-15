/* Unpublished visual candidate. Adapted camera/audio lifecycle from r4.
 * Original Moonlit artwork and collision are unchanged. No shared state writes.
 * Roof/door/tea integration deliberately withheld: required art is not recovered.
 */
(function(root){
 let disposed=false,timer=null,menus=[],lastPosition=null;
 function follow(){if(timer!==null){root.clearTimeout(timer);timer=null}WA.camera.followPlayer(true,400)}
 function audio(on){
  if(!on){WA.room.setProperty('native-audio','playAudio',undefined);WA.room.setProperty('native-audio','nativeSoundscape',undefined);return}
  WA.room.setProperty('native-audio','nativeSoundscape',JSON.stringify({url:'audio/tide-signal.wav',volume:0.05,x:880,y:560,innerRadius:32,outerRadius:450}));
  WA.room.setProperty('native-audio','audioVolume',0);WA.room.setProperty('native-audio','audioLoop',true);WA.room.setProperty('native-audio','playAudio','audio/silent-carrier.wav');
 }
 function view(){if(timer!==null)root.clearTimeout(timer);WA.camera.set(768,512,1536,1024,false,true,650);timer=root.setTimeout(()=>{timer=null;if(!disposed)follow()},6000)}
 function menu(label,callback){menus.push(WA.ui.registerMenuCommand(label,{key:label,callback:()=>{if(!disposed)callback()}}))}
 root.WA.onInit().then(()=>{disposed=false;menu('View Moonlit courtyard',view);menu('Return to walking view',follow);menu('Enable quiet bell ambience',()=>audio(true));menu('Silence ambience',()=>audio(false));WA.player.onPlayerMove(p=>{const moved=lastPosition&&(Math.abs(p.x-lastPosition.x)>0.5||Math.abs(p.y-lastPosition.y)>0.5);lastPosition=p;if(timer!==null&&moved)follow()})});
 root.addEventListener('pagehide',()=>{disposed=true;if(timer!==null)root.clearTimeout(timer);audio(false);menus.forEach(m=>m.remove());WA.camera.followPlayer(false)});
})(globalThis);
