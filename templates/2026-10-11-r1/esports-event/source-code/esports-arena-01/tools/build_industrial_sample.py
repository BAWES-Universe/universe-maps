from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];A=R/'assets';Q=R/'review';load=lambda n:Image.open(A/f'{n}.png').convert('RGBA');font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n);bold=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n)
W,H=960,544;b=Image.new('RGBA',(W,H));floor=load('industrial-floor-native')
for y in range(0,H,256):
 for x in range(0,W,256):b.alpha_composite(floor,(x,y))
a=Image.new('RGBA',(W,H));d=ImageDraw.Draw(b)
# Thin integrated team edge accents on real concrete material, no ornamental rug.
for x0,x1,col in [(48,400,'#42c9c1'),(560,912,'#bb805a')]:
 d.rounded_rectangle((x0,72,x1,295),radius=8,outline=col,width=3);d.line((x0+12,292,x1-12,292),fill=col,width=2)
for x in [0,256,512,704]:b.alpha_composite(load('industrial-wall-native'),(x,8))
d.rounded_rectangle((139,60,309,82),radius=3,fill='#152326',outline='#42c9c1');d.text((163,63),'TEAM WEST',font=bold(12),fill='#99e5dc')
d.rounded_rectangle((659,60,813,82),radius=3,fill='#282320',outline='#b98059');d.text((682,63),'CASTER DESK',font=bold(12),fill='#e6b88e')
# Players immediately meet the front lip with 1-3 pixels of head-space, not across a gap.
b.alpha_composite(load('industrial-desk-native'),(144,136));b.alpha_composite(load('industrial-caster-native'),(640,144));chair=load('industrial-chair-native');actors=[]
def seat(x,y,person=True):
 # Physical seat anchor top207 (body ends223); south chairback tile starts224.
 top=y-8;b.alpha_composite(chair,(x-16,top));a.alpha_composite(chair.crop((8,20,24,30)),(x-8,top+20));
 if person:actors.append((x,y,'north'))
for x in [176,240,304]:seat(x,207)
for x in [688,784]:seat(x,207)
for y in [383,479]:
 for x in [624,688,784,848]:seat(x,y,person=x!=848 or y==479)
d=ImageDraw.Draw(b);d.text((658,324),'SPECTATOR COURT',font=bold(12),fill='#b8c6c9')
# Central circulation strip marked only at its edges; unobstructed 96px usable route.
d.line((432,72,432,511),fill='#5b6669',width=1);d.line((528,72,528,511),fill='#5b6669',width=1)
# Small ambient floor light accents, not visual debris.
for x in [448,496]:
 for y in [112,240,368,496]:d.rounded_rectangle((x,y,x+15,y+2),radius=1,fill='#647b80')
actors.extend([(480,288,'south'),(240,336,'north')]);greg=load('greg-reference');frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('west',4),('east',7)]}
occ=b.copy()
for x,y,n in actors:occ.alpha_composite(frames[n],(x-16,y-16))
occ.alpha_composite(a);b.save(Q/'industrial-sample-base-native.png');a.save(Q/'industrial-sample-above-native.png');occ.save(Q/'industrial-occupied-native32.png')
board=Image.new('RGB',(992,650),'#111b20');dd=ImageDraw.Draw(board);dd.text((16,12),'ESPORTS / INDUSTRIAL ARENA / NATIVE32 ART GATE',font=bold(18),fill='#dce4e4');dd.text((16,41),'Original concrete, steel walls, task chairs, competition desk and two-person caster station.',font=font(13),fill='#96b2b8');board.paste(occ,(16,72));dd.text((16,628),'1:1 native source pixels. 32px Greg v3 QA fixture. Single level. Media setup and live play remain unverified.',font=font(12),fill='#96b2b8');board.save(Q/'REVIEW-REVISION-industrial-native32.png')
# Clear diagram: 1/3 scale annotated plan only, not runtime art.
p=Image.new('RGB',(880,706),'#111b20');dd=ImageDraw.Draw(p);dd.text((22,14),'ESPORTS ARENA / 64 × 52 NATIVE32 TILES',font=bold(18),fill='#e4e8e7');dd.text((22,41),'Composition diagram only. Runtime plan is 2048 × 1664 pixels.',font=font(12),fill='#9badb2');sx=.35;ox=82;oy=76
rects=[('WEST TEAM\nVideo call room',(96,128,480,576),'#2c5d61','#50c6bd'),('EAST TEAM\nVideo call room',(1472,128,480,576),'#604535','#ce9866'),('CASTER / PODIUM',(736,128,576,256),'#424a50','#a8bdc5'),('COMPETITION COURT',(704,448,640,128),'#303b42','#738f9a'),('SPECTATORS\nAudience area',(672,640,704,480),'#39464d','#a8bdc5'),('CHECK-IN',(192,1216,352,192),'#293b42','#708b95'),('SOCIAL + COFFEE',(1344,1216,544,288),'#293b42','#708b95'),('ARRIVAL',(944,1504,128,96),'#294249','#70b2b0')]
for label,(x,y,w,h),fill,out in rects:
 xx,yy=ox+int(x*sx),oy+int(y*sx);xx1,yy1=ox+int((x+w)*sx),oy+int((y+h)*sx);dd.rounded_rectangle((xx,yy,xx1,yy1),radius=6,fill=fill,outline=out,width=2);box=dd.multiline_textbbox((0,0),label,font=bold(11),align='center');dd.multiline_text((int((xx+xx1-box[2])/2),int((yy+yy1-box[3])/2)),label,font=bold(11),fill='#e0e4df',align='center')
# Perimeter ring and central south approach.
pts=[(608,384),(608,1152),(1440,1152),(1440,384)];pts=[(ox+int(x*sx),oy+int(y*sx))for x,y in pts];dd.line(pts,fill='#58a4aa',width=3);dd.line((ox+int(1008*sx),oy+int(1504*sx),ox+int(1008*sx),oy+int(1152*sx)),fill='#58a4aa',width=3)
dd.text((22,675),'96px clear loop / 96px team doors / quiet only at small arrival / no room overlap',font=font(13),fill='#a4bac0');p.save(Q/'LAYOUT-DIAGRAM.png')
(R/'source/COMPOSITION-PROPOSAL.md').write_text('''# Esports arena: revised industrial proposal\n\n64 × 52 native32 tiles, 2048 × 1664 pixels. Contemporary graphite concrete/rubber venue with steel shell, restrained teal West Team and copper East Team accents, and purposeful light strips. No gold-star rugs or fantasy architecture. All new furniture/material/architecture masters generated through built-in imagegen; originals and native scale manifest retained.\n\nTwo opposite six-seat team suites (five players plus coach/alternate) occupy the upper side wings. A genuinely separate caster/broadcast desk with audio mixer and microphones is centered north. The central competition court and short spectator banks are framed by a 96px circulation loop. South arrival supports check-in and a social/coffee lounge.\n\nTwo isolated team Video call room definitions; one caster speaker/podium and one spectator listener area; no overlaps. Only the small 2 × 2 tile arrival receiver is quiet. Social seats are ordinary proximity. No portals, scores, game integration, roof script, focus script or true multiheight physics.\n\nPlayers sit directly at equipment. The revised sample uses a native192 × 49 competition desk and192 × 41 caster desk, 32 × 36 task chairs, and unchanged32px Greg v3 fixture. Actual16 × 16 bodies and safe backrest partitions will be verified after approval.\n\nFirst gate: review/REVIEW-REVISION-industrial-native32.png and review/LAYOUT-DIAGRAM.png. Revised bounded source art only; await root release before full implementation.\n''')
