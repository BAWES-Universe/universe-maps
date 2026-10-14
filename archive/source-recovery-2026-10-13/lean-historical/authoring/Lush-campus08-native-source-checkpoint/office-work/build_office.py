from PIL import Image, ImageDraw
from pathlib import Path
import json, hashlib, math
import numpy as np
R=Path(__file__).resolve().parent
S=Path('/workspace/shared/recovered-pre-island-package/sources/office')
G=json.loads((S/'source-coordinate-geometry.json').read_text())
W,H=1536,960
names=['floor','environment','rugs','objects','foreground','glass','overhead-shade']
src={n:Image.open(S/f'office-v4-{n}.png').convert('RGBA') for n in names}
L={n:Image.new('RGBA',(W,H)) for n in names}
manifest=[]
def cp(n,box,dest,desc):
 x,y,w,h=box;dx,dy=dest
 tile=src[n].crop((x+32,y+32,x+w+32,y+h+32))
 L[n].alpha_composite(tile,(dx+32,dy+32))
 manifest.append({'layer':n,'source':str(S/f'office-v4-{n}.png'),'sourceCrop':[x+32,y+32,x+w+32,y+h+32],'destination':[dx+32,dy+32],'scale':1,'purpose':desc})
def crops(ns,box,dest,desc):
 for n in ns:cp(n,box,dest,desc)
# Exact original sandstone foundation and the two northern work receivers.
cp('floor',(0,0,1024,896),(0,0),'main sandstone foundation')
crops(['environment','glass','overhead-shade'],(0,0,960,640),(0,0),'original two lush work receivers')
crops(['environment','foreground','glass','overhead-shade'],(1920,0,64,640),(960,0),'original east shell at native scale')
crops(['objects','foreground'],(96,176,832,256),(96,176),'exact four native two-person islands and eight chairs')
# Southern foyer uses original west/east shell, inlaid spine, and native floor receivers.
crops(['environment','foreground','glass','overhead-shade'],(0,1088,96,256),(0,640),'foyer west shell')
crops(['environment','foreground','glass','overhead-shade'],(1920,1088,64,256),(960,640),'east shell with open gallery connection')
crops(['environment','glass','overhead-shade'],(928,1088,128,256),(448,640),'continuous central inlaid spine')
crops(['environment','glass','overhead-shade'],(96,1088,352,240),(96,640),'lounge sandstone floor')
# Preserve the grand welcome motif at native size: ornamental ends plus full central flower.
# Only unadorned intermediate floor spans are omitted to fit the compact reception bay.
cp('environment',(1120,1088,64,240),(576,640),'original welcome inlay left ornamental end')
cp('environment',(1280,1088,256,240),(640,640),'original full native welcome flower and central inlay')
cp('environment',(1632,1088,64,240),(896,640),'original welcome inlay right ornamental end')
# Both unobstructed entrance edges use native low fascia, with a128px main gap.
crops(['environment','foreground','glass'],(96,1328,352,16),(96,880),'west entrance fascia')
crops(['environment','foreground','glass'],(1056,1328,384,16),(576,880),'east entrance fascia')
# Move the source cross-lounge128px south so it does not capture desk crosslane walkers.
crops(['rugs','objects','foreground'],(144,464,224,208),(144,592),'one native welcoming lounge, clear of work egress')
# Grand counter is shortened by removing its central160px service span, without scaling.
# Original first and last144px sections retain their original end caps and equipment.
cp('objects',(1136,1200,144,48),(624,736),'reception first native counter end')
cp('objects',(1440,1200,144,48),(768,736),'reception last native counter end')
# Exactly two original staff chairs. No third station survives.
for sx,dx in [(1200,688),(1520,848)]:
 crops(['objects','foreground'],(sx-24,1152,48,48),(dx-24,688),'native reception staff chair')
