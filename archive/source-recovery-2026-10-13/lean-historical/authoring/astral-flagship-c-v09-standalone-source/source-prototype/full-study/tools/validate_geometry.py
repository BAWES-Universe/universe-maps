from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
from frozen_inputs import frozen_b_input
R=Path(__file__).resolve().parents[1];P=R.parent
alpha=np.array(Image.open(R/'masks/full-shell-occlusion-alpha.png'))
yy,xx=np.where(alpha>0);bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
source=json.loads(frozen_b_input('source/collision-grid.json').read_text());old=np.array(source['grid'],dtype=np.uint8)
proposal=np.ones((76,88),dtype=np.uint8);proposal[8:68,4:84]=old;proposal[68:76,24:32]=0
# This is validation in memory, NOT a saved runtime collision grid.
def body_hits(x,y,r):
 x0,x1=x-r,x+r
 y0,y1=(y,y+16)if r==8 else(y-r,y+r)
 return bool((proposal[y0//32:(y1-1)//32+1,x0//32:(x1-1)//32+1]!=0).any())
route_paths={
 'south':[(896,y) for y in range(2240,1935,-8)],
 'hallEast':[(x,752) for x in range(1888,1535,-8)],
 'foyerEast':[(x,1648) for x in range(1888,1535,-8)]}
route_checks={}
for name,path in route_paths.items():route_checks[name]={'samples':len(path),'body16Blocked':[[x,y]for x,y in path if body_hits(x,y,8)],'frame32Blocked':[[x,y]for x,y in path if body_hits(x,y,16)]}
source_hashes={relative:hashlib.sha256(frozen_b_input(relative).read_bytes()).hexdigest()for relative in ['assets/runtime-base.png','assets/runtime-above.png','assets/greg-reference.png','source/collision-grid.json','source/quiet-grid.json']}
# Exact all-alpha clearance is measured in the relevant native approach bands.
sa=alpha[:,512:1280];south_max=int(np.where(sa>0)[0].max())
side_max={}
for name,y0,y1 in [('hall',432,880),('foyer',1328,1776)]:side_max[name]=int(np.where(alpha[y0:y1]>0)[1].max())
old_quiet=json.loads(frozen_b_input('source/quiet-grid.json').read_text());q=np.array(old_quiet['grid']);qy,qx=np.where(q>0)
quiet_source_bounds=[int(qx.min()*32),int(qy.min()*32),int((qx.max()+1)*32),int((qy.max()+1)*32)]
rects={'interiorBody':[128,256,1664,2032],'southApproach':[512,1696,1280,2112],'hallEastApproach':[1536,432,1832,880],'foyerEastApproach':[1536,1328,1832,1776]}
hold={k:[v[0]-32,v[1]-32,v[2]+32,v[3]+32]for k,v in rects.items()}
# Native graphics inventory: every raster is original size or uniform reduction.
geometry={
 'status':'Final visual-source geometry proposal. Runtime, collision grid and quiet receiver are NOT edited.',
 'worldPixels':[2816,2432],'worldTiles':[88,76],'tileSize':32,'translationPixels':[128,256],'translationTiles':[4,8],
 'acceptedSourceWorldPixels':[2560,1920],'acceptedBodySourceXYXY':[0,0,1536,1728],
 'acceptedInteriorBodyWorldXYXY':[128,256,1664,1984],'southThresholdWorldY':2032,
 'acceptedArrivalOpeningWorldXYXY':[768,1968,1024,2032],
 'actualBuildingVisualAlphaBoundsXYXY':bbox,
 'spawn':{'center':[896,2176],'body16XYXY':[888,2176,904,2192],'frame32XYXY':[880,2160,912,2192],'direction':'north'},
 'entrances':{
  'south':{'threshold':{'y':2032,'visualClearX':[832,960]},'existingCollisionOpeningX':[768,1024],'approachApronXYXY':[768,2032,1024,2432],'revealSouthY':2112,'restoreSouthY':2144,'allAlphaSouthernmostY':south_max,'full32FrameMarginPx':2112-16-(south_max+1)},
  'hallEast':{'threshold':{'x':1664,'visualClearY':[704,800]},'existingSourceOpeningWorldXYXY':[1536,704,1696,800],'conservativeApronXYXY':[1664,736,1920,800],'routeCenterline':[[1664,752],[1888,752]],'revealEastX':1832,'restoreEastX':1864,'allAlphaEasternmostX':side_max['hall'],'full32FrameMarginPx':1832-16-(side_max['hall']+1)},
  'foyerEast':{'threshold':{'x':1664,'visualClearY':[1600,1696]},'existingSourceOpeningWorldXYXY':[1600,1568,1664,1728],'conservativeApronXYXY':[1664,1568,1920,1696],'routeCenterline':[[1664,1648],[1888,1648]],'revealEastX':1832,'restoreEastX':1864,'allAlphaEasternmostX':side_max['foyer'],'full32FrameMarginPx':1832-16-(side_max['foyer']+1)}},
 'exteriorWalkabilityProposal':{'preserveFrozenBGridExactlyAfterTranslation':True,'preserveAWithOnlyApprovedBTableDelta':[[68,13],[69,13],[74,13],[75,13]],'addedWalkableRectXYXY':[768,2176,1024,2432],'addedWalkableTileRectXYXY':[24,68,32,76],'addedCellCount':64,'allOtherNewCells':'blocked unless explicitly designed and tested later','notACompiledGrid':True},
 'spawnQuietReceiverProposal':{'oneReceiverOnly':True,'cellCount':16,'tilesXYXY':[26,66,30,70],'pixelsXYXY':[832,2112,960,2240],'replacesAReceiverInsteadOfAddingSecond':True,'oldSourceBoundsXYXY':quiet_source_bounds,'oldTranslatedBoundsXYXY':[quiet_source_bounds[0]+128,quiet_source_bounds[1]+256,quiet_source_bounds[2]+128,quiet_source_bounds[3]+256],'audioEdited':False},
 'revealStateContract':{'entryUnionXYXY':rects,'holdOpenUnionXYXY':hold,'transition':'Instant hide of all new tall shell art plus its shadows on entry to any entry rectangle; stay revealed while in any hold rectangle; restore only after exiting the complete hold union.','initialize':'Revealed if spawned/teleported within entry union; evaluate before first visible frame.','roofFades':'No fade is asserted safe; instant hide is the current source plan.','collisionIndependent':True,'outsideCamera':'ordinary follow and user manual zoom; no new exterior camera state','hallFocus':'Independent existing native hall focus; translate accepted hall coordinates only; shell visibility must never drive it.'},
 'modules':[
  {'id':'approved-south-entrance','nativeSize':[640,320],'origin':[576,1762],'cropMasterXYXY':[0,104,1536,872],'scaleX':'5/12','scaleY':'5/12','master':'../masters/entrance-generated-master-01.png'},
  {'id':'hall-roof','nativeSize':[1536,1024],'origin':[128,96],'scaleX':'1','scaleY':'1','master':'masters/hall-roof-master-01.png'},
  {'id':'foyer-roof','nativeSize':[1536,1024],'origin':[128,1072],'scaleX':'1','scaleY':'1','master':'masters/foyer-roof-master-03.png'},
  {'id':'south-window','nativeSize':[80,250],'masterCrop':[136,200,328,800],'scaleX':'5/12','scaleY':'5/12'},
  {'id':'south-pier','nativeSize':[50,260],'masterCrop':[328,200,448,824],'scaleX':'5/12','scaleY':'5/12'},
  {'id':'hall-window','nativeSize':[96,300],'masterCrop':[136,200,328,800],'scaleX':'1/2','scaleY':'1/2'},
  {'id':'hall-pier','nativeSize':[60,312],'masterCrop':[328,200,448,824],'scaleX':'1/2','scaleY':'1/2'},
  {'id':'east-porch','nativeSize':[240,360],'origins':[[1600,488],[1600,1384]],'scaleX':'15/64','scaleY':'15/64','master':'side-porch/masters/east-side-generated-03.png'},
  {'id':'new-margin-grass','nativeSize':[768,512],'scaleX':'1/2','scaleY':'1/2','master':'masters/exterior-expansion-grass-master.png','scope':'Only new margins outside translated A; tiled with alternating reflection and native64px boundary continuation.'}],
 'placement':{'southWallFootY':2032,'southWindowY':1802,'southPierCentersX':[[153,265,377,489,601],[1191,1303,1415,1527,1639]],'hallFacadeNominalFootY':1264,'hallWindowY':988,'hallPierCentersX':[158+134*i for i in range(12)],'eastMainWallPlaneX':1664},
 'collisionRouteChecks':route_checks,'sourceHashes':source_hashes,'sourceSnapshot':'source-b-frozen','sourcePolicy':'Frozen B base, above, grid and anchors, with exact accepted A hall/foyer preserved; A and B are not modified.',
 'remainingLimits':['Side north foot positions are source-geometry inferences beneath naturally occluding canopy.','No authenticated walking, click-to-move, shell-state, camera, proximity/audio or device acceptance test.','New margins and approach extension are source proposals. Frozen finished B exterior and pavilion are integrated read-only.','No TMJ, WAM, runtime, engine, GitHub or Library mutation.']}
(R/'geometry-contract.json').write_text(json.dumps(geometry,indent=2)+'\n')
proof={'frozenBGridTranslatedExactlyInMemory':bool(np.array_equal(proposal[8:68,4:84],old)),'addedWalkableCells':int((proposal[68:76,24:32]==0).sum()),'spawnBody16Free':not body_hits(896,2176,8),'spawnFrame32Free':not body_hits(896,2176,16),'routes':route_checks,'geometryOnly':True,'runtimeWritten':False,'quietWritten':False,'revealFrameMargins':{k:v['full32FrameMarginPx']for k,v in geometry['entrances'].items()}}
(R/'validation/geometry-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
