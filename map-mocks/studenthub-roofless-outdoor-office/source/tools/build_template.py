from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
import json, math, hashlib, shutil
R=Path(__file__).resolve().parents[1]; W,H=960,768; T=32
# Archive portability: make output folders on a clean checkout.
for folder in ["assets", "map/tilesets", "docs"]:
 (R/folder).mkdir(parents=True,exist_ok=True)
L={n:Image.new('RGBA',(W,H)) for n in ['ground','furniture','glass','structure']}; C=[[1]*30 for _ in range(24)]; manifest=[]
def down(im,size):
 assert size[0]<=im.width and size[1]<=im.height
 return im.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
def repeat(im,size):
 o=Image.new('RGBA',size)
 for y in range(0,size[1],im.height):
  for x in range(0,size[0],im.width):o.alpha_composite(im,(x,y))
 return o
def rect(layer,b,fill,outline=None,width=1,r=0):
 target=Image.new('RGBA',(W,H)) if layer=='ground' and isinstance(fill,tuple) and len(fill)==4 and fill[3]<255 else L[layer]
 d=ImageDraw.Draw(target);f=d.rounded_rectangle if r else d.rectangle
 f(b,fill=fill,outline=outline,width=width,**({'radius':r} if r else {}))
 if target is not L[layer]:L[layer].alpha_composite(target)
