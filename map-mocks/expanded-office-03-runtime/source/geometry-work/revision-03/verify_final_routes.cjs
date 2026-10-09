'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=__dirname;
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n)));
const write=(n,d)=>fs.writeFileSync(path.join(root,n),JSON.stringify(d,null,2)+'\n');
const g=read('source-coordinate-geometry.json'),grid=read('collision-grid-source.json');
const core=require('../universe-painted-arrival/runtime-work/route-core.js');
const width=grid.width,height=grid.height,size=16,baseBlocked=new Set(grid.blockedIndices);
const goals=g.goals,actors=goals.filter(t=>t.kind!=='checkpoint');
const overlap=(a,b)=>a.x<b.x+b.width&&b.x<a.x+a.width&&a.y<b.y+b.height&&b.y<a.y+a.height;
const body=p=>({x:p.x-8,y:p.y,width:16,height:16});
const direction={north:{x:0,y:-1},south:{x:0,y:1},east:{x:1,y:0},west:{x:-1,y:0}};
function segmentHits(a,b,r){
  const epsilon=.000001; let near=0,far=1;
  for(const [origin,v,low,high] of [[a.x,b.x-a.x,r.x-8+epsilon,r.x+r.width+8-epsilon],[a.y,b.y-a.y,r.y-16+epsilon,r.y+r.height-epsilon]]){
    if(Math.abs(v)<epsilon){if(origin<low||origin>high)return false;}
    else{let p=(low-origin)/v,q=(high-origin)/v;if(p>q)[p,q]=[q,p];near=Math.max(near,p);far=Math.min(far,q);if(near>far)return false;}
  }return near<=far;
}
function blockedFor(targetId,startId){
  const occ=actors.filter(t=>t.id!==targetId&&t.id!==startId);
  const blocked=new Set(baseBlocked);
  for(const p of occ){const r=p.bodyBounds;for(let y=Math.floor(r.y/16);y<Math.ceil((r.y+r.height)/16);y++)for(let x=Math.floor(r.x/16);x<Math.ceil((r.x+r.width)/16);x++)blocked.add(y*width+x);}
  return {blocked,occ};
}
function verifySegments(points,blocked,occ){
  const issues=[];
  for(let i=0;i<points.length;i++){
    if(!core.bodyClear(points[i],width,height,blocked,size))issues.push({type:'grid-body-blocked',point:i});
    if(i===0)continue;
    if(!core.segmentClear(points[i-1],points[i],width,height,blocked,size))issues.push({type:'grid-sweep-blocked',segment:i-1});
    for(const r of g.allCollisionRectangles)if(segmentHits(points[i-1],points[i],r))issues.push({type:'source-sweep-collision',segment:i-1,id:r.id});
    for(const p of occ)if(segmentHits(points[i-1],points[i],p.bodyBounds))issues.push({type:'occupied-body-collision',segment:i-1,id:p.id});
  }return issues;
}
function compact(points){
  const out=[];
  for(const p of points){const v={x:p.x,y:p.y};if(out.length&&out.at(-1).x===v.x&&out.at(-1).y===v.y)continue;
    if(out.length>=2){const a=out.at(-2),b=out.at(-1);if((a.x===b.x&&b.x===v.x)||(a.y===b.y&&b.y===v.y))out.pop();}
    out.push(v);
  }return out;
}
const endpointChecks=goals.map(t=>({id:t.id,sourceConflicts:g.allCollisionRectangles.filter(r=>overlap(body(t),r)).map(r=>r.id),gridClear:core.bodyClear(t,width,height,baseBlocked,size)}));
const contactChecks=[];
for(const t of actors){
  const {blocked,occ}=blockedFor(t.id,null);
  if(t.kind==='team-seat'){
    const station=g.stations.find(s=>s.id===t.id),bench=g.workbenches.find(b=>b.id===station.sharedWorkbenchId);
    const p=t.facing==='south'?{x:bench.table.x+64,y:t.y}:{x:t.x,y:t.y+32};
    station.approach=p;t.approach=p;
    station.contactApproach={...p,finalWalkDirection:p.x<t.x?'east':p.x>t.x?'west':'north',pushDirection:t.contactDirection,method:'walk checked approach to seat; then attempt1px toward table'};
    t.contactApproach=station.contactApproach;
    const issues=verifySegments([p,t],blocked,occ);
    const d=direction[t.contactDirection],pressed={x:t.x+d.x,y:t.y+d.y};
    contactChecks.push({id:t.id,approach:p,seat:{x:t.x,y:t.y},pushDirection:t.contactDirection,
      sourceApproachPassed:!issues.length,onePixelTowardTableBlocked:!core.bodyClear(pressed,width,height,baseBlocked,size),issues});
  }else if(t.contactDirection){
    const d=direction[t.contactDirection],pressed={x:t.x+d.x,y:t.y+d.y};
    contactChecks.push({id:t.id,seat:{x:t.x,y:t.y},pushDirection:t.contactDirection,
      onePixelTowardTableBlocked:!core.bodyClear(pressed,width,height,baseBlocked,size),sourceApproachPassed:true});
  }
}
const routes=[],results=[];
for(const startId of ['main-entrance','reception-visitor']){
  const start=goals.find(t=>t.id===startId);
  for(const target of goals){
    if(target.id===startId)continue;
    const {blocked,occ}=blockedFor(target.id,start.id);
    const destination=target.approach||target;
    const found=core.findRoute(start,destination,width,height,blocked,size);
    if(!found){results.push({id:`${start.id}-to-${target.id}`,passed:false,issues:[{type:'BFS-no-route'}]});continue;}
    const points=compact([start,...found,...(target.approach?[target]:[])]);
    for(const reverse of [false,true]){
      const pts=reverse?[...points].reverse():points;
      const issues=verifySegments(pts,blocked,occ);
      results.push({id:`${start.id}-to-${target.id}${reverse?'-reverse':''}`,passed:issues.length===0,issues,
        occupiedBodiesTested:occ.length,waypointCount:pts.length});
    }
    const crossedClaims=[...new Set(g.claimPlots.filter(p=>p.id!==target.claimPlotId&&points.some((v,i)=>i&&segmentHits(points[i-1],v,p))).map(p=>p.id))];
    routes.push({id:`${start.id}-to-${target.id}`,startId:start.id,targetId:target.id,targetKind:target.kind,
      coordinateSpace:'source office pixels',points,alsoTestReverse:true,otherOccupiedBodies:occ.length,
      otherDraftClaimAreasTraversed:crossedClaims,claimNote:'Draft ownership areas do not restrict physical entry.',contactApproach:target.contactApproach||null});
  }
}
const failures=results.filter(t=>!t.passed),badEndpoints=endpointChecks.filter(t=>!t.gridClear||t.sourceConflicts.length),badContacts=contactChecks.filter(t=>!t.onePixelTowardTableBlocked||!t.sourceApproachPassed);
const status=failures.length||badEndpoints.length||badContacts.length?'failed':'passed';
write('route-validation.json',{status,routeCount:routes.length,directionalTestCount:results.length,
  endpointCount:endpointChecks.length,contactTestCount:contactChecks.length,
  failedCount:failures.length+badEndpoints.length+badContacts.length,
  coordinateSpace:'source office pixels; full-canvas grid verified by translated equivalence',
  physicalBody:{xOffset:-8,yOffset:0,width:16,height:16},gridCellSize:16,
  occupiedState:'Every other furniture/reception goal body is blocked; this is an offline conservative occupancy fixture, not live multiplayer.',
  endpointChecks,contactChecks,results});
