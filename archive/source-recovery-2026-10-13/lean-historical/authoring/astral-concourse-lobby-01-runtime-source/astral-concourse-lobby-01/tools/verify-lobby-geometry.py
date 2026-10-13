from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from collections import deque
import numpy as np,json
R=Path(__file__).resolve().parents[1];V=R/'validation';V.mkdir(exist_ok=True)
m=json.loads((R/'map32/astral-concourse-lobby.tmj').read_text());h=json.loads((R/'source/collision-grid.json').read_text());g=np.array(h['grid'],np.uint8);W,H=1152,896
base=Image.new('RGBA',(W,H));fg=Image.new('RGBA',(W,H));atlas={}
for t in m['tilesets']:atlas[t['firstgid']]=(t,Image.open(R/'map32'/t['image']).convert('RGBA'))
for l in m['layers']:
 if l['type']!='tilelayer' or l.get('opacity')==0:continue
 out=fg if l['name']=='lobby-above' else base
 for i,v in enumerate(l['data']):
  if not v:continue
  key=max(k for k in atlas if k<=v);t,im=atlas[key];n=v-key;x=n%t['columns']*32;y=n//t['columns']*32
  out.alpha_composite(im.crop((x,y,x+32,y+32)),((i%m['width'])*32,(i//m['width'])*32))
for im,name in [(base,'lobby-base'),(fg,'lobby-above')]:assert ImageChops.difference(im,Image.open(R/'assets'/f'{name}.png')).getbbox() is None
empty=Image.alpha_composite(base,fg);empty.save(R/'review/lobby-runtime-empty-native.png')
reach=np.zeros_like(g,bool);q=deque([(h['start'][0]//32,h['start'][1]//32)])
while q:
 x,y=q.popleft()
 if not(0<=x<36 and 0<=y<28)or g[y,x]or reach[y,x]:continue
 reach[y,x]=True;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16)
clear=((ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa])==0)&(X>=8)&(X+8<=W)&(Y+16<=H)&reach[Y//32,X//32]
sheet=np.asarray(Image.open(R/'references/greg-reference.png'));head=np.zeros((14,32),bool)
for r in range(4):
 for c in range(3):head|=sheet[r*32:r*32+14,c*32:c*32+32,3]>32
foreground=np.asarray(fg)[:,:,3]>32;danger=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy)
 danger[y0:y1,x0:x1]|=foreground[y0+dy:y1+dy,x0+dx:x1+dx]
bad=clear&danger;(V/'head-danger.bin').write_bytes(danger.tobytes())
rows=[]
for p in h['landmarks']:
 x,y=p['x'],p['y'];rows.append({'id':p['id'],'bodyClear':bool(clear[y,x]),'headClear':not bool(danger[y,x]),'reachable':bool(reach[y//32,x//32])})
x,y,w,ht=h['startRect'];spawns=[(xx,yy)for yy in range(y,y+ht+1)for xx in range(x,x+w+1)]
safe=[bool(clear[yy,xx])and not danger[yy,xx]for xx,yy in spawns]
fringe=[(xx,yy)for yy in range(y,y+ht+2)for xx in range(x,x+w+2)if xx>x+w or yy>y+ht]
safe_fringe=[bool(clear[yy,xx])and not danger[yy,xx]for xx,yy in fringe]
unreachable=[(int(x),int(y))for y,x in np.argwhere((g==0)&~reach)]
report={'scope':'Compiled native32 tiles; source-matched 16x16 body at x±8,y..y+16. Union of upper14px of all12 native32 Woka frames. Every reachable integer body-clear placement. Not live engine/render/network verification.','walkableCells':int((g==0).sum()),'reachableCells':int(reach.sum()),'unreachableCells':unreachable,'bodyClearReachablePlacements':int(clear.sum()),'headConflicts':int(bad.sum()),'defaultWamZeroInsetIntegerSpawns':len(spawns),'safeDefaultWamSpawns':sum(safe),'landmarks':rows,'exactCompiledLayers':True}
report['conservativeFloatingPointFringePositions']=len(fringe)
report['safeFloatingPointFringePositions']=sum(safe_fringe)
report['allPass']=bool(not unreachable and not bad.any()and all(safe)and all(safe_fringe)and all(p['bodyClear']and p['headClear']and p['reachable']for p in rows))
(V/'geometry.json').write_text(json.dumps(report,indent=2)+'\n')
shade=Image.new('RGBA',(W,H));d=ImageDraw.Draw(shade)
for yy,xx in np.argwhere(g):d.rectangle((int(xx)*32,int(yy)*32,int(xx+1)*32-1,int(yy+1)*32-1),fill=(230,35,55,100))
for p in h['landmarks']:d.ellipse((p['x']-4,p['y']-4,p['x']+4,p['y']+4),fill=(64,255,184,255))
Image.alpha_composite(empty,shade).save(R/'review/lobby-collision-native.png')
occupied=base.copy();sheetim=Image.open(R/'references/greg-reference.png').convert('RGBA')
for n,xx,yy,frame in [('arrival',576,736,10),('reception',496,656,4),('crossroads',688,432,4),('west-social',288,304,10),('east-social',864,304,10),('flagship',576,272,10)]:
 sx=frame%3*32;sy=frame//3*32;occupied.alpha_composite(sheetim.crop((sx,sy,sx+32,sy+32)),(xx-16,yy-16))
occupied.alpha_composite(fg);occupied.save(R/'review/lobby-runtime-occupied-native.png')
print(json.dumps(report,indent=2));assert report['allPass']
