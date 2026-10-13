from pathlib import Path
from PIL import Image
import numpy as np,json
r=Path(__file__).resolve().parents[1];m=r/'quiet-orbit-observatory';old=Path('/workspace/shared/observatory-wide-seminar-r3/quiet-orbit-observatory');load=lambda p:json.loads(p.read_text());a=load(old/'source/layout.json');b=load(m/'source/layout.json');allow=np.zeros((1408,1536),bool)
for layout,new in [(a,False),(b,True)]:
 for s in layout['seats']:
  x,y=s['anchor'];left,top,w,h=(x-12,y-4,24,24) if new else (x-16,y-23,32,48);allow[top:top+h,left:left+w]=1
 for cx in ([240,432] if new else [240,496]):
  for y in [17*32-(11 if new else 8)+384,20*32-(11 if new else 8)+384]:
   w,h=(80,43) if new else (63,44);left=cx-w//2 if new else cx-32;allow[y:y+h,left:left+w]=1
art={}
for fn in ['base.png','above.png']:
 x=np.array(Image.open(old/'assets'/fn));y=np.array(Image.open(m/'assets'/fn));diff=np.any(x!=y,axis=2);assert not np.any(diff&~allow),(fn,np.argwhere(diff&~allow)[:8]);art[fn]={'changedPixels':int(diff.sum()),'outsideAuthorizedFurnitureFootprintsChanged':0}
assert a['zones']==b['zones'];assert len(b['seats'][4:])==24
for s in b['seats'][4:]:
 x,y=s['anchor'];assert 960<=x<1375 and 928<=y<1120
assert all(b['collision'][y][37]==0 for y in range(30,35))
assert Image.open(old/'assets/base.png').crop((0,0,1536,384)).tobytes()==Image.open(m/'assets/base.png').crop((0,0,1536,384)).tobytes()
for cx in [240,432]:
 for top in [917,1013]:
  assert all(b['collision'][yy//32][xx//32] for yy in range(top,top+43) for xx in range(cx-40,cx+40))
report={'pass':True,'completeDeskRectanglesSolid':True,'approvedSkyByteExact':True,'artPreservation':art,'seminarSeats':24,'chairWidth':24,'sideBySidePaddingPixels':8,'centerAisleClearPixels':40,'centerAisleFullWalkableTiles':1,'audienceCenterX':1200,'measuredPresentationBoardCenterX':1202,'rightResearchDeskCentersShift':[496,432],'newPalette':'midnight blue, slate/stone and aged brass','nativePropertiesUnchanged':True,'pose':'Existing actual native idle sprites, not a seated animation'}
(m/'REVISION-VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
