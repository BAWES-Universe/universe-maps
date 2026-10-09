#!/usr/bin/env python3
"""Register generated art; composite unchanged assets; verify geometric routes. Draw no raster furniture."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from scipy import ndimage
import numpy as np,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];M=R.parent/'art-meeting';G=Path('../universe-native-team-fixture/assets/greg-reference.png')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def measure(im):
 a=im.getchannel('A');ar=np.array(a)
 return dict(canvas=list(im.size),alphaBounds={str(t):a.point(lambda v:255 if v>=t else 0).getbbox() for t in [1,16,32,64,128,240]},nonzeroPixels=int((ar>0).sum()),opaquePixels=int((ar>=240).sum()))
master=Image.open(R/'source/workbench-master.png').convert('RGBA');ar=np.array(master.getchannel('A'))
labels,n=ndimage.label(ar>=32);count=np.bincount(labels.ravel());count[0]=0;ys,xs=np.where(labels==count.argmax());crop=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
piece=master.crop(crop).convert('RGBa').resize((128,96),Image.Resampling.LANCZOS).convert('RGBA');piece.save(R/'assets/workbench-visible-native.png')
im=Image.new('RGBA',(160,128));im.alpha_composite(piece,(16,16));im.save(R/'assets/workbench-native.png')
# Trace true foot contact bands using real source pixels only, on native padded canvas.
contact_polys=[[(18,106),(26,106),(26,111),(18,111)],[(134,106),(142,106),(142,111),(134,111)]]
mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
for p in contact_polys:d.polygon(p,fill=255)
contact=im.copy();contact.putalpha(ImageChops.multiply(im.getchannel('A'),mask));contact.save(R/'assets/workbench-contact-native.png');mask.save(R/'assets/workbench-contact-mask.png')
chairs={}
for facing in ['north','south']:
 for suffix in ['native','foreground-native','contact-native']:
  name=f'chair-{facing}-{suffix}.png';shutil.copyfile(M/'assets'/name,R/'assets'/name)
 chairs[facing]=dict(source=str(M/'assets'/f'chair-{facing}-native.png'),sha256=sha(R/'assets'/f'chair-{facing}-native.png'),unmodifiedCopy=True,**measure(Image.open(R/'assets'/f'chair-{facing}-native.png').convert('RGBA')))
geo=dict(format='shared-workbench-native-geometry-v1',units='native world pixels; rectangles half-open',status='static art and geometry proof; no runtime or live claim wiring',table=dict(visibleRectangle=[0,0,128,96],asset='assets/workbench-native.png',assetCanvas=[160,128],assetOriginRelativeToVisible=[-16,-16],collisionRectangle=[0,0,128,96],topPlaneApproximateRectangle=[0,0,128,86],ownership='shared fixed fixture; no owner or whole-table claim'),avatar=dict(source=str(G),sourceSha256=sha(G),frameSize=[32,32],scale=1,bodyRelativeToCenter=[-8,0,16,16],protectedHeadRelativeToCenter=[-16,-16,32,14]),chairs=dict(canvas=[48,64],paintedBounds=[9,8,30,36],collision='none; walkable seat allocations'),seats=[],proof=dict(canvas=[256,256],tableVisibleOrigin=[64,80],gateway=[16,128],allOtherSeatsOccupied=True))
for side,cy,facing,frame,anchor in [('north',-16,'south',1,[24,32]),('south',96,'north',10,[24,16])]:
 for ix,cx in enumerate([32,96]):
  center=[cx,cy];proofCenter=[cx+64,cy+80];py=24 if side=='north' else 224
  route=[[16,128],[32,128],[32,py],[proofCenter[0],py],proofCenter]
  geo['seats'].append(dict(id=f'{side}-{ix+1}',centerRelativeToTable=center,facing=facing,frameIndex=frame,spriteRelativeToTable=[cx-16,cy-16,32,32],bodyRelativeToTable=[cx-8,cy,16,16],chairAsset=f'assets/chair-{facing}-native.png',foregroundAsset=f'assets/chair-{facing}-foreground-native.png',chairAnchorLocal=anchor,chairOriginRelativeToTable=[cx-anchor[0],cy-anchor[1]],entryRouteProof=route,exitRouteProof=list(reversed(route)),scale=1,livePlayer=False,claim='seat/work-edge scope only; exact claim rectangle left to integrating parent'))
(R/'geometry-plan.json').write_text(json.dumps(geo,indent=2)+'\n')
base=Image.new('RGBA',(256,256));foreground=Image.new('RGBA',base.size)
for s in geo['seats']:
 x,y=s['chairOriginRelativeToTable'];pos=(x+64,y+80)
 base.alpha_composite(Image.open(R/s['chairAsset']),pos);foreground.alpha_composite(Image.open(R/s['foregroundAsset']),pos)
base.alpha_composite(im,(48,64));base.save(R/'assets/workbench-four-empty-native.png');foreground.save(R/'assets/workbench-four-foreground-native.png')
neutral=Image.new('RGBA',base.size,'#e4ddc7');neutral.alpha_composite(base);neutral.save(R/'proofs/workbench-four-empty-native.png');neutral.resize((768,768),Image.Resampling.NEAREST).save(R/'proofs/workbench-four-empty-3x.png')
greg=Image.open(G).convert('RGBA');heads=[]
for s in geo['seats']:
 f=s['frameIndex'];sprite=greg.crop(((f%3)*32,(f//3)*32,(f%3+1)*32,(f//3+1)*32));cx,cy=s['centerRelativeToTable'];cx+=64;cy+=80
 neutral.alpha_composite(sprite,(cx-16,cy-16));fa=np.array(foreground.crop((cx-16,cy-16,cx+16,cy+16)).getchannel('A'));ga=np.array(sprite.getchannel('A'));head=int(((fa[:14]>0)&(ga[:14]>0)).sum());torso=int(((fa[14:]>0)&(ga[14:]>0)).sum());heads.append(dict(seat=s['id'],scale=1,headPixelsCovered=head,torsoPixelsOccluded=torso,passed=head==0))
neutral.alpha_composite(foreground);neutral.save(R/'proofs/workbench-four-occupied-native.png');neutral.resize((768,768),Image.Resampling.NEAREST).save(R/'proofs/workbench-four-occupied-3x.png')
# Enumerate all1px center positions along each route and reverse route.16x16 body must fit scene, avoid table, and avoid all other occupied bodies.
def overlap(a,b):return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]
def sweep(route):
 for a,b in zip(route,route[1:]):
  dx=b[0]-a[0];dy=b[1]-a[1];assert not(dx and dy)
  n=max(abs(dx),abs(dy))
  for i in range(n+1):yield [a[0]+(dx//n if n else 0)*i,a[1]+(dy//n if n else 0)*i]
routes=[]
for s in geo['seats']:
 others=[[z['bodyRelativeToTable'][0]+64,z['bodyRelativeToTable'][1]+80,16,16] for z in geo['seats'] if z['id']!=s['id']]
 for direction in ['entry','exit']:
  bad=[];points=list(sweep(s[f'{direction}RouteProof']))
  for cx,cy in points:
   body=[cx-8,cy,16,16]
   if body[0]<0 or body[1]<0 or body[0]+16>256 or body[1]+16>256 or overlap(body,[64,80,128,96]) or any(overlap(body,o) for o in others):bad.append([cx,cy])
  routes.append(dict(seat=s['id'],direction=direction,sampledPositions=len(points),collisions=bad,passed=not bad))
# Diagram annotations only; no asset pixels drawn.
diagram=neutral.copy();d=ImageDraw.Draw(diagram);d.rectangle((64,80,191,175),outline='#d52850')
for i,s in enumerate(geo['seats']):
 col=['#237bc1','#2b9340','#8548c3','#c77212'][i];d.line([tuple(p) for p in s['entryRouteProof']],fill=col,width=1);cx,cy=s['centerRelativeToTable'];cx+=64;cy+=80;d.rectangle((cx-8,cy,cx+7,cy+15),outline=col);d.text((cx+17,cy-12),s['id'],fill=col)
diagram.resize((768,768),Image.Resampling.NEAREST).save(R/'proofs/workbench-four-geometry-3x.png')
checks=dict(heads=heads,routes=routes,allPassed=all(h['passed'] for h in heads) and all(r['passed'] for r in routes),scope='Offline static fixture. No runtime claim or multiplayer acceptance implied.');(R/'proofs/checks.json').write_text(json.dumps(checks,indent=2)+'\n')
manifest=dict(status='native artwork and static geometry verified',generator='built-in imagegen only; no paid external API',promptFiles=['source/workbench-prompt.txt','source/workbench-orientation-refine-prompt.txt'],table=dict(source='source/workbench-master.png',sourceSha256=sha(R/'source/workbench-master.png'),sourceCanvas=list(master.size),sourceCrop=crop,registration=dict(method='trim largest alpha>=32 connected object bounds, premultiplied LANCZOS resize to128x96, paste at16,16',artRedrawn=False,rotation=False,reflection=False),native=measure(im),visible=measure(piece),contact=dict(**measure(contact),nativePolygons=contact_polys,meaning='Actual generated foot/contact pixels; decorative antialiasing is not a physical obstacle.')),chairs=chairs,composite=dict(empty='assets/workbench-four-empty-native.png',foreground='assets/workbench-four-foreground-native.png',visibleTableOrigin=[64,80],canvas=[256,256]),checks='proofs/checks.json')
(R/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(sourceCrop=crop,table=measure(im),checks=checks)))
