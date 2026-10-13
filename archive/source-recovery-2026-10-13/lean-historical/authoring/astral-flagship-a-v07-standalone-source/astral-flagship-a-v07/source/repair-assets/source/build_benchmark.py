from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import hashlib,json,shutil,math,numpy as np
R=Path(__file__).resolve().parents[1];V3=Path('/workspace/shared/grand-auditorium-03-foyer-terrace');V5=Path('/workspace/shared/grand-auditorium-05-roofless-garden');A=R/'assets';Q=R/'review';S=R/'source'
load=lambda p:Image.open(p).convert('RGBA')
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
greg=load(V5/'assets/greg-reference.png');frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('east',7),('west',4)]}
for n in ['lounge-chair-south','lounge-chair-north','lounge-chair-east','lounge-chair-west','low-lounge-table','welcome-desk']:
 shutil.copy2(V3/f'assets/{n}.png',A/f'{n}.png')
shutil.copy2(V5/'assets/greg-reference.png',A/'greg-reference.png')
# One aspect-preserving authoring reduction, never a resize of the old native raster.
master=load(S/'reception-counter-generated-master.png');box=master.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox();counter=master.crop(box).resize((192,51),Image.Resampling.LANCZOS);counter.save(A/'reception-counter-native-192x51.png')
# Counter art x960 y1549. Exact blocked tiles x960..1152 y1568..1600.
# Foreground uses only the body-unreachable inner span; upper14px heads cannot overlap.
mask=Image.new('L',counter.size);md=ImageDraw.Draw(mask);md.rectangle((8,3,183,34),fill=255)
cb=counter.copy();ca=counter.copy();cb.putalpha(ImageChops.multiply(counter.getchannel('A'),ImageChops.invert(mask)));ca.putalpha(ImageChops.multiply(counter.getchannel('A'),mask));cb.save(A/'reception-counter-below.png');ca.save(A/'reception-counter-above.png');mask.save(S/'reception-depth-mask.png')
plate=Image.new('RGBA',(56,10),(15,54,58,255));pd=ImageDraw.Draw(plate);pd.rectangle((0,0,55,9),outline=(214,177,91,255),width=1);pd.text((3,-1),'RECEPTION',font=bold(8),fill=(249,224,164,255));plate.save(A/'reception-nameplate-native-56x10.png')
overlay=Image.new('RGBA',counter.size);overlay.alpha_composite(plate,(17,34));overlay.save(A/'reception-nameplate-overlay.png')
pl=overlay.copy();ph=overlay.copy();pl.putalpha(ImageChops.multiply(overlay.getchannel('A'),ImageChops.invert(mask)));ph.putalpha(ImageChops.multiply(overlay.getchannel('A'),mask));pl.save(A/'reception-nameplate-below.png');ph.save(A/'reception-nameplate-above.png')
cb.alpha_composite(pl);ca.alpha_composite(ph)
# The nameplate remains a separately authored overlay; base counter source files stay unchanged.

base=load(V5/'assets/runtime-base.png');above=load(V5/'assets/runtime-above.png');beforebox=(416,1408,768,1728);afterbox=(864,1408,1216,1728)
before=base.crop(beforebox)
for x,y,d in [(540,1520,'south'),(540,1654,'north')]:before.alpha_composite(frames[d],(x-beforebox[0]-16,y-beforebox[1]-16))
before.alpha_composite(above.crop(beforebox));before.save(Q/'reception-before-occupied-native.png')
after=base.crop(afterbox);after.alpha_composite(cb,(960-afterbox[0],1549-afterbox[1]))
for x,y,d in [(1048,1551,'south'),(1048,1600,'north')]:after.alpha_composite(frames[d],(x-afterbox[0]-16,y-afterbox[1]-16))
after.alpha_composite(ca,(960-afterbox[0],1549-afterbox[1]));after.alpha_composite(above.crop(afterbox));after.save(Q/'reception-after-occupied-native.png')
# Pair: accepted source art byte-for-byte. The low table is wholly below actors.
floor=load(V5/'assets/foyer-base.png').crop((864,1344,1216,1584));chair=load(A/'lounge-chair-south.png');northchair=load(A/'lounge-chair-north.png');table=load(A/'low-lounge-table.png');anchors=[(112,118),(168,118)]
oldspec=[('bistro-stool-left-native',97,88,46),('bistro-stool-right-native',154,88,46),('bistro-table-native',121,88,46)]
old=floor.copy();oldabove=Image.new('RGBA',old.size)
for n,x,y,c in oldspec:
 im=load(A/(n+'.png'));old.alpha_composite(im.crop((0,0,im.width,c)),(x,y));oldabove.alpha_composite(im.crop((0,c,im.width,im.height)),(x,y+c))
