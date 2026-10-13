from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'celestial-transit-garden-calm-draft';src=R/'source/proof-actors';meta=json.loads((src/'PROVENANCE.json').read_text());head=np.zeros((14,32),bool);rows=[]
for a in meta['actors']:
 for direction,rec in a['frames'].items():
  p=src/f"{a['index']}-{direction}.png";im=Image.open(p).convert('RGBA');assert im.size==(32,32);h=hashlib.sha256(im.tobytes()).hexdigest();assert h==rec['rgba_sha256'];head|=np.asarray(im)[:14,:,3]>32;rows.append(dict(actor=a['file'],direction=direction,rgbaSHA256=h,hashMatches=True))
g=np.array(json.loads((P/'source/layout.json').read_text())['grid']);blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((1536,2048));xa=np.maximum(0,X-8);xb=np.minimum(2048,X+8);yb=np.minimum(1536,Y+16);v=ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa];clear=(v==0)&(X>=8)&(X+8<=2048)&(Y+16<=1536);fg=np.asarray(Image.open(P/'source/runtime-above.png'))[:,:,3]>32;bad=np.zeros_like(clear)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(2048,2048-dx);y0=max(0,-dy);y1=min(1536,1536-dy);bad[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
report=dict(actualRepoActors=len(meta['actors']),unmodifiedNativeFrames=len(rows),headUnionPixels=int(head.sum()),safeBodyPlacements=int(clear.sum()),headConflicts=int((clear&bad).sum()),allPass=not bool((clear&bad).any()),frames=rows);(P/'validation/diverse-proof-actors.json').write_text(json.dumps(report,indent=2));assert report['allPass'];print({k:v for k,v in report.items()if k!='frames'})
