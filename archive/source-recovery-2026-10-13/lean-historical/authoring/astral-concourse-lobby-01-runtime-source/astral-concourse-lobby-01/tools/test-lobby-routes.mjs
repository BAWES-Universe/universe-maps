import fs from 'node:fs';import vm from 'node:vm';import path from 'node:path';import{fileURLToPath}from'node:url';
const R=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');globalThis.window=globalThis;vm.runInThisContext(fs.readFileSync(R+'/validation/easystar-0.4.4.js','utf8'));const n=await import(R+'/validation/native-path-model-speed9.mjs');const m=JSON.parse(fs.readFileSync(R+'/map32/astral-concourse-lobby.tmj'));const h=JSON.parse(fs.readFileSync(R+'/source/collision-grid.json')),g=h.grid,mgr=new n.PathfindingManager(g,{width:32,height:32}),danger=fs.readFileSync(R+'/validation/head-danger.bin'),rows=[],traces=[];
function head(p){for(const x of[Math.floor(p.x),Math.ceil(p.x)])for(const y of[Math.floor(p.y),Math.ceil(p.y)])if(x>=0&&x<1152&&y>=0&&y<896&&danger[y*1152+x])return true;return false;}
async function leg(id,start,click,label,save=false){const p=new n.NativePathPlayer(...start),fit=mgr.fitBodyWithinTile(click.x,click.y,32,32),route=await mgr.findPathFromGameCoordinates({x:p.x,y:p.y},click,false);let frames=0,body=0,heads=0;const samples=[];function check(q){if(n.bodyOverlap(m,g,q))body++;if(head(q))heads++;}check(p);if(route.length){p.setPathToFollow(route,9);while(p.pathToFollow&&frames++<10000){const old={x:p.x,y:p.y};p.followPath(1000/60);check(p);const steps=Math.ceil(Math.hypot(p.x-old.x,p.y-old.y)/.5);for(let i=1;i<steps;i++)check({x:old.x+(p.x-old.x)*i/steps,y:old.y+(p.y-old.y)*i/steps});if(save)samples.push([p.x,p.y,p._lastDirection]);}}
const result={id,label,start,click,final:[p.x,p.y],pathFound:!!route.length,endpointExact:Math.hypot(p.x-fit.x,p.y-fit.y+16)<.001,bodyConflicts:body,headConflicts:heads,frames};rows.push(result);if(save)traces.push({...result,path:route,samples});return[p.x,p.y];}
let cells=0;
for(let y=0;y<g.length;y++)for(let x=0;x<g[y].length;x++)if(!g[y][x]){
 cells++;const start=x===Math.floor(h.start[0]/32)&&y===Math.floor(h.start[1]/32)?[576,432]:h.start;
 for(const dx of[8,16,23])for(const dy of[16,23,31]){
  const end=await leg(`cell-${x}-${y}`,start,{x:x*32+dx,y:y*32+dy},'floor-arrival');
  await leg(`cell-${x}-${y}`,end,{x:start[0],y:start[1]+16},'floor-return');
 }
}
for(const p of h.landmarks){
 const start=p.id==='arrival'?[576,432]:h.start;
 const end=await leg(p.id,start,{x:p.x,y:p.y+16},'landmark-arrival',true);
 await leg(p.id,end,{x:start[0],y:start[1]+16},'landmark-return',true);
}
const failures=rows.filter(r=>!r.pathFound||!r.endpointExact||r.bodyConflicts||r.headConflicts);
const report={scope:'Current75666c0 source-matched native PathfindingManager/Player adapter retained from the frozen Flagship verification. EasyStar0.4.4, native32, nearest=false, source-default speed9,60Hz plus0.5px sweep. No live engine, renderer, pointer-event, network or multiplayer acceptance. Same-cell exact-click behavior is not claimed; alternate approach origin used for default spawn cell.',walkableCells:cells,practicalClickPointsPerCell:9,legs:rows.length,failures:failures.length,allPass:failures.length===0,failedRows:failures,rows};
fs.writeFileSync(R+'/validation/native-routes.json',JSON.stringify(report,null,2));fs.writeFileSync(R+'/validation/route-traces.json',JSON.stringify(traces,null,2));console.log({cells,legs:rows.length,failures:failures.length,failedRows:failures.slice(0,5)});if(failures.length)process.exitCode=1;
