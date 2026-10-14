from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import json,math,random,shutil,hashlib
R=Path(__file__).resolve().parents[1];O=R/'map';L=json.load(open(R/'layout.json'));W,H=L['mapWidth'],L['mapHeight'];T=32
random.seed(37)
def save(im,name):
 p=O/'tilesets'/name;im.save(p);return 'tilesets/'+name
# Code-native continuous midnight terrain and fog. The entire finite world is painted.
bg=Image.new('RGBA',(256,256),(9,18,34,255));d=ImageDraw.Draw(bg)
for i in range(1800):
 x=random.randrange(256);y=random.randrange(256);v=random.randrange(7,24);d.point((x,y),fill=(v,v+10,v+22,255))
for i in range(15):
 x=random.randrange(256);y=random.randrange(256);d.ellipse((x,y,x+random.randrange(40,140),y+random.randrange(12,50)),fill=(12,25,44,255))
save(bg,'midnight-terrain.png')
markers=Image.new('RGBA',(64,32));ImageDraw.Draw(markers).rectangle((32,0,63,31),fill=(0,0,0,0));save(markers,'markers.png')
# Art normalization only: scale and crop to tile-aligned asset canvases; preserve supplied alpha.
def normalize(src,box,size,name):
 im=Image.open(src).convert('RGBA');im=im.crop(box) if box else im
 im.thumbnail(size,Image.Resampling.LANCZOS);out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,size[1]-im.height));save(out,name);return out
shutil.copyfile(R/'art-source/gate-environment.png',O/'tilesets/gate-ground.png')
shutil.copyfile(R/'art-source/town/plaza-ground.png',O/'tilesets/town-ground.png')
normalize(R/'art-source/gate-front-arch.png',None,(448,576),'gate-front.png')
interiors=R/'art-source/town/interiors-source.png';boxes=[(30,43,863,541),(925,68,1507,490),(911,558,1497,944)]
# Clean architecture from imagegen, original alpha silhouette preserved during asset assembly.
empty=Image.open(R/'art-source/town/interiors-empty-floor.png').convert('RGBA');empty.putalpha(Image.open(interiors).getchannel('A'));empty.save(O/'images/interiors-empty-alpha.png')
for b,box in zip(L['buildings'],boxes):normalize(O/'images/interiors-empty-alpha.png',box,(b['width'],b['height']),b['id']+'-interior.png')
furniture_specs={
 'studenthub':[((117,305,338,490),(96,96),64,128),((579,305,781,490),(96,96),288,128),((354,168,574,282),(128,64),160,64),((114,216,291,308),(96,64),64,64),((650,212,776,317),(64,64),320,64),((46,313,117,415),(32,64),32,160),((756,405,811,493),(32,64),384,160)],
 'cafe':[((976,278,1145,374),(96,64),64,160),((1280,280,1458,374),(96,64),224,160)],
 'archive':[((945,717,1087,884),(64,64),64,96),((1301,731,1443,887),(64,64),224,96)]
}
furniture_collision={}
for b in L['buildings']:
 feet=Image.new('RGBA',(b['width'],b['height']));tops=Image.new('RGBA',feet.size);furniture_collision[b['id']]=[]
 for i,(box,size,x,y) in enumerate(furniture_specs[b['id']]):
  obj=normalize(R/'art-source/town/interiors-furniture-alpha.png',box,size,b['id']+'-object-'+str(i)+'.png');cut=size[1]-32
  feet.alpha_composite(obj.crop((0,cut,size[0],size[1])),(x,y+cut));tops.alpha_composite(obj.crop((0,0,size[0],cut)),(x,y));furniture_collision[b['id']].append((x,y+cut,size[0],32))
 save(feet,b['id']+'-furniture-feet.png');save(tops,b['id']+'-furniture-canopies.png')

