from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,collections,numpy as np,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1]; D=json.load(open(R/'source/design.json')); W,H=D['world']; C,N=W//32,H//32
for d in ['map32','review','validation']:(R/d).mkdir(exist_ok=True)
def js(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def props(**v):return [dict(name=k,type='bool' if isinstance(x,bool) else 'int' if isinstance(x,int) else 'string',value=x) for k,x in v.items()]
art=Image.open(R/'source/generated-art.png').convert('RGBA');assert art.size==(W,H)
chair_mask=Image.new('L',(W,H))
if D.get('chairAsset'):
 master=Image.open(R/'source'/D['chairAsset']).convert('RGBA');box=master.getchannel('A').getbbox();chair=master if D.get('chairNative') else master.crop(box).resize((32,37),Image.Resampling.LANCZOS);chair.save(R/'source/chair-native.png')
 rail=Image.new('RGBA',chair.size);rail.paste(chair.crop((4,14,28,24)),(4,14));rail.save(R/'source/chair-rail-native.png')
 for seat in D['seats']:
  x,y=seat['anchor'];art.alpha_composite(chair,(x-16,y-12));chair_mask.paste(rail.getchannel('A'),(x-16,y-12))

mask=Image.new('L',(W,H));dm=ImageDraw.Draw(mask)
for poly in D['walkPolygons']:dm.polygon([tuple(p) for p in poly],fill=255)
for r in D['solidRects']:dm.rectangle(r,fill=0)
# Review-authored visible object footprints rasterized to native32 collision cells.
a=np.asarray(mask);g=np.ones((N,C),np.uint8)
for y in range(N):
 for x in range(C):
  g[y,x]=int((a[y*32:(y+1)*32,x*32:(x+1)*32]>0).mean()<.62)
for r in D.get('openCells',[]):
 x,y=r;g[y,x]=0
for r in D.get('blockedCells',[]):
 x,y=r;g[y,x]=1
spawn=D['spawn']; sx,sy=spawn
seats=[dict(**s,floorClick=[s['anchor'][0],s['anchor'][1]+16],kind='walk-to visual chair; unchanged native standing frame') for s in D['seats']]
anchors=[dict(**s,floorClick=[s['anchor'][0],s['anchor'][1]+16]) for s in D['anchors']]
layout=dict(title=D['title'],id=D['id'],world=[W,H],spawn=spawn,collision=g.tolist(),seats=seats,anchors=anchors,zones=D['zones']);js(R/'source/layout.json',layout)
b=g.repeat(32,0).repeat(32,1).astype(bool);ii=np.pad(b.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(json.load(open(R/'source/native-head-union.json'))['mask'],bool);unsafe=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
fm=Image.new('L',(W,H));d=ImageDraw.Draw(fm)
for r in D['foregroundRects']:d.rectangle(r,fill=255)
candidate=(np.asarray(fm)>0)|(np.asarray(chair_mask)>0);fg=candidate&~unsafe;full=np.array(art);hi=np.zeros_like(full);hi[fg]=full[fg];lo=full.copy();lo[fg]=0;base=Image.fromarray(lo);above=Image.fromarray(hi)
assert Image.alpha_composite(base,above).tobytes()==art.tobytes()
sets=[];layers=[];gid=1
for name,im in [('ground-and-architecture',base),('foreground',above)]:
 if name=='foreground':layers.append(dict(name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 tiles=[];lookup={};data=[]
 for y in range(N):
  for x in range(C):
   t=im.crop((x*32,y*32,x*32+32,y*32+32));k=t.tobytes()
   if not t.getchannel('A').getbbox():data.append(0);continue
   if k not in lookup:lookup[k]=len(tiles);tiles.append(t)
   data.append(gid+lookup[k])
 for page,start in enumerate(range(0,len(tiles),1024)):
  ts=tiles[start:start+1024];cols=min(32,len(ts));atlas=Image.new('RGBA',(cols*32,math.ceil(len(ts)/cols)*32))
  for i,t in enumerate(ts):atlas.paste(t,(i%cols*32,i//cols*32))
  fn=f'{name}-{page}.png';atlas.save(R/'map32'/fn);sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=cols,tilecount=len(ts)))
 layers.append(dict(name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=1,data=data));gid+=len(tiles)
Image.new('RGBA',(32,32)).save(R/'map32/logic.png')
sets.append(dict(firstgid=gid,name='collision',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,dict(name='collision',type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=0,data=[gid if v else 0 for v in g.flat]));gid+=1
sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1));quiet=[0]*(C*N);quiet[(sy//32)*C+sx//32]=gid;layers.insert(2,dict(name='quiet-arrival',type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=0,data=quiet,properties=props(silent=True)))
start=dict(id=1,name='start',type='area',**{'class':'area'},x=sx-16,y=sy-16,width=32,height=32,visible=True,rotation=0,properties=props(start=True))
layers.append(dict(name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[start]))
for i,l in enumerate(layers):l['id']=i+1
m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=C,height=N,tilewidth=32,tileheight=32,nextlayerid=len(layers)+1,nextobjectid=2,layers=layers,tilesets=sets,properties=props(name=D['title'],wokaScale=1,status='Local authorable candidate; independent, live and publication unverified'))
js(R/'map32/map.tmj',m)
areas=[dict(id=D['id']+'-zone-'+str(i+1),name=z['name'],x=z['rect'][0],y=z['rect'][1],width=z['rect'][2],height=z['rect'][3],visible=True,properties=[]) for i,z in enumerate(D['zones'])];js(R/'map32/map.wam',dict(version='2.0.0',mapUrl='./map.tmj',entities={},entityCollections=[],areas=areas))
# Decode the written TMJ and atlas pages, never substitute the source art.
dec=[];at={s['image']:Image.open(R/'map32'/s['image']).convert('RGBA') for s in sets}
for l in m['layers']:
 if l['type']!='tilelayer' or l.get('opacity')==0:continue
 im=Image.new('RGBA',(W,H))
 for j,v in enumerate(l['data']):
  if not v:continue
  s=max((s for s in sets if s['firstgid']<=v),key=lambda s:s['firstgid']);n=v-s['firstgid'];x=n%s['columns']*32;y=n//s['columns']*32;im.paste(at[s['image']].crop((x,y,x+32,y+32)),(j%C*32,j//C*32))
 dec.append(im)
empty=Image.alpha_composite(*dec);assert empty.tobytes()==art.tobytes();empty.save(R/'review/decoded-art.png');dec[0].save(R/'review/decoded-ground.png');dec[1].save(R/'review/decoded-foreground.png')
reach=set();q=collections.deque([(sx//32,sy//32)])
while q:
 x,y=q.popleft()
 if not(0<=x<C and 0<=y<N) or g[y,x] or (x,y) in reach:continue
 reach.add((x,y));q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
checks=dict(scope='Author checks; not independent or live',decodedExact=True,foregroundPixels=int(fg.sum()),semanticRailPixels=int((np.asarray(chair_mask)>32).sum()),semanticRailLost=int(((np.asarray(chair_mask)>32)&~fg).sum()),headConflicts=int((fg&unsafe).sum()),openCells=int((g==0).sum()),reachableCells=len(reach),unreachableCells=[[x,y] for y in range(N) for x in range(C) if g[y,x]==0 and (x,y) not in reach],anchors=[dict(name=s['name'],bodyClear=bool(clear[s['anchor'][1],s['anchor'][0]]),reachable=(s['anchor'][0]//32,s['anchor'][1]//32) in reach) for s in seats+anchors],spawnBodyClear=bool(clear[sy,sx]));js(R/'validation/geometry.json',checks)
dbg=empty.copy();d=ImageDraw.Draw(dbg,'RGBA')
for y in range(N):
 for x in range(C):
  if g[y,x]:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(200,20,40,95))
for s in seats+anchors:
 x,y=s['anchor'];d.rectangle((x-8,y,x+7,y+15),outline=(0,255,255,255));d.text((x,y-15),s['name'],fill='white')
dbg.save(R/'review/collision.png');print(json.dumps(checks,indent=2))
