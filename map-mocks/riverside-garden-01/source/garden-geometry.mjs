/** Native-pixel garden module. Avatar position is the CENTER of an unchanged 32×32 frame. */
export const GARDEN = Object.freeze({
 id:'magical-universe-riverside-garden',nativeSize:{width:1024,height:1024},tileSize:32,
 worldOrigin:{x:2176,y:1920},entry:{x:16,y:272},attachment:{x:0,y:288,width:96},
 avatar:{frame:{x:-16,y:-16,width:32,height:32},body:{x:-8,y:0,width:16,height:16},scale:1},
 fire:{x:492,y:520,radius:62,plannedCenter:{x:496,y:528}},
 walkable:[
  [[0,244],[180,244],[262,256],[408,240],[568,232],[654,236],[700,264],[720,300],[728,424],[720,708],[729,838],[792,960],[834,1024],[790,1024],[756,951],[683,858],[650,812],[650,714],[635,701],[590,717],[539,735],[451,735],[379,711],[322,676],[290,626],[274,566],[280,483],[295,418],[325,378],[304,354],[249,350],[208,348],[151,348],[125,338],[0,338]]
 ],
 obstacles:[
  {id:'fire-ring-and-flower-corners',type:'circle',x:492,y:520,radius:62},
  {id:'north-bench',type:'rect',x:417,y:362,width:148,height:56},
  {id:'south-bench',type:'rect',x:417,y:602,width:148,height:59},
  {id:'west-bench',type:'rect',x:344,y:453,width:56,height:126},
  {id:'east-bench',type:'rect',x:587,y:453,width:52,height:126},
  {id:'upper-west-planter',type:'circle',x:327,y:349,radius:25},
  {id:'upper-east-planter',type:'circle',x:625,y:320,radius:27},
  {id:'lower-east-planter',type:'circle',x:624,y:698,radius:26},
  {id:'river-path-planter',type:'circle',x:774,y:817,radius:22},
  {id:'low-left-court-flowers',type:'circle',x:348,y:672,radius:23}
 ],
 benches:[
  {id:'north',facing:'down',spriteRow:0,approach:{x:492,y:426},seat:{x:492,y:392},exit:{x:492,y:426},bodyPassage:{x:470,y:384,width:44,height:62},occlusion:[444,405,548,414]},
  {id:'south',facing:'up',spriteRow:3,approach:{x:492,y:584},seat:{x:492,y:623},exit:{x:492,y:584},bodyPassage:{x:470,y:584,width:44,height:68},occlusion:[443,636,548,651]},
  {id:'west',facing:'right',spriteRow:2,approach:{x:416,y:520},seat:{x:378,y:520},exit:{x:416,y:520},bodyPassage:{x:368,y:508,width:64,height:40},occlusion:[383,483,396,561]},
  {id:'east',facing:'left',spriteRow:1,approach:{x:568,y:520},seat:{x:606,y:520},exit:{x:568,y:520},bodyPassage:{x:558,y:508,width:65,height:40},occlusion:[589,483,602,561]}
 ],
 receivers:{west:{edge:'west',from:240,to:336,center:288,clearWidth:96},northRiver:{edge:'north',from:836,to:1024},southRiver:{edge:'south',from:874,to:1024},southPath:{edge:'south',from:790,to:834,status:'closed until host connects'}},
 quietZonesWorld:[{id:'StudentHub-all-teams',x:512,y:320,width:1984,height:1344},{id:'meeting-gallery',x:2560,y:768,width:384,height:832}],
 audio:{id:'riverside-fire',kind:'fire',url:'./audio/fire-gentle-original.mp3',center:{x:492,y:520},innerRadius:160,outerRadius:384,maxGain:.06,bounds:{x:80,y:136,width:796,height:784},edgeFade:48}
});
export const toWorld=p=>({x:p.x+GARDEN.worldOrigin.x,y:p.y+GARDEN.worldOrigin.y});
export const fromWorld=p=>({x:p.x-GARDEN.worldOrigin.x,y:p.y-GARDEN.worldOrigin.y});
export const feet=p=>({x:p.x,y:p.y+16});
export function inPoly(p,poly){let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if(((a[1]>p.y)!==(b[1]>p.y))&&(p.x<(b[0]-a[0])*(p.y-a[1])/(b[1]-a[1])+a[0]))c=!c;}return c;}
export function inRect(p,r){return p.x>=r.x&&p.x<r.x+r.width&&p.y>=r.y&&p.y<r.y+r.height;}
function hitsObstacle(p,o){return o.type==='circle'?Math.hypot(p.x-o.x,p.y-o.y)<=o.radius:inRect(p,o);}
export function isPointWalkable(p,{benchId=null,allowBoundary=false}={}){
 if(!p||!Number.isFinite(p.x)||!Number.isFinite(p.y))return false;
 if((!allowBoundary&&(p.x<0||p.x>=1024||p.y<0||p.y>=1008))||!GARDEN.walkable.some(poly=>inPoly(p,poly)))return false;
 const bench=GARDEN.benches.find(b=>b.id===benchId);
 return !GARDEN.obstacles.some(o=>hitsObstacle(p,o)&&!(bench&&o.id===bench.id+'-bench'&&inRect(p,bench.bodyPassage)));
}
export function canStand(p,options={}){
 // Continuous 16×16 native body. Include every edge pixel, not only a center sample.
 for(let y=0;y<16;y+=2)for(let x=-8;x<8;x+=2)if(!isPointWalkable({x:p.x+x,y:p.y+y},options))return false;
 return true;
}
export function sweep(a,b,options={}){const n=Math.max(1,Math.ceil(Math.hypot(b.x-a.x,b.y-a.y)/2));for(let i=0;i<=n;i++)if(!canStand({x:a.x+(b.x-a.x)*i/n,y:a.y+(b.y-a.y)*i/n},options))return false;return true;}
export function findPath(start,target,{benchId=null}={}){
 const opts={benchId};if(!canStand(start,opts)||!canStand(target,opts))return null;
 if(sweep(start,target,opts))return [start,target];
 const step=8,key=p=>p.x+','+p.y,grid=p=>({x:Math.round(p.x/step)*step,y:Math.round(p.y/step)*step});
 const a=grid(start),b=grid(target);if(!canStand(a,opts)||!canStand(b,opts))return null;
 const open=[a],cost=new Map([[key(a),0]]),prev=new Map(),closed=new Set();
 const heuristic=p=>Math.abs(p.x-b.x)+Math.abs(p.y-b.y);
 while(open.length){open.sort((p,q)=>(cost.get(key(p))+heuristic(p))-(cost.get(key(q))+heuristic(q)));const p=open.shift(),pk=key(p);if(closed.has(pk))continue;closed.add(pk);
  if(pk===key(b)){const path=[target,b];let q=p;while(prev.has(key(q))){q=prev.get(key(q));path.push(q);}path.push(start);path.reverse();return path.filter((p,i,arr)=>!i||p.x!==arr[i-1].x||p.y!==arr[i-1].y);}
  for(const [dx,dy]of [[step,0],[-step,0],[0,step],[0,-step]]){const q={x:p.x+dx,y:p.y+dy},qk=key(q);if(closed.has(qk)||!sweep(p,q,opts))continue;const c=cost.get(pk)+step;if(c<(cost.get(qk)??Infinity)){cost.set(qk,c);prev.set(qk,p);open.push(q);}}
 }return null;
}
const clamp=x=>Math.min(1,Math.max(0,x));const smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
export function fireGainAtWorld(worldPosition,{muted=false,suspended=false,ready=true}={}){
 if(muted||suspended||!ready||!worldPosition||!Number.isFinite(worldPosition.x)||!Number.isFinite(worldPosition.y))return 0;
 if(GARDEN.quietZonesWorld.some(z=>inRect(worldPosition,z)))return 0;
 const p=fromWorld(worldPosition),s=GARDEN.audio;if(!inRect(p,s.bounds))return 0;
 const edge=Math.min(p.x-s.bounds.x,s.bounds.x+s.bounds.width-p.x,p.y-s.bounds.y,s.bounds.y+s.bounds.height-p.y);
 const distance=Math.hypot(p.x-s.center.x,p.y-s.center.y);
 return s.maxGain*(1-smooth((distance-s.innerRadius)/(s.outerRadius-s.innerRadius)))*smooth(edge/s.edgeFade);
}
