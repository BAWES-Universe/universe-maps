#!/usr/bin/env python3
"""Verify real source-pixel masks and delivered native artifact dimensions."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];m=json.loads((R/'asset-manifest.json').read_text());checks=[]
for name,data in m['assets'].items():
 p=R/data['source'];checks.append(dict(asset=name,test='original master hash',passed=hashlib.sha256(p.read_bytes()).hexdigest()==data['sourceSha256']))
 native=Image.open(R/'assets'/f'{name}-native.png').convert('RGBA');a=np.array(native)
 x,y,w,h=data['registration']['targetVisibleRectangle'];checks.append(dict(asset=name,test='native visible size',passed=list(native.getbbox())==[x,y,x+w,y+h]))
 for kind in ['foreground','contact']:
  p=R/'assets'/f'{name}-{kind}-native.png'
  if not p.exists():continue
  component=np.array(Image.open(p).convert('RGBA'));selected=component[:,:,3]>0;checks.append(dict(asset=name,test=kind+' exact source RGBA',selectedPixels=int(selected.sum()),passed=bool(np.array_equal(component[selected],a[selected]))))
p=R/'assets/table-small-side-contact-foreground-native.png';component=np.array(Image.open(p).convert('RGBA'));native=np.array(Image.open(R/'assets/table-small-native.png').convert('RGBA'));selected=component[:,:,3]>0;checks.append(dict(asset='table-small',test='side table contact exact source RGBA',selectedPixels=int(selected.sum()),passed=bool(np.array_equal(component[selected],native[selected]))))
for name,size in [('small-four-cardinal',[256,192]),('conference-six',[256,384])]:
 for suffix in ['empty-native','foreground-native']:
  im=Image.open(R/'assets'/f'{name}-{suffix}.png');checks.append(dict(asset=f'{name}-{suffix}',test='transparent RGBA and native dimensions',passed=im.mode=='RGBA' and list(im.size)==size and im.getchannel('A').getextrema()==(0,255)))
for p in ['pixel-checks.json','route-checks.json']:
 d=json.loads((R/'proofs'/p).read_text());checks.append(dict(asset=p,test='reported checks pass',passed=d['passed']))
out=dict(passed=all(c['passed'] for c in checks),checks=checks);(R/'proofs/source-integrity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],checks=len(checks))))
