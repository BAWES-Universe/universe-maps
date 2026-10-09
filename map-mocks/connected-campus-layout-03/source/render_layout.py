from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import html, json, math
OUT=Path('../magical-arrival-layout')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
C={'bg':'#102b32','panel':'#183941','muted':'#a9c4c4','cream':'#eadcc0','ink':'#17383d','gold':'#e8b566','team':'#b9d3c0','glass':'#b8dddf','public':'#ded0ac','green':'#4b7761','garden':'#294f46','water':'#65b9c0','path':'#c4bfa7','pink':'#bc989a','white':'#f3eee3'}
class Canvas:
 def __init__(self,w,h):
  self.w,self.h=w,h; self.im=Image.new('RGB',(w,h),C['bg']);self.d=ImageDraw.Draw(self.im);self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="{C["bg"]}"/>']
 def rect(self,b,fill,stroke=None,sw=1,r=0,dash=None):
  x,y,x2,y2=b
  if r:self.d.rounded_rectangle(b,radius=r,fill=fill,outline=stroke,width=sw)
  else:self.d.rectangle(b,fill=fill,outline=stroke,width=sw)
  self.svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" rx="{r}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def circle(self,x,y,r,fill,stroke=None,sw=1):
  self.d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=stroke,width=sw);self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')
 def line(self,pts,fill,sw=1):
  self.d.line(pts,fill=fill,width=sw,joint='curve'); self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
 def text(self,x,y,s,size=18,fill=None,bold=False,anchor='la'):
  font=ImageFont.truetype(BOLD if bold else FONT,size);fill=fill or C['white'];self.d.text((x,y),s,font=font,fill=fill,anchor=anchor)
  self.svg.append(f'<text x="{x}" y="{y+size*.81}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{"middle" if anchor=="ma" else "start"}" fill="{fill}">{html.escape(s)}</text>')
 def save(self,name):
  self.im.save(OUT/f'{name}.png'); (OUT/f'{name}.svg').write_text(''.join(self.svg)+'</svg>')
def tag(c,x,y,n):
 c.circle(x,y,15,C['bg'],C['gold'],2);c.text(x,y-10,str(n),17,C['gold'],True,'ma')
def paragraph(c,x,y,lines,size=18,color=None):
 for i,t in enumerate(lines):c.text(x,y+i*(size+8),t,size,color or C['muted'])
def furniture(c,x,y,w=30,h=16):
 c.rect((x,y,x+w,y+h),C['gold'],C['ink'],1,3)
def arrow(c,pts,fill=C['gold'],sw=5):
 c.line(pts,fill,sw);x,y=pts[-1];a=math.atan2(y-pts[-2][1],x-pts[-2][0]);c.line([(x-12*math.cos(a-.5),y-12*math.sin(a-.5)),(x,y),(x-12*math.cos(a+.5),y-12*math.sin(a+.5))],fill,sw)
# Full site. Every position uses 32 px tile; center painted square is exactly 1024 px.
c=Canvas(1700,1510);c.text(48,32,'ONE HOME, ONE TOWN',34,bold=True);c.text(48,80,'Complete-campus planning proposal • surrounding extensions are unbuilt • schematic, not finished art',18,C['muted'])
ox,oy,S=48,142,.52
P=lambda x,y:(ox+x*S,oy+y*S)
B=lambda x,y,w,h:(ox+x*S,oy+y*S,ox+(x+w)*S,oy+(y+h)*S)
def box(x,y,w,h,fill,stroke=C['ink'],sw=3,r=4):c.rect(B(x,y,w,h),fill,stroke,sw,r)
def path(pts,w=96):c.line([P(x,y) for x,y in pts],C['path'],int(w*S))
def label(x,y,t,s=16):c.text(*P(x,y),t,s,C['ink'],True,'ma')
# Continuous ground, not separate islands.
box(0,0,2304,2368,C['garden'],None,0,72)
box(704,672,992,1152,C['path'],None,0,60)
# planted edge courtyards
for x,y,r in [(256,160,120),(1856,128,110),(2130,680,125),(320,1520,155),(1900,1720,155),(200,2140,130),(2120,2200,120)]:
 px,py=P(x,y);c.circle(px,py,r*S,C['green'])
