from pathlib import Path
from PIL import Image,ImageChops
import numpy as np,json,hashlib,math,shutil
R=Path(__file__).resolve().parents[1];O=R/'map32';O.mkdir(exist_ok=True);W,H=1536,1280;T=32;C,N=W//T,H//T
jwrite=lambda p,x:Path(p).write_text(json.dumps(x,indent=2)+'\n')
def props(**kw):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in kw.items()]
base=Image.open(R/'assets/hall-architecture.png').convert('RGBA');fg=Image.new('RGBA',(W,H));chair=Image.open(R/'assets/chair-below.png').convert('RGBA');srcfg=Image.open(R/'assets/chair-above.png').convert('RGBA');back=srcfg.copy();mask=Image.new('L',back.size,0);mask.paste(srcfg.getchannel('A').crop((8,0,24,48)),(8,0));back.putalpha(mask);back.save(R/'assets/chair-foreground-safe.png')
# Split the exact original foreground, moving outer arms below actors.
original_empty=Image.alpha_composite(chair,srcfg)
outer=srcfg.copy(); outer.paste((0,0,0,0),(8,0,24,48));chair.alpha_composite(outer)
assert ImageChops.difference(original_empty,Image.alpha_composite(chair,back)).getbbox() is None
chair.save(R/'assets/chair-below-safe.png')
seats=[]
for b,bx in enumerate((192,608,1024)):
 for row in range(7):
  for col in range(10):
   x=bx+16+col*32;ay=432+row*64; y=ay-1
   base.alpha_composite(chair,(x-16,ay-16));fg.alpha_composite(back,(x-16,ay-16));seats.append({'id':f'{chr(65+b)}{row+1:02}-{col+1:02}','x':x,'y':y,'artAnchor':[x,ay],'bank':b,'row':row,'column':col,'floorClick':[x,y+16],'floorClickRect':[x-8,ay,16,16],'rowFront':[x,ay-16]})
