"""Bounded native-pixel relocation; no synthesis, scale, engine, or source edits."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,copy,hashlib,shutil
R=Path(__file__).resolve().parent;S=R.parent/'sources/civic';P=R.parent/'module-phase-study';O=R/'importable-civic';O.mkdir(exist_ok=True)
read=lambda p:json.loads(Path(p).read_text())
write=lambda p,v:Path(p).write_text(json.dumps(v,indent=2)+'\n')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=read(S/'module.json');original=copy.deepcopy(m);m['worldOrigin']=[0,1136];m['tileSize']=32
images={n:Image.open(S/(n+'-native.png')).convert('RGBA')for n in ['architecture','furniture','foreground','glass','shadow']}
base=np.array(images['furniture']);fg=np.array(images['foreground']);source_base=base.copy();source_fg=fg.copy();moves=[]
# Explicit semantic native chair silhouette. At rows249..252, the source chair
# is already composited in front of the desk's bottom4 rows. Move its visible
# pixels only; retain every surviving table pixel and expose original floor.
# This does not invent the table surface that the flattened source never saved.
row_bounds={249:(147,173),250:(145,175),251:(145,175),252:(144,176)}
for x in [160,320,480]:
 mask=np.zeros((1152,640),bool)
 for y,(a,b)in row_bounds.items():mask[y,a+x-160:b+x-160]=True
 mask[253:304,x-24:x+24]=True
 mask&=source_base[:,:,3]>0
 ys,xs=np.where(mask);patch=source_base[ys,xs].copy();base[ys,xs]=0
 # Destination contains only the same chair's previous tail, cleared above.
 assert not np.any(base[ys+16,xs,3]),'chair destination contains other art'
 base[ys+16,xs]=patch
 fm=np.zeros(mask.shape,bool);fm[232:304,x-24:x+24]=source_fg[232:304,x-24:x+24,3]>0
 yy,xx=np.where(fm);fp=source_fg[yy,xx].copy();fg[yy,xx]=0;fg[yy+16,xx]=fp
 q=m['students'][[160,320,480].index(x)];q['center'][1]+=16;q['approach'][1]+=16
 q['chairRegistration']={'sourceVisibleBounds':[x-18,249,36,36],'translation':[0,16],'visualFloorFootprint':[x-16,272+16,32,16],'footprintPurpose':'Visible chair contact reference only. Source seats have no independent solid collider. Desk blocker retained unchanged.'}
 moves.append({'id':q['id'],'translation':[0,16],'sourceSelectedPixels':int(mask.sum()),'foregroundPixels':int(fm.sum()),'sourceUpperContour':{str(y):[a+x-160,b+x-160]for y,(a,b)in row_bounds.items()},'remainingContour':[x-24,253,48,51],'allSelectedRgbaPixelsPreserved':bool(np.array_equal(base[ys+16,xs],patch))})
# Move complete lectern, its rim, and existing64x32 solid; speaker stays fixed.
box=(280,640,360,752)
for name,arr,src in [('furniture',base,source_base),('foreground',fg,source_fg)]:
 x0,y0,x1,y1=box;mask=np.zeros(src.shape[:2],bool);mask[y0:y1,x0:x1]=src[y0:y1,x0:x1,3]>0;yy,xx=np.where(mask);p=src[yy,xx].copy();arr[yy,xx]=0;assert not np.any(arr[yy+16,xx,3]);arr[yy+16,xx]=p
 moves.append({'id':'lectern-'+name,'translation':[0,16],'sourceBounds':list(box),'sourceSelectedPixels':int(mask.sum()),'allSelectedRgbaPixelsPreserved':bool(np.array_equal(arr[yy+16,xx],p))})
m['speaker']['podiumOrigin'][1]+=16;m['speaker']['collision']['y']+=16
for o in m['blockers']:
 if o['id']=='podium-footprint':o['y']+=16
for route in m['routes']:
 route['role']='Legacy authored illustration only; not used to prove or force native click routing.'
 if route['target'] in ['student-1','student-2','student-3']:
  for p in route['points'][-2:]:p[1]+=16
m['registrationRepair']={'sourcePin':'d2bc57b63b4abab9303fb3cbcecf1a0450fd15cc','sourceModuleSha256':sha(S/'module.json'),'originRetainedFromCurrentCampus':[0,1136],'sourceModuleStaleOrigin':[0,1792],'moves':moves,'foregroundPolicy':'Original fixed chair-back foreground retained intact under translation; no actor-following mask and no full-back demotion. Native full-route chair-head overlap remains documented.','deskOcclusionCaveat':'The upper4 native rows of each visible chair overlap its table in the already flattened furniture source. The selected visible chair contour moves; all other furniture pixels remain untouched. Newly revealed pixels use untouched architecture; no hidden desk face is synthesized.','collisionPolicy':'Conservative whole32px cells from unchanged original floor and blockers except translated complete64x32 lectern. Seats retain their original non-solid interaction geometry.'}
for n in ['architecture','glass','shadow']:shutil.copyfile(S/(n+'-native.png'),O/(n+'-native.png'))
Image.fromarray(base).save(O/'furniture-native.png');Image.fromarray(fg).save(O/'foreground-native.png');write(O/'module.json',m)
# Reconstruct source8 world with only civic replacement, restoring fixed receivers.
C=Path('/workspace/shared/magical-campus-return-08/office-divider-study/campus-visible-divider-candidate')
wg=read(C/'map/collision-grid.json');g8=np.zeros((wg['height'],wg['width']),np.uint8);g8.flat[wg['blockedIndices']]=1
floor=Image.new('1',(640,1152));d=ImageDraw.Draw(floor)
for poly in [[[64,144],[576,144],[576,1088],[64,1088]],[[576,344],[640,344],[640,424],[576,424]],[[576,952],[640,952],[640,1032],[576,1032]]]:d.polygon([tuple(v)for v in poly],fill=1)
for o in m['blockers']:d.rectangle((o['x'],o['y'],o['x']+o['width']-1,o['y']+o['height']-1),fill=0)
local8=1-np.array(floor,np.uint8).reshape(144,8,80,8).min((1,3));g8[142:286,:80]=local8
for j in read(C/'map/compile-manifest.json')['connectors']:
 for x,y,w,h in j['openRects']:g8[y//8:(y+h)//8,x//8:(x+w)//8]=0
g8[0,:]=g8[-1,:]=g8[:,0]=g8[:,-1]=1;grid=g8.reshape(82,4,92,4).max((1,3));hyp=read(P/'civic-registration-hypothesis.json');assert np.array_equal(grid,np.array(hyp['grid']))
write(R/'collision-world32.json',{'cellSize':32,'width':92,'height':82,'outsideBlocked':True,'blockedIndices':np.flatnonzero(grid).tolist(),'grid':grid.tolist(),'scope':'Source08 world diagnostic with only bounded civic repair. Other modules are baseline, not final integrated09 geometry.'})
# A phase16 module cannot be snapped independently; retain its precise origin.
write(O/'collision-registration.json',{'tileSize':32,'worldOrigin':[0,1136],'worldPhase':[0,16],'walkablePolygons':[[[64,144],[576,144],[576,1088],[64,1088]],[[576,344],[640,344],[640,424],[576,424]],[[576,952],[640,952],[640,1032],[576,1032]]],'blockers':m['blockers'],'registration':'Apply local geometry at exact origin before conservativeOR32. Do not round this module origin to a32px boundary. Fixed receivers unchanged.'})
anchors=[]
for kind,arr in [('student',m['students']),('attendee',m['audience']),('teacher',[m['teacher']]),('speaker',[m['speaker']])]:
 for q in arr:anchors.append({'id':q['id'],'kind':kind,'position':[q['center'][0],q['center'][1]+1136]})
write(R/'before-test-input.json',{'anchors':read(P/'civic-dx0-dy0-fixed-receivers.json')['anchors'],'grid':read(P/'civic-dx0-dy0-fixed-receivers.json')['grid']})
write(R/'after-test-input.json',{'anchors':anchors,'grid':grid.tolist()})
# Native before/after artwork and seated review with authentic Greg32.
sheet=Image.open('/workspace/shared/recovered-pre-island-package/runtime/assets/greg.png').convert('RGBA');sp=np.array(sheet);head_union=np.zeros((14,32),bool)
for rr in range(4):
 for cc in range(3):head_union|=sp[rr*32:rr*32+14,cc*32:cc*32+32,3]>32
for tag,root,mod in [('before',S,original),('after',O,m)]:
 layer={n:Image.open(root/(n+'-native.png')).convert('RGBA')for n in images};empty=layer['architecture'].copy();empty.alpha_composite(layer['furniture']);occupied=empty.copy()
 occ=[]
 for q in mod['students']+mod['audience']+[mod['teacher'],mod['speaker']]:
  x,y=q['center'];fr=q['frame'];sprite=sheet.crop(((fr%3)*32,(fr//3)*32,(fr%3+1)*32,(fr//3+1)*32));occupied.alpha_composite(sprite,(x-16,y-16));sa=np.array(sprite)[:,:,3]>32;fa=np.array(layer['foreground'])[y-16:y+16,x-16:x+16,3]>32
  torso=sa.copy();torso[:14]=False;overlap=torso&fa;heads=sa[:14]&fa[:14]
  occ.append({'id':q['id'],'localAnchor':[x,y],'frame':fr,'torsoAndLegOpaquePixels':int(torso.sum()),'fixedForegroundOccludedTorsoAndLegPixels':int(overlap.sum()),'visibleTorsoAndLegPixels':int((torso&~fa).sum()),'headPixelsOccluded':int(heads.sum())})
 for n in ['foreground','glass','shadow']:empty.alpha_composite(layer[n]);occupied.alpha_composite(layer[n])
 empty.save(R/(tag+'-native.png'));occupied.save(R/(tag+'-greg32-native.png'));write(R/(tag+'-occupied-pixels.json'),occ)
 # Fullworld danger bitmap from all12 head masks, then queried by native model.
 fa=np.array(layer['foreground'])[:,:,3]>32;full=np.zeros((2624,2944),np.uint8);full[1136:2288,:640]=fa;danger=np.zeros_like(full)
 for yy,xx in np.argwhere(head_union):
  dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(2944,2944-dx);y0=max(0,-dy);y1=min(2624,2624-dy);danger[y0:y1,x0:x1]|=full[y0+dy:y1+dy,x0+dx:x1+dx]
 (R/(tag+'-greg12-head-danger.bin')).write_bytes(danger.tobytes())
# Review crops stay native on2-column layout. No image scaling.
for label,box in [('classroom',(112,176,528,448)),('lectern',(256,640,384,784)),('audience',(112,784,528,1056))]:
 before=Image.open(R/'before-greg32-native.png').crop(box);after=Image.open(R/'after-greg32-native.png').crop(box);board=Image.new('RGBA',(before.width*2+16,before.height),(22,27,37,255));board.paste(before,(0,0));board.paste(after,(before.width+16,0));board.save(R/(label+'-before-after-greg32-native.png'))
checks={'sourceFiles':{p.name:sha(p)for p in S.iterdir()if p.is_file()},'outputFiles':{p.name:sha(p)for p in O.iterdir()if p.is_file()},'architectureGlassShadowByteIdentical':all(sha(S/(n+'-native.png'))==sha(O/(n+'-native.png'))for n in ['architecture','glass','shadow']),'gridMatchesRegistrationHypothesis':True,'studentsFirstThreeAnchorShift':[0,16],'speakerAnchorUnchanged':m['speaker']['center']==original['speaker']['center'],'deskBlockersUnchanged':all(o==next(p for p in original['blockers']if p['id']==o['id'])for o in m['blockers']if o['id'].endswith('-desk')),'unchangedOtherFurniturePixels':bool(np.array_equal(base[320:640],source_base[320:640]) and np.array_equal(base[784:],source_base[784:])),'sourcePin':'d2bc57b63b4abab9303fb3cbcecf1a0450fd15cc','nativeModelSha256':sha('/workspace/shared/magical-campus-return-08/validation-work/native-path-model-speed9.mjs'),'easyStarSha256':sha('/workspace/shared/magical-campus-return-08/validation-work/easystar-0.4.4.js')}
write(R/'asset-verification.json',checks);print(json.dumps(checks,indent=2))