def line(layer,xy,fill,width=1):ImageDraw.Draw(L[layer]).line(xy,fill=fill,width=width)
def box(layer,texture,b):L[layer].alpha_composite(repeat(texture,(b[2]-b[0],b[3]-b[1])),b[:2])
def carve(x,y,w,h,value=0):
 for yy in range(y//32,(y+h+31)//32):
  for xx in range(x//32,(x+w+31)//32):C[yy][xx]=value
# Original materials: read at real material density; never enlarge a source.
m=Image.open(R/'art-source/materials-master.png').convert('RGBA');s=m.width//2
tex={n:down(m.crop(b),z) for n,b,z in [('stone',(0,0,s,s),(192,192)),('wood',(s,0,2*s,s),(192,192)),('soil',(0,s,s,2*s),(256,256)),('plaster',(s,s,2*s,2*s),(256,256))]}
for n,t in tex.items():t.save(R/'assets'/f'{n}.png')
grass=Image.open(R/'assets/grass-material-0.png').convert('RGBA');box('ground',grass,(0,0,W,H))
# One connected foundation, perimeter garden and short entrance.
rect('ground',(91,181,896,683),(20,30,24,68),r=32)
box('ground',tex['stone'],(96,176,896,656));box('ground',tex['stone'],(416,656,576,768))
carve(96,192,800,480);carve(416,640,160,128)
# Wide inner floor: no decorative routes separating coworkers.
rect('ground',(126,188,866,579),(124,110,78,255));box('ground',tex['stone'],(128,192,864,576))
# A single oak strip gives the shared rear workbench and meeting floor continuity.
box('ground',tex['wood'],(160,224,832,432))
# Pale stone spine continues from arrival, between the adjacent uses.
box('ground',tex['stone'],(480,224,576,576));line('ground',(480,224,480,575),(186,159,103,255),2);line('ground',(575,224,575,575),(186,159,103,255),2)
# Texture seam edge, little bevel and contact shadow, not an arbitrary colored stripe.
for y in [576,585]:line('ground',(128,y,447,y),(237,220,173,255),2);line('ground',(545,y,864,y),(237,220,173,255),2)
# Rear-wall floor contact and permanent footprint remain distinct from removable roof.
rect('ground',(128,216,864,225),(84,87,68,255));line('ground',(132,215,860,215),(204,183,132,255),2)
carve(128,160,736,64,1)
# Exact native props keep chairs close to table; floor approaches are separate.
def prop(n,x,y,layer='furniture',size=None):
 src=R/'assets'/f'{n}.png';im=Image.open(src).convert('RGBA')
 if size:im=down(im,size)
 L[layer].alpha_composite(im,(x,y));manifest.append({'asset':n,'x':x,'y':y,'width':im.width,'height':im.height,'layer':layer})
 dest=R/'assets'/f'{n}.png'
 if not dest.exists():shutil.copy2(src,dest)
 return im.size
# Small individual stations are neighbors on one back edge, not departments.
for x in [192,272]:
 prop('light-desk',x,232);prop('light-chair_n',x+17,268);carve(x,256,64,32,1)
# Shared four-person table is the core of the room.
for x in [362,420]:prop('light-chair_s',x,276)
prop('light-meeting_table',352,302)
for x in [362,420]:prop('light-chair_n',x,363)
carve(352,320,128,64,1)
# Adjoining four-person meeting room, only a few steps away.
for x in [682,740]:prop('light-chair_s',x,276)
prop('light-meeting_table',672,302)
for x in [682,740]:prop('light-chair_n',x,363)
carve(672,320,128,64,1)
# Warm compact conversation group: each seat faces the coffee table.
rug=Image.open(R/'assets/light-rug.png').convert('RGBA');rug=down(rug,(184,104));L['ground'].alpha_composite(rug,(192,438))
prop('couch_s',214,422);prop('coffee',239,478);prop('couch_w',295,474)
carve(224,448,64,32,1);carve(256,480,32,32,1);carve(320,480,32,32,1)
# A shared small shelf/refreshment edge, leaves grow beside the structure.
prop('light-desk',704,462);carve(704,480,64,32,1)
# Semantic glass panels, actual narrow vertical planes. Lower body/post portion below Woka.
def glass_h(x1,x2,y,height=52):
 rect('glass',(x1,y-height,x2,y),(109,176,164,27))
 for x in range(x1,x2+1,64):
  line('glass',(x,y-height,x,y),(60,101,93,175),2)
  line('glass',(x+8,y-height+5,min(x+31,x2),y-8),(236,247,212,67),1)
 line('structure',(x1,y-height,x2,y-height),(71,102,85,245),3)
 line('ground',(x1,y,x2,y),(87,97,73,255),4)
def glass_v(x,y1,y2):
 rect('glass',(x-12,y1,x+10,y2),(113,179,168,25))
 line('glass',(x-10,y1,x-10,y2),(89,132,116,140),2)
 line('ground',(x+8,y1,x+8,y2),(76,107,91,255),3)
 for y in range(y1,y2+1,64):line('glass',(x-10,y,x+10,y),(64,107,97,180),2)
# Transparent external sides and front; persistent shape survives roof adaptation.
glass_v(136,224,568);glass_v(856,224,568)
glass_h(136,448,576);glass_h(544,856,576)
carve(128,224,32,352,1);carve(832,224,32,352,1);carve(128,544,320,32,1);carve(544,544,320,32,1)
# Internal room has west entry at y352..416, readable from commons.
glass_v(584,224,352);glass_v(584,416,480);glass_h(584,832,480)
carve(576,224,32,128,1);carve(576,416,32,64,1);carve(576,480,256,32,1)
# Front foundations and amber lamps are anchored to posts, not freestanding stamps.
for x in [128,440,536,848]:
 rect('ground',(x,566,x+15,580),(113,115,85,255));box('structure',tex['plaster'],(x,517,x+16,567))
 line('structure',(x+2,519,x+2,566),(239,224,186,255),2)
 rect('structure',(x+4,503,x+12,521),(47,80,72,255),r=2);rect('structure',(x+6,506,x+10,518),(253,218,136,245))
# Independent original rear shell and roof cover, downsampled once to native footprint.
a=Image.open(R/'art-source/architecture-master.png').convert('RGBA')
back=a.crop((0,0,a.width,421));back=back.crop(back.getchannel('A').getbbox()); back=down(back,(736,160));L['structure'].alpha_composite(back,(128,64))
back.save(R/'assets/rear-shell.png')
# Original living garden kit: cropped components downsample once, no scene slicing.
g=Image.open(R/'art-source/garden-kit-master.png').convert('RGBA')
specs={'bed-a':((0,0,626,324),(160,84)),'bed-b':((628,0,1254,324),(160,84)),'corner-a':((44,324,607,722),(142,106)),'corner-b':((639,324,1208,723),(142,106)),'olive':((44,723,586,1254),(146,143)),'ferns':((630,752,1254,1240),(126,99))}
kit={}
for n,(b,z) in specs.items():
 a=g.crop(b);b2=a.getchannel('A').getbbox();a=a.crop(b2);a.thumbnail(z,Image.Resampling.LANCZOS);kit[n]=a;a.save(R/'assets'/f'{n}.png')
def plant(n,x,y):
 a=kit[n];L['structure'].alpha_composite(a,(x,y));manifest.append({'asset':n,'x':x,'y':y,'width':a.width,'height':a.height,'layer':'structure'})
# Joined planting follows the slab perimeter, with clear short arrival.
for n,x,y in [('bed-a',122,596),('bed-b',272,596),('bed-b',560,596),('bed-a',714,596),('corner-a',26,508),('corner-b',825,510),('olive',10,273),('olive',812,265),('ferns',58,160),('ferns',826,160)]:plant(n,x,y)
for b in [(96,608,320,64),(576,608,320,64),(64,544,64,128),(864,544,64,128),(96,288,64,128),(832,288,64,128)]:carve(*b,1)
# A few small fern clusters at room corners bring garden indoors without blocking windows.
for x,y in [(156,507),(786,512)]:prop('plant',x,y);carve((x//32)*32,544,32,32,1)
# Floor-level shadows connect furniture/building to materials. Roof shadow stays ground.
shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow);sd.rectangle((135,223,863,232),fill=(35,49,38,24));sd.rectangle((160,570,447,585),fill=(34,44,33,20));sd.rectangle((544,570,831,585),fill=(34,44,33,20));L['ground']=Image.alpha_composite(L['ground'],shadow)
# Atlas packs nonempty native32px cells, preserving semantic layers; no resampling in map.
cells={};tiles=[];data={}
for name,im in L.items():
 im.save(R/'assets'/f'layer-{name}.png');arr=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   tile=im.crop((x,y,x+T,y+T));key=tile.tobytes()
   if not tile.getchannel('A').getbbox():arr.append(0);continue
   if key not in cells:cells[key]=len(tiles)+1;tiles.append(tile)
   arr.append(cells[key])
 data[name]=arr
marker=len(tiles)+1;tiles.append(Image.new('RGBA',(32,32)));sets=[]
for i in range(math.ceil(len(tiles)/1024)):
 a=Image.new('RGBA',(1024,1024));chunk=tiles[i*1024:(i+1)*1024]
 for j,tile in enumerate(chunk):a.alpha_composite(tile,((j%32)*32,(j//32)*32))
 a.save(R/'map/tilesets'/f'proof-{i}.png');sets.append({'firstgid':i*1024+1,'name':f'proof-{i}','image':f'tilesets/proof-{i}.png','imagewidth':1024,'imageheight':1024,'tilewidth':32,'tileheight':32,'columns':32,'tilecount':1024,'margin':0,'spacing':0,'tiles':([{'id':marker-1-i*1024,'properties':[{'name':'collides','type':'bool','value':True}]}] if i*1024<marker<=(i+1)*1024 else [])})
layers=[]
def tl(n,arr):layers.append({'id':len(layers)+1,'name':n,'type':'tilelayer','width':30,'height':24,'x':0,'y':0,'visible':True,'opacity':1,'data':arr})
tl('permanent-collisions',[marker if z else 0 for row in C for z in row]);tl('ground',data['ground']);tl('furniture',data['furniture']);layers.append({'id':4,'name':'floorLayer','type':'objectgroup','objects':[],'visible':True,'opacity':1})
for n in ['glass','structure']:tl(n,data[n])
areas=[{'id':1,'name':'team-inside','class':'area','type':'area','x':160,'y':224,'width':672,'height':352,'properties':[]},{'id':2,'name':'start','class':'area','type':'area','x':448,'y':672,'width':96,'height':64,'properties':[{'name':'start','type':'bool','value':True}]},{'id':3,'name':'glass-meeting-room','class':'area','type':'area','x':608,'y':224,'width':224,'height':256}]
layers.append({'id':8,'name':'areas','type':'objectgroup','objects':areas,'visible':True,'opacity':1})
tmj={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','infinite':False,'width':30,'height':24,'tilewidth':32,'tileheight':32,'backgroundcolor':'#344335','layers':layers,'tilesets':sets,'properties':[],'nextlayerid':9,'nextobjectid':4}
(R/'map/studenthub-outdoor-office.tmj').write_text(json.dumps(tmj,separators=(',',':')))
layout={'width':W,'height':H,'spawn':{'x':496,'y':704},'building':{'x':160,'y':224,'width':672,'height':352},'waypoints':[{'name':'Entry garden','x':496,'y':624},{'name':'Shared commons','x':496,'y':480},{'name':'Work table front','x':400,'y':432},{'name':'Visible meeting room','x':736,'y':448,'role':'glass'},{'name':'Meeting table front','x':736,'y':432},{'name':'Rear workstation approach','x':528,'y':240},{'name':'Return through shared space','x':496,'y':480},{'name':'Exit restores roof','x':496,'y':704}],'referenceAvatars':[{'x':496,'y':336,'frame':1},{'x':624,'y':448,'frame':1},{'x':260,'y':320,'frame':1}]}
(R/'layout.json').write_text(json.dumps(layout,indent=2));(R/'docs/asset-placements.json').write_text(json.dumps(manifest,indent=2))
# Actual layer composition and unchanged avatar at native32px; not a generated mockup.
for roofOn in [False]:
 out=L['ground'].copy();out.alpha_composite(L['furniture']);greg=Image.open(R/'qa/greg.png').convert('RGBA')
 for p in ([{'x':496,'y':624,'frame':1}] if roofOn else layout['referenceAvatars']+[{'x':496,'y':496,'frame':1}]):
  frame=p['frame'];sp=greg.crop((frame*32,0,frame*32+32,32));out.alpha_composite(sp,(p['x']-16,p['y']-16))
 out.alpha_composite(L['glass']);out.alpha_composite(L['structure'])
 out.save(R/'docs'/'outdoor-native.png')
print(json.dumps({'uniqueTiles':len(tiles),'atlases':len(sets),'nativeWorld':[W,H],'collisionTiles':sum(map(sum,C))}))
