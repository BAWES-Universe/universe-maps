/* H009: explicit four-beat cam choreography, private temporary performance preset. */
(function(root){
'use strict';
const TREES=['petal','leaf','fruit'],CAMS=['eccentric','heart','snail'];
const PROGRAMS={eccentric:[2,1,0,1],heart:[0,1,2,1],snail:[2,2,1,0]};
const LAYERS=TREES.flatMap(t=>[t+'-phase-1',t+'-phase-2']);
const clone=v=>JSON.parse(JSON.stringify(v));
function fresh(){return{draft:{petal:'eccentric',leaf:'heart',fruit:'snail'},performance:null,beat:-1,completed:false,preset:null,runs:0,last:null};}
function advance(state,action){
 const next=clone(state),refuse=message=>({ok:false,next:clone(state),message});
 if(!action||typeof action!=='object')throw Error('Action object required');
 switch(action.type){
 case 'cam':if(!TREES.includes(action.tree)||!CAMS.includes(action.cam))throw Error('Unknown cam');next.draft[action.tree]=action.cam;break;
 case 'start':next.performance=clone(state.draft);next.beat=0;next.completed=false;break;
 case 'step':if(!state.performance)return refuse('Choose Begin performance before advancing the hand-driven beat.');if(state.beat>=3)return refuse('Four beats are complete. Save this performance or Begin performance to replay.');next.beat++;if(next.beat===3){next.completed=true;next.runs++;}break;
 case 'save':if(!state.completed||!state.performance)return refuse('Complete all four explicit beats before saving a temporary performance preset.');next.preset=clone(state.performance);break;
 case 'load':if(!state.preset)return refuse('No temporary preset is saved in this visit.');next.draft=clone(state.preset);break;
 default:throw Error('Unknown orchard action');
 }
 next.last=null;return{ok:true,next,message:'Orchard updated.'};
}
function phases(state){return state.performance?Object.fromEntries(TREES.map(t=>[t,PROGRAMS[state.performance[t]][state.beat]])):{petal:0,leaf:0,fruit:0};}
function visible(state){const p=phases(state);return TREES.filter(t=>p[t]!==0).map(t=>t+'-phase-'+p[t]);}
function createExperience(WA,layout){
 const anchors=layout.anchors;
 let state=fresh(),current=null,popup=null,notice=null,epoch=0,disposed=false,busy=false,transition=0,moveCount=0,lastPosition=null,started=false,moveSub,menus=[],moving=null;
 const shown=Object.fromEntries(LAYERS.map(n=>[n,false]));
 function close(){epoch++;if(popup){popup.close();popup=null;}if(notice){const old=notice;notice=null;Promise.resolve(old.remove()).catch(()=>{});}}
 function message(text){if(disposed)return;close();const ticket=epoch;notice=WA.ui.displayActionMessage({message:text,callback:()=>{if(!disposed&&ticket===epoch)close();}});}
 function show(id,text,buttons=[]){if(disposed||busy)return;close();const ticket=epoch;popup=WA.ui.openPopup('popup-'+id,text,buttons.map(([label,fn])=>({label,callback:()=>{if(!disposed&&!busy&&current===id&&ticket===epoch)fn();}})).concat([{label:'Close',callback:()=>{if(ticket===epoch)close();}}]));}
 function update(){if(disposed||busy||moving!==false)return;const wanted=visible(state);for(const n of LAYERS){const on=wanted.includes(n);if(shown[n]!==on){WA.room[on?'showLayer':'hideLayer'](n);shown[n]=on;}}}
 function summary(){const p=phases(state),word=['open / all lit','alternating','closed / unlit'];return 'Draft cams: '+TREES.map(t=>t+' '+state.draft[t]).join(', ')+'. '+(state.performance?'Performance beat '+(state.beat+1)+' of 4: '+TREES.map(t=>t+' '+word[p[t]]).join('; ')+'. ':'No performance begun. ')+(state.completed?'Performance complete. ':'')+'Temporary preset: '+(state.preset?TREES.map(t=>t+' '+state.preset[t]).join(', '):'none')+'.'+(state.last?' '+state.last:'');}
 function journal(){message('MECHANICAL ORCHARD / '+summary()+' Each of three tree sculptures has its own cam. ECCENTRIC: closed, alternating, open, alternating. HEART: open, alternating, closed, alternating. SNAIL: closed, closed, alternating, open. Begin performance snapshots the draft cams. Advance one beat explicitly to inspect each untimed pose; there is no automatic playback or sound. The petal vanes fold, leaves turn, and fruit lamps visibly switch. Editing draft cams never rewrites the running performance. After beat four, Save temporary preset copies that completed performance; Load preset changes draft cams only. Presets exist only for this visitor until full reload or confirmed reset. Cam-house doors and Close preserve everything. The two branch benches are contact locations with normal native standing frames, not automatic sitting.');}
 function mutate(action){const r=advance(state,action);state=r.next;if(!r.ok)state.last=r.message;update();visit(current);}
 function reset(){state=fresh();update();visit(current);}
 async function travel(to){
  if(disposed||busy)return;busy=true;close();const token=++transition,a=anchors[to],nativeMoveAtStart=moveCount,uiAtStart=epoch;
  try{await WA.player.teleport(a.x,a.y);if(disposed||token!==transition)return;busy=false;update();
   const observed=moveCount>nativeMoveAtStart&&lastPosition?lastPosition:{x:a.x,y:a.y};
   position(observed,epoch===uiAtStart);
  }catch(error){if(disposed||token!==transition)return;busy=false;update();
   if(moveCount>nativeMoveAtStart&&lastPosition){position(lastPosition,epoch===uiAtStart);return;}
   const count=moveCount;let recovered=null;try{recovered=await WA.player.getPosition();}catch(_){}
   if(!disposed&&token===transition&&moveCount===count){const announce=epoch===uiAtStart;if(recovered)position(recovered,announce);if(announce)message('The doorway could not complete the move. Your cam choices, current beat and local preset are safe. Walk back to the door or choose Inspect nearby to retry.');}
  }
 }
 function visit(id){if(!id||busy||disposed)return;const a=anchors[id];if(a.to){show(id,id==='houseDoor'?'The cam house contains three replaceable cam mechanisms and the temporary preset desk.':'Return to the three kinetic tree sculptures. Cam choices, performance beat and local preset are preserved.',[[a.action,()=>travel(a.to)]]);return;}
 const act=(label,action)=>[label,()=>mutate(action)];
 if(TREES.includes(a.kind)){const tree=a.kind;show(id,tree.toUpperCase()+' CAM / '+summary()+' Choose a cam for this tree. The draft can change while an earlier performance remains on display.',CAMS.map(cam=>act('Fit '+cam,{type:'cam',tree,cam})).concat([['Orchard notes',journal]]));return;}
 switch(id){
 case 'arrival':show(id,'MECHANICAL ORCHARD / Walk the broad loops around three living-looking machines. Use a crank or enter the cam house to choose three cams. The south viewing station stages an untimed four-beat performance.',[['Orchard notes',journal]]);break;
 case 'performance':show(id,'VIEWING PLATFORM / '+summary()+' Begin snapshots the three draft cams. Advance beat moves each sculpture to its next pose.',[act('Begin performance',{type:'start'}),act('Advance beat',{type:'step'}),act('Save temporary preset',{type:'save'}),['Orchard notes',journal]]);break;
 case 'presetDesk':show(id,'CAM-HOUSE PRESET DESK / '+summary()+' Saving requires the complete fourth beat. Loading restores draft cams only. This is a private temporary visit preset, cleared by full reload.',[act('Save temporary preset',{type:'save'}),act('Load preset into draft',{type:'load'}),['Orchard notes',journal],['Reset this visit',()=>show('presetDesk','Clear all cam choices, visible performance, completed count and temporary preset?',[['Confirm reset',reset]])]]);break;
 }
 }
 function position(p,announce=true){if(disposed)return;lastPosition={x:p.x,y:p.y,moving:p.moving};moveCount++;if(typeof p.moving==='boolean'){moving=p.moving;if(!moving)update();}if(busy)return;const next=Object.keys(anchors).filter(k=>anchors[k].kind!=='route').find(k=>Math.hypot(p.x-anchors[k].x,p.y-anchors[k].y)<=anchors[k].radius)||null;if(next===current)return;if(announce)close();current=next;if(next&&announce)visit(next);}
 async function init(){if(started||disposed)return;started=true;await WA.onInit();if(disposed)return;update();menus=[WA.ui.registerMenuCommand('Orchard notes',journal),WA.ui.registerMenuCommand('Inspect nearby',()=>current?visit(current):message('Walk beside a tree crank, cam mechanism, performance station or open cam-house doorway. Touch/right-click clear floor to move. All clues work silently.'))];moveSub=WA.player.onPlayerMove(position);const n=moveCount,uiEpoch=epoch;const p=await WA.player.getPosition();if(!disposed&&!busy&&moveCount===n)position(p,epoch===uiEpoch);}
 function dispose(){if(disposed)return;disposed=true;transition++;close();moveSub?.unsubscribe();menus.forEach(m=>m.remove());menus=[];}
 return{init,dispose,position,snapshot:()=>({...clone(state),current,busy,moving})};
}
if(typeof module!=='undefined'&&module.exports)module.exports={createExperience,advance,fresh,visible,phases,LAYERS,CAMS,TREES,PROGRAMS};
if(root.WA){const e=createExperience(root.WA,root.MechanicalOrchardLayout);root.addEventListener('pagehide',()=>e.dispose(),{once:true});e.init().catch(error=>console.error('Mechanical orchard could not initialize:',error));}
})(typeof globalThis!=='undefined'?globalThis:this);
