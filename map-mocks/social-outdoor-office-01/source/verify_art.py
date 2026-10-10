from pathlib import Path
from PIL import Image
import json,hashlib,os
R=Path(__file__).resolve().parents[1];m=json.loads((R/'map/studenthub-outdoor-office.tmj').read_text());S=json.loads((R/'source/seat-contract.json').read_text());a=R/'source/generated'; originalAssets=Path(os.environ.get('OUTDOOR_OFFICE_SOURCE',R/'source/archive-inputs'))/'source/assets'
base=Image.open(a/'layer-furniture-base.png').convert('RGBA');fg=Image.open(a/'layer-seat-foreground.png').convert('RGBA');orig=Image.open(a/'layer-furniture-repositioned.png').convert('RGBA');same=Image.alpha_composite(base,fg).tobytes()==orig.tobytes()
assert same
# Atlas reconstruction must reproduce authored layers pixel-for-pixel.
sets=[]
for t in m['tilesets']:
 im=Image.open((R/'map'/t['image']).resolve()).convert('RGBA');assert im.size==(t['imagewidth'],t['imageheight']);sets.append((t,im))
checks=[]
for l in m['layers']:
 if l['type']=='tilelayer':
  assert len(l['data'])==m['width']*m['height']; assert len(set([l['id']]))==1
  if l['name']=='permanent-collisions':continue
  out=Image.new('RGBA',(960,768))
  for i,gid in enumerate(l['data']):
   if not gid:continue
   t,im=next((t,im) for t,im in reversed(sets) if gid>=t['firstgid']);j=gid-t['firstgid'];assert j<t['tilecount'];x=j%t['columns']*m['tilewidth'];y=j//t['columns']*m['tilewidth']
   out.alpha_composite(im.crop((x,y,x+m['tilewidth'],y+m['tileheight'])),((i%m['width'])*m['tilewidth'],(i//m['width'])*m['tilewidth']))
  name='layer-furniture-base.png' if l['name']=='furniture' else f"layer-{l['name']}.png"; asset=a/name if (a/name).exists() else originalAssets/name; src=Image.open(asset).convert('RGBA')
  assert out.tobytes()==src.tobytes(),l['name'];checks.append(l['name'])
 else:
  for o in l.get('objects',[]):assert isinstance(o['visible'],bool)
assert len({l['id'] for l in m['layers']})==len(m['layers'])
assert not any(p['name'] in ['script','silent'] for p in m.get('properties',[]))
head=[]
for s in S['seats']:
 x,y=s['x'],s['y'];box=(x-12,y-16,x+12,y-6);area=fg.crop(box).getchannel('A');head.append({'seat':s['id'],'headTop10pxUncovered':not bool(area.getbbox())})
assert all(h['headTop10pxUncovered'] for h in head)
report={'scope':'Local structure/reference, exact atlas pixel roundtrip and authored mask geometry; not official target repository schema/import.','mapSha256':hashlib.sha256((R/'map/studenthub-outdoor-office.tmj').read_bytes()).hexdigest(),'furnitureSplitPixelExact':same,'atlasLayerRoundtripPass':checks,'areaVisibilityAndUniqueLayerIDsPass':True,'noScriptOrSilentProperty':True,'seatHeadClearance':head}
(R/'source/generated/art-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
