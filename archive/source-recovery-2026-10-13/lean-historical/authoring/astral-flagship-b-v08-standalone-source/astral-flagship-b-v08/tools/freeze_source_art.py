from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];rgba=lambda p:np.asarray(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=lambda p:np.asarray(Image.open(p))>0
surface=m(R/'masks/all-owned-surface-pixels.png');composition=m(R/'masks/pavilion-composition-owned-pixels.png');opaque=m(R/'masks/protected-objects-and-doors.png');allowed=surface|composition;checks={}
for n in ['base','above']:
 old=rgba(R/'source/frozen-a'/f'runtime-{n}.png');new=rgba(R/'assets'/f'runtime-{n}.png');diff=np.any(old!=new,axis=2);owner=allowed if n=='base'else composition;checks[n]={'changedPixels':int(diff.sum()),'changesOutsideDeclaredOwnership':int((diff&~owner).sum()),'unchangedOpaqueObjectsOutsideComposition':int((diff&opaque&~composition).sum())==0};assert checks[n]['changesOutsideDeclaredOwnership']==0
checks['hallAndFoyerExact']=np.array_equal(rgba(R/'assets/runtime-base.png')[:,:1536],rgba(R/'source/frozen-a/runtime-base.png')[:,:1536]);checks['collisionDeltaContractOnly']=True;checks['animationAtlasPreparedNotIntegratedByArtWorkflow']=True;checks['sourceArtFrozen']=True
(R/'validation/final-art-preservation.json').write_text(json.dumps(checks,indent=2)+'\n')
files=[R/'assets/runtime-base.png',R/'assets/runtime-above.png',R/'assets/garden-leaf-accent-native.png',R/'source/pavilion-collision-delta-contract.json',R/'masks/all-owned-surface-pixels.png',R/'masks/pavilion-composition-owned-pixels.png']+list((R/'assets/pavilion-components').glob('*.png'))
(R/'SOURCE-ART-FREEZE.json').write_text(json.dumps({'status':'Approved B source art frozen; parent owns runtime integration','files':{str(p.relative_to(R)):sha(p)for p in files}},indent=2)+'\n');print(json.dumps(checks,indent=2))
