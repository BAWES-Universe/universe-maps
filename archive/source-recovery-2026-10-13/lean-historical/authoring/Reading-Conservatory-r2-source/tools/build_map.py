from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,collections,hashlib
R=Path(__file__).resolve().parents[1];O=R/'candidate';T=32;C=24;N=16;W=768;H=512
for f in ['map32','source','review']:(O/f).mkdir(parents=True,exist_ok=True)
def js(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def props(**x):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in x.items()]
art=Image.open(R/'working/art-native.png').convert('RGBA');base=Image.open(R/'working/base.png').convert('RGBA');above=Image.open(R/'working/above.png').convert('RGBA')
g=np.ones((N,C),dtype=np.uint8)
for x,y,w,h in [(5,5,14,6),(2,5,4,2),(18,5,4,1),(19,6,3,1),(11,11,2,5)]:g[y:y+h,x:x+w]=0
# Large library counter, table footprints and rear chair bases are solid.
g[5,9:15]=1
for x in [7,9,14,16]:g[6,x]=1;g[9,x]=1
for x in [8,15]:g[7:9,x]=1
g[6,20]=1
# Reassign only foreground pixels that cannot obscure any admitted native head.
b=g.repeat(T,0).repeat(T,1).astype(bool);ii=np.pad(b.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(b.shape);xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(json.load(open(R/'source-assets/native-head-union.json'))['mask'],bool);unsafe=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
raw_fg=np.array(above)[:,:,3]>0;safe_fg=raw_fg&~unsafe;full=np.array(art);hi=np.zeros_like(full);hi[safe_fg]=full[safe_fg];lo=full.copy();lo[safe_fg]=0;above=Image.fromarray(hi);base=Image.fromarray(lo)
assert Image.alpha_composite(base,above).tobytes()==art.tobytes()
spawn=[12,14];seats=[];anchors=[]
for group,xs in [('West',[244,300]),('East',[468,524])]:
 for row,y,d in [('north',224,'south'),('south',271,'north')]:
  for num,x in enumerate(xs,1):seats.append(dict(name=f'{group} reading {row} {num}',anchor=[x,y],floorClick=[x,y+16],direction=d,kind='walk-to chair; native standing idle only'))
for name,x,d in [('Mentorship west',616,'east'),('Mentorship east',696,'west')]:seats.append(dict(name=name,anchor=[x,192],floorClick=[x,208],direction=d,kind='walk-to chair; native standing idle only'))
for name,x,y in [('West standing reading desk',84,160),('East standing reading desk',140,160),('Quiet study interior',112,207),('West bookshelf approach',176,271),('East bookshelf approach',592,271),('Central aisle',376,271),('South cross aisle west',208,335),('South cross aisle east',560,335),('Inside entrance',376,335),('Doorway',376,367),('Outer landing',376,399),('Arrival',400,463)]:anchors.append(dict(name=name,anchor=[x,y],floorClick=[x,y+16],cell=[x//32,y//32],kind='walk-to approach'))
layout=dict(title='Reading Conservatory',version='functional candidate r2',dimensions=[C,N],spawn=spawn,collision=g.tolist(),seats=seats,anchors=anchors,zones=[dict(name='West reading conversation',rect=[223,223,97,65]),dict(name='East reading conversation',rect=[447,223,97,65]),dict(name='Mentorship conversation',rect=[607,175,98,50])],notes='Ten manually faced native idle chair anchors. No sitting pose, automatic facing or snapping. Three optional distinct native LiveKit conversation areas; actual media services are untested. All scripts map-only; no engine change.')
js(O/'source/layout.json',layout)
areas=[]
for i,z in enumerate(layout['zones']):
 x,y,w,h=z['rect'];rid=f'reading-conservatory-r2-group-{i+1}'
 areas.append(dict(id=rid,name=z['name'],x=x,y=y,width=w,height=h,visible=True,properties=[dict(id=rid+'-room',type='livekitRoomProperty',roomName=rid,livekitRoomConfig=dict(startWithAudioMuted=False,startWithVideoMuted=True,disableChat=False))]))
js(O/'map32/map.wam',dict(version='2.0.0',mapUrl='./map.tmj',entities={},entityCollections=[],areas=areas))
sets=[];layers=[];gid=1
def layer(name,data,opacity=1):return dict(name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=data)
for name,im in [('architecture-and-furniture',base),('foreground',above)]:
 if name=='foreground':layers.append(dict(name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 tiles=[];lookup={};data=[]
 for y in range(N):
  for x in range(C):
   t=im.crop((x*T,y*T,(x+1)*T,(y+1)*T));k=t.tobytes()
   if not t.getbbox():data.append(0);continue
   if k not in lookup:lookup[k]=len(tiles);tiles.append(t)
   data.append(gid+lookup[k])
 cols=min(24,len(tiles));atlas=Image.new('RGBA',(cols*T,math.ceil(len(tiles)/cols)*T))
 for j,t in enumerate(tiles):atlas.paste(t,(j%cols*T,j//cols*T))
 fn=name+'.png';atlas.save(O/'map32'/fn);sets.append(dict(firstgid=gid,name=name,image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(tiles)));layers.append(layer(name,data));gid+=len(tiles)
Image.new('RGBA',(32,32)).save(O/'map32/logic.png')
sets.append(dict(firstgid=gid,name='collision',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,layer('collision',[gid if v else 0 for row in g for v in row],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1));quiet=[0]*(C*N);quiet[spawn[1]*C+spawn[0]]=gid;ql=layer('quiet-arrival',quiet,0);ql['properties']=props(silent=True);layers.insert(2,ql)
start=dict(id=1,name='start',type='area',**{'class':'area'},x=spawn[0]*T,y=spawn[1]*T,width=T,height=T,rotation=0,visible=True,properties=props(start=True));layers.append(dict(name='map-areas',type='objectgroup',x=0,y=0,opacity=1,visible=True,objects=[start],draworder='topdown'))
for i,l in enumerate(layers):l['id']=i+1
m=dict(compressionlevel=-1,width=C,height=N,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tilewidth=T,tileheight=T,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=2,backgroundcolor='#344834',properties=props(name='Reading Conservatory',category='Knowledge and Social',wokaScale=1,status='Unpublished functional candidate; not live tested'),layers=layers,tilesets=sets);js(O/'map32/map.tmj',m)
# Actual atlas round-trip, no preview shortcuts.
dec=[]
for l in m['layers']:
 if l['type']!='tilelayer' or l.get('opacity')==0:continue
 im=Image.new('RGBA',(W,H))
 for j,v in enumerate(l['data']):
  if not v:continue
  s=max((s for s in m['tilesets'] if s['firstgid']<=v),key=lambda s:s['firstgid']);at=Image.open(O/'map32'/s['image']).convert('RGBA');n=v-s['firstgid'];x=n%s['columns']*T;y=n//s['columns']*T;im.paste(at.crop((x,y,x+T,y+T)),(j%C*T,j//C*T))
 dec.append(im)
assert Image.alpha_composite(*dec).tobytes()==art.tobytes();art.save(O/'review/empty-native.png');dec[0].save(O/'review/base-native.png');dec[1].save(O/'review/foreground-native.png')
# Authentic varied frames are retained as compiled full-scene review inputs.
actor_meta=json.load(open(R/'source-assets/ACTOR-PROVENANCE.json'))['actors']
overlays={d:Image.open(R/'source-assets'/f'proof-actors-{d}.png').convert('RGBA') for d in ['south','west','east','north']}
occ=dec[0].copy();actors=[]
for seat,meta in zip(seats,actor_meta):
 assert seat['anchor']==meta['anchor'] and seat['name']==meta['seat']
 x,y=seat['anchor'];d=seat['direction'];fr=overlays[d].crop((x-16,y-16,x+16,y+16));assert hashlib.sha256(fr.tobytes()).hexdigest()==meta['frames'][d]['rgba_sha256']
 occ.alpha_composite(fr,(x-16,y-16));actors.append(dict(seat=seat['name'],anchor=seat['anchor'],direction=d,source=meta,exact_frame_rgba_sha256=hashlib.sha256(fr.tobytes()).hexdigest()))
occ.alpha_composite(dec[1]);occ.save(O/'review/manually-faced-native.png');occ.save(O/'review/occupied-native.png');js(O/'source/MANUALLY-FACED-PROOF.json',actors)
# Body-space domain and all actual foreground intersections, not only anchors.
b=g.repeat(T,0).repeat(T,1).astype(bool);ii=np.pad(b.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(b.shape);xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(json.load(open(R/'source-assets/native-head-union.json'))['mask'],bool);fm=np.array(dec[1])[:,:,3]>0;conf=[]
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);z=clear[y0:y1,x0:x1]&fm[y0+dy:y1+dy,x0+dx:x1+dx]
 if z.any():
  zy,zx=np.argwhere(z)[0];conf.append([int(zx+x0),int(zy+y0),dx,dy,int(z.sum())])
reach={tuple(spawn)};q=collections.deque(reach)
while q:
 x,y=q.popleft()
 for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=nx<C and 0<=ny<N and not g[ny,nx] and (nx,ny) not in reach:reach.add((nx,ny));q.append((nx,ny))
checks={'connected_cells':len(reach),'open_cells':int((g==0).sum()),'all_open_cells_connected':len(reach)==int((g==0).sum()),'body_clear_positions':int(clear.sum()),'head_intersections':sum(x[-1] for x in conf),'head_examples':conf[:8],'anchor_checks':[dict(name=a['name'],clear=bool(clear[a['anchor'][1],a['anchor'][0]]),connected=(a['anchor'][0]//32,a['anchor'][1]//32) in reach) for a in seats+anchors],'source_art_roundtrip':True,'foreground_pixels_retained':int(safe_fg.sum()),'foreground_pixels_moved_to_background':int((raw_fg&unsafe).sum()),'native_routes':'not run yet','live_runtime':'not tested'};js(O/'STATIC-CHECKS.json',checks)
dbg=art.copy();d=ImageDraw.Draw(dbg,'RGBA')
for y in range(N):
 for x in range(C):
  if g[y,x]:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(180,20,40,100))
  d.rectangle((x*32,y*32,x*32+31,y*32+31),outline=(0,0,0,75))
for a in seats+anchors:
 x,y=a['anchor'];d.rectangle((x-8,y,x+7,y+15),outline=(0,250,255,255));d.text((x-6,y-12),str((x//32,y//32)),fill=(255,255,255,255))
dbg.save(O/'review/collision-diagnostic.png');print(json.dumps(checks,indent=2))

# Frozen native trace input is retained for offline proof reconstruction, with binding checks.
for name,target in [('frozen-seat-route-traces.json','SEAT-ROUTE-TRACES.json'),('frozen-spawn-seat-arrivals.json','SPAWN-SEAT-ARRIVALS.json')]:
 p=R/'source-assets'/name
 if p.exists():
  j=json.load(open(p))
  for fn,h in j['inputHashes'].items():assert hashlib.sha256((O/fn).read_bytes()).hexdigest()==h,(fn,'stale native proof input')
  js(O/'source'/target,j)
(O/'GUIDE.md').write_bytes((R/'GUIDE.md').read_bytes())
(O/'map32/README.md').write_bytes((R/'RUNTIME-README.md').read_bytes())
