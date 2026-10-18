"""Compare native16 optimizer output to source, including every used pixel and tile property."""
from pathlib import Path
from PIL import Image
import json,hashlib
r=Path(__file__).resolve().parents[2]
def load(root):
 m=json.loads((root/'campus.tmj').read_text());used={gid for l in m['layers'] if l['type']=='tilelayer' for gid in l['data'] if gid};signatures={0:None}
 for ts in m['tilesets']:
  im=Image.open(root/ts['image']).convert('RGBA');props={t['id']:t for t in ts.get('tiles',[])};cols=ts['columns'];start=ts['firstgid']
  for gid in used.intersection(range(start,start+ts['tilecount'])):
   local=gid-start;x=ts.get('margin',0)+(local%cols)*(16+ts.get('spacing',0));y=ts.get('margin',0)+(local//cols)*(16+ts.get('spacing',0));meta={k:v for k,v in props.get(local,{}).items() if k!='id'}
   signatures[gid]=hashlib.sha256(im.crop((x,y,x+16,y+16)).tobytes()+json.dumps(meta,sort_keys=True).encode()).digest()
 return m,signatures
source,ss=load(r);optimized,os=load(r/'dist');checks={}
checks['nativeDimensionsUnchanged']=all(source[k]==optimized[k] for k in ['width','height','tilewidth','tileheight'])
checks['layerOrderUnchanged']=[l['name'] for l in source['layers']]==[l['name'] for l in optimized['layers']]
checks['layers']={}
for a,b in zip(source['layers'],optimized['layers']):
 if a['type']=='tilelayer':checks['layers'][a['name']]=all(ss[x]==os[y] for x,y in zip(a['data'],b['data'])) and len(a['data'])==len(b['data'])
 else:checks['layers'][a['name']]=a==b
checks['allLayerPixelsAndTilePropertiesEqual']=all(checks['layers'].values())
checks['runtimeScriptPresent']=all((r/'dist'/p['value']).exists() for p in optimized.get('properties',[]) if p['name']=='script')
checks['runtimeScriptByteIdentical']=(r/'runtime.js').read_bytes()==(r/'dist/runtime.js').read_bytes()
(r/'review/optimizer-equivalence.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2));assert all(v for k,v in checks.items() if k!='layers')
