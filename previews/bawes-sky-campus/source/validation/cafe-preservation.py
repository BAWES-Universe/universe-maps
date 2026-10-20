"""Verify accepted interior pixels/collision and scenic exterior are unchanged."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import json,subprocess,hashlib
r=Path(__file__).resolve().parents[2];base='45b7535';prefix='previews/bawes-sky-campus/'
def prior(p):return subprocess.check_output(['git','show',base+':'+prefix+p],cwd=r)
a=json.loads(prior('campus.tmj'));b=json.loads((r/'campus.tmj').read_text())
checks={};images={}
def signature(m,g,old):
 if not g:return None
 t=next(t for t in reversed(m['tilesets']) if t['firstgid']<=g);key=(old,t['image'])
 if key not in images:images[key]=Image.open(BytesIO(prior(t['image'])) if old else r/t['image']).convert('RGBA')
 n=g-t['firstgid'];x=t.get('margin',0)+(n%t['columns'])*(16+t.get('spacing',0));y=t.get('margin',0)+(n//t['columns'])*(16+t.get('spacing',0));return hashlib.sha256(images[key].crop((x,y,x+16,y+16)).tobytes()).digest()
for name in [l['name'] for l in a['layers'] if l['type']=='tilelayer' and l['name'].startswith(('office-','meeting-'))]:
 x=next(l for l in a['layers'] if l['name']==name);y=next(l for l in b['layers'] if l['name']==name)
 pairs=set(zip(x['data'],y['data']));checks[name]=all(signature(a,i,True)==signature(b,j,False) for i,j in pairs)
checks['scenerySourceImagesByteIdentical']=all(prior(t['image'])==(r/t['image']).read_bytes() for t in a['tilesets'] if t['name'].startswith('scenery-and-campus'))
# Only authorized exterior gate proximity changes; accepted interior logic is exact.
checks['runtimeOnlyExteriorProximityChanged']=prior('runtime.js').decode().replace('const near=contains(position,door.box,80);',"const near=contains(position,door.box,door.id==='office-front'&&!contains(position,layout.cutaway)?64:80);").replace('   if(open||!moving){',"   // Exterior approach settles before gate layers change, avoiding path-target drift.\n   if(door.id==='office-front'&&moving&&!contains(position,layout.cutaway))continue;\n   if(open||!moving){")== (r/'runtime.js').read_text()
x=next(l['data'] for l in a['layers'] if l['name']=='persistent-collision');y=next(l['data'] for l in b['layers'] if l['name']=='persistent-collision');cols=b['width']
checks['officeCollisionIdentical']=all(bool(x[ty*cols+tx])==bool(y[ty*cols+tx]) for ty in range(2448//16,3040//16) for tx in range(2944//16,5088//16))
checks['foregroundAbovePlayers']=next(i for i,l in enumerate(b['layers']) if l['name']=='cafe-foreground')>next(i for i,l in enumerate(b['layers']) if l['name']=='floorLayer')
(r/'review/cafe-preservation.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2));assert all(checks.values())
