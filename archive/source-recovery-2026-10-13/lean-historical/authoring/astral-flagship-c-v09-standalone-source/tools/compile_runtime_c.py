"""Losslessly pack native32 C. All mutable layers are decorative only."""
from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'map32';T=32;W,H=2816,2432;C,N=W//T,H//T
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
props=lambda **d:[{'name':k,'type':'bool'if isinstance(v,bool)else'int'if isinstance(v,int)else'float'if isinstance(v,float)else'string','value':v}for k,v in d.items()]
g=json.loads((R/'source/collision-grid.json').read_text())['grid'];q=json.loads((R/'source/quiet-grid.json').read_text())['grid'];reveal=json.loads((R/'source/reveal-contract.json').read_text());sets=[];layers=[];gid=1;audit=[];lid=0
used={'grand-auditorium.tmj','grand-auditorium.wam','building-reveal.js'}
def ident():
 global lid
 lid+=1;return lid
def tl(name,data,opacity=1,visible=True):return dict(id=ident(),name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=visible,opacity=opacity,data=list(map(int,data)))
def pack(filename,name=None,visible=True):
 global gid
 name=name or filename;im=Image.open(R/'assets'/f'{filename}.png').convert('RGBA');assert im.size==(W,H)
 p=np.array(im);p[p[:,:,3]==0]=0;im=Image.fromarray(p);cells=[];lookup={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   tile=im.crop((x,y,x+T,y+T));blob=tile.tobytes()
   if not tile.getchannel('A').getbbox():data.append(0);continue
   if blob not in lookup:lookup[blob]=len(cells);cells.append(tile)
   data.append(gid+lookup[blob])
 restored=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restored.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 assert restored.tobytes()==im.tobytes(),filename
 for page,start in enumerate(range(0,len(cells),1024)):
  part=cells[start:start+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*T,math.ceil(len(part)/cols)*T))
  for i,tile in enumerate(part):atlas.paste(tile,((i%cols)*T,(i//cols)*T))
  fn=f'{name}-p{page}.png';atlas.save(O/fn);used.add(fn)
  sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(part)))
 audit.append({'layer':name,'asset':filename,'uniqueTiles':len(cells),'pixelExact':True,'sha256':hashlib.sha256((R/'assets'/f'{filename}.png').read_bytes()).hexdigest()});gid+=len(cells)
 return tl(name,data,visible=visible)
def group(name,asset):
 # Visible group container with explicitly hidden descendants: native flat layer
 # loading reads the child visibility; API showLayer(group) toggles descendants.
 child=pack(asset,'art',False)
 return dict(id=ident(),name=name,type='group',x=0,y=0,visible=True,opacity=1,layers=[child])
# Avoid atlas file name collisions among the semantic groups.
def deco(name,asset):
 child=pack(asset,name+'-art',False)
 return dict(id=ident(),name=name,type='group',x=0,y=0,visible=True,opacity=1,layers=[child])
layers.append(pack('runtime-base','interior-base'))
for f in ['collision-cell.png','quiet-marker.png']:shutil.copy2(R/'source/frozen-b'/f,O/f);used.add(f)
sets.append(dict(firstgid=gid,name='permanent-collision',image='collision-cell.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.append(tl('collision-permanent',[gid if v else 0 for row in g for v in row],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet-marker-noncolliding',image='quiet-marker.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1));quiet=tl('quiet-spawn-receiver',[gid if v else 0 for row in q for v in row]);quiet['properties']=props(silent=True);layers.append(quiet);gid+=1
animation=json.loads((R/'source/animation-placement.json').read_text());shutil.copy2(R/'source/frozen-b/garden-accent.png',O/'garden-accent.png');used.add('garden-accent.png');sets.append(dict(firstgid=gid,name='garden-native-accent',image='garden-accent.png',imagewidth=128,imageheight=32,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=4,tilecount=4,tiles=[dict(id=0,animation=[dict(tileid=i,duration=ms)for i,ms in enumerate(animation['durationsMs'])])]))
ad=[0]*(C*N)
for p in animation['placements']:
 x,y=p['cell'];assert g[y][x] and not q[y][x];ad[y*C+x]=gid
layers.append(tl('garden-native-animation',ad));gid+=4
for owner in ['hall','foyer']:layers.append(deco('v09-'+owner+'-shadow',owner+'-shadow'))
layers.append(dict(id=ident(),name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]));layers.append(pack('runtime-above','interior-above'))
for name,asset in [('v09-hall-shell','hall-shell'),('v09-foyer-wings','foyer-wings'),('v09-foyer-roof','foyer-roof'),('v09-foyer-front','foyer-front')]:layers.append(deco(name,asset))
areas=[dict(id=1,name='start',x=864,y=2144,width=64,height=64,properties=props(start=True)),dict(id=2,name='flagship-c-native-stage-focus',x=128,y=256,width=1536,height=1008,properties=props(focusable=True,zoomMargin=.15))]
for i,a in enumerate(reveal['areas'],3):areas.append(dict(id=i,**{k:v for k,v in a.items()if k!='playerCenterXYXY'},properties=[]))
for a in areas:a.update({'class':'area','type':'area','rotation':0,'visible':True})
layers.append(dict(id=ident(),name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=areas))
m=dict(compressionlevel=-1,height=N,width=C,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=T,tilewidth=T,type='map',version='1.10',nextlayerid=lid+1,nextobjectid=len(areas)+1,backgroundcolor='#102c32',properties=props(name='Astral Concourse / Building C / Native32',visualSeats=210,loungeSeats=16,casualSeats=12,wokaScale=1,status='Local candidate; source validation and user review pending',script='./building-reveal.js'),layers=layers,tilesets=sets)
write(O/'grand-auditorium.tmj',m);shutil.copy2(R/'source/companion.wam',O/'grand-auditorium.wam')
for p in O.iterdir():
 if p.is_file()and p.name not in used:raise ValueError('Unexpected runtime file: '+p.name)
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()]
write(R/'RUNTIME-MANIFEST.json',{'nativeTileSize':32,'worldPixels':[W,H],'files':files,'atlasRoundTrips':audit,'quietCells':sum(sum(r)for r in q),'dynamicVisibility':True,'defaultShellHidden':True,'nativeFocus':{'bounds':[128,256,1536,1008],'zoomMargin':.15,'rotationVerified':False},'liveMediaVerified':False})
Image.alpha_composite(Image.open(R/'assets/runtime-base.png').convert('RGBA'),Image.open(R/'assets/runtime-above.png').convert('RGBA')).save(R/'review/runtime-empty-native.png');print(json.dumps({'runtimeFiles':len(files),'bytes':sum(f['bytes']for f in files),'areas':len(areas),'layers':len(layers),'atlasLayers':len(audit)},indent=2))
