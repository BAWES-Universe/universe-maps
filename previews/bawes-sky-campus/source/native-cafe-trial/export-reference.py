"""Export existing TMJ pixels without resampling; no art generation or map edits."""
from pathlib import Path
from PIL import Image
import json,bisect
root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
m=json.loads((root/'campus.tmj').read_text()); sets=m['tilesets']; starts=[s['firstgid'] for s in sets]; cache={}
x,y,w,h=1984,3712,1536,1024
im=Image.new('RGBA',(w,h))
for layer in m['layers']:
 if layer['type']!='tilelayer' or not layer.get('visible',True) or layer['name'] in ['persistent-collision','start','office-interior']:continue
 for ty in range(y//16,(y+h)//16):
  for tx in range(x//16,(x+w)//16):
   gid=layer['data'][ty*m['width']+tx]
   if not gid:continue
   s=sets[bisect.bisect_right(starts,gid)-1]; key=s['image']
   if key not in cache:cache[key]=Image.open(root/key).convert('RGBA')
   k=gid-s['firstgid']; margin=s.get('margin',0); spacing=s.get('spacing',0)
   sx=margin+(k%s['columns'])*(16+spacing);sy=margin+(k//s['columns'])*(16+spacing)
   tile=cache[key].crop((sx,sy,sx+16,sy+16));im.alpha_composite(tile,(tx*16-x,ty*16-y))
im.save(out/'registered-reference.png')
(out/'registration.json').write_text(json.dumps({'base':'851a243dfe31a1ffe4a18adbb9775b3d97c97fa2','worldBounds':[x,y,w,h],'pixelScale':1,'sharedEastBridge':{'worldRect':[3280,4240,240,160],'candidateRect':[1296,528,240,160]},'southOverlapForNextPanel':{'worldRect':[1984,4480,1536,256],'candidateRect':[0,768,1536,256]},'furnitureTargets':{'woka':32,'sofaWidth':144,'tableWidth':64,'chairWidth':48,'stoolWidth':32},'status':'reference export; no candidate integration'},indent=2)+'\n')
