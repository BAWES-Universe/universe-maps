"""Original campus compiler. Native 32px geometry; no reference-map assets/layout copied."""
import json, math, random
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
W,H,T=96,88,32
SIZE=(W*T,H*T)
rng=random.Random(41)
floor=Image.new('RGBA',SIZE,'#728c65');d=ImageDraw.Draw(floor)
backs=Image.new('RGBA',SIZE);bd=ImageDraw.Draw(backs)
blocked=set();seats=[];tables=[];covers={};buildings=[];portal_slots=[]
ART={n:Image.open(ROOT/'source/licensed-wa-village'/f'{n}.png').convert('RGBA') for n in ['tables','chairs','100R_Floor','decor','trees-shadow','grounds-assets','couches']}
def stamp(name,box,xy,size=None,target=None):
 im=ART[name].crop(box)
 if size:im=im.resize(size,Image.Resampling.LANCZOS)
 (floor if target is None else target).alpha_composite(im,tuple(map(int,xy)))
def rug(box,color='#526773'):
 x,y,w,h=box;d.rounded_rectangle((x*T+3,y*T+3,(x+w)*T-4,(y+h)*T-4),5,fill=color,outline='#a5a59a',width=2)
 for yy in range(y*T+7,(y+h)*T-5,3):d.line((x*T+7,yy,(x+w)*T-8,yy),fill='#627781')
 d.rectangle((x*T+12,y*T+12,(x+w)*T-13,(y+h)*T-13),outline='#89999b',width=2)

def fitted_shell(filename,w,h,door_x,front_rows,source_split):
 im=Image.open(ROOT/'source'/filename).convert('RGBA')
 im=im.crop(im.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox())
 sw,sh=im.size;scan=im.getchannel('A');yy=int(sh*.94);left=right=sw//2
 while left>0 and scan.getpixel((left,yy))<32:left-=1
 while right<sw-1 and scan.getpixel((right,yy))<32:right+=1
 assert left<sw//2<right, 'The central opening must have true alpha.'
 cut=int(sh*source_split);top=(h-front_rows)*T;out=Image.new('RGBA',(w*T,h*T))
 out.alpha_composite(im.crop((0,0,sw,cut)).resize((w*T,top),Image.Resampling.LANCZOS),(0,0))
 for source,dest in [((0,left),(0,door_x*T)),((left,right),(door_x*T,(door_x+6)*T)),((right,sw),((door_x+6)*T,w*T))]:
  out.alpha_composite(im.crop((source[0],cut,source[1],sh)).resize((dest[1]-dest[0],front_rows*T),Image.Resampling.LANCZOS),(dest[0],top))
 return out
def rect(box,color,outline=None):
 x,y,w,h=box;d.rectangle((x*T,y*T,(x+w)*T-1,(y+h)*T-1),fill=color,outline=outline)
def wall(box):
 x,y,w,h=box;rect(box,'#435258','#b9b9a8')
 if h==1:
  for yy in range(5,30):
   shade=yy/30;d.line((x*T+2,y*T+yy,(x+w)*T-3,y*T+yy),fill=(int(203-35*shade),int(201-37*shade),int(180-30*shade)))
  d.line((x*T+2,y*T+5,(x+w)*T-3,y*T+5),fill='#ece6ce',width=2)
  for xx in range(x*T+64,(x+w)*T,64):d.line((xx,y*T+6,xx,y*T+29),fill='#969b8f')
 else:
  for xx in range(4,29):
   shade=xx/32;d.line((x*T+xx,y*T+2,x*T+xx,(y+h)*T-3),fill=(int(201-38*shade),int(201-36*shade),int(183-30*shade)))
  for yy in range(y*T+64,(y+h)*T,64):d.line((x*T+4,yy,x*T+28,yy),fill='#9eaa9d')
def block(box):
 x,y,w,h=box;blocked.update((a,b) for a in range(x,x+w) for b in range(y,y+h))
