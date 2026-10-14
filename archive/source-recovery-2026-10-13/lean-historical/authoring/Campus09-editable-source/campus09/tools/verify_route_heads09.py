from pathlib import Path
from PIL import Image
import numpy as np,json,math
R=Path(__file__).resolve().parents[1];above=np.asarray(Image.open(R/'layers/campus-above.png').convert('RGBA'))[:,:,3];sheet=np.asarray(Image.open(R/'validation/greg.png').convert('RGBA'))
heads=[sheet[(i//3)*32:(i//3)*32+14,(i%3)*32:(i%3+1)*32,3]>0 for i in range(12)]
rows=[]
for fn in ['integrated-office-route-traces09.json','compiled-public-route-traces09.json']:
 for item in json.loads((R/'docs'/fn).read_text()):
  hits=0;maxpix=0;first=None;peak=None;framing=0
  for x,y,dx,dy in item['trace']:
   facing=6 if dx>0.001 else 3 if dx<-.001 else 0 if dy>0.001 else 9
   high=0
   for xx,yy in {(math.floor(x)-16,math.floor(y)-16),(math.ceil(x)-16,math.ceil(y)-16)}:
    a=above[yy:yy+14,xx:xx+32]
    if a.shape!=(14,32):framing+=1;continue
    for i in range(facing,facing+3):high=max(high,int(np.count_nonzero(heads[i]&(a>=224))))
   if high:
    hits+=1;first=first or[x,y,dx,dy]
    if high>maxpix:maxpix=high;peak=[x,y,dx,dy]
  rows.append({'id':item['id'],'direction':item.get('direction'),'group':item.get('group','office'),'samples':len(item['trace']),'opaqueHeadHitSamples':hits,'maxHeadPixels':maxpix,'first':first,'peak':peak,'offMapHeadCrops':framing})
report={'scope':'Actual combined compiled-source above layer, every traced native movement position; three animation frames for movement direction, conservative floor/ceil raster positions. Opacity224+ counts opaque occlusion; legitimate translucent glass/shade remains below threshold. No dynamic masks or browser claim.','allPass':all(not r['opaqueHeadHitSamples']and not r['offMapHeadCrops']for r in rows),'routes':rows}
(R/'docs/compiled-route-head-clearance09.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'allPass':report['allPass'],'routes':len(rows),'samples':sum(r['samples']for r in rows),'failures':[r for r in rows if r['opaqueHeadHitSamples']or r['offMapHeadCrops']]}))