podium=Image.open(R/'assets/podium-below.png');podiumfg=Image.open(R/'assets/podium-above.png');base.alpha_composite(podium,(728,256));fg.alpha_composite(podiumfg,(728,256))
base.save(R/'assets/hall-base.png');fg.save(R/'assets/hall-above.png')
g=np.ones((N,C),dtype=np.uint8)
def clear(x,y,w,h):assert all(v%32==0 for v in [x,y,w,h]);g[y//T:(y+h)//T,x//T:(x+w)//T]=0
def block(x,y,w,h):assert all(v%32==0 for v in [x,y,w,h]);g[y//T:(y+h)//T,x//T:(x+w)//T]=1
clear(128,384,1280,544)  # hall floor and broad aisles
clear(256,1024,1024,128) # clear arrival vestibule, keeps side displays protected
clear(704,1152,128,128)  # south entry receiver, no external destination bound yet
clear(512,896,96,160);clear(928,896,96,160) # rear portals aligned with carpet aisles
clear(288,224,960,96)   # timber stage
clear(256,288,64,128);clear(1216,288,64,128) # accessible stage steps
# Rear-foot / chair-back row barriers on the native32 collision grid.
for s in seats:block(s['x']-16,s['artAnchor'][1]+16,32,32)
# Native32 conservative footprint includes podium sides to protect walking heads.
block(704,288,128,32)
# Potted plants at rear outside corners are physical features.
block(128,832,64,96);block(1344,832,64,96)
sets=[];layers=[];gid=1;audit=[]
def tl(name,data,opacity=1):return {'id':0,'name':name,'type':'tilelayer','x':0,'y':0,'width':C,'height':N,'visible':True,'opacity':opacity,'data':list(map(int,data))}
for name,im in [('hall-base',base),('hall-above',fg)]:
 if name=='hall-above':layers.append({'id':0,'name':'floorLayer','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':[]})
 cells=[];lookup={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   tile=im.crop((x,y,x+T,y+T));blob=tile.tobytes()
   if not tile.getchannel('A').getbbox():data.append(0);continue
   if blob not in lookup:lookup[blob]=len(cells);cells.append(tile)
   data.append(gid+lookup[blob])
 restore=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restore.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 assert ImageChops.difference(im,restore).getbbox() is None
 for page,start in enumerate(range(0,len(cells),1024)):
  parts=cells[start:start+1024];cols=min(32,len(parts));rows=math.ceil(len(parts)/cols);atlas=Image.new('RGBA',(cols*T,rows*T))
  for i,cell in enumerate(parts):atlas.paste(cell,((i%cols)*T,(i//cols)*T))
  pn=f'{name}-p{page}';atlas.save(O/f'{pn}.png');sets.append({'firstgid':gid+start,'name':pn,'image':f'{pn}.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':cols,'tilecount':len(parts)})
 layers.append(tl(name,data));audit.append({'layer':name,'uniqueTiles':len(cells),'exactPixelRoundTrip':True});gid+=len(cells)
Image.new('RGBA',(T,T),(240,30,70,90)).save(O/'collision-cell.png');sets.append({'firstgid':gid,'name':'permanent-collision','image':'collision-cell.png','imagewidth':T,'imageheight':T,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':props(collides=True)}]});layers.insert(1,tl('collision-permanent',[gid if x else 0 for x in g.flat],0))
objects=[{'id':1,'name':'start','class':'area','type':'area','x':736,'y':1056,'width':64,'height':64,'rotation':0,'visible':True,'properties':props(start=True)},{'id':2,'name':'quiet-arrival-vestibule','class':'area','type':'area','x':128,'y':1008,'width':1280,'height':272,'rotation':0,'visible':True,'properties':props(silent=True)},{'id':3,'name':'Flagship Hall','class':'area','type':'area','x':128,'y':384,'width':1280,'height':624,'rotation':0,'visible':True,'properties':props(venueHallId='astral-flagship',visualSeats=210,broadcastRequiresWam=True)}]
layers.append({'id':0,'name':'map-areas','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':objects})
for i,l in enumerate(layers):l['id']=i+1
m={'compressionlevel':-1,'height':N,'width':C,'infinite':False,'orientation':'orthogonal','renderorder':'right-down','tiledversion':'1.11.2','tileheight':T,'tilewidth':T,'type':'map','version':'1.10','nextlayerid':len(layers)+1,'nextobjectid':4,'backgroundcolor':'#102c32','properties':props(name='Astral Concourse — Flagship Hall',visualSeats=210,wokaScale=1,status='Local configured candidate; room WAM activation and live acceptance pending'),'layers':layers,'tilesets':sets}
jwrite(O/'grand-auditorium.tmj',m)
wam={'version':'2.0.0','mapUrl':'./grand-auditorium.tmj','entities':{},'entityCollections':[],'areas':[{'id':'astral-flagship-podium','name':'Flagship Podium','x':256,'y':208,'width':1024,'height':128,'visible':True,'properties':[{'id':'astral-flagship-broadcast','type':'speakerMegaphone','name':'astral-flagship-stage','chatEnabled':False}]},{'id':'astral-flagship-audience','name':'Flagship Audience','x':128,'y':384,'width':1280,'height':623,'visible':True,'properties':[{'id':'astral-flagship-receive','type':'listenerMegaphone','speakerZoneName':'astral-flagship-podium','chatEnabled':False}]},{'id':'astral-flagship-quiet-arrival','name':'Quiet arrival vestibule','x':128,'y':1008,'width':1280,'height':272,'visible':True,'properties':[{'id':'astral-flagship-silent','type':'silent'}]},{'id':'astral-flagship-spawn','name':'Flagship arrival','x':736,'y':1056,'width':64,'height':64,'visible':True,'properties':[{'id':'astral-flagship-start','type':'start','isDefault':True}]}]}
jwrite(O/'grand-auditorium.wam',wam)
jwrite(R/'source/seats.json',seats);jwrite(R/'source/collision-grid.json',{'width':C,'height':N,'tileSize':T,'grid':g.tolist(),'blockedIndices':np.flatnonzero(g).tolist(),'start':[768,1088],'speaker':[768,264],'anchors':[[s['id'],s['x'],s['y']]for s in seats]})
jwrite(R/'source/build-manifest.json',{'title':'Astral Concourse / Flagship Hall','world':[W,H],'nativeTileSize':32,'visualSeats':len(seats),'banks':3,'seatsPerRow':10,'rowsPerBank':7,'horizontalSeatPitch':32,'rowPitch':64,'nativeWokaScale':1,'chairForeground':'Original central16px lower chair-back pixels above actors; all original outer arm/back pixels retained below actors. Exact empty-scene union.','speakerTarget':[768,264],'quietSpawn':[768,1088],'atlasRoundTrips':audit,'engineChanges':False,'ambientAudio':False,'broadcast':'WAM configured candidate. Enter room via companion WAM; plain TMJ alone is insufficient. Live verification pending.','connectionToOtherHalls':'Unbound. Shared lobby/Forum/Arena/Studios remain approved masterplan only. No broken exit URL added.','validationScope':'Static source and native source-extracted movement harness; no browser or multiplayer acceptance.'})
print(json.dumps({'mapSize':[C,N],'tileSize':T,'seats':len(seats),'tilesets':len(sets),'walkableCells':int((g==0).sum()),'collisionCells':int(g.sum()),'atlasRoundTrips':audit},indent=2))
