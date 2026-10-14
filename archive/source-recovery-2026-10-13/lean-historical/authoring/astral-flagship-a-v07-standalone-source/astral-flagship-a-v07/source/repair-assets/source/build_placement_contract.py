from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFont
import json,numpy as np,hashlib
R=Path(__file__).resolve().parents[1];V5=Path('/workspace/shared/grand-auditorium-05-roofless-garden');A=R/'assets';S=R/'source';Q=R/'review'
load=lambda p:Image.open(p).convert('RGBA');write=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
old=json.loads((V5/'source/runtime-layout.json').read_text());garden=json.loads((V5/'source/garden-layout.json').read_text());grid=np.array(json.loads((V5/'source/collision-grid.json').read_text())['grid'],bool);world=grid.repeat(32,0).repeat(32,1)
ids=['indoor-casual','terrace-view-pair','terrace-lower-pair','terrace-garden-pair','garden-pair-1','garden-pair-2']
remove=[]
for o in old['solidTileRectangles']+garden['objects']:
 if any(o['id'].startswith(p)for p in ids)or o['id']=='welcome':
  rect=o.get('xywh',o.get('solidFootprintXYWH'));x,y,w,h=rect;world[y:y+h,x:x+w]=False
  if o['id']not in remove:remove.append(o['id'])
world[1568:1600,960:1152]=True
# Seats preserve56px within each pair. All face north toward foyer/hall or garden/view.
def pair(id,cx,ay,table,why,paths,apron):
 return {'id':id,'center':[cx,ay],'anchorDistancePx':56,'direction':'north','rationale':why,'chairs':[],'table':table,'expectedApproachPaths':paths,'principalClearApronXYWH':apron}
pairs=[
 pair('indoor-casual',1264,1583,[1312,1532,64,36],'Original pair center and anchors retained. Face the open foyer/hall. Low table sits northeast, outside the clear north approach and reception east return.',{'left':[[1236,1583],[1236,1520],[1184,1520]],'right':[[1292,1583],[1292,1520],[1184,1520]]},[1216,1504,96,64]),
 pair('terrace-view-pair',2256,1223,[2400,1244,64,36],'Move27px south from originaly1196 so the north-facing view seats have a broad apron by the garden rail. Table at the far east edge leaves92px of visible right-side space.',{'left':[[2228,1223],[2228,1152],[2160,1152],[2160,1312]],'right':[[2284,1223],[2284,1152],[2336,1152],[2336,1312]]},[2208,1120,96,64]),
 pair('terrace-lower-pair',1776,1607,[1920,1628,64,36],'Move7px south to fit north-chair foreground to the existing base row; face the garden/coffee terrace. Side table east with92px visible escape space.',{'left':[[1748,1607],[1748,1536],[1680,1536]],'right':[[1804,1607],[1804,1536],[1856,1536]]},[1728,1504,96,64]),
 pair('terrace-garden-pair',2224,1607,[2016,1628,64,36],'Move7px south; face the garden. Table is west, away from the southeast tree and principal north escape. Existing south planter stays untouched.',{'left':[[2196,1607],[2196,1536],[2144,1536]],'right':[[2252,1607],[2252,1536],[2320,1536]]},[2176,1504,96,64]),
 pair('garden-pair-1',2068,231,None,'Shift pair4px east and7px south to avoid west pergola strip and fit north-chair depth. Deliberately remove the tall table. Preserve64px central entry.',{'left':[[2040,231],[2040,176],[2176,176],[2176,336]],'right':[[2096,231],[2096,176],[2176,176],[2176,336]]},[2016,144,128,64]),
 pair('garden-pair-2',2284,231,None,'Shift pair4px west and7px south to avoid east pergola strip and fit north-chair depth. Deliberately remove the tall table. Preserve64px central entry.',{'left':[[2256,231],[2256,176],[2176,176],[2176,336]],'right':[[2312,231],[2312,176],[2176,176],[2176,336]]},[2208,144,128,64])]