def material(box,kind):
 x,y,w,h=box
 if kind=='sand':
  rect(box,'#dbcba7')
  for _ in range(w*h*65):
   xx=x*T+rng.randrange(w*T);yy=y*T+rng.randrange(h*T)
   d.point((xx,yy),fill=rng.choice(['#d0bc93','#dfcfac','#e8d8b8','#d5c29e']))
  return
 if kind in ['wood','slate']:
  tile=ART['100R_Floor'].crop((0,32,128,160) if kind=='wood' else (512,736,640,864))
  for yy in range(y*T,(y+h)*T,128):
   for xx in range(x*T,(x+w)*T,128):floor.alpha_composite(tile.crop((0,0,min(128,(x+w)*T-xx),min(128,(y+h)*T-yy))),(xx,yy))
 else:
  rect(box,'#c8c5b9' if kind=='stone' else '#dbcba7')
  for yy in range(y*T,(y+h)*T,16):
   for xx in range(x*T,(x+w)*T,32):
    xx1=min(xx+31,(x+w)*T-1);yy1=min(yy+15,(y+h)*T-1)
    tone=rng.choice(['#c4c1b5','#c9c6bb','#cecbc0','#babbb2']) if kind=='stone' else rng.choice(['#dac9a5','#dfcfac','#d6c5a0'])
    d.rectangle((xx+1,yy+1,xx1,yy1),fill=tone)
    for _ in range(5):d.point((xx+rng.randrange(32),yy+rng.randrange(16)),fill='#ddd9cb' if kind=='stone' else '#e8d8b5')
 # A built edge gives every deck and path an actual thickness.
 d.line((x*T,(y+h)*T-1,(x+w)*T-1,(y+h)*T-1),fill='#8c9287',width=2)
# Landscape texture is original, generated once with a fixed seed.
for _ in range(21000):
 x=rng.randrange(W*T);y=rng.randrange(H*T);d.line((x,y,x+2,y),fill=rng.choice(['#7c986a','#627f56','#91a777']))
# An interconnected street grid, with separate front square and northern lanes.
for box in [(4,26,88,6),(34,4,7,67),(4,51,88,7),(4,4,6,60),(90,4,3,67),(4,63,89,6),(40,26,5,32),(67,4,6,60)]:material(box,'stone')
material((8,51,56,12),'stone');material((4,69,89,9),'sand')
# Shore is separated from the playable beach by a shallow edging, no hidden pits.
rect((1,78,94,H-79),'#537f90');block((1,78,94,H-79))
for yy in range(78*T,(H-1)*T):
 depth=(yy-78*T)/((H-79)*T)
 d.line((T,yy,(W-1)*T-1,yy),fill=(int(92-25*depth),int(145-32*depth),int(155-22*depth)))
for yy in range(78*T+6,(H-1)*T,24):
 for xx in range(32,95*T,64):
  offset=rng.randrange(16);d.arc((xx+offset,yy,xx+offset+40,yy+10),0,150,fill='#9bbcb9',width=1)
d.line((T,78*T,(W-1)*T-1,78*T),fill='#ece2c4',width=4)
shore=[(xx,round(78*T-12+8*math.sin(xx/93)+5*math.sin(xx/211))) for xx in range(T,(W-1)*T,4)]
d.polygon(shore+[((W-1)*T,79*T),(T,79*T)],fill='#82a7a2')
d.line(shore,fill='#e6dfc4',width=3)
for i,(xx,yy) in enumerate(shore):
 if i%5==0:d.line((xx,yy-3,xx+8,yy-5),fill='#f1e7cc',width=1)
for box in [(0,0,W,1),(0,H-1,W,1),(0,1,1,H-2),(W-1,1,1,H-2)]:block(box);rect(box,'#344b46')
def chair(x,y,color='#657d83'):
 seats.append([x,y])
 # Native 32px furniture, split at seat depth so a Woka occupies it naturally.
 im=ART['chairs'].crop((896,320,928,368) if color=='work' else (608,64,640,112) if color in ['social','pantry'] else (896,256,928,304))
 floor.alpha_composite(im,(x*T,y*T-24))
 backs.alpha_composite(im.crop((0,34,32,48)),(x*T,y*T+10))
