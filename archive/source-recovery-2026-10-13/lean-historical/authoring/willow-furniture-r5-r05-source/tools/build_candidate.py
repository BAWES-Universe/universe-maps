from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).parent))
import build_maps as B
R=Path(__file__).resolve().parents[1]; B.R=R;B.S=R/'source'
WOKAS=json.loads((R/'woka-source/manifest.json').read_text())['sprites']
old_partition=B.Map.partition_foreground

def pair(self,id,x,y):
 garden='patio' in id
 if id=='pavilion-west':x=288
 if id=='pavilion-east':x=512
 if garden:
  if x%32!=16:x+=8
  cy=y-32;ty=cy//32*32
  art=B.rgba(B.S/'table-stone.png').resize((32,29),Image.Resampling.LANCZOS)
  self.base.alpha_composite(art,(x-16,ty));self.rect((x-16,ty,x+16,ty+29))
  self.objects.append(dict(asset='table-stone',xy=[x-16,ty],size=[32,29],collision=[x-16,ty,x+16,ty+29]))
  xx=x
  coords=[('north',xx,cy-32,'south'),('south',xx,cy+32,'north')]
 else:
  dx=64 if x%32==16 else 48;tw=64 if dx==64 else 48
  self.asset('table-teak',x-tw//2,y-16,solid=(x-tw//2,y-16,x+tw//2,y-16+round(44*tw/48)),scale=tw/48)
  coords=[('left',x-dx,y,'east'),('right',x+dx,y,'west')]
 for suffix,xx,yy,direction in coords:
  cw,ch=(32,40) if garden else (40,44)
  art=B.rgba(B.S/f'chair-{direction}.png').resize((cw,ch),Image.Resampling.LANCZOS)
  px=xx-cw//2+(-3 if direction=='east' else 3 if direction=='west' else 0);py=yy-18
  self.base.alpha_composite(art,(px,py));self.used.add(f'chair-{direction}.png')
  a=np.array(art);fg=a[:,:,3].copy();fg[:round(ch*(.46 if direction=='north' else .70 if direction=='south' else .61))]=0
  self.foreground_candidate.paste(Image.fromarray(fg),(px,py))
  if not garden:
   self.rect((xx-48,yy//32*32,xx-16,yy//32*32+32) if direction=='east' else (xx+16,yy//32*32,xx+48,yy//32*32+32))
  # Front rail/back faces reserve only one row below, with clear lateral/upper entry.
  self.rect((px//32*32,(yy//32+1)*32,((px+cw-1)//32+1)*32,(yy//32+2)*32))
  self.anchor(id+'-'+suffix,xx,yy,direction,'seat')
  self.objects.append(dict(asset='chair-'+direction,xy=[px,py],size=list(art.size),seatAnchor=[xx,yy],facing=direction,panAlignment='Authentic idle-frame pelvis over cushion, feet behind front rail'))

B.Map.pair=pair
B.Map.label=lambda *args,**kwargs:None
# Use union of all actual Woka frame heads, not only the old placeholder.
def partition(self):
 g=self.grid;blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((self.H,self.W));xa=np.maximum(0,X-8);xb=np.minimum(self.W,X+8);yb=np.minimum(self.H,Y+16);v=ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa];clear=(v==0)&(X>=8)&(X+8<=self.W)&(Y+16<=self.H)
 head=np.zeros((14,32),bool)
 for w in WOKAS:
  sp=np.array(B.rgba(R/'woka-source'/w['file']))
  for row in range(4):
   for col in range(3):head|=sp[row*32:row*32+14,col*32:col*32+32,3]>32
 unsafe=np.zeros((self.H,self.W),bool)
 for yy,xx in np.argwhere(head):
  dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(self.W,self.W-dx);y0=max(0,-dy);y1=min(self.H,self.H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
 candidate=np.array(self.foreground_candidate)>32;safe=candidate&~unsafe;original=np.array(self.base);lo=original.copy();hi=np.zeros_like(lo);hi[safe]=lo[safe];lo[safe]=0;self.base=Image.fromarray(lo);self.above=Image.fromarray(hi)
 B.jw(self.r/'validation/depth-partition.json',dict(candidatePixels=int(candidate.sum()),foregroundSafePixels=int(safe.sum()),all144WokaFrameHeadsProtected=True,originalCompositeByteExact=Image.alpha_composite(self.base,self.above).tobytes()==Image.fromarray(original).tobytes(),headSafety='Union of upper14px in 144 authentic Woka frames at every body-clear integer position'))
B.Map.partition_foreground=partition
old_finish=B.Map.finish
def finish(self):
 for a in self.anchors:
  if a['id']=='tea-counter-front':a['x']=400
 # Independent actual-atlas tangent failures: reserve full foliage/raised-bed footprints.
 for name,box in [
  ('jasmine-northwest-raised-bed-rim',(320,672,416,704)),
  ('jasmine-west-dense-foliage',(320,736,416,864)),
  ('jasmine-south-flower-bed',(416,832,480,864)),
  ('pavilion-left-stair-planter-full',(320,288,352,384)),
  ('pavilion-right-stair-planter-full',(448,288,480,384)),
 ]:self.protect(name,box)
 # Re-author continuous bed/river-bank footprints from full actual-atlas boundary inspection.
 self.protect('rose-northern-flower-overhang',(192,512,256,544))
 self.protect('rose-southwest-flower-edge',(160,608,192,640))
 self.protect('main-path-west-flowering-bed',(288,416,384,560))
 self.protect('pavilion-east-base-planter',(640,320,736,384))
 self.protect('main-path-west-bed-tip',(384,544,416,576))
 for row,left in [(20,14),(21,14),(22,15),(23,16),(24,17),(25,19),(26,20),(27,22),(28,23)]:
  self.protect('river-bank-contiguous-row-'+str(row),(left*32,(row-5)*32,800,(row-4)*32))
 for row,left,right in [(25,15,17),(26,15,18),(27,16,19),(28,16,19),(29,16,19),(30,16,19),(31,16,18)]:
  self.protect('jasmine-east-raised-divider-row-'+str(row),(left*32,(row-5)*32,right*32,(row-4)*32))
 # A single coherent image-edited garden slice replaces fragmented paving stamps.
 # Registration aligns the two original circular medallion centers within a few native pixels.
 art=B.rgba(B.S/'garden-path-generous-final.png')
 mask=Image.new('L',(640,640));ImageDraw.Draw(mask).polygon([(0,128),(224,96),(336,144),(416,192),(480,224),(544,272),(576,384),(512,464),(448,480),(0,480)],fill=255);mask=mask.filter(B.ImageFilter.GaussianBlur(5))
 self.base.paste(art,(128,384),mask);mask.save(self.r/'source/path-repair-alpha-mask.png')
 # Restore the exact accepted native furniture above the edited floor, using its source assets.
 for ob in self.objects:
  if ob['asset'].startswith(('chair-','table-')) and ob['xy'][1]>500 and ob['xy'][0]<600:
   prop=B.rgba(B.S/(ob['asset']+'.png')).resize(tuple(ob['size']),Image.Resampling.LANCZOS);self.base.alpha_composite(prop,tuple(ob['xy']))
 self.objects.append(dict(asset='coherent-guided-garden-approach-edit',xy=[128,384],size=[640,640],collision=None,sceneryRepair=True))
 # Complete 96px turning floors, cleared in the image edit before admission.
 for row,cols in [(25,[8,9,10,14,16,17,18]),(26,[8,9,10,16,17,18,19]),(27,[8,9,10,11,12,19]),(24,[16,17,18])]:
  for col in cols:self.grid[row-5,col]=0
 self.grid[26-5,11:13]=1
 self.grid[26-5,7]=1
 self.grid[24-5,18]=1
 self.protect('bridge-north-raised-rail-full-two-cells',(1184,192,1248,224))
 # Closed decorative pockets are not admitted walkable cells.
 from collections import deque
 B.jw(self.r/'validation/pre-prune-grid.json',self.grid.tolist())
 reach=np.zeros_like(self.grid,bool);q=deque([(self.spawn[0]//32,self.spawn[1]//32)])
 while q:
  x,y=q.popleft()
  if not(0<=x<self.C and 0<=y<self.N) or self.grid[y,x] or reach[y,x]:continue
  reach[y,x]=True;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
 excluded=[list(map(int,v[::-1])) for v in np.argwhere((self.grid==0)&~reach)]
 self.grid[(self.grid==0)&~reach]=1
 B.jw(self.r/'validation/closed-pockets.json',{'excludedUnreachableDecorativeCells':excluded})
 # Add five scenic-only native32 rows north, preserving old world pixels at y+160.
 offset=160
 maskpath=self.r/'source/authored-walkable-mask.png'
 if maskpath.exists():
  oldmask=Image.open(maskpath);newmask=Image.new('L',(self.W,self.H+offset));newmask.paste(oldmask,(0,offset));newmask.save(maskpath)
 oldbase=self.base;bg=Image.new('RGBA',(self.W,self.H+offset));bg.paste(B.rgba(B.S/'north-context-generated.png').crop((0,0,self.W,offset)),(0,0));bg.alpha_composite(oldbase,(0,offset));self.base=bg
 fg=Image.new('L',bg.size);fg.paste(self.foreground_candidate,(0,offset));self.foreground_candidate=fg
 self.grid=np.pad(self.grid,((5,0),(0,0)),constant_values=1);self.quiet=np.pad(self.quiet,((5,0),(0,0)));self.H+=offset;self.N+=5;self.above=Image.new('RGBA',bg.size);self.spawn=(self.spawn[0],self.spawn[1]+offset)
 for a in self.anchors:a['y']+=offset
 for a in self.areas:a['y']+=offset
 for a in self.objects:
  a['xy'][1]+=offset
  if a.get('seatAnchor'):a['seatAnchor'][1]+=offset
  if a.get('collision'):
   box=list(a['collision']);box[1]+=offset;box[3]+=offset;a['collision']=box
 for a in self.fixtures:a['solidXYXY']=[a['solidXYXY'][0],a['solidXYXY'][1]+offset,a['solidXYXY'][2],a['solidXYXY'][3]+offset]
 return old_finish(self)
B.Map.finish=finish
m=B.cafe()
# Render all twelve seats from compiled runtime layers, with varied authentic sprites.
under=B.rgba(m.r/'source/runtime-base.png');over=B.rgba(m.r/'source/runtime-above.png');occ=under.copy();seats=[a for a in m.anchors if a['kind']=='seat'];proof=[]
for i,a in enumerate(seats):
 w=WOKAS[i];sheet=B.rgba(R/'woka-source'/w['file']);f={'east':7,'west':4,'north':10,'south':1}[a['direction']];sp=sheet.crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32));occ.alpha_composite(sp,(a['x']-16,a['y']-16));proof.append(dict(**a,woka=w['file'],frame=f,nativeSize=[32,32],scale=1))
occ.alpha_composite(over);occ.save(m.r/'review/all-12-wokas-native.png')
card=Image.new('RGB',(1536,480),'#182f29');d=ImageDraw.Draw(card);font=ImageFont.truetype(B.F,16)
for i,(title,box) in enumerate([('Pavilion: four different Wokas',(192,170,608,294)),('Quay and waterside',(784,260,1264,516)),('Rose and jasmine gardens',(140,528,536,830))]):
 box=(box[0],box[1]+160,box[2],box[3]+160);crop=occ.crop(box);x=i*512+(512-crop.width)//2;card.paste(crop,(x,55),crop);d.text((i*512+18,18),title,font=font,fill='white')
d.text((18,405),'100% native pixels. Real 32px repository idle frames. No invented sitting pose or avatar rescaling.',font=font,fill='white');d.text((18,435),'Furniture candidate: directional facing and lower-rail occlusion; source-native entry replay is separate.',font=font,fill='white');card.save(m.r/'review/occupied-closeups-100pct.png')
B.jw(m.r/'validation/occupied-proof.json',dict(seatCount=len(seats),uniqueWokas=len(set(p['woka'] for p in proof)),nativeIdleFrames=True,sittingAnimation=False,proof=proof))
# Original master remains exact outside furniture and the documented approach terrain repair.
empty=Image.alpha_composite(under,over);master=Image.new('RGBA',empty.size);master.paste(B.rgba(B.S/'north-context-generated.png').crop((0,0,1536,160)),(0,0));master.alpha_composite(B.rgba(B.S/'tea-garden-clear-landing-master.png'),(0,160));allowed=Image.new('L',master.size);d=ImageDraw.Draw(allowed)
for ob in m.objects:
 x,y=ob['xy'];w,h=ob['size'];d.rectangle((x,y,x+w-1,y+h-1),fill=255)
# No baked labels in this revision.
changed=np.any(np.array(empty)!=np.array(master),axis=2);outside=changed & (np.array(allowed)==0);B.jw(m.r/'validation/scenery-preservation.json',dict(outsideFurnitureAndDocumentedApproachRepairChangedPixels=int(outside.sum()),allPass=not outside.any()))
print('Saved',m.r)
