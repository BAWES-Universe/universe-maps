from pathlib import Path
import json,hashlib
from collections import deque,Counter
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'source';V=R/'validation';V.mkdir(exist_ok=True)
l=json.loads((S/'layout.json').read_text());g=np.array(json.loads((S/'collision-grid.json').read_text())['grid']);q=np.array(json.loads((S/'quiet-grid.json').read_text())['grid']);wam=json.loads((R/'map32/conference.wam').read_text());errors=[]
def body(p):
 x,y=p;x0=int((x-8)//32);x1=int((x+8-1e-7)//32);y0=int(y//32);y1=int((y+16-1e-7)//32)
 return bool(np.any(g[y0:y1+1,x0:x1+1]))
def roles(p):
 x,y=p;y+=16;return[a['id']for a in wam['areas']if a['x']<=x<=a['x']+a['width']and a['y']<=y<=a['y']+a['height']]
for a in l['seats']+l['social']+l['landmarks']:
 if body(a['anchor']):errors.append({'id':a['id'],'issue':'blocked anchor','anchor':a['anchor']})
 rs=roles(a['anchor'])
 expected = ('lantern-'+a['room']+'-audience') if a.get('kind')=='audience' else a.get('room') if a.get('kind')=='group' else ('lantern-'+a['id'].split('-')[0]+'-podium') if a.get('kind')=='speaker' else None
 expected=a.get('expectedRole') or expected
 if (expected and rs!=[expected])or(not expected and rs):errors.append({'id':a['id'],'issue':'wrong role','actual':rs,'expected':expected})
start=l['start'];stack=deque([(start[0]//32,start[1]//32)]);seen=set(stack)
while stack:
 x,y=stack.popleft()
 for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
  z=(x+dx,y+dy)
  if 0<=z[0]<g.shape[1]and 0<=z[1]<g.shape[0]and not g[z[1],z[0]]and z not in seen:seen.add(z);stack.append(z)
if len(seen)!=int((g==0).sum()):errors.append({'issue':'disconnected open cells','count':int((g==0).sum())-len(seen)})
# Full avatar-head occlusion scan, using the union of all12 unchanged native frames and alpha>32.
above=np.array(Image.open(R/'assets/runtime-above.png').convert('RGBA'))[:,:,3]>32;greg=np.array(Image.open(R/'assets/greg-reference.png').convert('RGBA'));mask=np.zeros((14,32),bool)
for i in range(12):mask|=greg[(i//3)*32:(i//3)*32+14,(i%3)*32:(i%3+1)*32,3]>32
H,W=above.shape;danger=np.zeros((H,W),bool)
for yy,xx in zip(*np.where(mask)):
 dy=yy-16;dx=xx-16;y0=max(0,-dy);y1=min(H,H-dy);x0=max(0,-dx);x1=min(W,W-dx);danger[y0:y1,x0:x1]|=above[y0+dy:y1+dy,x0+dx:x1+dx]
clear=np.ones((H,W),bool)
# A native body spans at most2x2 cells. Guard map bounds explicitly.
for dy in [0,15]:
 for dx in [-8,7]:
  ys=np.clip((np.arange(H)+dy)//32,0,g.shape[0]-1);xs=np.clip((np.arange(W)+dx)//32,0,g.shape[1]-1);clear&=g[ys[:,None],xs[None,:]]==0
clear[:,:8]=False;clear[:,W-7:]=False;clear[H-15:]=False
unsafe=np.argwhere(danger&clear);danger.astype(np.uint8).tofile(V/'head-danger.bin')
if len(unsafe):errors.append({'issue':'head overlaps','positions':len(unsafe),'examples':[[int(x),int(y)]for y,x in unsafe[:30]]})
result={'errors':errors,'pass':not errors,'connectedOpenCells':len(seen),'totalOpenCells':int((g==0).sum()),'hallSeats':len(l['seats']),'socialSeats':len(l['social']),'anchors':len(l['seats']+l['social']+l['landmarks']),'quietCells':int(q.sum()),'bodyClearPlacements':int(clear.sum()),'unsafeHeadPlacements':len(unsafe),'scope':'Offline geometry/role/pixel-mask check. Source route and live media acceptance separate.'};(V/'static-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if not errors else 1)
