"""Authored native32 art assembly. Original v01 and v02 inputs are read-only.
No runtime generation, external publication, or activation is performed.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import json, hashlib, math, shutil
R=Path(__file__).resolve().parents[1]; V1=R/'source/reuse-inputs/v01'; V2=R/'source/reuse-inputs/v02'; W,H=2560,1920
S=R/'source'; A=R/'assets'; Q=R/'review'
for p in [S,A,Q]:p.mkdir(exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda s:ImageFont.truetype(F,s); b=lambda s:ImageFont.truetype(B,s)
assets={}; crop_records=[]
def cut(name,src,box,size=None):
 im=Image.open(src).convert('RGBA').crop(box); ab=im.getchannel('A').point(lambda p: 255 if p>8 else 0).getbbox(); im=im.crop(ab) if ab else im
 if size:im=im.resize(size,Image.Resampling.LANCZOS)
 im.save(A/(name+'.png'));assets[name]=im
 crop_records.append({'asset':name,'source':str(src.relative_to(R)) if src.is_relative_to(R) else str(src),'cropXYXY':list(box),'alphaTrimXYXY':list(ab) if ab else None,'nativeSize':list(im.size),'resampling':'Lanczos only at component-authoring stage; no rotation'})
 return im
def rgba(x):return Image.open(x).convert('RGBA')
# Reconstruct exact original runtime base and above independently, not flattened preview.
m=json.loads((V1/'map32/grand-auditorium.tmj').read_text()); sets=[(t,rgba(V1/'map32'/t['image'])) for t in m['tilesets']]
def render_old(n):
 im=Image.new('RGBA',(1536,1280));l=next(l for l in m['layers'] if l['name']==n)
 for i,gid in enumerate(l['data']):
  if not gid:continue
  t,a=next((t,a) for t,a in reversed(sets) if t['firstgid']<=gid);v=gid-t['firstgid'];sx=v%t['columns']*32;sy=v//t['columns']*32
  im.alpha_composite(a.crop((sx,sy,sx+32,sy+32)),(i%m['width']*32,i//m['width']*32))
 return im
oldbase=render_old('hall-base');oldabove=render_old('hall-above'); old=oldbase.copy();old.alpha_composite(oldabove)
oldbase.save(S/'v01-runtime-base.png');oldabove.save(S/'v01-runtime-above.png')
shutil.copy2(V1/'assets/greg-reference.png',A/'greg-reference.png');greg=rgba(A/'greg-reference.png');frames={}
for n,fr in [('south',1),('north',10),('west',4),('east',7)]:
 frames[n]=greg.crop((fr%3*32,fr//3*32,fr%3*32+32,fr//3*32+32));frames[n].save(A/('greg-'+n+'-review-only.png'))
# Four newly generated perspective directions, no 2D rotation.
master=S/'lounge-four-directions-master.png'; im=rgba(master);mw,mh=im.size
for n,box,size in [('south',(0,0,mw//2,mh//2),(48,48)),('north',(mw//2,0,mw,mh//2),(48,44)),('east',(0,mh//2,mw//2,mh),(42,50)),('west',(mw//2,mh//2,mw,mh),(42,50))]:cut('lounge-chair-'+n,master,box,size)
cut('rug-wide',S/'rugs-master.png',(0,0,1100,887),(352,224));cut('rug-square',S/'rugs-master.png',(1100,0,1774,887),(224,224))
cut('planter-low',S/'environment-props-master.png',(0,0,843,796),(120,48));cut('citrus-tree',S/'environment-props-master.png',(843,0,1277,796),(64,90));cut('welcome-desk',S/'environment-props-master.png',(1277,0,1975,796),(112,68))
for n in ['coffee-counter-native','lounge-table-native','bistro-stool-left-native','bistro-stool-right-native','bistro-table-native']:
 shutil.copy2(V2/'assets'/(n+'.png'),A/(n+'.png'));assets[n]=rgba(A/(n+'.png'))
cut('low-lounge-table',S/'low-table-east-rail-master.png',(0,0,920,1141),(64,36));cut('terrace-east-rail',S/'low-table-east-rail-master.png',(920,0,1379,1141),(44,352))
cut('terrace-rail',S/'terrace-architecture-master.png',(0,0,1536,420),(352,48));cut('coffee-pergola',S/'terrace-architecture-master.png',(0,420,1536,1024),(448,136))
# Authored reusable architecture/material cutouts, exact original project art.
for n,box in [('sandstone-tile',(258,1009,322,1073)),('wall-left',(40,336,96,536)),('wall-right',(1440,336,1496,536)),('wall-horizontal',(260,1174,516,1230)),('threshold-panel',(258,944,448,1008)),('gold-post',(626,1136,688,1266)),('wood-deck-tile',(640,220,832,252))]:
 cut(n,V1/'review/flagship-empty-native.png',box)
# The plant/rug/table layers remain independent from architecture.
arch=Image.new('RGBA',(W,H));garden=rgba(S/'garden-view-master.png').resize((W,H),Image.Resampling.LANCZOS);arch.alpha_composite(garden)
def tile(dst,src,rect):
 x0,y0,x1,y1=rect
 for y in range(y0,y1,src.height):
  for x in range(x0,x1,src.width):dst.alpha_composite(src.crop((0,0,min(src.width,x1-x),min(src.height,y1-y))),(x,y))
def line(rect,color,width=1):ImageDraw.Draw(arch).rectangle(rect,outline=color,width=width)
# Terrace is clearly timber, visually distinct from the indoor sandstone.
tile(arch,assets['wood-deck-tile'],(1504,1088,2496,1744)); d=ImageDraw.Draw(arch)
for y in range(1088,1745,32):d.line((1504,y,2496,y),fill='#684825',width=1);d.line((1504,y+1,2496,y+1),fill='#c18b49',width=1)
for row,y in enumerate(range(1088,1744,32)):
 for x in range(1504+(row%2)*96,2496,192):d.line((x,y,x,y+30),fill='#886137',width=1)
# Sandstone foyer and the broad south entry path.
tile(arch,assets['sandstone-tile'],(64,944,1472,1776)); tile(arch,assets['sandstone-tile'],(640,1776,896,1920));d=ImageDraw.Draw(arch)
for y in range(1008,1713,64):d.line((64,y,1472,y),fill=(165,125,73,110),width=1)
for x in range(64,1473,64):d.line((x,1008,x,1712),fill=(165,125,73,100),width=1)
# Decorative floor inlay communicates the unfurnished connected routes without floor labels.
for x0,x1 in [(496,624),(912,1040)]:
 for x in [x0,x1]:d.line((x,1008,x,1312),fill='#b99559',width=2);d.line((x+4,1008,x+4,1312),fill='#e9ca8a',width=1)
for y in [1312,1440]:d.line((96,y,1472,y),fill='#b99559',width=2);d.line((96,y+4,1472,y+4),fill='#e9ca8a',width=1)
for x in [640,896]:d.line((x,1440,x,1920),fill='#b99559',width=2);d.line((x+4,1440,x+4,1920),fill='#e9ca8a',width=1)
# Extend the room boundary outward by one native tile below the preserved hall.
tile(arch,assets['wall-left'],(8,944,64,1776));tile(arch,assets['wall-right'],(1472,944,1528,1312));tile(arch,assets['wall-right'],(1472,1472,1528,1776))
tile(arch,assets['wall-horizontal'],(64,1712,640,1768));tile(arch,assets['wall-horizontal'],(896,1712,1472,1768))
# Exact old hall depth layers remain unchanged through y944. Rear threshold is rebuilt below.
arch.alpha_composite(oldbase.crop((0,0,1536,944)),(0,0)); original_fg=Image.new('RGBA',(W,H));original_fg.alpha_composite(oldabove.crop((0,0,1536,944)),(0,0))
threshold=oldbase.crop((0,944,1536,1008)); arch.alpha_composite(threshold,(0,944))
# Both mirror crowns begin in this rebuilt band: replace their full x-spans with ordinary paneling.
for xa,xb in [(96,256),(1280,1440)]:tile(arch,assets['threshold-panel'],(xa,944,xb,1008))
# Finish new east-facing opening with stepped stone jambs; no fake destination object.
tile(arch,assets['sandstone-tile'],(1472,1312,1536,1472))
d=ImageDraw.Draw(arch)
for y in [1296,1472]:
 d.rectangle((1464,y,1535,y+15),fill='#b27c38',outline='#684722',width=2);d.rectangle((1468,y+2,1531,y+9),fill='#edcc85')
d.rectangle((1472,1312,1535,1471),outline='#b8945d',width=1)
# Broad main entrance uses the familiar gold-lit posts, positioned outside the clear opening.
arch.alpha_composite(assets['gold-post'],(578,1662));arch.alpha_composite(ImageOps.mirror(assets['gold-post']),(896,1662))
# Low terrace balustrade, with discrete posts. Scenery beyond is visibly separated.
def hrail(x0,x1,y):
 dd=ImageDraw.Draw(arch);dd.rectangle((x0,y+10,x1,y+37),fill='#725332')
 for x in range(x0+12,x1,32):dd.rectangle((x,y+8,x+6,y+35),fill='#d9b973');dd.line((x+1,y+10,x+1,y+33),fill='#f1d79b',width=2)
 dd.rectangle((x0,y,x1,y+7),fill='#f0d3a0',outline='#9e7744',width=2);dd.rectangle((x0,y+36,x1,y+42),fill='#b38b50',outline='#795932',width=1)
 for x in range(x0,x1,192):dd.rectangle((x-4,y-7,x+17,y+42),fill='#d8b574',outline='#97713d',width=2);dd.rectangle((x-7,y-10,x+20,y-2),fill='#f1d79b',outline='#a77d42',width=1)
tile(arch,assets['terrace-rail'],(1536,1040,2496,1088));tile(arch,assets['terrace-rail'],(1536,1712,2496,1760))
arch.alpha_composite(assets['terrace-east-rail'],(2460,1056));arch.alpha_composite(assets['terrace-east-rail'],(2460,1392))
# A small cutaway pergola establishes the sheltered coffee area without hiding queue/actors.
shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow)
for x in range(1704,2113,48):sd.polygon([(x,1116),(x+10,1116),(x+54,1288),(x+44,1288)],fill=(63,49,25,18))
arch.alpha_composite(shadow); d=ImageDraw.Draw(arch)
arch.alpha_composite(assets['coffee-pergola'],(1696,1088))
# Small physical signs, not large labels on occupied rugs/floors.
def sign(x,y,text,w=108):
 dd=ImageDraw.Draw(arch);dd.rounded_rectangle((x,y,x+w,y+23),radius=3,fill='#164249',outline='#d2a14f',width=2);bb=dd.textbbox((0,0),text,font=b(10));dd.text((x+(w-(bb[2]-bb[0]))/2,y+5),text,font=b(10),fill='#f5e0b5')
sign(1348,1019,'TERRACE  →',108);sign(684,982,'FOYER',168)
# Layered furniture and rugs, all component placements retained for later collision compilation.
rugs=Image.new('RGBA',(W,H)); furnishings=Image.new('RGBA',(W,H)); fg=original_fg.copy(); placements=[];anchors=[];groups=[]
def place(id,n,x,y,front=None):
 im=assets[n]; furnishings.alpha_composite(im,(x,y));placements.append({'id':id,'asset':'assets/'+n+'.png','x':x,'y':y,'width':im.width,'height':im.height,'foregroundFromLocalY':front})
 if front is not None:
  fg.alpha_composite(im.crop((0,front,im.width,im.height)),(x,y+front))
 return im
# Chairs are given actual inward-looking variants and approach gaps around tables.
centers=[('lounge-01',(96,1072,448,1296),(272,1184)),('lounge-02',(640,1072,864,1296),(752,1184)),('lounge-03',(1120,1072,1440,1296),(1280,1184)),('lounge-04',(96,1456,448,1680),(272,1568))]
for i,(gid,rect,(cx,cy)) in enumerate(centers):
 x0,y0,x1,y1=rect; rug=assets['rug-square'] if x1-x0==224 else assets['rug-wide'].resize((x1-x0,y1-y0),Image.Resampling.LANCZOS);rugs.alpha_composite(rug,(x0,y0))
 group={'id':gid,'bounds':list(rect),'type':'visual meeting-room candidate only','seats':[]};groups.append(group)
 # North seat faces south; south seat faces north. Side seats face into their table.
 poses=[('N','south',cx-24,cy-87,cx,cy-59,39),('S','north',cx-24,cy+39,cx,cy+55,25),('W','east',cx-87,cy-27,cx-62,cy-2,41),('E','west',cx+45,cy-27,cx+62,cy-2,41)]
 if gid=='lounge-02':poses=[(a,n,x+(6 if a=='W' else -6 if a=='E' else 0),y,ax+(6 if a=='W' else -6 if a=='E' else 0),ay,fr) for a,n,x,y,ax,ay,fr in poses]
 for a,n,x,y,ax,ay,fr in poses:
  sid=gid+'-'+a;place(sid,'lounge-chair-'+n,x,y,fr);anchor={'id':sid,'x':ax,'y':ay,'direction':n,'floorClick':[ax,ay+16],'group':gid};anchors.append(anchor);group['seats'].append(sid)
 table=assets['low-lounge-table'];place(gid+'-table','low-lounge-table',cx-table.width//2,cy-16,table.height-8)
 # Low edge planter defines the bay without closing the entry toward the concourse.
 if gid!='lounge-02':place(gid+'-planter','planter-low',x0+20,y0-24,None)
# Arrival assistance is off the central arrival route, with customer room in front.
place('welcome','welcome-desk',484,1564,58); sign(486,1541,'WELCOME',108)
# Coffee has separate counter and customer apron north of the route, no bay floor labels.
place('coffee','coffee-counter-native',1836,1112,None)
for pid,x,y in [('coffee-tree-left',1628,1106),('coffee-tree-right',2376,1106),('terrace-tree-southwest',1552,1588),('terrace-tree-southeast',2396,1588),('foyer-tree-south',1380,1594)]:place(pid,'citrus-tree',x,y,None)
# Four close casual pairs, outside meeting rugs and quiet circulation.
pairs=[]
for pid,cx,cy in [('indoor-casual',1248,1584),('terrace-view-pair',2240,1196),('terrace-lower-pair',1760,1600),('terrace-garden-pair',2208,1600)]:
 pair_anchors=[]
 # Resting centers are56px apart, beneath64px source proximity start default.
 for side,dx,n in [('left',-28,'bistro-stool-left-native'),('right',28,'bistro-stool-right-native')]:
  im=assets[n];x=cx+dx-im.width//2;y=cy-30;sid=pid+'-'+side;place(sid,n,x,y,im.height-8);an={'id':sid,'x':cx+dx,'y':cy,'direction':'south','floorClick':[cx+dx,cy+16],'pair':pid};anchors.append(an);pair_anchors.append(sid)
 im=assets['bistro-table-native'];place(pid+'-table','bistro-table-native',cx-im.width//2,cy-30,im.height-8)
 pairs.append({'id':pid,'anchors':pair_anchors,'center':[cx,cy],'anchorDistancePx':56,'function':'ordinary proximity candidate; deployed distances unknown'})
# Plant accents stay out of four hall/terrace movement paths.
for pid,x,y in [('east-bay-edge',1296,1454),('terrace-south-edge',1984,1680),('west-entry-edge',128,1664)]:place(pid,'planter-low',x,y,None)
# Save separate source layers. Remove above strips from base so every pixel has one layer owner.
architecture=arch.copy();architecture.save(S/'architecture-native.png');rugs.save(S/'rugs-native.png');furnishings.save(S/'furniture-native.png')
base=arch.copy();base.alpha_composite(rugs);base.alpha_composite(furnishings)
# Foreground pixel source replacement is transparent in base, exact empty-scene union restored below.
# Full furniture remains in base intentionally for review; handoff supplies strips and parent will compile exact ownership.
base.save(A/'hall-base.png');fg.save(A/'hall-above.png');fg.save(S/'foreground-native.png')
empty=base.copy();empty.alpha_composite(fg);empty.save(Q/'flagship-v03-empty-native.png')
occupied=base.copy()
oldseats=json.loads((V1/'source/seats.json').read_text())
for i,s in enumerate(oldseats):
 if (i*7)%17<10:occupied.alpha_composite(frames['north'],(s['x']-16,s['y']-16))
review_actors=[]
for i,a in enumerate(anchors):
 if a.get('group') and ((i%4)==3):continue
 occupied.alpha_composite(frames[a['direction']],(a['x']-16,a['y']-16));review_actors.append(a)
for aid,x,y,n in [('stage-speaker',768,264,'south'),('hall-west',560,924,'north'),('hall-east',976,1032,'south'),('arrival',768,1672,'north'),('cross-concourse',768,1376,'east'),('terrace-door',1504,1392,'east'),('coffee-customer-1',1876,1240,'north'),('coffee-customer-2',1924,1288,'north'),('welcome-customer',540,1654,'north'),('terrace-walk',2020,1392,'west'),('view-watcher',2312,1108,'north')]:
 occupied.alpha_composite(frames[n],(x-16,y-16));review_actors.append({'id':aid,'x':x,'y':y,'direction':n})
occupied.alpha_composite(fg);occupied.save(Q/'flagship-v03-occupied-native.png')
# Complete native-scale views: no enlarged avatars, no missing foreground.
occupied.crop((0,928,2560,1856)).save(Q/'foyer-terrace-occupied-native.png');empty.crop((0,928,2560,1856)).save(Q/'foyer-terrace-empty-native.png')
occupied.crop((32,944,1536,1792)).save(Q/'indoor-foyer-occupied-native.png');occupied.crop((1408,992,2560,1792)).save(Q/'terrace-occupied-native.png')
occupied.crop((64,1024,480,1344)).save(Q/'lounge-group-occupied-native.png');occupied.crop((1376,1248,1696,1536)).save(Q/'terrace-door-occupied-native.png')
# Curated overview, artwork remains clean; presentation labels live outside art.
card=Image.new('RGB',(1920,1700),'#102e34');cd=ImageDraw.Draw(card)
cd.text((48,26),'FLAGSHIP 03',font=b(18),fill='#caa263');cd.text((48,60),'A grand foyer. A garden-side coffee terrace.',font=b(34),fill='#f5e5c3')
cd.text((48,112),'One continuous map  ·  Four bounded indoor lounge groups  ·  Clear arrival and hall approaches',font=f(18),fill='#c4d1ce')
thumb=occupied.resize((1792,1344),Image.Resampling.LANCZOS);card.paste(thumb,(64,162))
notes=[('01  HALL PRESERVED','Original giant stage and all210 chairs'),('02  ROOM TO GATHER','44×22-tile foyer with four defined rugs'),('03  A REAL RIGHT-SIDE EXIT','Continuous timber terrace and garden view'),('04  COFFEE OFF THE ROUTE','Counter apron and four casual seat pairs')]
for i,(h,t) in enumerate(notes):x=64+(i%2)*900;y=1540+(i//2)*64;cd.text((x,y),h,font=b(16),fill='#e0bd79');cd.text((x,y+25),t,font=f(15),fill='#dae3db')
cd.text((64,1672),'ART REVIEW ONLY  ·  Native32 world / unchanged32px Greg fixture  ·  Media configuration and live join remain unverified',font=f(13),fill='#9fb6b6');card.save(Q/'flagship-v03-overview.png')
# Analytical route/zone overlay is separate from polished art.
plan=empty.copy();ol=Image.new('RGBA',(W,H));od=ImageDraw.Draw(ol)
quiet=[{'id':'west-hall-approach','bounds':[512,1008,608,1344]},{'id':'east-hall-approach','bounds':[928,1008,1024,1344]},{'id':'cross-concourse','bounds':[512,1344,1536,1440]},{'id':'arrival','bounds':[672,1440,864,1920]}]
for r in quiet:od.rectangle(r['bounds'],fill=(97,217,234,45),outline=(70,191,208,225),width=3)
for g in groups:od.rectangle(g['bounds'],fill=(35,138,117,35),outline=(140,237,197,220),width=3)
od.rectangle((1760,1216,2112,1312),fill=(251,164,63,35),outline=(255,177,75,230),width=3)
for a in anchors:od.ellipse((a['x']-5,a['y']-5,a['x']+5,a['y']+5),fill=(255,255,255,220))
plan.alpha_composite(ol);plan.crop((0,928,2560,1856)).save(Q/'layout-review-overlay-native.png')
layout={'status':'art review checkpoint; not a compiled map','tileSize':32,'worldPixels':[W,H],'worldTiles':[W//32,H//32],'preservedHallXYXY':[0,0,1536,944],'foyerInterior':[64,1008,1472,1712],'foyerInteriorTiles':[44,22],'hallDoors':[[512,944,608,1008],[928,944,1024,1008]],'terraceDoor':[1472,1312,1536,1472],'mainArrivalOpening':[640,1712,896,1776],'terraceInterior':[1536,1088,2464,1712],'groupBays':groups,'quietRouteCandidates':quiet,'coffeeCounterBounds':[1836,1112,2004,1206],'coffeeCustomerApron':[1760,1216,2112,1312],'coffeeStaffAllowance':[1808,1088,2048,1112],'informalPairs':pairs,'furniture':placements,'socialAnchors':anchors,'reviewActors':review_actors,'depthIntent':'Retain original base/above through y944 exactly. New chairs use separate lower-apron/back strips; actor head overlap and live local/remote depth remain to be verified before publication. Review foreground duplicated over complete furniture union; parent should make exact runtime layer ownership when compiling.','zonesNote':'Visual rugs only; future unique livekitRoomProperty per rug requires user native-editor setup. Quiet-route candidates are intentionally separate. No media provider activated.','noMirrorPixelsBelowThreshold':True,'sourceMeetingDistanceDefaults':{'startPx':64,'groupRadiusPx':48,'deployedOverrides':'unknown'}}
(S/'art-layout.json').write_text(json.dumps(layout,indent=2));(S/'component-crops.json').write_text(json.dumps(crop_records,indent=2))
# Verify invariants in pixel space.
a=empty.crop((0,0,1536,944));o=old.crop((0,0,1536,944));assert a.tobytes()==o.tobytes(), 'Preserved hall pixels drifted'
checks={'nativePixels':[W,H],'hallPixelsAboveY944ByteEqual':True,'audienceChairRecords':len(oldseats),'gregSHA256':hashlib.sha256((A/'greg-reference.png').read_bytes()).hexdigest(),'foyerDepthTiles':22,'groupBays':4,'groupSeats':16,'casualPairs':4,'casualAnchorDistancesPx':[56]*4,'compiled':False,'published':False,'imagegenMasters':['lounge-four-directions-master.png','rugs-master.png','environment-props-master.png','garden-view-master.png','terrace-architecture-master.png','low-table-east-rail-master.png']}
(S/'art-verification.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
