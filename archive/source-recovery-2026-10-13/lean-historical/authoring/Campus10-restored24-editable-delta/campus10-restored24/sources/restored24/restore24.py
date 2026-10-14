from pathlib import Path
from PIL import Image
import json,copy,shutil,hashlib,numpy as np
O=Path(__file__).resolve().parent; D=O/'importable-civic10-24seats'; C=Path('/workspace/shared/magical-campus-current32-10'); S=Path('/workspace/shared/campus10-functional-audit/lower-back-study/importable-civic10'); P=Path('/workspace/shared/campus10-functional-audit/lower-back-study/paired16/importable-civic10-16seats')
J=lambda p:json.loads(Path(p).read_text()); W=lambda p,v:Path(p).write_text(json.dumps(v,indent=2)+'\n');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
current=J(C/'sources/civic/module.json'); orig24=J(S/'module.json');m=copy.deepcopy(current); restored=[q for q in orig24['audience'] if q['id'] not in {a['id'] for a in m['audience']}]; ids={q['id'] for q in restored};layer_proof=[]
for name in ['architecture','glass','shadow']:shutil.copyfile(C/f'sources/civic/{name}-native.png',D/f'{name}-native.png')
for name in ['furniture','foreground']:
 a=np.array(Image.open(C/f'sources/civic/{name}-native.png'));p=np.array(Image.open(P/f'{name}-native.png'));s=np.array(Image.open(S/f'{name}-native.png'));assert np.array_equal(a,p),name
 delta=np.any(s!=p,axis=2);bounds=np.zeros(delta.shape,bool)
 for q in restored:
  x,y=q['center'];bounds[y-8:y+32,x-24:x+24]=True
 assert not np.any(delta&~bounds)
 b=a.copy();b[delta]=s[delta];Image.fromarray(b).save(D/f'{name}-native.png');layer_proof.append({'name':name,'changedPixels':int(delta.sum()),'changesOnlyWithinRestoredEightChairs':True,'classroomAndPodiumPixelsUnchanged':bool(np.array_equal(a[:800],b[:800])),'original24PixelExact':bool(np.array_equal(s,b))})
m['audience']=copy.deepcopy(orig24['audience']);m['blockers'] += [copy.deepcopy(b) for b in orig24['blockers'] if any(b['id'].startswith(i+'-visible-rear-foot-') for i in ids)]
for q in restored:m['nativePracticalFloorClickRectangles'][q['id']]=copy.deepcopy(orig24['nativePracticalFloorClickRectangles'][q['id']])
m['registrationRepair']['chairs']='Restore all24 audience seats: two adjacent three-chair banks in each of four rows. Columns152,200,256 and384,440,488; local rows824,888,952,1016 (64px). All30 original chairs are8px south of09; first/last audience columns are+8/-8px to preserve collision/head clearance.'
m['registrationRepair']['peerLimitation']='Communal24-seat layout. Seat endpoints and empty-room routes are map-clear. Native global pathfinding does not avoid occupied players; row-entry routes may cross seated peer bodies. See current24-seat route/body report; no crowd-avoidance or live proximity claim.'
m['validationSummary']={'status':'Pending candidate checks in sibling verification reports; previous16-seat claims removed','audienceSeats':24,'classroomSeats':6}
m['scope']='Local restoration of24-seat auditorium into current10 source module. Current10 classroom furniture, podium, door art, walkable openings and non-auditorium blockers preserved. No engine, avatar, grid or runtime interaction changes.'
W(D/'module.json',m);reg=J(C/'sources/civic/collision-registration.json');reg['blockers']=m['blockers'];W(D/'collision-registration.json',reg)
# Reuse current10 world geometry, adding only restored visible rear-leg cells; independent source compilation is performed later by integrator.
gridMeta=J(C/'map32/collision-grid.json');g=np.zeros((gridMeta['height'],gridMeta['width']),np.uint8);g.flat[gridMeta['blockedIndices']]=1;before=g.copy()
for b in m['blockers']:
 if not any(b['id'].startswith(i+'-visible-rear-foot-') for i in ids):continue
 x,y,w,h=b['x'],b['y']+1136,b['width'],b['height'];g[y//32:(y+h-1)//32+1,x//32:(x+w-1)//32+1]=1
anchors=[[q['id'],q['center'][0],q['center'][1]+1136] for q in m['students']+m['audience']];W(O/'candidate-grid.json',{'grid':g.tolist(),'anchors':anchors,'scope':'Current10 compiled world grid plus conservative32 cells of16 restored visible rear-foot rectangles.'})
W(O/'restoration-proof.json',{'restoredIDs':sorted(ids,key=lambda s:int(s.split('-')[1])),'source24':str(S),'current10':str(C),'layerProof':layer_proof,'unchangedMetadata':{k:current[k]==m[k] for k in ['students','teacher','speaker','doorRegistration10','publicDoorAnchors','zones']},'unchangedImageHashes':{name:sha(D/f'{name}-native.png')==sha(C/f'sources/civic/{name}-native.png') for name in ['architecture','glass','shadow']},'addedBlockedCells':[[int(x),int(y)] for y,x in np.argwhere(g!=before)],'sourceHashes':{str(p):sha(p) for p in [S/'furniture-native.png',S/'foreground-native.png',C/'sources/civic/module.json',C/'map32/collision-grid.json']}})
print('Restored',len(restored),'chairs;',int((g!=before).sum()),'added native32 cells; other geometry and source art preserved.')
