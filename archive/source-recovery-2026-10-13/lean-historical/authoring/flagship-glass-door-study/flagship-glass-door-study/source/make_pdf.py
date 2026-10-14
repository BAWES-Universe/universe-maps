from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor as C
from reportlab.lib.utils import ImageReader
from pathlib import Path
R=Path(__file__).resolve().parents[1]; out=R/'output/pdf/flagship-glass-design-study.pdf'
c=canvas.Canvas(str(out),pagesize=(842,595));c.setTitle('Flagship | Glass foyer and arrival study')
BG='#102B31';TEXT='#F4EAD7';GOLD='#D9B86F';MUTED='#A9C3BD';GLASS='#467C80'
def rect(x,y,w,h,color,stroke=None):
 c.setFillColor(C(color));c.setStrokeColor(C(stroke or color));c.rect(x,y,w,h,fill=1,stroke=bool(stroke))
def text(x,y,t,size=10,color=TEXT,font='Helvetica'):
 c.setFillColor(C(color));c.setFont(font,size);c.drawString(x,y,t)
def lines(x,y,arr,size=11,leading=17,col=TEXT):
 for t in arr:text(x,y,t,size,col);y-=leading
 return y
def start(n,title,sub):
 rect(0,0,842,595,BG);text(34,558,'FLAGSHIP  /  ARCHITECTURE STUDY',10,GOLD,'Helvetica-Bold');text(34,524,title,26,TEXT,'Helvetica-Bold');text(34,501,sub,10,MUTED);text(34,22,'11 OCT 2026  |  DESIGN REVIEW ONLY  |  No existing map changed or published',8,MUTED);text(790,22,str(n),10,GOLD)
