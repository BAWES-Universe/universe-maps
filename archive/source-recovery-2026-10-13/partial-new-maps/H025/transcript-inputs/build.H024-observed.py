from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,collections,numpy as np
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/design.json').read_text());W,H=D['world'];C,N=W//32,H//32
for v in ['map32','review','validation']:(R/v).mkdir(exist_ok=True)
def js(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def props(**v):return [dict(name=k,type='bool'if isinstance(a,bool)else'int'if isinstance(a,int)else'string',value=a)for k,a in v.items()]
base=Image.new('RGBA',(W,H));above=Image.new('RGBA',(W,H));g=np.ones((N,C),np.uint8);rooms=[];seats=[];anchors=[];neg=[]
for d in D['rooms']:
 ox,oy=d['offset'];im=Image.open(R/'art/masters'/d['art']).convert('RGBA');assert im.size==(1536,1024);base.paste(im,(ox,oy));m=Image.new('L',im.size);dr=ImageDraw.Draw(m)
 for p in d['walkPolygons']:dr.polygon([tuple(a)for a in p],fill=255)
 for p in d['solidRects']:dr.rectangle(p,fill=0)
 for p in d.get('solidPolygons',[]):dr.polygon([tuple(q)for q in p],fill=0)
 a=np.asarray(m);gg=np.ones((32,48),np.uint8)
 for y in range(32):
  for x in range(48):gg[y,x]=int((a[y*32:(y+1)*32,x*32:(x+1)*32]>0).mean()<d.get('walkCoverageRequired',.51))
 # Fully traced physical-footprint masks reserve every touched native32 cell.
 hard=Image.new('L',im.size);hd=ImageDraw.Draw(hard)
 for poly in d.get('fullFixturePolygons',[]):hd.polygon([tuple(v)for v in poly],fill=255)
 ha=np.asarray(hard)
 for y in range(32):
  for x in range(48):
   if ha[y*32:y*32+32,x*32:x*32+32].any():gg[y,x]=1
 for x,y in d['openCells']:gg[y,x]=0
 for x,y in d['blockedCells']:gg[y,x]=1
 g[oy//32:oy//32+32,ox//32:ox//32+48]=gg
 ss=[];aa=[]
 for s in d['seats']:
  v={**s,'room':d['id'],'anchor':[s['anchor'][0]+ox,s['anchor'][1]+oy],'floorClick':[s['anchor'][0]+ox,s['anchor'][1]+oy+16],'cushionBounds':[s['cushionBounds'][0]+ox,s['cushionBounds'][1]+oy,s['cushionBounds'][2]+ox,s['cushionBounds'][3]+oy],'kind':'unchanged native32 standing frame at visual seat; no automatic sitting/facing'};seats.append(v);ss.append(v)
 for a in d['anchors']:
  v={**a,'room':d['id'],'anchor':[a['anchor'][0]+ox,a['anchor'][1]+oy],'floorClick':[a['anchor'][0]+ox,a['anchor'][1]+oy+16]};anchors.append(v);aa.append(v)
 for q in d['fixtureNegatives']:neg.append({**q,'room':d['id'],'point':[q['point'][0]+ox,q['point'][1]+oy]})
 fm=Image.new('L',im.size);dr=ImageDraw.Draw(fm)
 for p in d['foregroundPolygons']:dr.polygon([tuple(a)for a in p],fill=255)
 fg=im.copy();fg.putalpha(fm);above.paste(fg,(ox,oy));rooms.append(dict(id=d['id'],bounds=[ox,oy,1536,1024],spawn=[d['spawn'][0]+ox,d['spawn'][1]+oy],seats=ss,anchors=aa,fixtureNegatives=[n for n in neg if n['room']==d['id']]))
interactive={s['id']:dict(x=s['anchor'][0],y=s['anchor'][1],radius=s.get('radius',28),room=s['room'])for s in anchors if'id'in s}
for a,b in D['doors']:interactive[a]['to']=b;interactive[b]['to']=a;interactive[a]['action']='Enter lookout';interactive[b]['action']='Return to causeway'
layout=dict(id=D['id'],title=D['title'],world=[W,H],spawn=rooms[0]['spawn'],collision=g.tolist(),rooms=rooms,seats=seats,anchors=anchors,interactive=interactive,doors=D['doors'],stateLayers=D['stateLayers']);js(R/'source/layout.json',layout)
# Opaque ground is retained beneath genuine foreground surfaces, avoiding complementary alpha holes.
overlays={}
for spec in D['overlays']:
 im=Image.open(R/'art/masters'/spec['art']).convert('RGBA');layer=Image.new('RGBA',(W,H));rect=spec['rect'];ox,oy=spec['offset'];layer.paste(im.crop(rect),(rect[0]+ox,rect[1]+oy));overlays[spec['name']]=layer
sets=[];layers=[];gid=1
def pack(name,im,visible=True):
 global gid
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
 layers.append(dict(name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=visible,opacity=1,data=data));gid+=len(tiles)
pack('ground-and-architecture',base)
for k,im in overlays.items():pack(k,im,False)
layers.append(dict(name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]));pack('foreground',above)
Image.new('RGBA',(32,32)).save(R/'map32/logic.png');sets.append(dict(firstgid=gid,name='collision',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,dict(name='collision',type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=0,data=[gid if v else 0 for v in g.flat]));gid+=1
sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1));quiet=[0]*(C*N)
for x0,y0,x1,y1 in D['silentRects']:
 for y in range(y0//32,y1//32):
  for x in range(x0//32,x1//32):quiet[y*C+x]=gid
layers.insert(2,dict(name='quiet-arrival',type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=0,data=quiet,properties=props(silent=True)))
sx,sy=layout['spawn'];objs=[dict(id=1,name='start',type='area',**{'class':'area'},x=sx-8,y=sy-8,width=16,height=16,visible=True,rotation=0,properties=props(start=True))]
for i,(k,a)in enumerate(interactive.items(),2):objs.append(dict(id=i,name='causeway-popup-'+k,type='',x=a['x']-160,y=a['y']-164,width=320,height=144,visible=True,rotation=0))
layers.append(dict(name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=objs))
for i,l in enumerate(layers):l['id']=i+1
m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=C,height=N,tilewidth=32,tileheight=32,nextlayerid=len(layers)+1,nextobjectid=len(objs)+1,layers=layers,tilesets=sets,properties=props(name=D['title'],script='causeway.js',wokaScale=1,status='Authored pilot; live verification and publication pending'))
js(R/'map32/map.tmj',m);js(R/'map32/map.wam',dict(version='2.0.0',mapUrl='./map.tmj',entities={},entityCollections=[],areas=[]));(R/'map32/causeway.js').write_text('globalThis.CausewayLayout = '+json.dumps({'anchors':interactive},separators=(',',':'))+';\n'+(R/'source/controller.js').read_text())
# Decode actual emitted TMJ and PNG atlases.
at={s['image']:Image.open(R/'map32'/s['image']).convert('RGBA')for s in sets};dec={}
for l in m['layers']:
 if l['type']!='tilelayer'or l.get('opacity')==0:continue
 im=Image.new('RGBA',(W,H))
 for j,v in enumerate(l['data']):
  if not v:continue
  s=max((s for s in sets if s['firstgid']<=v),key=lambda s:s['firstgid']);n=v-s['firstgid'];x=n%s['columns']*32;y=n//s['columns']*32;im.paste(at[s['image']].crop((x,y,x+32,y+32)),(j%C*32,j//C*32))
 dec[l['name']]=im
empty=Image.alpha_composite(dec['ground-and-architecture'],dec['foreground']);assert empty.tobytes()==base.tobytes();dec['ground-and-architecture'].save(R/'review/decoded-ground.png');dec['foreground'].save(R/'review/decoded-foreground.png')
complete=dec['ground-and-architecture'].copy()
for name in D['completedLayers']:complete=Image.alpha_composite(complete,dec[name])
complete=Image.alpha_composite(complete,dec['foreground']);
for rr in rooms:
 x,y,w,h=rr['bounds'];empty.crop((x,y,x+w,y+h)).save(R/'review'/f"{rr['id']}-decoded-empty.png")
 complete.crop((x,y,x+w,y+h)).save(R/'review'/f"{rr['id']}-decoded-complete.png")
# Native body origin admissibility and true foreground head conflicts.
b=g.repeat(32,0).repeat(32,1).astype(bool);ii=np.pad(b.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(json.loads((R/'source/native-head-union.json').read_text())['mask'],bool);unsafe=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
f=np.asarray(above)[:,:,3]>0;checks={'scope':'Author source checks, not independent/live','decodedExact':True,'opaqueBase':base.getchannel('A').getextrema()==(255,255),'foregroundPixels':int(f.sum()),'headConflicts':int((f&unsafe).sum()),'headConflictPixels':np.argwhere(f&unsafe)[:50].tolist(),'anchors':[dict(name=s['name'],bodyClear=bool(clear[s['anchor'][1],s['anchor'][0]]))for s in seats+anchors],'fixtureNegatives':[dict(**p,blocked=bool(g[p['point'][1]//32,p['point'][0]//32]))for p in neg]}
js(R/'validation/geometry.json',checks)
over=Image.new('RGBA',(W,H));dr=ImageDraw.Draw(over)
for y in range(N):
 for x in range(C):
  if g[y,x]:dr.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(220,16,32,95))
dbg=Image.alpha_composite(empty,over);dr=ImageDraw.Draw(dbg)
for s in seats+anchors:
 x,y=s['anchor'];dr.rectangle((x-8,y,x+7,y+15),outline='#00ffff');dr.text((x+10,y-8),s['name'],fill='white')
for rr in rooms:
 x,y,w,h=rr['bounds'];dbg.crop((x,y,x+w,y+h)).save(R/'review'/f"{rr['id']}-collision.png")
js(R/'validation/state-layers.json',dict(collisionInvariant=True,movementGuard='Intended state updates are cached while moving; only final changed layers are flushed after moving:false.',layers={k:{'pixels':int((np.asarray(v)[:,:,3]>0).sum()),'sha256':hashlib.sha256(v.tobytes()).hexdigest()}for k,v in overlays.items()}));print(json.dumps({**checks,'headConflictPixels':checks['headConflictPixels'][:4]},indent=2))

assert checks['decodedExact'] and checks['opaqueBase'] and checks['headConflicts']==0
assert all(a['bodyClear']for a in checks['anchors'])
assert all(a['blocked']for a in checks['fixtureNegatives'])
