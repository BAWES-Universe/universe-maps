"""Source-preserving corrective A assembly. Native assets; explicit local repair ownership."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,copy,shutil
R=Path(__file__).resolve().parents[1];V=R/'source/reuse-v03';B=R/'source/reuse-v05';A=R/'source/repair-assets';S=R/'source';W,H=2560,1920
load=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n');rgba=lambda p:Image.open(p).convert('RGBA');blank=lambda:Image.new('RGBA',(W,H))
c=load(S/'baseline-v05/runtime-layout.json');orig=copy.deepcopy(c);contract=load(A/'source/six-pair-placement-contract.json');removed=set(contract['removeObjectIds']);v3=load(V/'runtime-layout.json')
adjustments=load(S/'repair-placement-adjustments.json')
for pair in contract['pairs']:
 if pair['id'] in adjustments['tableOverrides']:pair['table'].update(adjustments['tableOverrides'][pair['id']])
# Source rendering reconstructs every existing pixel in the repaired indoor/deck zones.
arch=rgba(V/'architecture-native.png');floor=arch.crop((704,1456,768,1520));plain=Image.new('RGBA',(128,96))
for yy in range(1520,1665,64):
 for xx in range(448,641,64):plain.alpha_composite(floor,(xx-480,yy-1536))
arch.paste(plain.crop((6,5,114,28)),(486,1541)) # old code-authored WELCOME sign only
arch.alpha_composite(rgba(V/'rugs-native.png'));furn=[p for p in v3['furniture']if p['id']not in removed]
for p in furn:
 if p['id']=='lounge02-west-low-divider':p['x']=576;p['solidFootprintXYWH'][0]=576
 if p['id']=='lounge02-east-low-divider':p['x']=896;p['solidFootprintXYWH'][0]=896
 if p['id']=='lounge02-north-low-divider':p['x']=608;p['width']=288;p['asset']='assets/divider-native-288x48.png';p['solidFootprintXYWH']=[608,1056,288,32]
anchors={q['id']:q for q in v3['socialAnchors']};fg=blank()
for p in furn:
 im=rgba(V/p['asset']);lo=im.copy();hi=Image.new('RGBA',im.size);an=anchors.get(p['id'])
 if an:
  y=p['foregroundFromLocalY'];x=an['x']-p['x'];cell=an['x']//32*32;box=(max(0,x-8,cell+8-p['x']),y,min(im.width,x+8,cell+24-p['x']),im.height);hi.paste(im.crop(box),(box[0],box[1]));lo.paste((0,0,0,0),box)
 arch.alpha_composite(lo,(p['x'],p['y']));fg.alpha_composite(hi,(p['x'],p['y']))
base=rgba(B/'assets/runtime-base.png');above=rgba(B/'assets/runtime-above.png');newobjects=[];newanchors=[];patches=[{'id':'center-bay-wider','xyxy':[576,1040,928,1312]},{'id':'old-welcome','xyxy':[480,1536,608,1632]}]
for p in orig['furniture']:
 if p['id']in removed:patches.append({'id':'remove-'+p['id'],'xyxy':[p['x'],p['y'],p['x']+p['width'],p['y']+p['height']]})
def addcomponent(p,root=A,kind='chair',pair=None):
 x,y,w,h=p['artXYWH'];lo=rgba(root/p.get('belowAsset',p['asset']));hi=rgba(root/p['aboveAsset'])if p.get('aboveAsset')else Image.new('RGBA',(w,h))
 arch.alpha_composite(lo,(x,y));fg.alpha_composite(hi,(x,y));patches.append({'id':'add-'+p['id'],'xyxy':[x,y,x+w,y+h]})
 record={'id':p['id'],'asset':'source/repair-assets/'+p['asset'],'x':x,'y':y,'width':w,'height':h,'solidFootprintXYWH':p['solidFootprintXYWH'],'belowAsset':'source/repair-assets/'+p.get('belowAsset',p['asset']),'aboveAsset':'source/repair-assets/'+p['aboveAsset']if p.get('aboveAsset')else None,'foregroundFromLocalY':p.get('foregroundFromLocalY')};newobjects.append(record)
 if kind=='chair':newanchors.append({'id':p['id'],'x':p['anchor'][0],'y':p['anchor'][1],'direction':p['direction'],'floorClick':p['floorClick'],'pair':pair,'solidFootprintXYWH':p['solidFootprintXYWH'],'chairBackFootprintXYWH':p['solidFootprintXYWH']})
for pair in contract['pairs']:
 if pair['id'].startswith('garden-'):continue
 for chair in pair['chairs']:addcomponent(chair,pair=pair['id'])
 if pair.get('table'):addcomponent(pair['table'],kind='table')
rec=contract['receptionComponent'];addcomponent(rec,kind='counter')
if rec.get('nameplate'):
 p=rec['nameplate'];x,y,w,h=p['artXYWH'];rx,ry=rec['artXYWH'][:2];arch.alpha_composite(rgba(A/p['belowAsset']),(rx,ry));fg.alpha_composite(rgba(A/p['aboveAsset']),(rx,ry));patches.append({'id':'reception-marker','xyxy':[x,y,x+w,y+h]})
# v05 foundation flattened translucent original floor linework over this exact source backdrop.
opaque=Image.new('RGBA',(W,H),'#102e34');opaque.alpha_composite(arch)
for p in patches:
 b=tuple(p['xyxy']);base.paste(opaque.crop(b),b[:2]);above.paste(fg.crop(b),b[:2])
# Reconstruct only the pavilion furniture patch without the rejected tall tables/stools.
plan=load(B/'art-layer-plan.json');gardenbase=Image.new('RGBA',(W,H),'#102e34');gardenabove=blank()
for n in plan['below']:
 if n!='garden-furniture-below':gardenbase.alpha_composite(rgba(B/'assets'/f'{n}.png'))
for n in plan['above']:
 if n!='garden-furniture-above':gardenabove.alpha_composite(rgba(B/'assets'/f'{n}.png'))
for pair in contract['pairs']:
 if not pair['id'].startswith('garden-'):continue
 for p in pair['chairs']:
  x,y,w,h=p['artXYWH'];gardenbase.alpha_composite(rgba(A/p['belowAsset']),(x,y));gardenabove.alpha_composite(rgba(A/p['aboveAsset']),(x,y));newobjects.append({'id':p['id'],'asset':'source/repair-assets/'+p['asset'],'x':x,'y':y,'width':w,'height':h,'solidFootprintXYWH':p['solidFootprintXYWH'],'belowAsset':'source/repair-assets/'+p['belowAsset'],'aboveAsset':'source/repair-assets/'+p['aboveAsset'],'foregroundFromLocalY':p['foregroundFromLocalY']});newanchors.append({'id':p['id'],'x':p['anchor'][0],'y':p['anchor'][1],'direction':p['direction'],'floorClick':p['floorClick'],'pair':pair['id'],'solidFootprintXYWH':p['solidFootprintXYWH'],'chairBackFootprintXYWH':p['solidFootprintXYWH']})
b=(1992,184,2344,272);base.paste(gardenbase.crop(b),b[:2]);above.paste(gardenabove.crop(b),b[:2]);patches.append({'id':'pavilion-seating','xyxy':list(b)})
base.save(R/'assets/runtime-base.png');above.save(R/'assets/runtime-above.png');shutil.copy2(B/'assets/greg-reference.png',R/'assets/greg-reference.png')
# Reapply retained physical objects after removing old footprints, avoiding ownership-clearing bugs.
h=load(S/'baseline-v05/collision-grid.json');g=np.array(h['grid'],np.uint8);oldg=g.copy();garden=load(S/'baseline-v05/garden-layout.json');oldsolids=orig['solidTileRectangles']+[{'id':p['id'],'xywh':p['solidFootprintXYWH']}for p in garden['objects']]
def rect(box,v):
 x,y,w,h=box
 if any(z%32 for z in box):raise ValueError('Collision is not native32 '+str(box))
 g[y//32:(y+h)//32,x//32:(x+w)//32]=v
for p in oldsolids:
 if p['id']in removed:rect(p['xywh'],0)
for y in range(34,41):g[y][19]=0;g[y][27]=0
for y in range(33,41):g[y][18]=1;g[y][28]=1
for x in range(19,28):g[33][x]=1
retained=[p for p in oldsolids if p['id']not in removed and not p['id'].startswith('lounge02-')]
for p in retained:rect(p['xywh'],1)
for p in newobjects:rect(p['solidFootprintXYWH'],1)
# Retain the explicitly trimmed v05 corner override; old solid metadata predates that repair.
for x,y in garden.get('runtimeRouteAdjustments',{}).get('openedCells',[]):g[y,x]=0
for x,y in garden.get('runtimeRouteAdjustments',{}).get('closedCells',[]):g[y,x]=1
h['grid']=g.tolist();h['socialAnchors']=[q for q in h['socialAnchors']if q.get('group')]+newanchors
for p in h['landmarks']:
 if p['id']=='welcome-customer':p['x'],p['y']=rec['customerAnchor']
h['landmarks']+=[{'id':'reception-staff','x':rec['staffAnchor'][0],'y':rec['staffAnchor'][1]},{'id':'reception-east-return','x':1192,'y':1536}]
save(S/'collision-grid.json',h)
c['furniture']=furn+newobjects;c['socialAnchors']=h['socialAnchors'];c['informalPairs']=[{'id':p['id'],'center':p['center'],'anchors':[q['id']for q in p['chairs']],'anchorDistancePx':56,'function':'ordinary proximity candidate; source default64px, deployed settings/media unverified'}for p in contract['pairs']];c['solidTileRectangles']=retained+[{'id':p['id'],'xywh':p['solidFootprintXYWH']}for p in newobjects]+[{'id':'lounge02-west-low-divider','xywh':[576,1056,32,256]},{'id':'lounge02-east-low-divider','xywh':[896,1056,32,256]},{'id':'lounge02-north-low-divider','xywh':[608,1056,288,32]}];c['quietTileRectangles']=[{'id':'spawn-receiver','xywh':[704,1760,128,128]}];c['quietRouteCandidates']=[];c['reception']=rec;c['status']='Corrective A integrated local candidate; route/visual review and actual room setup pending';c['repairRectangles']=patches;c['placementAdjustments']=adjustments;c['nativeFocus']={'bounds':[0,0,1536,1008],'zoomMargin':.15,'initialViewportSourceChecks':True,'rotationLimitation':True,'noScriptOrLayerVisibility':True};save(S/'runtime-layout.json',c)
garden['objects']=[p for p in garden['objects']if p['id']not in removed]+[{'id':p['id'],'type':'casual-chair-base','solidFootprintXYWH':p['solidFootprintXYWH']}for p in newobjects if p['id'].startswith('garden-')];garden['socialAnchors']=[q for q in newanchors if q['pair'].startswith('garden-')];garden['informalPairs']=[q for q in c['informalPairs']if q['id'].startswith('garden-')];save(S/'garden-layout.json',garden)
allow=np.zeros((H,W),bool)
for p in patches:x0,y0,x1,y1=p['xyxy'];allow[y0:y1,x0:x1]=1
checks=[]
for n,im in [('base',base),('above',above)]:
 before=np.asarray(rgba(B/'assets'/f'runtime-{n}.png'));after=np.asarray(im);diff=np.any(before!=after,axis=2);checks.append({'layer':n,'changedPixels':int(diff.sum()),'changesOutsideDeclaredRepairs':int((diff&~allow).sum())})
report={'preservation':checks,'acceptedHallPixelsExact':base.crop((0,0,1536,944)).tobytes()==rgba(B/'assets/runtime-base.png').crop((0,0,1536,944)).tobytes(),'repairRectangles':patches,'collisionDelta':[{'cell':[int(x),int(y)],'before':int(oldg[y,x]),'after':int(g[y,x])}for y,x in np.argwhere(g!=oldg)],'casualSeats':len(newanchors),'receptionHasConversationZone':False,'originalVersionsEdited':False};save(R/'validation/cleanup-integration.json',report);print(json.dumps({k:v for k,v in report.items()if k not in ['repairRectangles','collisionDelta']},indent=2))
