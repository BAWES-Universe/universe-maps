"""Pack authored native layers; preserve frozen v03 collision, quiet and seat geometry."""
from pathlib import Path
from PIL import Image
import json, math, hashlib, shutil
import numpy as np

R=Path(__file__).resolve().parents[1]
V3=R.parent/'grand-auditorium-03-foyer-terrace'
O=R/'map32'; O.mkdir(exist_ok=True)
W,H,T=2560,1920,32
C,N=W//T,H//T
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
props=lambda **d:[{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in d.items()]
tilesets=[]; audit=[]; gid=1; lid=0
def new_id():
 global lid
 lid+=1
 return lid
def tilelayer(name,data,opacity=1):
 return dict(id=new_id(),name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=list(map(int,data)))
def pack(name):
 global gid
 im=Image.open(R/'assets'/f'{name}.png').convert('RGBA')
 assert im.size==(W,H)
 # Canonicalize invisible RGB only; visible RGBA remains pixel-exact.
 pixels=np.array(im); pixels[pixels[:,:,3]==0]=0; im=Image.fromarray(pixels,'RGBA')
 cells=[];lookup={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   tile=im.crop((x,y,x+T,y+T));blob=tile.tobytes()
   if not tile.getchannel('A').getbbox():data.append(0);continue
   if blob not in lookup:lookup[blob]=len(cells);cells.append(tile)
   data.append(gid+lookup[blob])
 restored=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restored.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 assert restored.tobytes()==im.tobytes(),name
 for page,start in enumerate(range(0,len(cells),1024)):
  part=cells[start:start+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*T,math.ceil(len(part)/cols)*T))
  for i,t in enumerate(part):atlas.paste(t,((i%cols)*T,(i//cols)*T))
  fn=f'{name}-p{page}.png';atlas.save(O/fn)
  tilesets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(part)))
 audit.append(dict(asset=name,sha256=sha(R/'assets'/f'{name}.png'),uniqueTiles=len(cells),pixelExactRoundTrip=True))
 gid+=len(cells)
 return tilelayer(name,data)
def group(name,children):
 return dict(id=new_id(),name=name,type='group',x=0,y=0,visible=True,opacity=1,layers=[pack(n) for n in children])

layers=[group('v04-surroundings-below',['garden-topdown','shadows-exterior-cast','foyer-base','terrace-base','foyer-shadows-contact','terrace-shadows-contact','foyer-walls-raised']),pack('hall-base'),pack('hall-walls-raised')]
g=json.loads((R/'source/collision-grid.json').read_text())['grid']
q=json.loads((R/'source/quiet-grid.json').read_text())['grid']
for filename in ['collision-cell.png','quiet-marker.png']:shutil.copy2(V3/'map32'/filename,O/filename)
tilesets.append(dict(firstgid=gid,name='permanent-collision',image='collision-cell.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]))
layers.append(tilelayer('collision-permanent',[gid if v else 0 for row in g for v in row],0));gid+=1
tilesets.append(dict(firstgid=gid,name='quiet-marker-noncolliding',image='quiet-marker.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1))
quiet=tilelayer('quiet-arrival-and-main-circulation',[gid if v else 0 for row in q for v in row]);quiet['properties']=props(silent=True);layers.append(quiet);gid+=1
layers.append(dict(id=new_id(),name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
layers.extend([pack('hall-above'),group('v04-surroundings-above',['foyer-above','terrace-above']),group('v04-hall-roof',['roof-auditorium-shadow','roof-auditorium-full']),group('v04-foyer-roof',['roof-foyer-shadow','roof-foyer-full'])])
# Native membership uses player foot point (x,y+16), with inclusive rectangle edges.
# The small foyer door margins cover the avatar head before it passes under the shell.
# Hall/foyer overlap is an intentional common doorway band, independent of media areas.
areas=[dict(id=1,name='start',x=736,y=1792,width=64,height=64,properties=props(start=True)),dict(id=2,name='v04-hall-interior',x=0,y=0,width=1535,height=1007,properties=[]),dict(id=3,name='v04-foyer-interior',x=0,y=960,width=1544,height=848,properties=[])]
for a in areas:a.update({'class':'area','type':'area','rotation':0,'visible':True})
layers.append(dict(id=new_id(),name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=areas))
m=dict(compressionlevel=-1,height=N,width=C,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=T,tilewidth=T,type='map',version='1.10',nextlayerid=lid+1,nextobjectid=4,backgroundcolor='#102c32',properties=props(name='Astral Concourse / Flagship v04 Top-down Garden',visualSeats=210,loungeSeats=16,casualSeats=8,wokaScale=1,status='Local candidate; source tests and user visual review pending',script='./flagship-focus.js'),layers=layers,tilesets=tilesets)
write(O/'grand-auditorium.tmj',m)
wam=json.loads((V3/'map32/grand-auditorium.wam').read_text().replace('astral-flagship-v03','astral-flagship-v04').replace('Flagship v03','Flagship v04'))
write(O/'grand-auditorium.wam',wam)
write(R/'validation/atlas-roundtrips.json',audit)
write(R/'source/runtime-layer-contract.json',dict(nativeTileSize=T,world=[W,H],areas=areas,focusRectangle=[0,0,1536,1008],permanentLayers=['collision-permanent','quiet-arrival-and-main-circulation','hall-base','hall-walls-raised','hall-above'],decorativeGroups=['v04-surroundings-below','v04-surroundings-above','v04-hall-roof','v04-foyer-roof'],roofTransition='Immediate full reveal; no alpha tween or ghost layer during play',collisionSourceSHA256=sha(R/'source/collision-grid.json'),quietSourceSHA256=sha(R/'source/quiet-grid.json'),v03CollisionUnchanged=(R/'source/collision-grid.json').read_bytes()==(V3/'source/collision-grid.json').read_bytes(),v03QuietUnchanged=(R/'source/quiet-grid.json').read_bytes()==(V3/'source/quiet-grid.json').read_bytes(),note='Visibility changes replan native active paths despite identical collision grid. Final safe intended-tile route tests required; exact pointer endpoint not guaranteed.'))
print(json.dumps({'atlasLayers':len(audit),'uniqueTiles':sum(a['uniqueTiles'] for a in audit),'runtimePngFiles':len(list(O.glob('*.png'))),'tileGrid':[C,N],'nativeRegions':areas},indent=2))
