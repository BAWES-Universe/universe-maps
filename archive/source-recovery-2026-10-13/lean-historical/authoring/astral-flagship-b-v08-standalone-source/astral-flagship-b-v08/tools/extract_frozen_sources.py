"""Copy A read-only inputs and derive exact artwork ownership masks for B's surface proposal."""
from PIL import Image,ImageDraw,ImageChops
from pathlib import Path
import json,shutil,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];A=R.parent/'grand-auditorium-07-clean';V3=A/'source/reuse-v03';V5=A/'source/reuse-v05';S=R/'source';W,H=2560,1920
rgba=lambda p:Image.open(p).convert('RGBA');blank=lambda:Image.new('RGBA',(W,H));j=lambda p:json.loads(p.read_text())
for rel in ['assets/runtime-base.png','assets/runtime-above.png','assets/greg-reference.png','review/qa-actors-only.png','source/runtime-layout.json','source/garden-layout.json','source/collision-grid.json','source/quiet-grid.json','source/seats.json']:
 shutil.copy2(A/rel,S/'frozen-a'/Path(rel).name)
shutil.copy2(R.parent/'grand-auditorium-05-roofless-garden/source/garden-walkable-mask.png',R/'masks/garden-original-footprint.png')
# Furniture source RGBA is unchanged. Opaque base pixels stay exact; translucent edges recompose over new material.
furn=blank();furnbelow=blank();cfg=j(A/'source/runtime-layout.json');components=[]
for p in cfg['furniture']:
 if p['x']<1536:continue
 path=A/p['asset'] if p['asset'].startswith('source/') else V3/p['asset']
 im=rgba(path);furn.alpha_composite(im,(p['x'],p['y']));low=rgba(A/p['belowAsset']) if p.get('belowAsset') else im;furnbelow.alpha_composite(low,(p['x'],p['y']));components.append({'id':p['id'],'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'artXYWH':[p['x'],p['y'],im.width,im.height]})
# Exact native structural alpha: coffee frame, deck rails and garden pavilion.
struct=blank()
struct.alpha_composite(rgba(R.parent/'grand-auditorium-03-foyer-terrace/assets/coffee-pergola.png'),(1696,1088))
rail=rgba(R.parent/'grand-auditorium-03-foyer-terrace/assets/terrace-rail.png')
for y in [1040,1712]:
 for x in range(1536,2496,rail.width):struct.alpha_composite(rail.crop((0,0,min(rail.width,2496-x),48)),(x,y))
# Keep the real open garden gate; do not reintroduce a rail across it.
struct.paste((0,0,0,0),(2144,1024,2272,1088))
for x in [2120,2272]:struct.alpha_composite(rail.crop((0,0,24,48)),(x,1040))
for y in [1056,1392]:struct.alpha_composite(rgba(R.parent/'grand-auditorium-03-foyer-terrace/assets/terrace-east-rail.png'),(2460,y))
struct.alpha_composite(rgba(V5/'assets/pergola-below.png'))
# Doorway cap pixels remain frozen, exact geometry/threshold art are not owned by B.
mask=np.asarray(struct.getchannel('A'))==255
mask|=np.asarray(furnbelow.getchannel('A'))==255
# Preserve all above-layer art. These pixels are also protected in frozen base for exact edges.
# The entire frozen above layer stays untouched, but its translucent pixels do not freeze old ground underneath.
for box in [(1408,440,1568,552)]:
 x0,y0,x1,y1=box;mask[y0:y1,x0:x1]=True
Image.fromarray(mask.astype('uint8')*255).save(R/'masks/protected-objects-and-doors.png')
Image.fromarray((np.asarray(furnbelow.getchannel('A'))==255).astype('uint8')*255).save(R/'masks/protected-furniture.png')
Image.fromarray(((np.asarray(furnbelow.getchannel('A'))>0)&(np.asarray(furnbelow.getchannel('A'))<255)).astype('uint8')*255).save(R/'masks/furniture-translucent-edges.png')
furn.save(S/'overlays/furniture-source-alpha.png');furnbelow.save(S/'overlays/furniture-below-source-alpha.png');struct.save(S/'overlays/structure-source-alpha.png')
# Reapply real authored translucent shading over the new material; never preserve the bad
# stage-light bake under a shadow polygon and never erase the shadow shape.
shadow=blank();d=ImageDraw.Draw(shadow)
for x in range(1704,2113,48):d.polygon([(x,1116),(x+10,1116),(x+54,1288),(x+44,1288)],fill=(63,49,25,18))
shadow.save(S/'overlays/coffee-cast-shadow.png')
for n in ['terrace-shadows-contact','pergola-shadows-below','shadows-exterior-cast']:shutil.copy2(V5/'assets'/f'{n}.png',S/'overlays'/f'{n}.png')
record={'frozenA':str(A),'frozenInputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in (S/'frozen-a').iterdir()},'protectedFurnitureComponents':components,'readOnlyOriginals':True}
(S/'FROZEN-INPUTS.json').write_text(json.dumps(record,indent=2)+'\n')
print('Frozen A copied; masks and exact shadow sources extracted.')
