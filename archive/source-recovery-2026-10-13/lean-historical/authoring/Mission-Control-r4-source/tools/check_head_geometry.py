from pathlib import Path
import json,hashlib,sys,math,collections
import numpy as np
from PIL import Image,ImageDraw
root=Path(sys.argv[1]);out=Path(__file__).resolve().parents[1]/'geometry-checks'/root.name;out.mkdir(parents=True,exist_ok=True)
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
props=lambda o:{p['name']:p['value'] for p in o.get('properties',[])}
issues=[];checks={};mfile=next((root/'map32').glob('*.tmj'));m=load(mfile);W=m['width'];H=m['height'];T=m['tilewidth'];assert T==32==m['tileheight'];checks['dimensions']=[W,H,T]
def flatten(ls):
 for l in ls:
  if l['type']=='group':yield from flatten(l['layers'])
  else:yield l
layers=list(flatten(m['layers']));sets=m['tilesets'];tiles={};atlas={}
for s in sets:
 if 'source' in s:raise ValueError('External tileset needs explicit audit')
 a=Image.open(mfile.parent/s['image']).convert('RGBA');assert a.size==(s['imagewidth'],s['imageheight']);assert s['tilewidth']==s['tileheight']==32
 atlas[s['firstgid']]=a
 for t in s.get('tiles',[]):tiles[s['firstgid']+t['id']]=props(t)
