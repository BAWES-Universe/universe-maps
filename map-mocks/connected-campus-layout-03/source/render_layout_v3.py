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

# One combined board: full public campus plus a readable office enlargement.
c=Canvas(2820,1840)
c.text(48,32,'ONE CONNECTED OFFICE, ROOM FOR EACH TEAM',37,bold=True)
c.text(48,86,'Revised planning proposal • expanded department pods + personal footprints • market behind HQ • riverside garden',21,C['muted'])
c.text(48,140,'CAMPUS CONNECTIONS',24,C['gold'],True)
ox,oy,S=48,195,.355
P=lambda x,y:(ox+x*S,oy+y*S)
B=lambda x,y,w,h:(ox+x*S,oy+y*S,ox+(x+w)*S,oy+(y+h)*S)
def box(x,y,w,h,fill,stroke=C['ink'],sw=2,r=4):c.rect(B(x,y,w,h),fill,stroke,sw,r)
def path(pts,w=96):c.line([P(x,y) for x,y in pts],C['path'],max(1,int(w*S)))
def label(x,y,txt,sz=16,color=None):c.text(*P(x,y),txt,sz,color or C['ink'],True,'ma')
box(0,0,3200,3584,C['garden'],None,0,60)
# One river along the east side, no second shoreline.
river=[(3060,0),(3008,400),(3090,960),(3050,1470),(3090,1960),(3020,2460),(3100,3060),(3060,3584)]
c.line([P(x,y) for x,y in river],C['cream'],69)
c.line([P(x,y) for x,y in river],C['water'],60)
c.line([P(x+18,y) for x,y in river],'#91ced0',3)
# Public court and obvious axis.
box(736,1664,1760,1184,C['path'],None,0,55)
path([(1504,3430),(1504,1632)],192)
path([(608,1792),(2752,1792)],96)
# Back lane is entirely outside the office, reached by the west side.
path([(768,1792),(448,1792),(448,256),(1920,256)],96)
path([(448,960),(192,960)],96)
# Large connected workplace; low internal dividers, one architectural shell.
box(512,320,1984,1344,C['team'],C['cream'],7,10)
label(1504,328,'STUDENTHUB · ONE SHARED OFFICE',17)
pods=[('Operations',64,64),('Recruitment',544,64),('Sales',1056,64),('Tech',1536,64),('Design / Media',64,704),('Marketing',544,704),('Research',1056,704),('Flexible growth',1536,704)]
for title,x,y in pods:
 box(512+x,320+y,352,384,'#99beae',C['green'],2,8)
 label(512+x+176,320+y+28,title,14)
 for xx,yy in [(x+32,y+112),(x+208,y+112)]:
  box(512+xx,320+yy,80,32,C['gold'],C['ink'],1,3)
  px,py=P(512+xx+40,320+yy+58);c.circle(px,py,4,C['ink'])
 # dotted prospective extension is represented by clear plus marker, not an actual seat count
 label(512+x+176,320+y+264,'expandable',12)
path([(640,320+576),(2400,320+576)],128)
path([(1504,320+448),(1504,320+1344)],128)
label(1504,852,'SHARED TEAM SPINE',14)
box(1632,1472,288,80,C['gold'],C['ink'],2,5)
label(1776,1576,'reception',14)
box(736,1440,288,144,C['pink'],C['cream'],2,6)
label(880,1490,'lounge',14)
# Open entrance is wider than the walkable lane.
box(1440,1640,128,48,C['path'],None,0)
# Attached quiet meeting gallery with direct HQ connection and front visitor route.
path([(2496,1184),(2656,1184)],96)
box(2560,768,384,832,C['glass'],C['cream'],5,6)
for yy in [816,1056]:
 box(2592,yy,320,176,C['team'],C['ink'],1,5)
 label(2752,yy+58,'MEETING',13)
box(2592,1296,320,256,C['cream'],C['ink'],1,5);label(2752,1390,'CONFERENCE',14)
path([(2752,1600),(2752,1792)],96)
# Two small back-of-house market booths, modest inventory footprint.
for x in [1088,1504]:
 box(x,32,160,128,C['public'],C['cream'],3,3);box(x,32,160,32,C['green'],None,0)
label(1380,187,'SMALL MARKET · BEHIND HQ',16,C['white'])
# Optional portal garden is reached from the same public side lane.
for x,y in [(192,656),(160,928),(224,1216)]:
 a,b=P(x,y);c.circle(a,b,26,C['glass'],C['gold'],3);c.circle(a,b,14,C['bg'])
