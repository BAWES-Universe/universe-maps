/* Map-local cutaways and proximity doors. No navigation prompts, audio or destinations. */
(async () => {
 await WA.onInit();
 const layout={"office":[2944,2448,2144,592],"cutaway":[2944,2448,2144,592],"doors":[{"id":"meeting-1","box":[4432,2896,96,16],"inside":[4352,2560,272,336],"lock":"meetingLock1"},{"id":"meeting-2","box":[4832,2896,96,16],"inside":[4752,2560,272,336],"lock":"meetingLock2"},{"id":"office-front","box":[3920,3024,192,16],"inside":[2960,2496,2112,528]}]};
 let position=await WA.player.getPosition(),moving=false;
 const states=new Map(),visibility=new Map(),egress=new Set();
 const contains=(p,b,pad=0)=>p.x>=b[0]-pad&&p.x<b[0]+b[2]+pad&&p.y>=b[1]-pad&&p.y<b[1]+b[3]+pad;
 const show=(name,visible)=>{if(visibility.get(name)!==visible){visible?WA.room.showLayer(name):WA.room.hideLayer(name);visibility.set(name,visible)}};
 let entranceOpen=false,entranceSequence=0;
 const reduced=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 function animateEntrance(open){
  if(open===entranceOpen)return;
  entranceOpen=open;const token=++entranceSequence;
  const frames=open?[1,2,3,4]:[3,2,1,0];
  const paint=frame=>{if(frame===0&&!open)show('office-front-door',true);show('office-front-leaves',frame===0);for(let i=1;i<4;i++)show('office-front-slide-'+i,frame===i)};
  if(reduced()){paint(open?4:0);return;}
  let index=0;const advance=()=>{if(token!==entranceSequence)return;paint(frames[index++]);if(index<frames.length)setTimeout(advance,180)};advance();
 }
 function update(){
  // This pinned client replans active paths whenever any layer visibility changes.
  // Apply cutaways and door closing at rest to avoid shifting 16px-grid click targets.
  if(!moving){
   const inside=contains(position,layout.cutaway);
   show('office-cover',!inside);show('office-window-interior',!inside);
   for(const layer of ['office-floor','office-walls','office-furniture','office-chair-fronts','office-glazing'])show(layer,inside);
  }
  for(const door of layout.doors){
   // Exit remains available to an occupant even when another client has locked the room.
   if(contains(position,door.inside))egress.add(door.id);
   if(!contains(position,door.inside,80))egress.delete(door.id);
   const state=states.get(door.lock),locked=!!(state?.locked&&state.expiresAt>Date.now());
   const near=contains(position,door.box,door.id==='office-front'&&!contains(position,layout.cutaway)?64:80);
   const open=door.lock ? (contains(position,door.inside)||near&&(!locked||egress.has(door.id))) : contains(position,door.inside)||near;
   // Exterior approach settles before gate layers change, avoiding path-target drift.
   if(door.id==='office-front'&&moving&&!contains(position,layout.cutaway))continue;
   if(open||!moving){if(door.id==='office-front'){if(open)show('office-front-door',false);animateEntrance(open)}else {show(door.id+'-door',!open);show(door.id+'-glass',!open&&contains(position,layout.cutaway));}}
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

/* Candidate-local seat approach, using public map movement events and moveTo only. */
(async()=>{
 await WA.onInit();
 const seats=[{"x": 3080, "y": 2656, "group": "focus", "facing": "up"}, {"x": 3512, "y": 2656, "group": "focus", "facing": "up"}, {"x": 3240, "y": 2624, "group": "project", "facing": "down"}, {"x": 3240, "y": 2768, "group": "project", "facing": "up"}, {"x": 3320, "y": 2624, "group": "project", "facing": "down"}, {"x": 3320, "y": 2768, "group": "project", "facing": "up"}, {"x": 3080, "y": 2896, "group": "outward-lounge", "facing": "down"}, {"x": 3128, "y": 2896, "group": "outward-lounge", "facing": "down"}, {"x": 3432, "y": 2896, "group": "outward-lounge", "facing": "down"}, {"x": 3480, "y": 2896, "group": "outward-lounge", "facing": "down"}, {"x": 3800, "y": 2640, "group": "reception", "facing": "down"}, {"x": 4456, "y": 2640, "group": "meeting", "facing": "down"}, {"x": 4456, "y": 2768, "group": "meeting", "facing": "up"}, {"x": 4536, "y": 2640, "group": "meeting", "facing": "down"}, {"x": 4536, "y": 2768, "group": "meeting", "facing": "up"}, {"x": 4856, "y": 2640, "group": "meeting", "facing": "down"}, {"x": 4856, "y": 2768, "group": "meeting", "facing": "up"}, {"x": 4936, "y": 2640, "group": "meeting", "facing": "down"}, {"x": 4936, "y": 2768, "group": "meeting", "facing": "up"}, {"x": 5528, "y": 3168, "group": "audience", "facing": "up"}, {"x": 5592, "y": 3168, "group": "audience", "facing": "up"}, {"x": 5656, "y": 3168, "group": "audience", "facing": "up"}, {"x": 5720, "y": 3168, "group": "audience", "facing": "up"}, {"x": 5528, "y": 3232, "group": "audience", "facing": "up"}, {"x": 5592, "y": 3232, "group": "audience", "facing": "up"}, {"x": 5656, "y": 3232, "group": "audience", "facing": "up"}, {"x": 5720, "y": 3232, "group": "audience", "facing": "up"}, {"x": 5528, "y": 3296, "group": "audience", "facing": "up"}, {"x": 5592, "y": 3296, "group": "audience", "facing": "up"}, {"x": 5656, "y": 3296, "group": "audience", "facing": "up"}, {"x": 5720, "y": 3296, "group": "audience", "facing": "up"}, {"x": 5528, "y": 3360, "group": "audience", "facing": "up"}, {"x": 5592, "y": 3360, "group": "audience", "facing": "up"}, {"x": 5656, "y": 3360, "group": "audience", "facing": "up"}, {"x": 5720, "y": 3360, "group": "audience", "facing": "up"}, {"x": 5880, "y": 3168, "group": "audience", "facing": "up"}, {"x": 5944, "y": 3168, "group": "audience", "facing": "up"}, {"x": 6008, "y": 3168, "group": "audience", "facing": "up"}, {"x": 6072, "y": 3168, "group": "audience", "facing": "up"}, {"x": 5880, "y": 3232, "group": "audience", "facing": "up"}, {"x": 5944, "y": 3232, "group": "audience", "facing": "up"}, {"x": 6008, "y": 3232, "group": "audience", "facing": "up"}, {"x": 6072, "y": 3232, "group": "audience", "facing": "up"}, {"x": 5880, "y": 3296, "group": "audience", "facing": "up"}, {"x": 5944, "y": 3296, "group": "audience", "facing": "up"}, {"x": 6008, "y": 3296, "group": "audience", "facing": "up"}, {"x": 6072, "y": 3296, "group": "audience", "facing": "up"}, {"x": 5880, "y": 3360, "group": "audience", "facing": "up"}, {"x": 5944, "y": 3360, "group": "audience", "facing": "up"}, {"x": 6008, "y": 3360, "group": "audience", "facing": "up"}, {"x": 6072, "y": 3360, "group": "audience", "facing": "up"}, {"x": 2392, "y": 4320, "group": "cafe-lounge", "facing": "down"}, {"x": 2424, "y": 4320, "group": "cafe-lounge", "facing": "down"}, {"x": 3000, "y": 4320, "group": "cafe-lounge", "facing": "down"}, {"x": 3032, "y": 4320, "group": "cafe-lounge", "facing": "down"}, {"x": 2360, "y": 4352, "group": "cafe-armchair", "facing": "right"}, {"x": 3064, "y": 4352, "group": "cafe-armchair", "facing": "left"}, {"x": 2568, "y": 4208, "group": "cafe-bar", "facing": "up"}, {"x": 2664, "y": 4208, "group": "cafe-bar", "facing": "up"}, {"x": 2776, "y": 4208, "group": "cafe-bar", "facing": "up"}, {"x": 2872, "y": 4208, "group": "cafe-bar", "facing": "up"}, {"x": 2328, "y": 2896, "group": "greenhouse", "facing": "down"}, {"x": 2584, "y": 2896, "group": "greenhouse", "facing": "down"}, {"x": 2120, "y": 3232, "group": "conservatory-lounge", "facing": "down"}, {"x": 2152, "y": 3232, "group": "conservatory-lounge", "facing": "down"}, {"x": 3544, "y": 3168, "group": "outdoor-lounge", "facing": "down"}, {"x": 3592, "y": 3168, "group": "outdoor-lounge", "facing": "down"}, {"x": 4376, "y": 3168, "group": "outdoor-lounge", "facing": "down"}, {"x": 4424, "y": 3168, "group": "outdoor-lounge", "facing": "down"}, {"x": 5160, "y": 4240, "group": "outdoor-lounge", "facing": "down"}, {"x": 5208, "y": 4240, "group": "outdoor-lounge", "facing": "down"}];
 const candidates=seats;
 let busy=false,lastSeat=null,pending=null;
 WA.player.onPlayerMove(event=>{
  if(busy)return;
  if(event.moving){clearTimeout(pending);if(lastSeat&&Math.hypot(event.x-lastSeat.x,event.y-lastSeat.y)>24)lastSeat=null;return;}
  const seat=candidates.find(s=>Math.hypot(event.x-s.x,event.y-s.y)<(s.group==='cafe-armchair'?20:12));
  if(!seat||seat===lastSeat)return;
  if(event.direction===seat.facing){lastSeat=seat;return;}
  pending=setTimeout(async()=>{
   busy=true;
   try{
    const [dx,dy]=({up:[0,16],down:[0,-16],right:[-32,0],left:[32,0]})[seat.facing];
    const approach=await WA.player.moveTo(seat.x+dx,seat.y+dy);
    if(!approach.cancelled){
     const arrival=await WA.player.moveTo(seat.x,seat.y);
     if(!arrival.cancelled)lastSeat=seat;
    }
   }catch(error){console.warn('Seat approach unavailable',error)}finally{busy=false;}
  },120);
 });
})().catch(error=>console.error('Seat alignment initialization failed',error));

/* A local roof cutaway for the greenhouse reading room. */
(async()=>{
 await WA.onInit();
 let visible=false;
 function update(p){
  if(p.moving)return;
  const inside=p.x>=2208&&p.x<2656&&p.y>=2880&&p.y<3120;
  if(inside===visible)return;
  visible=inside;
  for(const name of ['greenhouse-interior','greenhouse-chair-fronts']){
   inside?WA.room.showLayer(name):WA.room.hideLayer(name);
  }
 }
 update(await WA.player.getPosition());WA.player.onPlayerMove(update);
})().catch(error=>console.error('Greenhouse initialization failed',error));
