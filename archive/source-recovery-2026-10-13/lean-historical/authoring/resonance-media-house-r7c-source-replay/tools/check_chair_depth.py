from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
import render_runtime_proofs as pr
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';j=pr.layout;g=np.array(j['grid'],bool);fg=np.array(pr.above)[:,:,3]>32;H,W=fg.shape
head=np.zeros((14,32),bool)
for _,s in pr.frames:head|=np.array(s)[:14,:,3]>32
for r in range(4):
 for c in range(3):head|=np.array(pr.greg)[r*32:r*32+14,c*32:c*32+32,3]>32
blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
danger=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
rows=[]
chairs=[a for a in j['anchors'] if a['id'].startswith('editor-') or a['id'].startswith('screen-viewer-')]
for a in chairs:
 x,y=a['x'],a['y'];over=np.array(pr.above.crop((x-16,y-16,x+16,y+16)))[:,:,3]>32
 per=[]
 for meta,sprite in pr.frames:
  pix=np.array(sprite)[:,:,3]>32;per.append(dict(file=meta['file'],direction=meta['direction'],upper18Overlap=int((over[:18]&pix[:18]).sum()),lower14Overlap=int((over[18:]&pix[18:]).sum())))
 rows.append(dict(id=a['id'],anchor=[x,y],frameChecks=per,headClear=all(v['upper18Overlap']==0 for v in per),railVisibleOnEveryFrame=all(v['lower14Overlap']>0 for v in per)))
offsets=[(0,-12),(0,-8),(0,0),(0,1),(-8,0),(8,0),(0,8),(0,12)];cases=[];contact=Image.new('RGB',(8*128,4*128),'#252525');d=ImageDraw.Draw(contact)
for ci,a in enumerate([chairs[0],chairs[3]]):
 for fi,face in enumerate(['north','south']):
  for oi,(dx,dy) in enumerate(offsets):
   x,y=a['x']+dx,a['y']+dy;ok=bool(clear[y,x]);cases.append(dict(id=a['id'],xy=[x,y],offset=[dx,dy],facing=face,bodyClear=ok,upper14Conflict=bool(danger[y,x]) if ok else None))
   pos=(oi*128,(ci*2+fi)*128)
   if ok:im=pr.scene([dict(x=x,y=y,direction=face)]).crop((x-32,y-32,x+32,y+32)).resize((128,128),Image.Resampling.NEAREST);contact.paste(im,pos)
   d.text((pos[0]+2,pos[1]+2),f'{a["id"]} {face}',fill='white');d.text((pos[0]+2,pos[1]+15),f'{dx:+d},{dy:+d} '+('admitted' if ok else 'rear solid'),fill='white')
contact.save(P/'review/chair-motion-extrema.png')
report=dict(allPass=not (clear&danger).any() and all(r['headClear'] and r['railVisibleOnEveryFrame'] for r in rows),exhaustiveBodyClearPositions=int(clear.sum()),upper14HeadConflicts=int((clear&danger).sum()),headMask='Union of all included real proof frames and 12 native Greg frames; every integer body-clear position',arrivalChecks=rows,motionExtrema=cases,aboveAlphaPixels=int(fg.sum()),maskMethod='True asset-alpha backrest rails only, no whole-chair/ground rectangles, no head-driven rail clipping',standingOnly=True,liveGameplay=False)
(P/'validation/chair-depth-check.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['arrivalChecks','motionExtrema']});assert report['allPass']

(P/'validation/depth-partition.json').write_text(json.dumps(dict(scope='Semantic six chair-back silhouette rails, untrimmed by head mask; generated exterior paths repaired physically',foregroundPixels=int(fg.sum()),headSafeAtEveryBodyClearPosition=not (clear&danger).any(),lowerBodyOwnership=True,wholeChairMasks=False,headClipping=False),indent=2)+'\n')