label(230,1380,'PORTALS',15,C['white'])
# Civic pavilion: teacher/student classroom plus stage/podium/audience.
box(32,1824,608,1120,C['public'],C['cream'],5,8)
box(64,1856,544,448,C['cream'],C['ink'],2);label(336,1900,'CLASSROOM',18)
box(192,1984,256,48,C['green'],C['ink'],1)
for x in [144,272,400,528]:
 for y in [2096,2208]:box(x,y,64,32,C['gold'],C['ink'],1,2)
box(64,2368,544,544,C['cream'],C['ink'],2);label(336,2412,'GREAT HALL',18)
box(160,2500,352,96,C['green'],C['ink'],1)
box(308,2570,40,32,C['gold'],C['ink'],1)
for x in [176,272,400,496]:
 for y in [2690,2770,2850]:box(x,y,32,32,C['ink'],None,0,2)
path([(608,2176),(704,2176),(704,1792)],96);path([(608,2784),(704,2784),(704,2176)],96)
# Fountain and common lounge off the direct route.
a,b=P(1248,1984);c.circle(a,b,128*S,C['cream'],C['ink'],3);c.circle(a,b,98*S,C['water'],C['ink'],2);c.circle(a,b,28*S,C['gold'])
box(1872,1920,352,224,C['pink'],C['cream'],2,12);box(1896,1944,288,48,C['team'],C['ink'],1,4)
box(1896,2032,48,80,C['team'],C['ink'],1,4);box(2136,2032,48,80,C['team'],C['ink'],1,4)
label(2056,2200,'COMMONS',16)
# Plant the former market frontage rather than adding inventory.
for x,y,w,h in [(960,2320,256,288),(1856,2320,288,288),(1030,2690,176,128),(1856,2690,176,128)]:box(x,y,w,h,C['green'],C['garden'],2,30)
label(1504,2850,'LANTERN AVENUE',17,C['white'])
# Riverside public garden and open fire-circle, no travel through office.
path([(2320,2208),(2576,2208),(2864,2208),(2880,2720)],96)
path([(2576,2208),(2496,2448),(2576,2660),(2820,2660)],96)
a,b=P(2672,2448);c.circle(a,b,212*S,C['path'],C['cream'],3);c.circle(a,b,58*S,C['cream'],C['ink'],2);c.circle(a,b,36*S,'#b47144',C['ink'],2);c.circle(a,b,18*S,C['gold'])
for x,y,w,h in [(2592,2304,160,32),(2528,2400,32,128),(2784,2400,32,128),(2592,2576,160,32)]:box(x,y,w,h,C['team'],C['ink'],1,5)
label(2672,2730,'FIREPIT + GARDEN',16,C['white']);label(2672,2790,'local crackle · proposed',12,C['muted'])
for x,y,rad in [(2660,2040,86),(2590,2920,120),(2820,3100,108),(840,3030,112),(2096,3220,120)]:
 a,b=P(x,y);c.circle(a,b,rad*S,C['green'])
