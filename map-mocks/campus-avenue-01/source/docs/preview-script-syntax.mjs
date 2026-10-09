
import { AVENUE, canStand, toWorld } from './avenue-geometry.mjs';
const canvas=document.querySelector('#scene'),ctx=canvas.getContext('2d');
const load=src=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=src});
const [base,fore,greg,mask]=await Promise.all(['./layers/avenue-base.png','./layers/avenue-foliage-foreground.png','./assets/greg-reference.png','./layers/avenue-walkable-mask.png'].map(load));
let p={...AVENUE.arrival},row=0,frame=1,keys=new Set,last=performance.now();
document.querySelector('#reset').onclick=()=>{p={...AVENUE.arrival};row=0;frame=1};
addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d'].includes(e.key)){keys.add(e.key);e.preventDefault()}});
addEventListener('keyup',e=>keys.delete(e.key));
addEventListener('blur',()=>keys.clear());
function draw(now){const dt=Math.min(.04,(now-last)/1000);last=now;let dx=0,dy=0;
if(keys.has('ArrowUp')||keys.has('w')){dy=-1;row=3}if(keys.has('ArrowDown')||keys.has('s')){dy=1;row=0}if(keys.has('ArrowLeft')||keys.has('a')){dx=-1;row=1}if(keys.has('ArrowRight')||keys.has('d')){dx=1;row=2}
const n=Math.hypot(dx,dy)||1,step=100*dt;
if(canStand({x:p.x+dx/n*step,y:p.y}))p.x+=dx/n*step;if(canStand({x:p.x,y:p.y+dy/n*step}))p.y+=dy/n*step;
frame=dx||dy?Math.floor(now/150)%3:1;ctx.clearRect(0,0,1472,576);ctx.drawImage(base,0,0);
if(document.querySelector('#mask').checked){ctx.save();ctx.globalAlpha=.33;ctx.drawImage(mask,0,0);ctx.restore()}
ctx.imageSmoothingEnabled=false;ctx.drawImage(greg,frame*32,row*32,32,32,Math.round(p.x)-16,Math.round(p.y)-16,32,32);ctx.drawImage(fore,0,0);
const w=toWorld(p);document.querySelector('#position').textContent=`World ${Math.round(w.x)}, ${Math.round(w.y)}`;requestAnimationFrame(draw)}requestAnimationFrame(draw);
