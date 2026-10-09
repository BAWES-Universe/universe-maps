#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np
R=Path(__file__).resolve().parents[1];M=R.parent/'art-meeting'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for direction in ['north','south']:
 for suffix in ['native','foreground-native','contact-native']:
  name=f'chair-{direction}-{suffix}.png';checks.append(dict(file=f'assets/{name}',source=str(M/'assets'/name),sha256=sha(R/'assets'/name),byteIdentical=sha(R/'assets'/name)==sha(M/'assets'/name)))
 for suffix in ['foreground-native','contact-native']:
  base=np.array(Image.open(R/'assets'/f'chair-{direction}-native.png').convert('RGBA'));overlay=np.array(Image.open(R/'assets'/f'chair-{direction}-{suffix}.png').convert('RGBA'));mask=overlay[:,:,3]>0;assert np.array_equal(overlay[mask],base[mask])
base=np.array(Image.open(R/'assets/workbench-native.png').convert('RGBA'));contact=np.array(Image.open(R/'assets/workbench-contact-native.png').convert('RGBA'));mask=contact[:,:,3]>0;contact_pass=np.array_equal(base[mask],contact[mask])
report=dict(chairCopies=checks,tableContactUnchangedSourcePixels=contact_pass,artworkMethod='Generated table pixels; only alpha-bound trim, registered premultiplied resize, pixel-subset masks and compositing. No painted or generated character modifications; no sprite rotations/reflections.',allPassed=all(c['byteIdentical'] for c in checks) and contact_pass)
(R/'proofs/source-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
manifest=json.loads((R/'asset-manifest.json').read_text())
for name,key in [('workbench-four-empty-native','base'),('workbench-four-foreground-native','foreground')]:
 im=Image.open(R/'assets'/f'{name}.png');b=im.getchannel('A').getbbox();manifest['composite'][key+'AlphaBounds']=b;manifest['composite'][key+'BoundsRelativeToVisibleTable']=[b[0]-64,b[1]-80,b[2]-b[0],b[3]-b[1]]
manifest['sourceIntegrity']='proofs/source-integrity.json';(R/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(report))
