from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];m=json.loads((R/'map32/grand-auditorium.tmj').read_text());W,H=m['width']*32,m['height']*32;sets=[]
for ts in m['tilesets']:sets.append((ts,Image.open(R/'map32'/ts['image']).convert('RGBA')))
def render(name):
 l=next(x for x in m['layers']if x['name']==name);im=Image.new('RGBA',(W,H))
 for i,gid in enumerate(l['data']):
  if not gid:continue
  ts,atlas=next((t,a)for t,a in reversed(sets)if t['firstgid']<=gid);v=gid-ts['firstgid'];x=v%ts['columns']*32;y=v//ts['columns']*32;im.alpha_composite(atlas.crop((x,y,x+32,y+32)),(i%m['width']*32,i//m['width']*32))
 return im
base=render('hall-base');fg=render('hall-above');greg=Image.open(R/'assets/greg-reference.png');north=greg.crop((32,96,64,128));south=greg.crop((32,0,64,32));seats=json.loads((R/'source/seats.json').read_text());empty=base.copy();empty.alpha_composite(fg);empty.save(R/'review/flagship-empty-native.png');occupied=base.copy()
for i,s in enumerate(seats):
 if (i*7)%17<10:occupied.alpha_composite(north,(s['x']-16,s['y']-16))
for x,y,sp in [(768,264,south),(560,772,north),(976,644,south),(768,1088,north),(736,1072,south),(1216,1056,south)]:occupied.alpha_composite(sp,(x-16,y-16))
occupied.alpha_composite(fg);occupied.save(R/'review/flagship-occupied-native.png')
f=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s);b=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
thumb=occupied.resize((960,800),Image.Resampling.LANCZOS);card=Image.new('RGB',(1280,936),'#112f36');card.paste(thumb,(320,84));d=ImageDraw.Draw(card);d.text((32,24),'A connected event venue',font=b(30),fill='#f6d598');d.text((32,72),'FLAGSHIP HALL',font=b(18),fill='#d6ae66')
for y,head,txt in [(136,'210 visible seats','3 banks × 10 seats × 7 rows'),(234,'32 px world grid','Unchanged 32 px Woka sprites'),(332,'Distinct stage','Two side approaches + lectern'),(430,'Quiet arrival','Vestibule before audience entry'),(528,'Broadcast candidate','Native WAM; live join unverified'),(626,'Expandable venue','Shared hub + distinct hall plans')]:d.text((32,y),head,font=b(18),fill='white');d.text((32,y+30),txt,font=f(14),fill='#b1c6c9')
d.text((32,891),'PROTOTYPE 01  |  Rendered from compiled TMJ  |  No concurrent-capacity or live-media claim',font=f(16),fill='#cfdbdc');card.save(R/'review/flagship-overview.png')
proof=Image.new('RGB',(1280,806),'#112f36');d=ImageDraw.Draw(proof);d.text((24,18),'Native scale · Woka32 at 1:1',font=b(24),fill='#f6d598');proof.paste(occupied.crop((448,192,1088,512)),(0,62));proof.paste(occupied.crop((160,576,800,896)),(640,62));proof.paste(occupied.crop((448,896,1088,1248)),(0,404));proof.paste(empty.crop((640,512,1280,864)),(640,404));d.text((16,768),'Compiled source: stage, reachable seats, continuous aisles, quiet vestibule. Live rendering remains unverified.',font=f(15),fill='#d5e1df');proof.save(R/'review/native-scale-composition.png')
# Close1:1 samples show the actor both in a chair and moving beside its back.
proof=Image.new('RGBA',(1024,620),'#112f36');d=ImageDraw.Draw(proof);d.text((16,16),'Static furniture depth · live local/remote views unverified',font=b(21),fill='#f6d598');cases=[('Native target, north',(592,544,1104,800),[(752,623,10)]),('Beside chairback, south',(592,544,1104,800),[(600,656,1)]),('Front row route, east',(160,384,672,640),[(352,416,7)]),('Lectern approach',(512,160,1024,416),[(680,272,7),(768,264,1)])]
for i,(name,box,people)in enumerate(cases):
 im=base.crop(box)
 for x,y,fr in people:im.alpha_composite(greg.crop((fr%3*32,fr//3*32,fr%3*32+32,fr//3*32+32)),(x-box[0]-16,y-box[1]-16))
 im.alpha_composite(fg.crop(box));px=i%2*512;py=i//2*288+46;proof.alpha_composite(im,(px,py));d.text((px+12,py+264),name,font=f(14),fill='white')
proof.save(R/'review/furniture-depth-native.png')
