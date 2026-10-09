/* Source-coordinate tests using the previously reviewed native16×16 body helper. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const corePath = '../universe-painted-arrival/runtime-work/route-core.js';
const core = require(corePath);
const root = __dirname;
const geometry = JSON.parse(fs.readFileSync(path.join(root, 'source-coordinate-geometry.json')));
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'route-manifest.json')));
const size = 16, width = 152, height = 84;
const rects = geometry.permanentWalls.concat(geometry.lowDividers, geometry.furnitureCollisionRectangles);
const overlap = (a,b) => a.x < b.x+b.width && b.x < a.x+a.width && a.y < b.y+b.height && b.y < a.y+a.height;
const inside = (p,r) => p.x >= r.x && p.x < r.x+r.width && p.y >= r.y && p.y < r.y+r.height;
const blocked = new Set();
for (let y=0; y<height; y++) for (let x=0; x<width; x++) {
  const cell = {x:x*size,y:y*size,width:size,height:size};
  const center={x:cell.x+size/2,y:cell.y+size/2};
  if (!geometry.floor.envelopes.some(r => inside(center,r)) || rects.some(r => overlap(cell,r))) blocked.add(y*width+x);
}
function sweepRect(a,b) {
  if (a.x !== b.x && a.y !== b.y) throw new Error('Explicit manifest contains non-axis-aligned path');
  return {x:Math.min(a.x,b.x)-8,y:Math.min(a.y,b.y),width:Math.abs(a.x-b.x)+16,height:Math.abs(a.y-b.y)+16};
}
const results = [];
for (const route of manifest.routes) {
  const target = geometry.stations.find(s => s.id === route.targetStationId);
  const otherPlots = target ? geometry.claimPlots.filter(p => p.id !== target.claimPlotId) : geometry.claimPlots;
  const otherOccupants = geometry.stations.filter(s => s.id !== target?.id).map(s => ({...s.seat.bodyBounds,id:s.id}));
  for (const reverse of route.alsoTestReverse ? [false,true] : [false]) {
    const points = reverse ? [...route.points].reverse() : route.points;
    const issues=[];
    for (let i=0;i<points.length;i++) {
      if (!core.bodyClear(points[i],width,height,blocked,size)) issues.push({type:'blocked-body',point:i});
      if (i===0) continue;
      if (!core.segmentClear(points[i-1],points[i],width,height,blocked,size)) issues.push({type:'blocked-segment',segment:i-1});
      const swept=sweepRect(points[i-1],points[i]);
      for (const p of otherPlots) if (overlap(swept,p)) issues.push({type:'crossed-other-claim',segment:i-1,id:p.id});
      for (const p of otherOccupants) if (overlap(swept,p)) issues.push({type:'crossed-occupied-seat',segment:i-1,id:p.id});
    }
    const found = core.findRoute(points[0],points.at(-1),width,height,blocked,size);
    const foundValid = !!found && [points[0],...found].every((p,i,all)=>i===0 || core.segmentClear(all[i-1],p,width,height,blocked,size));
    if (!foundValid) issues.push({type:'core-route-search-failed'});
    results.push({id:route.id+(reverse?'-reverse':''),passed:issues.length===0,issues,
      sourceWaypointCount:points.length,coreGeneratedWaypointCount:found?.length??0,
      exactOtherPlotAvoidance:true,otherSeatBodiesTested:otherOccupants.length});
  }
}
// A native body immediately inside the desk fails. The exact seat touching
// the south edge succeeds. This catches accidental visual-only desk blockers.
const contactStops=geometry.stations.map(s=>({id:s.id,
  seatBodyClear:core.bodyClear(s.seat,width,height,blocked,size),
  onePixelTowardTableBlocked:!core.bodyClear({x:s.seat.x,y:s.seat.y+(s.seat.facing==='south'?1:-1)},width,height,blocked,size)}));
const failed=results.filter(r=>!r.passed);
const contactFailed=contactStops.filter(r=>!r.seatBodyClear||!r.onePixelTowardTableBlocked);
const report={status:failed.length||contactFailed.length?'failed':'passed',
  routeCount:manifest.routes.length,directionalTestCount:results.length,failedCount:failed.length+contactFailed.length,
  blockedTileCount:blocked.size,widthTiles:width,heightTiles:height,nativeTileSize:size,
  body:{xOffset:-8,yOffset:0,width:16,height:16},
  implementation:{path:corePath,sha256:crypto.createHash('sha256').update(fs.readFileSync(corePath)).digest('hex')},
  claimPlotAvoidance:'Exact half-open rectangle sweeps; claims are deliberately not tile-rounded.',
  scope:'Physical workbench geometry plus offline native-body routing; revised receiver cabinet masks are EXCLUDED pending assembly. No engine, audio, permissions, ownership, or live multiplayer behavior asserted.',
  furniturePending:geometry.reservations.map(r=>r.id),pendingObstacleMasks:geometry.pendingObstacleMasks,tmjPackaging:geometry.packaging,results,contactStops};
fs.writeFileSync(path.join(root,'route-validation.json'),JSON.stringify(report,null,2)+'\n');
fs.writeFileSync(path.join(root,'collision-grid.json'),JSON.stringify({width,height,tileSize:size,blockedIndices:[...blocked].sort((a,b)=>a-b)},null,2)+'\n');
console.log(JSON.stringify({status:report.status,routeCount:report.routeCount,directionalTests:results.length,contactStops:contactStops.length,failures:failed,contactFailed},null,2));
if(report.status!=='passed') process.exitCode=1;
