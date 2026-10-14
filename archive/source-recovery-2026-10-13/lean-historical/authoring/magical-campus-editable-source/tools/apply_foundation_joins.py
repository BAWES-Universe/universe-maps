from pathlib import Path
from PIL import Image,ImageChops
import json,numpy as np,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R.parent/'universe-campus-joins';src=S/'layers/garden-foundation-joins.png';expected='6f71f323dd86a021f7d627b0bdc6e6b185862ac8b2d971900eba7c1e2a6a391d'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(src)==expected
old=Image.open(R/'layers/campus-base.png').convert('RGBA');join=Image.open(src).convert('RGBA');assert join.size==old.size==(3200,3072)
mask=np.asarray(join)[:,:,3]>0;g=json.loads((R/'map16/collision-grid.json').read_text());solid=np.zeros((192,200),bool);solid.flat[g['blockedIndices']]=1;assert np.all(solid.repeat(16,0).repeat(16,1)[mask])
# The new art was registered against the old complete overview, never replaces authored nonvoid pixels.
flat=Image.open(R/'docs/campus-source-overview.png').convert('RGBA');a=np.asarray(flat);oldvoid=np.all(a[:,:,:3]==[12,32,41],axis=2);assert np.all(oldvoid[mask])
archive=R/'history/before-foundation-joins';archive.mkdir(parents=True,exist_ok=True)
for f in ['layers/campus-base.png','docs/campus-source-overview.png','map16/compile-manifest.json']:
 d=archive/Path(f).name
 if not d.exists():shutil.copy2(R/f,d)
old.alpha_composite(join);old.save(R/'layers/campus-base.png');flat.alpha_composite(join);flat.save(R/'docs/campus-source-overview.png');flat.resize((1600,1536),Image.Resampling.LANCZOS).save(R/'docs/campus-source-overview-half.png')
d=R/'sources/joins';d.mkdir(exist_ok=True);shutil.copy2(src,d/src.name);shutil.copy2(S/'join-verification.json',d/'join-verification.json')
p=R/'map/compile-manifest.json';m=json.loads(p.read_text());m['sourceAudit']=[x for x in m['sourceAudit'] if x['module']!='joins'];m['sourceAudit'].append({'module':'joins','source':str(src),'copy':'sources/joins/'+src.name,'sha256':sha(src),'origin':[0,0],'size':[3200,3072],'targetLayer':'base','scale':1});m['artifactArtState']='Final joined source images;8px atlases remain historical pre-join; use current map16.';m['foundationJoins']={'sourceHash':sha(src),'filledPixels':int(mask.sum()),'onlyPreviouslyBlockedCells':True,'originalNonvoidPixelsChanged':0,'collisionChanges':0};p.write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m['foundationJoins'],indent=2))