# Compact conference gallery with a public southern entrance and a main-hall link.
crops(names,(1984,896,448,448),(1024,448),'one conference gallery at source scale')
crops(['environment','foreground','glass','overhead-shade'],(1984,448,448,64),(1024,448),'gallery original north shell cap')
# Native entry pads extend to module boundary for the campus integrator.
cp('floor',(928,1280,128,32),(448,896),'main entry continuation')
cp('environment',(928,1280,128,32),(448,896),'main inlaid entry continuation')
cp('floor',(2016,1280,96,32),(1056,896),'gallery entry continuation')
cp('environment',(2016,1280,96,32),(1056,896),'gallery inlaid entry continuation')
# Correct source low-furniture layer ownership without changing a single flat art pixel.
# These pieces are below head height and otherwise hide heads during a southern approach.
# The sofa arms and all structural foreground remain fixed above actors.
for box,reason in [((208,689,368,720),'sofa low front lip')]:
 tile=L['foreground'].crop(box)
 L['objects'].alpha_composite(tile,(box[0],box[1]))
 L['foreground'].paste((0,0,0,0),box)
 manifest.append({'operation':'fixed-layer-reclassification','from':'foreground','to':'objects','canvasCrop':list(box),'reason':reason,'artPixelsUnchanged':True})
# Pixels below a seated Greg's32px frame are chair feet, not torso occluders.
# Keep the entire visible seated back above the actor, but place the low feet below.
# Combined with the physical rear foot, an approaching head cannot cross the back.
for x,y in [(224,384),(384,384),(704,384),(864,384),(288,768),(1280,704),(1344,704),(1408,704)]:
 box=(x-24,y+16,x+24,y+48)
 tile=L['foreground'].crop(box)
 L['objects'].alpha_composite(tile,(box[0],box[1]))
 L['foreground'].paste((0,0,0,0),box)
 manifest.append({'operation':'fixed-layer-reclassification','from':'foreground','to':'objects','canvasCrop':list(box),'reason':'chair feet below the occupied avatar frame; seated torso back retained above actors','artPixelsUnchanged':True})
# Sources have no floor lettering applied: office-v4-labels is intentionally never read.
for n,im in L.items():im.save(R/f'office-{n}.png')
base=Image.new('RGBA',(W,H))
for n in ['floor','environment','rugs','objects']:base.alpha_composite(L[n])
base.save(R/'office-base.png')
flat=base.copy()
for n in ['foreground','glass','overhead-shade']:flat.alpha_composite(L[n])
flat.save(R/'office-overview.png')
# Geometry is authored in native source pixels, exported with the agreed32px margin.
rects=[]
def rect(i,x,y,w,h,k='permanent-wall'):
 rects.append(dict(id=i,x=x+32,y=y+32,width=w,height=h,kind=k))
rect('north-shell',0,0,1024,176)
rect('west-shell',0,176,96,720)
rect('east-shell-upper',960,176,64,464)
rect('east-shell-lower',960,688,64,208)
rect('south-west-fascia',96,880,352,16)
rect('south-east-fascia',576,880,384,16)
# The exact cabinet and table bounds are retained from the frozen two work receivers.
for q in G['lowDividers']:
 if any(t in q['id'] for t in ['operations','recruitment']):rect(q['id'],q['x'],q['y'],q['width'],q['height'],q['kind'])
for q in G['furnitureCollisionRectangles']:
 if any(t in q['id'] for t in ['operations','recruitment']):rect(q['id'],q['x'],q['y'],q['width'],q['height'],q['kind'])
 if q['id'].startswith('cross-lounge-west'):
  rect(q['id'],q['x'],q['y']+128,q['width'],q['height'],q['kind'])
rect('two-service-reception',624,736,288,32,'reception-counter')
# Painted chair rear feet are permanent blockers behind the16px-high sitting pocket.
# This keeps complete chair backs in fixed foreground and enforces natural lateral entry.
for i,x,y in [('work-left-a',192,352),('work-left-b',352,352),('work-right-a',672,352),('work-right-b',832,352),('lounge-guest',256,736),('meeting-a',1248,672),('meeting-b',1312,672),('meeting-c',1376,672)]:
 rect(i+'-chair-rear-foot',x-16,y+16,32,16,'painted-chair-rear-foot')
