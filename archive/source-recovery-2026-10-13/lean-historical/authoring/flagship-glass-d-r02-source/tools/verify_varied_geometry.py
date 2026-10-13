from pathlib import Path
from PIL import Image,ImageDraw
from collections import deque
import numpy as np,json
R=Path(__file__).resolve().parents[1];assert len(list((R/'source/wokas').glob('woka-proof-*.png')))==8, 'Optional licensed Pipoya fixtures are excluded from delivery; restore authorized sheets per source/wokas/WOKA-PROOF.json before this preview/varied check';V=R/'validation';m=json.loads((R/'map32/grand-auditorium.tmj').read_text());h=json.loads((R/'source/collision-grid.json').read_text());g=np.array(h['grid'],np.uint8);W=m['width']*32;H=m['height']*32;fg=np.asarray(Image.open(R/'assets/runtime-above.png'))[:,:,3]>32;sp=np.asarray(Image.open(R/'assets/greg-reference.png'));head=np.zeros((14,32),bool)
for sheet in [sp]+[np.asarray(Image.open(p).convert('RGBA')) for p in (R/'source/wokas').glob('woka-proof-*.png')]:
 for r in range(4):
  for c in range(3):head|=sheet[r*32:r*32+14,c*32:c*32+32,3]>32
reach=np.zeros_like(g,bool);queue=deque([(h['start'][0]//32,h['start'][1]//32)])
while queue:
 x,y=queue.popleft()
 if not(0<=x<g.shape[1] and 0<=y<g.shape[0])or g[y,x]or reach[y,x]:continue
 reach[y,x]=1;queue.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);s=ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa];clear=(s==0)&(X>=8)&(X+8<=W)&(Y+16<=H)&reach[Y//32,X//32];danger=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
bad=clear&danger;yy,xx=np.where(bad);seats=json.loads((R/'source/seats.json').read_text());allanchors=[];quiet=np.array(json.loads((R/'source/quiet-grid.json').read_text())['grid']);
for q in seats+h['socialAnchors']+h['landmarks']:
 x,y=q['x'],q['y'];allanchors.append({'id':q['id'],'bodyClear':bool(clear[y,x]),'headClear':not bool(danger[y,x]),'reachable':bool(reach[y//32,x//32]),'silent':bool(quiet[y//32,x//32])})
wam=json.loads((R/'map32/grand-auditorium.wam').read_text());wa=next(a for a in wam['areas']if any(p.get('type')=='start'and p.get('isDefault')for p in a['properties']));wx,wy,ww,wh=[wa[k]for k in['x','y','width','height']];spawns=[bool(clear[y,x])and not danger[y,x]and bool(quiet[y//32,x//32])for y in range(wy,wy+wh+2)for x in range(wx,wx+ww+2)];badanchors=[q for q in allanchors if not q['bodyClear']or not q['headClear']or not q['reachable']];socialIds={q['id']for q in h['socialAnchors']};socialquiet=[q for q in allanchors if q['id']in socialIds and q['silent']]
report={'scope':'Permanent foreground only; dynamic shell masks are tested by route/state audit. Every reachable integer body-clear position,16x16 native body x-8..x+8/y..y+16; union of all12 frames from Greg32 and eight varied original32 Woka sheets, upper14px alpha>32. Source/static test, not live rendering.','world':[W,H],'walkableCells':int((g==0).sum()),'reachableCells':int(reach.sum()),'unreachableWalkableCells':int(((g==0)&~reach).sum()),'bodyClearReachablePlacements':int(clear.sum()),'headConflictPlacements':int(bad.sum()),'firstHeadConflicts':[[int(x),int(y)]for x,y in zip(xx[:30],yy[:30])],'anchorCount':len(allanchors),'badAnchors':badanchors,'socialAnchorsInSilence':socialquiet,'conservativeFullWamSpawnCount':len(spawns),'safeAndSilentSpawns':sum(spawns),'allPass':not bad.any()and not badanchors and not socialquiet and all(spawns)and not((g==0)&~reach).any(),'anchors':allanchors};(V/'geometry-varied.json').write_text(json.dumps(report,indent=2)+'\n');(V/'head-danger-varied.bin').write_bytes(danger.tobytes())
im=Image.open(R/'review/runtime-empty-native.png').convert('RGBA');shade=Image.new('RGBA',(W,H));d=ImageDraw.Draw(shade)
for y,x in np.argwhere(g):d.rectangle((int(x)*32,int(y)*32,int(x+1)*32-1,int(y+1)*32-1),fill=(220,24,54,95))
for q in seats+h['socialAnchors']:d.ellipse((q['x']-3,q['y']-3,q['x']+3,q['y']+3),fill=(70,255,187,230))
for x,y in zip(xx,yy):d.point((int(x),int(y)),fill=(255,255,0,255))
im.alpha_composite(shade);im.save(Path('/tmp/flagship-glass-r02-varied-collision.png'));print(json.dumps({k:v for k,v in report.items()if k!='anchors'},indent=2));
if not report['allPass']:raise SystemExit(1)
