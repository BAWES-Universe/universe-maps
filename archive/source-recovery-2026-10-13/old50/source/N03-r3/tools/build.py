from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,math,collections,sys,subprocess
R=Path(__file__).resolve().parents[1];T=32;W=1024;H=896;C=W//T;N=H//T
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def js(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def props(**kw):return [dict(name=k,type='bool' if isinstance(v,bool) else 'string',value=v) for k,v in kw.items()]
class Map:
 def __init__(self,id,title,crops):
  self.id=id;self.title=title;self.out=R/id
  for f in ['source','map32','review','validation']:(self.out/f).mkdir(parents=True,exist_ok=True)
  self.original=Image.open(R/'source'/f'{id}-original.png').convert('RGBA');self.crops=crops;self.assets={};self.base=Image.new('RGBA',(W,H));self.fore=Image.new('RGBA',(W,H));self.grid=[[0]*C for _ in range(N)];self.anchors=[];self.objects=[];self.zones=[];self.start=[528,784]
  for k,b in crops.items():
   a=self.original.crop(tuple(b));bb=a.getbbox();self.assets[k]=a.crop(bb) if bb else a
 def fill(self,k,x,y,w,h):
  # Texture sampling is code-native atlas assembly; generation is immutable.
  a=self.assets[k];a=a.crop((a.width//4,a.height//4,a.width*3//4,a.height*3//4)).resize((64,64),Image.Resampling.LANCZOS).convert('RGB').convert('RGBA')
  for yy in range(y*32,(y+h)*32,64):
   for xx in range(x*32,(x+w)*32,64):self.base.alpha_composite(a.crop((0,0,min(64,(x+w)*32-xx),min(64,(y+h)*32-yy))),(xx,yy))
 def block(self,x,y,w,h):
  for yy in range(y,y+h):
   for xx in range(x,x+w):self.grid[yy][xx]=1
 def wall(self,x,y,w,h=1):
  self.fill('wall',x,y,w,h);self.block(x,y,w,h);self.objects.append(dict(asset='wall',rect=[x*32,y*32,w*32,h*32],collision=[x,y,w,h],depth='base'))
 def sprite(self,k,x,y,w,h,block=True,depth=False):
  a=self.assets[k].resize((w*32,h*32),Image.Resampling.LANCZOS);xx=x*32;yy=y*32
  if depth:
   # Upper canopy above avatars, foot/pot remains below. Split within bounded object only.
   split=max(1,a.height-32);self.fore.alpha_composite(a.crop((0,0,a.width,split)),(xx,yy));self.base.alpha_composite(a.crop((0,split,a.width,a.height)),(xx,yy+split))
   if block:self.block(x,y+h-1,w,1)
  else:
   self.base.alpha_composite(a,(xx,yy))
   if block:self.block(x,y,w,h)
  self.objects.append(dict(asset=k,rect=[xx,yy,w*32,h*32],collision=[x,y+h-1,w,1] if depth and block else [x,y,w,h] if block else None,depth='bounded canopy' if depth else 'base'))
 def seat(self,x,y,d='south',k='seat1'):
  self.sprite(k,x,y,1,1,False);self.anchor('seat-'+str(len(self.anchors)+1),x,y,d,'seat')
 def anchor(self,id,x,y,d='south',kind='route'):
  self.anchors.append(dict(id=id,x=x*32+16,y=y*32+8,direction=d,kind=kind))
 def perimeter(self):
  self.wall(0,0,C);self.wall(0,N-1,C);self.wall(0,1,1,N-2);self.wall(C-1,1,1,N-2)
 def finish(self):
  P=self.out;self.base.save(P/'source/runtime-base.png');self.fore.save(P/'source/runtime-foreground.png')
  js(P/'source/layout.json',dict(title=self.title,grid=self.grid,start=self.start,anchors=self.anchors,objects=self.objects,world=[W,H],cropCoordinates=self.crops,sourceArt=f'../../source/{self.id}-original.png'))
  sets=[];layers=[];gid=1
  for name,im in [('ground',self.base),('foreground',self.fore)]:
   if name=='foreground':layers.append(dict(name='floorLayer',type='objectgroup',objects=[],visible=True,opacity=1))
   tiles=[];lookup={};data=[]
   for y in range(N):
    for x in range(C):
     t=im.crop((x*T,y*T,(x+1)*T,(y+1)*T));b=t.tobytes()
     if not t.getbbox():data.append(0);continue
     if b not in lookup:lookup[b]=len(tiles);tiles.append(t)
     data.append(gid+lookup[b])
   cols=32;atlas=Image.new('RGBA',(1024,math.ceil(len(tiles)/cols)*32))
   for i,t in enumerate(tiles):atlas.paste(t,(i%cols*32,i//cols*32))
   atlas.save(P/'map32'/f'{name}.png');sets.append(dict(firstgid=gid,name=name,image=f'{name}.png',imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,columns=cols,tilecount=len(tiles),spacing=0,margin=0));layers.append(dict(name=name,type='tilelayer',width=C,height=N,data=data,visible=True,opacity=1));gid+=len(tiles)
  Image.new('RGBA',(32,32)).save(P/'map32/logic.png');sets.append(dict(firstgid=gid,name='logic',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,spacing=0,margin=0,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,dict(name='collision',type='tilelayer',width=C,height=N,data=[gid if z else 0 for row in self.grid for z in row],opacity=0,visible=True))
  gid+=1
  sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,spacing=0,margin=0));quiet=[0]*(C*N)
  for qy in range(self.start[1]//32-1,self.start[1]//32+2):
   for qx in range(self.start[0]//32-1,self.start[0]//32+2):quiet[qy*C+qx]=gid
  layers.insert(2,dict(name='arrival-quiet',type='tilelayer',width=C,height=N,data=quiet,opacity=0,visible=True,properties=props(silent=True)))
  start=dict(id=1,name='start',type='area',x=self.start[0]-16,y=self.start[1]-16,width=32,height=32,visible=True,properties=props(start=True));layers.append(dict(name='areas',type='objectgroup',objects=[start],opacity=1,visible=True))
  for i,l in enumerate(layers):l.update(id=i+1,x=0,y=0)
  m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,tilewidth=32,tileheight=32,width=C,height=N,layers=layers,tilesets=sets,nextlayerid=len(layers)+1,nextobjectid=2,properties=props(title=self.title,status='Local authorable candidate; live playtest pending'))
  js(P/'map32'/f'{self.id}.tmj',m);js(P/'map32'/f'{self.id}.wam',dict(version='2.0.0',mapUrl=f'./{self.id}.tmj',entities={},entityCollections=[],areas=[dict(id='arrival',name='Arrival',x=self.start[0]-16,y=self.start[1]-16,width=32,height=32,visible=True,properties=[dict(id='start',type='start',isDefault=True)])]))
  # Decode actual emitted TMJ and atlases; proofs never use source base directly.
  decoded=[];atlas_cache={v['image']:Image.open(P/'map32'/v['image']).convert('RGBA') for v in sets}
  for l in m['layers']:
   if l['type']!='tilelayer' or not l['opacity']:continue
   im=Image.new('RGBA',(W,H))
   for i,g in enumerate(l['data']):
    if not g:continue
    s=max((s for s in sets if s['firstgid']<=g),key=lambda s:s['firstgid']);at=atlas_cache[s['image']];n=g-s['firstgid'];xx=n%s['columns']*32;yy=n//s['columns']*32;im.alpha_composite(at.crop((xx,yy,xx+32,yy+32)),(i%C*32,i//C*32))
   decoded.append(im)
  assert decoded[0].tobytes()==self.base.tobytes() and decoded[1].tobytes()==self.fore.tobytes()
  Image.alpha_composite(*decoded).save(P/'review/empty-native.png');occupied=decoded[0].copy();meta=json.loads((R/'fixtures/ACTOR-PROVENANCE.json').read_text())['actors'];records=[]
  for i,a in enumerate(self.anchors):
   s=meta[i%len(meta)];ox,oy=s['anchor'];sheet=Image.open(R/'fixtures'/f"proof-actors-{a['direction']}.png").convert('RGBA');frame=sheet.crop((ox-16,oy-16,ox+16,oy+16));expected=s['frames'][a['direction']]['rgba_sha256'];assert hashlib.sha256(frame.tobytes()).hexdigest()==expected,(s['file'],a['direction'])
   occupied.alpha_composite(frame,(a['x']-16,a['y']-16));records.append(dict(anchor=a['id'],position=[a['x'],a['y']],direction=a['direction'],file=s['file'],source=s['path'],repoCommit=s['repoCommit'],frameSHA256=expected))
  occupied.alpha_composite(decoded[1]);occupied.save(P/'review/occupied-native.png');js(P/'review/occupants.json',records)
  col=Image.alpha_composite(*decoded);overlay=Image.new('RGBA',col.size);d=ImageDraw.Draw(overlay)
  for y,row in enumerate(self.grid):
   for x,v in enumerate(row):
    if v:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(255,30,30,75),outline=(255,30,30,180))
  Image.alpha_composite(col,overlay).save(P/'review/collision.png')
  card=Image.new('RGB',(1024,1024),'#17242a');card.paste(occupied,(0,70));d=ImageDraw.Draw(card);d.text((24,14),self.id+' / '+self.title,font=ImageFont.truetype(FONT,26),fill='white');d.text((24,48),'Native32 authorable candidate | decoded atlas proof | live playtest pending',font=ImageFont.truetype(FONT,15),fill='#c9d7da');d.text((24,986),'Actual repository Wokas. Standing frames; illustrative facings. No activity mechanics or animation.',font=ImageFont.truetype(FONT,15),fill='#c9d7da');card.save(P/'review/review.png')
  # Exhaustive integer spawn domains, body x +/-8, y..y+16.
  def clear(x,y):return all(0<=xx<C and 0<=yy<N and self.grid[yy][xx]==0 for yy in range(y//32,(y+15)//32+1) for xx in range((x-8)//32,(x+7)//32+1))
  assert all(clear(x,y) for y in range(self.start[1]-16,self.start[1]+18) for x in range(self.start[0]-16,self.start[0]+18))
  assert all(clear(a['x'],a['y']) for a in self.anchors)
  js(P/'validation/static.json',dict(atlasRoundtrip=True,spawnDomainPositions=1156,allSpawnBodiesClear=True,anchorBodiesClear=True,nativeFramePixels=[32,32],standingOnly=True,automaticFacing=False,animation=False,livePlaytest=False,proof='Decoded current TMJ atlases with hash-verified varied repository frames',foreground='Only bounded canopy pixels; floors below floorLayer',objectFootprints=self.objects))
  print(self.id,'built',len(self.anchors),'anchors',flush=True)

def N01_atlas():
 crops=dict(floor=[42,47,299,294],terrace=[349,52,592,292],wall=[652,54,895,291],outer=[959,58,1200,290],fireplace=[12,307,346,660],table=[399,475,703,660],seat1=[767,464,950,656],seat2=[1015,458,1208,656],couch=[20,710,501,924],sidecouch=[540,700,728,925],tree=[767,653,972,955],plant=[1038,676,1224,935],rack=[27,943,335,1213],window=[347,946,707,1214],logs=[716,1024,909,1205],rug=[918,972,1231,1207])
 m=Map('N01','Ember Ridge Lodge',crops);m.fill('outer',0,0,C,N);m.perimeter();m.fill('terrace',2,3,28,22);m.fill('floor',6,7,20,14)
 m.wall(6,6,20);m.wall(6,7,1,14);m.wall(25,7,1,14);m.wall(6,21,8);m.wall(19,21,7)
 m.sprite('window',8,5,5,2);m.sprite('window',19,5,5,2);m.sprite('fireplace',14,6,4,4);m.sprite('rug',10,11,12,8,False);m.sprite('table',14,13,4,2);m.sprite('rack',7,18,3,2);m.sprite('logs',21,8,3,2)
 for x,y,d,k in [(12,12,'east','seat1'),(12,15,'east','seat2'),(19,12,'west','seat2'),(19,15,'west','seat1'),(15,11,'south','seat1'),(17,17,'north','seat2')]:m.seat(x,y,d,k)
 for x,y in [(2,2),(27,2),(2,18),(28,18)]:m.sprite('tree',x,y,2,4,True,True)
 for x,y in [(8,3),(22,3),(3,10),(28,10)]:m.sprite('plant',x,y,1,2,True,True)
 m.sprite('table',11,23,3,1);m.seat(10,23,'east');m.seat(15,23,'west','seat2');m.anchor('arrival',16,24);m.anchor('west-terrace',4,15);m.anchor('east-terrace',27,15);m.anchor('snow-view',16,3);m.finish()
def N02_atlas():
 crops=dict(floor=[32,35,306,300],terrace=[346,35,606,294],wall=[647,34,926,298],outer=[967,38,1226,294],fountain=[24,316,315,605],table=[359,330,610,595],seat1=[661,340,922,589],seat2=[971,329,1229,593],canopy=[26,622,313,902],divan=[327,653,648,899],tree=[650,590,945,913],plant=[977,620,1226,906],lantern=[86,919,253,1229],arch=[356,913,609,1227],tea=[648,925,935,1218],rug=[964,924,1228,1219])
 m=Map('N02','Lantern Dune Majlis',crops);m.fill('outer',0,0,C,N);m.perimeter();m.fill('terrace',3,3,26,22);m.fill('floor',11,7,10,14)
 m.sprite('fountain',14,11,4,4);m.sprite('rug',4,9,6,10,False);m.sprite('rug',22,8,6,10,False);m.sprite('table',6,12,2,2);m.sprite('tea',24,11,2,2)
 for x,y,d,k in [(5,11,'east','seat1'),(8,11,'west','seat2'),(5,15,'east','seat2'),(8,15,'west','seat1'),(23,10,'east','seat2'),(26,10,'west','seat1'),(23,14,'east','seat1'),(26,14,'west','seat2'),(14,18,'north','seat1'),(17,18,'north','seat2')]:m.seat(x,y,d,k)
 for x,y in [(3,2),(26,2),(3,20),(27,20)]:m.sprite('tree',x,y,2,4,True,True)
 for x,y in [(11,4),(19,4),(11,21),(20,21)]:m.sprite('lantern',x,y,1,2)
 m.wall(5,5,7);m.wall(20,5,7);m.sprite('canopy',13,3,6,3,False,True);m.block(13,5,1,1);m.block(18,5,1,1)
 m.anchor('arrival',16,24);m.anchor('fountain-west',12,13);m.anchor('fountain-east',19,13);m.anchor('north-court',16,7);m.finish()
def N03_atlas():
 crops=dict(floor=[48,46,288,294],terrace=[349,43,609,301],wall=[662,44,909,296],outer=[971,40,1211,300],kiln=[25,307,303,604],table=[345,345,658,611],seat1=[715,368,898,594],seat2=[979,367,1212,594],wheel=[39,643,300,905],rack=[357,630,613,912],tree=[649,611,943,930],plant=[975,633,1215,911],shelf=[39,932,311,1224],window=[336,916,621,1221],sink=[649,940,944,1212],rug=[968,929,1219,1211])
 m=Map('N03','Clay Circle Atelier',crops);m.fill('outer',0,0,C,N);m.perimeter();m.fill('terrace',4,4,24,21);m.fill('floor',5,6,22,14)
 m.wall(4,5,23);m.wall(4,6,1,14);m.wall(27,5,1,15);m.wall(4,20,11);m.wall(19,20,9);m.wall(21,6,1,5)
 m.sprite('window',7,4,5,2);m.sprite('window',14,4,5,2);m.sprite('kiln',23,6,3,3);m.sprite('rack',23,10,3,2);m.sprite('sink',5,7,3,2);m.sprite('shelf',5,16,3,3)
 m.sprite('table',10,9,7,2);m.sprite('table',12,15,6,2);m.sprite('wheel',20,14,2,2);m.sprite('wheel',23,16,2,2)
 for x,y,d in [(10,8,'south'),(13,8,'south'),(16,8,'south'),(10,12,'north'),(14,12,'north'),(13,18,'north'),(16,18,'north'),(20,17,'north'),(24,19,'north')]:m.seat(x,y,d)
 m.sprite('rug',8,22,4,3,False);m.seat(8,23,'east','seat2');m.seat(11,23,'west','seat2')
 for x,y in [(2,2),(28,2),(2,20),(28,20)]:m.sprite('tree',x,y,2,3,True,True)
 m.anchor('arrival',16,24);m.anchor('central-aisle',18,12);m.anchor('kiln-approach',25,13);m.anchor('courtyard',23,23);m.finish()
def N01():
 m=Map('N01','Ember Ridge Lodge',{});m.base=Image.open(R/'source/N01-scene-r2.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,744]
 spans={7:[(2,2),(29,29)],8:[(2,2),(9,12),(19,20),(29,30)],9:[(2,2),(8,12),(18,20),(29,30)],10:[(2,2),(7,20),(29,30)],11:[(2,2),(7,26),(29,30)],12:[(2,2),(7,26),(29,30)],13:[(2,2),(7,26),(29,30)],14:[(2,2),(5,26),(29,30)],15:[(2,2),(5,12),(15,16),(19,26),(29,30)],16:[(2,2),(6,12),(15,16),(19,26),(29,30)],17:[(1,2),(15,16),(29,30)],18:[(1,2),(14,17),(29,30)],19:[(2,3),(6,7),(14,17),(24,25),(28,29)],20:[(2,7),(12,18),(24,29)],21:[(3,12),(14,17),(19,28)],22:[(6,11),(14,17),(20,25)],23:[(10,21)],24:[(12,18)],25:[(13,17)],26:[(14,17)],27:[(14,17)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(9,8,1,1)
 # Allow middle room circulation north/south of the circles.
 for y in [9,10]:
  for x in range(21,27):
   if y==10:m.grid[y][x]=0
 for x in range(13,18):m.grid[10][x]=0
 # Bounded chimney/upper lintel depth only; no floor or rugs in foreground.
 box=(446,111,579,267);m.fore.alpha_composite(m.base.crop(box),box[:2]);m.objects=[dict(asset='full composed architecture',depth='bounded chimney',foregroundBox=box),dict(asset='scenery / structure collision',method='manually reviewed row spans; no broad foreground floors')]
 for i,(x,y,d) in enumerate([(312,388,'east'),(408,388,'west'),(312,452,'east'),(408,452,'west'),(616,388,'east'),(712,388,'west'),(616,452,'east'),(712,452,'west')]):m.anchors.append(dict(id='cushion-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',520,744),('hearth-approach',520,328),('service-approach',784,352),('west-snow-path',80,456),('east-snow-path',944,456),('threshold',520,608)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N02():
 m=Map('N02','Lantern Dune Majlis',{});m.base=Image.open(R/'source/N02-scene-r3.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[328,808]
 spans={8:[(5,6),(9,13)],9:[(4,15)],10:[(3,23)],11:[(3,14),(22,24)],12:[(3,14),(22,24)],13:[(3,14),(22,24)],14:[(3,14),(22,24)],15:[(3,14),(22,24),(28,29)],16:[(4,15),(21,24),(27,29)],17:[(5,22),(26,29)],18:[(7,21),(26,28)],19:[(8,18),(25,27)],20:[(8,11),(14,18),(25,26)],21:[(8,11),(18,21),(24,25)],22:[(8,11),(19,25)],23:[(8,11),(20,25)],24:[(8,13),(22,25)],25:[(8,13),(25,26)],26:[(9,13),(26,27)],27:[(10,15),(26,27)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 # Garden stair connector passes behind its low wall and alongside the fountain court.
 for x,y in [(26,17),(26,19),(25,20),(22,22),(21,23),(21,24),(22,24),(24,25),(25,25)]:m.grid[y][x]=0
 m.block(29,15,1,1);m.block(23,22,1,1)
 # Northern arcade lintel only; no floor or rug in foreground.
 box=(290,122,497,201);m.fore.alpha_composite(m.base.crop(box),box[:2]);m.objects=[dict(asset='full composed arcade/courtyard/garden',collision='manually authored native32 rows'),dict(asset='arcade lintel',foregroundBox=box)]
 seats=[(264,320,'south'),(184,352,'east'),(344,352,'west'),(184,448,'east'),(344,448,'west'),(264,480,'north'),(904,520,'east'),(944,544,'west'),(784,712,'east'),(824,736,'west')]
 for i,(x,y,d) in enumerate(seats):m.anchors.append(dict(id='cushion-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',328,808),('courtyard-entry',328,616),('fountain-west',456,424),('fountain-east',744,424),('tea-approach',680,328),('garden-junction',648,680)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N03():
 m=Map('N03','Clay Circle Atelier',{});m.base=Image.open(R/'source/N03-empty-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[616,680]
 spans={7:[(31,31)],8:[(31,31)],9:[(8,23),(31,31)],10:[(8,23),(31,31)],11:[(7,25),(31,31)],12:[(6,25),(31,31)],13:[(3,25),(31,31)],14:[(3,25),(31,31)],15:[(9,25),(31,31)],16:[(12,26),(31,31)],17:[(18,20),(31,31)],18:[(18,20),(31,31)],19:[(18,20),(31,31)],20:[(18,20),(31,31)],21:[(17,20),(31,31)],22:[(14,20),(31,31)],23:[(10,16),(18,20),(31,31)],24:[(8,11),(14,15),(20,22),(30,31)],25:[(4,10),(22,30)],26:[(1,8)],27:[(2,7)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 # Bridge landings, stair turns and garden path form one admitted connected network.
 for x,y in [(17,22),(17,23),(16,24),(12,24),(13,24),(19,23),(20,23),(21,23),(21,24),(22,24),(23,24),(30,24),(30,23)]:m.grid[y][x]=0
 # Protect the real bridge south parapet and keep travel on its clear north deck.
 for x,y in [(13,23),(14,23),(15,23),(16,23),(17,23),(12,24),(13,24),(14,24),(15,24),(16,24)]:m.grid[y][x]=1
 for x,y in [(12,22),(13,22)]:m.grid[y][x]=0
 m.block(4,25,1,1)
 # Original generated pottery kit, recomposed at exact native footprints.
 kit=Image.open(R/'source/N03-original.png').convert('RGBA');stool=kit.crop((715,368,898,594));stool=stool.crop(stool.getbbox()).resize((24,30),Image.Resampling.LANCZOS);table=kit.crop((345,345,658,611));m.assets['clay-worktable']=table.crop(table.getbbox());m.sprite('clay-worktable',16,12,3,2)
 for x,y in [(488,360),(632,360),(488,396),(632,396),(488,452),(632,452)]:m.base.alpha_composite(stool,(x-12,y))
 # Pottery kiln hood stays above actors without any floor pixels.
 box=(808,137,921,239);m.fore.alpha_composite(m.base.crop(box),box[:2]);m.objects=[dict(asset='full atelier / canal garden / bridge',collision='manually authored native32 row spans'),dict(asset='kiln hood',foregroundBox=box)]
 seats=[(488,360,'east'),(632,360,'west'),(488,396,'east'),(632,396,'west'),(488,452,'east'),(632,452,'west'),(136,424,'east'),(208,424,'west')]
 for i,(x,y,d) in enumerate(seats):m.anchors.append(dict(id='seat-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',616,680),('clay-table-approach',552,456),('workbench-approach',520,296),('kiln-approach',744,328),('bridge',328,744),('east-garden',1000,648)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N04():
 m=Map('N04','Glassleaf Cooking Club',{});m.base=Image.open(R/'source/N04-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[368,808]
 spans={5:[(1,1)],6:[(1,1)],7:[(1,1),(5,17),(20,26),(31,31)],8:[(1,1),(5,17),(20,26),(31,31)],9:[(1,1),(5,17),(20,26),(31,31)],10:[(1,1),(5,17),(20,26),(31,31)],11:[(1,1),(5,18),(20,26),(31,31)],12:[(1,1),(5,18),(20,26),(31,31)],13:[(1,1),(6,17),(21,26),(31,31)],14:[(1,1),(7,16),(21,27),(31,31)],15:[(1,1),(10,12),(22,25),(31,31)],16:[(1,1),(10,12),(23,25),(31,31)],17:[(1,1),(10,12),(23,25),(31,31)],18:[(1,2),(10,12),(23,25),(30,31)],19:[(2,30)],20:[(10,13),(28,29)],21:[(10,13),(29,30)],22:[(10,13),(29,30)],23:[(10,13),(30,31)],24:[(10,13),(30,31)],25:[(10,13),(31,31)],26:[(10,13)],27:[(9,14)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(6,7,4,3);m.block(10,10,4,3)
 box=(178,79,595,123);m.fore.alpha_composite(m.base.crop(box),box[:2]);m.objects=[dict(asset='herb island',collision=[6,7,4,3]),dict(asset='communal preparation island',collision=[10,10,4,3]),dict(asset='greenhouse upper iron lintel',foregroundBox=box)]
 # Semantic flowered gateway garland mask: outlined band, with beige paving rejected.
 mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask);poly=[(310,716),(327,712),(333,706),(341,713),(350,706),(358,713),(364,705),(372,713),(380,706),(387,713),(395,704),(404,714),(414,709),(422,717),(434,713),(444,725),(451,750),(445,773),(431,767),(421,751),(414,743),(403,740),(394,732),(387,738),(379,735),(373,747),(365,736),(353,737),(345,744),(337,751),(330,768),(317,774),(310,749)]
 md.polygon(poly,fill=255);pixels=m.base.load();mp=mask.load()
 for yy in range(700,778):
  for xx in range(305,455):
   if mp[xx,yy]:
    r,g,b,_=pixels[xx,yy]
    if not ((r<160 and g<170) or g>r*1.01 or (abs(r-g)<22 and abs(g-b)<24)):mp[xx,yy]=0
 garland=m.base.copy();garland.putalpha(mask);m.fore.alpha_composite(garland);m.objects.append(dict(asset='flowered gateway overhead garland',foregroundPolygon=poly,selection='Dark/green/neutral flower pixels only within traced band; beige paving rejected'))
 seats=[(336,296,'south'),(440,296,'south'),(328,424,'north'),(456,424,'north'),(728,256,'east'),(776,256,'west'),(728,332,'east'),(776,332,'west'),(744,424,'east'),(792,424,'west')]
 for i,(x,y,d) in enumerate(seats):m.anchors.append(dict(id='seat-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',368,808),('arch-north',368,704),('arch-under',368,736),('arch-south',368,768),('prep-approach',488,360),('herb-approach',344,232),('terrace-serving',840,360),('garden-junction',520,616),('west-path',48,456),('east-path',1000,456)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N05():
 m=Map('N05','Dicewood Table Club',{});m.base=Image.open(R/'source/N05-empty-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[712,840]
 spans={7:[(4,20)],8:[(4,20),(23,27),(31,31)],9:[(4,20),(23,27),(31,31)],10:[(4,20),(23,27),(31,31)],11:[(4,20),(22,27),(31,31)],12:[(4,20),(22,23),(31,31)],13:[(4,23),(31,31)],14:[(4,23),(31,31)],15:[(5,17),(20,23),(31,31)],16:[(5,17),(20,23),(31,31)],17:[(9,17),(20,23),(31,31)],18:[(9,16),(20,23),(31,31)],19:[(9,16),(20,24),(30,31)],20:[(9,15),(19,25),(30,31)],21:[(12,15),(19,25),(29,31)],22:[(12,15),(20,24),(28,31)],23:[(12,15),(20,24),(28,31)],24:[(15,15),(19,25),(28,31)],25:[(18,31)],26:[(18,31)],27:[(18,31)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 kit=Image.open(R/'source/N05-furniture-kit.png').convert('RGBA')
 for name,box in [('game-table-a',(126,80,681,594)),('game-table-b',(870,85,1410,590)),('stool-teal',(265,665,522,946)),('stool-red',(1007,665,1270,942))]:
  im=kit.crop(box);m.assets[name]=im.crop(im.getbbox())
 for x,y,k in [(7,10,'game-table-a'),(16,10,'game-table-b'),(12,15,'game-table-b')]:m.sprite(k,x,y,3,2)
 seats=[]
 for i,(cx,cy) in enumerate([(264,328),(552,328),(424,488)]):
  for x,y,d in [(cx,cy-40,'south'),(cx-64,cy,'east'),(cx+80,cy,'west'),(cx,cy+64,'north')]:
   # Map-specific positions are exact native fitted endpoints; table stations have walkable approaches.
   stool=m.assets['stool-teal' if i==0 else 'stool-red'].resize((32,34),Image.Resampling.LANCZOS);m.base.alpha_composite(stool,(x-16,y-2));seats.append((x,y,d))
 seats += [(808,268,'east'),(872,296,'west')]
 for i,(x,y,d) in enumerate(seats):m.anchors.append(dict(id='seat-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 # Glass canopy owns its bounded roof polygon, frame opaque and glazing translucent.
 poly=[(559,612),(613,593),(790,593),(839,616),(848,648),(558,648)];mask=Image.new('L',(W,H));ImageDraw.Draw(mask).polygon(poly,fill=1);roof=Image.new('RGBA',(W,H));rp=roof.load();mp=mask.load();bp=m.base.load()
 for yy in range(590,650):
  for xx in range(555,852):
   if mp[xx,yy]:
    r,g,b,_=bp[xx,yy];rp[xx,yy]=(r,g,b,255 if max(r,g,b)<100 else 105)
 # Conservative admitted-native-head envelope fades overhead frame/glazing only where heads can pass.
 head=Image.new('L',(W,H));hd=ImageDraw.Draw(head)
 for yy,row in enumerate(m.grid):
  for xx,v in enumerate(row):
   if not v:hd.rectangle((xx*32-8,yy*32-16,xx*32+40,yy*32+17),fill=255)
 hp=head.load()
 for yy in range(590,650):
  for xx in range(555,852):
   if hp[xx,yy] and rp[xx,yy][3]:rp[xx,yy]=(*rp[xx,yy][:3],min(65,rp[xx,yy][3]))
 m.fore.alpha_composite(roof);m.objects.append(dict(asset='entrance glass canopy',foregroundPolygon=poly,glazingAlpha=105,frameAlpha=255))
 for id,x,y in [('arrival',712,840),('canopy-under',712,616),('canopy-north',712,584),('canopy-south',712,648),('canopy-west',680,616),('canopy-east',744,616),('main-stairs',712,520),('game-aisle',424,328),('quiet-alcove',744,360),('east-alley',1000,616)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N06():
 m=Map('N06','Copperbeat Rehearsal',{});m.base=Image.open(R/'source/N06-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[728,808]
 spans={3:[(2,2),(29,29)],4:[(2,2),(29,29)],5:[(2,2),(29,29)],6:[(2,2),(29,29)],7:[(1,2),(29,30)],8:[(1,2),(8,20),(22,26),(29,30)],9:[(1,2),(5,19),(21,26),(29,30)],10:[(1,1),(5,26),(30,31)],11:[(1,1),(5,20),(22,26),(30,31)],12:[(1,1),(5,20),(30,31)],13:[(1,1),(5,20),(30,31)],14:[(1,1),(13,13),(19,19),(30,31)],15:[(1,1),(13,13),(19,26),(30,31)],16:[(1,1),(5,15),(19,27),(30,31)],17:[(1,1),(5,15),(19,27),(30,31)],18:[(1,1),(5,15),(19,27),(30,31)],19:[(1,1),(6,15),(19,27),(30,31)],20:[(1,1),(22,23),(30,31)],21:[(1,1),(22,23),(30,31)],22:[(1,1),(22,23),(30,31)],23:[(1,1),(21,24),(30,31)],24:[(1,1),(20,26),(30,31)],25:[(1,31)],26:[(1,31)],27:[(1,31)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(10,17,2,3)
 # Booth's physical south glazing, not an arbitrary floor rectangle.
 box=(684,337,907,402);roof=Image.new('RGBA',(W,H));rp=roof.load();bp=m.base.load()
 for yy in range(box[1],box[3]):
  for xx in range(box[0],box[2]):
   r,g,b,_=bp[xx,yy];frame=yy<345 or yy>394 or xx<691 or xx>899 or 759<xx<767 or 821<xx<830;rp[xx,yy]=(r,g,b,255 if frame else 90)
 # Head-readable transparent glazing across every admitted body/head envelope.
 head=Image.new('L',(W,H));hd=ImageDraw.Draw(head)
 for yy,row in enumerate(m.grid):
  for xx,v in enumerate(row):
   if not v:hd.rectangle((xx*32-8,yy*32-16,xx*32+40,yy*32+17),fill=255)
 hp=head.load()
 for yy in range(box[1],box[3]):
  for xx in range(box[0],box[2]):
   if hp[xx,yy] and rp[xx,yy][3]:rp[xx,yy]=(*rp[xx,yy][:3],min(65,rp[xx,yy][3]))
 m.fore.alpha_composite(roof);m.objects=[dict(asset='lounge tea tables',collision=[10,17,2,3]),dict(asset='control booth south glass',foregroundBox=box,frameAlpha=255,glassAlpha=90)]
 seats=[(760,256,'north'),(808,256,'north'),(248,520,'east'),(424,520,'west'),(248,584,'east'),(424,584,'west')]
 for i,(x,y,d) in enumerate(seats):m.anchors.append(dict(id='seat-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',728,808),('rehearsal-center',424,328),('piano-approach',584,264),('guitar-approach',520,264),('control-window',760,360),('lounge-entry',424,488),('entry-hall',744,552),('west-alley',48,616),('east-alley',1000,616)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N07():
 m=Map('N07','Harbor Tongues Exchange',{});m.base=Image.open(R/'source/N07-scene-r2.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,776]
 spans={7:[(3,5),(27,28)],8:[(2,4),(7,24),(27,29)],9:[(2,4),(7,24),(27,29)],10:[(2,29)],11:[(2,4),(7,24),(27,29)],12:[(2,4),(7,24),(27,29)],13:[(2,4),(7,24),(27,29)],14:[(2,4),(14,16),(27,29)],15:[(2,11),(14,16),(20,29)],16:[(14,17)],17:[(14,17)],18:[(14,17)],19:[(14,17)],20:[(14,17)],21:[(14,17)],22:[(14,17)],23:[(14,17)],24:[(14,17)],25:[(14,17)],26:[(13,18)],27:[(0,31)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(19,12,6,2)
 for box in [(215,451,411,474),(587,451,821,474)]:m.fore.alpha_composite(m.base.crop(box),box[:2])
 head=Image.new('L',(W,H));hd=ImageDraw.Draw(head)
 for yy,row in enumerate(m.grid):
  for xx,v in enumerate(row):
   if not v:hd.rectangle((xx*32-8,yy*32-16,xx*32+40,yy*32+17),fill=255)
 hp=head.load();fp=m.fore.load()
 for yy in range(H):
  for xx in range(W):
   if hp[xx,yy] and fp[xx,yy][3]:fp[xx,yy]=(*fp[xx,yy][:3],min(65,fp[xx,yy][3]))
 m.objects=[dict(asset='display shelf',collision=[19,12,6,2]),dict(asset='solid southern blue/white railing panels',foregroundBoxes=[[215,451,411,474],[587,451,821,474]])]
 seats=[(264,256,'east'),(360,256,'west'),(360,288,'north'),(664,256,'east'),(744,256,'west'),(264,416,'east'),(312,424,'north'),(360,416,'west')]
 for i,(x,y,d) in enumerate(seats):m.anchors.append(dict(id='cushion-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',520,776),('compass-discussion',520,360),('north-aisle',488,264),('west-boardwalk',112,424),('east-boardwalk',904,424),('pier-midpoint',520,648),('quay',520,872)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N08():
 m=Map('N08','Mosswater Tea House',{});m.base=Image.open(R/'source/N08-scene-r2.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[360,744]
 spans={7:[(6,15)],8:[(6,28)],9:[(6,28)],10:[(7,14),(25,28)],11:[(9,12),(26,27)],12:[(10,11),(27,27)],13:[(10,11),(27,27)],14:[(10,11),(27,27)],15:[(10,11),(27,27)],16:[(10,11),(27,27)],17:[(10,11),(26,28)],18:[(10,11),(25,29)],19:[(10,11),(26,28)],20:[(10,11),(27,28)],21:[(10,11),(27,28)],22:[(9,12),(27,28)],23:[(0,31)],24:[(9,12)],25:[(10,11)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.fore.alpha_composite(m.base.crop((150,82,520,108)),(150,82))
 # The open-air bridge replaces canopy/posts so head visibility and generous horizontal circulation are structural.
 m.objects=[dict(asset='tatami rooms, open cedar bridge, pond walks',collision='manually reviewed native32 floor spans; pond, screens, counters, foliage and rails excluded')]
 for i,(x,y,d) in enumerate([(280,256,'east'),(408,256,'west'),(280,296,'east'),(408,296,'west'),(280,328,'east'),(408,328,'west'),(840,296,'east'),(888,296,'west')]):m.anchors.append(dict(id='zabuton-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',360,744),('tea-preparation',360,232),('open-bridge',648,296),('main-tatami',360,296),('south-deck',360,584),('garden-bay',872,584),('east-garden',872,456),('stone-crossing',616,744)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N09():
 m=Map('N09','Turntable Dance Loft',{});m.base=Image.open(R/'source/N09-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,840]
 spans={5:[(3,29)],6:[(2,29)],7:[(2,29)],8:[(2,29)],9:[(2,6),(8,29)],10:[(2,6),(8,29)],11:[(2,6),(8,29)],12:[(2,29)],13:[(2,6),(8,29)],14:[(2,6),(8,29)],15:[(2,6),(8,29)],16:[(14,17),(25,26)],17:[(14,17),(25,26)],18:[(2,3),(14,17),(25,27)],19:[(2,3),(7,29)],20:[(2,3),(7,29)],21:[(2,3),(7,29)],22:[(2,3),(14,17),(30,31)],23:[(2,3),(14,17),(30,31)],24:[(1,3),(14,17),(30,31)],25:[(1,3),(14,17),(30,31)],26:[(1,31)],27:[(1,31)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(5,10,1,2)
 # DJ equipment is solid. Its broad stage approach remains separate from the sprung floor.
 m.fore.alpha_composite(m.base.crop((300,1,989,30)),(300,1));m.objects=[dict(asset='listening lounge side table',collision=[5,10,1,2]),dict(asset='loft windows and brick lintel',foregroundBox=[300,1,989,30]),dict(asset='floor and garden patio',collision='native32 floor spans exclude equipment, walls, window sills, terrace planters and stairs parapets')]
 for i,(x,y) in enumerate([(120,256),(168,256),(120,352),(120,448),(168,448)]):m.anchors.append(dict(id='lounge-chair-'+str(i+1),x=x,y=y,direction='south',kind='seat'))
 for id,x,y in [('arrival',520,840),('dance-center',616,360),('dj-approach',232,200),('mirror-side',296,392),('window-side',808,200),('entry-doors',520,584),('patio',744,648),('side-entry',840,552),('west-pavement',104,744),('east-pavement',1000,744)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N10():
 m=Map('N10','Silvergrain Photo Club',{});m.base=Image.open(R/'source/N10-scene-r2.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,840]
 spans={6:[],7:[],8:[(22,23),(25,28)],9:[(3,19),(22,28)],10:[(3,19),(22,28)],11:[(3,19),(22,28)],12:[(3,19),(22,28)],13:[(3,19),(22,28)],14:[(3,19),(23,27)],15:[(3,19),(23,26)],16:[(4,26)],17:[(4,26)],18:[(14,17),(27,28)],19:[(14,17),(28,29)],20:[(14,17),(28,29)],21:[(2,6),(14,17),(28,29)],22:[(2,6),(14,17),(28,29)],23:[(3,8),(13,18),(28,29)],24:[(1,31)],25:[(1,31)],26:[(0,31)],27:[(0,31)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 for box in [(7,11,2,4),(15,11,2,4),(7,8,4,2),(13,8,3,2),(17,8,3,2),(3,8,1,1),(5,17,1,1)]:m.block(*box)
 m.block(5,21,3,1);m.block(22,8,7,3);m.block(28,11,1,3)
 # Northern exhibition lighting rail is above architecture, never over a reachable head.
 m.fore.alpha_composite(m.base.crop((132,159,607,174)),(132,159));m.objects=[dict(asset='photo review tables',collision=[[7,11,2,4],[15,11,2,4]]),dict(asset='north exhibition benches',collision=[[7,8,4,1],[13,8,3,1],[17,8,3,1]]),dict(asset='salon side furniture',collision=[5,17,1,1]),dict(asset='north light rail',foregroundBox=[132,159,607,174])]
 for i,(x,y,d) in enumerate([(200,384,'east'),(304,384,'west'),(200,448,'east'),(304,448,'west'),(248,335,'south'),(456,384,'east'),(552,384,'west'),(456,448,'east'),(552,448,'west'),(504,335,'south'),(136,552,'south'),(216,552,'south')]):m.anchors.append(dict(id='review-chair-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',520,840),('gallery-aisle',392,328),('print-wall',392,328),('darkroom-aisle',808,392),('darkroom-entry',776,488),('lobby',520,552),('front-stairs',520,712),('east-garden',936,712)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N11():
 m=Map('N11','Framehouse Film Society',{});m.base=Image.open(R/'source/N11-scene-r2.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,808]
 spans={0:[(2,2)],1:[(2,2)],2:[(2,2)],3:[(2,2)],4:[(2,2)],5:[(2,2)],6:[(2,2)],7:[(2,2),(9,16)],8:[(2,2),(7,17)],9:[(2,2),(6,17),(21,24)],10:[(2,2),(6,17),(20,26)],11:[(2,2),(6,17),(19,26)],12:[(2,2),(6,26)],13:[(2,2),(6,26)],14:[(2,2),(10,26)],15:[(2,2),(14,17),(22,24)],16:[(2,2),(14,17)],17:[(2,2),(7,8),(12,18),(21,24)],18:[(2,2),(6,8),(12,24)],19:[(2,2),(6,8),(12,24)],20:[(2,2),(14,17)],21:[(2,2),(14,17),(29,29)],22:[(2,29)],23:[(2,29)],24:[(0,31)],25:[(0,31)],26:[(0,31)],27:[(0,31)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 # Real lobby floor below the ticket booth connects its west bay to the central lobby.
 for x in range(6,13):m.grid[19][x]=0
 m.fore.alpha_composite(m.base.crop((365,62,483,112)),(365,62));m.objects=[dict(asset='Art Deco screen crown',foregroundBox=[365,62,483,112]),dict(asset='screening poufs',semantics='backless velvet native-fitting seats, no fixed foreground backrests'),dict(asset='walls, bar, ticket booth, screen and lamps',collision='native32 manually authored floor spans')]
 for y in [296,360]:
  for x in [310,360,399,440,488]:m.anchors.append(dict(id='screening-pouf-'+str(len(m.anchors)+1),x=x,y=y,direction='north',kind='seat'))
 for x,y,d in [(680,360,'east'),(776,360,'west'),(680,448,'east'),(776,448,'west'),(712,616,'north'),(744,616,'north')]:m.anchors.append(dict(id='salon-seat-'+str(len(m.anchors)+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',520,808),('screen-approach',424,264),('cinema-side-aisle',232,360),('discussion-center',744,392),('coffee-approach',840,392),('lobby-center',520,584),('west-lobby',248,616),('entrance',520,680),('west-sidewalk',136,744),('east-sidewalk',904,744)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N12():
 m=Map('N12','Tideglass Aquarium Hall',{});m.base=Image.open(R/'source/N12-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,808]
 spans={9:[(6,11),(17,18),(23,25)],10:[(6,25)],11:[(6,25)],12:[(6,28)],13:[(6,29)],14:[(6,29)],15:[(5,28)],16:[(6,26)],17:[(6,26)],18:[(7,25)],19:[(12,19)],20:[(6,26)],21:[(5,26)],22:[(5,26)],23:[(6,25)],24:[(7,24)],25:[(9,22)],26:[(9,22)],27:[(9,22)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 for box in [(7,9,1,1),(24,9,1,1),(12,10,5,1),(19,10,4,1),(7,20,1,1),(24,20,1,1),(11,18,2,3),(19,18,2,3)]:m.block(*box)
 # Kiosk and shell case are bounded solids at the tank edge, never floor overlays.
 m.fore.alpha_composite(m.base.crop((207,158,810,174)),(207,158));m.objects=[dict(asset='tank upper cornice',foregroundBox=[207,158,810,174]),dict(asset='tanks, kiosk, shell case and boardwalk edge planters',collision='native32 spans trace broad room and connected boardwalk; exhibits excluded')]
 for i,(x,y,d) in enumerate([(280,367,'east'),(360,367,'west'),(408,399,'west'),(248,424,'east'),(744,431,'south'),(808,456,'west'),(696,480,'east'),(776,512,'north')]):m.anchors.append(dict(id='marine-pouf-'+str(i+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',520,808),('tank-gallery',520,360),('curve-tank-view',200,456),('shell-display',680,360),('tidepool-view',808,360),('central-floor',520,488),('entry',520,616),('boardwalk-west',264,712),('boardwalk-east',808,712)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N13():
 m=Map('N13','Snowsteam Bathhouse',{});m.base=Image.open(R/'source/N13-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,808]
 spans={8:[(3,16),(19,19)],9:[(3,16),(19,19)],10:[(3,16),(19,19)],11:[(3,19)],12:[(3,16),(19,19)],13:[(3,16),(19,19)],14:[(3,16),(19,19)],15:[(3,15),(19,19)],16:[(7,11),(19,27)],17:[(7,11),(21,27)],18:[(7,11),(25,27)],19:[(7,11),(25,27)],20:[(4,28)],21:[(3,28)],22:[(2,29)],23:[(3,28)],24:[(4,26)],25:[(8,23)],26:[(11,19)],27:[(12,17)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(22,16,3,1)
 m.fore.alpha_composite(m.base.crop((65,144,574,162)),(65,144));m.objects=[dict(asset='cedar lintel',foregroundBox=[65,144,574,162]),dict(asset='three broad backless relaxation benches',semantics='usable low seating surfaces, clear surrounding aisles'),dict(asset='snow, lockers, bath and rocky garden',collision='native32 traced lounge, connecting doorway, stone terrace and expansive forecourt')]
 for y,xs in [(328,[152,200,232,344,376,408]),(424,[264,304,344])]:
  for x in xs:m.anchors.append(dict(id='cedar-bench-'+str(len(m.anchors)+1),x=x,y=y,direction='south',kind='seat'))
 for id,x,y in [('arrival',520,808),('locker-approach',264,264),('lounge-aisle',296,392),('pool-doorway',552,360),('pool-west',616,424),('pool-south',808,520),('stone-exit',840,616),('lodge-exit',296,584),('forecourt-west',200,712),('forecourt-east',872,712)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N14():
 m=Map('N14','Skylot Garden Commons',{});m.base=Image.open(R/'source/N14-scene-r2.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,840]
 spans={9:[(4,23)],10:[(4,27)],11:[(4,27)],12:[(4,28)],13:[(4,28)],14:[(4,28)],15:[(4,28)],16:[(6,28)],17:[(6,28)],18:[(6,28)],19:[(6,28)],20:[(9,28)],21:[(15,17)],22:[(15,17)],23:[(15,17)],24:[(15,17)],25:[(14,18)],26:[(13,19)],27:[(13,19)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 beds=[(4,9,6,3),(11,9,6,3),(4,13,6,2),(11,13,6,2),(4,16,6,3),(11,16,6,3)]
 for b in beds:m.block(*b)
 m.block(19,12,8,3)
 m.block(18,9,6,1);m.block(23,10,6,1)
 m.fore.alpha_composite(m.base.crop((771,174,898,196)),(771,174));m.objects=[dict(asset='raised vegetable beds',collision=beds),dict(asset='picnic tabletop',collision=[19,12,8,3]),dict(asset='scenic greenhouse ridge',foregroundBox=[771,174,898,196]),dict(asset='roof floor and stair landing',collision='whole connected broad paving manually traced; parapets, shed, glasshouse and planters excluded')]
 for y in [367,488]:
  for x in [680,744,808]:m.anchors.append(dict(id='picnic-bench-'+str(len(m.anchors)+1),x=x,y=y,direction='south' if y==367 else 'north',kind='seat'))
 for x,y in [(776,559),(840,527),(808,591),(872,584)]:m.anchors.append(dict(id='terracotta-stool-'+str(len(m.anchors)+1),x=x,y=y,direction='south',kind='seat'))
 for id,x,y in [('arrival',520,840),('garden-center',552,424),('crop-crosspath',328,392),('south-crops',520,616),('greenhouse-approach',680,328),('social-deck',648,552),('stair-top',520,648),('east-path',904,392)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N15():
 m=Map('N15','Threadwell Craft Studio',{});m.base=Image.open(R/'source/N15-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,712]
 spans={9:[(8,27)],10:[(8,28)],11:[(8,28)],12:[(3,28)],13:[(8,28)],14:[(8,28)],15:[(8,28)],16:[(8,28)],17:[(13,18)],18:[(13,18)],19:[(14,18)],20:[(0,31)],21:[(0,31)],22:[(0,31)],23:[(13,18)],24:[(13,18)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(12,12,8,3);m.block(17,15,2,1)
 for x in [1,6,10,21,24,29]:m.block(x,22,1,1)
 m.fore.alpha_composite(m.base.crop((153,225,874,239)),(153,225));m.objects=[dict(asset='cutting table',collision=[12,12,8,3]),dict(asset='hanging cloth edge',collision=[17,15,2,1]),dict(asset='courtyard bollards',collisionColumns=[1,6,10,21,24,29],row=22),dict(asset='upper fabric-shelf rail',foregroundBox=[153,225,874,239]),dict(asset='looms and fabric shelving',collision='excluded solid fixtures; broad studio floor admitted')]
 for x,y in [(456,352),(568,352),(456,512),(568,512),(744,416),(808,392),(856,424),(728,456),(872,456)]:m.anchors.append(dict(id='craft-stool-'+str(len(m.anchors)+1),x=x,y=y,direction='south',kind='seat'))
 for id,x,y in [('arrival',520,712),('north-loom',280,328),('south-loom',280,456),('fabric-library',520,320),('cutting-table-west',344,424),('stitch-circle',808,456),('entrance',520,584),('courtyard-west',200,680),('courtyard-east',808,680),('canal-steps',520,776)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N16():
 m=Map('N16','Rainveil Meditation',{});m.base=Image.open(R/'source/N16-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,776]
 spans={9:[(9,25)],10:[(9,25)],11:[(9,25)],12:[(3,25)],13:[(3,25)],14:[(3,25)],15:[(3,25)],16:[(4,8),(14,19)],17:[(14,19)],18:[(14,19)],19:[(8,24)],20:[(6,24)],21:[(5,24)],22:[(6,24)],23:[(8,23)],24:[(11,21)],25:[(14,19)],26:[(14,18)],27:[(14,18)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(9,15,5,1);m.block(19,15,7,1);m.block(19,16,1,3)
 m.fore.alpha_composite(m.base.crop((580,196,651,210)),(580,196));m.objects=[dict(asset='bamboo chime crossbar',foregroundBox=[580,196,651,210]),dict(asset='open L-shaped bamboo platform and stone arrival clearing',collision='full connected deck/steps/clearing spans; ferns, boundary rails, jungle and waterfall excluded')]
 for x,y in [(296,399),(360,367),(440,352),(520,335),(592,335),(664,352),(728,367),(792,399)]:m.anchors.append(dict(id='meditation-cushion-'+str(len(m.anchors)+1),x=x,y=y,direction='south',kind='seat'))
 for id,x,y in [('arrival',520,776),('waterfall-view',776,456),('bowl-shrine',392,296),('chime-approach',616,296),('west-platform',168,456),('meditation-aisle',520,424),('stairs',520,552),('clearing-west',296,680),('clearing-east',744,680)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
def N17():
 m=Map('N17','Neon Nickel Arcade',{});m.base=Image.open(R/'source/N17-scene.png').convert('RGBA');m.grid=[[1]*C for _ in range(N)];m.start=[520,808]
 spans={9:[(5,5)],10:[(4,29)],11:[(4,30)],12:[(4,30)],13:[(4,30)],14:[(4,30)],15:[(3,30)],16:[(3,30)],17:[(3,30)],18:[(9,22)],19:[(10,21)],20:[(8,23)],21:[(7,24)],22:[(6,25)],23:[(5,26)],24:[(4,27)],25:[(4,27)],26:[(4,27)],27:[(4,27)]}
 for y,ranges in spans.items():
  for a,b in ranges:
   for x in range(a,b+1):m.grid[y][x]=0
 m.block(10,13,3,3);m.block(19,13,4,3);m.block(4,10,1,5);m.block(9,19,2,3);m.block(21,19,3,3)
 m.fore.alpha_composite(m.base.crop((187,153,923,171)),(187,153));m.objects=[dict(asset='cocktail arcade tables',collision=[[10,13,3,3],[19,13,4,3]]),dict(asset='north cabinet trim',foregroundBox=[187,153,923,171]),dict(asset='arcade cabinets, snack counter, refrigerator and street planters',collision='native32 explicit broad room and forecourt spans exclude fixture footprints')]
 for x,y,d in [(296,448,'east'),(424,448,'west'),(600,448,'east'),(744,448,'west'),(968,392,'west'),(968,456,'west'),(968,520,'west'),(904,559,'north')]:m.anchors.append(dict(id='arcade-seat-'+str(len(m.anchors)+1),x=x,y=y,direction=d,kind='seat'))
 for id,x,y in [('arrival',520,808),('cabinet-row',520,328),('pinball-approach',808,328),('snack-approach',168,424),('social-center',520,488),('lounge-front',904,488),('open-doors',520,616),('forecourt-west',232,776),('forecourt-east',808,776)]:m.anchors.append(dict(id=id,x=x,y=y,direction='south',kind='route'))
 m.finish()
if __name__=='__main__':globals()[sys.argv[1]]()
