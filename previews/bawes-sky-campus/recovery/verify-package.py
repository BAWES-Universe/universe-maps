"""Compare all used pixels/properties and resolved animation frames across packaging."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent
def load(root):
 m=json.loads((root/'campus.tmj').read_text());used={g for l in m['layers'] if l['type']=='tilelayer' for g in l['data'] if g};sig={0:None}
 for s in m['tilesets']:
  im=Image.open(root/s['image']).convert('RGBA');meta={t['id']:t for t in s.get('tiles',[])}
  def pixels(n):
   x=s.get('margin',0)+(n%s['columns'])*(16+s.get('spacing',0));y=s.get('margin',0)+(n//s['columns'])*(16+s.get('spacing',0))
   return hashlib.sha256(im.crop((x,y,x+16,y+16)).tobytes()).hexdigest()
  for g in used.intersection(range(s['firstgid'],s['firstgid']+s['tilecount'])):
   n=g-s['firstgid'];p={k:v for k,v in meta.get(n,{}).items() if k not in ['id','animation']}
   frames=[(pixels(f['tileid']),f['duration']) for f in meta.get(n,{}).get('animation',[])]
   sig[g]=(pixels(n),json.dumps(p,sort_keys=True),frames)
 return m,sig
a,sa=load(R/'package');b,sb=load(R/'package/dist')
checks={'dimensions':all(a[k]==b[k] for k in ['width','height','tilewidth','tileheight']), 'layerOrder':[l['name'] for l in a['layers']]==[l['name'] for l in b['layers']], 'layers':{}}
for x,y in zip(a['layers'],b['layers']):
 checks['layers'][x['name']]=x==y if x['type']!='tilelayer' else len(x['data'])==len(y['data']) and all(sa[g]==sb[h] for g,h in zip(x['data'],y['data']))
checks['runtimeIdentical']=(R/'package/runtime.js').read_bytes()==(R/'package/dist/runtime.js').read_bytes()
checks['pass']=checks['dimensions'] and checks['layerOrder'] and checks['runtimeIdentical'] and all(checks['layers'].values())
(R/'evidence/package-equivalence.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2));assert checks['pass']