write('route-manifest.json',{status,coordinateSpace:'source office pixels',renderTranslation:{x:32,y:32},routes});
write('route-manifest-full-canvas.json',{status,coordinateSpace:'rendered full canvas',translationApplied:{x:32,y:32},routes:routes.map(r=>({...r,coordinateSpace:'rendered full canvas',points:r.points.map(p=>({x:p.x+32,y:p.y+32})),contactApproach:r.contactApproach?{...r.contactApproach,x:r.contactApproach.x+32,y:r.contactApproach.y+32}:null}))});
g.status=status==='passed'?'assembled-art geometry and route checks passed; compiled runtime verification separate':'geometry blocked; inspect route-validation.json';
write('source-coordinate-geometry.json',g);
write('checkpoint-manifest.json',{status,coordinateSpace:'source office pixels',renderTranslation:{x:32,y:32},origins:['main-entrance','reception-visitor'],goals});
write('checkpoint-manifest-full-canvas.json',{status,coordinateSpace:'rendered full canvas',translationApplied:{x:32,y:32},origins:['main-entrance','reception-visitor'],goals:goals.map(t=>({...t,x:t.x+32,y:t.y+32,bodyBounds:{...t.bodyBounds,x:t.bodyBounds.x+32,y:t.bodyBounds.y+32},approach:t.approach?{x:t.approach.x+32,y:t.approach.y+32}:undefined,contactApproach:t.contactApproach?{...t.contactApproach,x:t.contactApproach.x+32,y:t.contactApproach.y+32}:undefined}))});
console.log(JSON.stringify({status,routes:routes.length,directionalTests:results.length,endpoints:goals.length,contactTests:contactChecks.length,badEndpoints,badContacts,routeFailures:failures.slice(0,15)},null,2));
if(status!=='passed')process.exitCode=1;
