"""Self-contained native32 compiler for the approved six-mat source-only variant."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math,collections
R=Path(__file__).resolve().parents[1];SLUG='timber-mixed-six-mat-instructor-facing-r2';O=R/SLUG
T=32;C=24;N=16;W=768;H=512
for f in ['map32','source','review','assets']:(O/f).mkdir(parents=True,exist_ok=True)
def js(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def props(**x):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in x.items()]
concept=Image.open(R/'previews/instructor-facing-concept.png').convert('RGBA');art=Image.open(R/'previews/runtime-doorway-candidate.png').convert('RGBA')
g=np.ones((N,C),dtype=np.uint8)
# Explicit whole-cell floor. Approved bounded doorway repairs create one
# safe entrance and full inscribed floor across each retained furniture nook.
for x,y,w,h in [(6,3,3,1),(15,3,5,1),(4,4,16,4),(9,8,6,3),(11,11,2,5),(7,10,2,1),(4,11,4,1),(15,10,2,1),(16,11,4,1)]:g[y:y+h,x:x+w]=0
# Entire projected source block and bottle silhouettes occupy row 5. Native
# mat arrivals use lower, clear portions; all six remain connected through row 6.
for x in [5,6,7,8,9,14,15,16,17,18]:g[5,x]=1
spawn=[12,14]
anchors=[]
def anchor(name,x,y,kind='approach',direction='north'):
 anchors.append(dict(name=name,cell=[x//32,y//32],anchor=[x,y],floorClick=[x,y+16],kind=kind,direction=direction))
anchor('instructor position',376,143,'instructor','south')
for name,x in [('west mat 1',168),('west mat 2',216),('west mat 3',272),('east mat 1',496),('east mat 2',552),('east mat 3',600)]:anchor(name,x,199,'mat')
for name,x,y in [('central medallion',376,239),('west weights approach',144,207),('east weights approach',624,207),('rower approach',176,143),('bike approach',624,143),('studio threshold',376,303),('arrival hall',376,399),('arrival',400,463),('west bench nook approach',240,367),('east water nook approach',528,367),('west bench front',176,367),('west nook interior',144,367),('east refreshments front',592,367),('east nook interior',624,367),('bottom central stairs',376,495)]:anchor(name,x,y)
# Conservative source-depth split: retain source pixels only around periphery,
# and never above any reachable native head from any proof Woka direction.
blocked=g.repeat(T,0).repeat(T,1).astype(bool);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(blocked.shape);xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(json.loads((R/'source-assets/native-head-union.json').read_text())['mask'],bool)
unsafe=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
cand=Image.new('L',(W,H));d=ImageDraw.Draw(cand)
for poly in [[(0,120),(72,112),(104,213),(76,300),(0,330)],[(683,112),(768,110),(768,356),(694,264)],[(270,407),(312,409),(321,465),(277,466)],[(446,405),(492,405),(504,465),(449,466)]]:d.polygon(poly,fill=255)
candidate=np.array(cand)>0;rgb=np.array(art)[:,:,:3].astype(float);leaf=(rgb[:,:,1]>rgb[:,:,0]*.82)&(rgb[:,:,1]>rgb[:,:,2]*1.35)&((rgb[:,:,1]-rgb[:,:,2])>16)
for x0,y0,x1,y1 in [(144,358,204,402),(558,358,624,402)]:candidate[y0:y1,x0:x1]|=leaf[y0:y1,x0:x1]
safe=candidate&~unsafe;lo=np.array(art);hi=np.zeros_like(lo);hi[safe]=lo[safe];lo[safe]=0;base=Image.fromarray(lo);above=Image.fromarray(hi);assert Image.alpha_composite(base,above).tobytes()==art.tobytes()
base.save(O/'assets/base.png');above.save(O/'assets/above.png')
zones=[dict(name='Instructor front',rect=[320,128,128,32],kind='speaker'),dict(name='Yoga participant floor',rect=[128,192,512,64],kind='listener')]
js(O/'source/layout.json',dict(title='Timber Yoga · Instructor-Facing Six Mats',category='Activity / mixed gym and yoga',dimensions=[C,N],spawn=spawn,anchors=anchors,seats=[],zones=zones,collision=g.tolist(),notes='Six walk-to standing mat positions; no exercise, sitting or equipment animation. Bounded source-only native doorway repair makes both nook approaches accessible; furniture remains scenery.'))
sets=[];layers=[];gid=1;roundtrips=[]
def layer(name,data,opacity=1):return dict(name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=data)
for name,im in [('architecture-and-furniture',base),('foreground',above)]:
 if name=='foreground':layers.append(dict(name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 tiles=[];lookup={};data=[]
 for y in range(N):
  for x in range(C):
   tile=im.crop((x*T,y*T,(x+1)*T,(y+1)*T));key=tile.tobytes()
   if not tile.getbbox():data.append(0);continue
   if key not in lookup:lookup[key]=len(tiles);tiles.append(tile)
   data.append(gid+lookup[key])
 cols=min(24,len(tiles));atlas=Image.new('RGBA',(cols*T,math.ceil(len(tiles)/cols)*T))
 for j,t in enumerate(tiles):atlas.paste(t,(j%cols*T,j//cols*T))
 fn=name+'.png';atlas.save(O/'map32'/fn);sets.append(dict(firstgid=gid,name=name,image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(tiles)))
 layers.append(layer(name,data));roundtrips.append(dict(layer=name,tiles=len(tiles)));gid+=len(tiles)
Image.new('RGBA',(32,32)).save(O/'map32/logic.png')
sets.append(dict(firstgid=gid,name='collision',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,layer('collision',[gid if v else 0 for row in g for v in row],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1));quiet=[0]*(C*N);quiet[spawn[1]*C+spawn[0]]=gid;ql=layer('spawn-only-silence',quiet,0);ql['properties']=props(silent=True);layers.insert(2,ql)
start=dict(id=1,name='start',type='area',**{'class':'area'},x=spawn[0]*T,y=spawn[1]*T,width=T,height=T,rotation=0,visible=True,properties=props(start=True));layers.append(dict(name='map-areas',type='objectgroup',x=0,y=0,opacity=1,visible=True,objects=[start],draworder='topdown'))
for i,l in enumerate(layers):l['id']=i+1
m=dict(compressionlevel=-1,width=C,height=N,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tilewidth=T,tileheight=T,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=2,backgroundcolor='#20322b',properties=props(name='Timber Yoga · Instructor-Facing Six Mats',category='Activities',wokaScale=1,status='Local native32 candidate; no live deployment claim'),layers=layers,tilesets=sets);js(O/'map32/map.tmj',m)
areas=[]
for i,z in enumerate(zones):
 x,y,w,h=z['rect'];pid=f'{SLUG}-{i}';ps=[dict(id=pid+'-speaker',type='speakerMegaphone',name=pid,chatEnabled=False)] if z['kind']=='speaker' else [dict(id=pid+'-listener',type='listenerMegaphone',speakerZoneName=f'{SLUG}-0',chatEnabled=False)]
 areas.append(dict(id=pid,name=z['name'],x=x,y=y,width=w-1,height=h-1,visible=True,properties=ps))
js(O/'map32/map.wam',dict(version='2.0.0',mapUrl='./map.tmj',entities={},entityCollections=[],areas=areas))
# Decode the written TMJ and actual atlas files for every render.
m=json.loads((O/'map32/map.tmj').read_text());decoded=[]
for l in m['layers']:
 if l['type']!='tilelayer' or l.get('opacity')==0:continue
 im=Image.new('RGBA',(W,H))
 for j,v in enumerate(l['data']):
  if not v:continue
  s=max((s for s in m['tilesets'] if s['firstgid']<=v),key=lambda s:s['firstgid']);at=Image.open(O/'map32'/s['image']).convert('RGBA');n=v-s['firstgid'];x=n%s['columns']*T;y=n//s['columns']*T;im.paste(at.crop((x,y,x+T,y+T)),(j%C*T,j//C*T))
 decoded.append(im)
assert decoded[0].tobytes()==base.tobytes() and decoded[1].tobytes()==above.tobytes()
empty=Image.alpha_composite(*decoded);assert empty.tobytes()==art.tobytes();empty.save(O/'review/empty-native.png')
occupied=decoded[0].copy();occupied.alpha_composite(Image.open(R/'source-assets/occupied-proof-overlay.png').convert('RGBA'));occupied.alpha_composite(decoded[1]);occupied.save(O/'review/occupied-native.png');occupied.crop((96,288,680,400)).save(O/'review/nooks-occupied-native.png');occupied.crop((112,112,656,264)).save(O/'review/classroom-occupied-native.png');occupied.crop((256,344,512,512)).save(O/'review/entry-occupied-native.png')
for f in ['WOKA-PROOF.json','native-head-union.json']:(O/'source'/f).write_bytes((R/'source-assets'/f).read_bytes())
(O/'source/RUNTIME-DOORWAY-PATCH.json').write_bytes((R/'previews/RUNTIME-DOORWAY-PATCH.json').read_bytes())
(O/'source/SOURCE-PRESERVATION.json').write_bytes((R/'previews/SOURCE-PRESERVATION.json').read_bytes())
reachable={tuple(spawn)};q=collections.deque(reachable)
while q:
 x,y=q.popleft()
 for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=nx<C and 0<=ny<N and not g[ny,nx] and (nx,ny) not in reachable:reachable.add((nx,ny));q.append((nx,ny))
for a in anchors:
 assert tuple(a['cell']) in reachable,a
 x,y=a['anchor'];assert clear[y,x],a
js(O/'VALIDATION.json',dict(nativeTileSize=32,world=[W,H],dimensions=[C,N],sourceUniformScale=.5,sourceCompositeExact=True,atlasRoundtripsExact=True,reachableCells=len(reachable),walkableCells=int((g==0).sum()),anchors=len(anchors),matAnchors=6,allAnchorsBodyClear=True,quietCells=1,spawnOnlySilence=True,sourceDepthPixels=int(safe.sum()),actualSourceWokaFrames=True,livePlaytest='not run',media='optional native WAM roles, not live tested',nooks='Both nook approaches reachable via approved bounded native doorway repair; furniture is scenery',scope='Source-to-atlas exactness, cell connectivity, anchor body geometry; pinned route replay and independent geometry are separate evidence.'))
(O/'GUIDE.md').write_bytes((R/'GUIDE.md').read_bytes())
print(str(O))
