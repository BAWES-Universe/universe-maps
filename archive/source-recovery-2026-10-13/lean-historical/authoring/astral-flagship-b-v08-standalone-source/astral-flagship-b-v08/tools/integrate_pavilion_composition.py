"""Approved B pavilion composition. Native source chairs/tables; explicit pixel and collision contract.
This script changes B art only. Parent owns collision/TMJ integration and route validation.
Run after rebuild_material_proposal.py to obtain the final B source artwork.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';Q=R/'review';W,H=2560,1920;rgba=lambda p:Image.open(p).convert('RGBA');write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
for p in [S/'material-only',R/'assets/pavilion-components',Q/'material-only']:p.mkdir(exist_ok=True)
# Main script is the stable material source; freeze it before this composition-only pass.
for n in ['runtime-base','runtime-above']:shutil.copy2(R/'assets'/f'{n}.png',S/'material-only'/f'{n}.png')
for n in ['flagship-b-overview','pavilion-before-after-native']:shutil.copy2(Q/f'{n}.png',Q/'material-only'/f'{n}.png')
base=rgba(S/'material-only/runtime-base.png');above=rgba(S/'material-only/runtime-above.png');materialbase=base.copy();materialabove=above.copy();clean=rgba(S/'overlays/stone-new-material-under-furniture.png');cfg=json.loads((S/'frozen-a/runtime-layout.json').read_text());old=[p for p in cfg['furniture']if p['id'].startswith('garden-pair-')]
chair=rgba(S/'frozen-a-furniture/lounge-chair-north.png');table=rgba(S/'frozen-a-furniture/low-lounge-table.png');chair.save(R/'assets/pavilion-components/lounge-chair-north.png');table.save(R/'assets/pavilion-components/low-lounge-table.png')
allow=np.zeros((H,W),bool);objects=[];anchors=[]
def clear(box):
 x,y,x1,y1=box;base.paste(clean.crop(box),(x,y));above.paste((0,0,0,0),box);allow[y:y1,x:x1]=True
for p in old:clear((p['x'],p['y'],p['x']+p['width'],p['y']+p['height']))
# Clear any newly occupied but previously empty adjacent pixels from the clean material owner.
for x in [2016,2064,2240,2288]:clear((x,215,x+48,259))
for x in [2048,2240]:clear((x,156,x+64,192))
for i,(x,oldp) in enumerate(zip([2016,2064,2240,2288],old)):
 y=215;ax=x+24;ay=231;cell=ax//32*32;localx=ax-x;cut=(max(0,localx-8,cell+8-x),25,min(48,localx+8,cell+24-x),44)
 lo=chair.copy();hi=Image.new('RGBA',chair.size);hi.paste(chair.crop(cut),cut[:2]);lo.paste((0,0,0,0),cut);id=oldp['id'];below=f'assets/pavilion-components/{id}-below.png';over=f'assets/pavilion-components/{id}-above.png';lo.save(R/below);hi.save(R/over);base.alpha_composite(lo,(x,y));above.alpha_composite(hi,(x,y));foot=[cell,256,32,32]
 objects.append({'id':id,'asset':'assets/pavilion-components/lounge-chair-north.png','belowAsset':below,'aboveAsset':over,'x':x,'y':y,'width':48,'height':44,'artXYWH':[x,y,48,44],'solidFootprintXYWH':foot,'foregroundFromLocalY':25,'safeAboveLocalXYXY':list(cut),'anchor':[ax,ay],'direction':'north','floorClick':[ax,ay+16]});anchors.append({'id':id,'x':ax,'y':ay,'direction':'north','floorClick':[ax,ay+16],'pair':'garden-pair-'+str(i//2+1),'solidFootprintXYWH':foot,'chairBackFootprintXYWH':foot})
for i,x in enumerate([2048,2240]):
 id='garden-pair-'+str(i+1)+'-table';base.alpha_composite(table,(x,156));objects.append({'id':id,'asset':'assets/pavilion-components/low-lounge-table.png','belowAsset':'assets/pavilion-components/low-lounge-table.png','aboveAsset':None,'x':x,'y':156,'width':64,'height':36,'artXYWH':[x,156,64,36],'solidFootprintXYWH':[x,160,64,32],'foregroundFromLocalY':None})
base.save(R/'assets/runtime-base.png');above.save(R/'assets/runtime-above.png');Image.fromarray(allow.astype('uint8')*255).save(R/'masks/pavilion-composition-owned-pixels.png')
actors=rgba(S/'frozen-a/qa-actors-only.png');actors.paste((0,0,0,0),(1992,184,2344,272));greg=rgba(S/'frozen-a/greg-reference.png');north=greg.crop((32,96,64,128))
for p in anchors:actors.alpha_composite(north,(p['x']-16,p['y']-16))
actors.save(S/'qa-actors-final-b.png');occupied=base.copy();occupied.alpha_composite(actors);occupied.alpha_composite(above);occupied.save(Q/'flagship-b-occupied-native.png');empty=base.copy();empty.alpha_composite(above);empty.save(Q/'flagship-b-empty-native.png')
oldocc=rgba(S/'frozen-a/runtime-base.png');oldocc.alpha_composite(rgba(S/'frozen-a/qa-actors-only.png'));oldocc.alpha_composite(rgba(S/'frozen-a/runtime-above.png'))
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
for name,box in {'terrace':(1536,1056,2496,1760),'coffee':(1600,1072,2368,1312),'path':(1536,368,2304,624),'pavilion':(1920,48,2400,400),'garden':(1408,0,2496,1120),'garden-terrace-join':(2048,944,2368,1184)}.items():
 before=oldocc.crop(box);after=occupied.crop(box);after.save(Q/f'flagship-b-{name}-occupied-native.png');board=Image.new('RGB',(before.width*2+60,before.height+100),'#123036');d=ImageDraw.Draw(board);d.text((20,14),name.upper()+' / native 1:1 occupied proof',font=bold(18),fill='#f6dda6');d.text((20,49),'Frozen corrective A',font=font(15),fill='#cbddda');d.text((before.width+40,49),'Final B source art',font=font(15),fill='#cbddda');board.paste(before,(20,80));board.paste(after,(before.width+40,80));board.save(Q/f'{name}-before-after-native.png')
card=Image.new('RGB',(1664,1400),'#123036');d=ImageDraw.Draw(card);d.text((40,24),'FLAGSHIP B / GARDEN MATERIAL + PAVILION PROPOSAL',font=bold(27),fill='#f6dda6');d.text((40,68),'Mellow timber • Outdoor limestone • Paired pavilion tables •128px clear central passage',font=font(20),fill='#cbddda');card.paste(occupied.resize((1584,1188),Image.Resampling.LANCZOS),(40,112));d.text((40,1320),'Original hall, foyer, reception and native chair artwork preserved. B pavilion placement refined.',font=font(19),fill='#ebc77f');d.text((40,1355),'Static occupied source-art render, not live gameplay. Collision/TMJ and animation integration follow separately.',font=font(16),fill='#b9cfca');card.save(Q/'flagship-b-overview.png')
# Geometry delta is explicit, native32 and not applied by this art script.
contract={'status':'Approved B pavilion art integrated; parent must apply and verify collision/anchors.','removeOrReplaceFurnitureIds':[p['id']for p in old],'furniture':objects,'socialAnchors':anchors,'informalPairs':[{'id':'garden-pair-'+str(i+1),'center':[2064 if i==0 else 2288,231],'anchors':[a['id']for a in anchors[i*2:i*2+2]],'anchorDistancePx':48}for i in range(2)],'collisionDelta':{'removeCells':[],'addCells':[[64,5],[65,5],[70,5],[71,5]],'existingChairFootprintsUnchanged':True},'centralClearPassageXYWH':[2112,112,128,240],'centralClearTurnaroundXYWH':[2112,128,128,128],'safeForegroundRule':'Intersect anchor horizontal[ax-8,ax+8) with its native cell core[cell+8,cell+24); local y25..44; original A rule.','foregroundSourceChanged':False,'nativeChairSize':[48,44],'nativeTableSize':[64,36],'noNewTableAboveStrips':True,'notes':['All four accepted chair assets remain native and unrotated.','Only inner-left art shifts8px west and inner-right art shifts8px east.','Tables use native-aligned64×32px footprints; art begins4px north of solid tile row.','New table footprints do not enter central128px passage.']}
write(S/'pavilion-collision-delta-contract.json',contract)
checks={}
for name,oldim,newim in [('base',materialbase,base),('above',materialabove,above)]:
 diff=np.any(np.asarray(oldim)!=np.asarray(newim),axis=2);checks[name]={'changedPixels':int(diff.sum()),'changedOutsidePavilionOwnership':int((diff&~allow).sum())};assert checks[name]['changedOutsidePavilionOwnership']==0
# Exact raw source union for every chair; no full-width shifted strips.
checks['chairSourceSplitExact']=all(Image.alpha_composite(rgba(R/p['belowAsset']),rgba(R/p['aboveAsset'])).tobytes()==chair.tobytes()for p in objects if p['aboveAsset']);checks['foregroundStripWidthsPx']=[p['safeAboveLocalXYXY'][2]-p['safeAboveLocalXYXY'][0]for p in objects if p['aboveAsset']];checks['hallFoyerExact']=base.crop((0,0,1536,H)).tobytes()==rgba(S/'frozen-a/runtime-base.png').crop((0,0,1536,H)).tobytes();checks['parentCollisionIntegrationRequired']=True;checks['compiledByThisScript']=False;write(R/'validation/pavilion-integration.json',checks);assert checks['chairSourceSplitExact']and checks['hallFoyerExact'];print(json.dumps(checks,indent=2))