def image(p,x,y,w,h):c.drawImage(str(p),x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
start(1,'One connected foyer, terrace and arrival','CONCEPT  |  A spatial plan for review, not an implemented Flagship redesign')
# schematic generous overall diagram left
rect(34,79,480,397,'#183A3F');rect(65,355,270,89,'#294B4D',GOLD);text(84,410,'APPROVED STAGE',14,GOLD,'Helvetica-Bold');lines(84,390,['Retain stage; keep hall geometry out of this study.','Do not broaden the redesign into this zone.'],9,14)
rect(65,218,270,126,'#DED4B9');text(84,323,'DOUBLE-HEIGHT GLASS FOYER',12,BG,'Helvetica-Bold')
# central spine
rect(183,218,56,89,'#F4EAD7');text(188,266,'CLEAR',8,BG);text(189,253,'SPINE',8,BG)
# reception and social
rect(84,283,65,18,'#587A72',GOLD);text(85,270,'Reception',8,BG)
for x,y in [(94,239),(282,283),(282,243)]:
 c.setFillColor(C('#5D7B71'));c.circle(x,y,10,fill=1,stroke=0)
 c.setStrokeColor(C('#A48B56'));c.circle(x,y,17,fill=0,stroke=1)
text(251,310,'Lounge bays',8,BG)
rect(347,218,130,126,'#638079');text(360,323,'TERRACE',12,TEXT,'Helvetica-Bold');lines(359,302,['Same stone + brass','Low glass balustrade','Garden-edge seating'],9,14)
# direct glass link
rect(331,262,20,33,'#B4D6CF');text(361,239,'Open sightline',8,TEXT)
rect(185,91,52,124,'#C8B794');rect(65,91,112,111,'#315B4F');rect(246,91,231,111,'#315B4F');text(266,159,'LOW PLANTING',11,MUTED,'Helvetica-Bold');lines(266,141,['Continuous garden edge','Clear path to foyer and terrace'],9,14)
rect(175,203,72,14,GOLD);text(90,185,'KEEP LIKED PORTAL',9,GOLD,'Helvetica-Bold');text(188,117,'ARRIVAL',8,BG)
# connector arrows
c.setStrokeColor(C('#E9DCA9'));c.setLineWidth(2);c.line(218,149,218,245);c.line(302,255,357,255)
lines(548,449,['A quieter, taller silhouette'],17,23,GOLD)
lines(548,415,['1  Keep the approved stage untouched.','2  Keep the liked exterior entrance.','3  Align the foyer with its arrival axis.','4  Extend materials onto the terrace.','5  Place social bays beside the route,','    with no furniture in the door run.'],11,23)
lines(548,243,['Height without disappearing'],17,23,GOLD)
lines(548,210,['Keep rear glazing, columns and a thin','upper cornice permanently visible.','Only a genuine view-blocking roof strip','may cut away on entry. Do not hide','the entire building front or silhouette.'],11,18)
text(548,89,'Schematic proportions; native32 layout follows review.',8,MUTED)
c.showPage()
start(2,'Keep the portal. Add light and height.','CONCEPT  |  Transparent architecture with warm stone, brass and restrained teal')
image(R/'source/references/preserved-entrance.png',34,261,370,216)
text(34,246,'EXISTING ENTRANCE TO PRESERVE',10,GOLD,'Helvetica-Bold');text(34,230,'Reference from v09. This study does not replace its artwork.',9,MUTED)
image(R/'source/references/preserved-stage.png',34,89,370,124)
text(34,76,'APPROVED STAGE: unchanged',9,GOLD,'Helvetica-Bold')
# original diagram elevation right
rect(438,263,370,213,'#25464A')
for i in range(6):
 x=454+i*55;rect(x,308,51,136,GLASS,GOLD);c.setStrokeColor(C('#98C4BD'));c.line(x+7,430,x+40,322);c.setStrokeColor(C(GOLD));c.line(x,375,x+51,375)
rect(448,444,346,7,GOLD);rect(448,301,346,7,GOLD)
# retain abstract portal silhouette, label not exact graphic
rect(563,290,114,73,'#C7B382',GOLD);rect(586,290,69,57,'#173138');text(590,315,'RETAIN',10,GOLD,'Helvetica-Bold');text(590,301,'PORTAL',10,GOLD,'Helvetica-Bold')
text(449,463,'DOUBLE-HEIGHT GLAZING / PERMANENT FRAME',9,TEXT,'Helvetica-Bold')
text(438,246,'ILLUSTRATIVE ELEVATION, NOT FINAL GAME ART',9,GOLD,'Helvetica-Bold')
lines(438,219,['- Tall rear glass establishes height outside and inside.','- Sparse reflections keep the world readable through it.','- Ground-floor glass stays below avatar drawing depth.','- Opaque columns stay beside walkable space.','- The terrace repeats the foyer floor and planter rhythm.'],11,20)
for i,col in enumerate(['#E4D8BE','#D9B86F','#467C80','#638079']):rect(440+i*91,76,76,24,col)
for i,label in enumerate(['Warm stone','Brass frame','Blue-green glass','Soft planting']):text(440+i*91,61,label,8,MUTED)
c.showPage()
start(3,'A small working door study, with a clear limit','IMPLEMENTED FIXTURE  |  Native 32px tiles + map-only script; no new engine behavior')
image(R/'renders/fixture-closed.png',34,235,370,238);image(R/'renders/fixture-open.png',438,235,370,238)
text(34,226,'CLOSED: glass leaves + collidable threshold',10,GOLD,'Helvetica-Bold');text(438,226,'OPEN: leaves parked aside; tall frame remains',10,GOLD,'Helvetica-Bold')
text(34,208,'Decoded tilemap compositions. These are not live browser screenshots.',9,MUTED)
lines(34,181,['53 source-executed cases on pinned fork 60e7afd','Repeated approaches, retreats and crossings from both sides;','native touch pathfinding and collision visibility; no art above avatar depth.'],11,17)
lines(438,181,['2 explicit single-tap limitations, reproduced','A tap across a closed door from beyond its trigger cannot route.','Tap the approach first, then cross. Seamless far-tap is not proven.'],11,17,GOLD)
lines(34,115,['The fixture is intentionally simple test art, separate from the final visual design.','Multi-user occupancy, authenticated gameplay and live deployment compatibility still need acceptance.'],10,16)
text(34,66,'Sources: official door properties  |  closing-doors tutorial  |  official starter conference.tmj',8,MUTED)
links=[('https://docs.workadventu.re/map-building/tiled-editor/extra-features/doors/',(74,61,240,74)),('https://docs.workadventu.re/blog/closing-doors/',(249,61,403,74)),('https://github.com/workadventure/map-starter-kit/blob/master/conference.tmj',(415,61,640,74))]
for url,box in links:c.linkURL(url,box,relative=0)
c.save();print(out)
