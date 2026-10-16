"""Original campus compiler. Native 32px geometry; no reference-map assets/layout copied."""
import json, math, random
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
W,H,T=96,88,32
SIZE=(W*T,H*T)
rng=random.Random(41)
floor=Image.new('RGBA',SIZE,'#64776c');d=ImageDraw.Draw(floor)
backs=Image.new('RGBA',SIZE);bd=ImageDraw.Draw(backs)
blocked=set();seats=[];tables=[];covers={};buildings=[];portal_slots=[]
def rect(box,color,outline=None):
 x,y,w,h=box;d.rectangle((x*T,y*T,(x+w)*T-1,(y+h)*T-1),fill=color,outline=outline)
def block(box):
 x,y,w,h=box;blocked.update((a,b) for a in range(x,x+w) for b in range(y,y+h))
def material(box,kind):
 x,y,w,h=box
 colors={'stone':('#b9b6ab','#aaa89e','#cecbc0'),'wood':('#b7a181','#a38c6f','#cbb796'),'slate':('#6d7880','#5f6972','#859099'),'sand':('#d5c7a4','#ccbd99','#e3d7b8')}
 base,seam,light=colors[kind];rect(box,base)
 tw,th=(64,32) if kind=='stone' else (64,16) if kind=='wood' else (32,32)
 for yy in range(y*T,(y+h)*T,th):
  for xx in range(x*T,(x+w)*T,tw):
   d.line((xx,yy,min(xx+tw-1,(x+w)*T-1),yy),fill=seam)
   if kind!='sand':d.line((xx,yy,xx,min(yy+th-1,(y+h)*T-1)),fill=seam)
   for _ in range(5):d.point((xx+rng.randrange(min(tw,(x+w)*T-xx)),yy+rng.randrange(min(th,(y+h)*T-yy))),fill=light)
# Landscape texture is original, generated once with a fixed seed.
for _ in range(21000):
 x=rng.randrange(W*T);y=rng.randrange(H*T);d.line((x,y,x+2,y),fill=rng.choice(['#6c8071','#5d7267','#748575']))
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
for box in [(0,0,W,1),(0,H-1,W,1),(0,1,1,H-2),(W-1,1,1,H-2)]:block(box);rect(box,'#344b46')
def chair(x,y,color='#657d83'):
 seats.append([x,y]);d.ellipse((x*T+2,y*T+8,x*T+30,y*T+23),fill='#4d514d')
 d.rounded_rectangle((x*T+5,y*T-5,x*T+27,y*T+16),5,fill=color,outline='#bdc7be')
 bd.rounded_rectangle((x*T+4,y*T+9,x*T+28,y*T+17),3,fill='#354d55',outline='#a3b6b3')
 bd.line((x*T+8,y*T+12,x*T+24,y*T+12),fill='#6d8d91')
def table(x,y,w,h,kind='work'):
 tables.append([x,y,w,h]);block((x,y,w,h))
 d.rounded_rectangle((x*T+3,y*T+5,(x+w)*T-1,(y+h)*T-1),5,fill='#514e49')
 d.rounded_rectangle((x*T+2,y*T+1,(x+w)*T-4,(y+h)*T-6),7,fill='#d1b58a' if kind!='meeting' else '#d9d5c8',outline='#776d5d',width=2)
 for xx in range(x*T+7,(x+w)*T-5,16):d.line((xx,y*T+6,xx,(y+h)*T-10),fill='#c4a77e' if kind!='meeting' else '#c5c4bc')
 if kind=='work':
  for a in range(x,x+w,2):
   d.rounded_rectangle((a*T+7,y*T+5,a*T+26,y*T+18),2,fill='#24323d',outline='#6a7d89')
   d.rectangle((a*T+10,y*T+8,a*T+23,y*T+14),fill='#7b96a7')
   d.line((a*T+9,y*T+22,a*T+24,y*T+22),fill='#eee4d0',width=3)
 else:
  d.rectangle((x*T+10,y*T+8,x*T+24,y*T+18),fill='#f1ece0')
  d.ellipse(((x+w)*T-23,y*T+8,(x+w)*T-15,y*T+16),fill='#ece5d7',outline='#797166')
 for sx in range(x,x+w):chair(sx,y+h+1)
def planter(x,y,w=3,h=3):
 block((x,y,w,h));rect((x,y,w,h),'#46574d','#8b9c8e')
 d.rectangle((x*T+4,y*T+4,(x+w)*T-5,(y+h)*T-5),fill='#344b3c')
 for _ in range(w*h*14):
  px=x*T+8+rng.randrange(w*T-16);py=y*T+8+rng.randrange(h*T-16)
  d.ellipse((px-5,py-3,px+5,py+4),fill=rng.choice(['#5d7f58','#709164','#8b9f70','#476e51']))