path([(1184,2144),(1184,768)],192);path([(640,880),(1760,880)],96);path([(736,704),(736,1216)],96);path([(1504,640),(1696,640)],96)
# Painted proof extent and workplace
box(640,256,1024,1024,None,C['gold'],3,0)
c.text(*P(652,268),'PAINTED STUDY: 1024 × 1024 px',14,C['gold'],True)
box(800,352,704,416,C['team'],C['cream'],7,8)
box(1312,384,160,192,C['glass'],C['ink'],2,4)
box(848,384,416,64,C['green'],None,0)
label(1090,490,'STUDENTHUB',24);label(1090,542,'shared team core',16)
# core desks
for x,y in [(896,592),(1152,592)]:
 a,b=P(x,y);furniture(c,a,b,44,16);c.circle(a+9,b+26,5,C['ink']);c.circle(a+35,b+26,5,C['ink'])
box(1248,672,128,48,C['gold'],C['ink'],1,4);label(1300,732,'reception',13)
box(832,664,160,64,C['pink'],C['cream'],2,5)
box(832,664,48,64,C['team'],C['ink'],1,3)
# doormark open
path([(1184,720),(1184,792)],96)
# conference extension
box(1568,352,448,384,C['glass'],C['cream'],6,8)
box(1600,384,160,128,C['team'],C['ink'],1);box(1792,384,192,128,C['team'],C['ink'],1)
label(1800,559,'MEETING GALLERY',18);label(1792,606,'2 quiet + conference',13)
# Civic wing, contiguous public cloister
box(64,448,608,896,C['public'],C['cream'],7,8)
box(96,480,544,352,C['cream'],C['ink'],2);label(368,512,'CLASSROOM',19)
box(256,568,224,40,C['green'],C['ink'],1)
for xx in [160,288,416,544]:
 for yy in [656,736]:
  a,b=P(xx,yy);furniture(c,a,b,25,13)
box(96,896,544,416,C['cream'],C['ink'],2);label(368,928,'GREAT HALL',19)
box(192,976,352,80,C['green'],C['ink'],2)
a,b=P(348,1032);furniture(c,a,b,18,13)
for xx in [192,272,464,544]:
 for yy in [1120,1184,1248]:
  a,b=P(xx,yy);c.rect((a,b,a+12,b+12),C['ink'],None,0,2)
path([(640,752),(736,752)],64);path([(640,1152),(736,1152)],64)
# fountain off axis + lounge
px,py=P(1056,976);c.circle(px,py,104*S,C['cream'],C['ink'],3);c.circle(px,py,80*S,C['water'],C['ink'],2);c.circle(px,py,24*S,C['gold'])
box(1344,944,224,160,C['pink'],C['cream'],3,16)
box(1360,960,192,40,C['team'],C['ink'],2,6);box(1360,1024,40,64,C['team'],C['ink'],2,6);box(1512,1024,40,64,C['team'],C['ink'],2,6)
label(1456,1140,'couches + carpet',14)
# market shops set back from street
for x,y in [(768,1376),(1376,1376),(768,1568),(1376,1568)]:
 box(x,y,160,128,C['public'],C['cream'],4,3);box(x,y,160,32,C['green'],None,0)
label(1184,1730,'MARKET LANE',18)
# portal garden future rooms
path([(1600,1248),(1952,1248)],96)
for x,y in [(1824,1056),(2048,1248),(1824,1472)]:
 a,b=P(x,y);c.circle(a,b,40,C['glass'],C['gold'],3);c.circle(a,b,22,C['bg'])
