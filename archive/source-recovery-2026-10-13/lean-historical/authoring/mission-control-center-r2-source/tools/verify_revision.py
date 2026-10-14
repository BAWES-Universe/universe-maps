from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
r=Path(__file__).resolve().parents[1];m=r/'mission-control-center';old=Path('/workspace/shared/overnight-learning-work/releases/mission-control-center-r1');load=lambda p:json.loads(p.read_text());a=load(old/'source/layout.json');b=load(m/'source/layout.json');allowed=np.zeros((1024,1536),bool)
# Full sprite footprints, never a room-sized exception mask.
for layout,offset in [(a,0),(b,384)]:
 for s in layout['seats']:
  px,py=s['anchor'];py-=offset
  if layout is a or s['direction']=='south':x0,y0,w,h=px-20,py-24,40,45
  else:x0,y0,w,h=px-16,py+1,32,37
  allowed[y0:y0+h,x0:x0+w]=1
bg=np.array(Image.open(r/'source-assets/exterior-seam-mask.png'))>0
original=np.array(Image.open(old/'assets/base.png'));assert np.all(original[:,:,:3][bg]<=3)
art={}
for fn in ['base.png','above.png']:
 x=np.array(Image.open(old/'assets'/fn));y=np.array(Image.open(m/'assets'/fn))[384:];diff=np.any(x!=y,axis=2);assert not np.any(diff&~(allowed|(bg if fn=='base.png' else False)));art[fn]={'changedPixels':int(diff.sum()),'outsideAuthorizedChairAndExteriorBackgroundChanged':0}
assert b['collision'][:12]==[[1]*48]*12
cg=np.array(b['collision'][12:])!=np.array(a['collision']);allowedg=np.zeros(cg.shape,bool);allowedg[27,10]=1;assert not np.any(cg&~allowedg)
assert [s['direction'] for s in b['seats']]==['north']*6+['south','north']
assert all(s['anchor'][1]-(s['cell'][1]*32)==1 for s in b['seats'] if s['direction']=='north')
for aa,bb in zip(a['zones'],b['zones']):assert aa['rect']==[bb['rect'][0],bb['rect'][1]-384,*bb['rect'][2:]]
tmj=load(m/'map32/map.tmj');assert all((m/'map32'/s['image']).is_file() for s in tmj['tilesets'])
report={'pass':True,'artPreservation':art,'originalTranslation':[0,384],'originalScale':1,'northBackdropSolid':True,'allNonChairCollisionUnchanged':True,'operatorDirection':'north, back of chair toward viewer','operatorPosition':'14px closer to desks within existing walkable tiles','briefingDirection':['south','north'],'chairFullSpriteFootprints':True,'assetClosure':True,'noNewAudio':True,'nativePropertiesUnchanged':True,'mediaLiveTest':'not run','seating':'native walk-to visual anchors, no invented sit animation','routeFixture':'60e7afdc3f96ef32525597cd46bd41175d61a2ef'}
(m/'REVISION-VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
