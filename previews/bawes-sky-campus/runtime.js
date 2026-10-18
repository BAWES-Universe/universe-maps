/* Map-local cutaways and proximity doors. No navigation prompts, audio or destinations. */
(async () => {
 await WA.onInit();
 const layout={"office":[2944,2448,2144,592],"cutaway":[2944,2448,2144,592],"doors":[{"id":"meeting-1","box":[4320,2816,16,96],"inside":[4336,2784,288,160],"lock":"meetingLock1"},{"id":"meeting-2","box":[4704,2816,16,96],"inside":[4720,2784,288,160],"lock":"meetingLock2"},{"id":"office-front","box":[3920,3024,192,16],"inside":[2960,2528,2112,496]}]};
 let position=await WA.player.getPosition(),moving=false;
 const states=new Map(),visibility=new Map(),egress=new Set();
 const contains=(p,b,pad=0)=>p.x>=b[0]-pad&&p.x<b[0]+b[2]+pad&&p.y>=b[1]-pad&&p.y<b[1]+b[3]+pad;
 const show=(name,visible)=>{if(visibility.get(name)!==visible){visible?WA.room.showLayer(name):WA.room.hideLayer(name);visibility.set(name,visible)}};
 let entranceOpen=false,entranceSequence=0,steamUntil=0,steamFrame=0,beveragePrompt;
 const reduced=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const steamOff=()=>{for(let i=0;i<3;i++)show('beverage-steam-'+i,false)};
 const nearBeverage=()=>contains(position,[layout.office[0]+1168,layout.office[1]+256,176,144]);
 function animateEntrance(open){
  if(open===entranceOpen)return;
  entranceOpen=open;const token=++entranceSequence;
  const frames=open?[1,2,3,4]:[3,2,1,0];
  const paint=frame=>{if(frame===0&&!open)show('office-front-door',true);show('office-front-leaves',frame===0);for(let i=1;i<4;i++)show('office-front-slide-'+i,frame===i)};
  if(reduced()){paint(open?4:0);return;}
  let index=0;const advance=()=>{if(token!==entranceSequence)return;paint(frames[index++]);if(index<frames.length)setTimeout(advance,180)};advance();
 }
 setInterval(()=>{
  const active=Date.now()<steamUntil&&!moving&&nearBeverage()&&!reduced();
  if(!active){steamOff();return;}
  steamFrame=(steamFrame+1)%3;
  for(let i=0;i<3;i++)show('beverage-steam-'+i,i===steamFrame);
 },220);
 function update(){
  // This pinned client replans active paths whenever any layer visibility changes.
  // Apply cutaways and door closing at rest to avoid shifting 16px-grid click targets.
  if(!moving){
   const inside=contains(position,layout.cutaway);
   if(inside&&nearBeverage()&&Date.now()>=steamUntil&&!beveragePrompt){beveragePrompt=WA.ui.displayActionMessage({message:'Brew a warm drink',callback:()=>{steamUntil=Date.now()+5000;beveragePrompt=undefined}})}
   if((!inside||!nearBeverage())&&beveragePrompt){beveragePrompt.remove();beveragePrompt=undefined}

   show('reception-activity',inside&&contains(position,[layout.office[0]+1120,layout.office[1]+384,208,176])&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches);
   show('office-cover',!inside);show('office-window-interior',!inside);
   for(const layer of ['office-floor','office-walls','office-furniture','office-chair-fronts'])show(layer,inside);
  }
  for(const door of layout.doors){
   // Exit remains available to an occupant even when another client has locked the room.
   if(contains(position,door.inside))egress.add(door.id);
   if(!contains(position,door.inside,80))egress.delete(door.id);
   const state=states.get(door.lock),locked=!!(state?.locked&&state.expiresAt>Date.now());
   const near=contains(position,door.box,80);
   const open=door.lock ? near&&(!locked||egress.has(door.id)) : contains(position,door.inside)||near;
   if(open||!moving){if(door.id==='office-front'){if(open)show('office-front-door',false);animateEntrance(open)}else show(door.id+'-door',!open);}
  }
 }
 const owner=WA.player.uuid||WA.player.id;
 for(const door of layout.doors.filter(d=>d.lock)){
  states.set(door.lock,WA.state.loadVariable(door.lock));
  WA.state.onVariableChange(door.lock).subscribe(value=>{states.set(door.lock,value);update()});
  WA.ui.actionBar.addButton({id:door.lock,label:'Meeting '+door.id.split('-')[1]+' lock',toolTip:'Toggle courtesy lock while inside or as lock owner; expires after 15 minutes',location:'appsMenu',callback:async()=>{
   const state=states.get(door.lock);
   if(!contains(position,door.inside)&&state?.owner!==owner)return;
   const locked=!!(state?.locked&&state.expiresAt>Date.now());
   await WA.state.saveVariable(door.lock,{locked:!locked,owner:locked?null:owner,expiresAt:locked?0:Date.now()+900000});
  }});
 }
 WA.player.onPlayerMove(event=>{position={x:event.x,y:event.y};moving=event.moving;update()});
 setInterval(update,1000);update();
})().catch(error=>console.error('Sky campus initialization failed',error));
