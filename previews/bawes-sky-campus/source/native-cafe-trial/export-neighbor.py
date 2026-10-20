"""Export existing TMJ pixels without resampling; no art generation or map edits."""
from pathlib import Path
from PIL import Image
import json,bisect
root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
m=json.loads((root/'campus.tmj').read_text()); sets=m['tilesets']; starts=[s['firstgid'] for s in sets]; cache={}
import sys
x,y,w,h=map(int,sys.argv[2:6])
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

# Include completed native neighbors at their world registration, without resampling.
for name,ox,oy in json.loads((out/'panels.json').read_text()):
 a=Image.open(out/name).convert('RGBA');left=max(x,ox);top=max(y,oy);right=min(x+w,ox+a.width);bottom=min(y+h,oy+a.height)
 if right>left and bottom>top:im.alpha_composite(a.crop((left-ox,top-oy,right-ox,bottom-oy)),(left-x,top-y))
im.save(out/sys.argv[1])
