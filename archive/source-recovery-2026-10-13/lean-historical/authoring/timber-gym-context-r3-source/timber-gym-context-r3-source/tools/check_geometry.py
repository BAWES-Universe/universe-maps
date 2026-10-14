"""Independently decode final TMJ; full-body, role, mat, head and start QA."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib,math,collections,copy
import numpy as np
R=Path(__file__).resolve().parents[1];A=R/'source-assets';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=load(A/'spec.json');O=R/s['slug'];B=R/'baseline'
def write(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
props=lambda o:{p['name']:p['value'] for p in o.get('properties',[])}
def decode(folder):
 m=load(folder/'map.tmj');W,H=m['width'],m['height'];below=Image.new('RGBA',(W*32,H*32));above=Image.new('RGBA',below.size);dest=below;collision=np.zeros((H,W),bool);quiet=collision.copy();atlases={t['firstgid']:Image.open(folder/t['image']).convert('RGBA') for t in m['tilesets']};tp={t['firstgid']+v['id']:props(v) for t in m['tilesets'] for v in t.get('tiles',[])}
 for t in m['tilesets']:assert atlases[t['firstgid']].size==(t['imagewidth'],t['imageheight']);assert t['tilewidth']==t['tileheight']==32
 for l in m['layers']:
  if l['name']=='floorLayer':dest=above
  if l['type']!='tilelayer':continue
  assert len(l['data'])==W*H
  for i,gid in enumerate(l['data']):
   if not gid:continue
   y,x=divmod(i,W);assert not gid&0xe0000000
   if tp.get(gid,{}).get('collides'):assert l['visible'];collision[y,x]=True
   if props(l).get('silent'):assert l['visible'];quiet[y,x]=True
   t=max((t for t in m['tilesets'] if t['firstgid']<=gid),key=lambda t:t['firstgid']);j=gid-t['firstgid'];assert j<t['tilecount']
   if l.get('visible',True) and l.get('opacity',1):tx=j%t['columns']*32;ty=j//t['columns']*32;dest.alpha_composite(atlases[t['firstgid']].crop((tx,ty,tx+32,ty+32)),(x*32,y*32))
 return m,below,above,collision,quiet
m,base,above,col,quiet=decode(O/'map32');old,ob,oa,oc,oq=decode(B/'map32');l=load(O/'source/layout.json');W,H=m['width'],m['height'];empty=Image.alpha_composite(base,above);assert [W,H]==l['dimensions']==[30,27];assert np.array_equal(col,np.array(l['collision'],bool));assert int(quiet.sum())==1 and quiet[25,15];assert not quiet[20,15];assert not col[20,15]
original=Image.alpha_composite(ob,oa);expected=Image.open(A/'generated-border-master.png').convert('RGBA').resize((960,864),Image.Resampling.LANCZOS);expected.paste(original.resize((768,608),Image.Resampling.LANCZOS),(96,96));assert expected.tobytes()==empty.tobytes()==Image.open(A/'approved-empty.png').convert('RGBA').tobytes()==Image.open(O/'review/empty-native.png').convert('RGBA').tobytes();assert base.tobytes()==Image.open(O/'assets/base.png').convert('RGBA').tobytes();assert above.tobytes()==Image.open(O/'assets/above.png').convert('RGBA').tobytes()
for f,h in load(A/'baseline-hashes.json').items():assert sha(B/f)==h
reach=np.zeros_like(col);q=collections.deque([tuple(l['spawn'])])
while q:
 x,y=q.popleft()
 if not(0<=x<W and 0<=y<H) or col[y,x] or reach[y,x]:continue
 reach[y,x]=1;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
assert not ((~col)&(~reach)).any()
def body(x,y):
 if x-8<0 or x+8>W*32 or y<0 or y+16>H*32:return False
 return not col[int(y)//32:math.ceil((y+16)/32),math.floor((x-8)/32):math.ceil((x+8)/32)].any()
anchors=[]
for a in l['anchors']:
 x,y=a['anchor'];assert body(x,y) and reach[y//32,x//32],a;anchors.append(dict(name=a['name'],anchor=[x,y],bodyClear=True,reachable=True,quiet=bool(quiet[y//32,x//32])))
cap=load(O/'source/native-spawn-outcomes.json');start=next(a for ll in m['layers'] for a in ll.get('objects',[]) if a['name']=='start');assert start==cap['start'];assert start['width']==start['height']==32;assert len(cap['distinct'])==4;sp=[]
for x,y in cap['distinct']:assert body(x,y) and quiet[y//32,x//32];sp.append(dict(x=x,y=y,bodyClear=True,quiet=True))
for x in range(start['x'],start['x']+32):
 for y in range(start['y'],start['y']+32):assert body(x,y) and quiet[y//32,x//32],(x,y)
write('NATIVE-SPAWN-CHECKS.json',dict(scope='Earlier authentic native JS four-outcome capture translated under identical32x32 start semantics; startup class NOT freshly executed. Fresh safety checks include all1024integer origins in new start rectangle.',rows=sp,allActualOutcomesSafeAndQuiet=True,conservativeIntegerRectanglePositions=1024,allConservativePositionsClearAndQuiet=True,captureSha256=sha(O/'source/native-spawn-outcomes.json'),inputMapSha256=sha(O/'map32/map.tmj')))
blocked=col.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(blocked.shape);xa=np.maximum(0,X-8);xb=np.minimum(W*32,X+8);yb=np.minimum(H*32,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W*32)&(Y+16<=H*32)&reach[Y//32,X//32]
head=np.array(load(O/'source/native-head-union.json')['mask'],bool);fg=np.array(above)[:,:,3]>32;danger=np.zeros_like(fg)
for yy,xx in np.argwhere(head):
 dx,dy=int(xx)-16,int(yy)-16;x0,x1=max(0,-dx),min(W*32,W*32-dx);y0,y1=max(0,-dy),min(H*32,H*32-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
conflict=clear&danger;assert not conflict.any(),('foreground head conflicts',np.argwhere(conflict)[:10].tolist())
write('HEAD-GEOMETRY.json',dict(scope='Exhaustive integer body-clear/reachable origins against pinned native reference-head union and actual runtime foreground alpha>32.',bodyClearPositions=int(clear.sum()),headConflicts=0,headMaskSha256=sha(O/'source/native-head-union.json'),emptyCompositionPixelExact=True))
# Source depth provenance and a positive native-frame occlusion probe.
inheritedMask=np.zeros_like(fg);inheritedMask[96:704,96:864]=np.array(oa.resize((768,608),Image.Resampling.LANCZOS))[:,:,3]>32
assert (fg[inheritedMask]).all(), 'Original scaled foreground dropped'
assert int(fg.sum())>0 and not (np.array(base)[:,:,3][fg]).any(), 'Foreground not split out of base'
sourcep=load(A/'WOKA-PROOF.json')['actors'][0];sx,sy=sourcep['position'];probeSprite=Image.open(A/'occupied-proof-overlay.png').convert('RGBA').crop((sx-16,sy-16,sx+16,sy+16));alpha=np.array(probeSprite)[:,:,3]>0;overlap=np.zeros_like(fg,dtype=np.int16)
for yy,xx in np.argwhere(alpha):
 dx,dy=int(xx)-16,int(yy)-16;x0,x1=max(0,-dx),min(W*32,W*32-dx);y0,y1=max(0,-dy),min(H*32,H*32-dy);overlap[y0:y1,x0:x1]+=fg[y0+dy:y1+dy,x0+dx:x1+dx]
valid=clear&(Y>=500)&(Y<640)&(X>=180)&(X<790);score=np.where(valid,overlap,0);py,px=np.unravel_index(score.argmax(),score.shape);assert score[py,px]>0,'No functional native-depth witness';probe=Image.new('RGBA',base.size);probe.alpha_composite(probeSprite,(int(px)-16,int(py)-16));proberender=Image.alpha_composite(Image.alpha_composite(base,probe),above);proberender.crop((max(0,int(px)-80),max(0,int(py)-80),min(960,int(px)+80),min(864,int(py)+80))).save(O/'review/depth-native-probe.png')
write('DEPTH-CHECKS.json',dict(originalForegroundPixels=int((np.array(oa)[:,:,3]>32).sum()),scaledOriginalForegroundPixels=int(inheritedMask.sum()),originalScaledForegroundMaskRetained=True,foregroundPixels=int(fg.sum()),foregroundSplitOutOfBase=True,emptyScenePixelExact=True,foregroundNativeHeadConflicts=0,addedForegroundPurpose='Traced architecture-only elevated doorway/cap polygons reallocated from unchanged accepted artwork; no plant rectangles or floor plates. Collision uses ground support footprints, not the elevated cap artwork.',probe=dict(nativeSpriteSize=[32,32],position=[int(px),int(py)],fullBodyClear=True,headClear=True,occludedNativeSpritePixels=int(score[py,px]),render='review/depth-native-probe.png'),scope='Decoded actual TMJ layer order plus authentic native32 static proof; not live render execution.'))
solid=[]
for x0,y0,x1,y1 in s['solidBaseRectsToInspect']:
 assert blocked[y0:y1,x0:x1].all(),('solid base intersects open cell',[x0,y0,x1,y1]);solid.append(dict(rect=[x0,y0,x1,y1],allPixelsSolid=True))
assert not col[18:27,14:16].any();assert not col[21,14:16].any()
wam=load(O/'map32/map.wam');ow=load(B/'map32/map.wam');expectedwam=copy.deepcopy(ow)
for a in expectedwam['areas']:a['x']=a['x']*.5+96;a['y']=a['y']*.5+96;a['width']*=.5;a['height']*=.5
assert wam==expectedwam
rolechecks=[]
roleAnchorNames= {'gym':[['instructor position'],['demo audience'],['arrival bench approach','west nook interior'],['water station approach','east nook interior']], 'retreat':[['instructor position'],[a['name'] for a in l['anchors'] if a['kind']=='mat'],['tea cushion 1 approach','tea cushion 2 approach','tea cushion 3 approach'],['rest cushion 1 approach','rest cushion 2 approach','rest cushion 3 approach']]}[s['key']]
for area,names in zip(wam['areas'],roleAnchorNames):
 for name in names:
  a=next(a for a in l['anchors'] if a['name']==name);x,y=a['anchor'];inside=area['x']<=x<area['x']+area['width'] and area['y']<=y<area['y']+area['height'];assert inside,(name,area);rolechecks.append(dict(anchor=name,areaId=area['id'],containsAnchor=True))
write('ROLE-CHECKS.json',dict(originalIdsAndPropertiesExact=True,areaBoundsTransform='x*0.5+96,y*0.5+96,width*0.5,height*0.5',adjustments=[],functionalAnchors=rolechecks,liveMediaValidation=False,explanation='Geometry and preserved configuration only. Live broadcast/LiveKit/media permissions not exercised.'))
matchecks=[]
if s['key']=='retreat':
 rgb=np.array(empty)[:,:,:3]
 for a in l['anchors']:
  if a['kind'] not in ['mat','instructor']:continue
  x,y=a['anchor'];pixels=rgb[y:y+16,x-8:x+8].astype(int);mask=(pixels[:,:,0]>=65)&(pixels[:,:,0]<=90)&(pixels[:,:,1]>=58)&(pixels[:,:,1]<=84)&(pixels[:,:,2]>=50)&(pixels[:,:,2]<=78)&(abs(pixels[:,:,0]-pixels[:,:,1]-6)<=2)&(abs(pixels[:,:,1]-pixels[:,:,2]-8)<=2);assert mask.all(),('mat containment',a['name'],int(mask.sum()));matchecks.append(dict(anchor=a['name'],bodyRect=[x-8,y,16,16],nativeBodyPixels=256,pixelsOnOriginalCharcoalFace=256,fullBodyContained=True))
 assert len(matchecks)==13
write('MAT-CONTAINMENT.json',dict(applicable=s['key']=='retreat',studentMats=12 if s['key']=='retreat' else 0,instructorMats=1 if s['key']=='retreat' else 0,rows=matchecks,method='Every native16x16body pixel must lie inside the original uniformly resampled charcoal material, including its characteristicRGB relationships. Full scene preservation separately tested.'))
proof=load(O/'source/WOKA-PROOF.json');actorOverlay=Image.open(O/'review/actor-overlay-native.png').convert('RGBA');expectedOccupied=Image.alpha_composite(Image.alpha_composite(base,actorOverlay),above);assert expectedOccupied.tobytes()==Image.open(O/'review/occupied-native.png').convert('RGBA').tobytes();sourceoverlay=Image.open(A/'occupied-proof-overlay.png').convert('RGBA');rebuilt=Image.new('RGBA',base.size)
for a in proof['actors']:
 x,y=a['position'];assert body(x,y);sprite=sourceoverlay.crop(a['sourceCrop']);assert sprite.size==(32,32) and not a['resampled'];assert hashlib.sha256(sprite.tobytes()).hexdigest()==a['cropRgbaSha256'];rebuilt.alpha_composite(sprite,(x-16,y-16))
assert rebuilt.tobytes()==actorOverlay.tobytes()
if s['key']=='retreat':assert sum(a['kind']=='mat' for a in proof['actors'])==12 and sum(a['kind']=='instructor' for a in proof['actors'])==1
for t in m['tilesets']:assert 'woka' not in t['name'].lower() and 'actor' not in t['name'].lower()
write('GEOMETRY-CHECKS.json',dict(scope='Actual runtime TMJ decode; geometry separate from live engine verification.',dimensions=[W,H,32],wholeOriginalCoreUniformScalePixelExact=True,approvedEmptyPixelExact=True,runtimeDecodeMatchesEmptyProof=True,runtimeDecodeMatchesOccupiedProof=True,walkableCells=int((~col).sum()),unreachableCells=0,quietCells=1,oldSpawnQuiet=False,allStairRowsOpen=True,anchors=anchors,solidBases=solid,native32Actors=len(proof['actors']),runtimeContainsAvatars=False,nativeBody=[16,16],sourceHashes={str(p.relative_to(O)):sha(p) for p in sorted((O/'map32').iterdir())}))
shade=Image.new('RGBA',base.size);d=ImageDraw.Draw(shade)
for y,x in np.argwhere(col):d.rectangle((int(x)*32,int(y)*32,int(x)*32+31,int(y)*32+31),fill=(255,0,60,70))
for a in l['anchors']:
 x,y=a['anchor'];d.rectangle((x-8,y,x+7,y+15),outline=(0,255,180,230))
Image.alpha_composite(empty,shade).save(O/'review/collision-overlay.png')
print('PASS geometry:',s['slug'],int((~col).sum()),'walkable cells;',int(clear.sum()),'body-clear origins; zero head conflicts;1024safe/quiet startup origins;',len(matchecks),'fully contained mat bodies')

# Doorway diagnostic: green=open floor, blue=foreground, red=ground-level support footprints.
over=Image.new('RGBA',base.size);d=ImageDraw.Draw(over)
for yy,xx in np.argwhere(~col):d.rectangle((int(xx)*32,int(yy)*32,int(xx)*32+31,int(yy)*32+31),fill=(30,255,90,45),outline=(0,255,160,150))
z=np.zeros((864,960,4),np.uint8);z[fg]=[10,120,255,135];over=Image.alpha_composite(over,Image.fromarray(z));d=ImageDraw.Draw(over)
for box in s['solidBaseRectsToInspect']:d.rectangle(tuple(box),fill=(255,20,35,130))
Image.alpha_composite(empty,over).crop((160,480,800,656)).resize((1280,352),Image.Resampling.NEAREST).save(O/'review/doorway-depth-diagnostic.png')

if s['key']=='retreat':
 witnesses=s['row15GroundWitnesses'];im=empty.copy();ov=Image.new('RGBA',im.size);dd=ImageDraw.Draw(ov)
 for a in witnesses:
  x,y=a['cell'];x0,y0,x1,y1=a['rect'];assert col[y,x] and blocked[y0:y1,x0:x1].all();dd.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(230,30,45,35),outline=(230,30,45,255));dd.rectangle((x0,y0,x1-1,y1-1),fill=(255,0,30,200))
 crop=Image.alpha_composite(im,ov).crop((176,472,784,528)).resize((1216,112),Image.Resampling.NEAREST).convert('RGB');panel=Image.new('RGB',(1216,300),'#172620');panel.paste(crop,(0,0));dd=ImageDraw.Draw(panel);dd.text((12,126),'ROW15: red cells contain physical cushion/table feet or window/plant edges. Bright red = inscribed base witness.',fill='white');dd.text((12,145),'Middle cells10-18 stay open. Newly opened row12 restores the clear strip in front of all12student mats.',fill='white')
 for i,a in enumerate(witnesses):dd.text((12+(i//5)*600,172+(i%5)*22),str(a['cell'])+' '+a['name']+' '+str(a['rect']),fill='#e5e5e5')
 panel.save(O/'review/row15-ground-witnesses.png');write('NOOK-GROUND-CHECKS.json',dict(scope='Visual solid-base witnesses explaining conservative32px collision cells; bounds are inscribed witnesses, not entire object silhouettes.',row15Witnesses=witnesses,openRow15MiddleCells=list(range(10,19)),row12OpenCells=list(range(6,24)),row12ConcreteWitnesses=[dict(anchor=[232,390],body=[224,390,16,16],clear=body(232,390)),dict(anchor=[728,390],body=[720,390,16,16],clear=body(728,390))],rationale='No remaining closed row15cell is bare floor: each includes a real cushion/table/window-plant footprint. Opening a whole native collision cell would also open that object.'))
