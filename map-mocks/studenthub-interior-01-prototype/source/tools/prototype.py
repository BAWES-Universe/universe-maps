from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import random,math,json
R=Path(__file__).resolve().parents[1];random.seed(51)
W,H=1024,800
floor=Image.new('RGBA',(W,H),(13,27,37,255));base=Image.new('RGBA',(W,H));front=Image.new('RGBA',(W,H));collisions=[];placements=[]
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
def rect(x,y,w,h,color,layer=floor,outline=None):ImageDraw.Draw(layer).rectangle((x,y,x+w-1,y+h-1),fill=color,outline=outline)
def block(x,y,w,h):collisions.append([x,y,w,h])
def stone(x,y,w,h):
 d=ImageDraw.Draw(floor)
 for yy in range(y,y+h,32):
  for xx in range(x,x+w,32):
   v=random.randint(-5,5);d.rectangle((xx,yy,xx+31,yy+31),fill=(176+v,167+v,141+v));d.line((xx,yy,xx+31,yy),fill=(212,201,169));d.line((xx,yy+31,xx+31,yy+31),fill=(120,120,107));d.line((xx+31,yy,xx+31,yy+31),fill=(143,144,127))
def wood(x,y,w,h):
 d=ImageDraw.Draw(floor)
 for yy in range(y,y+h,16):
  for xx in range(x-64+(yy//16%2)*64,x+w,128):
   v=random.randint(-8,8);d.rectangle((max(x,xx),yy,min(xx+127,x+w-1),yy+15),fill=(104+v,77+v,55+v),outline=(66,52,42))
   for j in range(3):
    sx=max(x,xx)+random.randint(1,35);ex=min(xx+123,x+w-2);gy=yy+random.randint(3,13)
    if sx<ex:d.line((sx,gy,ex,gy),fill=(112+v,85+v,63+v))
def wall(x,y,w,h=32):
 rect(x,y,w,h,(57,82,75));rect(x,y,w,7,(223,208,167));rect(x,y+h-7,w,7,(46,49,40));rect(x,y+h-8,w,1,(174,141,84));block(x,y,w,h)
def text(t,x,y,size=f):
 d=ImageDraw.Draw(floor);bb=d.textbbox((0,0),t,font=size);ww=bb[2];d.rounded_rectangle((x-5,y-3,x+ww+5,y+17),3,fill=(20,42,43,255),outline=(143,128,85));d.text((x,y),t,font=size,fill=(240,221,169))
def asset(name,x,y,solid=True,cut=24,scale=1):
 im=Image.open(R/'assets'/f'{name}.png').convert('RGBA')
 if scale!=1:im.resize((int(im.width*scale),int(im.height*scale)))
 w,h=im.size;low=max(0,h-cut)
 base.alpha_composite(im.crop((0,low,w,h)),(x,y+low));front.alpha_composite(im.crop((0,0,w,low)),(x,y))
 if solid:block(x,y+max(h-24,0),w,min(24,h))
 placements.append({'name':name,'x':x,'y':y,'width':w,'height':h})
def carpet(x,y):floor.alpha_composite(Image.open(R/'assets/rug.png'),(x,y))
stone(32,0,960,800);wood(80,64,864,672)
# Shared office with three full-sized meeting rooms and open public reception.
wall(64,32,896,48);wall(64,64,16,672);wall(944,64,16,672)
wall(64,720,352,16);wall(544,720,416,16)
for x in [352,640]:wall(x,80,16,272)
for x in [80,368,656]:
 wall(x,352,64,20);wall(x+192,352,96,20)
for idx,x in enumerate([80,368,656]):
 asset('window',x+96,42,False)
 asset('meeting_table',x+80,184)
 for dx in [92,160]:
  asset('chair_s',x+dx,134)
  asset('chair_n',x+dx,286)
 asset('plant',x+12,93)
 text(['CEDAR · 4 people','OLIVE · 4 people','WILLOW · 4 people'][idx],x+76,329,small)
# Teamwork desks have wall-back screen surfaces, open approaches.
for x in [128,256,672,800]:
 asset('desk',x,424);asset('chair_n',x+18,491)
asset('bookshelf',80,390)
# Cozy public carpet/couches are at same native furniture scale.
carpet(375,400);asset('couch_s',438,388);asset('couch_e',368,455);asset('couch_w',608,455);asset('coffee',463,478)
asset('reception',424,593);asset('chair_s',478,549)
asset('plant',100,653);asset('plant',866,653)
asset('streetlamp',322,610);asset('streetlamp',634,610)
text('STUDENTHUB · RECEPTION',407,759)
text('TEAM WORKSPACE',125,561);text('TEAM WORKSPACE',671,561)
# Composite with original unchanged32px Woka; native baseline depth convention.
greg=Image.open(R/'qa/greg.png').crop((32,0,64,32));preview=floor.copy();preview.alpha_composite(base);preview.alpha_composite(greg,(496,672));preview.alpha_composite(front)
preview.save(R/'evidence/HQ-prototype-native.png');preview.resize((2048,1600),Image.Resampling.NEAREST).save(R/'evidence/HQ-prototype-2x.png')
floor.save(R/'evidence/proof-floor.png');base.save(R/'evidence/proof-bases.png');front.save(R/'evidence/proof-front.png')
grid=preview.copy();d=ImageDraw.Draw(grid)
for x,y,w,h in collisions:d.rectangle((x,y,x+w-1,y+h-1),fill=(238,79,104,80),outline=(255,77,112))
grid.save(R/'evidence/HQ-prototype-collision.png')
json.dump({'width':W,'height':H,'collisions':collisions,'placements':placements},open(R/'evidence/prototype-layout.json','w'),indent=2)
