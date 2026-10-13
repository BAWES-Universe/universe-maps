/* Native map-only lighthouse interiors. Progress is private to this same-map visit. */
(function(root){
'use strict';
function createExperience(WA, layout){
 let state={chart:false,key:false,fuse:false,power:false,bearing:0,lens:0,signal:[],complete:false},current=null,popup=null,notice=null,epoch=0,disposed=false,busy=false,moveSub,menus=[],moveCount=0,transitionId=0;
 const anchors=layout.anchors;
 function close(){epoch++;if(popup){popup.close();popup=null;}if(notice){const n=notice;notice=null;Promise.resolve(n.remove()).catch(()=>{});}}
 function message(text){if(disposed)return;close();const e=epoch;notice=WA.ui.displayActionMessage({message:text,callback:()=>{if(e===epoch&&!disposed)close();}});}
 function show(id,text,buttons=[]){if(disposed)return;close();const e=epoch;popup=WA.ui.openPopup('inside-popup-'+id,text,buttons.map(([label,fn])=>({label,callback:()=>{if(!disposed&&!busy&&e===epoch&&current===id)fn();}})).concat([{label:'Close',callback:()=>{if(e===epoch)close();}}]));}
 function update(){for(const [name,on]of [['house-key',state.key],['lens-focused',state.lens===1],['workshop-power',state.power],['lantern-lit',state.complete],['exterior-lit',state.complete]])WA.room[on?'showLayer':'hideLayer']('inside-'+name);}
 function journal(){message('KEEPER’S JOURNAL / '+(state.complete?'Beacon restored. Explore freely.':`Chart ${state.chart?'read':'unread'}; brass key ${state.key?'collected':'in house'}; fuse ${state.fuse?'installed':'not installed'}; power ${state.power?'on':'off'}; telescope ${state.bearing===2?'aligned':'unaligned'}; lens ${state.lens===1?'focused':'unfocused'}.` )+' Route: east house → northwest lighthouse workshop → upstairs lantern room. Read the chart, unlock the fuse, pump the generator, align instruments, send LOW–MIDDLE–HIGH. Doors and stairs keep your progress. Reload starts a new visit. Everything is silent.');}
 async function travel(destination){if(busy||disposed)return;busy=true;close();const ticket=++transitionId;const a=anchors[destination];try{await WA.player.teleport(a.x,a.y);if(disposed||ticket!==transitionId)return;busy=false;position({x:a.x,y:a.y});}catch(error){if(disposed||ticket!==transitionId)return;busy=false;current=null;try{const p=await WA.player.getPosition();if(!disposed&&ticket===transitionId)position(p);}catch(_){}message('The doorway did not complete its move. Your progress is safe. Try the nearby doorway again.');}}
 function mutate(fn){fn();update();visit(current);}
 function visit(id){if(!id||busy||disposed)return;
 const a=anchors[id];if(a.to){show(id,a.description,[[a.action||'Enter '+a.label,()=>travel(a.to)]]);return;}
 switch(id){
 case 'dock':show(id,'THE KEEPER’S RETURN\nEnter the east keeper’s house and northwest lighthouse. Explore real rooms and restore the beacon using the equipment inside. No timer; sound is off.',[['Open journal',journal]]);break;
 case 'chart':show(id,'THE KEEPER’S CHART\nA sketched ship sits northeast of the island. Margin notes: telescope bearing NORTHEAST, lens AMBER. Signal order: LOW, MIDDLE, HIGH.',[['Record chart',()=>mutate(()=>state.chart=true)]]);break;
 case 'key':show(id,state.key?'The brass key is already in your pocket.':'A brass fuse-cabinet key hangs inside the cupboard. The keeper’s spare fuse is in the lighthouse workshop.',state.key?[]:[['Take brass key',()=>mutate(()=>state.key=true)]]);break;
 case 'hearth':show(id,'The kettle is warm. The keeper’s log says: “A clear bearing, a steady lamp, then three notes home.” You can rest here and continue whenever you like.',[['Read journal',journal]]);break;
 case 'fuse':show(id,state.fuse?'The fresh fuse is firmly seated. Use the handwheel across the workshop.':state.key?'The brass key opens the cabinet. A spare fuse fits the empty socket.':'The fuse cabinet is locked. Look in the keeper’s house cupboard.',state.key&&!state.fuse?[['Install spare fuse',()=>mutate(()=>state.fuse=true)]]:[]);break;
 case 'wheel':show(id,state.power?'The generator hums silently in this visit. Power is steady; climb the stairs.':state.fuse?'The new fuse is ready. Turn the handwheel to charge the beacon.':'The generator cannot hold power until its fuse is replaced.',state.fuse&&!state.power?[['Turn handwheel',()=>mutate(()=>state.power=true)]]:[]);break;
 case 'telescope':show(id,`TELESCOPE\nCurrent bearing: ${['WEST','NORTH','NORTHEAST'][state.bearing]}. ${state.bearing===2?'The ship’s small pennant resolves in the glass.':'Only rolling water is visible.'}`,['WEST','NORTH','NORTHEAST'].map((v,i)=>[v,()=>mutate(()=>state.bearing=i)]));break;
 case 'lens':show(id,`FRESNEL LENS\nCurrent filter: ${['CLEAR','AMBER','BLUE'][state.lens]}. ${state.lens===1?'Warm amber gathers into one focused ray.':'The beam is diffuse.'}`,['CLEAR','AMBER','BLUE'].map((v,i)=>[v,()=>mutate(()=>state.lens=i)]));break;
 case 'console':
 if(state.complete){show(id,'SIGNAL RECEIVED\nThe ship replies with three flashes. The lighthouse is restored for your visit. Walk outside to see its warm lantern, or keep exploring.',[['Open journal',journal]]);break;}
 if(!state.power||state.bearing!==2||state.lens!==1){show(id,'TRANSMITTER\n'+(!state.power?'Power is off. Replace the workshop fuse and turn the handwheel. ': '')+(state.bearing!==2?'Align the telescope to the chart’s bearing. ':'')+(state.lens!==1?'Select the chart’s lens filter.':''),[['Open journal',journal]]);break;}
 show(id,`TRANSMIT / ${state.signal.length}/3\nSend the keeper’s three notes. A wrong note clears only the sequence.`,['LOW','MIDDLE','HIGH'].map(v=>[v,()=>{if(v!==['LOW','MIDDLE','HIGH'][state.signal.length]){state.signal=[];show(id,'The signal scattered. Equipment and inventory are safe. Try LOW, then MIDDLE, then HIGH.',[['Try again',()=>visit(id)]]);}else mutate(()=>{state.signal.push(v);if(state.signal.length===3)state.complete=true;});}]));break;
 default:show(id,'A quiet place to explore.',[['Open journal',journal]]);
 }
 }
 function position(p){if(disposed||busy)return;moveCount++;const next=Object.keys(anchors).find(k=>Math.hypot(p.x-anchors[k].x,p.y-anchors[k].y)<=anchors[k].radius)||null;if(next===current)return;close();current=next;if(next)visit(next);}
 async function init(){await WA.onInit();if(disposed)return;update();menus=[WA.ui.registerMenuCommand('Keeper’s journal',journal),WA.ui.registerMenuCommand('Inspect nearby',()=>current?visit(current):message('Walk to a brass floor inlay beside a doorway or instrument. Tap/right-click the floor to walk there, then choose its popup button.'))];moveSub=WA.player.onPlayerMove(position);const n=moveCount;const p=await WA.player.getPosition();if(!disposed&&moveCount===n&&!busy)position(p);}
 function dispose(){if(disposed)return;disposed=true;transitionId++;close();moveSub?.unsubscribe();menus.forEach(m=>m.remove());menus=[];}
 return{init,dispose,position,snapshot:()=>({...state,signal:[...state.signal],current,busy})};
}
if(typeof module!=='undefined'&&module.exports)module.exports={createExperience,layout:root.IslandLayout};
if(root.WA){const e=createExperience(root.WA,root.IslandLayout);root.addEventListener('pagehide',()=>e.dispose(),{once:true});e.init().catch(error=>console.error('Keeper visit could not initialize:',error));}
})(typeof globalThis!=='undefined'?globalThis:this);