def building(name,x,y,w,h,kind='office'):
 material((x,y,w,h),'wood' if kind!='portal' else 'slate')
 # Structural perimeter surrounds exactly the shell rectangle, with two clear doors.
 mid=x+w//2;door=mid-3
 for box in [(x,y,door-x,1),(door+6,y,x+w-door-6,1),(x,y+1,1,h-1),(x+w-1,y+1,1,h-1),(x+1,y+h-1,door-x-1,1),(door+6,y+h-1,x+w-door-7,1)]:
  if box[2]>0:block(box);rect(box,'#303d46','#8d999c')
 buildings.append(dict(name=name,footprint=[x,y,w,h],interior=[x+1,y+1,w-2,h-2],front_door=[door,y+h-1,6,1],rear_door=[door,y,6,1]))
 shell=Image.new('RGBA',SIZE);s=ImageDraw.Draw(shell)
 if kind=='tower':
  # Opaque podium roof fills the complete shell footprint outside; no exposed office floor.
  s.rectangle((x*T,y*T,(x+w)*T-1,(y+h-4)*T-1),fill='#354552',outline='#83959e',width=3)
  for yy in range(y*T+12,(y+h-4)*T,32):s.line((x*T+7,yy,(x+w)*T-8,yy),fill='#415662',width=1)
  art=Image.open(ROOT/'source/tower-cutout-original.png').convert('RGBA').crop((37,14,1432,1086)).resize((w*T,590),Image.Resampling.LANCZOS)
  for lo,hi in [(x+1,door),(door+6,x+w-1)]:s.rectangle((lo*T,(y+h-4)*T,hi*T-1,(y+h-1)*T-1),fill=(109,135,168,38))
  shell.alpha_composite(art,(x*T,(y+h)*T-590))
 else:
  # Full-footprint overhead shell, long transparent frontage; all removed locally on entry.
  roofbottom=y+h-4
  s.rectangle((x*T,y*T,(x+w)*T-1,roofbottom*T-1),fill=(54,76,85,235),outline='#b6c5c1',width=3)
  for xx in range(x*T+8,(x+w)*T-8,32):
   s.rectangle((xx,y*T+8,xx+23,roofbottom*T-8),fill=(103,156,166,105) if kind=='portal' else '#496976',outline=(167,204,205,155),width=1)
  if kind=='portal':
   for yy in range(y*T+8,roofbottom*T,64):s.line((x*T+6,yy,(x+w)*T-6,yy),fill='#a5c7c7',width=3)
  else:
   s.rectangle(((x+2)*T,(y+2)*T,(x+w-2)*T,(y+4)*T),fill='#75949b',outline='#b5c6c4',width=2)
  for lo,hi in [(x,door),(door+6,x+w)]:
   s.rectangle((lo*T,roofbottom*T,hi*T-1,(y+h)*T-1),fill=(103,163,184,48),outline='#aabfc0',width=2)
   for xx in range(lo*T,hi*T,64):s.line((xx,roofbottom*T,xx,(y+h)*T-1),fill='#91acb5',width=3)
   s.line((lo*T,(y+h)*T-5,hi*T-1,(y+h)*T-5),fill='#344f60',width=5)
  s.rectangle((door*T,roofbottom*T,(door+6)*T-1,roofbottom*T+8),fill='#cbbf9c')
 covers[name+'-glass-cover']=shell
 return buildings[-1]
# Buildings behind the tower, with a complete street between them and the tower.
building('cowork',10,8,24,16)
building('portal',44,8,23,16,'portal')
building('staff',73,8,17,16)
building('tower',10,32,24,19,'tower')
# Upper coworking: two focus clusters and two shared project tables, central clear aisle.
for args in [(13,11,4,1,'work'),(27,11,3,1,'work'),(13,18,4,2,'meeting'),(27,18,3,2,'meeting'),(76,11,3,1,'work'),(84,11,3,1,'work'),(76,18,3,2,'meeting'),(84,18,3,2,'meeting'),(13,35,4,2,'meeting'),(26,35,4,2,'meeting'),(13,46,3,1,'meeting'),(27,46,3,1,'work')]:table(*args)
# Near-spawn team meeting room: one explicit side door, no hidden exit walls.
for box in [(11,43,9,1),(19,44,1,3),(19,49,1,1)]:
 block(box);rect(box,'#61777b','#adbcba')
# Ground-accessible podium terraces link the offices to the rear street.
material((10,24,24,2),'wood')
for xx in range(10,34):
 if not 19<=xx<25:bd.line((xx*T,26*T-4,(xx+1)*T,26*T-4),fill='#bac2b6',width=3)
material((73,24,17,2),'wood')
for xx in range(73,90):
 if not 78<=xx<84:bd.line((xx*T,26*T-4,(xx+1)*T,26*T-4),fill='#bac2b6',width=3)
# Portal bays are original placed artwork, all unbound. Editor areas are supplied separately.
for i,(x,y) in enumerate([(47,11),(54,11),(61,11),(47,18),(54,18),(61,18)]):
 color=['#9f90d0','#6fabc0','#c5b37c'][i%3]
 d.ellipse((x*T,y*T+22,(x+3)*T,y*T+62),fill='#3c525e',outline=color,width=3)
 bd.arc((x*T+3,y*T-16,(x+3)*T-3,y*T+65),180,360,fill=color,width=6)
 for xx in [x*T+3,(x+3)*T-9]:bd.rectangle((xx,y*T+20,xx+5,y*T+44),fill=color)
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
for x in [75,78,81,84,87]:
 for y in [54,57]:chair(x,y)
for x in [74,83]:
 material((x,35,6,7),'wood');rect((x,35,6,1),'#50616a');block((x,35,6,1));table(x+1,37,3,1,'meeting')
# Planted street edges leave junctions and all entrances open.
for p in [(5,8,3,14),(36,8,3,14),(69,8,2,14),(12,28,5,2),(27,28,5,2),(46,28,5,2),(59,28,5,2),(5,35,3,12),(36,35,3,12),(8,59,2,3),(33,59,3,3),(66,59,4,3),(75,63,12,2),(46,71,4,3),(62,71,4,3)]:planter(*p)
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
mapdata=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=W,height=H,tilewidth=T,tileheight=T,nextlayerid=len(layers)+1,nextobjectid=2,layers=layers,tilesets=tilesets,properties=[dict(name='script',type='string',value='runtime.js'),dict(name='mapCopyright',type='string',value='Original BAWES campus. No WA Village artwork, map data or layout incorporated.')])
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
