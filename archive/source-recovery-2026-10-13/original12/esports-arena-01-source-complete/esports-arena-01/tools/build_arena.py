from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import numpy as np,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];A=R/'assets';S=R/'source';Q=R/'review';V=R/'validation';W,H=2048,1472;T=32;C,N=W//32,H//32
jw=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n');load=lambda n:Image.open(A/(n+'.png')).convert('RGBA');font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n);bold=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n)
base=Image.new('RGBA',(W,H),'#141b20');candidate=Image.new('RGBA',(W,H));g=np.ones((N,C),np.uint8);g[3:45,2:62]=0;placements=[];seats=[];social=[];landmarks=[];doors=[]
def block(x,y,w,h):
 assert all(v%32==0 for v in[x,y,w,h]);g[y//32:(y+h)//32,x//32:(x+w)//32]=1
floor=load('industrial-floor-native')
for y in range(96,1440,256):
 for x in range(64,1984,256):
  xx=min(256,1984-x);yy=min(256,1440-y);base.alpha_composite(floor.crop((0,0,xx,yy)),(x,y))
def paste(n,x,y,fgbox=None,collision=None):
 im=load(n);base.alpha_composite(im,(x,y));
 if fgbox:
  z=Image.new('RGBA',im.size);z.alpha_composite(im.crop(fgbox),(fgbox[0],fgbox[1]));candidate.alpha_composite(z,(x,y))
 if collision:block(*collision)
 placements.append({'asset':n+'.png','xy':[x,y],'size':list(im.size),'foregroundCandidate':list(fgbox)if fgbox else None,'collision':list(collision)if collision else None})
def hw(x,y,length):
 for dx in range(0,length,256):
  im=load('industrial-wall-native');w=min(256,length-dx);base.alpha_composite(im.crop((0,0,w,37)),(x+dx,y));candidate.alpha_composite(im.crop((0,0,w,37)),(x+dx,y))
 block(x,y, length,32);placements.append({'module':'horizontal wall','xy':[x,y],'width':length})
def vw(x,y,length):
 im=load('industrial-vertical-native')
 for dy in range(0,length,256):base.alpha_composite(im.crop((0,0,32,min(256,length-dy))),(x,y+dy));candidate.alpha_composite(im.crop((0,0,32,min(256,length-dy))),(x,y+dy))
 block(x,y,32,length);placements.append({'module':'vertical wall','xy':[x,y],'height':length})
def label(text,x,y,w=192,color='#85d2ce'):
 d=ImageDraw.Draw(base);d.rounded_rectangle((x,y,x+w,y+23),radius=3,fill='#1c292e',outline=color,width=1);bb=d.textbbox((0,0),text,font=bold(12));d.text((x+(w-bb[2])/2,y+4),text,font=bold(12),fill=color)
def seat(id,x,y,group=None,kind='spectator'):
 #40x45 fresh master reduction; low back physically overlays lower torso, never upper head.
 paste('industrial-chair40-native',x-20,y-24,(6,23,34,39),(x-16,((y+17)//32)*32,32,32));a={'id':id,'x':x,'y':y,'floorClick':[x,y+16],'artAnchor':[x,y+1],'kind':kind}
 if group:a['group']=group
 (social if group or kind!='spectator'else seats).append(a)
# Outer shell: visible architecture with broad real door on south edge.
hw(64,64,1920);vw(32,96,1312);vw(1984,96,1312);hw(64,1408,896);hw(1088,1408,896);doors.append({'id':'arrival-door','bounds':[960,1408,1088,1440],'axis':'y'})
# Purposeful raised-looking platform drawing remains one floor physics level.
d=ImageDraw.Draw(base)
d.rounded_rectangle((696,112,1352,463),radius=16,fill='#151e23',outline='#475760',width=5);d.line((712,457,1336,457),fill='#5b898f',width=3);d.line((720,462,1328,462),fill='#101417',width=5)
# Native black rubber texture covers platform, retaining shaped metal perimeter.
platform=Image.new('RGBA',(624,304));pdraw=ImageDraw.Draw(platform)
for y in range(0,304,16):pdraw.line((0,y,624,y),fill='#293238',width=1)
base.alpha_composite(platform,(712,128));hw(704,96,640);vw(672,128,320);vw(1344,128,320);paste('industrial-screen-native',864,144,collision=(864,160,320,64));label('CASTER / PRESENTATION',928,248,192,'#b2c1c6');paste('industrial-caster-native',928,312,collision=(928,320,192,32));seat('caster-west',976,367,kind='caster');seat('caster-east',1072,367,kind='caster')
# Team suites are physical pods with walls,96px south doors, equipment and directionally matched seats.
for name,x0,acc in [('west',96,'#51bfc1'),('east',1472,'#c28d64')]:
 group='esports-'+name+'-team';hw(x0,128,448);vw(x0,160,544);vw(x0+416,160,544);hw(x0,704,192);hw(x0+288,704,160);doors.append({'id':name+'-team-door','bounds':[x0+192,704,x0+288,736],'axis':'y','allowed':[group]})
 # Slim luminous sill and side ribs ground the pod identity without drawing a floor box.
 d=ImageDraw.Draw(base);d.line((x0+36,170,x0+412,170),fill=acc,width=3);d.line((x0+38,179,x0+38,685),fill='#3a5358'if name=='west'else'#59483f',width=3)
 label('TEAM '+name.upper(),x0+128,184,192,acc)
 for row,y in enumerate([272,464]):
  paste('industrial-desk-native',x0+80,y,collision=(x0+96,y+16,160,32))
  for col,x in enumerate([x0+112,x0+176,x0+240]):seat(f'{name}-team-{row*3+col+1}',x,y+63,group,'team')
 # Two dimensional sideline equipment racks preserve the clear player return lane.
 for yy in [272,464]:paste('industrial-rack-native',x0+344,yy,collision=(x0+352,yy+16,32,64))
 label('TEAM ACCESS',x0+177,661,96,acc)
# Central court framing: floor inlays, broadcast screen sightline and no obstructing decorative structures.
d=ImageDraw.Draw(base);d.line((704,528,1344,528),fill='#627b85',width=2);d.line((768,536,1280,536),fill='#34474f',width=2);d.text((952,551),'CENTRE COURT',font=bold(13),fill='#96afb8')
# Physical spectator chairs, four short banks with broad central and side aisles.
for r,y in enumerate([655,751,847,943]):
 for c,x in enumerate([784,848,912,1136,1200,1264]):seat(f'spectator-{r+1}-{c+1}',x,y)
 # Thin metal row rail behind chairs; remains below actors, collision only at seat backs.
 d.line((756,y+42,940,y+42),fill='#687076',width=2);d.line((1108,y+42,1292,y+42),fill='#687076',width=2)
# Perimeter wayfinding uses short light ticks, avoiding route-altering scenery.
for x in [608,1440]:
 for y in range(416,1153,96):d.rounded_rectangle((x-14,y,x+14,y+3),radius=1,fill='#587e84')
for x in range(640,1441,128):d.rounded_rectangle((x,1150,x+31,1153),radius=1,fill='#587e84')
label('SPECTATOR COURT',912,1064,224,'#a7b6be')
# Two deliberate arrival niches, physically grounded by matching architectural wings.
# The open central approach remains x768..1280 and connects directly to the perimeter loop.
hw(160,1088,448);vw(160,1120,224);hw(1376,1056,544);vw(1888,1088,256)
d=ImageDraw.Draw(base)
# Warm practical floor-edge lights and native wall depth frame the service alcoves.
d.line((192,1351,608,1351),fill='#99764f',width=2);d.line((1376,1351,1880,1351),fill='#99764f',width=2)
d.line((195,1356,605,1356),fill='#26363c',width=5);d.line((1379,1356,1877,1356),fill='#26363c',width=5)
paste('industrial-counter-native',256,1161,(8,8,184,39),collision=(256,1184,192,32));label('CHECK-IN',288,1122,128,'#b5c4c9');social += [{'id':'check-in-staff','x':344,'y':1167,'floorClick':[344,1183],'kind':'service'},{'id':'check-in-visitor','x':344,'y':1216,'floorClick':[344,1232],'kind':'service'}]
paste('industrial-counter-native',1632,1129,(8,8,184,39),collision=(1632,1152,192,32));label('COFFEE / SOCIAL',1632,1090,192,'#caa57e');social += [{'id':'coffee-staff','x':1720,'y':1135,'floorClick':[1720,1151],'kind':'service'},{'id':'coffee-visitor','x':1720,'y':1184,'floorClick':[1720,1200],'kind':'service'}]
for k,x0 in enumerate([1432,1688]):
 paste('industrial-sofa-native',x0,1248,(8,36,104,44),(x0+8,1248,96,32))
 for j,x in enumerate([x0+28,x0+84]):social.append({'id':f'social-pair-{k+1}-{j+1}','x':x,'y':1280,'floorClick':[x,1296],'kind':'casual','facing':'south','pair':k+1})
# Real native raster pilasters replace flat perimeter debug-like light rectangles.
for x in [64,1952]:
 for y in [864,1120,1312]:vw(x,y,64)
label('ARENA ENTRANCE',912,1346,224,'#b0c7cb')
# Native body-clear mask, used solely to safely partition candidate foreground. Whole art composition remains exact.
blocked=g.repeat(32,0).repeat(32,1).astype(np.int32);ii=np.pad(blocked.cumsum(0).cumsum(1),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
greg=load('greg-reference');sp=np.array(greg);head=np.zeros((14,32),bool)
for r in range(4):
 for c in range(3):head |= sp[r*32:r*32+14,c*32:c*32+32,3]>32
headReach=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);headReach[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
p=np.array(candidate);p[headReach]=0;above=Image.fromarray(p);alpha=np.asarray(above.getchannel('A'));bp=np.array(base);ap=np.array(above);# Remove exact selected source pixels from base, but preserve anti-aliased pixels by full composite split.
# Every foreground candidate was composited into base. To ensure byte-exact empty reconstruction, foreground uses final composited source pixels above alpha32; exact empty reconstruction is retained, while head-safe partition prevents edge halos on heads.
mask=(alpha>32);fg=np.zeros_like(bp);fg[mask]=bp[mask];bp[mask]=0;base=Image.fromarray(bp);above=Image.fromarray(fg);base.save(A/'runtime-base.png');above.save(A/'runtime-above.png')
quiet=np.zeros_like(g);quiet[42:44,31:33]=1;start=[1016,1376]
landmarks=[{'id':n,'x':x,'y':y}for n,x,y in [('spawn',*start),('west-loop',608,768),('east-loop',1440,768),('court',1024,512),('audience-aisle',1024,800),('south-loop',1024,1152),('west-team-threshold',336,736),('east-team-threshold',1712,736),('caster-approach',1024,416),('social-entry',1536,1312)]]
for x in landmarks:
 if x['x']%32==0:x['x']+=16
 x['floorClick']=[x['x'],x['y']+16]
# Exact physical room rectangles stop before team doors/circulation; native inclusion edges already converted exclusive-1.
areas=[{'id':'esports-caster-podium','name':'Caster and presentation','x':736,'y':256,'width':575,'height':191,'visible':True,'properties':[{'id':'esports-broadcast','type':'speakerMegaphone','name':'esports-caster','chatEnabled':False}]},{'id':'esports-spectators','name':'Spectator audience','x':736,'y':608,'width':575,'height':415,'visible':True,'properties':[{'id':'esports-listen','type':'listenerMegaphone','speakerZoneName':'esports-caster-podium','chatEnabled':False}]},{'id':'esports-arrival','name':'Arrival','x':1000,'y':1352,'width':31,'height':31,'visible':True,'properties':[{'id':'esports-start','type':'start','isDefault':True}]}]
for name,x in [('west',128),('east',1504)]:areas.append({'id':'esports-'+name+'-team','name':'Team '+name.title(),'x':x,'y':192,'width':383,'height':447,'visible':True,'properties':[{'id':'esports-'+name+'-team-call','type':'livekitRoomProperty','roomName':'esports-arena-v01-'+name+'-team','livekitRoomConfig':{'startWithAudioMuted':False,'startWithVideoMuted':False,'disableChat':False}}]})
jw(S/'collision-grid.json',{'tileSize':32,'width':C,'height':N,'grid':g.tolist(),'start':start,'speaker':[1024,416],'socialAnchors':social,'landmarks':landmarks});jw(S/'quiet-grid.json',{'grid':quiet.tolist()});jw(S/'seats.json',seats);jw(S/'runtime-layout.json',{'world':[W,H],'singleLevel':True,'start':start,'teamRooms':areas[-2:],'doors':doors,'placements':placements,'camera':'ordinary follow; no focus script','depthContract':'Original art below; lower chair backs and structural inner pixels above floorLayer, clipped against union of all twelve Greg upper14px head masks over every body-clear native position.'});jw(S/'areas.json',areas)
# Render source proof at actual native scale; QA actors never enter runtime layers.
frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('west',4),('east',7)]};empty=Image.alpha_composite(base,above);empty.save(Q/'runtime-empty-native.png');occupied=base.copy()
for z in seats+social+landmarks:occupied.alpha_composite(frames[z.get('facing','north'if z.get('kind')in ['team','spectator','caster']else'south')],(z['x']-16,z['y']-16))
occupied.alpha_composite(above);occupied.save(Q/'runtime-occupied-native.png')
for name,box in [('west-team',(96,128,544,736)),('caster',(704,112,1344,480)),('spectator',(720,608,1328,1024)),('arrival-social',(1376,1056,1920,1376))]:occupied.crop(box).save(Q/f'native32-{name}-occupied.png')
over=occupied.convert('RGB').resize((1024,H//2),Image.Resampling.LANCZOS);board=Image.new('RGB',(1056,H//2+72),'#101b20');board.paste(over,(16,54));dd=ImageDraw.Draw(board);dd.text((16,13),'CIRCUIT ARENA / REDUCED 50% OVERVIEW',font=bold(19),fill='#cadade');board.save(Q/'OVERVIEW-occupied-50percent.png')
jw(V/'build-report.json',{'world':[W,H],'tileSize':32,'spectatorSeats':len(seats),'teamSeats':sum(bool(x.get('group'))for x in social),'casterSeats':sum(x['kind']=='caster'for x in social),'casualSeats':sum(x['kind']=='casual'for x in social),'quietCells':int(quiet.sum()),'foregroundPixels':int(mask.sum()),'noTrueMultiheight':True,'qaActorsOnly':True});print(json.dumps(json.load(open(V/'build-report.json')),indent=2))
