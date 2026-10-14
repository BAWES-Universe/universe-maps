from pathlib import Path
from PIL import Image,ImageDraw
import compiler as b
import json,hashlib,copy,numpy as np
R=Path(__file__).resolve().parents[1];B=R/'baseline';slug='timber-movement-studio-r2';dx=dy=96
b.C,b.N,b.W,b.H=30,27,960,864
read=lambda p:json.loads(p.read_text())
old=read(B/'r1-layout.json');oldbase=Image.open(B/'r1-base.png').convert('RGBA');oldabove=Image.open(B/'r1-above.png').convert('RGBA')
m=b.Map(slug,'Timber Movement Studio - Woodland Landing','Activity / open class',b.P)
# Only the generated border is resampled. The full approved r1 scene remains pixel-exact.
master=Image.open(R/'source-assets/generated-border-master.png').convert('RGBA');m.base=master.resize((960,864),Image.Resampling.LANCZOS);m.base.paste(oldbase,(dx,dy));m.above=Image.new('RGBA',(960,864));m.above.paste(oldabove,(dx,dy));m.d=ImageDraw.Draw(m.base);m.a=ImageDraw.Draw(m.above)
m.g=np.ones((27,30),dtype=int);m.g[3:22,3:27]=np.array(old['collision']);m.g=m.g.tolist()
# Inscribed native32 cells on actual stone/gravel, preserving the complete rocky/planted edge.
for r in [(13,22,4,1),(12,23,6,1),(11,24,8,1),(12,25,6,1),(13,26,4,1)]:m.block(*r,0)
m.spawn=(15,25)
m.anchors=copy.deepcopy(old['anchors']);m.seats=[];m.zones=copy.deepcopy(old['zones'])
for a in m.anchors:
 a['cell'][0]+=3;a['cell'][1]+=3
 for key in ['anchor','floorClick']:
  if key in a:a[key][0]+=dx;a[key][1]+=dy
for a in m.zones:a['rect'][0]+=dx;a['rect'][1]+=dy
for name,x,y in [('outdoor gathering west',12,24),('outdoor gathering east',17,24),('outdoor landing center',15,23),('outdoor arrival',15,25)]:m.anchor(name,x,y)
m.cropboxes=[('class-floor',(192,272,768,544)),('entry-and-landing',(320,576,704,864)),('outdoor-gathering',(288,688,704,864)),('north-scenery',(0,0,960,272))]
m.finish();out=R/slug
# Preserve exact optional role IDs/configuration while translating into the wider canvas.
wam=read(B/'r1-map.wam')
for a in wam['areas']:a['x']+=dx;a['y']+=dy
b.js(out/'map32/map.wam',wam)
# Restore original authored sub-cell instructor endpoint after compiler serialization.
layout=read(out/'source/layout.json');layout['anchors']=m.anchors;b.js(out/'source/layout.json',layout)
# Authoritative proof positions are translated exact; three genuine idle actors occupy the new landing.
actors=Image.new('RGBA',(960,864));actors.paste(Image.open(R/'source-assets/occupied-proof-overlay.png').convert('RGBA'),(96,96));actors.alpha_composite(Image.open(R/'source-assets/outdoor-proof-overlay.png').convert('RGBA'))
occupied=m.base.copy();occupied.alpha_composite(actors);occupied.alpha_composite(m.above);occupied.save(out/'review/occupied-native.png');occupied.save(out/'review/overview.png')
for name,box in m.cropboxes:occupied.crop(box).save(out/'review'/f'{name}-occupied-native.png')
base_restore=m.base.crop((96,96,864,704));above_restore=m.above.crop((96,96,864,704));assert base_restore.tobytes()==oldbase.tobytes();assert above_restore.tobytes()==oldabove.tobytes();assert np.array_equal(np.array(m.g)[3:22,3:27],np.array(old['collision']))
proof={'originalBasePixelExact':True,'originalForegroundPixelExact':True,'originalCollisionExact':True,'originalSeatAndRoleCoordinatesTranslatedOnly':True,'offset':[96,96],'oldWorld':[768,608],'newWorld':[960,864],'newLandingCells':sum(sum(1 for v in row if not v) for row in m.g)-sum(sum(1 for v in row if not v) for row in old['collision']),'spawnMovedFrom':[400,560],'spawnMovedTo':[496,816],'spawnQuietCells':1,'oldSpawnNowOrdinaryCirculation':True,'originalTmjSha256':hashlib.sha256((B/'r1-map.tmj').read_bytes()).hexdigest(),'sourceMasterSize':list(master.size),'originalSceneRescaled':False}
b.js(out/'PRESERVATION.json',proof)
p=read(R/'source-assets/WOKA-PROOF.json')
for a in p['actors']:a['position'][0]+=96;a['position'][1]+=96
p['actors']+=read(R/'source-assets/OUTDOOR-WOKA-PROOF.json')['actors'];p['pose']='Unchanged genuine native32 idle frames, manually faced for static proof only; no sitting/dance/auto-facing';b.js(out/'source/WOKA-PROOF.json',p)
(out/'GUIDE.md').write_bytes((R/'GUIDE.md').read_bytes())
files=[]
for folder in ['assets','map32','source','review']:
 for p in sorted((out/folder).rglob('*')):
  if p.is_file():files.append({'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for name in ['GUIDE.md','PRESERVATION.json','VALIDATION.json']:
 p=out/name;files.append({'path':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
b.js(out/'MANIFEST.json',{'slug':slug,'title':m.title,'nativeTileSize':32,'world':[960,864],'status':'Unpublished r2 candidate; source QA, user design approval and live tests separate','files':files})
(R/'preview').mkdir(exist_ok=True);occupied.save(R/'preview/compiled-occupied.png')
print(json.dumps(proof,indent=2))
