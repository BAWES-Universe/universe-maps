import {GARDEN,canStand,findPath,sweep,feet,toWorld} from '../garden-geometry.mjs';
import {createGardenAudio} from '../garden-audio.mjs';
const c=document.querySelector('#map'),ctx=c.getContext('2d'),status=document.querySelector('#status'),audioLabel=document.querySelector('#audio');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');let motion=!reduced.matches,debug=false,pos={...GARDEN.entry},row=0,frame=1,moving=false,seat=null,queue=[],done=null,last=0,walkClock=0,disposed=false;
const load=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src;});
const [base,foliage,foreground,water,fire,shade,shadow,greg]=await Promise.all(['../layers/garden-base.png','../layers/garden-foliage-foreground.png','../layers/garden-foreground.png','../layers/garden-water.png','../layers/garden-fire.png','../layers/garden-shade-mask.png','../layers/avatar-contact-shadow.png','./greg-gulf-woka-v3.png'].map(load));
const scratch=document.createElement('canvas');scratch.width=1024;scratch.height=1024;const sctx=scratch.getContext('2d');
const avatar=document.createElement('canvas');avatar.width=32;avatar.height=32;const actx=avatar.getContext('2d');
const audio=createGardenAudio({suspendMapSfxWhenHidden:true,onState:s=>{audioLabel.textContent=s.ready&&!s.muted?(s.gain>0?'Local crackle '+Math.round(s.gain/.06*100)+'%':'Outside sound range'):'Sound off';}});audio.setPosition(pos);
const setStatus=()=>{status.textContent=seat?`${seat[0].toUpperCase()+seat.slice(1)} bench spot · facing ${GARDEN.benches.find(b=>b.id===seat).facing}`:moving?'Walking through the garden':'Garden path';};
function resolveRoute(value){queue=[];moving=false;if(done){const f=done;done=null;f(value);}setStatus();}
function moveTo(target,{benchId=null}={}){resolveRoute(false);const path=findPath(pos,target,{benchId});if(!path)return Promise.resolve(false);queue=path.slice(1).map(p=>({...p,benchId}));moving=queue.length>0;setStatus();return new Promise(resolve=>{done=resolve;if(!moving)resolveRoute(true);});}
async function leaveSeat(){if(!seat)return true;const b=GARDEN.benches.find(b=>b.id===seat);seat=null;return moveTo(b.exit,{benchId:b.id});}
async function walkToBench(id){await leaveSeat();const b=GARDEN.benches.find(b=>b.id===id);if(!b)return false;if(!await moveTo(b.approach))return false;if(!await moveTo(b.seat,{benchId:b.id}))return false;seat=b.id;row=b.spriteRow;frame=1;setStatus();return true;}
async function walkTo(target){await leaveSeat();return moveTo(target);}
function nearestBench(){return [...GARDEN.benches].sort((a,b)=>Math.hypot(pos.x-a.approach.x,pos.y-a.approach.y)-Math.hypot(pos.x-b.approach.x,pos.y-b.approach.y))[0];}
for(const button of document.querySelectorAll('[data-bench]'))button.onclick=()=>walkToBench(button.dataset.bench);
c.addEventListener('pointerdown',e=>{const r=c.getBoundingClientRect(),p={x:(e.clientX-r.left)*1024/r.width,y:(e.clientY-r.top)*1024/r.height-16};c.focus();walkTo(p);});
const keys=new Set();addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d','e','E'].includes(e.key))e.preventDefault();if(e.key.toLowerCase()==='e'){if(seat)void leaveSeat();else{const b=nearestBench();if(Math.hypot(pos.x-b.approach.x,pos.y-b.approach.y)<72)void walkToBench(b.id);}return;}keys.add(e.key.toLowerCase());});addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));addEventListener('blur',()=>keys.clear());
document.querySelector('#zoom').onclick=e=>{document.body.classList.toggle('native');e.target.textContent=document.body.classList.contains('native')?'Fit view':'Native 1×';};
document.querySelector('#debug').onclick=e=>{debug=!debug;e.target.setAttribute('aria-pressed',debug);};
const motionButton=document.querySelector('#motion');function motionUI(){motionButton.textContent=motion?'Motion on':'Motion off';motionButton.setAttribute('aria-pressed',!motion);}motionButton.onclick=()=>{motion=!motion;motionUI();};reduced.addEventListener('change',e=>{motion=!e.matches;motionUI();});motionUI();
document.querySelector('#sound').onclick=async e=>{try{if(!audio.snapshot().ready){audio.setMuted(false);await audio.start();}else audio.setMuted(!audio.snapshot().muted);e.target.textContent=audio.snapshot().muted?'Enable crackle':'Mute crackle';}catch(err){audio.setMuted(true);audioLabel.textContent='Sound could not start';console.error(err);}};
function face(dx,dy){if(Math.abs(dx)>Math.abs(dy))row=dx>0?2:1;else if(dy)row=dy>0?0:3;}
function update(dt){
 let dx=(keys.has('d')||keys.has('arrowright')?1:0)-(keys.has('a')||keys.has('arrowleft')?1:0),dy=(keys.has('s')||keys.has('arrowdown')?1:0)-(keys.has('w')||keys.has('arrowup')?1:0);
 if((dx||dy)&&!seat){resolveRoute(false);const l=Math.hypot(dx,dy),next={x:pos.x+dx/l*120*dt,y:pos.y+dy/l*120*dt};if(sweep(pos,next)){pos=next;moving=true;face(dx,dy);}}else if(queue.length){const q=queue[0],dx=q.x-pos.x,dy=q.y-pos.y,d=Math.hypot(dx,dy),step=130*dt;face(dx,dy);if(d<=step){pos={x:q.x,y:q.y};queue.shift();if(!queue.length)resolveRoute(true);}else{const next={x:pos.x+dx/d*step,y:pos.y+dy/d*step};if(sweep(pos,next,{benchId:q.benchId}))pos=next;else resolveRoute(false);}}
 else if(!dx&&!dy)moving=false;
 walkClock+=dt;frame=moving?Math.floor(walkClock*9)%3:1;audio.setPosition(pos);
}
function draw(t){ctx.clearRect(0,0,1024,1024);ctx.drawImage(base,0,0);
 if(motion){ctx.drawImage(water,0,Math.sin(t*.0009)*1.15);ctx.save();ctx.globalAlpha=.35+.12*Math.sin(t*.006);ctx.drawImage(fire,0,Math.sin(t*.009)*.7);ctx.restore();}
 const f=feet(pos);ctx.drawImage(shadow,Math.round(pos.x-16),Math.round(f.y-9));
 actx.clearRect(0,0,32,32);actx.imageSmoothingEnabled=false;actx.drawImage(greg,frame*32,row*32,32,32,0,0,32,32);
 // Runtime received warmth is clipped to opaque avatar pixels, never edits the Woka asset.
 const distance=Math.hypot(f.x-GARDEN.fire.x,f.y-GARDEN.fire.y),warm=Math.max(0,1-distance/200)*.075;
 if(warm){actx.globalCompositeOperation='source-atop';actx.fillStyle=`rgba(255,175,68,${warm})`;actx.fillRect(0,0,32,32);actx.globalCompositeOperation='source-over';}
 ctx.imageSmoothingEnabled=false;ctx.drawImage(avatar,Math.round(pos.x-16),Math.round(pos.y-16));ctx.imageSmoothingEnabled=true;
 ctx.drawImage(foliage,0,0);
 if(seat){const b=GARDEN.benches.find(b=>b.id===seat),box=b.occlusion;sctx.clearRect(0,0,1024,1024);sctx.drawImage(foreground,...box.slice(0,2),box[2]-box[0],box[3]-box[1],...box.slice(0,2),box[2]-box[0],box[3]-box[1]);
  // A seated-position Woka still uses its original standing frame. Preserve all head pixels.
  sctx.clearRect(Math.floor(pos.x-16),Math.floor(pos.y-16),32,19);ctx.drawImage(scratch,0,0);
 }
 if(debug){ctx.save();ctx.lineWidth=1;ctx.strokeStyle='#58e8e5';for(const poly of GARDEN.walkable){ctx.beginPath();poly.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.stroke();}ctx.strokeStyle='#ff668a';for(const o of GARDEN.obstacles){if(o.type==='rect')ctx.strokeRect(o.x,o.y,o.width,o.height);else{ctx.beginPath();ctx.arc(o.x,o.y,o.radius,0,Math.PI*2);ctx.stroke();}}ctx.fillStyle='#5cf09c99';ctx.fillRect(pos.x-8,pos.y,16,16);ctx.strokeStyle='#fff';ctx.strokeRect(pos.x-16,pos.y-16,32,32);ctx.restore();}
}
function tick(t){if(disposed)return;const dt=Math.min(.04,(t-last)/1000||0);last=t;update(dt);draw(t);requestAnimationFrame(tick);}requestAnimationFrame(tick);
window.gardenPreview={ready:true,GARDEN,walkTo,walkToBench,leaveSeat,getState:()=>({position:{...pos},worldPosition:toWorld(pos),feet:feet(pos),seat,row,frame,moving,queue:queue.length,motion,debug,audio:audio.snapshot()}),setPosition(p){if(!canStand(p))throw Error('Invalid path position');resolveRoute(false);seat=null;pos={...p};audio.setPosition(pos);},setMotion(v){motion=Boolean(v);motionUI();},setSuspended:v=>audio.setSuspended(v),audio,render:draw};
addEventListener('pagehide',()=>{disposed=true;audio.dispose();},{once:true});
