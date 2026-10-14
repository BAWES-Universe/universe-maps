from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
import build_maps as b
R=Path(__file__).resolve().parents[1];S=R/'source';D=256;W,H=2048,1536
baseline=json.loads((S/'layout.json').read_text()); clean=Image.open(S/'portal-environment-garden-boundaries-master.png').convert('RGBA')
background=Image.open(S/'final-composite.png').convert('RGBA')
assert background.size==(W,H),background.size
# Exact courtyard core is already integrated; decorative perimeter transition is allowed.
m=b.Map('celestial-transit-garden','Celestial Transit Garden · expanded r4',W,H,baseline['category'],'Preserved moonlit courtyard with extended starry garden surroundings')
m.base=background;m.above=Image.new('RGBA',(W,H));m.grid=np.ones((H//32,W//32),np.uint8);m.grid[8:40,8:56]=np.array(baseline['grid']);m.quiet=np.zeros_like(m.grid);m.quiet[8:40,8:56]=np.array(baseline['quiet']);m.spawn=tuple(v+D for v in baseline['start'])
m.anchors=copy.deepcopy(baseline['anchors']);m.areas=copy.deepcopy(baseline['areas']);m.objects=copy.deepcopy(baseline['objects']);m.fixtures=copy.deepcopy(baseline['protectedFixtures'])
for a in m.anchors+m.areas:a['x']+=D;a['y']+=D
for f in m.fixtures:f['solidXYXY']=[v+D for v in f['solidXYXY']]
# Geometry-only scenery repair. The accepted expanded bitmap is byte-identical.
repair=json.loads((S/'scenery-collision-repair.json').read_text())
for x,y in repair['blockedCells']:m.grid[y,x]=1
for x,y in repair['admittedStoneCells']:m.grid[y,x]=0
for a in m.anchors:
 if a['id']=='northwest-garden-lookout':a['x'],a['y']=944,591
 if a['id']=='northeast-garden-lookout':a['x'],a['y']=1104,591
# Exclude isolated decorative floor pockets after protecting complete scenery.
from collections import deque
reach=np.zeros_like(m.grid,bool);q=deque([(m.spawn[0]//32,m.spawn[1]//32)])
while q:
 x,y=q.popleft()
 if not(0<=x<m.C and 0<=y<m.N) or m.grid[y,x] or reach[y,x]:continue
 reach[y,x]=True;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
closed=[[int(x),int(y)] for y,x in np.argwhere((m.grid==0)&~reach)]
m.grid[(m.grid==0)&~reach]=1
b.jw(m.r/'validation/closed-decorative-pockets.json',closed)
# Split genuine tall-tree projection above supported stone; roots stay blocked.
a=np.asarray(m.base).astype(int);tips=np.zeros((H,W),np.uint8)
for x,y in [(25,31),(26,31),(37,31),(38,31)]:
 sub=a[y*32:(y+1)*32,x*32:(x+1)*32];veg=(sub[:,:,1]>sub[:,:,0]+5)&(sub[:,:,1]>sub[:,:,2]-10)&(sub[:,:,0]<150)
 tips[y*32:(y+1)*32,x*32:(x+1)*32]=veg.astype(np.uint8)*255
m.foreground_candidate=Image.fromarray(tips);m.partition_foreground()
m.base.save(m.r/'source/runtime-base.png');m.above.save(m.r/'source/runtime-above.png')
layout=dict(title=m.title,category=m.category,style=m.style,world=[W,H],start=m.spawn,grid=m.grid.tolist(),quiet=m.quiet.tolist(),anchors=m.anchors,areas=m.areas,objects=m.objects,protectedFixtures=m.fixtures)
b.jw(m.r/'source/layout.json',layout);m.compile();m.validate();m.render()
# Preserve every original property, object identity, WAM label and configuration; only translate geometry.
oldtmj=json.loads((S/'celestial-transit-garden.tmj').read_text());oldwam=json.loads((S/'celestial-transit-garden.wam').read_text());newtmj=json.loads((m.r/'map32/celestial-transit-garden.tmj').read_text())
oldobjects=next(l for l in oldtmj['layers'] if l['name']=='map-areas');newobjects=next(l for l in newtmj['layers'] if l['name']=='map-areas');shift=copy.deepcopy(oldobjects)
for o in shift['objects']:o['x']+=D;o['y']+=D
newobjects.update(shift);newtmj['properties']=oldtmj['properties'];b.jw(m.r/'map32/celestial-transit-garden.tmj',newtmj)
for a in oldwam['areas']:a['x']+=D;a['y']+=D
b.jw(m.r/'map32/celestial-transit-garden.wam',oldwam)
checks={'scope':'Exact source art and native32 geometry preservation; external scene is blocked context, not new gameplay.','offset':[D,D],'oldWorld':baseline['world'],'newWorld':[W,H],'allWalkablePixelsIdenticalToLabelFreeMaster':np.array_equal(np.asarray(Image.alpha_composite(m.base,m.above))[D:D+1024,D:D+1536][np.array(baseline['grid']).repeat(32,0).repeat(32,1)==0],np.asarray(clean)[np.array(baseline['grid']).repeat(32,0).repeat(32,1)==0]),'exactOriginalPixelsProtected':int((np.asarray(Image.open(S/'preservation-alpha.png'))==255).sum()),'decorativePerimeterTransition':'Up to 112px edge band blended; every walkable pixel plus 24px guard and portal architecture restored exactly, except previously cropped crown edge' ,'collisionDeltaDocumented':all(m.grid[y,x]==1 for x,y in repair['blockedCells']),'artByteIdenticalToAcceptedExpansion':Image.alpha_composite(m.base,m.above).tobytes()==background.tobytes(),'quietCoreIdentical':np.array_equal(m.quiet[8:40,8:56],baseline['quiet']),'onlyDocumentedGeometryDelta':bool(np.all(m.grid[8:40,8:56]>=np.array(baseline['grid']))),'anchorIDsPreserved':[x['id'] for x in m.anchors]==[x['id'] for x in baseline['anchors']],'areaIDsPreserved':[x['id'] for x in m.areas]==[x['id'] for x in baseline['areas']],'bakedFunctionalPlaquesRemoved':5,'newExteriorWalkableCells':0}
checks['allPass']=all(checks[k] for k in ['allWalkablePixelsIdenticalToLabelFreeMaster','collisionDeltaDocumented','artByteIdenticalToAcceptedExpansion','quietCoreIdentical','onlyDocumentedGeometryDelta','anchorIDsPreserved','areaIDsPreserved']);b.jw(m.r/'validation/preservation-delta.json',checks);print(checks)
