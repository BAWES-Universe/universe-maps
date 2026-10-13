"""Exhaustive native body/head roof coverage, using actual compiled room extents."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];V=R/'validation';W,H=2560,1920
m=json.loads((R/'map32/grand-auditorium.tmj').read_text());areas={a['name']:a for l in m['layers']if l['type']=='objectgroup'for a in l.get('objects',[])}
g=np.array(json.loads((R/'source/collision-grid.json').read_text())['grid']);blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
sp=np.array(Image.open(R/'source/v03-greg-reference.png'));head=np.zeros((14,32),bool)
for r in range(4):
 for c in range(3):head|=sp[r*32:r*32+14,c*32:c*32+32,3]>32

def member(a):return(X>=a['x'])&(X<=a['x']+a['width'])&(Y+16>=a['y'])&(Y+16<=a['y']+a['height'])
def danger_for(fg):
 out=np.zeros((H,W),bool)
 for yy,xx in np.argwhere(head):
  dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);out[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
 return out
hall=member(areas['v04-hall-interior']);foyer=member(areas['v04-foyer-interior']);rows=[]
for name,inside in [('roof-auditorium-full',hall),('roof-foyer-full',hall|foyer)]:
 danger=danger_for(np.array(Image.open(R/'assets'/f'{name}.png'))[:,:,3]>32);bad=clear&danger&~inside;yy,xx=np.where(bad)
 rows.append(dict(asset=name,coveredBodyClearPlacements=int((clear&danger).sum()),outsideRevealConflicts=int(bad.sum()),firstConflicts=list(map(list,zip(xx[:20].tolist(),yy[:20].tolist())))))
above=np.array(Image.open(R/'assets/furniture-and-hall-above.png'))[:,:,3]>32;danger=danger_for(above);baseconflicts=int((clear&danger).sum());(V/'head-danger.bin').write_bytes(danger.tobytes())
cfg=json.loads((R/'source/runtime-layout.json').read_text());social=[dict(id=a['id'],hallFocus=bool(hall[a['y'],a['x']]),foyerReveal=bool(foyer[a['y'],a['x']]))for a in cfg['socialAnchors']]
report=dict(scope='Every native16x16 body-clear integer position; union of all12 Greg32 upper14px head masks. Areas use inclusive x,y+16. Source/static coverage, no live renderer or bridge timing claim.',bodyClearPlacements=int(clear.sum()),roofs=rows,furnitureHeadConflicts=baseconflicts,socialAnchors=social,allPass=all(r['outsideRevealConflicts']==0 for r in rows)and baseconflicts==0 and not any(a['hallFocus']for a in social),tmjSHA256=hashlib.sha256((R/'map32/grand-auditorium.tmj').read_bytes()).hexdigest())
(V/'roof-and-depth-coverage.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['allPass']
