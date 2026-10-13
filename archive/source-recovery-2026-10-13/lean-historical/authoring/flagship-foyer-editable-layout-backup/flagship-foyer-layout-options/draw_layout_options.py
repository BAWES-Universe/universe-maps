from pathlib import Path
from PIL import Image
import base64, html, json, subprocess
P=Path(__file__).resolve().parent; (P/'context').mkdir(exist_ok=True)
SRC=Path('/workspace/shared/grand-auditorium-01/review/flagship-empty-native.png')
CROPS={'unchanged-auditorium-context':(0,0,1536,944),'unchanged-rear-hall-context':(64,720,1472,944)}
if SRC.exists():
 im=Image.open(SRC)
 for name,box in CROPS.items():im.crop(box).save(P/'context'/f'{name}.png')
else:
 for name in CROPS:
  if not (P/'context'/f'{name}.png').exists():raise FileNotFoundError('Keep the bundled context folder beside this script.')
def data_img(name):return 'data:image/png;base64,'+base64.b64encode((P/'context'/f'{name}.png').read_bytes()).decode()
C={'ink':'#163C40','muted':'#5A7473','paper':'#FBFAF6','floor':'#F1EBDD','line':'#C4C8BE','social':'#D5E6DF','chair':'#327A77','coffee':'#BB793E','coffee_lite':'#F0DDC3','route':'#DCEFF3','blue':'#408F9D','green':'#D6DFBC','plant':'#8B9E71','white':'#FFFFFF'}
class SVG:
 def __init__(self,w=1800,h=1390):
  self.w,self.h=w,h;self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="#408F9D" stroke-width="1.5"/></marker><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M-2,2 L2,-2 M0,10 L10,0 M8,12 L12,8" stroke="#C0BDAF" stroke-width="1"/></pattern></defs>'];self.rect(0,0,w,h,C['paper'])
 def add(self,s):self.a.append(s)
 def rect(self,x,y,w,h,fill,stroke=None,sw=1,r=0,dash=None):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def line(self,x1,y1,x2,y2,stroke=C['line'],sw=1,dash=None):self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def path(self,d,fill='none',stroke=None,sw=1,dash=None,arrow=False):self.add(f'<path d="{d}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else '')+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def circle(self,x,y,r,fill,stroke=None,sw=1):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
 def text(self,x,y,t,size=22,weight=400,fill=C['ink'],anchor='start',spacing=None):self.add(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'+(f' letter-spacing="{spacing}"' if spacing else '')+'>'+html.escape(t)+'</text>')
 def multiline(self,x,y,lines,size=22,lineh=31,**kw):
  for i,line in enumerate(lines):self.text(x,y+i*lineh,line,size,**kw)
 def image(self,name,x,y,w,h):self.add(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{data_img(name)}"/>')
 def save(self,name):
  path=P/f'{name}.svg';path.write_text('\n'.join(self.a+['</svg>'])); subprocess.run(['inkscape',str(path),'--export-type=png',f'--export-filename={P/name}.png'],check=True,capture_output=True)

def header(s,letter,title,sub,badge):
 s.rect(0,0,1800,12,C['ink']);s.rect(60,47,67,67,C['ink'],r=16);s.text(93.5,95,letter,43,700,C['white'],'middle');s.text(148,81,title,42,700);s.text(148,116,sub,22,400,C['muted']);s.rect(1440,50,300,44,'#E7EBDD',r=22);s.text(1590,79,badge,17,700,C['ink'],'middle');s.line(60,145,1740,145,C['line'],1)

def hall_context(s,x,y,g):
 s.image('unchanged-rear-hall-context',x,y,44*g,7*g)
 # The source context ends at y944. Represent the next64 pixels as a plain threshold only.
 ty=y+7*g;s.rect(x,ty,44*g,2*g,'#E9E4D9',C['ink'],2)
 for a,b in [(14,17),(27,30)]:
  s.rect(x+a*g,ty-2,(b-a)*g,2*g+4,C['floor']);s.line(x+a*g,ty,x+a*g,ty+2*g,C['ink'],3);s.line(x+b*g,ty,x+b*g,ty+2*g,C['ink'],3)
 s.text(x+1*g,y+6.2*g,'EXISTING AUDITORIUM · REAR ROWS',18,700,C['white'])
 return ty+2*g

def inset_and_cards(s,side_x=1370,base_y=175,which='A'):
 w=370
 s.text(side_x,base_y,'YOUR HALL STAYS',21,700)
 s.image('unchanged-auditorium-context',side_x,base_y+17,w,w*944/1536)
 s.multiline(side_x,base_y+17+w*944/1536+28,['Original giant stage + 210 chairs.','Context only; furniture is untouched.'],17,25,fill=C['muted'])
 if which=='A':
  yy=base_y+342
  cards=[('01','Rooms to stay in',['Four proper lounge bays,','with chairs facing around tables.','16 lounge seats + 4 café seats.']),('02','A clear way through',['4-tile receiving landings sit','below the 3-tile hall openings.','Arrival stays out of social bays.']),('03','Coffee has its own space',['Separate counter + service apron.','The queue stays inside its bay,','away from both hall approaches.'])]
 else:
  yy=base_y+342
  cards=[('01','An outdoor destination',['The social space bends east','into a garden-side commons.','It is not another indoor box.']),('02','A broad promenade',['8-tile-wide circulation band','below the landing and stairs.','A step-free side path also fits.']),('03','A café pavilion',['Coffee is offset from the doors.','Lower lounge groups have their','own covered garden-facing bays.'])]
 for num,title,lines in cards:
  s.circle(side_x+16,yy-7,17,C['ink']);s.text(side_x+16,yy-1,num,14,700,C['white'],'middle');s.text(side_x+46,yy,title,21,700)
  s.multiline(side_x+46,yy+34,lines,18,27,fill=C['muted']);yy+=155
 return yy

class Plan:
 def __init__(self,s,x,y,g):self.s=s;self.x=x;self.y=y;self.g=g
 def xy(self,x,y):return self.x+x*self.g,self.y+y*self.g
 def rect(self,x,y,w,h,fill,stroke=None,sw=1,r=0,dash=None):self.s.rect(*self.xy(x,y),w*self.g,h*self.g,fill,stroke,sw,r,dash)
 def line(self,x1,y1,x2,y2,color=C['line'],sw=1,dash=None):self.s.line(*self.xy(x1,y1),*self.xy(x2,y2),color,sw,dash)
 def text(self,x,y,t,size=20,weight=400,fill=C['ink'],anchor='start'):self.s.text(*self.xy(x,y),t,size,weight,fill,anchor)
 def route(self,points,sw=3,arrow=True,dash='8 10'):
  xy=[self.xy(*z) for z in points];d='M '+' L '.join(f'{x},{y}' for x,y in xy);self.s.path(d,stroke=C['blue'],sw=sw,dash=dash,arrow=arrow)
 def grid(self,x,y,w,h):
  for i in range(w+1):self.line(x+i,y,x+i,y+h,'#CBCBC1',0.6)
  for j in range(h+1):self.line(x,y+j,x+w,y+j,'#CBCBC1',0.6)
 def chair(self,x,y,angle=0):
  px,py=self.xy(x,y);g=self.g;self.s.add(f'<g transform="translate({px},{py}) rotate({angle})">');self.s.rect(-.48*g,-.48*g,.96*g,.96*g,C['chair'],C['ink'],1,r=.15*g);self.s.rect(-.48*g,-.48*g,.96*g,.24*g,'#9AC3B5',C['ink'],.8,r=.07*g);self.s.add('</g>')
 def table(self,x,y,r=.65):self.s.circle(*self.xy(x,y),r*self.g,'#EBCF9E',C['coffee'],1.4)
 def person(self,x,y,rot=0):
  px,py=self.xy(x,y);g=self.g;self.s.add(f'<g transform="translate({px},{py}) rotate({rot})">');self.s.rect(-.5*g,-.5*g,g,g,'none','#7B8880',.8,dash='2 3');self.s.add(f'<ellipse cx="0" cy="{.14*g}" rx="{.34*g}" ry="{.27*g}" fill="#163C40"/>');self.s.circle(0,-.17*g,.2*g,'#FBFAF6','#163C40',1.4);self.s.add('</g>')
 def plant(self,x,y,w=1.8,h=.8):
  self.rect(x,y,w,h,'#9DAD86',C['plant'],1,r=3)
  for i in range(max(1,int(w*1.5))):self.s.circle(*self.xy(x+(i+.5)/(max(1,int(w*1.5)))*w,y+h/2),min(w,h)*self.g*.3,'#7E9868')
 def group(self,x,y,w,h,label,variant=0,seatcount=4):
  self.rect(x,y,w,h,C['social'],'#9BBBAD',1.5,r=9);self.text(x+.5,y+.92,label,18,700)
  cx=x+w/2;cy=y+h*.58
  self.table(cx,cy,.76)
  configs=[[(0,-1.7,0),(1.8,0,90),(0,1.7,180),(-1.8,0,-90)], [(-1.7,-.5,-70),(-.2,-1.9,10),(1.65,.25,95),(-.4,1.8,190)], [(-1.7,-.2,-90),(.1,-1.8,0),(1.65,-.1,90),(.4,1.8,180)]]
  for a,b,ang in configs[variant%3][:seatcount]:self.chair(cx+a,cy+b,ang)
  self.plant(x+w-2.7,y+h-.7,2.3,.45)

def dimension(s,x1,y1,x2,y2,label,vertical=False):
 s.line(x1,y1,x2,y2,C['muted'],1)
 if not vertical:
  s.line(x1,y1-7,x1,y1+7,C['muted'],1);s.line(x2,y2-7,x2,y2+7,C['muted'],1);s.text((x1+x2)/2,y1-9,label,19,600,C['muted'],'middle')
 else:
  s.line(x1-7,y1,x1+7,y1,C['muted'],1);s.line(x2-7,y2,x2+7,y2,C['muted'],1);s.add(f'<text x="{x1-12}" y="{(y1+y2)/2}" transform="rotate(-90 {x1-12} {(y1+y2)/2})" font-family="DejaVu Sans, sans-serif" font-size="18" font-weight="600" fill="{C["muted"]}" text-anchor="middle">{label}</text>')

def bottom(s,y,scale,trade,which):
 s.line(60,y,1740,y,C['line'],1);s.text(65,y+41,'PLAN KEY',18,700)
 for x,fill,label in [(204,C['social'],'Lounge bay'),(430,C['route'],'Clear route'),(660,C['coffee_lite'],'Coffee / service'),(962,C['green'],'Planting')]:
  s.rect(x,y+22,25,25,fill,C['muted'],1,r=3);s.text(x+37,y+42,label,18)
 s.text(65,y+83,scale,18,600);s.text(65,y+114,'Dashed square = 1×1-tile avatar scale guide. This is a spatial diagram, not a collision or capacity test.',18,fill=C['muted'])
 s.text(65,y+156,'TRADE-OFF',17,700);s.text(195,y+156,trade,20)
 s.text(65,y+203,'FOR VISUAL CHOICE ONLY · Proposed foyer is schematic · No new map artwork, room link or publication',18,700,C['muted'])
 s.text(65,y+232,'Social seat symbols are a design proposal, not accommodation for all 210 attendees. Neither mirror is retained.',17,fill=C['muted'])

# A: the grid starts at the original interior x64; hall openings map to x14–17 and x27–30.
s=SVG(1800,1460);header(s,'A','Deep indoor concourse','A generous foyer directly below the auditorium you liked.','RECOMMENDED · INTERIOR')
g=28;x=80;context_y=180;fy=hall_context(s,x,context_y,g);p=Plan(s,x,fy,g)
p.rect(0,0,44,22,C['floor'],C['ink'],3);p.grid(0,0,44,22)
# Quiet arrival / door circulation is spatially independent of furniture bays.
for a,b,c,d in [(13.5,0,4,13.5),(26.5,0,4,13.5),(13.5,9.5,17,4),(20,13.5,4,8.5)]:p.rect(a,b,c,d,C['route'])
p.grid(0,0,44,22)
p.group(1,2,11,7,'LOUNGE 01 · 11×7',0)
p.group(18.5,2,7,7,'LOUNGE 02',1)
p.group(32,2,11,7,'LOUNGE 03 · 11×7',2)
p.group(1,14,11,7,'LOUNGE 04 · 11×7',1)
p.rect(32,14,11,7,C['coffee_lite'],'#C79D72',1.5,r=8);p.text(32.5,14.93,'COFFEE BAY · 11×7',18,700)
# Counter has a real staff side, apron and separate seated pocket.
p.rect(38,15.3,4.3,1.1,C['coffee'],C['ink'],1.5,r=3);p.text(40.15,16.05,'COUNTER',13,700,C['white'],'middle');p.rect(38,16.7,4.3,3,'#F8EDDD','#BD9167',1,dash='5 5');p.text(40.15,18.25,'QUEUE',14,700,C['coffee'],'middle');p.text(40.15,18.93,'3-tile apron',13,400,C['coffee'],'middle')
p.table(34.7,18.1,.68)
for xx,yy,ang in [(34.7,16.6,0),(36.15,18.1,90),(34.7,19.6,180),(33.2,18.1,-90)]:p.chair(xx,yy,ang)
p.text(34.7,20.8,'4 café seats',16,400,C['muted'],'middle')
p.rect(17.5,17,1.75,2.5,'#D6CDB9',C['muted'],1,r=4);p.text(16.95,20.4,'WELCOME',15,700,anchor='middle');p.text(24.8,19.5,'DIRECT',18,700,C['blue']);p.text(24.8,20.35,'ARRIVAL',18,700,C['blue'])
# Routes do not pass through seating/coffee.
p.route([(22,21.35),(22,11.5),(15.5,11.5),(15.5,.5)]);p.route([(22,11.5),(28.5,11.5),(28.5,.5)]);p.text(22,12.65,'4-TILE CROSS-CONCOURSE',17,700,C['blue'],'middle')
p.text(15.5,1.08,'4 tiles',15,600,C['blue'],'middle');p.text(28.5,1.08,'4 tiles',15,600,C['blue'],'middle')
# Quiet intentional footfall, not fake event occupancy.
for xx,yy,rot in [(15.5,5.1,0),(28.5,7.5,0),(22,17.2,0),(31.1,11.4,90),(39.2,17.6,0)]:p.person(xx,yy,rot)
# South entrance is shown as an opening in the schematic wall.
p.line(18,22,26,22,C['floor'],5);p.text(22,23.4,'MAIN ARRIVAL · 8-tile opening',20,700,C['ink'],'middle')
dimension(s,x,fy-14,x+44*g,fy-14,'44 native tiles across the new interior')
dimension(s,x-26,fy,x-26,fy+22*g,'22 tiles deep',True)
s.text(x,fy+22*g+78,'Existing 3-tile hall openings stay aligned and feed new 4-tile receiving landings.',18,fill=C['muted'])
inset_and_cards(s)
# Native footprint scale in side panel.
sp=Plan(s,1370,1040,28);sp.person(.5,.5);s.multiline(1420,1051,['Avatar guide at plan scale','1 tile = 32 native pixels'],17,25,fill=C['muted']);
bottom(s,1180,'Drawing scale: 28 px per native 32 px tile (87.5%). Hall rear strip uses exactly the same scale.','Larger indoor footprint; the hall and foyer can remain one continuous room.','A');s.save('option-a-deep-indoor-concourse')

# B: substantially offset L-shaped outdoor composition, a different footprint and arrival experience.
s=SVG(1800,1560);header(s,'B','Covered garden + café forecourt','An offset social commons connected to the surrounding landscape.','ALTERNATIVE · EXTERIOR')
g=20;x=70;context_y=181;fy=hall_context(s,x,context_y,g);p=Plan(s,x,fy,g)
# Continuous surrounding ground first, no island boundary.
p.rect(-1,0,66,41,C['green']);p.grid(0,0,64,40)
# Upper landing, east cafe wing, 8-tile promenade, and the south-facing east commons produce an L.
outline=[(0,0),(44,0),(44,3),(64,3),(64,40),(46,40),(46,22),(0,22)]
coords=[p.xy(*z) for z in outline];s.path('M '+' L '.join(f'{a},{b}' for a,b in coords)+' Z',C['floor'],C['ink'],2.5)
# Broader route below the steps.
p.rect(0,14,64,8,C['route']);p.rect(46,14,5,26,C['route']);p.grid(0,0,64,40)
# Facade depth reserve distinct from hall (not new art).
p.rect(0,0,44,3,'#E0DED4',C['muted'],1,dash='6 5');p.rect(0,0,44,3,'url(#hatch)')
for a,b in [(14,17),(27,30)]:p.rect(a,0,b-a,3,C['route'])
p.text(1,1.3,'FAÇADE DEPTH RESERVE',16,700,C['muted']);p.text(1,2.35,'3 tiles for later artwork',16,400,C['muted'])
# Porch level has proper lounge bays and the clear door approaches.
p.rect(13.5,3,4,8,C['route']);p.rect(26.5,3,4,8,C['route'])
p.group(1,4,11,6,'LOUNGE 01',0)
p.group(32,4,10,6,'LOUNGE 02',2)
p.plant(19,4,5,2);p.text(21.5,8.3,'OPEN',15,700,C['muted'],'middle');p.text(21.5,9.2,'LANDING',15,700,C['muted'],'middle')
# Wide terrace stair with space for a parallel step-free path; no code claim.
p.rect(0,11,38,3,'#E3D8C4',C['muted'],1)
for yy in [11.55,12.1,12.65,13.2]:p.line(0,yy,38,yy,'#B7AA90',1.2)
p.text(19,12.98,'BROAD TERRACE STEPS',17,700,C['muted'],'middle');p.rect(44,3,3,11,'#ECE3D1',C['muted'],1);p.route([(45.5,13.3),(45.5,10.4)],2.4);p.text(45.5,11.95,'RAMP',13,700,C['muted'],'middle')
# East pavilion with service porch. It has its own east/south access, not on a door axis.
p.rect(47,3,16,11,C['coffee_lite'],'#BA936C',2,r=5);p.text(47.6,4.22,'COFFEE PAVILION',20,700)
p.rect(56,5.5,5.5,1.25,C['coffee'],C['ink'],1,r=3);p.text(58.75,6.4,'COUNTER',13,700,C['white'],'middle');p.rect(56,7.2,5.5,3.5,'#F8EDDD','#BD9167',1,dash='5 5');p.text(58.75,8.9,'QUEUE',16,700,C['coffee'],'middle');p.text(58.75,9.8,'3.5-tile apron',14,fill=C['coffee'],anchor='middle')
p.table(51,8.8,.75)
for xx,yy,ang in [(51,7,0),(52.8,8.8,90),(51,10.6,180),(49.2,8.8,-90)]:p.chair(xx,yy,ang)
p.text(51,12.55,'4 café seats',16,fill=C['muted'],anchor='middle');p.plant(61.5,11.5,.65,1.5)
# Lower east wing: garden-facing quiet staying pockets, separately from the promenade.
p.group(52,23.2,11,7,'GARDEN LOUNGE',1)
p.group(52,31.2,11,7,'GARDEN LOUNGE',2)
# Canopy outline expresses coverage, with columns kept out of main walk.
p.rect(.4,3.5,43.2,7.2,'none',C['muted'],1.4,dash='7 6');p.rect(46.5,3.5,17,36.2,'none',C['muted'],1.4,dash='7 6')
for xx,yy in [(46.9,3.8),(63.1,3.8),(63.1,13.1),(63.1,23),(63.1,39.2),(47,39.2)]:p.rect(xx-.18,yy-.18,.36,.36,C['ink'])
# Garden connection: paths open through the full landscape, not a detached water island.
s.path('M '+ ' L '.join(f'{a},{b}' for a,b in [p.xy(12,41),p.xy(12,26),p.xy(20,21)]),fill='none',stroke='#E7DFCB',sw=4*g)
p.route([(12,39),(12,26),(20,21)],2.5)
p.plant(3,26,5,1.5);p.plant(29,27.5,8,1.5);p.plant(2,37,4,1.1);p.plant(29,37,7,1.1);p.plant(39,24.5,3,1.2)
p.text(26,32.65,'CONTINUOUS GARDEN',24,700,C['muted'],'middle');p.text(26,34.1,'Paths can continue west and south.',18,fill=C['muted'],anchor='middle')
# Main 8-tile circulation arrows and arrivals.
p.route([(3,18),(23,18),(28.5,15.3)],3,False);p.route([(28.5,15.3),(28.5,3.35)],3);p.route([(15.5,18),(15.5,3.35)],3);p.route([(49,38.3),(49,18),(37,18)],3,False)
p.text(30,20.8,'8-TILE-WIDE PROMENADE',22,700,C['blue'],'middle');p.text(49,41.15,'SECOND ARRIVAL',17,700,C['blue'],'middle')
for xx,yy,rot in [(15.5,6.4,0),(28.5,8.2,0),(17.5,18.2,90),(34.5,18.2,90),(49,26,0),(58,8,0)]:p.person(xx,yy,rot)
# Promenade dimension; garden paths are intentionally open-ended.
dimension(s,x-24,fy+14*g,x-24,fy+22*g,'8 tiles clear',True)
s.text(x,fy+41*g+46,'Covered terraces + offset pavilion + garden commons. The dashed perimeter marks proposed canopy coverage.',18,fill=C['muted'])
inset_and_cards(s,which='B')
sp=Plan(s,1370,1044,20);sp.person(.5,.5);s.multiline(1411,1054,['Avatar guide at plan scale','1 tile = 32 native pixels'],17,25,fill=C['muted'])
bottom(s,1280,'Drawing scale: 20 px per native 32 px tile (62.5%). Hall rear strip uses exactly the same scale.','More exterior depth and a larger overall site; façade and room-transition design comes later.','B');s.save('option-b-covered-garden-forecourt')

# Audit-friendly metadata and notes: these are review diagrams, never runtime assets.
manifest={'status':'schematic layout choice only; pending user visual approval','source_context':{'path':str(SRC),'original_size':[1536,1280],'unchanged_full_hall_crop_xyxy':list(CROPS['unchanged-auditorium-context']),'unchanged_rear_crop_xyxy':list(CROPS['unchanged-rear-hall-context']),'reason_for_crop_end':'The mirror crowns intrude below y944. The y944..1007 threshold is shown schematically, not as altered original pixels.','preservation':'Original image and map files were not edited. Stage, 210-seat geometry, and both actual door x-ranges remain unchanged.'},'door_native_x_ranges':[[512,608],[928,1024]],'native_grid_px':32,'A':{'drawing_px_per_tile':28,'interior_width_tiles':44,'interior_depth_tiles':22,'approach_width_tiles':4,'cross_concourse_width_tiles':4,'visual_social_seats':20},'B':{'drawing_px_per_tile':20,'overall_schematic_width_tiles':64,'overall_schematic_depth_tiles':40,'promenade_width_tiles':8,'visual_social_seats':20},'runtime_changes':False,'published':False}
(P/'layout-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('\n'.join(str(P/name) for name in ['option-a-deep-indoor-concourse.png','option-b-covered-garden-forecourt.png','layout-manifest.json']))
