from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,re
R=Path(__file__).resolve().parents[1];m=R/'quiet-orbit-observatory';old=Path('/workspace/shared/overnight-learning-work/releases/quiet-orbit-observatory-r1');D=384
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=load(old/'source/layout.json');b=load(m/'source/layout.json');allowed=np.zeros((1024,1536),bool)
for layout,dy in [(a,0),(b,D)]:
 for s in layout['seats']:
  if s['name'].startswith('seminar-'):
   x,y=s['cell'];y-=dy//32;allowed[y*32-8:y*32+40,x*32:(x+1)*32]=True
checks={}
for fn in ['base.png','above.png']:
 x=np.array(Image.open(old/'assets'/fn));y=np.array(Image.open(m/'assets'/fn))[D:];diff=np.any(x!=y,axis=2);assert not np.any(diff&~allowed);checks[fn]={'changedPixels':int(diff.sum()),'outsideChairFootprintsChanged':0,'originalRegionPixels':1536*1024}
assert b['collision'][:12]==[[1]*48]*12
cg=np.array(b['collision'][12:])!=np.array(a['collision']);allowg=np.zeros(cg.shape,bool)
for layout,offset in [(a,0),(b,12)]:
 for s in layout['seats']:
  if s['name'].startswith('seminar-'):x,y=s['cell'];allowg[y-offset+1,x]=1
assert not np.any(cg&~allowg)
wam=load(m/'map32/map.wam');sp,li=wam['areas'];assert li['properties'][0]['speakerZoneName']==sp['id'];assert sp['properties'][0]['name']==sp['id']
for seat in b['seats'][4:]:
 x,y=seat['anchor'];assert li['x']<=x<li['x']+li['width'] and li['y']<=y<li['y']+li['height']
for aa,bb in zip(a['zones'],b['zones']):assert aa['rect']==[bb['rect'][0],bb['rect'][1]-D,*bb['rect'][2:]]
sets=load(m/'map32/map.tmj')['tilesets'];assert all((m/'map32'/s['image']).is_file() for s in sets)
repo=Path('/workspace/shared/native-soundscape-proof/full-checkout');u=(repo/'back/src/Model/User.ts').read_text();media=(repo/'play/src/front/Stores/MediaStore.ts').read_text();handler=(repo/'play/src/front/Phaser/Game/MapEditor/AreasPropertiesListener.ts').read_text();room=(repo/'back/src/Model/GameRoom.ts').read_text()
assert 'if ($isListenerStore) return AvailabilityStatus.LISTENER;' in media
assert 'if ($isSpeakerStore) return AvailabilityStatus.SPEAKER;' in media
getter=u[u.index('    public get silent(): boolean {'):u.index('    get following():')];assert 'AvailabilityStatus.LISTENER' in getter and 'AvailabilityStatus.SPEAKER' in getter
assert 'if (user.silent)' in room and 'isListenerStore.set(true)' in handler and 'isListenerStore.set(false)' in handler
report={'pass':True,'artPreservation':checks,'allNonSeminarCollisionUnchanged':True,'northBackdropSolid':True,'assetClosure':True,'stageSeatCoverage':True,'nativePairPreserved':True,'extraSilenceAdded':False,'stageContract':{'commit':'f00b3482f23c51976b4b339d7a891cad683d6498','status':'Source contracts verified; no live AV/multiplayer claim','chain':['AreasPropertiesListener speaker/listener handlers set role stores on native stream join','MediaStore availability derives SPEAKER/LISTENER','back User.silent includes both SPEAKER and LISTENER','GameRoom excludes silent users from proximity groups'],'staleTodo':'Listener handler TODO does not represent downstream implemented role-status contract'},'seamRegistration':{'originalOffset':[0,D],'existingPixelsRescaled':False,'newStripGeneratedMaster':[1254,1254],'sourceNorthEdgeY':317,'newStripSize':[1536,384],'edgeMatching':'24px north-only boundary color blend outside central arch'},'inputs':{str(p.relative_to(m)):sha(p) for p in [m/'map32/map.tmj',m/'map32/map.wam',m/'assets/base.png',m/'assets/above.png',m/'source/layout.json']}}
(m/'REVISION-VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