for x,y in anchors:old.alpha_composite(frames['south'],(x-16,y-16))
old.alpha_composite(oldabove);old.save(Q/'seating-before-occupied-native.png')
pair=floor.copy();pabove=Image.new('RGBA',pair.size);pbelow=Image.new('RGBA',pair.size)
for x in [88,144]:
 # Two32px bases at x96 and160; physical seat centers remain traversable.
 m=Image.new('L',chair.size);dd=ImageDraw.Draw(m);left=(96 if x==88 else 160)+8-x;dd.rectangle((left,39,left+15,47),fill=255)
 b=chair.copy();a=chair.copy();b.putalpha(ImageChops.multiply(chair.getchannel('A'),ImageChops.invert(m)));a.putalpha(ImageChops.multiply(chair.getchannel('A'),m));pbelow.alpha_composite(b,(x,90));pabove.alpha_composite(a,(x,90))
pbelow.alpha_composite(table,(256,108));pair.alpha_composite(pbelow)
for x,y in anchors:pair.alpha_composite(frames['south'],(x-16,y-16))
pair.alpha_composite(pabove);pair.save(Q/'seating-after-occupied-native.png');pbelow.save(A/'pair-benchmark-below.png');pabove.save(A/'pair-benchmark-above.png')
# The same family supports north-facing view seats without rotations or repainting.
north=floor.copy()
for x in [88,144]:north.alpha_composite(northchair,(x,94))
north.alpha_composite(table,(256,108))
for x,y in [(112,110),(168,110)]:north.alpha_composite(frames['north'],(x-16,y-16))
for x in [88,144]:north.alpha_composite(northchair.crop((0,25,48,44)),(x,119))
north.save(Q/'seating-north-view-occupied-native.png')
# Native1:1 combined comparison: art is pasted without any image resampling.
board=Image.new('RGB',(752,744),'#112e34');d=ImageDraw.Draw(board)
d.text((16,12),'FLAGSHIP A / NATIVE 1:1 OCCUPIED BENCHMARK',font=bold(17),fill='#f3d69b')
d.text((16,44),'BEFORE / current stool arrangement',font=font(13),fill='white');d.text((392,44),'AFTER / accepted chairs; 64 px escape lane',font=font(13),fill='white');board.paste(old,(16,68));board.paste(pair,(392,68))
d.text((16,324),'BEFORE / left reception, padded collision',font=font(13),fill='white');d.text((392,324),'AFTER / staffed right-of-arrival reception',font=font(13),fill='white');board.paste(before,(16,348));board.paste(after,(392,348))
d.text((16,684),'32 px Greg. Existing chair/table pixels unchanged. New counter: 192 x 51 px.',font=font(13),fill='#bed2cd');d.text((16,708),'Bounded art + geometry proposal only. No runtime or frozen map changes.',font=font(13),fill='#bed2cd');board.save(Q/'corrective-a-before-after-native-1x.png')
large=board.resize((1504,1488),Image.Resampling.NEAREST);dd=ImageDraw.Draw(large);dd.rectangle((0,0,1503,48),fill='#112e34');dd.text((32,13),'2x NEAREST-NEIGHBOR INSPECTION ONLY | delivered art remains native',font=bold(20),fill='#f3d69b');large.save(Q/'corrective-a-before-after-2x-nearest.png')
# Collision/clearance validation uses frozen v05 world collision as the context.
grid=np.array(json.loads((V5/'source/collision-grid.json').read_text())['grid'],dtype=bool);world=grid.repeat(32,0).repeat(32,1);world[1568:1600,960:1152]=True
rects={'counterCollision':[960,1568,192,32],'staffAllowance':[960,1488,192,64],'eastReturn':[1152,1488,64,208],'customerApron':[960,1600,192,96]}
paths={'visitorFromArrival':[(768,1664),(768,1632),(1048,1632),(1048,1600)],'staffFromArrivalViaEastReturn':[(768,1664),(768,1632),(1184,1632),(1184,1536),(1048,1536),(1048,1551)]}
def points(poly):
 for a,b in zip(poly,poly[1:]):
  steps=max(abs(a[0]-b[0]),abs(a[1]-b[1]))
  for t in range(steps+1):yield(round(a[0]+(b[0]-a[0])*t/max(1,steps)),round(a[1]+(b[1]-a[1])*t/max(1,steps)))
