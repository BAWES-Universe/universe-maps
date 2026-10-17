/* Map-local cutaways and proximity doors. No navigation prompts, audio or destinations. */
(async () => {
 await WA.onInit();
 const layout={"office":[2896,1664,2240,1440],"cutaway":[2768,1536,2496,1568],"doors":[{"id":"meeting-1","box":[4272,2448,16,96],"inside":[4288,2416,240,160],"lock":"meetingLock1"},{"id":"meeting-2","box":[4656,2448,16,96],"inside":[4672,2416,240,160],"lock":"meetingLock2"},{"id":"meeting-3","box":[4272,2736,16,96],"inside":[4288,2704,240,160],"lock":"meetingLock3"},{"id":"meeting-4","box":[4656,2736,16,96],"inside":[4672,2704,240,160],"lock":"meetingLock4"},{"id":"office-front","box":[3920,3088,192,16],"inside":[2912,1680,2208,1408]},{"id":"office-rear","box":[3920,1664,192,16],"inside":[2912,1680,2208,1408]}]};
 let position=await WA.player.getPosition(),moving=false;
 const states=new Map(),visibility=new Map(),egress=new Set();
 const contains=(p,b,pad=0)=>p.x>=b[0]-pad&&p.x<b[0]+b[2]+pad&&p.y>=b[1]-pad&&p.y<b[1]+b[3]+pad;
 const show=(name,visible)=>{if(visibility.get(name)!==visible){visible?WA.room.showLayer(name):WA.room.hideLayer(name);visibility.set(name,visible)}};
 function update(){
  // This pinned client replans active paths whenever any layer visibility changes.
  // Apply cutaways and door closing at rest to avoid shifting 16px-grid click targets.
  if(!moving){
   const inside=contains(position,layout.cutaway);
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
   if(open||!moving)show(door.id+'-door',!open);
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