for b,box in zip(L['buildings'],[(24,10,897,593),(929,36,1513,498),(900,508,1511,959)]):normalize(R/'art-source/town/exteriors-source.png',box,(b['width'],b['height']),b['id']+'-roof.png')
# A native-sized, crisp signage system is deliberately code-native for legible exact names.
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
except:font=ImageFont.load_default()
signs=Image.new('RGBA',(1536,1024));sd=ImageDraw.Draw(signs)
for b in L['buildings']:
 x=b['doorX']-L['town']['origin']['x'];y=b['doorY']-L['town']['origin']['y']+18;text=b['label'];tw=sd.textbbox((0,0),text,font=font)[2];sd.rounded_rectangle((x-tw//2-12,y-2,x+tw//2+12,y+22),4,fill=(18,48,54,246),outline=(223,175,88,255),width=1);sd.text((x-tw//2,y),text,font=font,fill=(255,232,174,255))
sd.rounded_rectangle((698,873,838,899),5,fill=(14,46,57,230),outline=(135,224,234,255));sd.text((711,878),'The Butterfly Gate',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12),fill=(204,248,244,255))
save(signs,'town-details.png')
# Each focus veil is local, non-colliding, and leaves the active building entirely clear.
for b in L['buildings']:
 v=Image.new('RGBA',(1536,1024),(5,15,32,125));vd=ImageDraw.Draw(v);x=b['x']-2304;y=b['y']-512;vd.rounded_rectangle((x-24,y-36,x+b['width']+24,y+b['height']+48),25,fill=(0,0,0,0));save(v,b['id']+'-focus.png')
# Effects are transparent tile animations. Frames carry no collides properties.
def glow(w,h,points,frame=0):
 out=Image.new('RGBA',(w,h));dr=ImageDraw.Draw(out)
 for x,y,r in points:
  a=18+int(5*math.sin(frame*math.pi/4+x));dr.ellipse((x-r,y-r/3,x+r,y+r/3),fill=(255,191,76,a))
 return out.filter(ImageFilter.GaussianBlur(6))
gateLights=[(256,1439,62),(773,1439,62),(249,1107,55),(783,1107,55),(324,756,40),(700,756,40),(378,516,50),(644,516,50)]
townLights=[(120,135,62),(452,480,62),(1350,490,70),(780,670,60),(680,780,52),(870,780,52)]
save(glow(1024,1536,gateLights),'gate-steady.png');save(glow(1536,1024,townLights),'town-steady.png')
# Efficient atlas construction: only cells whose alpha changes are emitted, 8 consecutive frames per cell.
fx_specs=[]
def effect(name,frames,origin):
 tw,th=frames[0].width//32,frames[0].height//32;cells=[]
 for y in range(th):
  for x in range(tw):
   box=(x*32,y*32,x*32+32,y*32+32)
   if any(im.crop(box).getchannel('A').getbbox() for im in frames):cells.append((x,y))
 cols=32;n=len(cells)*len(frames);rows=math.ceil(n/cols);atlas=Image.new('RGBA',(cols*32,rows*32));animations=[]
 for i,(x,y) in enumerate(cells):
  ids=[]
  for f,im in enumerate(frames):
   k=i*len(frames)+f;atlas.alpha_composite(im.crop((x*32,y*32,x*32+32,y*32+32)),((k%cols)*32,(k//cols)*32));ids.append({'tileid':k,'duration':130 if 'butterflies' in name else 240})
  animations.append({'id':i*len(frames),'animation':ids})
 save(atlas,name+'.png');fx_specs.append({'name':name,'cells':cells,'frames':len(frames),'animations':animations,'origin':origin})
for prefix,size,lights,origin in [('gate',(1024,1536),gateLights,(512,384)),('town',(1536,1024),townLights,(2304,512))]:effect(prefix+'-pulse',[glow(*size,lights,f) for f in range(8)],origin)
# Water bands follow the portal flow and fountain basin, using subtle cyan translucent dashes.
water=[]
for f in range(8):
 im=Image.new('RGBA',(1024,1536));dr=ImageDraw.Draw(im)
 for x,y,w,h in [(435,470,154,68)]:
  for k in range(8):
   yy=y+((k*17+f*3)%h);dr.arc((x,yy,x+w,yy+8),5,160,fill=(112,235,248,95),width=1)
 water.append(im)
effect('gate-water',water,(512,384));water=[]
for f in range(8):
 im=Image.new('RGBA',(1536,1024));dr=ImageDraw.Draw(im)
 for k in range(4):
  r=16+(k*19+f*3)%71;dr.arc((768-r,479-r*.46,768+r,479+r*.46),10,170,fill=(182,255,241,145),width=1);dr.arc((768-r,479-r*.46,768+r,479+r*.46),200,315,fill=(75,231,229,135),width=1)
 water.append(im)
effect('town-water',water,(2304,512))
frames=[]
for f in range(16):
 im=Image.new('RGBA',(512,768));dr=ImageDraw.Draw(im)
 for i in range(22):
  t=((i/22)+f/16)%1;x=256+(1-t)*(155*math.sin(i*2.39))+15*math.sin(t*8+i);y=744-t*710;flap=2+int(abs(math.sin(f*1.4+i))*3);col=(255,215+int(i%4)*8,119,230)
  dr.ellipse((x-flap-3,y-3,x-1,y+2),fill=col);dr.ellipse((x+1,y-3,x+flap+3,y+2),fill=col);dr.line((x,y-2,x,y+3),fill=(255,247,203,255));dr.point((x,y+9),fill=(240,208,119,80))
 frames.append(im)
effect('gate-butterflies',frames,(768,928))
# TMJ assembly.
tiles=[];nextgid=1

def tileset(name,file,animations=None,properties=None):
 global nextgid
 im=Image.open(O/file);w,h=im.size;ts={'firstgid':nextgid,'name':name,'image':file,'imagewidth':w,'imageheight':h,'tilewidth':32,'tileheight':32,'columns':w//32,'tilecount':w*h//1024,'margin':0,'spacing':0,'properties':[{'name':'tilesetCopyright','type':'string','value':'Original AI-assisted environment art and original code-native effects. See ART-PROVENANCE.md.'}]}
 if animations:ts['tiles']=animations
 if properties:ts['tiles']=properties
 nextgid+=ts['tilecount'];tiles.append(ts);return ts
marker=tileset('markers','tilesets/markers.png',properties=[{'id':0,'properties':[{'name':'collides','type':'bool','value':True}]}]);terrain=tileset('midnight','tilesets/midnight-terrain.png')
layers=[]
def layer(name,visible=True):
 a={'id':len(layers)+1,'name':name,'type':'tilelayer','x':0,'y':0,'width':W,'height':H,'opacity':1,'visible':visible,'data':[0]*(W*H)};layers.append(a);return a

def stamp(a,t,x,y,rows=None):
 x//=32;y//=32
 for sy in range(t['imageheight']//32) if rows is None else rows:
  for sx in range(t['columns']):
   if 0<=x+sx<W and 0<=y+sy<H:a['data'][(y+sy)*W+x+sx]=t['firstgid']+sy*t['columns']+sx

def image_layer(name,file,x,y,visible=True,rows=None):
 ts=tileset(name,file);a=layer(name,visible);stamp(a,ts,x,y,rows);return a,ts
collision=layer('permanent-collisions');collision['data']=[1]*(W*H)
def carve(x,y,w,h,value=0):
 for yy in range(y//32,(y+h)//32):
  for xx in range(x//32,(x+w)//32):collision['data'][yy*W+xx]=value
for lo,hi,left,right in [(480,704,384,640),(704,864,352,672),(864,1056,320,704),(1056,1504,256,768)]:carve(512+left,384+lo,right-left,hi-lo)
# Side terraces stay scenery; the central promenade connects every building without long travel.
for x,y,w,h in [(672,64,224,896),(128,64,576,448),(864,96,416,512),(864,512,416,416),(352,352,352,224),(512,512,192,224)]:carve(2304+x,512+y,w,h)
# Fountain basin and planters are solid; peripheral paths remain connected.
for yy in range(12,18):
 for xx in range(20,28):
  if ((xx*32+16-768)/120)**2+((yy*32+16-480)/96)**2<1:carve(2304+xx*32,512+yy*32,32,32,1)
for b in L['buildings']:
 x,y,w,h=b['x'],b['y'],b['width'],b['height'];carve(x,y,w,h);carve(x,y,w,64,1);carve(x,y,32,h,1);carve(x+w-32,y,32,h,1);carve(x,y+h-32,w,32,1);carve(b['doorX']-32,y+h-32,64,64)
 for rx,ry,rw,rh in furniture_collision[b['id']]:carve(x+rx,y+ry,rw,rh,1)
for px,py in [(3232,1024),(2880,1024)]:carve(px,py+64,64,32,1)
start=layer('start');start['data'][(1760//32)*W+1024//32]=marker['firstgid']+1
base=layer('midnight-surroundings')
for yy in range(H):
 for xx in range(W):base['data'][yy*W+xx]=terrain['firstgid']+(yy%8)*8+(xx%8)
# Optional full painted extensions fit underneath the unchanged authored scene.
expanded=Image.open(R/'art-source/gate-environment-expanded.png').convert('RGBA').resize((2048,2048),Image.Resampling.LANCZOS);save(expanded,'gate-ground.png');layer('gate-surroundings');image_layer('gate-ground','tilesets/gate-ground.png',0,128)
# Native brick-and-garden buffer covers camera space beyond the hero plaza artwork.
buffer=Image.new('RGBA',(2304,1792),(55,55,55,255));bd=ImageDraw.Draw(buffer)
for yy in range(0,1792,16):
 for xx in range(-32,2304,32):
  z=random.randrange(-8,9);x=xx+(16 if yy//16%2 else 0);bd.rectangle((x+1,yy+1,x+31,yy+15),fill=(75+z,68+z,62+z,255))
for i in range(1600):
 x=random.randrange(2304);y=random.randrange(1792)
 if 355<x<1949 and 355<y<1437:continue
 r=random.randrange(7,30);bd.ellipse((x-r,y-r*.5,x+r,y+r*.6),fill=random.choice([(19,43,44,255),(26,55,48,255),(34,63,48,255),(39,63,52,255)]))
 for k in range(5):
  xx=x+random.randrange(-r,r);yy=y+random.randrange(-r//2,r//2+1);bd.ellipse((xx,yy,xx+4,yy+2),fill=random.choice([(64,81,52,255),(71,75,57,255),(35,74,60,255)]))
save(buffer,'town-surroundings.png');image_layer('town-surroundings','tilesets/town-surroundings.png',1920,128)
image_layer('town-ground','tilesets/town-ground.png',2304,512)
# Smooth native atmospheric edge veil. Source artwork is unchanged.
fog=Image.new('RGBA',(2304,1792));fp=fog.load()
for yy in range(1792):
 for xx in range(2304):
  edge=min(xx-384,1920-xx,yy-384,1408-yy)
  if edge<180:
   alpha=int(255*max(0,min(1,(160-edge)/170))**1.7);fp[xx,yy]=(9,18,34,alpha)
save(fog,'town-edge-fog.png');image_layer('town-edge-fog','tilesets/town-edge-fog.png',1920,128)
for b in L['buildings']:
 image_layer(b['id']+'-interior','tilesets/'+b['id']+'-interior.png',b['x'],b['y']);image_layer(b['id']+'-furniture-feet','tilesets/'+b['id']+'-furniture-feet.png',b['x'],b['y'])
olive=normalize(R/'art-source/town/olive-small.png',None,(64,96),'town-olive.png')
shadow=Image.new('RGBA',(64,96));ImageDraw.Draw(shadow).ellipse((10,83,54,95),fill=(9,22,21,105));save(shadow.filter(ImageFilter.GaussianBlur(2)),'town-olive-shadow.png');a,shadowTs=image_layer('town-olive-shadow','tilesets/town-olive-shadow.png',3232,1024);stamp(a,shadowTs,2880,1024)
a,oliveTs=image_layer('town-olive-feet','tilesets/town-olive.png',3232,1024,rows=[2]);stamp(a,oliveTs,2880,1024,[2])
for prefix,origin in [('gate',(512,384)),('town',(2304,512))]:image_layer(prefix+'-steady','tilesets/'+prefix+'-steady.png',*origin)
for fx in fx_specs:
 if fx['name']=='gate-butterflies':continue
 ts=tileset(fx['name'],'tilesets/'+fx['name']+'.png',fx['animations']);a=layer(fx['name'],False);ox,oy=fx['origin']
 for i,(x,y) in enumerate(fx['cells']):a['data'][(oy//32+y)*W+ox//32+x]=ts['firstgid']+i*fx['frames']
areas=[]
def area(name,bounds):areas.append({'id':len(areas)+1,'name':name,'class':'area','type':'area','x':bounds['x'],'y':bounds['y'],'width':bounds['width'],'height':bounds['height'],'rotation':0,'visible':True,'properties':[]})
area('gate-approach',L['gate']['approach']);area('gate-threshold',L['gate']['threshold']);area('town-return',L['town']['return'])
for b in L['buildings']:area(b['id']+'-inside',b['zone'])
layers.append({'id':len(layers)+1,'name':'floorLayer','type':'objectgroup','x':0,'y':0,'opacity':1,'visible':True,'draworder':'topdown','objects':areas})
layer('gate-front')
a,ts=image_layer('town-olive-canopies','tilesets/town-olive.png',3232,1024,rows=[0,1]);stamp(a,ts,2880,1024,[0,1])
# Front wall strips and north architecture draw above players. Furniture feet alone collide.
for b in L['buildings']:
 image_layer(b['id']+'-furniture-canopies','tilesets/'+b['id']+'-furniture-canopies.png',b['x'],b['y'])
 a,ts=image_layer(b['id']+'-architecture','tilesets/'+b['id']+'-interior.png',b['x'],b['y'],rows=[0,1,b['height']//32-1]);
 roof=O/'tilesets'/(b['id']+'-roof.png')
 if roof.exists():image_layer(b['id']+'-roof','tilesets/'+b['id']+'-roof.png',b['x'],b['y'])
 else:layer(b['id']+'-roof')
image_layer('town-details','tilesets/town-details.png',2304,512)
for b in L['buildings']:image_layer(b['id']+'-focus','tilesets/'+b['id']+'-focus.png',2304,512,False)
for fx in fx_specs:
 if fx['name']!='gate-butterflies':continue
 ts=tileset(fx['name'],'tilesets/'+fx['name']+'.png',fx['animations']);a=layer(fx['name'],False);ox,oy=fx['origin']
 for i,(x,y) in enumerate(fx['cells']):a['data'][(oy//32+y)*W+ox//32+x]=ts['firstgid']+i*fx['frames']
m={'compressionlevel':-1,'width':W,'height':H,'infinite':False,'orientation':'orthogonal','renderorder':'right-down','tileheight':32,'tilewidth':32,'tiledversion':'1.10.2','type':'map','version':'1.10','nextlayerid':len(layers)+1,'nextobjectid':len(areas)+1,'properties':[{'name':'mapName','type':'string','value':'The Butterfly Gate · StudentHub Town'},{'name':'mapDescription','type':'string','value':'A position-reactive journey through a monumental gate into a living town, with local roof reveals, human-scale interiors and animated water and light.'},{'name':'script','type':'string','value':'scripts/town.js'}],'layers':layers,'tilesets':tiles}
json.dump(m,open(O/'butterfly-town.tmj','w'),separators=(',',':'));json.dump({'fx':fx_specs,'layout':L,'furnitureCollision':furniture_collision,'furniture':furniture_specs},open(R/'evidence/build-manifest.json','w'),indent=2)
print('Built',len(layers),'layers,',len(tiles),'atlases;',sum(g==0 for g in collision['data']),'walkable cells')

# Keep the deployable folder lean: only referenced raster atlases.
used={t['image'] for t in tiles}
for asset in (O/'tilesets').glob('*.png'):
 if str(asset.relative_to(O)) not in used:asset.unlink()
(O/'images/interiors-empty-alpha.png').unlink(missing_ok=True)