# Gallery source collision translated exactly; northern cap is the source wall64px.
rect('gallery-north-shell',1024,448,448,64)
for q in G['allCollisionRectangles']:
 if q['x']>=1984 and q['y']+q['height']>896:
  y=max(q['y'],896);h=q['y']+q['height']-y
  rect(q['id'],q['x']-960,y-448,q['width'],h,q.get('kind','permanent-wall'))
# Conference physical table bounds are present only once.
seen=set();rects=[q for q in rects if not ((key:=(q['x'],q['y'],q['width'],q['height'])) in seen or seen.add(key))]
envelopes=[dict(x=32,y=32,width=1024,height=896),dict(x=1056,y=480,width=448,height=448),dict(x=480,y=928,width=128,height=32),dict(x=1088,y=928,width=96,height=32)]
mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
for q in envelopes:d.rectangle((q['x'],q['y'],q['x']+q['width']-1,q['y']+q['height']-1),fill=255)
for q in rects:d.rectangle((q['x'],q['y'],q['x']+q['width']-1,q['y']+q['height']-1),fill=0)
mask.save(R/'office-walkable.png')
a=np.asarray(mask);blocked=(a.reshape(H//16,16,W//16,16).min((1,3))==0)
Image.fromarray(np.uint8(~blocked)*255).save(R/'office-walkable-grid.png')
grid=dict(cellSize=16,width=W//16,height=H//16,blockedIndices=np.flatnonzero(blocked).tolist(),outsideBlocked=True)
(R/'collision-grid.json').write_text(json.dumps(grid))
goals=[]
def goal(i,x,y,kind,facing='north',**extra):
 goals.append(dict(id=i,x=x+32,y=y+32,kind=kind,facing=facing,**extra))
for q in G['goals']:
 if q['kind']=='team-seat' and any(t in q['id'] for t in ['operations','recruitment']):
  goal(q['id'],q['x'],q['y'],'work-seat',q['facing'],contactDirection=q['contactDirection'],approach={'x':q['approach']['x']+32,'y':q['approach']['y']+32},workSide='left' if 'operations' in q['id'] else 'right')
 if q['id'].startswith('cross-lounge-west'):
  goal(q['id'],q['x'],q['y']+128,q['kind'],q['facing'])
 if q['id'].startswith('conference-') and q['kind']=='meeting-seat':
  goal(q['id'],q['x']-960,q['y']-448,q['kind'],q['facing'],contactDirection=q.get('contactDirection'))
for n,x in [(1,688),(2,848)]:
 goal(f'reception-staff-{n}',x,720,'reception-staff','south',contactDirection='south',station=n)
 goal(f'reception-visitor-{n}',x,768,'reception-visitor','north',contactDirection='north',station=n,intendedPartner=f'reception-staff-{n}')
 goal(f'reception-queue-{n}',x,848,'checkpoint','north',station=n)
for i,x,y,f in [('main-entrance',512,912,'north'),('gallery-public-entrance',1104,912,'north'),('shared-spine',512,560,'north'),('gallery-main-threshold',1008,656,'east'),('gallery-corridor',1104,656,'north'),('conference-threshold',1184,616,'east')]:goal(i,x,y,'checkpoint',f)
# Explicit safe desk egress:80px gap between stationary colleagues, then112px south of last row.
routes=[]
for q in goals:
 if q['kind']=='work-seat':
  cx=304 if q['workSide']=='left' else 784
  points=[[q['x'],q['y']],[cx,q['y']],[cx,496],[544,496],[544,912]]
  routes.append(dict(id=q['id']+'-egress',start=q['id'],points=points,otherPeerMinimumRequired=64,releaseBeyond=96))
# Reception visits approach separately from the south at112px from both visitor anchors.
for n,x in [(1,720),(2,880)]:
 routes.append(dict(id=f'reception-visitor-{n}-approach',start='main-entrance',points=[[544,944],[544,880],[x,880],[x,800]],intendedPartner=f'reception-staff-{n}',otherPeerMinimumRequired=64))
 # Staff use the northern approach,192px clear of the work seats.
 routes.append(dict(id=f'reception-staff-{n}-approach',start='shared-spine',points=[[544,592],[544,672],[x,672],[x,752]],intendedPartner=f'reception-visitor-{n}',otherPeerMinimumRequired=64))
routes.append(dict(id='public-gallery-approach',start='gallery-public-entrance',points=[[1136,944],[1136,688],[1184,688],[1184,648],[1216,648]],otherPeerMinimumRequired=64))
routes.append(dict(id='main-to-gallery',start='shared-spine',points=[[544,592],[544,672],[976,672],[976,688],[1136,688]],otherPeerMinimumRequired=64))
# Meeting and lounge approaches intentionally enter their own conversation groups.
meeting_ids=[q['id'] for q in goals if q['kind']=='meeting-seat']
lounge_ids=[q['id'] for q in goals if q['kind']=='lounge-seat']
for q in goals:
 if q['kind']=='meeting-seat':
  if q['facing']=='south':
   points=[[1216,648],[1216,560],[q['x'],560],[q['x'],q['y']]]
  elif q['x']==1280:
   points=[[1216,648],[1216,704],[1280,704]]
  else:
   side=q['x']-32
   points=[[1216,648],[1216,768],[side,768],[side,704],[q['x'],704]]
  routes.append(dict(id=q['id']+'-approach',start='conference-threshold',points=points,intendedGroupIds=meeting_ids,otherPeerMinimumRequired=64))
 if q['kind']=='lounge-seat':
  if q['facing']=='south':points=[[544,592],[544,720],[q['x'],720],[q['x'],q['y']]]
  else:points=[[544,592],[544,848],[336,848],[336,q['y']],[q['x'],q['y']]]
  routes.append(dict(id=q['id']+'-approach',start='shared-spine',points=points,intendedGroupIds=lounge_ids,otherPeerMinimumRequired=64))
# Both directions are validated; reverse egress is the entry route for each desk.
for route in routes:route['returnPoints']=list(reversed(route['points']))
module=dict(id='compact-lush-eight-seat-office',size=[W,H],campusOrigin=[704,64],geometryTranslation=[32,32],avatarFrame=[-16,-16,32,32],avatarBody=[-8,0,16,16],avatarScale=1,artScale=1,ordinaryWorkSeats=8,receptionServices=2,meetingSeats=6,floorTextLabels=False,foregroundPolicy='fixed authored source foreground only; no actor-following alpha masks',layers={'base':'office-base.png','foreground':'office-foreground.png','glass':'office-glass.png','shade':'office-overhead-shade.png'},floorEnvelopes=envelopes,colliders=rects,anchors=goals,routes=routes,social={'acquisition':64,'pairRetention':96,'seatColumnSpacing':160,'opposingSeatSpacing':112,'centralDeskRouteOtherPeerClearance':80,'workCrosslaneLastRowClearance':112},entrances=[{'id':'main','x':480,'y':912,'width':128,'height':48,'center':[544,944]},{'id':'gallery-public','x':1088,'y':912,'width':96,'height':48,'center':[1136,944]}],placeholders={'mainSign':{'kind':'existing teal banner with gold leaf emblem','liveRoutingConfigured':False},'meetingSign':{'kind':'existing teal gallery banner','liveRoutingConfigured':False}},liveServicesConfigured=False)
(R/'module.json').write_text(json.dumps(module,indent=2))
(R/'anchors.json').write_text(json.dumps(goals,indent=2))
(R/'routes.json').write_text(json.dumps(routes,indent=2))
(R/'compositing-manifest.json').write_text(json.dumps({'operations':manifest,'sourceHashes':{str(S/f'office-v4-{n}.png'):hashlib.sha256((S/f'office-v4-{n}.png').read_bytes()).hexdigest() for n in names},'resizes':0,'newArtGeneration':False},indent=2))
print('Built',W,H,'anchors',len(goals),'colliders',len(rects),'routes',len(routes))
