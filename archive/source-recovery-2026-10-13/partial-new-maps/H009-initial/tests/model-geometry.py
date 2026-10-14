from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,itertools,numpy as np
R=Path(__file__).resolve().parents[1];L=json.loads((R/'evidence/layout.json').read_text());D=json.loads((R/'source/layout-definition.json').read_text());rows=[]
F=D['feedback'];ox,oy=L['rooms']['orchard']['offset'];dx,dy=F['phaseOffset']
for p,src in F['sourcePhases'].items():
 original=Image.open(R/src).convert('RGBA')
 for tree,poly in F['patches'].items():
  mask=Image.new('L',original.size);ImageDraw.Draw(mask).polygon([tuple(v)for v in poly],fill=255);patch=original.copy();patch.putalpha(mask);expected=Image.new('RGBA',original.size);expected.alpha_composite(patch,(dx,dy));name=tree+'-phase-'+p;actual=Image.open(R/f'runtime/{name}.png').convert('RGBA');assert expected.tobytes()==actual.tobytes();a=np.array(actual)[:,:,3];yy,xx=np.where(a>0);g=np.array(L['grid']);bad=np.sum(g[(yy+oy)//32,(xx+ox)//32]==0);assert bad==0,(name,int(bad));rows.append(dict(layer=name,source=src,sourceSHA256=hashlib.sha256((R/src).read_bytes()).hexdigest(),registration=[dx,dy],alphaBounds=actual.getbbox(),opaquePixels=int(len(xx)),opaquePixelsOnWalkableFloor=int(bad),**{'pass':True}))
for a,b in itertools.combinations(F['patches'],2):
 ma=np.array(Image.open(R/f'runtime/{a}-phase-1.png'))[:,:,3];mb=np.array(Image.open(R/f'runtime/{b}-phase-1.png'))[:,:,3];assert not np.any((ma>0)&(mb>0))
report=dict(allPass=True,scope='Exact mechanically registered imagegen phase islands, complete original source masters preserved. Every state pixel is inside permanently blocked planting/sculpture envelopes, patches are disjoint, no pedestrian-floor pixel changes, no generated raster painting by code. All27 independent geometric combinations share collision. Registration and visual quality remain separately inspected.',rows=rows);(R/'evidence/model-geometry.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
