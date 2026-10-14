from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];d=json.loads((R/'source/layout-definition.json').read_text());l=json.loads((R/'evidence/layout.json').read_text());results=[]
for room,items in d.get('physicalFootprints',{}).items():
 ox,oy=l['rooms'][room]['offset'];w,h=l['rooms'][room]['size']
 for f in items:
  mask=Image.new('1',(w,h));ImageDraw.Draw(mask).polygon([tuple(p)for p in f['polygon']],fill=1);bad=[];pixels=0;x0,y0,x1,y1=mask.getbbox()
  for y in range(y0,y1):
   for x in range(x0,x1):
    if mask.getpixel((x,y)):
     pixels+=1
     if not l['grid'][(y+oy)//32][(x+ox)//32]:bad.append([x,y])
  results.append(dict(room=room,name=f['name'],polygon=f['polygon'],pixels=pixels,admittedPixels=bad,**{'pass':not bad}))
report=dict(allPass=all(v['pass']for v in results),scope='Author traced complete lower hard-base polygons on final art, each rasterized pixel must be collision-negative. Supplements independent visual review; does not turn arbitrary vegetation or upper projections into footprints.',tmjSHA256=hashlib.sha256((R/'runtime/mechanical-orchard.tmj').read_bytes()).hexdigest(),rows=results)
(R/'evidence/physical-footprints.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert report['allPass']
