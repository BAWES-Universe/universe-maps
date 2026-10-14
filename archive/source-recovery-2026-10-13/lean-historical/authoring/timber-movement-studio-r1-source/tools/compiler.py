from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import random,json,math,hashlib,collections,shutil
R=Path(__file__).resolve().parents[1]; T=32; C=44; N=36; W=C*T; H=N*T
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
def js(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def props(**o):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in o.items()]
def tint(c,v):return tuple(max(0,min(255,n+v)) for n in c)
class Map:
 def __init__(self,slug,title,category,palette):
  self.slug,self.title,self.category=slug,title,category;self.p=palette;self.rng=random.Random(slug);self.base=Image.new('RGBA',(W,H),palette['outer']);self.above=Image.new('RGBA',(W,H));self.d=ImageDraw.Draw(self.base);self.a=ImageDraw.Draw(self.above);self.g=[[1]*C for _ in range(N)];self.seats=[];self.anchors=[];self.zones=[];self.spawn=(22,33);self.cropboxes=[]
 def block(self,x,y,w,h,val=1):
  for yy in range(y,y+h):
   for xx in range(x,x+w):self.g[yy][xx]=val
 def floor(self,x,y,w,h,kind='stone',color=None):
  col=color or self.p['floor'];self.block(x,y,w,h,0)
  for yy in range(y*T,(y+h)*T,T):
   for xx in range(x*T,(x+w)*T,T):
    c=tint(col,self.rng.randint(-5,5));self.d.rectangle((xx,yy,xx+31,yy+31),fill=c)
    if kind=='wood':
     for dy in [0,8,16,24]:
      self.d.line((xx,yy+dy,xx+31,yy+dy),fill=tint(c,-16));self.d.line((xx+((dy*3)%29),yy+dy+1,xx+((dy*3)%29),yy+dy+7),fill=tint(c,-11))
      for i in range(3):
       sx=self.rng.randrange(24);self.d.line((xx+sx,yy+dy+3+i,xx+min(30,sx+8),yy+dy+3+i),fill=tint(c,self.rng.choice([-8,7])))
    else:
     self.d.line((xx,yy+31,xx+31,yy+31),fill=tint(c,-18));self.d.line((xx+31,yy,xx+31,yy+31),fill=tint(c,-18));self.d.line((xx+1,yy+1,xx+30,yy+1),fill=tint(c,12))
     for _ in range(12):
      sx,sy=self.rng.randrange(2,30),self.rng.randrange(2,30);self.d.point((xx+sx,yy+sy),fill=tint(c,self.rng.randint(-12,12)))
 def wall(self,x,y,w,h=1):
  self.block(x,y,w,h);x,y,w,h=x*T,y*T,w*T,h*T;co=self.p['wall'];self.d.rectangle((x+5,y+8,x+w+5,y+h+9),fill=(10,17,19,110));self.d.rectangle((x,y,x+w-1,y+h-1),fill=tint(co,-30));self.d.rectangle((x,y,x+w-1,y+h-9),fill=co)
  for yy in range(y,y+h-8,8):
   self.d.line((x,yy,x+w-1,yy),fill=tint(co,14))
   for xx in range(x+(16 if yy%16 else 0),x+w,32):self.d.line((xx,yy,xx,yy+7),fill=tint(co,-18))
  self.d.line((x,y+h-8,x+w-1,y+h-8),fill=tint(co,30));self.d.line((x,y+h-1,x+w-1,y+h-1),fill=tint(co,-55))
 def rug(self,x,y,w,h,color):
  b=(x*T+3,y*T+3,(x+w)*T-4,(y+h)*T-4);self.d.rectangle(b,fill=color,outline=self.p['accent'],width=2);self.d.rectangle((b[0]+6,b[1]+6,b[2]-6,b[3]-6),outline=tint(color,28))
  for xx in range(b[0]+16,b[2]-8,32):
   for yy in range(b[1]+16,b[3]-8,32):self.d.line((xx-3,yy,xx,yy-3,xx+3,yy,xx,yy+3,xx-3,yy),fill=tint(color,12),width=1)
 def label(self,x,y,s):
  box=self.d.textbbox((0,0),s,font=bold);ww=box[2]+18;self.d.rounded_rectangle((x*T,y*T,x*T+ww,y*T+23),radius=3,fill=self.p['dark'],outline=self.p['accent']);self.d.text((x*T+9,y*T+3),s,font=bold,fill=self.p['accent'])
 def table(self,x,y,w=3,h=1,monitor=False):
  self.block(x,y,w,h);xx,yy=x*T,y*T;ww,hh=w*T,h*T;col=self.p['wood'];self.d.rounded_rectangle((xx+4,yy+7,xx+ww+4,yy+hh+5),radius=6,fill=(10,13,13,100));self.d.rectangle((xx+5,yy+hh-1,xx+10,yy+hh+8),fill=self.p['dark']);self.d.rectangle((xx+ww-10,yy+hh-1,xx+ww-5,yy+hh+8),fill=self.p['dark']);self.d.rounded_rectangle((xx+1,yy+1,xx+ww-2,yy+hh-3),radius=5,fill=col,outline=tint(col,-45),width=2);self.d.line((xx+6,yy+4,xx+ww-7,yy+4),fill=tint(col,40),width=2)
  for dy in range(10,hh-5,6):self.d.line((xx+8,yy+dy,xx+ww-9,yy+dy),fill=tint(col,-9))
  if monitor:
   self.d.rectangle((xx+ww//2-15,yy+5,xx+ww//2+14,yy+19),fill='#111c27',outline='#879ca6');self.d.rectangle((xx+ww//2-12,yy+8,xx+ww//2+11,yy+15),fill=self.p['screen']);self.d.line((xx+ww//2-8,yy+24,xx+ww//2+9,yy+24),fill='#c4c9c5',width=3)
  else:
   self.d.rectangle((xx+ww//2-14,yy+8,xx+ww//2+8,yy+22),fill='#e9dcbc',outline='#9f8c68');self.d.line((xx+ww//2-3,yy+9,xx+ww//2-3,yy+21),fill='#baa789');self.d.ellipse((xx+ww-18,yy+8,xx+ww-11,yy+15),fill=self.p['accent'])
 def seat(self,x,y,name=None):
  xx,yy=x*T+16,y*T+16;co=self.p['seat'];self.d.ellipse((xx-13,yy-4,xx+16,yy+19),fill=(8,16,18,100));self.d.rectangle((xx-10,yy-9,xx+10,yy+9),fill=tint(co,-35),outline=self.p['dark']);self.d.rectangle((xx-8,yy-8,xx+8,yy+5),fill=co);self.d.line((xx-11,yy-5,xx-11,yy+12),fill=self.p['accent'],width=3);self.d.line((xx+11,yy-5,xx+11,yy+12),fill=self.p['accent'],width=3);self.a.rounded_rectangle((xx-11,yy+7,xx+11,yy+14),radius=2,fill=tint(co,-12),outline=self.p['accent']);self.a.line((xx-8,yy+8,xx+8,yy+8),fill=tint(co,35));self.seats.append({'name':name or f'seat-{len(self.seats)+1:02}','cell':[x,y],'anchor':[xx,yy-1],'floorClick':[xx,yy+15],'direction':'north'})
 def plant(self,x,y,large=False):
  self.block(x,y,1,1);xx,yy=x*T+16,y*T+18;rad=34 if large else 15
  self.d.ellipse((xx-rad+6,yy-rad+12,xx+rad+9,yy+rad+12),fill=(11,24,17,100));self.d.ellipse((xx-12,yy-3,xx+12,yy+15),fill='#7c5a37',outline='#bc9a63',width=2)
  dr=self.a if large else self.d
  dr.line((xx,yy+5,xx-1,yy-rad),fill='#68513a',width=7)
  for _ in range(36 if large else 15):
   dx=self.rng.randint(-rad,rad);dy=self.rng.randint(-rad,rad//2);r=self.rng.randint(4,10);dr.ellipse((xx+dx-r,yy+dy-r,xx+dx+r,yy+dy+r),fill=self.rng.choice(['#506b3c','#647b44','#899253','#3e603b']),outline='#3a5535')
 def shelf(self,x,y,w=3):
  self.table(x,y,w);xx,yy=x*T,y*T
  for dx in range(8,w*T-8,9):self.d.rectangle((xx+dx,yy+7,xx+dx+5,yy+23),fill=self.rng.choice(['#526759','#b79d61','#8f5548','#546b7b']),outline='#392f28')
 def screen(self,x,y,w=5,h=2,stars=False):
  self.block(x,y,w,h);xx,yy=x*T,y*T;ww,hh=w*T,h*T;self.d.rectangle((xx+4,yy+7,xx+ww+6,yy+hh+7),fill=self.p['dark']);self.d.rectangle((xx,yy,xx+ww-1,yy+hh-1),fill='#152b35',outline=self.p['accent'],width=3)
  for i in range(25 if stars else 8):
   px=self.rng.randint(xx+10,xx+ww-12);py=self.rng.randint(yy+8,yy+hh-10)
   if stars:self.d.ellipse((px,py,px+2,py+2),fill='#c0d7ce')
   else:self.d.line((px,py,min(xx+ww-7,px+20),py),fill=self.p['screen'],width=2)
  self.d.line((xx+7,yy+hh-8,xx+ww-8,yy+hh-8),fill=self.p['screen'])
 def anchor(self,name,x,y):self.anchors.append({'name':name,'cell':[x,y]})
 def zone(self,name,x,y,w,h,kind='meeting'):self.zones.append(dict(name=name,rect=[x*T,y*T,w*T,h*T],kind=kind))
 def shell(self,kind='stone'):
  self.floor(1,1,42,34,kind);self.wall(1,1,42);self.wall(1,34,19);self.wall(24,34,19);self.wall(1,2,1,32);self.wall(42,2,1,32);self.label(19,32,'ARRIVAL');self.anchor('arrival',22,33)
 def finish(self):
  out=R/self.slug
  for p in ['assets','map32','review','source']: (out/p).mkdir(parents=True,exist_ok=True)
  self.base.save(out/'assets/base.png');self.above.save(out/'assets/above.png');js(out/'source/layout.json',dict(title=self.title,category=self.category,spawn=self.spawn,seats=self.seats,anchors=self.anchors,zones=self.zones,collision=self.g))
  compile_map(self,out)
# Detailed native-scale source kit, reused at its original pixel dimensions.
A={p.stem:Image.open(p).convert('RGBA') for p in (R/'source-assets').glob('*.png')}
oldfloor=Map.floor

def detailed_floor(self,x,y,w,h,kind='stone',color=None):
 self.block(x,y,w,h,0);tile=A['wood' if kind=='wood' else 'plaster' if kind=='plaster' else 'stone'];patch=Image.new('RGBA',(w*T,h*T))
 for yy in range(0,h*T,tile.height):
  for xx in range(0,w*T,tile.width):patch.alpha_composite(tile,(xx,yy))
 self.base.alpha_composite(patch,(x*T,y*T))
 if color:
  overlay=Image.new('RGBA',patch.size,tuple(color)+(75,));self.base.alpha_composite(overlay,(x*T,y*T))
Map.floor=detailed_floor

def detailed_seat(self,x,y,name=None):
 self.block(x,y+1,1,1);xx,yy=x*T+16,y*T+16;self.base.alpha_composite(A['chair-below-safe'],(xx-16,yy-24));self.above.alpha_composite(A['chair-foreground-safe'],(xx-16,yy-24));self.seats.append({'name':name or f'seat-{len(self.seats)+1:02}','cell':[x,y],'anchor':[xx,yy-1],'floorClick':[xx,yy+15],'direction':'north'})
Map.seat=detailed_seat

def detailed_table(self,x,y,w=3,h=1,monitor=False):
 if monitor:
  im=A['light-desk'];self.block(x,y,2,1);self.base.alpha_composite(im,(x*T,y*T-8))
 else:
  im=A['light-meeting_table'];self.block(x,y,4,2);self.base.alpha_composite(im,(x*T,y*T-8))
Map.table=detailed_table

def detailed_plant(self,x,y,large=False):
 self.block(x,y,1,1);im=A['olive' if large else 'plant'];pos=(x*T+16-im.width//2,y*T+28-im.height);self.base.alpha_composite(im,pos)
Map.plant=detailed_plant

P=dict(outer='#27352f',floor=(200,183,146),wall=(204,187,152),wood=(151,111,67),accent='#d6b56b',dark='#233d38',seat=(38,78,73),screen='#aad4aa')
def academy():
 m=Map('olive-arabic-academy','Olive Arabic Academy','Knowledge',P);m.shell('plaster');m.floor(3,3,23,17,'wood');m.rug(5,8,20,11,(62,82,67));m.wall(26,2,1,17);m.wall(2,20,14);m.wall(20,20,7);m.label(5,3,'ARABIC ACADEMY');m.screen(9,5,10,2)
 m.base.alpha_composite(A['podium-below'],(13*T,7*T));m.above.alpha_composite(A['podium-above'],(13*T,7*T));m.block(13,7,3,2);m.anchor('teacher',14,9);m.zone('Teacher presentation',5,7,18,3,'speaker');m.zone('Classroom audience',4,10,21,9,'listener')
 for y in [11,13,15,17]:
  for x in [8,10,12,17,19,21]:m.seat(x,y)
 for y,label in [(3,'STUDY A'),(14,'STUDY B')]:
  m.floor(28,y,13,9,'wood');m.rug(29,y+2,10,6,(85,76,58));m.label(29,y,label);m.smalltable(32,y+4);m.seat(32,y+5);m.seat(33,y+5);m.anchor(label,33,y+7);m.zone(label,28,y+1,13,8);m.plant(39,y+2)
 m.wall(28,12,14);m.wall(28,24,14);m.floor(3,22,23,9,'stone');m.label(5,22,'OLIVE COURT');m.bed(13,26,5,3);m.plant(15,27,True);m.plant(6,27,True);m.plant(23,27,True);m.anchor('olive court',18,29);m.label(29,26,'READING GALLERY');m.shelf(30,29,3);m.shelf(37,29,3);m.anchor('reading gallery',34,29);m.cropboxes=[('classroom',(128,224,832,640)),('study',(896,64,1344,384)),('olive-court',(96,704,832,1024))];return m

def cowork():
 m=Map('timber-design-studio','Timber & Stone Design Studio','Work',dict(P,outer='#252d2d',wall=(145,148,140)));m.shell('stone');m.floor(3,3,18,18,'wood');m.floor(23,3,18,18,'wood');m.label(5,3,'DESIGN / NORTH');m.label(25,3,'DESIGN / SOUTH');m.wall(21,2,2,16)
 for x0 in [5,25]:
  for y in [7,14]:
   for x in [x0,x0+9]:m.table(x,y,monitor=True);m.seat(x,y+2,f'desk-{len(m.seats)+1}');m.anchor(f'desk aisle {x} {y}',x+3,y+2)
 for x in [3,19,24,40]:m.plant(x,5);m.plant(x,19)
 m.wall(2,22,12);m.wall(18,22,10);m.wall(32,22,10);m.floor(3,24,13,7,'wood');m.floor(28,24,13,7,'wood');m.label(4,24,'MEETING A');m.label(29,24,'MEETING B')
 for x in [7,32]:m.table(x,27);m.seat(x,30);m.seat(x+3,30);m.anchor('meeting bay '+str(x),x+5,29);m.zone('Meeting bay '+str(x),x-3,25,12,7)
 m.label(18,25,'MATERIALS');m.shelf(19,27,5);m.anchor('material library',22,30);m.cropboxes=[('desks',(96,128,672,640)),('meeting',(64,768,576,1056))];return m

def observatory():
 p=dict(P,outer='#101f2c',wall=(106,127,139),dark='#172d40',accent='#c6c9a4',screen='#89c8d4');m=Map('quiet-orbit-observatory','Quiet Orbit Observatory','Knowledge',p);m.shell('stone');m.floor(3,3,38,14,'plaster',(39,74,104));m.label(16,3,'QUIET ORBIT');m.screen(15,5,14,4,True);m.rug(14,10,16,6,(39,63,83))
 # Brass meridian in the dome, with a detailed optical instrument and radial observatory floor.
 cx,cy=22*T,12*T
 for rr in [60,85]:m.d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline='#bba970',width=2)
 m.d.line((cx-90,cy,cx+90,cy),fill='#9a926b');m.d.line((cx,cy-90,cx,cy+90),fill='#9a926b');m.d.ellipse((cx-27,cy-18,cx+27,cy+24),fill='#445966',outline='#c8bd8b',width=3);m.d.polygon([(cx-35,cy-28),(cx-20,cy-42),(cx+35,cy+9),(cx+20,cy+24)],fill='#abb5aa',outline='#d7c990');m.block(21,11,2,2);m.anchor('telescope deck',22,15)
 m.wall(2,18,17);m.wall(25,18,17);m.wall(27,19,1,12);m.floor(3,20,23,11,'wood',(33,60,75));m.floor(29,20,12,11,'plaster',(58,66,83));m.label(5,20,'RESEARCH STATIONS');m.label(30,20,'SEMINAR')
 for x,y in [(5,23),(14,23),(5,28),(14,28)]:m.table(x,y,monitor=True);m.seat(x,y+2)
 m.screen(31,23,7,2,True)
 for y in [27,30]:
  for x in [31,34,37]:m.seat(x,y)
 m.anchor('research aisle',23,26);m.anchor('seminar speaker',34,25);m.zone('Seminar speaker',30,25,10,1,'speaker');m.zone('Seminar audience',29,26,12,6,'listener');m.plant(4,5);m.plant(39,5);m.cropboxes=[('research',(96,640,864,1024)),('observatory',(352,128,1088,544))];return m

def command():
 p=dict(P,outer='#141c23',wall=(100,119,121),dark='#142830',accent='#d7b15c',screen='#7be0cd');m=Map('mission-control-center','Mission Control Center','Work',p);m.shell('stone');m.floor(3,3,38,19,'plaster',(32,66,73));m.label(16,3,'MISSION CONTROL');m.screen(7,5,10,3);m.screen(19,5,10,3,True);m.screen(31,5,8,3);m.rug(5,10,34,10,(33,57,64))
 for y,xs in [(11,[7,16,25,34]),(17,[11,20,29])]:
  for x in xs:m.table(x,y,monitor=True);m.seat(x,y+2);m.anchor(f'console {x} {y}',x+3,y+2)
 m.wall(2,23,13);m.wall(20,23,8);m.wall(33,23,9);m.floor(3,25,17,7,'wood',(58,62,65));m.floor(26,25,15,7,'plaster',(75,83,72));m.label(4,25,'MISSION BRIEFING');m.table(9,28);m.seat(8,31);m.seat(13,31);m.screen(5,27,3,2);m.anchor('briefing approach',16,30);m.zone('Briefing bay',3,26,17,7);m.label(28,25,'OPERATIONS LIBRARY');m.shelf(29,28,3);m.shelf(36,28,3);m.anchor('operations library',33,30);m.plant(4,10);m.plant(40,10);m.cropboxes=[('consoles',(160,288,1280,672)),('briefing',(96,800,672,1088))];return m
def compile_map(m,out):
 sets=[];layers=[];gid=1;aud=[]
 for old in (out/'map32').glob('*.png'):old.unlink()
 def layer(name,data,opacity=1):return dict(id=0,name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=data)
 for name,im in [('architecture-and-furniture',m.base),('seat-backs',m.above)]:
  if name=='seat-backs':layers.append(dict(id=0,name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
  cells=[];lookup={};data=[]
  for y in range(N):
   for x in range(C):
    tile=im.crop((x*T,y*T,(x+1)*T,(y+1)*T));b=tile.tobytes()
    if not tile.getbbox():data.append(0);continue
    if b not in lookup:lookup[b]=len(cells);cells.append(tile)
    data.append(gid+lookup[b])
  restored=Image.new('RGBA',(W,H))
  for i,v in enumerate(data):
   if v:restored.paste(cells[v-gid],(i%C*T,i//C*T))
  assert restored.tobytes()==im.tobytes()
  for pi,start in enumerate(range(0,len(cells),1024)):
   cc=cells[start:start+1024];cols=min(32,len(cc));atlas=Image.new('RGBA',(cols*T,math.ceil(len(cc)/cols)*T))
   for j,t in enumerate(cc):atlas.paste(t,(j%cols*T,j//cols*T))
   fn=f'{name}-{pi}.png';atlas.save(out/'map32'/fn);sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(cc)))
  layers.append(layer(name,data));aud.append(dict(layer=name,uniqueTiles=len(cells),atlasRoundtripExact=True));gid+=len(cells)
 transparent=Image.new('RGBA',(32,32));transparent.save(out/'map32/logic.png');sets.append(dict(firstgid=gid,name='collision',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,layer('collision',[gid if v else 0 for row in m.g for v in row],0));gid+=1
 sets.append(dict(firstgid=gid,name='quiet',image='logic.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1));quiet=[0]*(C*N);sx,sy=m.spawn;quiet[sy*C+sx]=gid;ql=layer('spawn-only-silence',quiet,0);ql['properties']=props(silent=True);layers.insert(2,ql)
 area=dict(id=1,name='start',type='area',**{'class':'area'},x=sx*T,y=sy*T,width=T,height=T,rotation=0,visible=True,properties=props(start=True));layers.append(dict(id=0,name='map-areas',type='objectgroup',x=0,y=0,opacity=1,visible=True,objects=[area],draworder='topdown'))
 for i,l in enumerate(layers):l['id']=i+1
 tmj=dict(compressionlevel=-1,width=C,height=N,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tilewidth=T,tileheight=T,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=2,backgroundcolor=m.p['outer'],properties=props(name=m.title,category=m.category,wokaScale=1,status='Review candidate; native32 static checks passed; live test pending'),layers=layers,tilesets=sets);js(out/'map32/map.tmj',tmj)
 # Native companion room semantics are explicit and optional to editor import.
 areas=[]
 for i,z in enumerate(m.zones):
  x,y,w,h=z['rect'];pid=f'{m.slug}-{i}';pr=[]
  if z['kind']=='meeting':pr=[dict(id=pid+'-room',type='livekitRoomProperty',roomName=pid,livekitRoomConfig=dict(startWithAudioMuted=False,startWithVideoMuted=False,disableChat=False))]
  elif z['kind']=='speaker':pr=[dict(id=pid+'-speaker',type='speakerMegaphone',name=pid,chatEnabled=False)]
  elif z['kind']=='listener':pr=[dict(id=pid+'-listener',type='listenerMegaphone',speakerZoneName=f"{m.slug}-{next(j for j,zz in enumerate(m.zones) if zz['kind']=='speaker')}",chatEnabled=False)]
  areas.append(dict(id=pid,name=z['name'],x=x,y=y,width=w-1,height=h-1,visible=True,properties=pr))
 wam=dict(version='2.0.0',mapUrl='./map.tmj',entities={},entityCollections=[],areas=areas);js(out/'map32/map.wam',wam)
 # Reachability, tile-body collision, exact layer split and source-owned seating checks.
 reachable={(sx,sy)};q=collections.deque(reachable)
 while q:
  x,y=q.popleft()
  for nx,ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if 0<=nx<C and 0<=ny<N and not m.g[ny][nx] and (nx,ny) not in reachable:reachable.add((nx,ny));q.append((nx,ny))
 targets=m.anchors+[dict(name=s['name'],cell=s['cell']) for s in m.seats];fail=[a for a in targets if tuple(a['cell']) not in reachable]
 assert not fail,fail
 for ss in m.seats:
  px,py=ss['anchor'];fx,fy=ss['floorClick'];assert [fx//32,fy//32]==ss['cell']
  assert not any(m.g[yy//32][xx//32] for xx in range(px-8,px+8) for yy in range(py,py+16)),ss
 # Render strictly from runtime atlases, not from build images.
 render=[]
 atlases={s['image']:Image.open(out/'map32'/s['image']).convert('RGBA') for s in sets}
 for l in layers:
  if l['type']!='tilelayer' or l['opacity']==0:continue
  im=Image.new('RGBA',(W,H))
  for i,v in enumerate(l['data']):
   if not v:continue
   ts=next(s for s in reversed(sets) if s['firstgid']<=v);a=atlases[ts['image']];n=v-ts['firstgid'];xx=n%ts['columns']*32;yy=n//ts['columns']*32;im.alpha_composite(a.crop((xx,yy,xx+32,yy+32)),(i%C*32,i//C*32))
  render.append(im)
 empty=Image.alpha_composite(render[0],render[1]);empty.save(out/'review/empty-native.png');occupied=render[0].copy();greg=A.get('greg-reference',Image.new('RGBA',(96,128)));actor=greg.crop((32,96,64,128));occlusion=0
 for s in m.seats:
  x,y=s['anchor'];occupied.alpha_composite(actor,(x-16,y-16));over=m.above.crop((x-16,y-16,x+16,y+16));occlusion+=int(bool(over.getbbox()))
 for a in m.anchors:
  x,y=a['cell'];af=greg.crop((32,0,64,32)) if a['name']=='teacher' or a['name']=='instructor position' else actor;occupied.alpha_composite(af,(x*T,y*T))
 occupied.alpha_composite(render[1]);occupied.save(out/'review/occupied-native.png')
 for name,box in m.cropboxes:occupied.crop(box).save(out/'review'/f'{name}-occupied-native.png')
 card=Image.new('RGB',(W,H+90),m.p['outer']);card.paste(occupied,(0,70));d=ImageDraw.Draw(card);d.text((28,12),m.title,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',25),fill=m.p['accent']);d.text((28,46),f'{m.category} | Native32 compiled map | Occupied static proof; live playtest pending',font=font,fill='white');card.save(out/'review/overview.png')
 audit=dict(nativeTileSize=32,dimensions=[C,N],seats=len(m.seats),deskCount=8 if m.slug=='timber-design-studio' else None,reachableTargetCount=len(targets),reachableCells=len(reachable),unreachableTargets=fail,quietCells=1,silenceRestrictedToSpawn=True,seatForegroundMatches=occlusion,seatCount=len(m.seats),nativeBodyAtSeatAnchorsClear=True,floorClickRemainsInSeatTile=True,floorLayerBetweenBaseAndForeground=True,atlasRoundtrips=aud,livePlaytest='not run',mediaConnections='not connected',botAIIntegrations='not implemented',routeMethod='Four-neighbor cell BFS; native body is x-8..x+8 and y..y+16, checked separately at authored anchors. No sub-tile collision cutouts. All seats and named room anchors tested.');js(out/'VALIDATION.json',audit)
 (out/'GUIDE.md').write_text(f'''# {m.title}\n\nCategory: {m.category}. Native32 candidate: {C}×{N} tiles, {len(m.seats)} usable visual seats.\n\n## Files and setup\n- Host the complete map32 directory together; use map.wam for an editor-managed room, or map.tmj for base map rendering. Do not move atlases individually.\n- Spawn, collision and single-cell spawn silence are built into TMJ. Seating is walk-to visual seating; no invented sitting animation or custom engine changes.\n- Companion WAM defines bounded {'presentation and meeting' if m.zones else 'room'} areas using current native properties. Review/import in the Universe editor; conferencing and broadcasts require deployment permissions/services and are not live-tested.\n- Screens are artwork only. Add your own document links, lesson materials or media destinations in the editor. No AI teacher, research integration or command data feed is implemented.\n\n## Checks\nAll {len(targets)} seat/room anchors reached from spawn through collision-free tile cells. Base and foreground atlases round-trip exactly; floorLayer separates avatars from chair backrails. Occupied proofs insert a reference avatar at native scale. These are static compiled-map renders, not live room screenshots.\n\n## Rebuild\nRun python tools/build_environments.py from the parent source bundle (Python 3 + Pillow). The source-assets folder contains frozen reused native artwork. Source paths and provenance are listed in ASSET-PROVENANCE.md. No paid generation or new dependencies/services were used.\n''')
 manifest=dict(slug=m.slug,title=m.title,category=m.category,validation='VALIDATION.json',overview='review/overview.png',runtime='map32/map.tmj',companion='map32/map.wam',nativeCrop=[f'review/{n}-occupied-native.png' for n,b in m.cropboxes],status='Local candidate, not published',files=[dict(path=str(p.relative_to(out)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file()]);js(out/'MANIFEST.json',manifest);print(m.slug,len(m.seats),'seats',len(targets),'reachable targets')
def textured_wall(self,x,y,w,h=1):
 self.block(x,y,w,h);xx,yy=x*T,y*T;ww,hh=w*T,h*T;tile=A['stone'];patch=Image.new('RGBA',(ww,hh))
 for dy in range(0,hh,192):
  for dx in range(0,ww,192):patch.alpha_composite(tile,(dx,dy))
 self.base.alpha_composite(patch,(xx,yy));co=self.p['wall'];self.d.rectangle((xx,yy+hh-10,xx+ww-1,yy+hh-1),fill=tint(co,-40));self.d.line((xx,yy,xx+ww-1,yy),fill=tint(co,35),width=2);self.d.line((xx,yy+hh-11,xx+ww-1,yy+hh-11),fill=tint(co,18),width=2)
 for dx in range(0,ww,32):self.d.line((xx+dx,yy+hh-9,xx+dx,yy+hh-2),fill=tint(co,-60))
 self.d.rectangle((xx+5,yy+hh,xx+ww+4,yy+hh+4),fill=tint(co,-70))
Map.wall=textured_wall

def detailed_screen(self,x,y,w=5,h=2,stars=False):
 self.block(x,y,w,h);xx,yy=x*T,y*T;ww,hh=w*T,h*T;co=self.p['screen'];self.d.rectangle((xx+4,yy+5,xx+ww+4,yy+hh+5),fill=self.p['dark']);self.d.rectangle((xx,yy,xx+ww-1,yy+hh-1),fill='#142d32',outline=self.p['accent'],width=3);self.d.rectangle((xx+5,yy+5,xx+ww-6,yy+hh-6),outline='#546f68')
 if 'academy' in self.slug:
  ar=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);self.d.text((xx+ww//2,yy+9),'أهلاً وسهلاً',font=ar,fill='#e4e1c5',anchor='mt',direction='rtl');self.d.text((xx+ww//2,yy+hh-18),'AHLAN WA SAHLAN',font=font,fill=co,anchor='mt')
 elif stars:
  center=(xx+ww//2,yy+hh//2)
  for rr in [hh//5,hh//3]:self.d.ellipse((center[0]-rr*2,center[1]-rr,center[0]+rr*2,center[1]+rr),outline='#365460')
  pts=[(xx+self.rng.randrange(12,ww-12),yy+self.rng.randrange(12,hh-12)) for _ in range(18)]
  self.d.line(pts[:6],fill='#546f80',width=1)
  for px,py in pts:self.d.ellipse((px-1,py-1,px+1,py+1),fill='#c5d7c8')
 else:
  self.d.text((xx+12,yy+10),'SYSTEM OVERVIEW' if w>4 else 'BRIEF',font=font,fill=co)
  for i in range(3):
   by=yy+34+i*13
   if by<yy+hh-8:self.d.line((xx+12,by,xx+ww-14,by),fill='#365963');self.d.line((xx+12,by,xx+12+int((ww-28)*(.4+i*.18)),by),fill=co,width=3)
Map.screen=detailed_screen

def reading_table(self,x,y,w=3):self.table(x,y)
Map.shelf=reading_table

def bed(self,x,y,w,h):
 self.d.rounded_rectangle((x*T,y*T,(x+w)*T,(y+h)*T),radius=18,fill='#9d916e',outline='#dfcda4',width=5);self.d.rounded_rectangle((x*T+7,y*T+7,(x+w)*T-7,(y+h)*T-7),radius=14,fill='#686b45',outline='#494d31',width=3)
 for _ in range(w*h*18):
  px=self.rng.randint(x*T+12,(x+w)*T-12);py=self.rng.randint(y*T+12,(y+h)*T-12);self.d.ellipse((px,py,px+2,py+2),fill=self.rng.choice(['#7d8453','#90925e','#595d3b']))
 self.block(x,y,w,h)
Map.bed=bed

oldacademy=academy
def academy():
 m=oldacademy();kit=A['academy-architectural-kit']
 # Authored architecture is fitted to bounded wall bands, not treated as a complete map image.
 window=kit.crop((77,0,1149,219)).resize((352,72),Image.Resampling.LANCZOS)
 board=kit.crop((22,866,1197,1106)).resize((384,79),Image.Resampling.LANCZOS)
 pier=kit.crop((164,664,252,865)).resize((28,64),Image.Resampling.LANCZOS)
 partition=kit.crop((127,1114,1108,1284)).resize((320,55),Image.Resampling.LANCZOS)
 for x in [64,416,768,1024]:m.base.alpha_composite(window,(x,32))
 m.block(2,1,40,2);m.base.alpha_composite(board,(256,144));m.block(8,4,12,3)
 for x,y in [(64,576),(800,576),(1248,336),(864,720),(64,928),(800,928)]:m.base.alpha_composite(pier,(x,y));m.block(x//32,y//32,1,2)
 # Courtyard perimeter has raised soil/plant beds; no carpet beneath trees.
 m.bed(4,26,5,3);m.plant(6,27,True);m.bed(21,26,4,3);m.plant(23,27,True)
 for x,y in [(96,640),(640,640),(896,768)]:
  m.base.alpha_composite(partition,(x,y));m.block(x//32,y//32,10,2)
 return m

def smalltable(self,x,y):
 self.base.alpha_composite(A['low-lounge-table'],(x*T,y*T));self.block(x,y,2,1)
Map.smalltable=smalltable

def rich_rug(self,x,y,w,h,color):
 src=A['rug-wide'];ww,hh=w*T-8,h*T-8;b=24;patch=Image.new('RGBA',(ww,hh));tile=src.crop((56,56,120,120))
 for dy in range(b,hh-b,64):
  for dx in range(b,ww-b,64):patch.alpha_composite(tile,(dx,dy))
 for dx in range(b,ww-b,64):
  for sy,dy in [(0,0),(src.height-b,hh-b)]:patch.alpha_composite(src.crop((56,sy,120,sy+b)),(dx,dy))
 for dy in range(b,hh-b,64):
  for sx,dx in [(0,0),(src.width-b,ww-b)]:patch.alpha_composite(src.crop((sx,56,sx+b,120)),(dx,dy))
 for sx,dx in [(0,0),(src.width-b,ww-b)]:
  for sy,dy in [(0,0),(src.height-b,hh-b)]:patch.alpha_composite(src.crop((sx,sy,sx+b,sy+b)),(dx,dy))
 self.base.alpha_composite(patch,(x*T+4,y*T+4))
Map.rug=rich_rug

if __name__=='__main__':
 import sys
 makers=[academy,cowork,observatory,command]
 for fn in makers:
  if len(sys.argv)==1 or sys.argv[1]==fn.__name__:fn().finish()
