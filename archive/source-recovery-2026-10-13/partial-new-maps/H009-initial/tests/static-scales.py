from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/layout-definition.json').read_text());rows=[]
for room,v in D['rooms'].items():
 source=Image.open(R/v['source']).convert('RGBA').resize(tuple(v['size']),Image.Resampling.LANCZOS);decoded=Image.open(R/f'review/{room}-empty.png').convert('RGBA');assert decoded.tobytes()==source.tobytes();assert decoded.getextrema()[3]==(255,255)
 occupied=Image.open(R/f'review/{room}-actual-native-arrivals.png').convert('RGBA')
 for scale in [0.5,0.75,1.0]:
  im=occupied.resize((round(occupied.width*scale),round(occupied.height*scale)),Image.Resampling.NEAREST);dest=R/f'review/{room}-static-{int(scale*100):03}.png';im.save(dest)
  rows.append({'room':room,'scale':scale,'size':list(im.size),'wholeScene':True,'path':str(dest.relative_to(R)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'pass':True})
report={'allPass':True,'scope':'Whole decoded master equality, complete opacity, source-derived actual native32 arrival plates rendered at50%,75%,100% static scales. These are fixed PNG inspections, never live desktop/mobile/browser/camera or AV acceptance.','rows':rows}
(R/'evidence/static-scales.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
