#!/usr/bin/env python3
"""Assembled-art source geometry, fixed native body, actual16px map grid."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ART=ROOT.parents[1]
load=lambda p:json.loads(p.read_text())
write=lambda name,data:(ROOT/name).write_text(json.dumps(data,indent=2)+'\n')
def rect(x,y,w,h):return dict(x=x,y=y,width=w,height=h)
def pt(x,y):return dict(x=x,y=y)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def overlap(a,b):return a['x']<b['x']+b['width'] and b['x']<a['x']+a['width'] and a['y']<b['y']+b['height'] and b['y']<a['y']+a['height']
def move(r,dx,dy):return dict(r,x=r['x']+dx,y=r['y']+dy)

g=copy.deepcopy(load(ROOT.parent/'revision-02/source-coordinate-geometry.json'))
assembly=load(ART/'docs/assembly-02-manifest.json')
script=(ART/'tools/assemble_office_v2.py').read_text()
assert 'tx,ty=pod[\'x\']+144,pod[\'y\']+144' in script, 'Await approved workbench art shift'
assert "put('objects',chair,x+56,592)" in script, 'Await approved guest chair correction'
assert assembly['translation']==[32,32] and assembly['canvas']==[2496,1408]
actual={b['team']:b for b in assembly['benchPlacements']}
g.update(format='studenthub-source-geometry-v3',revision='03-final-assembled-art',
         status='authoritative assembled-art collision draft pending generated route validation',
         coordinateSpace='office source pixels; add renderTranslation once',renderTranslation=pt(32,32),
         fullCanvas=rect(0,0,2496,1408))
g['packaging'].update(widthTiles=156,heightTiles=88,mapPixelWidth=2496,mapPixelHeight=1408,
                     sourceEnvelope=rect(0,0,2432,1344),renderTranslation=pt(32,32),
                     requirement='Use full-canvas collision-grid.json exactly, or translate collision-grid-source.json once. Art/Wokas remain unscaled.')
g['coordinateSystem']['origin']='upper-left of source main office; rendered source origin at(32,32)'
g['integrationChanges']=[
    'Every complete shared workbench group and its four personal plots moved32px east: table=pod+(144,144). Native geometry and artwork unchanged.',
    'Cross-aisle guest chairs moved8px south to asset y592 / north-facing center608, clearing coffee collision ending608.',
    'Actual receiver U cabinets, inset rear wall, outer strips and gallery rails replace prior diagram walls/dividers.',
]
for b in g['workbenches']:
    name=next(p['name'] for p in g['pods'] if p['id']==b['podId'])
    ar=actual[name]['table']; dx=ar[0]-b['table']['x'];dy=ar[1]-b['table']['y']
    assert dx==32 and dy==0
    for key in ['table','collision','tableAssetCanvas','compositeAssetCanvas','visibleFurnitureBounds']:b[key]=move(b[key],dx,dy)
    for s in g['stations']:
        if s['sharedWorkbenchId']!=b['id']:continue
        s['seat']['x']+=dx;s['seat']['y']+=dy
        for k in ['spriteBounds','bodyBounds']:s['seat'][k]=move(s['seat'][k],dx,dy)
        s['chairAssetCanvas']=move(s['chairAssetCanvas'],dx,dy)
        s.pop('approach',None)
    for p in g['claimPlots']:
        if p['workbenchId']==b['id']:p['x']+=dx;p['y']+=dy

walls=[];cabinets=[];furniture=[];goals=[];placements=[]
def add(out,identifier,x,y,w,h,kind,**extra):
    item=dict(id=identifier,**rect(x,y,w,h),kind=kind,**extra);out.append(item);return item
def goal(identifier,x,y,facing='north',kind='checkpoint',**extra):
    item=dict(id=identifier,x=x,y=y,facing=facing,kind=kind,bodyBounds=rect(x-8,y,16,16),**extra)
    goals.append(item);return item

add(walls,'main-rear-solid',0,0,1984,176,'permanent-wall')
add(walls,'main-west-solid',0,176,96,1168,'permanent-wall')
add(walls,'main-east-solid-north',1920,176,64,912,'permanent-wall')
add(walls,'main-east-solid-south',1920,1136,64,208,'permanent-wall')
add(walls,'main-south-west',96,1328,832,16,'permanent-wall')
add(walls,'main-south-east',1056,1328,864,16,'permanent-wall')
for p in g['pods']:
    x=p['x'];y=144 if p['y']<448 else 784
    add(cabinets,p['id']+'-cabinet-back',x+80,y,256,32,'receiver-fixed-cabinet')
    add(cabinets,p['id']+'-cabinet-west',x+32,y+16,48,192,'receiver-fixed-cabinet')
    add(cabinets,p['id']+'-cabinet-east',x+336,y+16,48,192,'receiver-fixed-cabinet')
    # Pixel-inspected inner lantern/bookcase floor elbow. It is not foliage.
    elbow_x=x+80 if x in [64,1056] else x+272
    add(cabinets,p['id']+'-cabinet-elbow',elbow_x,y+32,64,32,'receiver-fixed-cabinet',
        evidence='Native receiver pixel inspection; same crop transform as the authoritative assembler.')

GX,GY=1984,448
add(walls,'gallery-north-solid',GX,GY,448,64,'permanent-wall')
add(walls,'gallery-east-solid',GX+416,GY+64,32,832,'permanent-wall')
add(walls,'gallery-west-upper',GX,GY+64,32,576,'permanent-wall')
add(walls,'gallery-west-lower',GX,GY+688,32,208,'permanent-wall')
add(walls,'gallery-south-room-wall',GX+128,GY+864,288,32,'permanent-wall')
for i,(y0,y1) in enumerate([(0,112),(192,288),(368,576),(672,832)],1):
    add(walls,f'gallery-corridor-glass-{i}',GX+128,GY+y0,16,y1-y0,'permanent-glass-rail')
for i,y in enumerate([192,400],1):add(walls,f'gallery-room-rail-{i}',GX+144,GY+y,272,16,'permanent-glass-rail')
g['doorOpenings']=[
    dict(id='main-entrance',**rect(928,1328,128,16)),
    dict(id='office-gallery-connection',**rect(1920,1088,96,48)),
    dict(id='gallery-visitor-entrance',**rect(2016,1312,96,32)),
    dict(id='meeting-a-door',**rect(2112,560,16,80)),
    dict(id='meeting-b-door',**rect(2112,736,16,80)),
    dict(id='conference-door',**rect(2112,1024,16,96)),
]
for b in g['workbenches']:
    add(furniture,b['id'],**dict(x=b['table']['x'],y=b['table']['y'],w=128,h=96),kind='fixed-shared-workbench')
for s in g['stations']:
    goal(s['id'],s['seat']['x'],s['seat']['y'],s['seat']['facing'],'team-seat',
         claimPlotId=s['claimPlotId'],fixtureId=s['sharedWorkbenchId'],contactDirection=s['seat']['facing'])

rl=load(ART/'art-reception-lounge/geometry-plan.json')
north=load(ART/'art-reception-lounge/sofa-north-manifest.json')
def sofa(identifier,x,y,facing):
    local=rl['sofa']['collision_parts_asset'] if facing=='south' else [v[1] for v in north['collision_parts_local_xywh']]
    anchors=rl['sofa']['seat_anchors_asset'] if facing=='south' else north['seat_anchors_local']
    for i,(rx,ry,rw,rh) in enumerate(local):add(furniture,f'{identifier}-part-{i}',x+rx,y+ry,rw,rh,'sofa-floor')
    placements.append(dict(id=identifier,assetOrigin=pt(x,y),facing=facing,sourceManifest='art-reception-lounge/geometry-plan.json' if facing=='south' else 'art-reception-lounge/sofa-north-manifest.json'))
    for i,(ax,ay) in enumerate(anchors,1):goal(f'{identifier}-seat-{i}',x+ax,y+ay,facing,'lounge-seat',fixtureId=identifier)
def coffee(identifier,x,y):
    rx,ry,w,h=rl['coffee_table']['collision_local']
    add(furniture,identifier,x+rx,y+ry,w,h,'coffee-table')
    placements.append(dict(id=identifier,assetOrigin=pt(x,y),sourceManifest='art-reception-lounge/geometry-plan.json'))
for name,x in [('west',176),('east',1168)]:
    sofa(f'cross-lounge-{name}-sofa',x,464,'south')
    coffee(f'cross-lounge-{name}-coffee',x+32,560)
    goal(f'cross-lounge-{name}-guest',x+80,608,'north','lounge-seat',fixtureId=f'cross-lounge-{name}-guest-chair',contactDirection='north')
    placements.append(dict(id=f'cross-lounge-{name}-guest-chair',assetOrigin=pt(x+56,592),facing='north',sourceManifest='art-meeting/geometry-plan.json',chairAnchorLocal=pt(24,16)))
sofa('foyer-south-facing-sofa',304,1104,'south')
coffee('foyer-coffee',336,1184)
sofa('foyer-north-facing-sofa',304,1216,'north')
rx,ry,rw,rh=rl['reception']['collision_local']
add(furniture,'reception-counter',1120+rx,1168+ry,rw,rh,'reception-counter')
goal('reception-staff',1200,1168,'south','reception-position',fixtureId='reception-counter',contactDirection='south')
goal('reception-visitor',1200,1264,'north','reception-position',fixtureId='reception-counter')

meeting=load(ART/'art-meeting/geometry-plan.json')
layouts={m['id']:m for m in meeting['layouts']}
for room,layout,x,y in [('meeting-a','small-four-cardinal',2144,480),('meeting-b','small-four-cardinal',2144,672),('conference','conference-six',2144,896)]:
    m=layouts[layout];t=m['table']
    add(furniture,room+'-table',x+t['x'],y+t['y'],t['width'],t['height'],'meeting-table')
    placements.append(dict(id=room,layoutId=layout,assetOrigin=pt(x,y),sourceManifest='art-meeting/geometry-plan.json',placementSource='authoritative assembler; overrides older manifest placements'))
    for s in m['seats']:
        goal(room+'-'+s['id'],x+s['center'][0],y+s['center'][1],s['facing'],'meeting-seat',fixtureId=room+'-table',contactDirection=s['facing'])

checkpoints=[goal('main-entrance',992,1328,'north'),goal('shared-spine-center',992,624,'north'),
             goal('gallery-main-threshold',1968,1104,'east'),goal('gallery-corridor-entry',2064,1104,'north'),
             goal('gallery-south-entry',2064,1328,'north')]
for room,y in [('meeting-a',584),('meeting-b',760),('conference',1064)]:checkpoints.append(goal(room+'-threshold',2144,y,'east'))
g['permanentWalls']=walls;g['lowDividers']=cabinets;g['furnitureCollisionRectangles']=furniture
g['allCollisionRectangles']=walls+cabinets+furniture
g['sharedSpacePlacements']=placements;g['goals']=goals;g['checkpoints']=checkpoints
g['rooms']=[dict(id='meeting-a',name='Meeting A',**rect(2128,512,272,128)),dict(id='meeting-b',name='Meeting B',**rect(2128,656,272,192)),dict(id='conference',name='Conference',**rect(2128,864,272,448))]
g['namedAreas']=g['pods']+g['rooms']+[dict(id='south-foyer',name='South foyer',**rect(96,1088,1824,240))]
g['reservations']=[];g['pendingObstacleMasks']=None
g['floor']['policy']='Union of source main and gallery floor envelopes minus allCollisionRectangles. Outside floor is blocked. Full canvas adds32px outer margin.'
g['protectedSpines']=[dict(id='central-entrance-spine',**rect(928,176,128,1168))]
g['claims']['routeMeaning']='Ownership areas do not restrict walking; final routes may cross unoccupied work-edge parts of other draft plots while avoiding every occupied body.'
g['limitations']=['Offline assembled-art source checks plus real16px collision-grid packing; compiled runtime execution remains a separate verification step.','No live claiming, permissions, audio/video isolation or sitting animation configured.','Sofa floor colliders are distinct from elevated visual backs. Conservative16px cell coverage is accepted only after all exact seat bodies and routes pass.','Receiver cabinet elbows were included from actual pixel inspection; decorative upper foliage does not become a blanket floor blocker.']
sources=[ART/'tools/assemble_office_v2.py',ART/'docs/assembly-02-manifest.json',ART/'docs/office-interior-assembly-02-native.png',ART/'materials/receiver-panel-native-01.png',ART/'materials/gallery-native-02-open-doors.png',ART/'art-reception-lounge/geometry-plan.json',ART/'art-reception-lounge/sofa-north-manifest.json',ART/'art-meeting/geometry-plan.json']
g['assembledArtProvenance']=[dict(path=str(p),sha256=sha(p)) for p in sources]
g['baselineProvenance']=dict(revision02Geometry=str(ROOT.parent/'revision-02/source-coordinate-geometry.json'),sha256=sha(ROOT.parent/'revision-02/source-coordinate-geometry.json'))
write('source-coordinate-geometry.json',g)
write('furniture-collision-rectangles.json',dict(coordinateSpace='source office pixels',renderTranslation=pt(32,32),permanentWalls=walls,receiverCabinets=cabinets,furniture=furniture))
write('checkpoint-manifest.json',dict(coordinateSpace='source office pixels',renderTranslation=pt(32,32),origins=['main-entrance','reception-visitor'],goals=goals))
claims=[]
for p in g['claimPlots']:
    claims.append(dict(id=p['id'],name=p['name'],**{k:p[k] for k in ['x','y','width','height']},visible=True,properties=[dict(id=p['propertyId'],type='personalAreaPropertyData',accessClaimMode='dynamic',allowedTags=[],ownerId=None)]))
wam=dict(version='2.0.0',mapUrl='./studenthub-expanded-assembled-candidate.tmj',entities={},entityCollections=[],areas=[move(a,32,32) for a in claims],metadata=dict(name='StudentHub assembled office — OFFLINE DRAFT',description='Unassigned provisional seat/work-edge areas around fixed baked shared benches. Full-canvas coordinates. No live routing or claim configuration.'),vendor=dict(offlineDraft=True,coordinateSpace='rendered full canvas',sourceTranslation=pt(32,32),allOwnersUnassigned=True))
write('personal-areas.offline-draft.wam',wam)
write('claim-manifest.json',dict(coordinateSpace='source office pixels',renderTranslation=pt(32,32),areas=claims,fixedBenchesAreNotEntities=True))

def make_grid(width,height,offset):
    blocked=[];coverage=[];floors=[move(r,offset,offset) for r in g['floor']['envelopes']]
    coll=[move(r,offset,offset) for r in g['allCollisionRectangles']]
    for y in range(height):
        for x in range(width):
            cell=rect(x*16,y*16,16,16)
            inside=any(f['x']<=cell['x'] and f['y']<=cell['y'] and cell['x']+16<=f['x']+f['width'] and cell['y']+16<=f['y']+f['height'] for f in floors)
            if not inside or any(overlap(cell,r) for r in coll):blocked.append(y*width+x)
    return dict(coordinateSpace='rendered full canvas' if offset else 'source office pixels',translationApplied=pt(offset,offset),width=width,height=height,tileSize=16,pixelWidth=width*16,pixelHeight=height*16,blockedIndices=blocked,policy='Conservative coverage of every source physical blocker; narrow sofa arms rounded outward only after validating exact seats/routes.')
write('collision-grid-source.json',make_grid(152,84,0))
write('collision-grid.json',make_grid(156,88,32))
write('checkpoint-manifest-full-canvas.json',dict(coordinateSpace='rendered full canvas',translationApplied=pt(32,32),origins=['main-entrance','reception-visitor'],goals=[dict(move(t,32,32),bodyBounds=move(t['bodyBounds'],32,32)) for t in goals]))
print(json.dumps(dict(goals=len(goals),teamSeats=len(g['stations']),colliders=len(g['allCollisionRectangles']),grid='156×88@16px; full canvas2496×1408',revision='03')))
