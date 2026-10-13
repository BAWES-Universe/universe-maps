"""Compile isolated corrective A. Native32 only; permanent collision/quiet; native focus."""
from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'map32';T=32;W,H=2560,1920;C,N=80,60
jw=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
props=lambda **d:[{'name':k,'type':'bool'if isinstance(v,bool)else'int'if isinstance(v,int)else'float'if isinstance(v,float)else'string','value':v}for k,v in d.items()]
g=json.loads((R/'source/collision-grid.json').read_text())['grid'];q=json.loads((R/'source/quiet-grid.json').read_text())['grid'];cfg=json.loads((R/'source/runtime-layout.json').read_text());sets=[];layers=[];gid=1;audit=[]
def tl(name,data,opacity=1):return dict(id=0,name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=list(map(int,data)))
for name,filename in [('hall-base','runtime-base'),('hall-above','runtime-above')]:
 if name=='hall-above':layers.append(dict(id=0,name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 im=Image.open(R/'assets'/f'{filename}.png').convert('RGBA');p=np.array(im);p[p[:,:,3]==0]=0;im=Image.fromarray(p);cells=[];look={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   t=im.crop((x,y,x+T,y+T));b=t.tobytes()
   if not t.getchannel('A').getbbox():data.append(0);continue
   if b not in look:look[b]=len(cells);cells.append(t)
   data.append(gid+look[b])
 restore=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restore.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 if restore.tobytes()!=im.tobytes():raise ValueError('Atlas reconstruction is not byte exact')
 for page,start in enumerate(range(0,len(cells),1024)):
  part=cells[start:start+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*T,math.ceil(len(part)/cols)*T))
  for i,t in enumerate(part):atlas.paste(t,((i%cols)*T,(i//cols)*T))
  fn=f'{name}-p{page}.png';atlas.save(O/fn);sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(part)))
 layers.append(tl(name,data));audit.append({'layer':name,'tiles':len(cells),'pixelExact':True});gid+=len(cells)
for f in ['collision-cell.png','quiet-marker.png']:shutil.copy2(R/'source/baseline-v05'/f,O/f)
sets.append(dict(firstgid=gid,name='permanent-collision',image='collision-cell.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,tl('collision-permanent',[gid if v else 0 for row in g for v in row],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet-marker-noncolliding',image='quiet-marker.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1));ql=tl('quiet-spawn-receiver',[gid if v else 0 for row in q for v in row]);ql['properties']=props(silent=True);layers.insert(2,ql)
areas=[dict(id=1,name='start',type='area',x=736,y=1792,width=64,height=64,rotation=0,visible=True,properties=props(start=True)),dict(id=2,name='flagship-a-native-stage-focus',type='area',x=0,y=0,width=1536,height=1008,rotation=0,visible=True,properties=props(focusable=True,zoomMargin=.15))]
for a in areas:a['class']='area'
layers.append(dict(id=0,name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=areas))
for i,l in enumerate(layers):l['id']=i+1
m=dict(compressionlevel=-1,height=N,width=C,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=T,tilewidth=T,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=3,backgroundcolor='#102c32',properties=props(name='Astral Concourse / Corrective A / Same Layout',visualSeats=210,loungeSeats=16,casualSeats=12,wokaScale=1,status='Local corrective candidate; validation and review pending'),layers=layers,tilesets=sets);jw(O/'grand-auditorium.tmj',m)
wam=json.loads((R/'source/baseline-v05/grand-auditorium.wam').read_text().replace('astral-flagship-v05','astral-flagship-v07').replace('Flagship v05','Flagship v07'));jw(O/'grand-auditorium.wam',wam)
used={s['image']for s in sets}|{'grand-auditorium.tmj','grand-auditorium.wam'}
for p in O.iterdir():
 if p.is_file()and p.name not in used:raise ValueError('Unexpected stale runtime file '+p.name)
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()]
jw(R/'RUNTIME-MANIFEST.json',{'nativeTileSize':32,'files':files,'nativeFocus':{'bounds':[0,0,1536,1008],'zoomMargin':.15,'initialFocusVerifiedBySource':True,'rotationVerified':False},'script':False,'dynamicVisibility':False,'quietCells':sum(sum(r)for r in q),'atlasRoundTrips':audit,'liveMediaVerified':False})
Image.alpha_composite(Image.open(R/'assets/runtime-base.png').convert('RGBA'),Image.open(R/'assets/runtime-above.png').convert('RGBA')).save(R/'review/runtime-empty-native.png');print(json.dumps({'runtimeFiles':len(files),'quietCells':sum(sum(r)for r in q),'atlasRoundTrips':audit},indent=2))
