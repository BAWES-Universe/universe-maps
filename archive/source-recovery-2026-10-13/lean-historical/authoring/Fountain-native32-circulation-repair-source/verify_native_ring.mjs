import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';
const root='/workspace/shared/magical-campus-return-08/validation-work',R='/workspace/shared/magical-campus-standard32-09/fountain-study';
globalThis.window=globalThis;vm.runInThisContext(fs.readFileSync(root+'/easystar-0.4.4.js','utf8'));const native=await import(root+'/native-path-model-speed9.mjs');
const read=p=>JSON.parse(fs.readFileSync(p));const d=read(R+'/ring-geometry02.json');const b=new Set(d.blockedCells.map(([x,y])=>y*19+x));const grid=Array.from({length:14},(_,y)=>Array.from({length:19},(_,x)=>b.has(y*19+x)?1:0));
const manager=new native.PathfindingManager(grid,{width:32,height:32});const cells=d.pathCells;const points=cells.map(([x,y])=>({x:x*32+16,y:y*32+8}));
const results=[];let frames=0;
for(const direction of ['clockwise','counterclockwise'])for(let pass=0;pass<2;pass++){
 const route=direction==='clockwise'?points:[...points].reverse();const p=new native.NativePathPlayer(route[0].x,route[0].y);let overlaps=0,fallback=0;const legs=[];
 const destinations=route.filter((_,i)=>i%3===0||i===route.length-1);
 for(const end of destinations.slice(1)){
  const click={x:end.x,y:end.y+16};const path=await manager.findPathFromGameCoordinates({x:p.x,y:p.y},click,false);if(path.length===0)throw Error('Missing exact target route');
  p.setPathToFollow(path,9);let local=0;
  while(p.pathToFollow&&local<5000){p.followPath(1000/60);local++;frames++;if(native.bodyOverlap({tilewidth:32},grid,p))overlaps++;}
  const exact=Math.hypot(p.x-end.x,p.y-end.y)<.001;if(!exact)fallback++;legs.push({click,expectedSpriteCenter:end,final:{x:p.x,y:p.y},frames:local,exact});
 }
 results.push({direction,pass,legs,overlaps,wrongFinalPosition:fallback,pass:overlaps===0&&fallback===0});
}
// Source physical sweep of the independently prescribed cardinal joystick loop.
let sweepSamples=0,sweepOverlaps=0,minClearance=Infinity;
for(const order of [points,[...points].reverse()])for(let i=1;i<order.length;i++){
 const a=order[i-1],z=order[i],n=Math.ceil(Math.hypot(z.x-a.x,z.y-a.y));
 for(let k=0;k<=n;k++){const p={x:a.x+(z.x-a.x)*k/n,y:a.y+(z.y-a.y)*k/n};sweepSamples++;if(native.bodyOverlap({tilewidth:32},grid,p))sweepOverlaps++;
  for(const [bx,by]of d.blockedCells){const dx=Math.max(bx*32-(p.x+8),p.x-8-(bx+1)*32,0),dy=Math.max(by*32-(p.y+16),p.y-(by+1)*32,0);minClearance=Math.min(minClearance,Math.hypot(dx,dy));}
 }
}
const report={scope:'Unmodified current Universe source-extracted PathfindingManager and Player path methods, EasyStar0.4.4, native32cells,16x16body, speed9=180px/s,60Hz interpolation. Analytical source/geometry evidence only; no browser/nativeclient or physicalphone claim.',sourcePin:'d2bc57b63b4abab9303fb3cbcecf1a0450fd15cc',sourceSha256:crypto.createHash('sha256').update(fs.readFileSync(root+'/native-path-model-speed9.mjs')).digest('hex'),tileSize:32,body:[-8,0,16,16],frames,results,manualLoop:{source:'Independent cardinal joystick-style centerline,1px sweep both directions',samples:sweepSamples,overlaps:sweepOverlaps,minBodyClearancePx:minClearance,lengthPx:(points.length-1)*32,idealSecondsAtSourceDefault:((points.length-1)*32)/180},allPass:results.every(r=>r.pass)&&sweepOverlaps===0};fs.writeFileSync(R+'/native-ring-verification.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({allPass:report.allPass,frames,runs:results.length,manualLoop:report.manualLoop}));if(!report.allPass)process.exitCode=1;
