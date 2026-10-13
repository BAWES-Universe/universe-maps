"""Recompose bundled native source copies and connector crops; no external module trees."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];(R/'layers').mkdir(exist_ok=True);(R/'docs').mkdir(exist_ok=True);expected_path=R/'docs/derived-layer-rebuild.json';expected={x['path']:x for x in json.loads(expected_path.read_text())['layers']} if expected_path.exists() else {};m=json.loads((R/'map/compile-manifest.json').read_text());W,H=m['world'];names=['base','foreground','glass','shade','labels'];layers={n:Image.new('RGBA',(W,H)) for n in names}
for item in m['sourceAudit']:
 if item.get('metadata') or 'targetLayer' not in item:continue
 p=R/item['copy'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],str(p)+' differs from frozen source'
 layers[item['targetLayer']].alpha_composite(Image.open(p).convert('RGBA'),tuple(item['origin']))
for c in m['connectors']:
 layers['base'].alpha_composite(Image.open(R/c['source']).convert('RGBA').crop(tuple(c['sourceCrop'])),tuple(c['destination']))
for n,im in layers.items():
 p=R/f'layers/campus-{n}.png'
 frozen=expected.get(p.relative_to(R).as_posix())
 if frozen:assert list(im.size)==frozen['size'] and im.mode==frozen['mode'] and hashlib.sha256(im.tobytes()).hexdigest()==frozen['rgbaSha256'],n+' frozen exact RGBA hash differs'
 if p.exists():
  reference=Image.open(p).convert('RGBA');assert im.size==reference.size and im.mode==reference.mode and im.tobytes()==reference.tobytes(),n+' exact RGBA reconstruction differs'
 im.save(p)
above=Image.new('RGBA',(W,H));flat=Image.new('RGBA',(W,H),(12,32,41,255))
for n in names:flat.alpha_composite(layers[n])
for n in names[1:]:above.alpha_composite(layers[n])
frozen=expected.get('layers/campus-above.png')
if frozen:assert list(above.size)==frozen['size'] and hashlib.sha256(above.tobytes()).hexdigest()==frozen['rgbaSha256'],'above frozen exact RGBA hash differs'
above.save(R/'layers/campus-above.png');flat.save(R/'docs/campus-source-overview.png');flat.resize((1600,1536),Image.Resampling.LANCZOS).save(R/'docs/campus-source-overview-half.png');print('All five bundled source layers recompose pixel-identically.')
