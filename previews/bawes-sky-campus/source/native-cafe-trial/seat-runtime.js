/* Candidate-local seat approach, using public map movement events and moveTo only. */
(async()=>{
 await WA.onInit();
 const seats=__SEATS_JSON__;
 const candidates=seats.filter(s=>['audience','cafe-bar','conservatory-lounge','cafe-lounge','cafe-armchair'].includes(s.group));
 let busy=false,lastSeat=null,pending=null;
 WA.player.onPlayerMove(event=>{
  if(busy)return;
  if(event.moving){clearTimeout(pending);if(lastSeat&&Math.hypot(event.x-lastSeat.x,event.y-lastSeat.y)>24)lastSeat=null;return;}
  const seat=candidates.find(s=>Math.hypot(event.x-s.x,event.y-s.y)<(s.group==='cafe-armchair'?20:12));
  if(!seat||seat===lastSeat)return;
  lastSeat=seat;
  if(event.direction===seat.facing)return;
  pending=setTimeout(async()=>{
   busy=true;
   try{
    const [dx,dy]=({up:[0,16],down:[0,-16],right:[-32,0],left:[32,0]})[seat.facing];
    const approach=await WA.player.moveTo(seat.x+dx,seat.y+dy);
    if(!approach.cancelled)await WA.player.moveTo(seat.x,seat.y);
   }catch(error){console.warn('Seat approach unavailable',error)}finally{busy=false;}
  },120);
 });
})().catch(error=>console.error('Seat alignment initialization failed',error));
