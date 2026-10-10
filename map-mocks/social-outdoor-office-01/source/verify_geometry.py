from pathlib import Path
from collections import deque
import json,hashlib
R=Path(__file__).resolve().parents[1]; M=json.loads((R/'map/studenthub-outdoor-office.tmj').read_text()); W,H=M['width']*M['tilewidth'],M['height']*M['tileheight']; T=M['tilewidth']; MW=M['width']
C=next(l['data'] for l in M['layers'] if l['name']=='permanent-collisions')
def clear(x,y):
 if x<8 or x>W-8 or y<0 or y>H-16:return False
 return all(C[yy*MW+xx]==0 for yy in range(y//T,(y+15)//T+1) for xx in range((x-8)//T,(x+7)//T+1))
# Native body x-8..x+8, y..y+16; 8px node grid. Edge sweep at one pixel.
def edge(a,b):
 d=max(abs(b[0]-a[0]),abs(b[1]-a[1])); return all(clear(round(a[0]+(b[0]-a[0])*i/d),round(a[1]+(b[1]-a[1])*i/d)) for i in range(1,d+1))
s=(496,704);q=deque([s]);prev={s:None}
while q:
 a=q.popleft()
 for dx,dy in [(8,0),(-8,0),(0,8),(0,-8)]:
  b=a[0]+dx,a[1]+dy
  if b not in prev and clear(*b) and edge(a,b):prev[b]=a;q.append(b)
points=[('garden-entry',496,624),('commons',496,480),('west-table-front',400,400),('west-table-north',400,288),('east-table-front',736,400),('east-table-north',736,288),('west-desk-approach',224,304),('east-desk-approach',304,304),('lounge-approach',208,496),('refreshment-approach',736,512),('rear-spine',528,240),('exit',496,704)]
res=[]
for n,x,y in points:
 p=(x,y);path=[]
 if p in prev:
  while p is not None:path.append({'x':p[0],'y':p[1]});p=prev[p]
  path.reverse()
 res.append({'name':n,'x':x,'y':y,'clear':clear(x,y),'reachableFromSpawnAndReversible':bool(path),'route':path})
seats=json.loads((R/'source/seat-contract.json').read_text())['seats']
authored=[]
for seat in seats:
 anchor=(seat['x'],seat['y']);start=(seat['egress'][0]['x'],seat['egress'][0]['y']);others=[(o['x'],o['y']) for o in seats if o['id']!=seat['id']]
 def allowed(p):return all(clear(p[0]+dx,p[1]+dy) for dx in [-2,0,2] for dy in [-2,0,2]) and all(not(p[0]-10<o[0]+8 and p[0]+10>o[0]-8 and p[1]-2<o[1]+16 and p[1]+18>o[1]) for o in others)
 q=deque([start]);pr={start:None}
 while q:
  a=q.popleft()
  for dx,dy in [(8,0),(-8,0),(0,8),(0,-8)]:
   b=a[0]+dx,a[1]+dy
   if b not in pr and allowed(b) and edge(a,b):pr[b]=a;q.append(b)
 p=s;path=[]
 if p in pr:
  while p is not None:path.append({'x':p[0],'y':p[1]});p=pr[p]
  path.reverse();path.insert(0,{'x':anchor[0],'y':anchor[1]})
 # Compress collinear path for stable browser routing.
 simple=[]
 for i,p in enumerate(path):
  if i==0 or i==len(path)-1 or (path[i-1]['x']!=path[i+1]['x'] and path[i-1]['y']!=path[i+1]['y']):simple.append(p)
 authored.append({**seat,'clear':clear(*anchor),'allOtherSeatBodiesOccupiedExitPass':bool(path),'exitRoute':simple})
report={'scope':'Offline native16x16-body geometry, native32px map cells; not browser physics or multiplayer','avatarFrame':[32,32],'bodyBounds':'x-8..x+8, y..y+16','sourceMapSha256':hashlib.sha256((R/'map/studenthub-outdoor-office.tmj').read_bytes()).hexdigest(),'routes':res,'authoredSeatAudit':authored,'allApproachRoutesPass':all(p['reachableFromSpawnAndReversible'] for p in res),'allEightSeatExitRoutesPass':all(p['clear'] and p['allOtherSeatBodiesOccupiedExitPass'] for p in authored),'scripts':M.get('properties',[]),'limitations':['Other occupants modelled as native16px solid bodies for conservative route planning; not a live multiplayer test.','No forced interaction or silent property.']}
(R/'source/generated/geometry-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'approaches':report['allApproachRoutesPass'],'seatExits':report['allEightSeatExitRoutesPass'],'seats':[(r['id'],r['clear'],r['allOtherSeatBodiesOccupiedExitPass']) for r in authored]},indent=2))
