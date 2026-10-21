from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=P/'playable'
a=json.loads((R/'campus.tmj').read_text());b=json.loads((O/'campus.tmj').read_text());checks=json.loads((P/'candidate-checks.json').read_text());out={}
la={l['name']:l for l in a['layers']};lb={l['name']:l for l in b['layers']}
changed=[n for n in la if la[n]!=lb[n]]
allowed=['office-cover','persistent-collision','cafe-foreground','campus-chair-fronts','campus-bench-fronts','alcove-foreground','audience-fronts']
assert set(changed)<=set(allowed),changed
out['changedOriginalLayers']=changed
out['allOtherOriginalLayersIdentical']=True
rects=checks['collisionEditRects'];changed_cells=[]
for i,(v,w) in enumerate(zip(la['persistent-collision']['data'],lb['persistent-collision']['data'])):
 if v!=w:
  x=i%a['width']*16;y=i//a['width']*16
  assert any(bx<=x<bx+bw and by<=y<by+bh for bx,by,bw,bh in rects),(x,y)
  changed_cells.append([x,y])
out['changedCollisionCells']=len(changed_cells);out['collisionChangesBounded']=True
for s in b['tilesets']:
 q=O/s['image'];assert q.is_file(),q
 with Image.open(q) as im:assert im.size==(s['imagewidth'],s['imageheight']),(q,im.size)
valid={g for s in b['tilesets'] for g in range(s['firstgid'],s['firstgid']+s['tilecount'])};valid.add(0)
for l in b['layers']:
 if l['type']=='tilelayer':assert set(l['data'])<=valid,l['name']
out['tilesetsAndGidsValid']=True;out['tileSize']=b['tilewidth'];out['nativeScale']=checks['nativeScale'];out['exteriorAlphaUnchanged']=checks['exteriorAlphaUnchanged'];out['baseMapSha256']=hashlib.sha256((R/'campus.tmj').read_bytes()).hexdigest();out['runtimeSha256']=hashlib.sha256((R/'runtime.js').read_bytes()).hexdigest();out['candidateSha256']=hashlib.sha256((O/'campus.tmj').read_bytes()).hexdigest()
assert out['baseMapSha256']==checks['baseMapSha256'];assert out['runtimeSha256']==checks['runtimeSha256']
candidate_runtime=(O/'runtime.js').read_bytes();assert candidate_runtime.startswith((P/'campus-runtime-recovery.js').read_bytes());out['candidateRuntimeSha256']=hashlib.sha256(candidate_runtime).hexdigest();out['recoveryRuntimePreservedAsPrefix']=True
(P/'static-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
