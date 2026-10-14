"""Recompose bundled native source copies and connector crops; no external module trees."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];m=json.loads((R/'map/compile-manifest.json').read_text());W,H=m['world'];names=['base','foreground','glass','shade','labels'];layers={n:Image.new('RGBA',(W,H)) for n in names}
for item in m['sourceAudit']:
 if item.get('metadata') or 'targetLayer' not in item:continue
 p=R/item['copy'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],str(p)+' differs from frozen source'
 layers[item['targetLayer']].alpha_composite(Image.open(p).convert('RGBA'),tuple(item['origin']))
for c in m['connectors']:
 layers['base'].alpha_composite(Image.open(R/c['source']).convert('RGBA').crop(tuple(c['sourceCrop'])),tuple(c['destination']))
for n,im in layers.items():
 p=R/f'layers/campus-{n}.png'
 if p.exists():
  reference=Image.open(p).convert('RGBA');assert im.size==reference.size and im.mode==reference.mode and im.tobytes()==reference.tobytes(),n+' exact RGBA reconstruction differs'
 im.save(p)
above=Image.new('RGBA',(W,H));flat=Image.new('RGBA',(W,H),(12,32,41,255))
for n in names:flat.alpha_composite(layers[n])
for n in names[1:]:above.alpha_composite(layers[n])
above.save(R/'layers/campus-above.png');flat.save(R/'docs/campus-source-overview.png');flat.resize((1600,1536),Image.Resampling.LANCZOS).save(R/'docs/campus-source-overview-half.png');print('All five bundled source layers recompose pixel-identically.')
