"""Losslessly encode optimizer atlases with edge padding; record a truthful manifest."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,zipfile
R=Path(__file__).resolve().parent;root=R/'package/dist';p=root/'campus.tmj';m=json.loads(p.read_text())
for s in m['tilesets']:
 f=root/s['image'];im=Image.open(f).convert('RGBA')
 if not s.get('margin',0):
  im=Image.fromarray(np.pad(np.asarray(im),((1,1),(1,1),(0,0)),mode='edge'));s['margin']=1;s['imagewidth']+=2;s['imageheight']+=2
 im.save(f,compress_level=6)
p.write_text(json.dumps(m,separators=(',',':')))
files={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and p.name!='PUBLICATION.json'}
manifest={'status':'unpublished-test-candidate','tileSize':16,'recoveryBranch':'recovery/bawes-sky-campus-20261021','proposedDestination':'gh-pages:previews/bawes-sky-campus-recovery-20261021/','files':files}
(root/'PUBLICATION.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(R/'bawes-sky-campus-recovery.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root))
print(json.dumps({'packageBytes':sum(p.stat().st_size for p in root.rglob('*') if p.is_file()),'zipBytes':(R/'bawes-sky-campus-recovery.zip').stat().st_size}))
