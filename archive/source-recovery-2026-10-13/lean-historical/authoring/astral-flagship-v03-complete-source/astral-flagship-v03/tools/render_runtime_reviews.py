from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];Q=R/'review';a=json.loads((R/'source/runtime-layout.json').read_text());base=Image.open(R/'assets/runtime-base.png').convert('RGBA');fg=Image.open(R/'assets/runtime-above.png').convert('RGBA');greg=Image.open(R/'assets/greg-reference.png').convert('RGBA');frames={}
for n,i in [('north',10),('south',1),('east',7),('west',4)]:frames[n]=greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))
occ=base.copy();seats=json.loads((R/'source/seats.json').read_text())
for i,s in enumerate(seats):
 if(i*7)%17<10:occ.alpha_composite(frames['north'],(s['x']-16,s['y']-16))
actors=a['socialAnchors']+[q for q in a['reviewActors']if not q.get('group')and not q.get('pair')]+[{'id':'spawn','x':768,'y':1824,'direction':'north'}]
for q in actors:occ.alpha_composite(frames[q['direction']],(q['x']-16,q['y']-16))
occ.alpha_composite(fg);occ.save(Q/'runtime-occupied-native.png');occ.crop((32,944,1536,1792)).save(Q/'runtime-indoor-foyer-occupied-native.png');occ.crop((1408,992,2560,1792)).save(Q/'runtime-terrace-occupied-native.png');occ.crop((0,928,2560,1856)).save(Q/'runtime-foyer-terrace-occupied-native.png')
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';f=lambda z:ImageFont.truetype(F,z);b=lambda z:ImageFont.truetype(B,z)
card=Image.new('RGB',(1920,1720),'#102e34');d=ImageDraw.Draw(card);d.text((48,26),'FLAGSHIP 03',font=b(18),fill='#caa263');d.text((48,60),'A grand foyer. A garden-side coffee terrace.',font=b(34),fill='#f5e5c3');d.text((48,112),'Four lounge meeting squares  ·  Smaller casual pairs  ·  Quiet arrival and clear hall approaches',font=f(18),fill='#c4d1ce');card.paste(occ.resize((1792,1344),Image.Resampling.LANCZOS),(64,162))
notes=[('01  HALL PRESERVED','Original giant stage and all 210 chairs'),('02  ROOM TO GATHER','Four distinct lounge rugs with 16 resting places'),('03  RIGHT-SIDE TERRACE','Continuous threshold and a protected garden overlook'),('04  COFFEE OFF THE ROUTE','Solid counter, customer apron and four casual pairs')]
for i,(h,t)in enumerate(notes):x=64+(i%2)*900;y=1540+(i//2)*64;d.text((x,y),h,font=b(16),fill='#e0bd79');d.text((x,y+25),t,font=f(15),fill='#dae3db')
d.text((64,1672),'LOCAL COMPILED CANDIDATE  ·  Native 32px grid and Greg fixture  ·  Meeting/broadcast activation and live media tests pending',font=f(13),fill='#9fb6b6');card.save(Q/'runtime-overview.png')
# A true1:1 cropped depth comparison, no sprite enlargement.
empty=Image.alpha_composite(base,fg);sheet=Image.new('RGB',(1248,728),'#102e34');sd=ImageDraw.Draw(sheet)
for i,(name,box)in enumerate([('Lounge north / south / side chairs',(176,1080,368,1280)),('Four-way occupied square',(624,1064,880,1304)),('Casual56px pair',(1184,1504,1344,1664)),('Coffee customer approach',(1784,1080,2056,1312))]):
 x=(i%2)*624;y=(i//2)*364;sd.text((x+12,y+10),name,font=b(14),fill='#e0bd79');w=box[2]-box[0];sheet.paste(empty.crop(box),(x+12,y+42));sheet.paste(occ.crop(box),(x+324,y+42));sd.text((x+12,y+320),'EMPTY / exact native scale',font=f(12),fill='#dae3db');sd.text((x+324,y+320),'OCCUPIED / Greg32',font=f(12),fill='#dae3db')
sheet.save(Q/'runtime-furniture-depth-native.png')