label(1952,1625,'PORTAL GARDEN',17)
# giant threshold/arrival
box(896,1888,576,320,C['cream'],C['gold'],4,12)
box(864,1840,160,192,C['green'],C['cream'],4,7);box(1344,1840,160,192,C['green'],C['cream'],4,7)
box(1024,1856,320,48,C['gold'],None,0);label(1184,2040,'MONUMENTAL GATE',19);label(1184,2100,'arrival forecourt',15)
# circulation gold main, blue public, dashed meaning via keyed strings
arrow(c,[P(1184,2150),P(1184,1740),P(1184,1240),P(1184,800)],C['gold'],5)
arrow(c,[P(1100,880),P(736,880),P(736,1152),P(672,1152)],C['water'],4)
# proof numbers
for n,(x,y) in enumerate([(1510,1890),(1160,970),(805,350),(1710,348),(90,448),(91,891),(779,1370),(2030,1070)],1):tag(c,*P(x,y),n)
# clear right legend
rx=1285
c.text(rx,152,'A SMALL TEAM STAYS TOGETHER',18,C['gold'],True)
paragraph(c,rx,194,['Reception and everyday desks share','one room. Departments are useful','stations, never separate destinations.'],17)
items=[('1  ARRIVE',['Giant gate → lantern avenue.','The fountain and Hub door reveal','the next steps without a map.']),('2  GATHER',['Off-axis fountain keeps the direct','route clear. One warm outdoor','lounge sits beside it, not in it.']),('3  WORK TOGETHER',['Four daily seats, shared tool wall,','visible glass meeting room.','4–7 clear tile steps to first desks.']),('4  QUIET CONVERSATIONS',['Two small meeting rooms and one','flexible conference room extend','the same StudentHub shell.']),('5–6  LEARN / CONVENE',['One civic pavilion: teacher-led','classroom, stage, podium, audience.','Public cloister bypasses team desks.']),('7  MARKET / SHOPS',['Four sheltered, reachable booths.','Reserved counter positions for','future hosts and bot integrations.']),('8  EXPAND',['Portals reach bigger events,','labs or creator rooms. Daily work','still happens in the shared core.'])]
y=315
for title,lines in items:
 c.text(rx,y,title,18,C['white'],True);paragraph(c,rx,y+33,lines,16);y+=135
c.line([(rx,1280),(1650,1280)],C['green'],2)
paragraph(c,rx,1300,['Gold outline = painted study area.','Footprints indicate planned relationships.','Spatial access ≠ configured privacy.','No live services are asserted.'],15)
c.text(48,1430,'32 px per tile • unchanged 32 px Woka • main routes ≥ 3 tiles • 72 × 74 tile complete site envelope',17,C['muted'])
c.save('01-connected-campus-concept')
# Detail: scale native source pixel to .9, origin 56,160. Section visible at 922 square.
c=Canvas(1630,1340);c.text(48,32,'STUDENTHUB: RECEPTION TO TEAM IN VIEW',30,bold=True);c.text(48,78,'Dimensioned concept aligned to the lead’s 1024 × 1024 section • no separate department rooms',18,C['muted'])
ox,oy,S=48,146,.92
P=lambda x,y:(ox+x*S,oy+y*S)
B=lambda x,y,w,h:(ox+x*S,oy+y*S,ox+(x+w)*S,oy+(y+h)*S)
def r(x,y,w,h,fill,stroke=C['ink'],sw=2,rr=0):c.rect(B(x,y,w,h),fill,stroke,sw,rr)
def t(x,y,s,size=17,color=None):c.text(*P(x,y),s,size,color or C['ink'],True,'ma')
r(0,0,1024,1024,C['garden'],C['gold'],3)
r(120,496,824,468,C['path'],None,0,35)
r(160,96,704,416,C['cream'],C['cream'],9,8)
# A single room, perimeter station furniture, structural arches.
r(176,112,672,384,C['team'],C['ink'],2,4)
for x in [192,384,576,832]:r(x,112,16,24,C['green'],None,0)
# Glass meeting east, 5 x 6 tiles
r(672,128,160,192,C['glass'],C['ink'],3)
r(688,180,128,48,C['cream'],C['ink'],2,8)
for x in [704,784]:
 for y in [156,246]:
  a,b=P(x,y);c.circle(a,b,8,C['ink'])
t(752,278,'MEET',16)
# north perimeter shared tool counter bays -- three clearly different compositions
r(208,136,112,44,C['gold'],C['ink'],2,4);r(352,136,112,44,C['gold'],C['ink'],2,4);r(496,136,112,44,C['gold'],C['ink'],2,4)
t(264,185,'LAB',13);t(408,185,'OPS / CRM',13);t(552,185,'MEDIA / DESIGN',12)
# Thin rug unifies team group. Continuous center path intact.
r(216,232,432,200,'#98bcae',C['cream'],2,12)
# Six desks as two mirrored clusters; 64 px surfaces, 24 px chairs.
for x,y in [(248,244),(344,244),(440,244),(248,384),(344,384),(440,384)]:
 r(x,y,64,32,C['gold'],C['ink'],2,4)
 # chair drawn behind accessible desk-side, not inset into tabletop
 cy=y+50 if y==244 else y-34
 r(x+20,cy,24,24,C['green'],C['ink'],1,4)
 # workstation indicator
 r(x+16,y+7,28,6,C['ink'],None,0)
