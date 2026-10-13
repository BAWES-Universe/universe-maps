from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
from collections import deque
import build_maps as b
R=Path(__file__).resolve().parents[1];S=R/'source'
slug='celestial-transit-garden-calm-draft'
m=b.Map(slug,'Celestial Garden - calm draft',2048,1536,'Social / transit garden','Calmer color concept rebuilt as a separate unconfigured draft')
m.base=Image.open(S/'calm-master-native.png').convert('RGBA');m.grid=np.load(S/'diagnostic-grid.npy')
# Fresh art-authored corrections for painted gold floor details and genuine conifer projections.
adds=[[22,17],[26,32],[27,32],[28,32],[35,32],[36,32],[37,32],[42,27],[29,39],[30,39],[31,39],[32,39],[33,39],[34,39]]
for x,y in adds:m.grid[y,x]=0
for x,y in [(41,21),(30,28),(30,29),(30,30),(33,28),(33,29),(33,30),(29,32),(34,32),(29,35),(34,35),(33,31),(27,16),(36,16),(30,14),(33,14),(35,17),(23,17),(40,19),(25,21),(42,23),(21,24),(42,25),(21,26),(22,28),(41,28),(27,31),(36,31),(24,32),(39,32),(21,18),(39,21)]:m.grid[y,x]=1
feet=[('northeast-left-pot',[1360,472,1400,508]),('northeast-left-foot',[1396,448,1436,500]),('northeast-right-foot',[1516,480,1552,540]),('north-west-lantern-plinth',[924,380,968,440]),('north-east-lantern-plinth',[1080,380,1124,440]),('northwest-west-foot',[504,480,544,536]),('northwest-east-foot',[616,460,656,504]),('northwest-east-pot',[648,472,688,512]),('southwest-west-foot',[456,856,500,912]),('southwest-east-foot',[584,824,624,884]),('southwest-east-pot',[624,844,672,892]),('southeast-west-pot',[1376,844,1436,896]),('southeast-west-foot',[1420,824,1456,880]),('southeast-east-foot',[1544,856,1584,912])]
for name,box in feet:m.protect(name,box)
m.spawn=(1040,1231)
# Keep only main connected footprint; all discarded diagnostic cells recorded for visual review.
reach=np.zeros_like(m.grid,bool);q=deque([(m.spawn[0]//32,m.spawn[1]//32)])
while q:
 x,y=q.popleft()
 if not(0<=x<m.C and 0<=y<m.N) or m.grid[y,x] or reach[y,x]:continue
 reach[y,x]=True;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
closed=[[int(x),int(y)]for y,x in np.argwhere((m.grid==0)&~reach)];m.grid[(m.grid==0)&~reach]=1
m.quiet=np.zeros_like(m.grid);m.quiet[37:39,31:34]=1
for id,x,y,di,kind in [('destination-north',1040,448,'north','social'),('destination-northwest',616,512,'north','social'),('destination-northeast',1432,512,'north','social'),('destination-southwest',568,896,'north','social'),('destination-southeast',1480,896,'north','social'),('central-compass',1040,687,'south','social'),('south-spoke',1040,1007,'north','landmark'),('spawn',1040,1231,'north','spawn')]:m.anchor(id,x,y,di,kind)
for i,a in enumerate(m.anchors[:5]):m.zone(a['id'],f'DESTINATION {i+1:02} / unconfigured',(a['x']-20,a['y']-12,a['x']+20,a['y']+24),'Draft destination placeholder; no external service or exit configured')
# Fresh silhouette mask only for raised evergreen foliage above known ground paving.
a=np.asarray(m.base).astype(int);tips=np.zeros((1536,2048),np.uint8)
for x,y in [(26,32),(27,32),(36,32),(37,32)]:
 sub=a[y*32:(y+1)*32,x*32:(x+1)*32];veg=(sub[:,:,1]>sub[:,:,0]+5)&(sub[:,:,1]>sub[:,:,2]-10)&(sub[:,:,0]<150);tips[y*32:(y+1)*32,x*32:(x+1)*32]=veg.astype(np.uint8)*255
m.foreground_candidate=Image.fromarray(tips);m.partition_foreground()
m.base.save(m.r/'source/runtime-base.png');m.above.save(m.r/'source/runtime-above.png')
b.jw(m.r/'source/layout.json',dict(title=m.title,category=m.category,style=m.style,world=[2048,1536],start=m.spawn,grid=m.grid.tolist(),quiet=m.quiet.tolist(),anchors=m.anchors,areas=m.areas,objects=[],protectedFixtures=m.fixtures))
b.jw(m.r/'validation/fresh-authoring.json',dict(sourceArtwork='calm-master-native.png',sourceSHA256=hashlib.sha256((S/'calm-master-native.png').read_bytes()).hexdigest(),priorCollisionGridUsed=False,diagnosticRule='New-image floor segmentation with manually inspected painted-floor and conifer-projection overrides; independent review required',addedFloorCells=adds,closedDisconnectedDiagnosticCells=closed,status='DRAFT: awaiting independent actual-art review'))
m.compile();m.validate();m.render()
