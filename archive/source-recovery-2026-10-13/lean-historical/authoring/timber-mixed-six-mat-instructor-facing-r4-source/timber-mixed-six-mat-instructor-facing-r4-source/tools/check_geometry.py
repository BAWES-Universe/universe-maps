"""Actual runtime TMJ decode; exhaustive collision, quiet, head and preservation QA."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib,math,collections,copy
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'timber-mixed-six-mat-instructor-facing-r4';B=R/'baseline';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
props=lambda o:{p['name']:p['value'] for p in o.get('properties',[])}
def decode(folder):
 m=load(folder/'map.tmj');W,H=m['width'],m['height'];below=Image.new('RGBA',(W*32,H*32));above=Image.new('RGBA',below.size);dest=below;collision=np.zeros((H,W),bool);quiet=collision.copy();atlases={s['firstgid']:Image.open(folder/s['image']).convert('RGBA') for s in m['tilesets']};tileprops={s['firstgid']+t['id']:props(t) for s in m['tilesets'] for t in s.get('tiles',[])}
 for s in m['tilesets']:assert atlases[s['firstgid']].size==(s['imagewidth'],s['imageheight']);assert s['tilewidth']==s['tileheight']==32
 for l in m['layers']:
  if l['name']=='floorLayer':dest=above
  if l['type']!='tilelayer':continue
  assert len(l['data'])==W*H
  for i,gid in enumerate(l['data']):
   if not gid:continue
   y,x=divmod(i,W);assert not gid&0xe0000000
   if tileprops.get(gid,{}).get('collides'):assert l['visible'];collision[y,x]=True
   if props(l).get('silent'):assert l['visible'];quiet[y,x]=True
   s=max((s for s in m['tilesets'] if s['firstgid']<=gid),key=lambda s:s['firstgid']);j=gid-s['firstgid'];assert j<s['tilecount']
   if l.get('visible',True) and l.get('opacity',1):tx=j%s['columns']*32;ty=j//s['columns']*32;dest.alpha_composite(atlases[s['firstgid']].crop((tx,ty,tx+32,ty+32)),(x*32,y*32))
 return m,below,above,collision,quiet
m,base,above,col,quiet=decode(O/'map32');old,ob,oa,oc,oq=decode(B/'map32');l=load(O/'source/layout.json');ol=load(B/'source/layout.json');W,H=m['width'],m['height'];assert [W,H]==l['dimensions']==[30,27];assert np.array_equal(col,np.array(l['collision'],bool));assert np.array_equal(col[6:22,3:27],oc);assert int(quiet.sum())==1 and quiet[25,15] and not quiet[20,15]
box=(96,192,864,704);assert base.crop(box).tobytes()==ob.tobytes() and above.crop(box).tobytes()==oa.tobytes()
assert Image.alpha_composite(base,above).tobytes()==Image.open(O/'review/empty-native.png').convert('RGBA').tobytes();assert base.tobytes()==Image.open(O/'assets/base.png').convert('RGBA').tobytes();assert above.tobytes()==Image.open(O/'assets/above.png').convert('RGBA').tobytes()
for oldl in old['layers']:
 if oldl['type']!='tilelayer' or oldl['name']=='spawn-only-silence':continue
 now=next(x for x in m['layers'] if x['name']==oldl['name']);assert np.array_equal(np.array(now['data']).reshape(H,W)[6:22,3:27],np.array(oldl['data']).reshape(16,24))
for a,b in zip(ol['anchors'],l['anchors']):
 expect=copy.deepcopy(a)
 for k,dx,dy in [('cell',3,6),('anchor',96,192),('floorClick',96,192)]:
  if k in expect:expect[k][0]+=dx;expect[k][1]+=dy
 assert expect==b
for a,b in zip(ol['zones'],l['zones']):expect=copy.deepcopy(a);expect['rect'][0]+=96;expect['rect'][1]+=192;assert expect==b
wam=load(O/'map32/map.wam');owam=load(B/'map32/map.wam')
for a in owam['areas']:a['x']+=96;a['y']+=192
assert wam==owam
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
for a in l['anchors']+l['seats']:
 x,y=a['anchor'];ok=body(x,y) and bool(reach[y//32,x//32]);assert ok,a;anchors.append(dict(name=a['name'],anchor=[x,y],bodyClear=True,reachable=True,quiet=bool(quiet[y//32,x//32])))
cap=load(O/'source/native-spawn-outcomes.json');start=next(a for ll in m['layers'] for a in ll.get('objects',[]) if a['name']=='start');assert start==cap['start'];assert start['width']==start['height']==32;assert len(cap['distinct'])==4;sp=[]
for x,y in cap['distinct']:assert body(x,y) and quiet[y//32,x//32];sp.append(dict(x=x,y=y,bodyClear=True,quiet=True))
for x in range(start['x'],start['x']+32):
 for y in range(start['y'],start['y']+32):assert body(x,y) and quiet[y//32,x//32],(x,y)
write('NATIVE-SPAWN-CHECKS.json',dict(scope='Authentic earlier native JS four-outcome capture translated to same32x32 area semantics; not fresh startup execution. Fresh exhaustive checks include the larger1024-position integer-origin rectangle, every position clear and quiet.',rows=sp,allActualOutcomesSafeAndQuiet=True,conservativeIntegerRectanglePositions=1024,allConservativePositionsClearAndQuiet=True,captureSha256=sha(O/'source/native-spawn-outcomes.json'),inputMapSha256=sha(O/'map32/map.tmj')))
blocked=col.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(blocked.shape);xa=np.maximum(0,X-8);xb=np.minimum(W*32,X+8);yb=np.minimum(H*32,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W*32)&(Y+16<=H*32)&reach[Y//32,X//32]
head=np.array(load(O/'source/native-head-union.json')['mask'],bool);fg=np.array(above)[:,:,3]>32;danger=np.zeros_like(fg)
for yy,xx in np.argwhere(head):
 dx,dy=int(xx)-16,int(yy)-16;x0,x1=max(0,-dx),min(W*32,W*32-dx);y0,y1=max(0,-dy),min(H*32,H*32-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
conflict=clear&danger;assert not conflict.any(),np.argwhere(conflict)[:10]
write('HEAD-GEOMETRY.json',dict(scope='Exhaustive integer body-clear/reachable positions against native reference-head union and runtime foreground alpha>32.',bodyClearPositions=int(clear.sum()),headConflicts=0,foregroundPixelExactToTranslatedR3=True,headMaskSha256=sha(O/'source/native-head-union.json')))
# Inspect every newly admitted32px cell and every old blocked scenery cell.
newmask=~col;newmask[6:22,3:27]=False;cells=[[int(x),int(y)] for y,x in np.argwhere(newmask)];assert len(cells)==28;assert all(y>=22 for x,y in cells);assert not col[22:27,14:16].any()
proof=load(O/'source/WOKA-PROOF.json');actorOverlay=Image.open(O/'review/actor-overlay-native.png').convert('RGBA');expectedOccupied=Image.alpha_composite(Image.alpha_composite(base,actorOverlay),above);assert expectedOccupied.tobytes()==Image.open(O/'review/occupied-native.png').convert('RGBA').tobytes();originalOverlay=Image.open(R/'source-assets/r3-occupied-proof-overlay.png').convert('RGBA');assert actorOverlay.crop(box).tobytes()==originalOverlay.tobytes()
for a in proof['actors']:
 x,y=a['position'];assert body(x,y),(a['anchor'],x,y)
for a in proof['actors'][-3:]:
 sprite=originalOverlay.crop(tuple(a['sourceCrop']));assert hashlib.sha256(sprite.tobytes()).hexdigest()==a['cropRgbaSha256'];assert sprite.tobytes()==actorOverlay.crop((a['position'][0]-16,a['position'][1]-16,a['position'][0]+16,a['position'][1]+16)).tobytes()
write('GEOMETRY-CHECKS.json',dict(scope='Actual runtime TMJ decode and geometry, distinct from live engine verification.',dimensions=[W,H,32],originalLayersPixelExact=True,originalTileGidsExact=True,originalCollisionExact=True,originalAnchorsTranslatedOnly=True,originalRoleIdsAndConfigExact=True,runtimeDecodeMatchesEmptyProof=True,runtimeDecodeMatchesOccupiedProof=True,walkableCells=int((~col).sum()),unreachableCells=0,quietCells=int(quiet.sum()),oldSpawnQuiet=False,anchors=anchors,newOutdoorCells=cells,newOutdoorCellCount=len(cells),outdoorFloorBasis='Conservative inscribed stone-only cells on approved Movement border; blocked rocky/planted perimeter.',native32Actors=len(proof['actors']),unchangedOldProofActors=len(proof['actors'])-3,newNative32Crops=3,sourceHashes={str(p.relative_to(O)):sha(p) for p in sorted((O/'map32').iterdir())}))
shade=Image.new('RGBA',base.size);d=ImageDraw.Draw(shade)
for y,x in np.argwhere(col):d.rectangle((int(x)*32,int(y)*32,int(x)*32+31,int(y)*32+31),fill=(255,0,60,70))
for x,y in cells:d.rectangle((x*32,y*32,x*32+31,y*32+31),outline=(0,255,180,220))
Image.alpha_composite(Image.alpha_composite(base,above),shade).save(O/'review/collision-overlay.png');print('PASS geometry:',int((~col).sum()),'walkable cells;',int(clear.sum()),'body-clear origins; zero head conflicts;1024 safe/quiet startup rectangle origins')
