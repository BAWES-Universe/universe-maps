/* Original map-only controls using existing Universe APIs. No engine changes or destination URLs. */
(async () => {
 await WA.onInit();
 const rooms=ROOM_CONTRACTS, doors=DOOR_CONTRACTS;
 let position=await WA.player.getPosition();
 for(const room of rooms){
  const [x,y,w,h]=room.bounds;
  const apply=inside=>inside?WA.room.hideLayer(room.cover):WA.room.showLayer(room.cover);
  apply(position.x>=x&&position.x<x+w&&position.y>=y&&position.y<y+h);
  WA.room.onEnterLayer(room.layer).subscribe(()=>apply(true));
  WA.room.onLeaveLayer(room.layer).subscribe(()=>apply(false));
 }
 let lockState=WA.state.loadVariable('bawesMeetingLocked');
 let locked=!!(lockState&&lockState.locked&&lockState.expiresAt>Date.now());
 const userId=WA.player.uuid||WA.player.id;
 let actionLabel='',canExitMeeting=false;
 const doorVisibility=new Map();
 function update(){
  const p=position;
  // Inside occupants retain safe exit while a shared lock prevents outside entry.
  const insideMeeting=p.x>=352&&p.x<608&&p.y>=1408&&p.y<1600;
  if(insideMeeting)canExitMeeting=true;
  if(p.x>=672||p.y<1408||p.y>=1600)canExitMeeting=false;
  const insideTower=p.x>=352&&p.x<1056&&p.y>=1056&&p.y<1600;
  for(const door of doors){
   const [tx,ty,tw,th]=door.box,x=tx*32,y=ty*32,w=tw*32,h=th*32;
   const near=p.x>=x-64&&p.x<x+w+64&&p.y>=y-64&&p.y<y+h+64;
   const open=door.lockedVariable ? (canExitMeeting||(!locked&&near)) : (insideTower||near);
   if(doorVisibility.get(door.name)!==open){
    open?WA.room.hideLayer(door.name):WA.room.showLayer(door.name);
    doorVisibility.set(door.name,open);
   }
  }
  const ownerOutside=locked&&lockState.owner===userId&&p.x>=640&&p.x<736;
  const atControl=(insideMeeting&&p.x>=544&&p.x<608||ownerOutside)&&p.y>=1472&&p.y<1568;
  const label=atControl?(locked?'Unlock meeting door':'Lock meeting door'):'';
  if(label!==actionLabel){
   WA.ui.actionBar.removeButton('bawes-meeting-lock');actionLabel=label;
   if(label)WA.ui.actionBar.addButton({id:'bawes-meeting-lock',label,toolTip:label,location:'appsMenu',callback:async()=>{
    await WA.state.saveVariable('bawesMeetingLocked',{locked:!locked,owner:locked?null:userId,expiresAt:locked?0:Date.now()+15*60*1000});
   }});
  }
 }
 WA.state.onVariableChange('bawesMeetingLocked').subscribe(value=>{lockState=value;locked=!!(value&&value.locked&&value.expiresAt>Date.now());update()});
 setInterval(()=>{const active=!!(lockState&&lockState.locked&&lockState.expiresAt>Date.now());if(active!==locked){locked=active;update()}},1000);
 WA.player.onPlayerMove(event=>{position={x:event.x,y:event.y};update()});
 update();
})().catch(error=>console.error('Campus initialization failed',error));
