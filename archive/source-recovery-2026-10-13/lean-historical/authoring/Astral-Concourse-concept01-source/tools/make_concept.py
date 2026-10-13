from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1]
base=Image.open(R/'assets/hall-architecture.png').convert('RGBA'); below=Image.open(R/'assets/chair-below.png').convert('RGBA');above=Image.open(R/'assets/chair-above.png').convert('RGBA');fg=Image.new('RGBA',base.size);greg=Image.open(R/'assets/greg-reference.png'); north=greg.crop((32,96,64,128));south=greg.crop((32,0,64,32))
# Three straight native-size banks; architectural registration refinement is pending review.
seats=[]
for bank,bx in enumerate((192,608,1024)):
 for row in range(7):
  for col in range(10):
   x=bx+16+col*32;y=432+row*64
   base.alpha_composite(below,(x-16,y-16));fg.alpha_composite(above,(x-16,y-16));seats.append({'id':f'{chr(65+bank)}{row+1:02}-{col+1:02}','x':x,'y':y,'bank':bank,'row':row,'column':col})
base.alpha_composite(Image.open(R/'assets/podium-below.png'),(728,252));fg.alpha_composite(Image.open(R/'assets/podium-above.png'),(728,252))
empty=base.copy();empty.alpha_composite(fg);empty.save(R/'review/flagship-empty-native.png')
occupied=base.copy()
for i,s in enumerate(seats):
 if (i*7)%17<10:occupied.alpha_composite(north,(s['x']-16,s['y']-16))
for x,y,sp in [(768,266,south),(576,772,north),(960,644,south),(768,1088,north),(736,1072,south),(1216,1056,south)]:occupied.alpha_composite(sp,(x-16,y-16))
occupied.alpha_composite(fg);occupied.save(R/'review/flagship-occupied-native.png')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda s:ImageFont.truetype(font,s);b=lambda s:ImageFont.truetype(fb,s)
thumb=occupied.resize((960,800),Image.Resampling.LANCZOS);card=Image.new('RGB',(1280,936),'#112f36');card.paste(thumb,(320,84));d=ImageDraw.Draw(card);d.text((32,24),'A connected event venue',font=b(30),fill='#f6d598');d.text((32,72),'FLAGSHIP HALL',font=b(18),fill='#d6ae66')
for y,head,txt in [(136,'210 visible seats','3 banks × 10 seats × 7 rows'),(234,'32 px world grid','Unchanged 32 px Woka sprites'),(332,'Distinct stage','Two side approaches + lectern'),(430,'Quiet arrival','Vestibule before audience entry'),(528,'Broadcast candidate','WAM + live validation required'),(626,'Expandable venue','Linked maps through a shared hub')]:
 d.text((32,y),head,font=b(18),fill='white');d.multiline_text((32,y+30),txt,font=f(14),fill='#b1c6c9',spacing=6)
d.text((32,891),'CONCEPT 01  |  Static source composition  |  No live runtime or concurrent-capacity claim',font=f(16),fill='#cfdbdc');card.save(R/'review/flagship-overview.png')
proof=Image.new('RGB',(1280,806),'#112f36');d=ImageDraw.Draw(proof);d.text((24,18),'Native scale · Woka32 at 1:1',font=b(24),fill='#f6d598');proof.paste(occupied.crop((448,192,1088,512)),(0,62));proof.paste(occupied.crop((160,576,800,896)),(640,62));proof.paste(occupied.crop((448,896,1088,1248)),(0,404));proof.paste(empty.crop((640,512,1280,864)),(640,404));d.text((16,768),'Stage + front rows · bank/aisle composition · arrival vestibule · empty chair geometry',font=f(16),fill='#d5e1df');proof.save(R/'review/native-scale-composition.png')
# Readable masterplan is a diagram, not a promised live map or published site.
im=Image.new('RGB',(1440,1000),'#102a31');d=ImageDraw.Draw(im);d.text((48,36),'One venue. Different rooms. Parallel sessions.',font=b(34),fill='#f5d697');d.text((48,86),'Conference and esports share the arrival network; each hall has its own identity and broadcast.',font=f(20),fill='#c1d6d7')
boxes=[((70,180,620,420),'01 / Flagship Hall','210-seat plenary','Grand stage focus, three dense banks','Prototype first',True),((820,180,1370,420),'02 / Forum Hall','Parallel talks + panels','Compact horseshoe seating, closer conversation','Planned',False),((445,510,995,735),'Shared Arrival Lobby','Schedule + wayfinding','Visible hall portals, social pockets, expo frontage','Connected-map hub',False),((70,800,620,960),'03 / Arena Wing','Finals stage + spectators','Central play floor, opposing team stations','Planned',False),((820,800,1370,960),'04 / Studios + Expo','Workshops or parallel matches','Small distinct rooms, sponsor / demo loop','Planned',False)]
for a,bx in [((344,420),(608,510)),((1090,420),(830,510)),((608,735),(344,800)),((830,735),(1090,800))]:d.line((a,bx),fill='#719da0',width=5)
for rect,title,sub,detail,state,active in boxes:
 d.rounded_rectangle(rect,radius=18,fill='#1d434b' if not active else '#254f54',outline='#d6ad68' if active else '#537b81',width=3);x,y,xx,yy=rect;d.text((x+24,y+22),title,font=b(25),fill='#f4d8a7');d.text((x+24,y+65),sub,font=b(20),fill='white');d.text((x+24,y+102),detail,font=f(17),fill='#bfd6d5');
 if yy-y>200:d.text((x+24,yy-46),state,font=b(16),fill='#73c5c5')
im.save(R/'review/event-venue-masterplan.png')
(R/'source/seats.json').write_text(json.dumps(seats,indent=2)+'\n')
