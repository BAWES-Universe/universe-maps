"""Deterministic native32 compiler. Rescales environment0.5; never scales Wokas."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy,hashlib,math,shutil
import numpy as np
R=Path(__file__).resolve().parents[1];B=R/'baseline';A=R/'source-assets';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=read(A/'spec.json');O=R/s['slug'];W,H=30,27;T=32
for d in ['map32','assets','review','source']:(O/d).mkdir(parents=True,exist_ok=True)
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
for f,h in read(A/'baseline-hashes.json').items():assert sha(B/f)==h,f
old=read(B/'map32/map.tmj');oldl=read(B/'source/layout.json')
# Preserve exact accepted empty appearance, including mat material and alignment.
def decode(m,folder):
 below=Image.new('RGBA',(m['width']*32,m['height']*32));above=Image.new('RGBA',below.size);dest=below;atlases={t['image']:Image.open(folder/t['image']).convert('RGBA') for t in m['tilesets']}
 for l in m['layers']:
  if l['name']=='floorLayer':dest=above
  if l['type']!='tilelayer' or not l.get('visible',True) or l.get('opacity',1)==0:continue
  for i,gid in enumerate(l['data']):
   if not gid:continue
   assert not gid&0xe0000000
   t=max((t for t in m['tilesets'] if t['firstgid']<=gid),key=lambda t:t['firstgid']);j=gid-t['firstgid'];assert j<t['tilecount'];x=j%t['columns']*32;y=j//t['columns']*32
   dest.alpha_composite(atlases[t['image']].crop((x,y,x+32,y+32)),((i%m['width'])*32,(i//m['width'])*32))
 return below,above
originalbase,originalabove=decode(old,B/'map32');original=Image.alpha_composite(originalbase,originalabove);assert original.size==(1536,1216)
core=original.resize((768,608),Image.Resampling.LANCZOS);base=Image.open(A/'generated-border-master.png').convert('RGBA').resize((960,864),Image.Resampling.LANCZOS);base.paste(core,(96,96));assert base.tobytes()==Image.open(A/'approved-empty.png').convert('RGBA').tobytes()
g=np.ones((H,W),dtype=int)
for x,y,w,h in s['openRects']+s['landingOpenRects']:g[y:y+h,x:x+w]=0
for x,y in s.get('blockedCells',[]):g[y,x]=1
# Layer allocation changes no empty-scene pixels. Original foreground regions stay foreground.
oldabove=originalabove.resize((768,608),Image.Resampling.LANCZOS);mask=Image.new('L',base.size);mask.paste(oldabove.getchannel('A').point(lambda v:255 if v>32 else 0),(96,96));inheritedMask=mask.copy();md=ImageDraw.Draw(mask)
for polygon in s['foregroundArchitecturePolygons']:md.polygon([tuple(p) for p in polygon],fill=255)
# Added elevated-cap depth masks are constrained by the full reachable native head envelope.
if s['foregroundArchitecturePolygons']:
 blocked=g.astype(bool).repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(blocked.shape);xa=np.maximum(0,X-8);xb=np.minimum(W*32,X+8);yb=np.minimum(H*32,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W*32)&(Y+16<=H*32)
 head=np.array(read(A/'native-head-union.json')['mask'],bool);envelope=np.zeros_like(clear)
 for yy,xx in np.argwhere(head):
  dx,dy=int(xx)-16,int(yy)-16;x0,x1=max(0,-dx),min(W*32,W*32-dx);y0,y1=max(0,-dy),min(H*32,H*32-dy);envelope[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
 mask=Image.fromarray(np.where(envelope,0,np.array(mask)).astype('uint8'))
above=Image.new('RGBA',base.size);above.paste(base,(0,0),mask);base.paste((0,0,0,0),(0,0,960,864),mask)
base.save(O/'assets/base.png');above.save(O/'assets/above.png')
write(O/'source/foreground-polygons.json',dict(polygons=s['foregroundArchitecturePolygons'],notes=s['foregroundMaskNotes'],inheritedMaskPreserved=True))
addedMask=np.array(mask)>0;addedMask[np.array(inheritedMask)>0]=False;added=above.copy();added.putalpha(Image.fromarray((addedMask*255).astype('uint8')));added.save(O/'review/added-foreground-alpha.png')
cb=np.indices((864,960)).sum(0);yy,xx=np.indices((864,960));shade=np.where((xx//8+yy//8)%2,190,235).astype('uint8');bg=Image.fromarray(np.dstack([shade,shade,shade,np.full_like(shade,255)]),'RGBA');Image.alpha_composite(bg,added).crop((352,384,608,640)).resize((768,768),Image.Resampling.NEAREST).save(O/'review/added-foreground-checkerboard.png')
# Pack complete native32 tiles deterministically; transparent areas use gid0.
sets=[];gid=1
def pack(im,name):
 global gid
 tiles=[];data=[]
 for y in range(H):
  for x in range(W):
   tile=im.crop((x*32,y*32,x*32+32,y*32+32))
   if not tile.getbbox():data.append(0)
   else:data.append(gid+len(tiles));tiles.append(tile)
 if tiles:
  columns=24;atlas=Image.new('RGBA',(columns*32,math.ceil(len(tiles)/columns)*32))
  for i,tile in enumerate(tiles):atlas.paste(tile,((i%columns)*32,(i//columns)*32))
  atlas.save(O/'map32'/f'{name}.png');sets.append(dict(firstgid=gid,name=name,image=name+'.png',imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,columns=columns,tilecount=len(tiles),margin=0,spacing=0));gid+=len(tiles)
 return data
basedata=pack(base,'environment');abovedata=pack(above,'foreground');logic=Image.new('RGBA',(64,32));logic.save(O/'map32/logic.png');logicid=gid;sets.append(dict(firstgid=gid,name='logic',image='logic.png',imagewidth=64,imageheight=32,tilewidth=32,tileheight=32,columns=2,tilecount=2,margin=0,spacing=0,tiles=[dict(id=0,properties=[dict(name='collides',type='bool',value=True)])]))
def layer(name,data,id,**extra):return dict(name=name,type='tilelayer',x=0,y=0,width=W,height=H,visible=True,opacity=1,id=id,data=data,**extra)
spawn=s['spawnCell'];quiet=[0]*(W*H);quiet[spawn[1]*W+spawn[0]]=logicid+1
start=copy.deepcopy(next(a for l in old['layers'] for a in l.get('objects',[]) if a['name']=='start'));start.update(x=spawn[0]*32,y=spawn[1]*32,width=32,height=32)
m=copy.deepcopy(old);m.update(width=W,height=H,nextlayerid=7,tilesets=sets,layers=[layer('architecture-and-furniture',basedata,1),layer('collision',[logicid if c else 0 for c in g.flat],2),layer('spawn-only-silence',quiet,3,properties=[dict(name='silent',type='bool',value=True)]),dict(name='floorLayer',type='objectgroup',id=4,objects=[],visible=True,opacity=1),layer('foreground',abovedata,5),dict(name='map-areas',type='objectgroup',id=6,objects=[start],visible=True,opacity=1)])
for p in m['properties']:
 if p['name']=='name':p['value']=s['title']
 if p['name']=='status':p['value']='Unpublished native32 candidate; live media, keyboard physics and multi-user checks remain separate'
write(O/'map32/map.tmj',m)
wam=read(B/'map32/map.wam')
for a in wam['areas']:
 a['x']=a['x']*.5+96;a['y']=a['y']*.5+96;a['width']*=.5;a['height']*=.5
write(O/'map32/map.wam',wam)
anchors=[]
for a in s.get('matAnchors',[])+s['anchors']:
 name,x,y,*kind=a;k=kind[0] if kind else 'mat';anchors.append(dict(name=name,cell=[x//32,y//32],anchor=[x,y],floorClick=[x,y+16],kind=k,direction='south' if k=='instructor' else 'north'))
for name,x,y in [('outdoor gathering west',400,783),('outdoor gathering east',560,783),('outdoor landing center',496,751),('outdoor arrival',496,815)]:anchors.append(dict(name=name,cell=[x//32,y//32],anchor=[x,y],floorClick=[x,y+16],kind='approach',direction='north'))
zones=copy.deepcopy(oldl['zones'])
for z in zones:z['rect']=[z['rect'][0]*.5+96,z['rect'][1]*.5+96,z['rect'][2]*.5,z['rect'][3]*.5]
layout=dict(title=s['title'],category=oldl['category'],dimensions=[W,H],tileSize=32,spawn=spawn,seats=[],anchors=anchors,zones=zones,collision=g.tolist(),notes='Original1536x1216 artwork retained; complete artwork uniformly scaled0.5 at96,96 within960x864. Native Wokas32; reauthored native32 collision and floor-click anchors. Standing static proof only. Original role IDs and permissions retained; scaled role bounds are configuration, not fresh media validation.')
write(O/'source/layout.json',layout)
# Authentic earlier startup source capture, translated with same32x32 semantics.
cap=read(A/'native-spawn-outcomes.json');dx=start['x']-cap['start']['x'];dy=start['y']-cap['start']['y'];cap['originalCaptureSha256']=sha(A/'native-spawn-outcomes.json');cap['scope']='Earlier authentic JavaScript startup outcome capture translated to identical32x32 start-area semantics; no fresh StartPositionCalculator execution.';cap['translation']=[dx,dy];cap['start']=start
for r in cap['rows']:r['x']+=dx;r['y']+=dy
cap['distinct']=[[x+dx,y+dy] for x,y in cap['distinct']];write(O/'source/native-spawn-outcomes.json',cap);shutil.copyfile(A/'native-head-union.json',O/'source/native-head-union.json')
# Exact unscaled32px compiled native frame crops from previously pinned proof.
sourceproof=read(A/'WOKA-PROOF.json');sourceoverlay=Image.open(A/'occupied-proof-overlay.png').convert('RGBA');overlay=Image.new('RGBA',base.size);records=[]
if s['key']=='retreat':selected=[a for a in anchors if a['kind'] in ['mat','instructor'] or a['name'] in ['tea cushion 3 approach','rest cushion 3 approach','central social hall','outdoor gathering west','outdoor gathering east','outdoor arrival']]
else:selected=[a for a in anchors if a['name'] in ['instructor position','demo audience','strength bench north approach','strength bench south approach','cardio bike north approach','cardio bike south approach','cardio rower approach','arrival bench approach','water station approach','outdoor gathering west','outdoor gathering east','outdoor arrival']]
for i,a in enumerate(selected):
 idx=0 if a['kind']=='instructor' else 1+(i%6) if a['kind']=='mat' else 7+(i%4);oldactor=sourceproof['actors'][idx];sx,sy=oldactor['position'];box=[sx-16,sy-16,sx+16,sy+16];sprite=sourceoverlay.crop(box);x,y=a['anchor'];overlay.alpha_composite(sprite,(x-16,y-16));records.append(dict(oldactor,anchor=a['name'],position=[x,y],sourceOverlaySha256=sha(A/'occupied-proof-overlay.png'),sourceCrop=box,cropRgbaSha256=hashlib.sha256(sprite.tobytes()).hexdigest(),nativeFrameSize=[32,32],resampled=False,kind=a['kind']))
proof=dict(repoCommit=sourceproof['repoCommit'],pose='Unmodified native32 idle frames, static facing only; no sitting, yoga or equipment animation.',runtimeContainsAvatars=False,actors=records);write(O/'source/WOKA-PROOF.json',proof);overlay.save(O/'review/actor-overlay-native.png');empty=Image.alpha_composite(base,above);occupied=Image.alpha_composite(Image.alpha_composite(base,overlay),above);empty.save(O/'review/empty-native.png');occupied.save(O/'review/occupied-native.png')
for name,box in [('classroom',(176,264,800,464)),('nooks',(176,480,800,600)),('entry',(336,544,624,728)),('outdoor',(304,672,656,864))]:occupied.crop(box).save(O/'review'/f'{name}-occupied-native.png')
write(O/'SOURCE-PRESERVATION.json',dict(originalWorld=[1536,1216],newWorld=[960,864],uniformEnvironmentScale=.5,sourceOffset=[96,96],actorScale=1,approvedEmptySha256=sha(A/'approved-empty.png'),originalCoreUniformResamplePixelExact=True,originalHighResolutionSourcesRetained=True,baselineFiles=read(A/'baseline-hashes.json'),originalMatMaterialAndAlignmentPreserved=True,newGenerationCalls=0,geometryReauthored=True,oldGymStairBoundaryOpened=s['key']=='gym',roleIdsAndPermissionsExact=True,roleCoordinatesTransformedOnly=True,foregroundAllocation='Decoded original foreground alpha>32 scaled0.5; exact accepted-scene opaque pixels split out of base into foreground. Gym baseline has zero foreground; added entry posts and Retreat elevated caps use conservative traced architecture-only polygons from approved artwork with exhaustive head clearance. No empty-scene pixels changed.',newQuietSpawnCell=spawn,oldSpawnIsOrdinaryCirculation=True))
print('Built',s['slug'],len(anchors),'anchors;',int((g==0).sum()),'walkable cells')