# lounge, low furnishing along east half
r(680,352,144,96,C['pink'],C['cream'],2,10);r(688,360,128,32,C['cream'],C['ink'],2,5)
a,b=P(752,418);c.circle(a,b,14,C['gold'],C['ink'],2)
# south entry vestibule remains open and reception is to side
r(480,480,128,40,C['path'],None,0)
r(624,452,144,40,C['gold'],C['ink'],2,8);t(696,432,'RECEPTION',14)
# door piers remain after roof fade
r(464,464,16,48,C['green'],None,0);r(608,464,16,48,C['green'],None,0)
# welcome spawn (center passage 544,448) and everyday approach to nearest eastern desk
px,py=P(544,448);c.circle(px,py,14,C['white'],C['ink'],2);t(544,442,'W',12)
arrow(c,[P(544,444),P(560,400),P(560,336),P(488,336)],C['gold'],5)
# 32 px actual sprite proxy figure and footsteps tiny architectural not artwork
for x,y in [(552,414),(552,384),(552,354)]:
 a,b=P(x,y);c.circle(a,b,3,C['gold'])
# fountain offset with direct axis clear
for x,y,rad in [(280,658,76),(810,682,79),(210,850,80),(836,884,75)]:
 a,b=P(x,y);c.circle(a,b,rad*S,C['green'])
a,b=P(416,720);c.circle(a,b,90*S,C['cream'],C['ink'],3);c.circle(a,b,68*S,C['water'],C['ink'],2);c.circle(a,b,19*S,C['gold'])
r(648,760,160,120,C['pink'],C['cream'],2,8);r(656,768,144,32,C['cream'],C['ink'],2,5)
r(656,824,32,48,C['cream'],C['ink'],2,4);r(768,824,32,48,C['cream'],C['ink'],2,4)
t(418,838,'FOUNTAIN',18);t(728,916,'COMMONS',16)
arrow(c,[P(544,992),P(544,552)],C['gold'],6)
t(544,935,'FROM GIANT GATE',15)
# glass extension connection; beyond crop
c.line([P(848,368),P(995,368)],C['glass'],12);t(908,392,'to quiet rooms',13)
# location labels
for n,(x,y) in enumerate([(160,96),(616,440),(208,242),(668,122),(208,132),(656,352)],1):tag(c,*P(x,y),n)
rx=1040
c.text(rx,155,'ONE CONNECTED WORKPLACE',21,C['gold'],True)
paragraph(c,rx,200,['The open floor, shared rug and continuous','north wall keep the team visually together.','Six everyday desks use the same workspace.'],18)
notes=[('1  ROOM SHAPE SURVIVES REVEAL',['Outside: a real roof, clerestory and doorway.','Inside: fade only opaque roof surfaces; keep','rim, columns, glazing and low side walls.']),('2  A REAL WELCOME THRESHOLD',['Reception sits beside the route, not across it.','Spawn at (544, 448); door at (544, 512).','Nearest desk approach: about 6 tile steps.']),('3  DAILY WORK = ONE SHARED CORE',['576 × 352 px core envelope; glass meeting','room occupies its east edge. Furnished team','group stays within 432 × 200 px.']),('4  GLASS MEETING ROOM',['160 × 192 px room, 128 px table, 4 seats.','Glazing gives sightlines; actual call privacy','must be configured and tested separately.']),('5  TOOLS WITHOUT DEPARTMENT SILOS',['Lab bench; Ops / CRM dashboard; media +','design surface for Imagine, music and review.','They are shared stations, not live services.']),('6  INFORMAL CONVERSATION',['Small interior couch and rug off the aisle.','Larger outdoor lounge beside the fountain.','No duplicate carpet islands on the main path.'])]
y=330
for head,lines in notes:
 c.text(rx,y,head,18,C['white'],True);paragraph(c,rx,y+34,lines,17);y+=143
c.text(48,1140,'SCALE / CLEARANCE',19,C['gold'],True)
paragraph(c,48,1180,['32 px Woka • desk 64 × 32 px • chair 24 × 24 px • main route 96–128 px • clear chair pullback ≥ 32 px',
'Native image and engine proof still need to validate sprite fit, diagonal passage, collisions, shadows and roof transitions.'],17)
c.save('02-studenthub-core-concept')
print('Created:',*list(OUT.glob('*.png')),sep='\n')
