from pathlib import Path
from PIL import Image,ImageDraw
import json,itertools
R=Path(__file__).resolve().parents[1];m=json.loads((R/'runtime/mechanical-orchard.tmj').read_text());layout=json.loads((R/'evidence/layout.json').read_text());T=32;W=m['width'];H=m['height'];sets=m['tilesets'];cache={s['image']:Image.open(R/'runtime'/s['image']).convert('RGBA')for s in sets}
base=Image.new('RGBA',(W*T,H*T));fore=base.copy();decoded={};floor=False
for layer in m['layers']:
 if layer['name']=='floorLayer':floor=True
 if layer['type']!='tilelayer'or layer.get('opacity',1)==0:continue
 dst=Image.new('RGBA',base.size)
 for i,g in enumerate(layer['data']):
  if not g:continue
  ts=max((s for s in sets if s['firstgid']<=g),key=lambda s:s['firstgid']);n=g-ts['firstgid'];x=n%ts['columns']*T;y=n//ts['columns']*T;dst.alpha_composite(cache[ts['image']].crop((x,y,x+T,y+T)),(i%W*T,i//W*T))
 decoded[layer['name']]=dst
 if layer.get('visible',True):(fore if floor else base).alpha_composite(dst)
sheet=Image.open(R/'source/woka-proof.png').convert('RGBA');frame=sheet.crop((32,96,64,128));rows=json.loads((R/'evidence/native-routes.json').read_text())['rows']
for name,room in layout['rooms'].items():
 ox,oy=room['offset'];w,h=room['size'];box=(ox,oy,ox+w,oy+h);im=Image.alpha_composite(base,fore).crop(box);im.save(R/'review'/f'{name}-empty.png')
 overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
 for y in range(h//32):
  for x in range(w//32):
   if layout['grid'][oy//32+y][ox//32+x]:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(230,25,65,100))
 col=Image.alpha_composite(im,overlay);ImageDraw.Draw(col).text((8,8),'OFFLINE DECODED COLLISION / NOT LIVE GAME',fill='white');col.save(R/'review'/f'{name}-collision.png')
 native=base.crop(box);seen=set()
 for row in rows:
  x,y=row['final']
  if row['pass']and ox<=x<ox+w and oy<=y<oy+h and(x,y)not in seen:
   seen.add((x,y));direction=int(row.get('direction',3));f=sheet.crop((32,direction*32,64,direction*32+32));native.alpha_composite(f,(round(x-ox-16),round(y-oy-16)))
 Image.alpha_composite(native,fore.crop(box)).save(R/'review'/f'{name}-actual-native-arrivals.png')
 # All three fully closed is a genuine reachable independent-cam state.
 full=base.copy()
 for tree in ['petal','leaf','fruit']:full.alpha_composite(decoded[tree+'-phase-2'])
 Image.alpha_composite(full,fore).crop(box).save(R/'review'/f'{name}-closed.png')
# All actual geometric states with rendered exact runtime phases, no new artwork.
card=Image.new('RGB',(1536,9*176),(25,24,20));d=ImageDraw.Draw(card)
for i,p in enumerate(itertools.product(range(3),repeat=3)):
 im=base.copy()
 for tree,n in zip(['petal','leaf','fruit'],p):
  if n:im.alpha_composite(decoded[tree+'-phase-'+str(n)])
 im=Image.alpha_composite(im,fore).crop((150,320,1380,520)).resize((492,80),Image.Resampling.NEAREST);x=(i%3)*512;y=(i//3)*176;card.paste(im,(x,y+24));d.text((x+8,y+7),str(p)+' petal / leaf / fruit (offline)',fill='white')
card.save(R/'review/all27-sculpture-states.png')
print('Decoded emitted TMJ atlas layers, actual pinned native32 arrivals and all27 three-sculpture pose combinations. Offline QA only.')
