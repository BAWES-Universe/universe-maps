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
