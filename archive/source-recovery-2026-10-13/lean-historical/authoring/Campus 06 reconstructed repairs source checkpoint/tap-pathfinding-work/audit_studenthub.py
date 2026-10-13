#!/usr/bin/env python3
"""Read-only StudentHub source audit. Analytical swept-body checks, not a mobile playtest."""
import argparse, bisect, hashlib, heapq, json, math
from pathlib import Path
P=Path(__file__).parent
DEFAULT=Path('/workspace/shared/recovered-campus06/public/butterfly-town/v6/map16/magical-campus.tmj')
def props(o): return {p['name']:p['value'] for p in o.get('properties',[])}
def flat(layers):
 for l in layers:
  if l['type']=='group':yield from flat(l['layers'])
  else:yield l

def audit(path=DEFAULT):
 m=json.loads(path.read_text());w,h=m['width'],m['height'];ls=list(flat(m['layers']));by={l['name']:l for l in ls};ts=sorted(m['tilesets'],key=lambda s:s['firstgid']);firsts=[t['firstgid'] for t in ts]
 def tp(gid):
  if not gid:return {}
  gid=gid&0x1fffffff;t=ts[bisect.bisect_right(firsts,gid)-1]
  return props(next((tile for tile in t.get('tiles',[]) if tile['id']==gid-t['firstgid']),{}))
 def layer_grid(layer):return [bool(tp(g).get('collides',False)) for g in layer['data']]
 solids={l['name']:layer_grid(l) for l in ls if l['type']=='tilelayer'}
 collision=solids['collision-permanent']
 def blocked(x,y):return x<0 or y<0 or x>=w or y>=h or collision[y*w+x]
 def body_hits(px,py):
  # Native16x16 body: x−8..x+8 and y..y+16, with touching permitted.
  return [(x,y) for y in range(math.floor(py/16),math.floor((py+16-1e-7)/16)+1) for x in range(math.floor((px-8)/16),math.floor((px+8-1e-7)/16)+1) if blocked(x,y)]
 def path_cells(start,end):
  q=[(0,0,start)];dist={start:0};prev={start:None}
  while q:
   _,d,p=heapq.heappop(q)
   if d!=dist[p]:continue
   if p==end:break
   x,y=p
   for dx,dy in [(0,-1),(1,0),(0,1),(-1,0),(-1,-1),(1,-1),(1,1),(-1,1)]:
    n=x+dx,y+dy
    if blocked(*n) or (dx and dy and (blocked(x+dx,y) or blocked(x,y+dy))):continue
    nd=d+math.hypot(dx,dy)
    if nd>=dist.get(n,float('inf')):continue
    dist[n]=nd;prev[n]=p;heapq.heappush(q,(nd+math.hypot(n[0]-end[0],n[1]-end[1]),nd,n))
  if end not in prev:raise AssertionError(('no route',start,end))
  path=[];p=end
  while p is not None:path.append(p);p=prev[p]
  return path[::-1]
 def swept(points):
  hits=[];checks=0
  for a,b in zip(points,points[1:]):
   steps=max(1,math.ceil(max(abs(a[0]-b[0]),abs(a[1]-b[1]))*2))
   for k in range(steps+1):
    x=a[0]+(b[0]-a[0])*k/steps;y=a[1]+(b[1]-a[1])*k/steps;checks+=1
    if hit:=body_hits(x,y):hits.append({'position':[x,y],'blocked':hit})
  return checks,hits
 roof_names=[l['name'] for l in ls if l['name'].startswith('roof-')]
 assert len(roof_names)==4
 roof_colliders={n:sum(solids[n]) for n in roof_names};assert not any(roof_colliders.values())
 # Native updateCollisionGrid skips invisible layers, but not visible alpha-zero layers.
 assert by['collision-permanent']['visible'] is True and by['collision-permanent']['opacity']==0
 grid_states=[]
 for mask in range(16):
  included={n for i,n in enumerate(roof_names) if (mask>>i)&1}
  grid=[False]*(w*h)
  for l in ls:
   if l['type']!='tilelayer':continue
   if l['name'] in roof_names and l['name'] not in included:continue
   if l['name'] not in roof_names and not l.get('visible',True):continue
   grid=[a or b for a,b in zip(grid,solids[l['name']])]
  assert grid==collision
  grid_states.append(hashlib.sha256(bytes(grid)).hexdigest())
 rows=[]
 for y in range(91,107):
  opened=[x for x in range(101,118) if not blocked(x,y)]
  rows.append({'row':y,'worldY':[16*y,16*y+16],'openColumnsWithin101To117':opened})
 routes=[];total=0
 for start_x in range(107,113):
  for end_x in range(107,113):
   for southbound in [False,True]:
    start=(start_x,106 if not southbound else 88);end=(end_x,88 if not southbound else 106)
    route=path_cells(start,end)
    # These are interior route waypoints extracted native transform:
    # cell center y=16*row+8, Player adjustment −16 => origin16*row−8.
    points=[(x*16+8,y*16-8) for x,y in route]
    # Actual starting origin, followed by native −8px first waypoint,
    # and exact-target fit (floor tap y/16)*16 as final origin.
    points.insert(0,(start[0]*16+8,start[1]*16))
    points[-1]=(end[0]*16+8,end[1]*16)
    checks,hits=swept(points);total+=checks
    assert not hits,(start,end,hits[:3])
    routes.append({'startCell':start,'endCell':end,'cells':route,'nativeTransformedOrigins':points,'sweptSamples':checks,'bodyCollisionCount':len(hits)})
 # Native straight keyboard/joystick ingress from courtyard across both roof thresholds.
 checks,hits=swept([(1752,1712),(1752,1408)]);assert not hits;total+=checks
 contract=json.loads(props(m)['campusRoofContract']);areas={o['name']:o for l in ls for o in l.get('objects',[])}
 office=next(b for b in contract['buildings'] if b['id']=='office')
 result={
  'status':'read-only analytical audit; no live mobile reproduction',
  'map':str(path),'mapSha256':hashlib.sha256(path.read_bytes()).hexdigest(),
  'dimensions':[w,h,16,16],
  'collisionPermanent':{'visible':by['collision-permanent']['visible'],'opacity':by['collision-permanent']['opacity'],'collidingCells':sum(collision),'sha256':hashlib.sha256(bytes(collision)).hexdigest()},
  'adaptiveRoofCollidingCells':roof_colliders,'distinctCollisionGridHashesAcross16RoofStates':sorted(set(grid_states)),
  'studentHub':{'nativeContractId':'office','approach':areas[office['approachAreas'][0]],'interior':areas[office['interiorAreas'][0]],'doorCorridor':{'openColumns':[107,108,109,110,111,112],'worldLeft':1712,'worldRight':1808,'widthPx':96,'legal16pxBodyCenterX':[1720,1800]},'rows':rows},
  'routeVerification':{'count':len(routes),'sweptSamplesIncludingStraightJoystick':total,'sweepSpacingPx':0.5,'bodyDimensions':[16,16],'nativeIntermediateWaypointOrigin':['16*column+8','16*row-8'],'allClear':True,'scope':'six center columns,36start/end pairs, both directions, y1400..1712, including first8pxleg and exact-target endpoint; no actual touch/Phaser runtime'},
  'routes':routes,
 }
 return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--map',type=Path,default=DEFAULT);args=a.parse_args();r=audit(args.map)
 (P/'studenthub-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['routes','studentHub']},indent=2))
