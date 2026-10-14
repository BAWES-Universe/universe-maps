"""Deterministic, self-contained r4 compiler from frozen r3 runtime atlas inputs.
Only generated border is resized; old artwork, tile GIDs and geometry are translated.
"""
from pathlib import Path
import copy,json,hashlib,shutil,math
from PIL import Image
R=Path(__file__).resolve().parents[1]; B=R/'baseline'; O=R/'timber-mixed-six-mat-instructor-facing-r4'; W,H,T=30,27,32; DX,DY=96,192; CX,CY=3,6
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def decode(m,folder):
 below=Image.new('RGBA',(m['width']*32,m['height']*32));above=Image.new('RGBA',below.size);dest=below;atlases={s['image']:Image.open(folder/s['image']).convert('RGBA') for s in m['tilesets']}
 for l in m['layers']:
  if l['name']=='floorLayer':dest=above
  if l['type']!='tilelayer' or not l.get('visible',True) or l.get('opacity',1)==0:continue
  for i,gid in enumerate(l['data']):
   if not gid:continue
   assert not gid&0xe0000000
   s=max((s for s in m['tilesets'] if s['firstgid']<=gid),key=lambda s:s['firstgid']);idx=gid-s['firstgid'];assert idx<s['tilecount']
   a=atlases[s['image']];x=idx%s['columns']*32;y=idx//s['columns']*32
   dest.alpha_composite(a.crop((x,y,x+32,y+32)),((i%m['width'])*32,(i//m['width'])*32))
 return below,above
old=read(B/'map32/map.tmj');lold=read(B/'source/layout.json');freeze=read(B/'r3-freeze.json')
for p in (B/'map32').iterdir():assert sha(p)==freeze['runtimeFiles']['map32/'+p.name],p
for p in (B/'source').iterdir():assert sha(p)==freeze['runtimeFiles']['source/'+p.name],p
for d in ['map32','assets','source','review']: (O/d).mkdir(parents=True,exist_ok=True)
m=copy.deepcopy(old);m.update(width=W,height=H,nextlayerid=8)
for p in m['properties']:
 if p['name']=='name':p['value']='Timber Yoga Studio · woodland approach r4'
 if p['name']=='status':p['value']='Unpublished r4 candidate; source tests distinct from user approval and live validation'
for l in m['layers']:
 if l['type']=='tilelayer':
  data=[0]*(W*H)
  for y in range(old['height']):
   for x in range(old['width']):data[(y+CY)*W+x+CX]=l['data'][y*old['width']+x]
  l.update(width=W,height=H,data=data)
 else:
  for a in l.get('objects',[]):a['x']+=DX;a['y']+=DY
# Reuse all original packed atlases byte-for-byte and preserve every GID.
for s in m['tilesets']:shutil.copyfile(B/'map32'/s['image'],O/'map32'/s['image'])
# New tiles only outside the immutable original world rectangle.
master=Image.open(R/'source-assets/generated-border-master.png').convert('RGBA');border=master.resize((W*T,H*T),Image.Resampling.LANCZOS);gid0=max(s['firstgid']+s['tilecount'] for s in m['tilesets']);data=[0]*(W*H);cells=[]
for y in range(H):
 for x in range(W):
  if CX<=x<CX+old['width'] and CY<=y<CY+old['height']:continue
  data[y*W+x]=gid0+len(cells);cells.append(border.crop((x*T,y*T,(x+1)*T,(y+1)*T)))
cols=24;atlas=Image.new('RGBA',(cols*T,math.ceil(len(cells)/cols)*T))
for i,im in enumerate(cells):atlas.paste(im,((i%cols)*T,(i//cols)*T))
atlas.save(O/'map32/outdoor-border.png')
m['tilesets'].append(dict(firstgid=gid0,name='outdoor-border',image='outdoor-border.png',imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(cells)))
m['layers'].insert(0,dict(name='outdoor-border',type='tilelayer',x=0,y=0,width=W,height=H,visible=True,opacity=1,id=7,data=data))
# New land is conservative stone-only; every old collision cell remains identical.
g=[[1]*W for _ in range(H)]
for y,row in enumerate(lold['collision']):g[y+CY][CX:CX+old['width']]=row[:]
landing=[(13,22,4),(12,23,6),(11,24,8),(12,25,6),(13,26,4)]
for x,y,n in landing:
 for xx in range(x,x+n):g[y][xx]=0
spawn=[15,25];collisionGid=next(s['firstgid']+t['id'] for s in m['tilesets'] for t in s.get('tiles',[]) if any(p['name']=='collides' and p['value'] for p in t.get('properties',[])))
next(l for l in m['layers'] if l['name']=='collision')['data']=[collisionGid if c else 0 for row in g for c in row]
quiet=next(l for l in m['layers'] if l['name']=='spawn-only-silence');quietGid=next(v for v in quiet['data'] if v);quiet['data']=[0]*(W*H);quiet['data'][spawn[1]*W+spawn[0]]=quietGid
starts=[a for l in m['layers'] for a in l.get('objects',[]) if a['name']=='start'];assert len(starts)==1;starts[0].update(x=spawn[0]*T,y=spawn[1]*T)
layout=copy.deepcopy(lold);layout.update(title='Timber Yoga Studio · woodland approach r4',dimensions=[W,H],spawn=spawn,collision=g)
for a in layout['anchors']+layout['seats']:
 for k,d in [('cell',(CX,CY)),('anchor',(DX,DY)),('floorClick',(DX,DY))]:
  if k in a:a[k]=[a[k][0]+d[0],a[k][1]+d[1]]
for z in layout['zones']:z['rect'][0]+=DX;z['rect'][1]+=DY
for name,cell in [('outdoor gathering west',[12,24]),('outdoor gathering east',[17,24]),('outdoor landing center',[15,23]),('outdoor arrival',[15,25])]:
 x,y=cell;layout['anchors'].append(dict(name=name,cell=cell,anchor=[x*T+16,y*T+15],floorClick=[x*T+16,y*T+31],kind='approach',direction='north'))
layout['notes']+=' r4 preserves all r3 scene pixels, mats, props, nook repairs, collision, anchors and role IDs; exact translation96,192. New outdoor stone landing and one quiet spawn cell. Old spawn is ordinary circulation. Native32 standing proof only.'
wam=read(B/'map32/map.wam')
for a in wam['areas']:a['x']+=DX;a['y']+=DY
write(O/'map32/map.tmj',m);write(O/'map32/map.wam',wam);write(O/'source/layout.json',layout)
# Render proof from the completed runtime TMJ, never from an unrelated painted preview.
base,above=decode(read(O/'map32/map.tmj'),O/'map32');oldbase,oldabove=decode(old,B/'map32');base.save(O/'assets/base.png');above.save(O/'assets/above.png');empty=Image.alpha_composite(base,above);empty.save(O/'review/empty-native.png');box=(DX,DY,DX+oldbase.width,DY+oldbase.height)
assert base.crop(box).tobytes()==oldbase.tobytes();assert above.crop(box).tobytes()==oldabove.tobytes()
oldproof=read(B/'source/WOKA-PROOF.json');oldoverlay=Image.open(R/'source-assets/r3-occupied-proof-overlay.png').convert('RGBA');overlay=Image.new('RGBA',base.size);overlay.paste(oldoverlay,(DX,DY));proof=copy.deepcopy(oldproof)
for a in proof['actors']:a['position'][0]+=DX;a['position'][1]+=DY
outdoor=[]
for k,pos in enumerate([(400,783),(560,783),(496,815)]):
 a=copy.deepcopy(oldproof['actors'][8+k]);x,y=a['position'];sprite=oldoverlay.crop((x-16,y-16,x+16,y+16));overlay.alpha_composite(sprite,(pos[0]-16,pos[1]-16));a.update(anchor='outdoor scale proof '+str(k+1),position=list(pos),sourceOverlaySha256=sha(R/'source-assets/r3-occupied-proof-overlay.png'),sourceCrop=[x-16,y-16,x+16,y+16],cropRgbaSha256=hashlib.sha256(sprite.tobytes()).hexdigest(),nativeFrameSize=[32,32],resampled=False);outdoor.append(a)
proof['actors']+=outdoor;proof['pose']='Original native32 unscaled idle frames. Static review facing only; no scripted animations.';write(O/'source/WOKA-PROOF.json',proof);write(O/'source/OUTDOOR-WOKA-PROOF.json',dict(actors=outdoor));shutil.copyfile(B/'source/native-head-union.json',O/'source/native-head-union.json');overlay.save(O/'review/actor-overlay-native.png');occupied=Image.alpha_composite(Image.alpha_composite(base,overlay),above);occupied.save(O/'review/occupied-native.png')
for name,box in [('classroom',(192,288,800,496)),('nooks',(192,496,800,624)),('entry',(352,608,640,864)),('outdoor',(288,688,704,864))]:occupied.crop(box).save(O/'review'/f'{name}-occupied-native.png')
write(O/'PRESERVATION.json',dict(originalWorld=[768,512],newWorld=[960,864],offset=[DX,DY],originalBasePixelExact=True,originalForegroundPixelExact=True,originalSceneRescaled=False,originalPackedAtlasesByteExact={n:sha(O/'map32'/n) for n in ['architecture-and-furniture.png','foreground.png','logic.png']},originalCollisionExact=True,originalAnchorsAndRolesTranslatedOnly=True,originalMatCount=6,newOutdoorCells=sum(n for x,y,n in landing),spawnMovedFrom=[lold['spawn'][0]*T+16,lold['spawn'][1]*T+16],spawnMovedTo=[spawn[0]*T+16,spawn[1]*T+16],quietCells=1,oldSpawnNowOrdinaryCirculation=True,borderSourceSha256=sha(R/'source-assets/generated-border-master.png'),oldMapSha256=sha(B/'map32/map.tmj')))
shutil.copyfile(R/'source-assets/native-spawn-outcomes.json',O/'source/native-spawn-outcomes.json')
print('Built',O)
