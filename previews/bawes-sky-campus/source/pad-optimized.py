"""Preserve page-edge texels at fractional zoom; no logical tile pixels change."""
from pathlib import Path
from PIL import Image
import numpy as np,json
root=Path(__file__).resolve().parents[1]/'dist';p=root/'campus.tmj';m=json.loads(p.read_text())
for t in m['tilesets']:
 if t.get('margin',0):continue
 f=root/t['image'];im=Image.open(f).convert('RGBA')
 Image.fromarray(np.pad(np.asarray(im),((1,1),(1,1),(0,0)),mode='edge')).save(f)
 t['margin']=1;t['imagewidth']+=2;t['imageheight']+=2
p.write_text(json.dumps(m))
