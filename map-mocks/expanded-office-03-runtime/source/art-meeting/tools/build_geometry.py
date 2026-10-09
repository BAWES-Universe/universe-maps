#!/usr/bin/env python3
"""Offline meeting geometry and swept native-body route checks, not runtime."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def rect(x,y,w,h): return dict(x=x,y=y,width=w,height=h)
FRAMES={'south':1,'west':4,'east':7,'north':10}
ANCHORS={'north':[24,16],'south':[24,32],'east':[26,32],'west':[22,32]}
def seat(id,x,y,facing,route):
 a=ANCHORS[facing]
 return dict(id=id,center=[x,y],facing=facing,frameIndex=FRAMES[facing],spriteBounds=rect(x-16,y-16,32,32),bodyBounds=rect(x-8,y,16,16),chairAsset=f'assets/chair-{facing}-native.png',chairOrigin=[x-a[0],y-a[1]],chairAnchorLocal=a,foregroundAsset=f'assets/chair-{facing}-foreground-native.png',entryRoute=route,exitRoute=list(reversed(route)),scale=1,livePlayer=False)
small=dict(id='small-four-cardinal',interior=rect(0,0,256,192),door=rect(-32,64,32,96),table=rect(80,64,96,64),tableAsset='assets/table-small-native.png',tableOrigin=[64,48],tabletop=rect(80,64,96,48),seats=[
 seat('north-place',128,48,'south',[[16,104],[32,104],[32,16],[128,16],[128,48]]),
 seat('south-place',128,128,'north',[[16,104],[32,104],[32,160],[128,160],[128,128]]),
 seat('west-place',72,88,'east',[[16,104],[40,104],[40,88],[72,88]]),
 seat('east-place',184,88,'west',[[16,104],[32,104],[32,160],[224,160],[224,88],[184,88]])])
large=dict(id='conference-six',interior=rect(0,0,256,384),door=rect(-32,160,32,96),table=rect(32,128,192,96),tableAsset='assets/table-conference-native.png',tableOrigin=[16,112],tabletop=rect(32,128,192,80),seats=[])
for i,x in enumerate((64,128,192),1):
 large['seats'].append(seat(f'north-place-{i}',x,112,'south',[[16,200],[16,64],[x,64],[x,112]]))
 large['seats'].append(seat(f'south-place-{i}',x,224,'north',[[16,200],[16,288],[x,288],[x,224]]))
def overlap(a,b): return a['x']<b['x']+b['width'] and a['x']+a['width']>b['x'] and a['y']<b['y']+b['height'] and a['y']+a['height']>b['y']
results=[]
for layout in (small,large):
 for s in layout['seats']:
  blockers=[layout['table']]+[q['bodyBounds'] for q in layout['seats'] if q['id']!=s['id']]
  samples=[]; failures=[]
  for (x0,y0),(x1,y1) in zip(s['entryRoute'],s['entryRoute'][1:]):
   assert x0==x1 or y0==y1
   n=abs(x1-x0)+abs(y1-y0)
   for t in range(n+1):
    x=x0+(x1-x0)*t/max(n,1);y=y0+(y1-y0)*t/max(n,1);b=rect(x-8,y,16,16)
    inside=b['x']>=0 and b['y']>=0 and b['x']+16<=layout['interior']['width'] and b['y']+16<=layout['interior']['height']
    if not inside or any(overlap(b,q) for q in blockers):failures.append([x,y])
    samples.append([x,y])
  results.append(dict(layout=layout['id'],seat=s['id'],samples=len(samples),otherSeatsOccupied=True,forwardAndReverseSameSweptEnvelope=True,passed=not failures,failures=failures))
geometry=dict(format='meeting-native-geometry-v1',status='offline furniture registration and geometry proof; no engine/multiplayer/live wiring',units='native world pixels; half-open rectangles',avatar=dict(source='../universe-native-team-fixture/assets/greg-reference.png',frameSize=[32,32],scale=1,bodyRelativeToCenter=rect(-8,0,16,16),frames=FRAMES,protectedHeadRelative=rect(-16,-16,32,14)),chairCollision='none; seats are walkable allocations; table footprint blocks movement',layouts=[small,large],placements=[dict(roomId='meeting-a',layoutId=small['id'],origin=[2144,480]),dict(roomId='meeting-b',layoutId=small['id'],origin=[2144,704]),dict(roomId='conference',layoutId=large['id'],origin=[2144,928])],limits=['Static repeated Greg scale fixtures, not multiplayer users.','Exact seat interaction/claims and collision integration remain unimplemented.','Painted asset extents must be checked against planned table collision rectangles.','Routes sweep a16×16 body at1px increments with every other occupied seat body blocked.'])
(R/'geometry-plan.json').write_text(json.dumps(geometry,indent=2)+'\n')
(R/'proofs/route-checks.json').write_text(json.dumps(dict(passed=all(q['passed'] for q in results),checks=results),indent=2)+'\n')
print(json.dumps(dict(passed=all(q['passed'] for q in results),routes=len(results),samples=sum(q['samples'] for q in results))))