def table(x,y,w,h,kind='work'):
 tables.append([x,y,w,h]);block((x,y,w,h))
 if kind in ['social','pantry','creative']:
  # A carved timber communal café table replaces the schematic slab.
  stamp('tables',(64,2240,224,2304),(x*T,y*T-10),(w*T,h*T+10))
 elif kind=='meeting':
  stamp('tables',(864,736,1024,818),(x*T,y*T-14),(w*T,h*T+14))
 else:
  stamp('tables',(544,736,704,818),(x*T,y*T-14),(w*T,h*T+14))
 if kind=='work':
  for a in range(x,x+w,2):stamp('decor',(608,275,641,321),(a*T+8,y*T-9),(24,32))
 elif kind=='pantry':
  stamp('decor',(224,330,291,383),(x*T+4,y*T-12),(48,44))
  stamp('trees-shadow',(1395,151,1478,238),((x+w)*T-28,y*T-8),(28,32))
 elif kind=='creative':
  for j,color in enumerate(['#e9c76e','#d4b6d8','#9bc5c8']):
   d.rectangle((x*T+12+j*21,y*T+7,x*T+27+j*21,y*T+23),fill=color,outline='#7e8177')
 else:
  stamp('decor',(109,357,148,385),(x*T+12,y*T+3),(24,18))
  stamp('decor',(274,493,289,507),((x+w)*T-22,y*T+5),(10,10))
 for sx in range(x,x+w):chair(sx,y+h+1,kind)