# Giant gateway with a quiet centered approach.
box(1184,3056,640,352,C['cream'],C['gold'],4,12)
box(1120,3008,176,208,C['green'],C['cream'],4,6);box(1712,3008,176,208,C['green'],C['cream'],4,6)
box(1296,3024,416,48,C['gold'],None,0)
label(1504,3232,'MONUMENTAL GATE',20)
arrow(c,[P(1504,3392),P(1504,2816),P(1504,1728)],C['gold'],5)
arrow(c,[P(816,1792),P(448,1792),P(448,256),P(1000,256)],C['water'],4)
arrow(c,[P(2250,2208),P(2464,2208),P(2576,2250)],C['water'],4)
# Relationship captions avoid a false final capacity.
paragraph(c,48,1510,['Gate → fountain → reception → shared office spine.','Back-lane market and riverside hangout are optional public routes.','No public shortcut passes through department desks.'],22)
paragraph(c,48,1640,['Conceptual 32 px-tile coordinates; all footprints are proposals.','Earlier four-seat scheme is superseded. Top-down furniture scale','and claim-area behavior still require implementation validation.'],18)
# OFFICE ZOOM; positions are local to the single 1984 × 1344 shell.
ox,oy,S=1285,230,.72
P=lambda x,y:(ox+x*S,oy+y*S)
B=lambda x,y,w,h:(ox+x*S,oy+y*S,ox+(x+w)*S,oy+(y+h)*S)
c.text(1285,140,'STUDENTHUB · EXPANDABLE TEAM PODS',24,C['gold'],True)
c.text(1285,184,'Personal places within a connected office; team size is not assumed.',20,C['muted'])
box(0,0,1984,1344,C['team'],C['cream'],8,12)
# Shared 8-tile cross-spine plus 4-tile north/south approach.
box(32,448,1920,256,C['cream'],None,0)
box(928,448,128,896,C['cream'],None,0)
label(992,550,'SHARED SPINE · CLEAR SIGHTLINES',21)
label(992,590,'walk between teams without crossing their desks',17)
# Each pod has 2 worked examples and 2 dotted extension plots, not fixed capacity.
colors=['#90b6a5','#9bbdac','#a5c6b4','#91b0b1','#b9b5a0','#b0bfaa','#99bfb1','#bfd0c0']
for idx,(title,x,y) in enumerate(pods):
 box(x,y,352,384,colors[idx],C['green'],3,9)
 label(x+176,y+13,title.upper(),18)
 subtitle='Ahmed + team' if idx==0 else 'Fawaz + team' if idx==1 else ('Imagine / music / review' if idx==4 else 'capacity to confirm')
 label(x+176,y+43,subtitle,13)
 # individual plots with actual desk+chair in example row
 for j,dx in enumerate([32,192]):
  px,py=x+dx,y+64
  box(px,py,128,128,'#d9e4d6',C['ink'],1,3)
  box(px+32,py+18,64,32,C['gold'],C['ink'],1,3)
  box(px+52,py+64,24,24,C['green'],C['ink'],1,3)
  name='Ahmed' if idx==0 and j==0 else 'Fawaz' if idx==1 and j==0 else 'personal plot'
  label(px+64,py+103,name,12)
  # schematic dashed perimeter and plus symbol reserves potential growth
  px2,py2=px,y+224
  c.rect(B(px2,py2,128,128),None,C['green'],2,3,'7 6')
  label(px2+64,py2+29,'+',25)
  label(px2+64,py2+76,'growth',12)
 # planter edge leaves a broad opening facing the shared spine
 if y<500:box(x,y+376,96,8,C['green'],None,0);box(x+256,y+376,96,8,C['green'],None,0)
 else:box(x,y,96,8,C['green'],None,0);box(x+256,y,96,8,C['green'],None,0)
# Shared threshold, useful lounge and reception beside the lane.
box(224,1144,336,144,C['pink'],C['cream'],2,12)
box(240,1160,144,32,C['cream'],C['ink'],1,4);box(472,1200,32,64,C['cream'],C['ink'],1,4)
label(392,1254,'LOUNGE',16)
box(1120,1176,336,80,C['gold'],C['ink'],2,8)
label(1288,1280,'RECEPTION',18)
box(928,1320,128,40,C['path'],None,0)
a,b=P(992,1192);c.circle(a,b,15,C['white'],C['ink'],2);label(992,1182,'W',14)
arrow(c,[P(992,1176),P(992,672),P(992,640)],C['gold'],5)
# side exit to controlled meetings and front visitor approach
path([(1968,1136),(2050,1136)],96)
label(1780,1248,'→ quiet meeting gallery',17)
# Zoom legend / safeguards
c.text(1285,1260,'WHAT CHANGED',23,C['gold'],True)
paragraph(c,1285,1310,['• Larger office with distinct Operations, Recruitment, Sales, Tech,',
'  Design/Media, Marketing and Research clusters, plus a growth bay.',
'• Personal desk footprints are visible and individually claimable in intent.',
'  Two examples + growth plots illustrate each pod; they are not headcounts.',
'• Low dividers and wide shared paths balance recognition and focus.',
'  Actual speech separation and claim permissions need runtime verification.',
'• Market is behind the office; garden and firepit face one riverside.',
'  Crackle should fade locally and remain inaudible at work desks.'],20)
c.text(1285,1700,'TOP-DOWN PLAN, NOT A FINISHED RENDER',20,C['gold'],True)
paragraph(c,1285,1740,['Furniture, seating directions, occupancy and native-scale Woka clearance',
'are acceptance checks before new environment art is approved.'],18)
c.save('04-expanded-office-riverside-plan-v3')
