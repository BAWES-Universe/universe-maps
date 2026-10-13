from pathlib import Path
from PIL import Image,ImageChops
import json,numpy as np
R=Path(__file__).resolve().parents[1];M=R/'map32';m=json.loads((M/'magical-campus.tmj').read_text());T=m['tilewidth'];W=m['width']*T;H=m['height']*T
assert T==32
sets=[]
for ts in m['tilesets']:
 sets.append((ts,Image.open(M/ts['image']).convert('RGBA'),{x['id']:x for x in ts.get('tiles',[])}))
def tile(gid,time=0):
 ts,im,meta=next(x for x in reversed(sets) if gid>=x[0]['firstgid']);i=gid-ts['firstgid'];a=meta.get(i,{}).get('animation')
 if a:
  t=time%sum(f['duration']for f in a)
  for f in a:
   if t<f['duration']:i=f['tileid'];break
   t-=f['duration']
 c=ts['columns'];return im.crop((i%c*T,i//c*T,(i%c+1)*T,(i//c+1)*T))
def region(layer,box,time=0):
 x0,y0,x1,y1=box;out=Image.new('RGBA',((x1//T+1)*T,(y1//T+1)*T))
 # This source checker uses paste, not alpha-composite, because native cells do not overlap.
 for yy in range(max(0,y0//T),min(m['height'],(y1+T-1)//T)):
  for xx in range(max(0,x0//T),min(m['width'],(x1+T-1)//T)):
   g=layer['data'][yy*m['width']+xx]
   if g:out.paste(tile(g,time),(xx*T,yy*T))
 return out.crop(box)
def same_visible(a,b):
 aa=np.asarray(a);bb=np.asarray(b);return bool(np.array_equal(aa[:,:,3],bb[:,:,3]) and np.array_equal(aa[aa[:,:,3]>0],bb[aa[:,:,3]>0]))
checks=[]
for name in ['base','above']:
 layer=next(x for x in m['layers']if x['name']==f'campus-{name}');a=Image.open(R/f'layers/campus-{name}.png').convert('RGBA');b=region(layer,(0,0,W,H));ok=same_visible(a,b);assert ok;checks.append({'layer':name,'allAlphaAndVisibleRgbaIdentical':ok})
effects=json.loads((R/'effects/effects.json').read_text())['effects'];layer=next(x for x in m['layers']if x['name']=='campus-native-effects');base=Image.open(R/'layers/campus-base.png').convert('RGBA');above=Image.open(R/'layers/campus-above.png').convert('RGBA')
for e in effects:
 x,y=e['origin'];w,h=e['size'];box=(x,y,x+w,y+h);renders=[]
 for i,p in enumerate(e['frames']):
  a=Image.open(R/p).convert('RGBA');b=region(layer,box,i*e['duration']);assert same_visible(a,b),(e['name'],i)
  rendered=Image.alpha_composite(Image.alpha_composite(base.crop(box),b),above.crop(box)).convert('RGB');renders.append(np.asarray(rendered,dtype=np.int16))
 diff=np.max(np.abs(np.stack(renders)-renders[0]),axis=(0,3));visible=int((diff>3).sum());assert visible>20
 checks.append({'effect':e['name'],'sourceFramesIdentical':len(e['frames']),'visibleChangedPixelsAfterForeground':visible,'nativeFrameDurationMs':e['duration']})
report={'pass':True,'scope':'Offline exact visible RGBA and alpha reconstruction from compiled32px atlases, including every source animation frame. No browser pacing, audio playback or live path claim.','checks':checks}
(R/'docs/native32-pixel-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