def planter(x,y,w=3,h=3):
 block((x,y,w,h));rect((x,y,w,h),'#797e68','#d4c8a7')
 d.rectangle((x*T+5,y*T+5,(x+w)*T-6,(y+h)*T-6),fill='#486e45')
 for _ in range(w*h*9):
  px=x*T+8+rng.randrange(w*T-16);py=y*T+8+rng.randrange(h*T-16)
  d.ellipse((px-5,py-3,px+5,py+4),fill=rng.choice(['#6f944e','#8ea75b','#4b7b45','#b0b66b']))
 # Reference nursery sprites give beds height and recognisable species.
 if h>=6:
  for yy in range(y+2,y+h,4):stamp('trees-shadow',(977,18,1118,280),((x+w/2)*T-36,yy*T-72),(72,134),backs)
 elif w>=4:
  for xx in range(x+1,x+w,3):stamp('trees-shadow',(51,675,106,758),(xx*T-15,y*T-8),(32,48),backs)
 else:stamp('trees-shadow',(290,641,413,826),(x*T+(w*T-80)//2,y*T+h*T-122),(80,122),backs)
def building(name,x,y,w,h,kind='office'):
 material((x,y,w,h),'wood' if kind!='portal' else 'slate')
 # Structural perimeter surrounds exactly the shell rectangle, with two clear doors.
 mid=x+w//2;door=mid-3
 for box in [(x,y,door-x,1),(door+6,y,x+w-door-6,1),(x,y+1,1,h-1),(x+w-1,y+1,1,h-1),(x+1,y+h-1,door-x-1,1),(door+6,y+h-1,x+w-door-7,1)]:
  if box[2]>0:block(box);wall(box)
 buildings.append(dict(name=name,footprint=[x,y,w,h],interior=[x+1,y+1,w-2,h-2],front_door=[door,y+h-1,6,1],rear_door=[door,y,6,1]))
 shell=Image.new('RGBA',SIZE);s=ImageDraw.Draw(shell)
 if kind=='tower':
  # Full-footprint roof terraces are part of the removable architecture, not an exposed office.
  s.rectangle((x*T,y*T,(x+w)*T-1,(y+h-5)*T-1),fill='#6b746f',outline='#c1bda8',width=4)
  for yy in range(y*T+10,(y+h-5)*T,16):s.line((x*T+6,yy,(x+w)*T-7,yy),fill='#7c867c')
  for xx in range(x*T+8,(x+w)*T-8,32):s.line((xx,y*T+4,xx,(y+h-5)*T),fill='#616e68')
  shell.alpha_composite(fitted_shell('tower-complete-original.png',w,h,door-x,5,.84),(x*T,y*T))
 elif kind!='portal':
  s.rectangle((x*T,y*T,(x+w)*T-1,(y+h-4)*T-1),fill='#596d63',outline='#b8bea7',width=3)
  shell.alpha_composite(fitted_shell('cowork-polished-original.png',w,h,door-x,4,.74),(x*T,y*T))
 else:
  s.rectangle((x*T,y*T,(x+w)*T-1,(y+h-4)*T),fill='#6d806d',outline='#b6b8a0',width=3)
  shell.alpha_composite(fitted_shell('portal-pavilion-polished-original.png',w,h,door-x,4,.76),(x*T,y*T))
 covers[name+'-glass-cover']=shell
 return buildings[-1]
# Buildings behind the tower, with a complete street between them and the tower.
building('cowork',10,8,24,16)
building('portal',44,8,23,16,'portal')
building('staff',73,8,17,16)
building('tower',10,32,24,19,'tower')
# Room-scale rugs, wall-mounted storage and presentation furniture give usable zones identity.
for box in [(12,34,6,6),(25,34,7,6),(12,45,6,5),(26,45,6,5),(12,10,6,5),(26,10,6,5),(12,17,6,6),(26,17,6,6),(75,10,5,5),(83,10,5,5)]:rug(box)
# Place wall-mounted details on structural collision only; routes are unchanged.
for x,y in [(13,32),(26,32),(13,8),(27,8),(76,8),(84,8)]:
 block((x,y+1,3,1));stamp('decor',(447,615,555,704),(x*T,y*T),(96,64))
stamp('decor',(202,900,342,991),(12*T,43*T-42),(128,74))
# Inlaid arrival medallion and linear granite bands organise a square, rather than a blank grid.
d.ellipse((19*T,52*T,25*T,57*T),fill='#a5a99e',outline='#e8e1c9',width=6)
d.ellipse((19*T+14,52*T+14,25*T-14,57*T-14),outline='#747f7b',width=3)
for j in range(16):
 a=j*math.tau/16;b=(j+1)*math.tau/16;r1=54 if j%2==0 else 24;r2=54 if (j+1)%2==0 else 24
 d.polygon([(22*T,54.5*T),(22*T+math.cos(a)*r1,54.5*T+math.sin(a)*r1*.82),(22*T+math.cos(b)*r2,54.5*T+math.sin(b)*r2*.82)],fill='#d7ccb0' if j%2==0 else '#7b8985')
for x in [18,25]:d.rectangle((x*T+9,51*T,x*T+16,63*T-1),fill='#7b8988')
for box in [(9,57,8,5),(26,57,7,5),(46,58,6,5),(55,58,6,5)]:material(box,'wood')
# Upper coworking: two focus clusters and two shared project tables, central clear aisle.
for args in [(13,11,4,1,'work'),(27,11,3,1,'work'),(13,18,4,2,'meeting'),(27,18,3,2,'creative'),(76,11,3,1,'work'),(84,11,3,1,'work'),(76,18,3,2,'pantry'),(84,18,3,2,'meeting'),(13,35,4,2,'meeting'),(26,35,4,2,'meeting'),(13,46,3,1,'meeting'),(27,46,3,1,'work')]:table(*args)
# Two-seat lounge and standing project board keep the six-tile central aisle untouched.
rug((12,40,6,3),'#526773')
block((12,40,2,1));stamp('couches',(586,1152,662,1211),(12*T,40*T-16),(64,64))
for xx in [12,13]:seats.append([xx,41])
stamp('couches',(586,1196,662,1211),(12*T,41*T+10),(64,14),backs)
block((16,40,1,1));stamp('tables',(65,1024,127,1089),(16*T,40*T-8),(32,40))
block((28,41,4,1));stamp('decor',(202,900,342,991),(28*T,39*T),(128,80),backs)
# A few pots and task objects sit on existing structural footprints, never on routes.
for x,y in [(10,42),(33,42),(10,49),(33,49),(44,22),(66,22)]:stamp('trees-shadow',(1395,151,1478,238),(x*T-4,y*T-14),(40,46),backs)
# Near-spawn team meeting room: one explicit side door, no hidden exit walls.
for box in [(11,43,9,1),(19,44,1,3),(19,49,1,1)]:
 block(box);wall(box)
# Ground-accessible podium terraces link the offices to the rear street.
material((10,24,24,2),'wood')
for xx in range(10,34):
 if not 19<=xx<25:bd.line((xx*T,26*T-4,(xx+1)*T,26*T-4),fill='#bac2b6',width=3)
material((73,24,17,2),'wood')
for xx in range(73,90):
 if not 78<=xx<84:bd.line((xx*T,26*T-4,(xx+1)*T,26*T-4),fill='#bac2b6',width=3)
# Portal bays are original placed artwork, all unbound. Editor areas are supplied separately.
for i,(x,y) in enumerate([(47,11),(54,11),(61,11),(47,18),(54,18),(61,18)]):
 portal=Image.open(ROOT/'source/portal-polished-original.png').convert('RGBA')
 portal=portal.crop(portal.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox()).resize((96,96),Image.Resampling.LANCZOS)
 d.ellipse((x*T-5,y*T+28,(x+3)*T+5,y*T+66),fill='#3f535d',outline='#b5c6c5',width=2)
 backs.alpha_composite(portal,(x*T,y*T-32))
 portal_slots.append(dict(id='bawes-portal-'+str(i+1),name='Portal bay '+str(i+1),x=(x+1)*T,y=(y+1)*T,width=T,height=T,visible=True,properties=[]))
# Future StudentHub has its own useful court today, with generous edges for a later wing.
material((45,34,18,16),'stone')
for args in [(47,36,3,1,'work'),(57,36,3,1,'work'),(47,44,3,2,'meeting'),(57,44,3,2,'meeting')]:table(*args)
for p in [(45,34,1,16),(62,34,1,16)]:planter(*p)
# Team welcome/social cluster beside the outdoor spawn, and informal meeting gardens.
for args in [(12,58,3,1,'social'),(28,58,3,1,'social'),(47,59,3,1,'social'),(56,59,3,1,'social'),(14,71,3,1,'social'),(28,71,3,1,'social')]:table(*args)
# Open-air stage and conversation booths use the same native collision/furniture rules.
material((73,45,16,6),'wood')
rect((73,45,16,1),'#334955');block((73,45,16,1))
for x in [73,88]:rect((x,46,1,2),'#25333d','#6b7e88');block((x,46,1,2))
stamp('grounds-assets',(537,20,1028,348),(73*T,44*T),(16*T,7*T))
stamp('grounds-assets',(537,20,1028,68),(73*T,44*T),(16*T,T),backs)
for x in [75,78,81,84,87]:
 for y in [54,57]:chair(x,y)
for x in [74,83]:
 material((x,35,6,7),'wood');rect((x,35,6,1),'#50616a');block((x,35,6,1));table(x+1,37,3,1,'meeting')
# Planted street edges leave junctions and all entrances open.
for p in [(5,8,3,14),(36,8,3,14),(69,8,2,14),(12,28,5,2),(27,28,5,2),(46,28,5,2),(59,28,5,2),(5,35,3,12),(36,35,3,12),(8,59,2,3),(33,59,3,3),(66,59,4,3),(75,63,12,2),(46,71,4,3),(62,71,4,3)]:planter(*p)
# Planted outer edges break the empty rectangular lawn while keeping promenade widths.
for xx in [2,94]:
 for yy in [6,15,24,34,44,54,65,73]:
  block((xx-1,yy,2,2))
  stamp('trees-shadow',(18,16,286,334),(xx*T-42,yy*T-78),(96,128),backs)
# Shallow boardwalk insets and soft dune vegetation give the beach a usable sequence.
for x in [10,25,43,59,76]:
 material((x,69,7,2),'wood')
 for dx in [0,5]:
  block((x+dx,70,2,1));stamp('grounds-assets',(17,31,97,80),((x+dx)*T,70*T-16),(64,48))
 for j in range(48):
  xx=(x+3)*T+rng.randrange(96);yy=75*T+rng.randrange(70)
  d.line((xx,yy,xx-2,yy-5),fill=rng.choice(['#a4a76c','#9b9d5d','#b0aa73']))
# Cloth parasols are foreground canopies above the existing beach café tables.
for tx in [15,29]:
 cx=tx*T+16;cy=70*T+8
 d.ellipse((cx-64,cy+30,cx+66,cy+72),fill='#c1b38e')
 d.line((cx,cy+12,cx,72*T),fill='#9e8460',width=4)
 for j in range(12):
  a=j*math.tau/12;b=(j+1)*math.tau/12
  points=[(cx,cy-18),(cx+math.cos(a)*70,cy+math.sin(a)*39),(cx+math.cos(b)*70,cy+math.sin(b)*39)]
  bd.polygon(points,fill=['#e5d5b2','#f3e7cb','#cdbb96'][j%3],outline='#b5a17e')
 bd.ellipse((cx-4,cy-22,cx+4,cy-14),fill='#a3845c')
# A reflecting basin animates independently of roof visibility.
pond=[38,59,3,3];block(pond)
water=Image.open(ROOT/'water.png').convert('RGBA')
doors=[dict(name='tower-front-door',box=[19,50,6,1]),dict(name='tower-rear-door',box=[19,32,6,1]),dict(name='meeting-door',box=[19,47,1,2],lockedVariable='bawesMeetingLocked')]
# Export faithful tile atlases; explicit collision is never inferred from artwork.
layers=[];tilesets=[];gid=1
def atlas(name,img):
 global gid
 img.save(ROOT/(name+'.png'));tilesets.append(dict(firstgid=gid,name=name,image=name+'.png',imagewidth=SIZE[0],imageheight=SIZE[1],tilewidth=T,tileheight=T,tilecount=W*H,columns=W,margin=0,spacing=0))
 data=[gid+i if img.crop(((i%W)*T,(i//W)*T,(i%W+1)*T,(i//W+1)*T)).getbbox() else 0 for i in range(W*H)];gid+=W*H;return data
def layer(name,data):layers.append(dict(id=len(layers)+1,type='tilelayer',name=name,x=0,y=0,width=W,height=H,opacity=1,visible=True,data=data))
layer('ground-and-furniture',atlas('ground',floor))
watergid=gid;gid+=432
tilesets.append(dict(firstgid=watergid,name='water',image='water.png',imagewidth=768,imageheight=576,tilewidth=32,tileheight=32,tilecount=432,columns=24,tiles=[dict(id=ry*24+rx,animation=[dict(tileid=(frame//8*3+ry)*24+(frame%8)*3+rx,duration=40) for frame in range(48)]) for ry in range(3) for rx in range(3)]))
px,py,pw,ph=pond
layer('pond-motion',[watergid+(y-py)*24+x-px if px<=x<px+pw and py<=y<py+ph else 0 for y in range(H) for x in range(W)])
Image.new('RGBA',(64,32)).save(ROOT/'logic.png');logicgid=gid;gid+=2
tilesets.append(dict(firstgid=logicgid,name='logic',image='logic.png',imagewidth=64,imageheight=32,tilewidth=32,tileheight=32,tilecount=2,columns=2,tiles=[dict(id=0,properties=[dict(name='collides',type='bool',value=True)])]))
layer('persistent-collision',[logicgid if (x,y) in blocked else 0 for y in range(H) for x in range(W)])
layer('start',[logicgid+1 if (x,y)==(22,53) else 0 for y in range(H) for x in range(W)])
for b in buildings:
 ix,iy,iw,ih=b['interior'];layer(b['name']+'-interior',[logicgid+1 if ix<=x<ix+iw and iy<=y<iy+ih else 0 for y in range(H) for x in range(W)])
layers.append(dict(id=len(layers)+1,type='objectgroup',name='floorLayer',x=0,y=0,opacity=1,visible=True,objects=[dict(id=1,name='bawesMeetingLocked',type='variable',point=True,x=18*T,y=48*T,width=0,height=0,rotation=0,visible=True,properties=[dict(name='default',type='bool',value=False),dict(name='persist',type='bool',value=False)])]))
doorart=Image.new('RGBA',(64,32));dd=ImageDraw.Draw(doorart)
dd.rectangle((0,8,31,24),fill=(107,161,179,180),outline='#d7e2dc',width=2);dd.line((16,9,16,23),fill='#40596c',width=2)
dd.rectangle((40,0,56,31),fill=(107,161,179,180),outline='#d7e2dc',width=2);dd.line((41,16,55,16),fill='#40596c',width=2)
doorart.save(ROOT/'doors.png');doorgid=gid;gid+=2
tilesets.append(dict(firstgid=doorgid,name='doors',image='doors.png',imagewidth=64,imageheight=32,tilewidth=32,tileheight=32,tilecount=2,columns=2,tiles=[dict(id=i,properties=[dict(name='collides',type='bool',value=True)]) for i in range(2)]))
for door in doors:
 dx,dy,dw,dh=door['box'];layer(door['name'],[doorgid+(dw==1) if dx<=x<dx+dw and dy<=y<dy+dh else 0 for y in range(H) for x in range(W)])
layer('seat-backs',atlas('seat-backs',backs))
for name,img in covers.items():layer(name,atlas(name.removesuffix('-cover'),img))
mapdata=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=W,height=H,tilewidth=T,tileheight=T,nextlayerid=len(layers)+1,nextobjectid=2,layers=layers,tilesets=tilesets,properties=[dict(name='script',type='string',value='runtime.js'),dict(name='mapCopyright',type='string',value='Original BAWES campus layout and architecture with selected 100 Roads WA Village furniture/material assets, used under user-reported partnership permission; see source/ASSET-PROVENANCE.md.')])
(ROOT/'campus.tmj').write_text(json.dumps(mapdata,separators=(',',':'))+'\n')
tower=next(b for b in buildings if b['name']=='tower')
layout=dict(status='original town architecture in progress; visual acceptance pending',grid=[W,H,T],spawn=[22,53],entrance=tower['front_door'],rear_entrance=tower['rear_door'],interior=tower['interior'],building_footprint=tower['footprint'],buildings=buildings,studenthub_reserve=[45,34,18,16],seats=seats,tables=tables,pond=pond,main_route_width_px=192,portal_slots=portal_slots,doors=doors,meeting_room=[11,44,8,6],areas={'stage':[73,45,16,6],'beach':[4,69,89,9],'booths':[74,35,15,7],'staff_balcony':[73,24,17,2],'cowork_terrace':[10,24,24,2],'sea':[1,78,94,H-79]},tower_asset_bounds=[320,51*T-590,768,590])
(ROOT/'source/layout.json').write_text(json.dumps(layout,indent=2)+'\n')
(ROOT/'source/portal-areas.json').write_text(json.dumps(portal_slots,indent=2)+'\n')
# Static native Tiled maps do not install editor WAM areas; these are ready-to-configure coordinates.
contracts=[dict(layer=b['name']+'-interior',cover=b['name']+'-glass-cover',bounds=[n*T for n in b['interior']]) for b in buildings]
runtime=(ROOT/'source/runtime.template.js').read_text().replace('ROOM_CONTRACTS',json.dumps(contracts)).replace('DOOR_CONTRACTS',json.dumps(doors))
(ROOT/'runtime.js').write_text(runtime)
preview=floor.copy();preview.alpha_composite(water.crop((0,0,96,96)),(px*T,py*T));preview.alpha_composite(backs)
preview.save(ROOT/'review/inside.png');outside=preview.copy()
for img in covers.values():outside.alpha_composite(img)
outside.save(ROOT/'review/outside.png');floor.save(ROOT/'review/layout.png')
print(f'Built original {W}x{H} campus, {len(buildings)} complete cutaway footprints, {len(seats)} seats, six unbound portal bays.')
