"""Merge only this worker's masked pixels and ID-level geometry into a target source.
Usage: python apply_to_source.py /workspace/shared/magical-campus-current32-10
Never run against frozen09. Main build hardcoded civic polygons must consume the
included geometry-patch.json. Exterior receiver worker owns receiver material.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,sys
R=Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Provide target current source root')
T=Path(sys.argv[1]).resolve()
if 'standard32-09' in str(T) or T==Path('/workspace/shared/magical-campus-standard32-09'):raise SystemExit('Frozen09 cannot be modified')
manifest=json.loads((R/'door-source-manifest.json').read_text());geom=json.loads((R/'geometry-patch.json').read_text());log=[]
for a in manifest['artifacts']:
 target=T/a['source'];current=np.array(Image.open(target).convert('RGBA'));repl=np.array(Image.open(R/a['replacement']).convert('RGBA'));mask=np.array(Image.open(R/a['pixelReplacementMask']).convert('L'))>0
 assert current.shape==repl.shape and current.shape[:2]==mask.shape
 # Pixel ownership is only this explicit door mask; independent seating stays untouched.
 original=current.copy();current[mask]=repl[mask];assert np.array_equal(original[~mask],current[~mask]);Image.fromarray(current).save(target);log.append({'path':str(target),'ownedPixels':int(mask.sum()),'unownedPixelsUnchanged':True})
def merge_ids(path,key,updates,additions=()):
 m=json.loads(path.read_text());by={q['id']:q for q in m[key]}
 for id,delta in updates.items():
  assert id in by,('Missing collider ID',id);by[id].update(delta)
 for q in additions:
  if q['id']in by:by[q['id']].update(q)
  else:m[key].append(q)
 path.write_text(json.dumps(m,indent=2)+'\n');return m
cm=merge_ids(T/'sources/civic/module.json','blockers',geom['civicBlockerUpdates'])
cm['doorRegistration10']=json.loads((R/'importable/sources/civic/module.json').read_text())['doorRegistration10'];(T/'sources/civic/module.json').write_text(json.dumps(cm,indent=2)+'\n')
regpath=T/'sources/civic/collision-registration.json';reg=json.loads(regpath.read_text());reg['blockers']=cm['blockers'];reg['walkablePolygons']=geom['civicWalkablePolygons'];reg['registration']='Apply exact world origin0,1136 then conservativeOR32. Aligned96px civic doors; exterior receivers supplied separately.';regpath.write_text(json.dumps(reg,indent=2)+'\n')
om=merge_ids(T/'office-input/module.json','colliders',geom['officeColliderUpdates'],geom['officeColliderAdditions']);om['doorRegistration10']=json.loads((R/'importable/office-input/module.json').read_text())['doorRegistration10'];(T/'office-input/module.json').write_text(json.dumps(om,indent=2)+'\n')
p=T/'office-input/collision-grid.json';g=json.loads(p.read_text());a=np.zeros((g['height'],g['width']),np.uint8);a.flat[g['blockedIndices']]=1;c=g['cellSize']
for key,value in [('officeGridOpenRectsLocal',0),('officeGridBlockRectsLocal',1)]:
 for x,y,w,h in geom[key]:
  assert all(v%c==0 for v in [x,y,w,h]);a[y//c:(y+h)//c,x//c:(x+w)//c]=value
g['blockedIndices']=np.flatnonzero(a).tolist();p.write_text(json.dumps(g,indent=2)+'\n')
print(json.dumps({'target':str(T),'pixelMerges':log,'civicWalkablePolygons':geom['civicWalkablePolygons'],'requiredOfficeReceiverReplacements':geom['officeReceiverReplacements'],'requiredExteriorReceiverContracts':geom['exteriorDependency']},indent=2))
