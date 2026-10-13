from PIL import Image,ImageDraw
from pathlib import Path
from collections import deque
import numpy as np,json,math,hashlib
R=Path(__file__).resolve().parent
M=json.loads((R/'module.json').read_text());W,H=M['size']
g=json.loads((R/'collision-grid.json').read_text());blocked=np.zeros((g['height'],g['width']),np.uint8);blocked.flat[g['blockedIndices']]=1
walk=np.repeat(np.repeat(1-blocked,16,axis=0),16,axis=1)
fg=np.asarray(Image.open(R/'office-foreground.png'))[:,:,3]
sheet=np.asarray(Image.open('/workspace/shared/recovered-pre-island-package/runtime/assets/greg.png'))
heads=[]
for row in range(4):
 for col in range(3):heads.append(sheet[row*32:row*32+14,col*32:col*32+32,3]>32)
def free(x,y):return x>=8 and y>=0 and x+8<=W and y+16<=H and walk[y:y+16,x-8:x+8].all()
def pixels(points):
 out=[]
 for a,b in zip(points,points[1:]):
  assert a[0]==b[0] or a[1]==b[1],(a,b)
  dist=abs(a[0]-b[0])+abs(a[1]-b[1]);dx=0 if a[0]==b[0] else (1 if b[0]>a[0] else -1);dy=0 if a[1]==b[1] else (1 if b[1]>a[1] else -1)
  out.extend((a[0]+dx*t,a[1]+dy*t) for t in range(dist+1))
 return out
issues=[];checks=[];contacts=[];pairchecks=[]
occ=[q for q in M['anchors'] if q['kind'] in ['work-seat','reception-staff','reception-visitor','meeting-seat','lounge-seat']]
# BFS on exact body grid every4px to confirm connected access to every anchor.
spawn=(544,944);seen={spawn};queue=deque([spawn])
while queue:
 x,y=queue.popleft()
 for xx,yy in [(x+4,y),(x-4,y),(x,y+4),(x,y-4)]:
  if (xx,yy) not in seen and free(xx,yy):seen.add((xx,yy));queue.append((xx,yy))
for q in M['anchors']:
 ok=free(q['x'],q['y']);reachable=(q['x'],q['y']) in seen
 checks.append(dict(id=q['id'],collisionFree=bool(ok),reachable=reachable))
 if not(ok and reachable):issues.append(['anchor',q['id'],q['x'],q['y'],bool(ok),reachable])
routechecks=[];headchecks=0
for route in M['routes']:
 pts=pixels(route['points']);fail=[];headfail=[];minpeer=1e6;nearest=None
 for x,y in pts:
  if not free(x,y):fail.append([x,y])
  crop=fg[y-16:y-2,x-16:x+16]>32
  if crop.shape==(14,32):
   for i,head in enumerate(heads):
    headchecks+=1
    if (head&crop).any():headfail.append([x,y,i,int((head&crop).sum())])
  for peer in occ:
   if peer['id']==route.get('start') or peer['id']==route.get('intendedPartner') or peer['id']==route['id'].removesuffix('-approach') or peer['id'] in route.get('intendedGroupIds',[]):continue
   dist=math.hypot(peer['x']-x,peer['y']-y)
   if dist<minpeer:minpeer=dist;nearest=peer['id']
 socialok=minpeer>64
 rc=dict(id=route['id'],onePixelSamples=len(pts),collisionFailures=len(fail),headFrameFailures=len(headfail),minimumOtherPeerDistance=minpeer,nearestOtherPeer=nearest,socialAcquisitionClear=socialok)
 routechecks.append(rc)
 if fail:issues.append(['route-collision',route['id'],fail[:12]])
 if headfail:issues.append(['route-head',route['id'],headfail[:8]])
 if not socialok:issues.append(['route-social',route['id'],minpeer,nearest])
# Real one-pixel blocked contact sets the expected workstation facing.
for q in M['anchors']:
 if q.get('contactDirection'):
  dx,dy={'south':(0,1),'north':(0,-1),'east':(1,0),'west':(-1,0)}[q['contactDirection']]
  contact=not free(q['x']+dx,q['y']+dy)
  contacts.append(dict(id=q['id'],direction=q['contactDirection'],blockedOnePixelContact=contact))
  if not contact:issues.append(['contact-not-blocked',q['id']])
# Source-derived64px acquire/96px retain state machine for each intended service pair.
byid={q['id']:q for q in M['anchors']}
for route in M['routes']:
 if route.get('intendedPartner'):
  peer=byid[route['intendedPartner']];active=False;acquired=False
  for x,y in pixels(route['points']):
   dist=math.hypot(peer['x']-x,peer['y']-y)
   if active and dist>96:active=False
   elif not active and dist<=64:active=True;acquired=True
  at_contact=active
  for x,y in pixels(route['returnPoints']):
   dist=math.hypot(peer['x']-x,peer['y']-y)
   if active and dist>96:active=False
   elif not active and dist<=64:active=True
  check=dict(route=route['id'],intendedPartner=peer['id'],acquired=acquired,activeAt48PixelContact=at_contact,releasedAfterReturn=not active)
  pairchecks.append(check)
  if not(acquired and at_contact and not active):issues.append(['pair-state',check])
# All12 frame masks at every stationary authored anchor.
anchorheads=[]
for q in M['anchors']:
 x,y=q['x'],q['y'];crop=fg[y-16:y-2,x-16:x+16]>32
 for i,head in enumerate(heads):
  n=int((head&crop).sum());anchorheads.append(dict(id=q['id'],frame=i,overlap=n))
  if n:issues.append(['anchor-head',q['id'],i,n])
report=dict(passAll=not issues,scope='Offline native-body geometry and actual opaque top14px Greg masks against fixed foreground. All12 animation frames per1px route sample; glass/shade not solid occluders. No live multiplayer claim.',anchorChecks=checks,contactChecks=contacts,receptionPairChecks=pairchecks,routeChecks=routechecks,allFrameHeadSamples=headchecks,anchorFrameHeadSamples=len(anchorheads),connectedBodyOrigins=len(seen),issues=issues,ordinaryWorkSeats=sum(q['kind']=='work-seat' for q in M['anchors']),receptionServices=sum(q['kind']=='reception-staff' for q in M['anchors']),spriteSha256=hashlib.sha256(Path('/workspace/shared/recovered-pre-island-package/runtime/assets/greg.png').read_bytes()).hexdigest())
(R/'verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
# Native overview uses actual unchanged Greg at all seats, as a review sheet.
a=Image.open(R/'office-base.png');sp=Image.open('/workspace/shared/recovered-pre-island-package/runtime/assets/greg.png')
for q in occ:
 row={'south':0,'west':1,'east':2,'north':3}.get(q['facing'],3)
 a.alpha_composite(sp.crop((32,row*32,64,row*32+32)),(q['x']-16,q['y']-16))
for n in ['foreground','glass','overhead-shade']:a.alpha_composite(Image.open(R/f'office-{n}.png'))
a.save(R/'office-occupied-review.png')
