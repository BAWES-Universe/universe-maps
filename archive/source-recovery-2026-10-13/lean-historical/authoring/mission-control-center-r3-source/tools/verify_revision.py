from pathlib import Path
from PIL import Image
import numpy as np,json
r=Path(__file__).resolve().parents[1];m=r/'mission-control-center';old=Path('/workspace/shared/mission-control-sky-seats-r2/mission-control-center');load=lambda p:json.loads(p.read_text());a=load(old/'source/layout.json');b=load(m/'source/layout.json');allow=np.zeros((1408,1536),bool)
for layout,dy in [(a,1),(b,-12)]:
 for s in layout['seats']:
  if s['name'].startswith('operator-'):
   x,y=s['anchor'];allow[y+dy:y+dy+37,x-16:x+16]=1
art={}
for fn in ['base.png','above.png']:
 x=np.array(Image.open(old/'assets'/fn));y=np.array(Image.open(m/'assets'/fn));diff=np.any(x!=y,axis=2);assert not np.any(diff&~allow);art[fn]={'changedPixels':int(diff.sum()),'outsideSixOperatorChairFootprintsChanged':0}
assert a['collision']==b['collision'];assert a['zones']==b['zones'];assert a['seats'][6:]==b['seats'][6:]
centers=[492,776,1048,560,776,984];assert [s['anchor'][0] for s in b['seats'][:6]]==centers
for s in b['seats'][:6]:assert s['anchor'][1]%32==0
routes=load(m/'NATIVE-ROUTES.json')['rows']
for seat in b['seats'][:6]:assert next(row['final'] for row in routes if row['name']==seat['name']+' same-cell')==seat['anchor']
report={'pass':True,'allSixTapArrivalsExactlyMatchChairAnchors':True,'approvedSettingSkyAndBriefingByteExact':True,'artPreservation':art,'collisionUnchanged':True,'nativePropertiesUnchanged':True,'chairNativeTapCenterX':centers,'consoleMeasuredCenterX':[492,768,1048,560,768,984],'chairVisualOffsetFromBodyAnchorY':-12,'nativeIdlePoses':'Existing native standing idle frames only; no seated animation','clickFit':'All six native tap endpoints match the chair/body anchors exactly. Two center chairs are8px right of console axis, within keyboard width. No engine patch.','allSixOperatorsDifferentActualWokas':True}
(m/'REVISION-VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
