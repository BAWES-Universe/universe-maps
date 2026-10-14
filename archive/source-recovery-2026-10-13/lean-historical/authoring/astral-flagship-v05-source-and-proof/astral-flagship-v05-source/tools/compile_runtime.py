from pathlib import Path
from PIL import Image
from collections import deque
import json,math,hashlib,shutil,copy
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'map32';W,H,T=2560,1920,32;C,N=80,60
O.mkdir(exist_ok=True);(R/'validation').mkdir(exist_ok=True);(R/'review').mkdir(exist_ok=True)
jw=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
props=lambda **d:[{'name':k,'type':'bool'if isinstance(v,bool)else'int'if isinstance(v,int)else'string','value':v}for k,v in d.items()]
a=json.loads((R/'source/garden-layout.json').read_text());h=json.loads((R/'source/v04-collision-grid.json').read_text());g=np.array(h['grid'],np.uint8);oldg=g.copy();q=json.loads((R/'source/v04-quiet-grid.json').read_text());mask=np.array(Image.open(R/a['walkableMask']).convert('L'));coverage=mask.reshape(N,T,C,T).transpose(0,2,1,3).mean(axis=(2,3))/255
# Only fully paved native cells join the garden. Existing rooms retain their exact cells.
new=(coverage>=.995);g[new]=0
for key in ['hallGardenDoorXYXY','terraceGardenDoorXYXY']:
 x0,y0,x1,y1=a[key];assert all(v%32==0 for v in[x0,y0,x1,y1]);g[y0//32:y1//32,x0//32:x1//32]=0
for obj in a['objects']:
 x,y,w,hh=obj['solidFootprintXYWH'];assert all(v%32==0 for v in[x,y,w,hh]);g[y//32:(y+hh)//32,x//32:(x+w)//32]=1
for x,y in a.get('runtimeRouteAdjustments',{}).get('closedCells',[]):g[y,x]=1
for x,y in a.get('runtimeRouteAdjustments',{}).get('openedCells',[]):g[y,x]=0
h['grid']=g.tolist();h['socialAnchors']+=a['socialAnchors'];h['landmarks'] +=[dict(id=v['id'],x=v['xy'][0],y=v['xy'][1])for v in a['landmarks']];jw(R/'source/collision-grid.json',h);jw(R/'source/quiet-grid.json',q);shutil.copy2(R/'source/v04-seats.json',R/'source/seats.json')
cfg=json.loads((R/'source/v04-runtime-layout.json').read_text());cfg['socialAnchors']+=a['socialAnchors'];cfg['informalPairs']+=a['informalPairs'];cfg['garden']=copy.deepcopy(a);cfg['garden'].get('runtimeRouteAdjustments',{}).pop('trimmedFoliageAlphaAbove32Count',None);cfg['status']='Roofless garden local candidate; no dynamic visibility or camera script';jw(R/'source/runtime-layout.json',cfg)
sets=[];layers=[];gid=1

def tl(name,data,opacity=1):return dict(id=0,name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=list(map(int,data)))
for name,filename in [('hall-base','runtime-base'),('hall-above','runtime-above')]:
 if name=='hall-above':layers.append(dict(id=0,name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 im=Image.open(R/'assets'/f'{filename}.png').convert('RGBA');p=np.array(im);p[p[:,:,3]==0]=0;im=Image.fromarray(p,'RGBA');cells=[];look={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   t=im.crop((x,y,x+T,y+T));b=t.tobytes()
   if not t.getchannel('A').getbbox():data.append(0);continue
   if b not in look:look[b]=len(cells);cells.append(t)
   data.append(gid+look[b])
 restore=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restore.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 assert restore.tobytes()==im.tobytes()
 for page,start in enumerate(range(0,len(cells),1024)):
  part=cells[start:start+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*T,math.ceil(len(part)/cols)*T))
  for i,t in enumerate(part):atlas.paste(t,((i%cols)*T,(i//cols)*T))
  fn=f'{name}-p{page}.png';atlas.save(O/fn);sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(part)))
 layers.append(tl(name,data));gid+=len(cells)
for f in ['collision-cell.png','quiet-marker.png']:shutil.copy2(R/'source'/f,O/f)
sets.append(dict(firstgid=gid,name='permanent-collision',image='collision-cell.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,tl('collision-permanent',[gid if v else 0 for v in g.flat],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet-marker-noncolliding',image='quiet-marker.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=1,tilecount=1));ql=tl('quiet-arrival-and-main-circulation',[gid if v else 0 for row in q['grid']for v in row]);ql['properties']=props(silent=True);layers.insert(2,ql)
areas=[dict(id=1,name='start',type='area',x=736,y=1792,width=64,height=64,rotation=0,visible=True,properties=props(start=True))];areas[0]['class']='area';layers.append(dict(id=0,name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=areas))
for i,l in enumerate(layers):l['id']=i+1
m=dict(compressionlevel=-1,height=N,width=C,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=T,tilewidth=T,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=2,backgroundcolor='#102c32',properties=props(name='Astral Concourse / Roofless Garden (Option1)',visualSeats=210,loungeSeats=16,casualSeats=12,wokaScale=1,status='Roofless map; actual room WAM setup and live acceptance pending'),layers=layers,tilesets=sets);jw(O/'grand-auditorium.tmj',m)
wam=json.loads((R/'source/v04-area-template.wam').read_text().replace('astral-flagship-v04','astral-flagship-v05').replace('Flagship v04','Flagship v05'));jw(O/'grand-auditorium.wam',wam)
reachable=np.zeros_like(g,bool);todo=deque([(24,57)])
while todo:
 x,y=todo.popleft()
 if not(0<=x<C and 0<=y<N)or g[y,x]or reachable[y,x]:continue
 reachable[y,x]=1;todo.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
report=dict(walkableCells=int((g==0).sum()),reachableCells=int(reachable.sum()),unreachableWalkableCells=int(((g==0)&~reachable).sum()),openedCells=int(((oldg==1)&(g==0)).sum()),closedCells=int(((oldg==0)&(g==1)).sum()),quietCells=int(np.array(q['grid']).sum()),newGardenSeatCount=len(a['socialAnchors']),dynamicScripts=False,sceneryBeyondPavingWalkable=False)
jw(R/'validation/build-geometry.json',report);Image.alpha_composite(Image.open(R/'assets/runtime-base.png').convert('RGBA'),Image.open(R/'assets/runtime-above.png').convert('RGBA')).save(R/'review/runtime-empty-native.png');shutil.copy2(R/'source/v03-greg-reference.png',R/'assets/greg-reference.png');print(json.dumps(report,indent=2))