for p in pairs:
 for side,ax in [('left',p['center'][0]-28),('right',p['center'][0]+28)]:
  ay=p['center'][1];cy=((ay+25)//32)*32;cx=(ax//32)*32;art=[ax-24,ay-16,48,44];solid=[cx,cy,32,32]
  p['chairs'].append({'id':p['id']+'-'+side,'asset':'assets/lounge-chair-north.png','artXYWH':art,'anchor':[ax,ay],'floorClick':[ax,ay+16],'direction':'north','solidFootprintXYWH':solid,'foregroundFromLocalY':25,'foregroundSafeWorldXYXY':[cx+8,cy-16,cx+24,cy+16],'foregroundRule':'Intersection of original alpha, localy>=25 and safe world rectangle. All other original alpha remains below. No copied full-width strips.','belowAsset':'assets/'+p['id']+'-'+side+'-below.png','aboveAsset':'assets/'+p['id']+'-'+side+'-above.png'})
  world[cy:cy+32,cx:cx+32]=True
 if p['table']:
  x,y,w,h=p['table'];solid=[x,y+4,w,32];p['table']={'id':p['id']+'-table','asset':'assets/low-lounge-table.png','artXYWH':p['table'],'solidFootprintXYWH':solid,'depth':'All below actors. No overhead alpha.'};world[y+4:y+36,x:x+w]=True

greg=load(A/'greg-reference.png');frame=greg.crop((32,96,64,128));head=np.zeros((14,32),bool)
for row in range(4):
 for col in range(3):head|=np.asarray(greg.crop((col*32,row*32,col*32+32,row*32+14)).getchannel('A'))>32
fullfg=np.zeros(world.shape,bool)
for p in pairs:
 for c in p['chairs']:
  chair=load(A/'lounge-chair-north.png');x,y,w,h=c['artXYWH'];xx,yy,xxx,yyy=c['foregroundSafeWorldXYXY'];mask=Image.new('L',chair.size);d=ImageDraw.Draw(mask);x0=max(0,xx-x);x1=min(w,xxx-x);y0=max(25,yy-y);y1=min(h,yyy-y)
  if x0<x1 and y0<y1:d.rectangle((x0,y0,x1-1,y1-1),fill=255)
  lo=chair.copy();hi=chair.copy();lo.putalpha(ImageChops.multiply(chair.getchannel('A'),ImageChops.invert(mask)));hi.putalpha(ImageChops.multiply(chair.getchannel('A'),mask));lo.save(R/c['belowAsset']);hi.save(R/c['aboveAsset']);fullfg[y:y+h,x:x+w]|=np.asarray(hi.getchannel('A'))>32
  c['originalPixelPartitionVerified']=Image.alpha_composite(lo,hi).tobytes()==chair.tobytes()
# Static proof against every body-clear integer placement in bounded local neighborhoods.
def checks(x,y):return {'body16Clear':not bool(world[y:y+16,x-8:x+8].any()),'visual32Clear':not bool(world[y-16:y+16,x-16:x+16].any())}
def points(poly):
 for a,b in zip(poly,poly[1:]):
  n=max(abs(a[0]-b[0]),abs(a[1]-b[1]));
  for t in range(n+1):yield(round(a[0]+(b[0]-a[0])*t/max(n,1)),round(a[1]+(b[1]-a[1])*t/max(n,1)))
for p in pairs:
 p['approachValidation']={}
 for side,path in p['expectedApproachPaths'].items():
  ps=list(points(path));bad=[{'xy':list(pt),**checks(*pt)}for pt in ps if not all(checks(*pt).values())];p['approachValidation'][side]={'samples':len(ps),'badSamples':bad[:10],'pass':not bad}
 for c in p['chairs']:
  c['anchorValidation']=checks(*c['anchor']);fx,fy=c['floorClick'];fitted=[fx//32*32+min(24,max(8,fx%32)),fy//32*32+min(32,max(16,fy%32))-16];c['nativeFit']={'floorClick':c['floorClick'],'fittedAnchor':fitted,'authoredAnchor':c['anchor'],'exact':fitted==c['anchor']}

 cx,cy=p['center'];count=0;bad=[]
 for y in range(max(16,cy-96),min(world.shape[0]-16,cy+96)):
  for x in range(max(16,cx-128),min(world.shape[1]-16,cx+128)):
   if not checks(x,y)['body16Clear']:continue
   count+=1
   if(fullfg[y-16:y-2,x-16:x+16]&head).any():bad.append([x,y])
 p['headValidation']={'bodyClearIntegerPlacements':count,'headConflictCount':len(bad),'firstConflicts':bad[:8]}
 p['allStaticChecksPass']=not bad and all(v['pass']for v in p['approachValidation'].values())and all(all(c['anchorValidation'].values())for c in p['chairs'])and all(c['originalPixelPartitionVerified']for c in p['chairs'])and all(c['nativeFit']['exact']for c in p['chairs'])
contract={'status':'component placement proposal; full-map integration and live tests not performed','assetRoot':str(R),'sourceFrozenV05':str(V5),'removeObjectIds':remove,'removeOldWelcomSign':True,'preserveAcceptedCore':'210 hall seats,16 meeting chairs,rugs,stage,room footprints and garden connections unchanged','pairCount':6,'casualSeatCount':12,'reusedNativeAssets':['assets/lounge-chair-north.png','assets/low-lounge-table.png'],'noOutdoorSouthFacingSeats':True,'pavilionCentralClearLaneXYWH':[2144,144,64,208],'pavilionTables':'Both removed deliberately; no footprint or architecture expansion.','pairs':pairs,'reception':json.loads((S/'geometry-validation.json').read_text()),'allStaticPairChecksPass':all(p['allStaticChecksPass']for p in pairs),'nativeFitSource':{'file':'/workspace/shared/grand-auditorium-05-roofless-garden/validation/native-route-proof/extracted-current-source.cjs','function':'fitBodyWithinTile','bodyHeight':16,'bodyOffsetX':0,'bodyOffsetY':8,'xOffsetRange':[8,24],'floorClickYOffsetRange':[16,32],'actorYEqualsFittedClickYMinus':16},'integrationWarning':'Use per-placement above/below images, not a generic full-width furniture strip. Contract modifies components only; re-run complete runtime collision/pathfinding/head checks after integration. No new meeting areas or proximity claims are attached to reception.'}
contract.pop('removeOldWelcomSign',None)
contract['removeOldWelcomeSign']=True
contract['receptionComponent']={'id':'welcome','replaceOldId':'welcome','asset':'assets/reception-counter-native-192x51.png','artXYWH':[960,1549,192,51],'solidFootprintXYWH':[960,1568,192,32],'belowAsset':'assets/reception-counter-below.png','aboveAsset':'assets/reception-counter-above.png','maskAsset':'source/reception-depth-mask.png','foregroundSafeWorldXYXY':[968,1552,1144,1584],'staffAnchor':[1048,1551],'staffFloorClick':[1048,1567],'staffDirection':'south','customerAnchor':[1048,1600],'customerFloorClick':[1048,1616],'customerDirection':'north','staffAllowanceXYWH':[960,1488,192,64],'eastReturnXYWH':[1152,1488,64,208],'customerApronXYWH':[960,1600,192,96],'noConversationZone':True,'oldWelcomeLabel':'Remove old raster WELCOME label together with old desk. Do not retain it floating above old location.','provenance':'PROVENANCE.json'}
contract['receptionComponent']['nameplate']={'text':'RECEPTION','authoring':'Native code-authored text on front-left fascia; no new image generation.','asset':'assets/reception-nameplate-native-56x10.png','artXYWH':[977,1583,56,10],'overlayLocalOrigin':[17,34],'overlayAtCounterOrigin':'assets/reception-nameplate-overlay.png','belowAsset':'assets/reception-nameplate-below.png','aboveAsset':'assets/reception-nameplate-above.png','partition':'Same mask as counter. Compass ornament untouched. No collision change.'}
contract['receptionComponent']['customerVisualClearance']={'body16Clear':True,'full32BoundingBoxClear':False,'counterFrontSpriteOverlapPx':16,'upperHeadPixelsOccludedByCounterAbove':0,'interpretation':'Normal depth: the visitor stands below the counter collision, and the visible head overlays its front fascia. The counter above mask ends at1584 exclusive, exactly where the sprite begins.','full32BoxNativeFitAlternative':{'anchor':[1048,1632],'floorClick':[1048,1648]}}
contract['receptionComponent']['staffVisitorDistancePx']=49
contract['receptionComponent']['ordinaryProximity']='Two-player positions are within56px and source default64px. No new meeting area or live communication guarantee is added.'
contract['checkedPairBodyPlacements']=sum(p['headValidation']['bodyClearIntegerPlacements']for p in pairs)
contract['checkedPairRouteSamples']=sum(r['samples']for p in pairs for r in p['approachValidation'].values())
write(S/'six-pair-placement-contract.json',contract)
# Clean occupied component-only cards using existing native texture; no whole-map repaint.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
card=Image.new('RGB',(1120,1048),'#112e34');d=ImageDraw.Draw(card);d.text((16,10),'SIX NATIVE OCCUPIED PLACEMENTS / SOURCE CONTRACT',font=bold,fill='#f3d69b')
for idx,p in enumerate(pairs):
 col=idx%2;row=idx//2;ox=16+col*552;oy=52+row*324;cx,cy=p['center'];box=(cx-264,cy-128,cx+264,cy+128)
 # Native floor-only sample keeps copied asset colors and proportions directly comparable.
 floor=load(V5/'assets/foyer-base.png').crop((640,1328,1168,1584))
 for c in p['chairs']:
  x,y,_,_=c['artXYWH'];floor.alpha_composite(load(R/c['belowAsset']),(x-box[0],y-box[1]))
 if p['table']:
  x,y,_,_=p['table']['artXYWH'];floor.alpha_composite(load(A/'low-lounge-table.png'),(x-box[0],y-box[1]))
 for c in p['chairs']:
  x,y=c['anchor'];floor.alpha_composite(frame,(x-16-box[0],y-16-box[1]))
 for c in p['chairs']:
  x,y,_,_=c['artXYWH'];floor.alpha_composite(load(R/c['aboveAsset']),(x-box[0],y-box[1]))
 d.text((ox,oy),p['id']+' | '+str(p['center']),font=bold,fill='white');card.paste(floor,(ox,oy+27));d.text((ox,oy+290),'North-facing,56 px pair; '+('low side table'if p['table']else'no table; clear pavilion entry'),font=font,fill='#bfd0c9')
card.save(Q/'six-pair-components-native-1x.png')
print(json.dumps({'allPass':contract['allStaticPairChecksPass'],'pairs':[{ 'id':p['id'],'pass':p['allStaticChecksPass'],'head':p['headValidation'],'routes':p['approachValidation']}for p in pairs]},indent=2))
