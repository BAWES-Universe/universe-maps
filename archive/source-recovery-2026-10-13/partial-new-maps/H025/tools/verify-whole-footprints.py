from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];d=json.load(open(R/'source/design.json'));m=json.load(open(R/'map32/map.tmj'));g=np.array(next(l for l in m['layers']if l['name']=='collision')['data']).reshape((m['height'],m['width']))!=0;rows=[]
for room in d['rooms']:
 ox,oy=room['offset']
 for i,p in enumerate(room['fullFixturePolygons']):
  mask=Image.new('1',(1248,1248));ImageDraw.Draw(mask).polygon([tuple(a)for a in p],fill=1);ys,xs=np.where(np.asarray(mask));blocked=g[(ys+oy)//32,(xs+ox)//32];rows.append(dict(room=room['id'],index=i,pixels=len(xs),admittedPixels=int((~blocked).sum()),blockedAll=bool(blocked.all())))
out=dict(scope='Author raster audit of every declared whole grounded polygon; completeness still needs fresh independent art inspection.',tmjSHA256=hashlib.sha256((R/'map32/map.tmj').read_bytes()).hexdigest(),rows=rows,passAll=all(a['blockedAll']for a in rows));(R/'validation/whole-footprints.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='rows'},indent=2));assert out['passAll']
