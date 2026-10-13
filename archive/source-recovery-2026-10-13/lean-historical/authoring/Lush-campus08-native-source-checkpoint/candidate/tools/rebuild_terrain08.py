"""Reproduce native terrain RGB from preserved source crops and fixed authored alpha."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'sources';D=S/'terrain08';manifest=json.loads((D/'source-crop-manifest.json').read_text());out=Image.new('RGBA',tuple(manifest['canvas']))
for op in manifest['sourceCrops']:
 suffix=op['source'].split('/sources/',1)[1];im=Image.open(S/suffix).convert('RGBA').crop(op['sourceCrop'])
 if op['mirrorHorizontal']:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if op['localAlphaPolygon']:
  mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon([tuple(p)for p in op['localAlphaPolygon']],fill=255);im.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
 out.alpha_composite(im,tuple(op['destination']))
out.putalpha(Image.open(D/'terrain-underlay-alpha.png'))
expected=Image.open(D/'terrain-underlay-native.png').convert('RGBA');assert out.tobytes()==expected.tobytes();print('Terrain source+fixedalpha: exact native pixel rebuild')
market=np.asarray(Image.open(S/'market/market-base.png').convert('RGBA'));pixels=np.zeros((96,1120,4),np.uint8)
for y in range(96):
 sy=319-y if y<64 else 256+(y-64)
 for x in range(1120):
  k=(1760+x-1824)%1408;sx=k if k<704 else 1407-k;pixels[y,x]=market[sy,sx]
assert pixels.tobytes()==Image.open(D/'market-forecourt-proposed.png').convert('RGBA').tobytes();print('Market reflected receiver: exact native pixel rebuild')
