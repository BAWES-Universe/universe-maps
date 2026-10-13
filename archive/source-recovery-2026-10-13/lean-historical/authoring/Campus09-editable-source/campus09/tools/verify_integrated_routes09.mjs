import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';import path from 'node:path';const R=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),V=R+'/validation';
globalThis.window=globalThis;vm.runInThisContext(fs.readFileSync(V+'/easystar-0.4.4.js','utf8'));const n=await import(V+'/native-path-model-speed9.mjs');const read=p=>JSON.parse(fs.readFileSync(p));const map=read(R+'/map32/magical-campus.tmj'),grid=n.gridFromMap(map),manager=new n.PathfindingManager(grid,{width:32,height:32}),spawn={x:936,y:1568};
const regions=read(R+'/seating-study/practical-floor-regions.json').regions;const targets=regions.map(r=>({id:r.id,click:{x:r.floorTargetRectWorld[0]+16,y:r.floorTargetRectWorld[1]+8}}));
const states=[],rows=[];
for(const t of targets){
 let p=new n.NativePathPlayer(spawn.x,spawn.y);
 for(const direction of['arrival','departure']){
  const click=direction==='arrival'?t.click:{x:spawn.x,y:spawn.y+16};const fitted=manager.fitBodyWithinTile(click.x,click.y,32,32);const expected={x:fitted.x,y:fitted.y-16};const start={x:p.x,y:p.y};const route=await manager.findPathFromGameCoordinates(start,click,false);let frames=0,overlaps=0;const trace=[];
  if(route.length){p.setPathToFollow(route,9);while(p.pathToFollow&&frames<10000){const old={x:p.x,y:p.y};p.followPath(1000/60);frames++;if(n.bodyOverlap(map,grid,p))overlaps++;trace.push([p.x,p.y,p.x-old.x,p.y-old.y]);}}
  const exact=Math.hypot(p.x-expected.x,p.y-expected.y)<.001;rows.push({id:t.id,direction,start,click,expected,final:{x:p.x,y:p.y},frames,overlaps,exact,pathFound:route.length>0,pass:route.length>0&&exact&&overlaps===0});states.push({id:t.id,direction,trace});
 }
}
const report={scope:'Full newly compiled native32 campus, unmodified source path methods/EasyStar at180px/s,60Hz. No browser/client/device claim.',sourcePin:'d2bc57b63b4abab9303fb3cbcecf1a0450fd15cc',mapSha256:crypto.createHash('sha256').update(fs.readFileSync(R+'/map32/magical-campus.tmj')).digest('hex'),sourceModelSha256:crypto.createHash('sha256').update(fs.readFileSync(V+'/native-path-model-speed9.mjs')).digest('hex'),allPass:rows.every(r=>r.pass),rows};fs.writeFileSync(R+'/docs/integrated-office-routes09.json',JSON.stringify(report,null,2)+'\n');fs.writeFileSync(R+'/docs/integrated-office-route-traces09.json',JSON.stringify(states)+'\n');console.log(JSON.stringify({allPass:report.allPass,routes:rows.length,failures:rows.filter(r=>!r.pass)}));
