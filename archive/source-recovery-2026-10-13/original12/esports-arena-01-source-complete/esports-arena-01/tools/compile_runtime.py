from pathlib import Path
from PIL import Image
import numpy as np,json,math,hashlib
R=Path(__file__).resolve().parents[1];O=R/'map32';O.mkdir(exist_ok=True);W,H=2048,1472;C,N=64,46;T=32;gid=1;sets=[];layers=[];audit=[]
jw=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n');props=lambda **d:[{'name':k,'type':'bool'if isinstance(v,bool)else'int'if isinstance(v,int)else'float'if isinstance(v,float)else'string','value':v}for k,v in d.items()]
def tl(name,data,opacity=1):return dict(id=0,name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=list(map(int,data)))
for name in ['runtime-base','runtime-above']:
 if name=='runtime-above':layers.append(dict(id=0,name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 im=Image.open(R/'assets'/f'{name}.png').convert('RGBA');p=np.array(im);p[p[:,:,3]==0]=0;im=Image.fromarray(p);cells=[];look={};data=[]
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
 layers.append(tl(name,data));audit.append({'layer':name,'uniqueTiles':len(cells),'pixelExact':True});gid+=len(cells)
g=json.load(open(R/'source/collision-grid.json'));q=json.load(open(R/'source/quiet-grid.json'))['grid'];Image.new('RGBA',(32,32),(0,0,0,0)).save(O/'collision-cell.png');Image.new('RGBA',(32,32),(0,0,0,0)).save(O/'quiet-marker.png')
sets.append(dict(firstgid=gid,name='permanent-collision',image='collision-cell.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,tl('collision-permanent',[gid if v else 0 for row in g['grid']for v in row],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet-marker',image='quiet-marker.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1));quiet=tl('quiet-arrival-receiver',[gid if v else 0 for row in q for v in row]);quiet['properties']=props(silent=True);layers.insert(2,quiet)
start=dict(id=1,name='start',type='area',x=1000,y=1352,width=31,height=31,rotation=0,visible=True,properties=props(start=True));start['class']='area';layers.append(dict(id=0,name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[start]))
for i,l in enumerate(layers):l['id']=i+1
m=dict(compressionlevel=-1,height=N,width=C,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=32,tilewidth=32,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=2,backgroundcolor='#141b20',properties=props(name='Circuit Arena / Esports Event',visualSeats=24,teamSeats=12,casterSeats=2,socialSeats=4,wokaScale=1,status='Local source-validated template; not published or live-media accepted'),layers=layers,tilesets=sets);jw(O/'esports-arena.tmj',m);jw(O/'esports-arena.wam',{'version':'2.0.0','mapUrl':'./esports-arena.tmj','entities':{},'entityCollections':[],'areas':json.load(open(R/'source/areas.json'))})
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()];jw(R/'RUNTIME-MANIFEST.json',{'nativeTileSize':32,'world':[W,H],'files':files,'atlasRoundTrips':audit,'script':False,'focus':False,'dynamicVisibility':False,'quietCells':sum(sum(r)for r in q),'liveMediaVerified':False,'qaFixtureInRuntime':False});print(json.dumps({'runtimeFiles':len(files),'atlasRoundTrips':audit},indent=2))
