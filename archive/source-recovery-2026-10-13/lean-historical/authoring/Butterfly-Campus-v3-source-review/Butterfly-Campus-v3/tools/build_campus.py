from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
from pathlib import Path
from collections import deque
import json,math,random,hashlib,shutil
from light_room_materials import room_shell, light_assets, wall_strip, side_wall
R=Path(__file__).resolve().parents[1];O=R/'map';T=32;W=128;H=104;WW=W*T;HH=H*T;random.seed(81)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
assets={p.stem:Image.open(p).convert('RGBA') for p in (R/'assets').glob('*.png') if 'proof' not in p.stem}
assets.update(light_assets())
class Layer:
 def __init__(self,name):self.name=name;self.cells={};self.properties=[]
 def stamp(self,im,x,y):
  x=int(x);y=int(y)
  for ty in range(y//32,(y+im.height+31)//32):
   for tx in range(x//32,(x+im.width+31)//32):
    if not(0<=tx<W and 0<=ty<H):continue
    c=im.crop((tx*32-x,ty*32-y,tx*32-x+32,ty*32-y+32))
    if not c.getchannel('A').getbbox():continue
    key=(tx,ty)
    if key in self.cells:self.cells[key].alpha_composite(c)
    else:self.cells[key]=c
 def canvas(self):
  im=Image.new('RGBA',(WW,HH))
  for (x,y),c in self.cells.items():im.alpha_composite(c,(x*32,y*32))
  return im
layers={};order=[]
def L(name):
 if name not in layers:layers[name]=Layer(name);order.append(name)
 return layers[name]
collision=[1]*(W*H);footprints=[];rooms=[];areas=[];approaches={};placements=[]
def carve(x,y,w,h,value=0):
 for yy in range(max(0,math.floor(y/32)),min(H,math.ceil((y+h)/32))):
  for xx in range(max(0,math.floor(x/32)),min(W,math.ceil((x+w)/32))):collision[yy*W+xx]=value

def area(name,x,y,w,h,props=None):
 a={'id':len(areas)+1,'name':name,'class':'area','type':'area','x':x,'y':y,'width':w,'height':h,'rotation':0,'visible':True}
 if props:a['properties']=props
 areas.append(a)

def texrect(texture,w,h):
 im=Image.new('RGBA',(w,h))
 for yi,y in enumerate(range(0,h,texture.height)):
  for xi,x in enumerate(range(0,w,texture.width)):
   t=texture.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if xi%2 else texture
   if yi%2:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   im.alpha_composite(t.crop((0,0,min(t.width,w-x),min(t.height,h-y))),(x,y))
 return im

def sign(text,x,y,size=font,prefix='campus'):
 d=ImageDraw.Draw(Image.new('RGBA',(1,1)));bb=d.textbbox((0,0),text,font=size);w=bb[2]+26;im=Image.new('RGBA',(w,32));d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,w-1,29),5,fill=(26,47,47,248),outline=(204,168,96),width=2);d.line((7,4,w-8,4),fill=(236,205,134,140));d.text((13,7),text,font=size,fill=(252,235,188));L(prefix+'-signs').stamp(im,x-w//2,y)

def prop(name,x,y,prefix='campus',solid=True,foot=24,water=False):
 im=assets[name];w,h=im.size
 if name=='meeting_table':y=(int(y)//32)*32+16;foot=52
 cut=max(0,h-32)
 # All source images remain independent objects; only actual alpha overhang is above avatars.
 if water:
  L(prefix+'-bases').stamp(im,x,y)
 else:
  L(prefix+'-bases').stamp(im.crop((0,cut,w,h)),x,y+cut)
  L(prefix+'-front').stamp(im.crop((0,0,w,cut)),x,y)
 if solid:
  # A grid support anchor never changes when roofs/effects change visibility.
  fw=64 if name in ['outdoor-olive','outdoor-willow'] else max(24,w-12);fx=x+(w-fw)/2;fy=math.floor((y+h-foot)/32)*32;fh=32 if foot<=32 else math.ceil(foot/32)*32
  carve(fx,fy,fw,fh,1)
  if name=='reception':
   for sx in [math.floor((x+12)/32)*32,math.floor((x+w-12)/32)*32]:carve(sx,math.floor(y/32)*32,32,math.ceil((h-24)/32)*32,1)
  footprints.append({'name':name,'rect':[fx,fy,fw,fh],'placement':[x,y,w,h]})
 placements.append({'asset':name,'x':x,'y':y,'width':w,'height':h,'prefix':prefix})

def room(id,label,x,y,w,h,kind,roof=True):
 shell=room_shell(w,h)
 for suffix in ['floor','bases','front']:L(id+'-'+suffix).stamp(shell[suffix],x,y)
 doorw=128;dl=w//2-doorw//2;dr=dl+doorw
 carve(x+32,y+112,w-64,h-112,0);carve(x+dl,y+h-64,doorw,96,0)
 for rect in [(x,y,w,112),(x,y,32,h),(x+w-32,y,32,h),(x,y+h-64,dl,64),(x+dr,y+h-64,w-dr,64)]:carve(*rect,1)
 bounds={'x':x+32,'y':y+112,'width':w-64,'height':h-80};rooms.append({'id':id,'label':label,'bounds':bounds,'door':{'x':x+w//2,'y':y+h+16},'kind':kind})
 area(id+'-inside',**dict(zip(['x','y','w','h'],[bounds['x'],bounds['y'],bounds['width'],bounds['height']])))
 approaches[id+'-entry']=[x+w//2,y+h+16];approaches[id+'-lobby']=[x+w//2,y+h-112]
 sign(label,x+w//2,y+h+40)
 if roof:
  src=Image.open(R/'art-source'/({'creative':'creative-roof-original.png','research':'research-roof-original.png','learning':'learning-roof-original.png','operations':'operations-roof-original.png'}.get(kind,'hq-roof-original.png'))).convert('RGBA');src=src.crop(src.getchannel('A').point(lambda alpha:255 if alpha>8 else 0).getbbox());assert src.width>=w and src.height>=h,(id,src.size,w,h)
  im=src.resize((w,h),Image.Resampling.LANCZOS);L(id+'-roof').stamp(im,x,y)
 return x,y,w,h

def partition(prefix,x,y,w,gap=96):
 left=(w-gap)//2
 for xx,ww in [(x,left),(x+left+gap,w-left-gap)]:
  im=wall_strip(ww,48);L(prefix+'-bases').stamp(im.crop((0,32,ww,48)),xx,y+32);L(prefix+'-front').stamp(im.crop((0,0,ww,32)),xx,y);carve(xx,y,ww,32,1)

# Deliberate campus island: stone terrace and planted border; no repeated scenery outside boundary.
# A connected archipelago silhouette follows real departments and promenades.
# Empty top-right lawn is removed: the boundary itself explains the campus.
mask=Image.new('L',(WW,HH));md=ImageDraw.Draw(mask)
land=[(1152,160,1984,960),(2240,160,3072,960),(1152,992,2240,1952),(3200,800,4032,1600),(3200,1792,4032,2528),(1184,2176,2240,2912),(2112,1120,3104,2176),(2144,2160,3104,3024),(1200,880,2784,1120),(1200,1824,3264,2144),(2640,1504,3968,1760),(2640,2432,3968,2720),(1424,2784,2848,3024),(2384,704,2768,3024),(3040,1472,3296,2720),(2400,2912,2752,3200)]
for box in land:md.rounded_rectangle(box,64,fill=255)
# A few deliberate planted bays, rather than repeated off-map filler.
for cx,cy in [(3016,1120),(2160,2112),(3112,2720),(3736,2688),(1416,2880),(3904,2544)]:md.ellipse((cx-112,cy-96,cx+112,cy+112),fill=255)
edge=Image.new('RGBA',(WW,HH))
stone=texrect(assets['limestone-texture'],2944,3200)
for dy,level in [(80,.29),(56,.39),(32,.55),(12,.82)]:
 tinted=Image.eval(stone,lambda v:int(v*level));tinted.putalpha(ImageChops.offset(mask,0,dy).crop((1120,128,4064,3328)));edge.alpha_composite(tinted,(1120,128))
L('campus-island-edge').stamp(edge.crop((1120,128,4064,3328)),1120,128)
ground=Image.new('RGBA',(2944,3104))
for yy in range(0,3104,256):
 for xx in range(0,2944,256):
  variant=assets['grass-material-'+str((xx//256*7+yy//256*11+(xx//256*yy//256)%5)%8)];ground.alpha_composite(variant,(xx,yy))
gm=mask.crop((1120,128,4064,3232));ground.putalpha(gm);L('campus-garden-ground').stamp(ground,1120,128)
# Fine limestone promenades and generous connected activity courts.
paths=[(2448,736,256,2208),(1280,928,1456,160),(1248,1888,1984,192),(2688,1552,1216,160),(2688,2496,1216,160),(1472,2848,1344,128),(2176,1184,832,960),(2208,2224,864,672),(3104,1504,160,1168),(2448,2944,256,256)]
for x,y,w,h in paths:
 im=texrect(assets['limestone-texture'],w,h);d=ImageDraw.Draw(im);d.rectangle((2,2,w-3,h-3),outline=(169,152,111),width=3);d.rectangle((6,6,w-7,h-7),outline=(219,208,173),width=1);L('campus-promenade').stamp(im,x,y);carve(x+16,y+16,w-32,h-32)
# Dedicated north classroom.
x,y,w,h=room('learning','LEARNING HALL',1216,224,704,672,'learning')
prop('teacher',x+328,y+145,'learning');prop('bookshelf',x+48,y+110,'learning');prop('plant',x+600,y+132,'learning')
for ry in [280,408,536]:
 for rx in [112,320,528]:
  prop('desk',x+rx,y+ry,'learning');prop('chair_n',x+rx+18,y+ry+60,'learning')
approaches['learning-lobby']=[x+240,y+560];approaches['learning-teacher']=[x+416,y+224];area('learning-teaching',x+256,y+128,256,128);area('learning-students',x+64,y+256,w-128,320)
# Open event hall with stage, separate audience blocks and side/central aisles.
x,y,w,h=room('events','THE LANTERN STAGE',2304,224,704,672,'event',False)
stage=Image.open(R/'art-source/stage-original.png').convert('RGBA');stage=stage.crop(stage.getchannel('A').getbbox());stage.thumbnail((640,230),Image.Resampling.LANCZOS);L('events-floor').stamp(stage,x+(w-stage.width)//2,y-32)
step=Image.new('RGBA',(576,128));sd=ImageDraw.Draw(step);sd.rounded_rectangle((0,0,575,127),12,outline=(202,171,103,255),width=3);sd.line((6,120,570,120),fill=(229,203,144),width=3);L('events-floor').stamp(step,x+64,y+192)
prop('podium',x+328,y+176,'events');carve(x+64,y+112,w-128,100,1);carve(x+64,y+212,w-128,96,0)
for ry in [336,416,496,576]:
 for rx in [128,192,256,432,496,560]:prop('chair_n',x+rx,y+ry,'events')
area('events-stage',x+64,y+208,w-128,112);area('events-audience',x+64,y+336,w-128,256);approaches['events-speaker']=[x+352,y+264];approaches['events-audience']=[x+352,y+512]
# StudentHub: three independently usable meeting rooms plus reception/shared-work commons.
x,y,w,h=room('hq','STUDENTHUB HQ',1216,1056,960,832,'hq')
for idx,name in enumerate(['Cedar','Olive','Willow']):
 rx=x+idx*320
 if idx:
  p=side_wall(272);L('hq-front').stamp(p,rx,y+112);carve(rx,y+112,32,272,1)
 partition('hq',rx+32,y+384,256,128)
 prop('meeting_table',rx+96,y+224,'hq')
 for dx in [108,172]:prop('chair_s',rx+dx,y+168,'hq');prop('chair_n',rx+dx,y+320,'hq')
 prop('plant',rx+44,y+124,'hq');sign(name+' meeting',rx+160,y+360,small,'hq')
 area('hq-'+name.lower()+'-meeting',rx+40,y+120,240,264);approaches['hq-'+name.lower()]=[rx+240,y+288]
for rx in [96,256,656,816]:prop('desk',x+rx,y+480,'hq');prop('chair_n',x+rx+18,y+544,'hq')
L('hq-floor').stamp(assets['rug'],x+368,y+464);prop('couch_s',x+428,y+450,'hq');prop('couch_e',x+352,y+514,'hq');prop('couch_w',x+592,y+514,'hq');prop('coffee',x+464,y+526,'hq')
prop('reception',x+96,y+644,'hq');prop('chair_s',x+152,y+602,'hq');prop('plant',x+64,y+716,'hq');prop('plant',x+848,y+716,'hq')
approaches['hq-lobby']=[x+480,y+784];approaches['hq-reception']=[x+168,y+744];approaches['hq-teamwork']=[x+288,y+608];area('hq-team-workspace',x+64,y+448,w-128,192);area('hq-reception',x+64,y+608,256,192)
# Media/design atelier.
x,y,w,h=room('creative','MEDIA + DESIGN',3264,864,704,672,'creative')
for rx in [64,448]:prop('workbench',x+rx,y+168,'creative');prop('chair_n',x+rx+64,y+264,'creative')
prop('meeting_table',x+96,y+408,'creative');prop('chair_s',x+132,y+344,'creative');prop('chair_n',x+132,y+512,'creative')
L('creative-floor').stamp(assets['rug'],x+400,y+392);prop('couch_s',x+464,y+374,'creative');prop('coffee',x+488,y+464,'creative');prop('plant',x+592,y+160,'creative')
sign('IMAGE STUDIO',x+164,y+128,small,'creative');sign('MUSIC STUDIO',x+524,y+128,small,'creative');sign('DESIGN REVIEW',x+196,y+552,small,'creative')
area('creative-imagine-images',x+64,y+160,208,176);area('creative-music',x+416,y+160,224,176);area('creative-design-review',x+64,y+352,256,224);approaches['creative-image-workbench']=[x+144,y+304];approaches['creative-music-workbench']=[x+512,y+304]
# Research lab with actual station/reading approaches.
x,y,w,h=room('research','R&D RESEARCH LAB',3264,1856,704,608,'research')
prop('bookshelf',x+48,y+110,'research');prop('bookshelf',x+448,y+110,'research')
for rx in [112,464]:prop('workbench',x+rx,y+304,'research');prop('chair_n',x+rx+64,y+400,'research')
prop('meeting_table',x+288,y+192,'research');prop('plant',x+64,y+456,'research');prop('plant',x+584,y+456,'research')
area('research-lab',x+64,y+256,576,224);approaches['research-workbench']=[x+208,y+448]
# Operations and sales wing: two distinct purposeful rooms.
x,y,w,h=room('operations','OPERATIONS + SALES',1248,2240,928,608,'operations')
# Short central wall stops above a broad common reception passage.
L('operations-front').stamp(side_wall(304),x+448,y+112);carve(x+448,y+112,32,304,1)
for rx in [96,256,576,736]:prop('desk',x+rx,y+192,'operations');prop('chair_n',x+rx+18,y+272,'operations')
prop('meeting_table',x+144,y+368,'operations');prop('chair_n',x+176,y+472,'operations');prop('meeting_table',x+608,y+368,'operations');prop('chair_n',x+640,y+472,'operations')
sign('OPERATIONS',x+240,y+128,small,'operations');sign('SALES',x+688,y+128,small,'operations')
area('operations-command',x+40,y+128,384,368);area('sales-research',x+488,y+128,384,368);approaches['operations-station']=[x+224,y+320];approaches['sales-station']=[x+688,y+320]
# Public central landmarks and social commons with four different approaches.
prop('outdoor-fountain',2528,1328,solid=True,foot=128,water=True)
# Fountain entire basin is a solid circular obstacle; effects stay above water and below avatar.
carve(2560,1408,128,96,1);approaches['fountain']=[2624,1568]
for rx,ry in [(2336,1776),(2688,1776)]:
 L('campus-promenade').stamp(assets['rug'],rx,ry);prop('couch_s',rx+64,ry-16);prop('couch_e',rx-16,ry+40);prop('couch_w',rx+224,ry+40);prop('coffee',rx+96,ry+64)
area('student-commons',2272,1728,800,320);approaches['student-commons']=[2624,1968]
# A visible return portal makes the south transition discoverable.
portal=Image.open(R/'art-source/gate-arch-original.png').convert('RGBA');portal.thumbnail((192,240),Image.Resampling.LANCZOS);L('campus-front').stamp(portal,2464+(192-portal.width)//2,2912)
# The market remains open display space; no fake commerce/bot actions.
for i,(xx,yy) in enumerate([(2288,2304),(2816,2304),(2288,2592),(2816,2592)]):
 prop('outdoor-booth-navy' if i%2==0 else 'outdoor-booth-teal',xx,yy,foot=48);area('market-booth-'+str(i+1),xx-16,yy+128,160,96);approaches['market-booth-'+str(i+1)]=[xx+64,yy+176]
sign('STUDENT MARKET',2624,2416);sign('STUDENT COMMONS',2624,2072);sign('BUTTERFLY GATE',2560,3168)
# Deliberate planted pockets: all landscape feet solid, overhangs alpha-only.
for i,(xx,yy) in enumerate([(2216,1088),(2960,1096),(2192,1552),(2976,1552),(2240,2104),(2992,2112),(1232,1920),(2016,1952),(3096,2696),(3656,2704),(1360,2912),(3776,2496)]):
 prop('outdoor-olive' if i%3 else 'outdoor-willow',xx,yy,foot=32)
for xx,yy in [(2296,1256),(2880,1264),(2344,1616),(2856,1624),(2752,2064),(2176,2704),(2992,2704),(3072,1760),(3696,1760),(1856,864)]:prop('outdoor-garden',xx,yy,foot=64)
for xx,yy in [(2392,1000),(2712,1000),(2392,1600),(2744,1600),(2256,1856),(3080,1856),(2440,2184),(2712,2184),(2440,2792),(2712,2792)]:prop('streetlamp',xx,yy)
# Planted edges and warm light pools enrich real spaces without occupying circulation.
for xx,yy in [(1280,176),(1440,176),(1600,176),(1760,176),(2368,176),(2528,176),(2688,176),(2848,176),(2304,1312),(2304,1472),(2880,1312),(2880,1472),(2224,2032),(2992,2032),(3232,1632),(3808,1632),(3232,2576),(3808,2576)]:prop('border-planter',xx,yy,foot=24)
for xx,yy in [(2392,1000),(2712,1000),(2392,1600),(2744,1600),(2256,1856),(3080,1856),(2440,2184),(2712,2184),(2440,2792),(2712,2792)]:
 glow=Image.new('RGBA',(160,96));gd=ImageDraw.Draw(glow);gd.ellipse((8,12,152,84),fill=(255,197,94,32));L('campus-warm-lights').stamp(glow.filter(ImageFilter.GaussianBlur(20)),xx-64,yy+48)
sign('← StudentHub HQ',2368,1984,small);sign('Media + R&D →',2824,1984,small);sign('↑ Learning + Stage',2552,1080,small);sign('↓ Commons + Market',2776,1648,small);sign('↑ Media   R&D ↓',3184,2112,small)
# Quiet monumental gate uses original native artwork, downsampled once, never expanded.
gsrc=Image.open(R/'art-source/gate-original.png').convert('RGBA');g= gsrc.resize((960,1440),Image.Resampling.LANCZOS);gx,gy=32,1664
# Soft edge is a presentation fade only, not added repeated off-map scenery.
a=Image.new('L',g.size,255);ad=ImageDraw.Draw(a)
for n in range(48):ad.rectangle((n,n,959-n,1439-n),outline=round(255*n/47))
g.putalpha(a);L('gate-ground').stamp(g,gx,gy)
# Geometry follows the actual original painting's central paving, with side scenery blocked.
profile=[(544,432,592),(640,400,624),(736,384,640),(928,344,680),(1120,320,704),(1280,304,720),(1440,288,736)]
def paveat(y):
 for (a,l,r),(b,bl,br) in zip(profile,profile[1:]):
  if a<=y<=b:
   u=(y-a)/(b-a);return l+(bl-l)*u,r+(br-r)*u
 return (432,592) if y<544 else (288,736)
for yy in range(544,1440,32):
 left,right=paveat(yy);left=math.ceil((gx+left)/32)*32;right=math.floor((gx+right)/32)*32;carve(left,gy+yy,right-left,32)
gate={'bounds':{'x':32,'y':1664,'width':960,'height':1440},'spawn':{'x':512,'y':3000},'threshold':{'x':448,'y':2208,'width':128,'height':64}}
campus={'bounds':{'x':1120,'y':128,'width':2944,'height':3104},'spawn':{'x':2624,'y':2080},'return':{'x':2496,'y':3104,'width':128,'height':64}}
area('gate-bounds',**dict(zip(['x','y','w','h'],gate['bounds'].values())));area('campus-bounds',**dict(zip(['x','y','w','h'],campus['bounds'].values())));area('gate-threshold',**dict(zip(['x','y','w','h'],gate['threshold'].values())));area('campus-return',**dict(zip(['x','y','w','h'],campus['return'].values())))
for name,p in [('gate-spawn',gate['spawn']),('campus-spawn',campus['spawn'])]:areas.append({'id':len(areas)+1,'name':name,'class':'spawnPoint','type':'spawnPoint','point':True,'x':p['x'],'y':p['y'],'width':0,'height':0,'rotation':0,'visible':True})
area('start',464,2976,96,64,[{'name':'start','type':'bool','value':True}]);area('campus-entry',2576,2048,96,64,[{'name':'start','type':'bool','value':True}])
approaches['campus-entry']=[2624,2080];approaches['gate-return']=[2560,3072]
area('gate-onboarding-guide',384,2816,256,192);area('campus-guide-stop',2464,2048,320,160)
# Stable collision gaps for all named doorways. No collision is tied to roof visibility.
for r in rooms:
 d=r['door'];carve(d['x']-48,d['y']-16,96,64)
# Tile animations have separate native32px cells, no stale static foreground over water.
fx=[]
def animation(name,frames,x,y,duration=150):
 entries=[]
 for cy in range((frames[0].height+31)//32):
  for cx in range((frames[0].width+31)//32):
   seq=[im.crop((cx*32,cy*32,cx*32+32,cy*32+32)) for im in frames]
   if any(c.getchannel('A').getbbox() for c in seq):entries.append((x//32+cx,y//32+cy,seq))
 fx.append((name,entries,duration))
frames=[]
for f in range(8):
 im=Image.new('RGBA',(192,192));d=ImageDraw.Draw(im)
 for k in range(3):
  r=16+(k*13+f*2)%48;d.arc((96-r,118-r*.32,96+r,118+r*.32),2,172,fill=(183,249,232,160),width=1)
 for xx in [54,138]:
  for yy in range(82+f%4,115,7):d.line((xx,yy,xx,yy+3),fill=(212,255,255,150),width=1)
 frames.append(im)
animation('campus-water',frames,2528,1328,130)
# Original gate falls. Effects are registered inside visible water only.
frames=[]
for f in range(8):
 im=Image.new('RGBA',(960,1440));d=ImageDraw.Draw(im)
 for xx,yy,ww,hh in [(168,704,20,52),(150,853,24,58),(175,1092,18,84),(137,1304,22,60),(816,700,20,55),(826,850,22,58),(792,1089,24,78)]:
  for n in range(ww//3):
   sx=xx+n*3;sy=yy+(f*5+n*13)%max(1,hh-12);d.line((sx,sy,sx,sy+10),fill=(144,237,248,95),width=1)
 frames.append(im)
animation('gate-water',frames,gx,gy,110)
# Gently animated original butterfly glows remain separate and non-colliding.
frames=[]
for f in range(12):
 im=Image.new('RGBA',(256,512));d=ImageDraw.Draw(im)
 for i in range(12):
  u=(i/12+f/12)%1;xx=128+math.sin(i*2.4+u*7)*(56*(1-u));yy=490-u*460;wing=2+int(abs(math.sin(f+i))*2);d.ellipse((xx-wing-2,yy-2,xx-1,yy+2),fill=(255,229,147,205));d.ellipse((xx+1,yy-2,xx+wing+2,yy+2),fill=(255,229,147,205))
 frames.append(im)
animation('gate-butterflies',frames,384,2232//32*32,110)
# Build deduplicated1024 atlases; nothing uses image layers or resized tileobjects.
unique={};tileimgs=[];animations=[]
def gid(im,uniqueable=True):
 k=im.tobytes()
 if uniqueable and k in unique:return unique[k]
 n=len(tileimgs)+1;tileimgs.append(im)
 if uniqueable:unique[k]=n
 return n
marker=gid(Image.new('RGBA',(32,32)),False)
start_marker=gid(Image.new('RGBA',(32,32)),False)
maplayers=[{'id':1,'name':'permanent-collisions','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':[marker if c else 0 for c in collision]}]
def emit(name,data,props=None):
 l={'id':len(maplayers)+1,'name':name,'type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':data}
 if props:l['properties']=props
 if any(name.startswith(r['id']+'-') and name!=r['id']+'-roof' and r['kind']!='event' for r in rooms):l['visible']=False
 maplayers.append(l)
start_data=[0]*(W*H);start_data[(3000//32)*W+16]=start_marker
emit('start',start_data,[{'name':'start','type':'bool','value':True}])
# Non-colliding full-map native audio control. No audio properties are active by default.
emit('campus-audio-control',[start_marker]*(W*H))
# Every background/bases layer precedes floorLayer; foreground has actual alpha only.
for phase in ['below','above']:
 if phase=='above':maplayers.append({'id':len(maplayers)+1,'name':'floorLayer','type':'objectgroup','opacity':1,'visible':True,'objects':[]})
 for name in [n for n in order if not n.endswith('-signs')]+[n for n in order if n.endswith('-signs')]:
  above=name.endswith('-front') or name.endswith('-roof')
  if above!=(phase=='above'):continue
  data=[0]*(W*H)
  for (x,y),im in layers[name].cells.items():data[y*W+x]=gid(im)
  emit(name,data)
 if phase=='below':
  for name,entries,duration in fx:
   data=[0]*(W*H)
   for x,y,seq in entries:
    if len(tileimgs)%1024+len(seq)>1024:
     for _ in range(1024-len(tileimgs)%1024):gid(Image.new('RGBA',(32,32)),False)
    ids=[gid(c,False) for c in seq];data[y*W+x]=ids[0];animations.append((ids[0],[{'tileid':n-1,'duration':duration} for n in ids]))
   emit(name,data,[{'name':'reducedMotionHide','type':'bool','value':True}])
maplayers.append({'id':len(maplayers)+1,'name':'activity-areas','type':'objectgroup','opacity':1,'visible':True,'objects':areas})
# Split atlases must keep each animation's frames within one tileset; reserve all animationtiles in one atlas? Remap straightforward with per-frame check below.
# Phaser animations may not span tilesets; frames produced in consecutive runs can cross boundary. Keep atlas count chunks aligned by padding when needed in future revisions.
tilesets=[];n=len(tileimgs)
for ai,start in enumerate(range(0,n,1024)):
 chunk=tileimgs[start:start+1024];rows=math.ceil(len(chunk)/32);atlas=Image.new('RGBA',(1024,rows*32))
 for j,c in enumerate(chunk):atlas.alpha_composite(c,((j%32)*32,(j//32)*32))
 name=f'campus-atlas-{ai+1:02d}';file='tilesets/'+name+'.png';atlas.save(O/file)
 ts={'firstgid':start+1,'name':name,'image':file,'imagewidth':1024,'imageheight':rows*32,'tilewidth':32,'tileheight':32,'columns':32,'tilecount':rows*32,'margin':0,'spacing':0,'tiles':[]}
 if start==0:ts['tiles'].append({'id':0,'properties':[{'name':'collides','type':'bool','value':True}]})
 for first,seq in animations:
  if start<first<=start+len(chunk):
   assert all(start<=a['tileid']<start+1024 for a in seq),(first,'animation boundary')
   ts['tiles'].append({'id':first-start-1,'animation':[{'tileid':a['tileid']-start,'duration':a['duration']} for a in seq]})
 tilesets.append(ts)
map={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','infinite':False,'width':W,'height':H,'tilewidth':32,'tileheight':32,'backgroundcolor':'#0d1a24','layers':maplayers,'tilesets':tilesets,'properties':[{'name':'script','type':'string','value':'scripts/campus.js'},{'name':'campusVersion','type':'string','value':'3-candidate'},{'name':'audioEnabled','type':'bool','value':False}],'nextlayerid':len(maplayers)+1,'nextobjectid':len(areas)+1}
json.dump(map,open(O/'butterfly-campus.tmj','w'),separators=(',',':'))
layout={'tileSize':32,'mapWidth':W,'mapHeight':H,'phase':'full campus candidate','gate':gate,'campus':campus,'rooms':rooms,'proofPositions':approaches,'placements':placements}
json.dump(layout,open(R/'layout.json','w'),indent=2);json.dump(footprints,open(R/'evidence/footprints.json','w'),indent=2)
# Grid connectivity and body-clear waypoints; explicit failures retained for repair.
start=(int(campus['spawn']['y']+16)//32)*W+int(campus['spawn']['x'])//32;q=deque([start]);seen={start}
while q:
 i=q.popleft()
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  nx=i%W+dx;ny=i//W+dy;j=ny*W+nx
  if 0<=nx<W and 0<=ny<H and not collision[j] and j not in seen:seen.add(j);q.append(j)
checks={k:{'x':v[0],'y':v[1],'targetCellClear':not collision[(int(v[1]+16)//32)*W+int(v[0])//32],'reachable':(int(v[1]+16)//32)*W+int(v[0])//32 in seen} for k,v in approaches.items()}
json.dump({'scope':'static tile reachability, not rendered physics','checks':checks,'atlasCount':len(tilesets),'uniqueTiles':len(tileimgs),'textureBytesRGBA':sum(t['imagewidth']*t['imageheight']*4 for t in tilesets)},open(R/'evidence/static-map-checks.json','w'),indent=2)
# Honest visual review renders, separate from source-harness evidence.
for revealed in [False,True]:
 out=Image.new('RGBA',(WW,HH),(13,26,36,255))
 for phase in ['below','above']:
  for name in order:
   above=name.endswith('-front') or name.endswith('-roof')
   if above!=(phase=='above') or (revealed and name.endswith('-roof')):continue
   if not revealed and any(name.startswith(r['id']+'-') and name!=r['id']+'-roof' and r['kind']!='event' for r in rooms):continue
   for (x,y),im in layers[name].cells.items():out.alpha_composite(im,(x*32,y*32))
 out.resize((1536,1248),Image.Resampling.LANCZOS).save(R/'evidence'/('campus-overview-interiors.png' if revealed else 'campus-overview-exterior.png'))
 if revealed:
  out.crop((1184,1024,2208,1920)).save(R/'evidence/HQ-full-interior.png');out.crop((2240,160,3072,960)).save(R/'evidence/event-hall.png')
print(json.dumps({'atlases':len(tilesets),'uniqueTiles':len(tileimgs),'failedTargets':[k for k,v in checks.items() if not v['reachable']]}))