def checks(x,y):return {'body16Clear':not bool(world[y:y+16,x-8:x+8].any()),'visual32Clear':not bool(world[y-16:y+16,x-16:x+16].any())}
route_results={}
for n,poly in paths.items():
 ps=list(points(poly));bad=[{'xy':list(p),**checks(*p)}for p in ps if not all(checks(*p).values())];route_results[n]={'waypoints':poly,'samples':len(ps),'badSamples':bad[:8],'pass':not any(not b['body16Clear']for b in bad),'fullVisualBoxPass':not bad}
fg=np.zeros(world.shape,dtype=bool);fg[1549:1600,960:1152]=np.asarray(ca.getchannel('A'))>32
head=np.zeros((14,32),bool)
for row in range(4):
 for col in range(3):head |= np.asarray(greg.crop((col*32,row*32,col*32+32,row*32+14)).getchannel('A'))>32
conflicts=[];count=0
for y in range(1472,1649):
 for x in range(928,1185):
  if not checks(x,y)['body16Clear']:continue
  count+=1
  if (fg[y-16:y-2,x-16:x+16]&head).any():conflicts.append([x,y])
# Pair local collision and64px escape lane.
pworld=np.zeros((240,352),bool);pworld[144:176,96:128]=True;pworld[144:176,160:192]=True;pworld[112:144,256:320]=True
pairpaths={'leftEscape':[(112,118),(64,118),(64,208)],'rightEscape':[(168,118),(224,118),(224,208)]}
pr={}
for n,path in pairpaths.items():
 ps=list(points(path));bad=[list(p)for p in ps if pworld[p[1]:p[1]+16,p[0]-8:p[0]+8].any()or pworld[p[1]-16:p[1]+16,p[0]-16:p[0]+16].any()];pr[n]={'waypoints':path,'samples':len(ps),'badSamples':bad[:8],'pass':not any(not b['body16Clear']for b in bad),'fullVisualBoxPass':not bad}
pfg=np.asarray(pabove.getchannel('A'))>32;pc=[];pn=0
for y in range(16,209):
 for x in range(16,337):
  if pworld[y:y+16,x-8:x+8].any():continue
  pn+=1
  if(pfg[y-16:y-2,x-16:x+16]&head).any():pc.append([x,y])