collision=np.zeros((H,W),bool);quiet=np.zeros((H,W),bool);below=Image.new('RGBA',(W*T,H*T));above=Image.new('RGBA',below.size);dest=below;recons={}
for l in layers:
 if l['name']=='floorLayer':dest=above
 if l['type']!='tilelayer':continue
 assert len(l['data'])==W*H
 arr=np.array(l['data']).reshape(H,W)
 col=np.vectorize(lambda gid:tiles.get(int(gid)&0x1fffffff,{}).get('collides',False))(arr)
 if col.any():
  collision|=col
  if not l.get('visible',True):issues.append('Collision layer invisible flag '+l['name'])
 if props(l).get('silent'):quiet|=arr!=0
 im=Image.new('RGBA',below.size)
 for i,g in enumerate(l['data']):
  if not g:continue
  if g&0xe0000000:raise ValueError('Flipped tiles need explicit reconstruction')
  s=max((s for s in sets if s['firstgid']<=g),key=lambda s:s['firstgid']);j=g-s['firstgid'];assert j<s['tilecount'];x=j%s['columns']*T;y=j//s['columns']*T
  im.paste(atlas[s['firstgid']].crop((x,y,x+T,y+T)),((i%W)*T,(i//W)*T))
 recons[l['name']]=im
 if l.get('visible',True) and l.get('opacity',1)!=0:dest.alpha_composite(im)
below.save(out/'decoded-below.png');above.save(out/'decoded-above.png');empty=below.copy();empty.alpha_composite(above);empty.save(out/'decoded-empty.png')
checks['source_reconstruction']={}
for lname,paths in {'architecture-and-furniture':['assets/base.png'],'seat-backs':['assets/above.png'],'ground-and-objects':['source/runtime-base.png'],'foreground':['source/runtime-above.png']}.items():
 if lname not in recons:continue
 for p in paths:
  if (root/p).exists():
   src=np.array(Image.open(root/p).convert('RGBA'));dec=np.array(recons[lname]);src[src[:,:,3]==0]=0;dec[dec[:,:,3]==0]=0;ok=bool(np.array_equal(src,dec));checks['source_reconstruction'][p]=ok
   if not ok:issues.append('Atlas reconstruction differs '+p)
starts=[]
for l in layers:
 for a in l.get('objects',[]):
  if a.get('name')=='start' or props(a).get('start'):starts.append(a)
def body(x,y):
 if x-8<0 or x+8>W*T or y<0 or y+16>H*T:return False
 return not collision[int(y)//T:math.ceil((y+16)/T),int(x-8)//T:math.ceil((x+8)/T)].any()
def domain(a,k):
 lo=a[k]+16;hi=a[k]+a['width' if k=='x' else 'height']-16;n=hi-lo+1
 return range(math.floor(min(lo,lo+n-(1e-9 if n>0 else -1e-9))),math.floor(max(lo,lo+n-(1e-9 if n>0 else -1e-9)))+1)
spawnrows=[]
for a in starts:
 xs=list(domain(a,'x'));ys=list(domain(a,'y'));bad=[]
 for x in xs:
  for y in ys:
   if not body(x,y) or not quiet[y//32,x//32]:bad.append([x,y])
 spawnrows.append(dict(name=a['name'],xRange=[min(xs),max(xs)],yRange=[min(ys),max(ys)],samples=len(xs)*len(ys),bad=bad[:20],badCount=len(bad)))
 if bad:issues.append('Random spawn unsafe/unsilenced '+a['name'])
checks['random_spawns']=spawnrows
start=starts[0];sx=start['x']+start['width']//2;sy=start['y']+start['height']//2
reach=np.zeros_like(collision);q=collections.deque([(sx//32,sy//32)])
while q:
 x,y=q.popleft()
 if x<0 or y<0 or x>=W or y>=H or collision[y,x] or reach[y,x]:continue
 reach[y,x]=1;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
checks['walkable_cells']=int((~collision).sum());checks['unreachable_cells']=int((~collision&~reach).sum());checks['quiet_cells']=int(quiet.sum())
layout=load(root/'source/layout.json') if (root/'source/layout.json').exists() else {};anchors=[]
for a in layout.get('anchors',[])+layout.get('seats',[]):
 if 'anchor' in a:x,y=a['anchor']
 elif 'x' in a:x,y=a['x'],a['y']
 elif 'cell' in a:x,y=a['cell'][0]*32+16,a['cell'][1]*32+15
 else:continue
 anchors.append(dict(id=a.get('id',a.get('name')),x=x,y=y,bodyClear=body(x,y),reachable=bool(reach[y//32,x//32]),silent=bool(quiet[y//32,x//32])))
checks['anchors']=anchors
for a in anchors:
 if not a['bodyClear'] or not a['reachable']:issues.append('Invalid anchor '+str(a['id']))
# Exhaustive native body-clear integer positions and union of all reference head frames.
blocked=collision.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(blocked.shape);xa=np.maximum(0,X-8);xb=np.minimum(W*32,X+8);yb=np.minimum(H*32,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W*32)&(Y+16<=H*32)&reach[Y//32,X//32]
greg=Path(__file__).resolve().parents[1]/'source-assets/greg-reference.png';g=np.array(Image.open(greg).convert('RGBA'));head=np.zeros((14,32),bool)
for sprite in [greg]+sorted(greg.parent.glob('woka-proof-*.png')):
 g=np.array(Image.open(sprite).convert('RGBA'))
 for r in range(4):
  for c in range(3):head|=g[r*32:r*32+14,c*32:c*32+32,3]>32
head|=np.array(json.loads((greg.parent/'reference-head-mask.json').read_text()),dtype=bool)
checks['headReferenceSheets']=9
fg=np.array(above)[:,:,3]>32;danger=np.zeros_like(fg)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W*32,W*32-dx);y0=max(0,-dy);y1=min(H*32,H*32-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
conflict=clear&danger;np.savez_compressed(out/'geometry-masks.npz',clear=clear,danger=danger,conflict=conflict,collision=collision);checks['body_clear_positions']=int(clear.sum());checks['head_conflicts']=int(conflict.sum());checks['head_conflict_examples']=[[int(x),int(y)] for y,x in np.argwhere(conflict)[:30]]
if conflict.any():issues.append('Reachable foreground head conflicts')
overlay=empty.copy();shade=Image.new('RGBA',empty.size);d=ImageDraw.Draw(shade)
for y,x in np.argwhere(collision):d.rectangle((int(x)*32,int(y)*32,int(x)*32+31,int(y)*32+31),fill=(255,0,60,70))
for a in anchors:d.ellipse((a['x']-3,a['y']-3,a['x']+3,a['y']+3),fill='#00ffaa')
overlay.alpha_composite(shade);overlay.save(out/'collision-overlay.png')
checks['media_areas']=[]
for wf in (root/'map32').glob('*.wam'):
 wam=load(wf);areas=wam.get('areas',[]);ids={a['id'] for a in areas if any(p['type']=='speakerMegaphone' for p in a.get('properties',[]))}
 for a in areas:
  ps=a.get('properties',[]);checks['media_areas'].append(a)
  for p in ps:
   if p['type']=='start':
    margin=0 if p.get('isDefault') else 16
    xs=range(math.floor(a['x']+margin),math.floor(a['x']+a['width']-margin)+1);ys=range(math.floor(a['y']+margin),math.floor(a['y']+a['height']-margin)+1);bad=[]
    for x in xs:
     for y in ys:
      if not body(x,y) or not quiet[y//32,x//32]:bad.append([x,y])
    checks['random_spawns'].append(dict(name='WAM '+a['id'],margin=margin,samples=len(xs)*len(ys),bad=bad[:20],badCount=len(bad)))
    if bad:issues.append('Random WAM spawn unsafe/unsilenced '+a['id'])
  for p in ps:
   if p['type']=='listenerMegaphone' and p['speakerZoneName'] not in ids:issues.append('Listener references missing speaker '+a['id'])
  a['reachable_membership_positions']=int((clear&(X>=a['x'])&(X<=a['x']+a['width'])&(Y+16>=a['y'])&(Y+16<=a['y']+a['height'])).sum())
checks['issues']=issues;checks['scope']='Independent actual-TMJ atlas decode, collision-derived cardinal connectivity and exhaustive integer source body/head geometry; not native route replay, browser, physics keyboard, devices, media or deployment.'
checks['input_hashes']={str(p.relative_to(root)):sha(p) for p in sorted((root/'map32').glob('*')) if p.is_file()};(out/'independent-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps({k:v for k,v in checks.items() if k not in ['anchors','media_areas','input_hashes']},indent=2))
