from pathlib import Path
import json
from PIL import Image
root=Path('/workspace/shared/gate-b-experience/gate/map')
out=Path(__file__).parent
m=json.loads((root/'gate.tmj').read_text()); s=m['tilewidth']; w=m['width']
sets=[]
for t in m['tilesets']:
 sets.append((t,Image.open(root/t['image']).convert('RGBA')))
sets.sort(key=lambda a:a[0]['firstgid'])
def render(reduced):
 im=Image.new('RGBA',(w*s,m['height']*s))
 for l in m['layers']:
  if l['type']!='tilelayer' or not l.get('visible',True):continue
  p={x['name']:x['value'] for x in l.get('properties',[])}
  if p.get('transitOnly') or (reduced and p.get('reducedMotionHide')):continue
  for i,g in enumerate(l['data']):
   if not g:continue
   assert g < 0x10000000,'Flipped GID not implemented'
   t,a=next((t,a) for t,a in reversed(sets) if g>=t['firstgid'])
   n=g-t['firstgid']; meta=next((v for v in t.get('tiles',[]) if v['id']==n),{}); n=meta.get('animation',[{'tileid':n}])[0]['tileid']; c=t['columns'];tw=t['tilewidth'];th=t['tileheight']
   tile=a.crop((n%c*tw,n//c*th,(n%c+1)*tw,(n//c+1)*th))
   im.alpha_composite(tile,(i%w*s,i//w*s))
 return im
for r in [False,True]:render(r).save(out/('gate-reduced-static.png' if r else 'gate-normal-first-frame.png'))
print(out)