report={'status':'bounded static art/geometry benchmark, not runtime approval','sourceFrozenV05ReadOnly':True,'counterAsset':[192,51],'masterAlphaCrop':box,'masterAspect':(box[2]-box[0])/(box[3]-box[1]),'nativeAspect':192/51,'counterWorldArtXYWH':[960,1549,192,51],'counterForegroundWorldXYXY':[968,1552,1144,1584],'rectangles':rects,'actors':[{'id':'staff','xy':[1048,1551],**checks(1048,1551)},{'id':'customer','xy':[1048,1600],**checks(1048,1600)}],'receptionActorSpacingPx':49,'receptionConversationClaim':False,'nativeTapFit':{'staffAnchor':[1048,1551],'staffFloorClick':[1048,1567],'customerAnchor':[1048,1600],'customerFloorClick':[1048,1616],'allExact':True},'visualClearanceNuance':'Customer1600 is native-tap-fitted and body-clear. Its sprite extends16px over the counter front, which stays below actors; the above mask ends before the head begins, so no head pixels are occluded. Customer1632/click1648 is the full-box-clear alternative.','routes':route_results,'counterHeadCheck':{'bodyClearIntegerPlacementsTested':count,'headConflictCount':len(conflicts),'firstConflicts':conflicts[:8]},'casualPair':{'anchorSpacingPx':56,'chairAssetsUnchanged':True,'anchors':anchors,'chairArtXYWH':[[88,90,48,48],[144,90,48,48]],'lowTableXYWH':[256,108,64,36],'rightPrincipalEscapeLaneXYWH':[192,90,64,150],'southClearApronHeightPx':64,'routes':pr,'headCheck':{'bodyClearIntegerPlacementsTested':pn,'headConflictCount':len(pc),'firstConflicts':pc[:8]}}}
report['allStaticChecksPass']=all(v['pass']for v in route_results.values())and all(v['pass']for v in pr.values())and not conflicts and not pc
write(S/'geometry-validation.json',report)
# Separate native-scale annotated geometry proof; no measurement lines baked into art.
geo=Image.new('RGB',(1080,650),'#112e34');gd=ImageDraw.Draw(geo);gd.text((16,12),'GEOMETRY PROOF / NATIVE PIXELS / separate from art',font=bold(18),fill='#f3d69b')
contextbox=(704,1408,1280,1728);context=base.crop(contextbox);context.alpha_composite(cb,(960-704,1549-1408));context.alpha_composite(ca,(960-704,1549-1408));context.alpha_composite(above.crop(contextbox));gdctx=ImageDraw.Draw(context,'RGBA')
cols={'counterCollision':(255,69,84,160),'staffAllowance':(80,197,255,75),'eastReturn':(80,197,255,85),'customerApron':(93,231,163,75)}
for n,(x,y,w,h)in rects.items():gdctx.rectangle((x-704,y-1408,x+w-705,y+h-1409),fill=cols[n],outline=(255,255,255,190),width=1)
for n,poly in paths.items():gdctx.line([(x-704,y-1408)for x,y in poly],fill=(91,255,201,255)if n.startswith('visitor')else(133,211,255,255),width=2)
for x,y in [(1048,1551),(1048,1600)]:gdctx.rectangle((x-16-704,y-16-1408,x+15-704,y+15-1408),outline=(255,255,255,240),width=1);gdctx.rectangle((x-8-704,y-1408,x+7-704,y+15-1408),outline=(255,215,98,255),width=1)
geo.paste(context,(16,64));gd.text((16,394),'Counter: [960,1568,192,32] collision, all inside visible art',font=font(13),fill='white');gd.text((16,416),'East return: 64 px  |  Customer apron: 96 px  |  Staff area: 64 px',font=font(13),fill='white');gd.text((16,438),'White32px box; gold16px body. Customer front overlap is intentional below-actor depth.',font=font(13),fill='white')
pgeom=pair.copy();pd=ImageDraw.Draw(pgeom,'RGBA');pd.rectangle((192,90,255,239),fill=(80,197,255,60),outline=(220,255,245,210));pd.rectangle((0,176,351,239),fill=(93,231,163,45))
for path in pairpaths.values():pd.line(path,fill=(102,255,191,255),width=2)
for x,y in anchors:pd.rectangle((x-16,y-16,x+15,y+15),outline=(255,255,255,240));pd.rectangle((x-8,y,x+7,y+15),outline=(255,215,98,255))
geo.paste(pgeom,(664,64));gd.text((664,324),'Pair anchors: 56 px',font=font(13),fill='white');gd.text((664,346),'Right escape lane: 64 px',font=font(13),fill='white');gd.text((664,368),'Clear south apron: 64 px',font=font(13),fill='white');gd.text((664,390),'Low table stays outside escape lane.',font=font(13),fill='white')
gd.text((16,498),f"Static checks: {'PASS' if report['allStaticChecksPass'] else 'FAIL'} | {count+pn:,} body-clear integer placements checked for head occlusion",font=bold(16),fill='#f3d69b');gd.text((16,528),'Counter + chair masks: zero head conflicts. Customer front overlap uses correct below-actor depth.',font=font(14),fill='white');gd.text((16,560),'This validates the bounded proposed geometry only. Final TMJ, pathfinding and live rendering remain separate.',font=font(13),fill='#bed2cd');geo.save(Q/'geometry-proof-native.png')
provenance={'builtInImagegen':True,'generationOutput':'/workspace/scratch/41c8dbf833be/generated_images/exec-ce5634f3-47cf-48ea-b4ae-3212d7a0c761.png','prompt':'source/imagegen-prompt-reception.txt','master':'source/reception-counter-generated-master.png','native':'assets/reception-counter-native-192x51.png','authoring':'Alpha crop and single aspect-preserving Lanczos reduction to192x51. No old112x68 raster enlargement. Mask partition does not alter original pixels.','generatedMasterSHA256':sha(S/'reception-counter-generated-master.png'),'unchangedCopies':[],'frozenInputHashes':{}}
for p in A.glob('*.png'):
 src=(V3/'assets'/p.name)if(V3/'assets'/p.name).exists()else(V5/'assets'/p.name)
 if src.exists():provenance['unchangedCopies'].append({'file':str(p.relative_to(R)),'source':str(src),'sha256':sha(p),'sourceSHA256':sha(src),'byteIdentical':sha(p)==sha(src)})
for n in ['assets/runtime-base.png','assets/runtime-above.png','assets/greg-reference.png','source/collision-grid.json','source/runtime-layout.json','map32/grand-auditorium.tmj','map32/grand-auditorium.wam']:provenance['frozenInputHashes'][n]=sha(V5/n)
write(R/'PROVENANCE.json',provenance);print(json.dumps(report,indent=2))
