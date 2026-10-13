from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,collections,itertools,numpy as np,os,shutil
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/design.json').read_text());W,H=D['world'];C,N=W//32,H//32
for name in ['runtime','review','validation']:(R/name).mkdir(exist_ok=True)
# Frozen PNGs may share storage. Detach writable generated outputs before saving; never alter a freeze in place.
for folder in ['runtime','review']:
 for p in (R/folder).rglob('*.png'):
  if p.stat().st_nlink>1:
   q=p.with_suffix('.detached.png');shutil.copy2(p,q);os.replace(q,p)
p=R/D['nativeArt']
if p.exists()and p.stat().st_nlink>1:
 q=p.with_suffix('.detached.png');shutil.copy2(p,q);os.replace(q,p)
def js(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def props(**values):return [dict(name=k,type='bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string',value=v) for k,v in values.items()]
art=Image.new('RGBA',(W,H),(255,255,255,255));art.alpha_composite(Image.open(R/D['art']).convert('RGBA').resize((1152,768),Image.Resampling.LANCZOS));art.alpha_composite(Image.open(R/'art/masters/pattern-room-r1.png').convert('RGBA').resize((768,768),Image.Resampling.LANCZOS),(1152,0))
stoolSheet=Image.open(R/'art/masters/stools-r1.png').convert('RGBA');stoolProof=[]
for i,(x,y,w,h)in enumerate(D['stoolPlacements']):
 b=([92,330,668,707],[923,350,1457,707])[i];piece=stoolSheet.crop(b);art.alpha_composite(piece.resize((w,h),Image.Resampling.LANCZOS),(x,y));stoolProof.append(dict(index=i,wholeBounds=b,placement=[x,y,w,h],originalAlpha=True))
art.save(R/D['nativeArt']);js(R/'validation/whole-stool-crops.json',dict(components=stoolProof,scope='Original built-in raster stools with original alpha, mechanically cropped to whole wooden stool including every foot.'))
g=np.ones((N,C),np.uint8)
for x0,y0,x1,y1 in D['openRects']:g[y0:y1+1,x0:x1+1]=0
for x,y in D['blockedCells']:g[y,x]=1
seats=[dict(**s,floorClick=[s['anchor'][0],s['anchor'][1]+16],kind='Unmodified native standing frame; no auto-sit/facing')for s in D['seats']];anchors=[dict(**a,floorClick=[a['anchor'][0],a['anchor'][1]+16])for a in D['anchors']]
layout=dict(id=D['id'],title=D['title'],world=[W,H],spawn=D['spawn'],collision=g.tolist(),rooms=D['rooms'],seats=seats,anchors=anchors,doors=D['doors'],scenicBoundaries=D['scenicBoundaries']);js(R/'source/layout.json',layout)
blocked=g.repeat(32,0).repeat(32,1).astype(bool);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(json.loads((R/'source/native-head-union.json').read_text())['mask'],bool);unsafe=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
mask=Image.new('L',(W,H));dm=ImageDraw.Draw(mask)
for poly in D['foregroundPolygons']:dm.polygon([tuple(p)for p in poly],fill=255)
candidate=np.asarray(mask)>0;fg=candidate&~unsafe;full=np.array(art);above=np.zeros_like(full);above[fg]=full[fg];above=Image.fromarray(above)
# Complete opaque authored ground remains beneath semantic above-floor furniture pixels.
base=art.copy();assert Image.alpha_composite(base,above).tobytes()==art.tobytes()
overlays={};formMeta=[]
sheet=Image.open(R/'art/masters/patterns-r1.png').convert('RGBA');specimens=[];cropProof=[]
boxes=[[30,128,373,474],[405,128,750,474],[783,128,1129,474],[1162,129,1510,474],[30,536,373,907],[405,536,750,907],[783,536,1129,907],[1162,536,1510,907]]
for i,b in enumerate(boxes):
 piece=sheet.crop(b);specimens.append(piece);cropProof.append(dict(index=i,wholeBounds=b,sourceSHA256=hashlib.sha256(piece.tobytes()).hexdigest()))
def placeAll(piece,boxes):
 im=Image.new('RGBA',(W,H))
 for x,y,w,h in boxes:im.alpha_composite(piece.resize((w,h),Image.Resampling.LANCZOS),(x,y))
 return im
# Exact same local bitmask has the same original sample on both shallow trays and the pattern table.
for i,piece in enumerate(specimens):
 name='wet-'+str(i);overlays[name]=placeAll(piece,[[200,339,111,60],[487,339,110,60],[1428,311,212,99]]);formMeta.append(dict(layer=name,mask=i,originalCell=i))
for i,piece in enumerate(specimens):
 name='print-'+str(i);overlays[name]=placeAll(piece,[[976,243,54,64],[1040,243,54,64]]);formMeta.append(dict(layer=name,mask=i,originalCell=i,role='Explicitly lifted and hung print'))
js(R/'validation/whole-pattern-crops.json',dict(scope='Original generated patterns, whole sheets mechanically cropped and placed; no generated procedural paint or recoloring.',components=cropProof))
# Full dynamic footprint must stay inside the fixed physical table collision.
footprint=[]
for name,im in overlays.items():
 alpha=np.asarray(im)[:,:,3]>0;bad=int((alpha&~blocked).sum());assert bad==0,(name,bad);footprint.append(dict(layer=name,pixels=int(alpha.sum()),outsideFixedSolids=bad,bounds=im.getchannel('A').getbbox()))
js(R/'validation/dynamic-footprints.json',dict(collisionInvariant=True,layers=footprint))
sets=[];layers=[];gid=1
def pack(name,im,visible=True):
 global gid
 tiles=[];lookup={};data=[]
 for y in range(N):
  for x in range(C):
   t=im.crop((x*32,y*32,x*32+32,y*32+32));key=t.tobytes()
   if not t.getchannel('A').getbbox():data.append(0);continue
   if key not in lookup:lookup[key]=len(tiles);tiles.append(t)
   data.append(gid+lookup[key])
 for page,start in enumerate(range(0,len(tiles),1024)):
  ts=tiles[start:start+1024];cols=min(32,len(ts));atlas=Image.new('RGBA',(cols*32,math.ceil(len(ts)/cols)*32))
  for i,t in enumerate(ts):atlas.paste(t,(i%cols*32,i//cols*32))
  fn=f'{name}-{page}.png';atlas.save(R/'runtime'/fn);sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=cols,tilecount=len(ts)))
 layers.append(dict(name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=visible,opacity=1,data=data));gid+=len(tiles)
pack('ground-and-architecture',base)
for name,im in overlays.items():pack(name,im,name in ['wet-0','print-0'])
layers.append(dict(name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]));pack('foreground',above)
Image.new('RGBA',(32,32)).save(R/'runtime/logic.png');sets.append(dict(firstgid=gid,name='collision',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,dict(name='collision',type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=0,data=[gid if v else 0 for v in g.flat]));gid+=1
# Native silent:true suppresses proximity/AV; restrict it to the actual arrival, not the whole map.
qx,qy=D['spawn'][0]//32,D['spawn'][1]//32
quietData=[gid if x==qx and y==qy and not g[y,x] else 0 for y in range(N)for x in range(C)]
quietCells=[[i%C,i//C]for i,v in enumerate(quietData)if v]
quietSeats=[dict(name=s['name'],silent=bool(quietData[(s['anchor'][1]//32)*C+s['anchor'][0]//32]))for s in seats]
quietAnchors=[dict(name=a['name'],silent=bool(quietData[(a['anchor'][1]//32)*C+a['anchor'][0]//32]))for a in anchors]
assert len(quietCells)<=9 and all(not s['silent']for s in quietSeats)
js(R/'validation/quiet-arrival-scope.json',dict(scope='Local map-authored proximity/AV exclusion at true arrival only; no live acceptance or global privacy change.',spawn=D['spawn'],maximumTileBuffer=0,activeCells=quietCells,seats=quietSeats,anchors=quietAnchors))
sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1));layers.insert(2,dict(name='quiet-arrival',type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=0,data=quietData,properties=props(silent=True)))
sx,sy=D['spawn'];objects=[dict(id=1,name='start',type='area',**{'class':'area'},x=sx-16,y=sy-16,width=32,height=32,visible=True,rotation=0,properties=props(start=True))];interactive={a['id']:dict(x=a['anchor'][0],y=a['anchor'][1],radius=a['radius'],**{k:a[k]for k in ['to','action','description','label']if k in a})for a in anchors};interactive['journal']=dict(x=D['spawn'][0],y=D['spawn'][1],radius=28)
for i,(name,a)in enumerate(interactive.items(),2):objects.append(dict(id=i,name='marble-popup-'+name,type='',x=a['x']-150,y=a['y']-160,width=300,height=144,visible=True,rotation=0))
layers.append(dict(name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=objects))
for i,l in enumerate(layers):l['id']=i+1
m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=C,height=N,tilewidth=32,tileheight=32,nextlayerid=len(layers)+1,nextobjectid=len(objects)+1,layers=layers,tilesets=sets,properties=props(name=D['title'],script='experience.js',wokaScale=1,status='Author candidate; live review pending'))
js(R/'runtime/map.tmj',m);js(R/'runtime/map.wam',dict(version='2.0.0',mapUrl='./map.tmj',entities={},entityCollections=[],areas=[]));(R/'runtime/experience.js').write_text('globalThis.MarbleLayout = '+json.dumps({'anchors':interactive},separators=(',',':'))+';\n'+(R/'source/controller.js').read_text())
at={s['image']:Image.open(R/'runtime'/s['image']).convert('RGBA')for s in sets};decoded={}
for l in layers:
 if l['type']!='tilelayer'or l.get('opacity')==0:continue
 im=Image.new('RGBA',(W,H))
 for j,v in enumerate(l['data']):
  if not v:continue
  s=max((s for s in sets if s['firstgid']<=v),key=lambda s:s['firstgid']);n=v-s['firstgid'];x=n%s['columns']*32;y=n//s['columns']*32;im.paste(at[s['image']].crop((x,y,x+32,y+32)),(j%C*32,j//C*32))
 decoded[l['name']]=im;im.save(R/'review'/('decoded-'+l['name']+'.png'))
bare=Image.alpha_composite(decoded['ground-and-architecture'],decoded['foreground']);assert bare.tobytes()==art.tobytes();empty=base.copy()
for name in ['wet-0','print-0']:empty=Image.alpha_composite(empty,decoded[name])
empty=Image.alpha_composite(empty,above);empty.save(R/'review/decoded-art.png');decoded['ground-and-architecture'].save(R/'review/decoded-ground.png')
stateHashes={};logical=[];contact=Image.new('RGB',(1024,1536),'#243029');cd=ImageDraw.Draw(contact)
for wet in range(8):
 for printed in range(8):
  names=['wet-'+str(wet),'print-'+str(printed)];state=base.copy()
  for n in names:state=Image.alpha_composite(state,decoded[n])
  state=Image.alpha_composite(state,above);key=f'wet-{wet}-print-{printed}';stateHashes[key]=hashlib.sha256(state.tobytes()).hexdigest();logical.append(dict(name=key,wet=wet,printed=printed,showLayers=names,complete=printed>0))
  crop=Image.new('RGBA',(256,96));crop.alpha_composite(state.crop((193,333,321,403)),(0,0));crop.alpha_composite(state.crop((970,236,1100,310)).resize((128,70)),(128,0));cd.text((0,0),'',fill='white');i=wet*8+printed;contact.paste(crop,((i%4)*256,(i//4)*96));cd.text(((i%4)*256+4,(i//4)*96+78),key,fill='white')
assert len(set(stateHashes.values()))==64
contact.save(R/'review/all64-states.png')
checks=dict(decodedExact=True,opaqueGround=base.getchannel('A').getextrema()==(255,255),foregroundPixels=int(fg.sum()),candidateForegroundPixels=int(candidate.sum()),foregroundExcludedForHeadSafety=int((candidate&unsafe).sum()),headConflicts=int((fg&unsafe).sum()),openCells=int((g==0).sum()),anchors=[dict(name=a['name'],bodyClear=bool(clear[a['anchor'][1],a['anchor'][0]]))for a in seats+anchors],fixtureNegatives=[dict(**p,blocked=bool(g[p['point'][1]//32,p['point'][0]//32]))for p in D['fixtureNegatives']])
js(R/'validation/geometry.json',checks);js(R/'validation/state-layers.json',dict(scope='Eight wet pass subsets and eight separately copied drying-rack print states, including blank:64 unique physical displays. All three tools are explicit, each applied at most once per sheet. Applying tool order commutes deliberately; fresh sheet and visit reset are explicit.',collisionInvariant=True,states=list(stateHashes),stateHashes=stateHashes,logicalViews=logical,forms=formMeta))
over=Image.new('RGBA',(W,H));d=ImageDraw.Draw(over)
for y,row in enumerate(g):
 for x,b in enumerate(row):
  if b:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(205,20,47,100))
dbg=Image.alpha_composite(empty,over);d=ImageDraw.Draw(dbg)
for a in seats+anchors:
 x,y=a['anchor'];d.rectangle((x-8,y,x+7,y+15),outline='#00ffff');d.text((x+9,y-12),a['name'],fill='white')
dbg.save(R/'review/collision-readable.png');print(json.dumps(checks,indent=2));assert all(a['bodyClear']for a in checks['anchors']);assert all(p['blocked']for p in checks['fixtureNegatives'])
