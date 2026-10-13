"""Native asset assembly only. No runtime, TMJ, network or original-file mutation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import numpy as np,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];V3=R.parent/'grand-auditorium-03-foyer-terrace';S=R/'source';A=R/'assets';Q=R/'review';W,H=2560,1920
for p in [S,A,Q]:p.mkdir(exist_ok=True)
rgba=lambda p:Image.open(p).convert('RGBA')
blank=lambda:Image.new('RGBA',(W,H))
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=rgba(S/'v03-runtime-base.png');above=rgba(S/'v03-runtime-above.png');cfg=json.loads((S/'runtime-layout.json').read_text());g=np.array(json.loads((S/'collision-grid.json').read_text())['grid'],np.uint8);blocked=Image.fromarray(np.repeat(np.repeat(g*255,32,0),32,1),'L')
# Exact copies of frozen components are supplied separately for clean furniture ownership.
for name in ['runtime-furniture-full.png','runtime-furniture-below.png','runtime-furniture-above.png']:
 shutil.copy2(V3/'source'/name,S/name)
# Keep source pixel registration. Garden does not undergo scaling or rotation.
gm=rgba(S/'garden-topdown-master-v2.png');garden=blank();paver=gm.crop((718,472,770,524));grass=gm.crop((874,730,938,794))
def tile(dst,im,box):
 x0,y0,x1,y1=box
 for y in range(y0,y1,im.height):
  for x in range(x0,x1,im.width):dst.alpha_composite(im.crop((0,0,min(im.width,x1-x),min(im.height,y1-y))),(x,y))
tile(garden,grass,(0,0,W,H));garden.alpha_composite(gm.crop((256,0,1280,1024)),(1536,0));tile(garden,paver,(1536,1024,2560,1088))
# Native lower-edge fragments. The continuous entry remains the original sandstone.
garden.alpha_composite(gm.crop((0,0,1536,160)),(0,1760));garden.alpha_composite(gm.crop((256,0,1280,160)),(1536,1760))
# The east edge is one continuous native lawn/hedge strip, beyond the terrace footprint.
for y in range(1024,1760,736):garden.alpha_composite(gm.crop((1456,0,1512,min(736,1760-y))),(2504,y))
# Replace scenery only; preserve all deck, foyer, audience and stage source pixels.
em=Image.new('L',(W,H),0);ed=ImageDraw.Draw(em)
for box in [(1536,0,2560,1088),(2504,1040,2560,1760),(1536,1760,2560,1920),(0,1776,640,1920),(896,1776,1536,1920),(0,944,8,1776)]:ed.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
# Gold entrance-post tails remain the exact frozen source.
for box in [(578,1776,640,1792),(896,1776,958,1792)]:ed.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=0)
em.save(S/'exterior-replacement-mask.png');garden.putalpha(em);garden.save(A/'garden-topdown.png')
# Foundation is original art with exterior removed. Furniture and all exact hall pixels survive.
foundation=base.copy();foundation.putalpha(ImageChops.multiply(base.getchannel('A'),ImageChops.invert(em)))
# Reassemble original authored rail alpha over the new garden, avoiding old backdrop halos.
rail=rgba(S/'reuse-inputs/terrace-rail.png');tile(foundation,rail,(1536,1040,2496,1088))
erail=rgba(S/'reuse-inputs/terrace-east-rail.png');foundation.alpha_composite(erail.crop((0,0,erail.width,32)),(2460,1056))
foundation.save(A/'foundation-preserved.png');above.save(A/'furniture-and-hall-above.png')
def masked(im,boxes):
 m=Image.new('L',(W,H));d=ImageDraw.Draw(m)
 for b in boxes:d.rectangle((b[0],b[1],b[2]-1,b[3]-1),fill=255)
 out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),m));return out
hallboxes=[(0,0,1536,1008)];foyerboxes=[(0,1008,1536,1920)];terraceboxes=[(1536,0,W,H)]
for n,boxes in [('hall',hallboxes),('foyer',foyerboxes),('terrace',terraceboxes)]:
 masked(foundation,boxes).save(A/(n+'-base.png'));masked(above,boxes).save(A/(n+'-above.png'))
# Authored raised wall modules. Source trim alpha threshold is recorded, true alpha retained.
wm=rgba(S/'wall-height-master.png');wb=wm.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox();wall=wm.crop(wb).resize((320,80),Image.Resampling.LANCZOS);wall.save(A/'wall-south-module-320x80.png')
rm=rgba(S/'roof-topdown-master.png');rb=rm.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox();roof=rm.crop(rb)
# Correctly drawn vertical source border, not a rotated horizontal wall.
side=rm.crop((1423,202,1500,802)).resize((40,312),Image.Resampling.LANCZOS);side.save(A/'wall-east-module-40x312.png')
walls=blank()
for box in [(64,1696,578,1776),(958,1696,1472,1776)]:tile(walls,wall,box)
# Upper visible facade at hall/foyer boundary stays out of both doors and pillars.
shortwall=wall.resize((320,64),Image.Resampling.LANCZOS)
for box in [(96,944,448,1008),(640,944,864,1008),(1088,944,1440,1008)]:tile(walls,shortwall,box)
# The outer east face gains a real dark/stone vertical depth strip in an already blocked band.
tile(walls,side,(1496,0,1536,944))
# Never draw structural face pixels outside already blocked collision cells.
walls.putalpha(ImageChops.multiply(walls.getchannel('A'),blocked));walls.save(A/'walls-raised-faces.png')
masked(walls,[(0,0,1536,944)]).save(A/'hall-walls-raised.png');masked(walls,[(0,944,1536,H)]).save(A/'foyer-walls-raised.png')
# Independent cast shadows. Every pixel lies in existing blocked exterior footprints.
shadow=blank();sd=ImageDraw.Draw(shadow)
for box in [(1536,32,1568,1024),(64,1776,578,1800),(958,1776,1536,1800),(1536,1760,2504,1784),(2504,1096,2536,1784)]:
 x0,y0,x1,y1=box;sd.polygon([(x0,y0),(x1,y0+12),(x1,y1),(x0,y1-12)],fill=(16,31,24,64))
shadow.putalpha(ImageChops.multiply(shadow.getchannel('A'),blocked));shadow.save(A/'shadows-exterior-cast.png')
# Additional architectural contact shadows live in blocked boundary cells, separate from art.
contact=blank();cd=ImageDraw.Draw(contact)
for b in [(56,1008,64,1696),(1464,1008,1472,1312),(1464,1472,1472,1696),(64,1696,578,1705),(958,1696,1472,1705),(1536,1080,2464,1088),(1536,1696,2464,1712)]:cd.rectangle((b[0],b[1],b[2]-1,b[3]-1),fill=(15,29,28,36))
contact.putalpha(ImageChops.multiply(contact.getchannel('A'),blocked))
# Keep every original furniture pixel outside additional contact shading.
fm=rgba(S/'runtime-furniture-full.png').getchannel('A').point(lambda v:255 if v else 0)
contact.putalpha(ImageChops.multiply(contact.getchannel('A'),ImageChops.invert(fm)));contact.save(A/'shadows-contact.png')
masked(contact,foyerboxes).save(A/'foyer-shadows-contact.png');masked(contact,terraceboxes).save(A/'terrace-shadows-contact.png')
# Full-room roof overlays use nine-slice assembly. Slate tile scale and border widths stay native.
# Native authoring size one-half the master gives roof rows about16px, independent of32px movement grid.
roof=roof.resize((750,415),Image.Resampling.LANCZOS);roof.save(A/'roof-native-master.png')
def roof_panel(width,height):
 # Retain50px border corners; repeat unadorned native slate interior and linework.
 out=Image.new('RGBA',(width,height));border=50;center=roof.crop((60,60,200,188));tile(out,center,(border,border,width-border,height-border))
 tile(out,roof.crop((60,0,200,border)),(border,0,width-border,border));tile(out,roof.crop((60,roof.height-border,200,roof.height)),(border,height-border,width-border,height))
 tile(out,roof.crop((0,60,border,200)),(0,border,border,height-border));tile(out,roof.crop((roof.width-border,60,roof.width,200)),(width-border,border,width,height-border))
 for sx,sy,dx,dy in [(0,0,0,0),(roof.width-border,0,width-border,0),(0,roof.height-border,0,height-border),(roof.width-border,roof.height-border,width-border,height-border)]:out.alpha_composite(roof.crop((sx,sy,sx+border,sy+border)),(dx,dy))
 # One native center emblem, no stretch, carefully registered within tiled field.
 emblem=roof.crop((320,155,430,275));ea=np.asarray(emblem).copy();gold=(ea[:,:,0]>ea[:,:,2]*1.3)&(ea[:,:,0]>110)&(ea[:,:,1]>65);ea[:,:,3]=np.where(gold,ea[:,:,3],0);emblem=Image.fromarray(ea,'RGBA');out.alpha_composite(emblem,((width-emblem.width)//2,(height-emblem.height)//2))
 return out
roofpolish=rgba(S/'roof-topdown-master-v2.png');rpb=roofpolish.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox();roofpolish=roofpolish.crop(rpb)
hallroof=blank();hallroof.alpha_composite(roofpolish.resize((1472,976),Image.Resampling.LANCZOS),(32,0));hallroof.save(A/'roof-auditorium-full.png')
foyerroof=blank();foyerroof.alpha_composite(roofpolish.resize((1520,800),Image.Resampling.LANCZOS),(8,976));foyerroof.save(A/'roof-foyer-full.png')
# Roof-only closed-state shadow silhouettes, alpha controlled independently by integration.
rshadow=blank();rs=ImageDraw.Draw(rshadow);rs.polygon([(1504,24),(1544,56),(1544,984),(1548,1016),(1548,1792),(1536,1808),(920,1808),(896,1776),(1528,1776),(1528,976),(1504,976)],fill=(13,25,23,76));rshadow.save(A/'shadows-roof-closed.png')
masked(rshadow,[(0,0,W,1008)]).save(A/'roof-auditorium-shadow.png');masked(rshadow,[(0,1008,W,H)]).save(A/'roof-foyer-shadow.png')
for name,im in [('roof-auditorium',hallroof),('roof-foyer',foyerroof),('shadows-roof',rshadow)]:
 ghost=im.copy();ghost.putalpha(im.getchannel('A').point(lambda v:round(v*.18)));ghost.save(A/(name+'-ghost18.png'))
# Byte-exact native32 fixture remains review-only, never placed in any asset layer.
greg=rgba(S/'v03-greg-reference.png');frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('east',7),('west',4)]}
actors=blank();seats=json.loads((S/'seats.json').read_text())
for i,s in enumerate(seats):
 if(i*7)%17<10:actors.alpha_composite(frames['north'],(s['x']-16,s['y']-16))
for p in cfg['socialAnchors']+[q for q in cfg['reviewActors']if not q.get('group')and not q.get('pair')]+[{'x':768,'y':1824,'direction':'north'}]:actors.alpha_composite(frames[p['direction']],(p['x']-16,p['y']-16))
def render(occupied=True,roofalpha=0,focus=False):
 out=Image.new('RGBA',(W,H),'#102e34')
 for im in [garden,shadow,foundation,contact,walls]:out.alpha_composite(im)
 if occupied:out.alpha_composite(actors)
 out.alpha_composite(above)
 if roofalpha:
  sh=rshadow.copy();sh.putalpha(sh.getchannel('A').point(lambda v:round(v*roofalpha)));out.alpha_composite(sh)
  for im in [hallroof,foyerroof]:
   temp=im.copy();temp.putalpha(im.getchannel('A').point(lambda v:round(v*roofalpha)));out.alpha_composite(temp)
 if focus:
  # Art-state preview only: leave the preserved hall visible and hide all surroundings.
  focusim=Image.new('RGBA',(W,H),'#102e34')
  for im in [masked(foundation,hallboxes),masked(walls,[(0,0,1536,944)]),masked(actors,hallboxes),masked(above,hallboxes)]:focusim.alpha_composite(im)
  out=focusim
 return out
empty=render(False);inside=render(True);closed=render(True,1);faded=render(True,.18);focused=render(True,0,True)
for name,im in [('empty',empty),('occupied',inside),('outside-closed',closed),('transparency-18pct',faded),('hall-focused',focused)]:im.save(Q/('flagship-v04-'+name+'-native.png'))
for name,box in [('foyer-terrace',(0,928,2560,1856)),('foyer',(32,944,1536,1792)),('terrace',(1408,944,2560,1792)),('garden-scale',(1536,640,2560,1280)),('south-wall',(448,1584,1120,1840))]:inside.crop(box).save(Q/(name+'-occupied-native.png'))
closed.crop((448,1584,1120,1840)).save(Q/'south-entry-closed-native.png');faded.crop((32,944,1536,1792)).save(Q/'foyer-transparency-native.png')
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
card=Image.new('RGB',(1920,1716),'#102e34');d=ImageDraw.Draw(card);d.text((48,26),'FLAGSHIP 04  /  ORTHOGRAPHIC GARDEN',font=bold(18),fill='#ddb96e');d.text((48,62),'A single camera. A grounded garden hall.',font=bold(34),fill='#f5e5c3');d.text((48,115),'Original stage + 210 chairs  ·  Four meeting squares  ·  Separate full-room roofs, walls and cast shadows',font=font(18),fill='#c4d1ce');card.paste(inside.resize((1792,1344),Image.Resampling.LANCZOS),(64,160));d.text((64,1533),'NATIVE GARDEN SCALE',font=bold(16),fill='#dfbd79');d.text((64,1560),'Native paving, continuous lawn and irregular planting. No horizon or receding scenery.',font=font(17),fill='#dae3db');d.text((64,1600),'PRESERVED GEOMETRY',font=bold(16),fill='#dfbd79');d.text((64,1627),'All 24 social anchors, circulation, silent route and furniture depth remain unchanged.',font=font(17),fill='#dae3db');d.text((64,1671),'ART CANDIDATE ONLY  ·  Roofs hidden in this inside/revealed view  ·  Greg32 is an unchanged review fixture',font=font(13),fill='#9fb6b6');card.save(Q/'flagship-v04-overview.png')
# Side-by-side art-state board, explicit that this is design output, not runtime proof.
board=Image.new('RGB',(1920,1736),'#102e34');bd=ImageDraw.Draw(board);bd.text((32,24),'FLAGSHIP 04  /  FULL-ROOM LAYER STATES',font=bold(26),fill='#f5e5c3')
for i,(title,im)in enumerate([('OUTSIDE / CLOSED ROOFS',closed),('INSIDE / REVEALED',inside),('18% TRANSPARENCY STUDY',faded),('STAGE FOCUS / SURROUNDINGS HIDDEN',focused)]):
 x=32+(i%2)*944;y=88+(i//2)*808;bd.text((x,y),title,font=bold(17),fill='#dfbd79');board.paste(im.resize((912,684),Image.Resampling.LANCZOS),(x,y+38))
bd.text((32,1710),'DESIGN STATES ONLY. Runtime trigger, tween and camera implementation belongs to integration.',font=font(13),fill='#9fb6b6');board.save(Q/'full-room-layer-states.png')
# Layer extents and native alpha masks for reliable map-only integration.
meta=[]
roles={'garden-topdown':'Exterior scenery; hide as surroundings in stage focus.','foundation-preserved':'Convenience unsplit foundation; do not also render hall/foyer/terrace base.','furniture-and-hall-above':'Convenience unsplit above; do not also render per-room above.','walls-raised-faces':'Optional decorative wall-height overlay. All alpha inside existing blocked cells.','shadows-exterior-cast':'Decorative ground shadow in blocked exterior cells.','shadows-contact':'Decorative contact shadow, blocked boundary cells only.','roof-auditorium-full':'Full auditorium opaque roof for outside/closed state; hidden for inside/revealed and stage focus.','roof-foyer-full':'Full foyer opaque roof; hidden when foyer is occupied and during stage focus.','shadows-roof-closed':'Pairs with visible roof state only.'}
for path in sorted(A.glob('*.png')):
 im=rgba(path)
 if im.size!=(W,H):continue
 mask=im.getchannel('A');mask.save(S/(path.stem+'-alpha.png'));meta.append({'id':path.stem,'asset':str(path.relative_to(R)),'pixels':[W,H],'alphaBoundsXYXY':mask.getbbox(),'alphaMask':str((S/(path.stem+'-alpha.png')).relative_to(R)),'collides':False,'actorDepth':'above-player' if ('roof' in path.stem or path.stem.endswith('-above') or path.stem=='furniture-and-hall-above') else 'below-player','visibilityOwnership':'hall' if path.stem.startswith('hall-') else 'foyer' if path.stem.startswith('foyer-') else 'terrace' if path.stem.startswith('terrace-') else 'opaque-roof' if path.stem in ['roof-auditorium-full','roof-foyer-full','roof-auditorium-shadow','roof-foyer-shadow','shadows-roof-closed'] else 'ghost-roof' if 'ghost18' in path.stem else 'surroundings' if path.stem in ['garden-topdown','shadows-exterior-cast'] else 'convenience-only','role':roles.get(path.stem,'Per-room ownership; hall is retained during focus, foyer/terrace hidden.'),'opaquePixelCount':int(np.sum(np.asarray(mask)>250)),'nonzeroAlphaPixelCount':int(np.sum(np.asarray(mask)>0))})
write(S/'decorative-layer-plan.json',{'status':'Art-only candidate; no trigger or runtime implementation','runtimeVisualGroups':{'alwaysBelowPlayer':['hall-base','hall-walls-raised'],'alwaysAbovePlayer':['hall-above'],'surroundings-below':['garden-topdown','shadows-exterior-cast','foyer-base','terrace-base','foyer-shadows-contact','terrace-shadows-contact','foyer-walls-raised'],'surroundings-above':['foyer-above','terrace-above'],'hall-roof':['roof-auditorium-shadow','roof-auditorium-full'],'foyer-roof':['roof-foyer-shadow','roof-foyer-full']},'runtimePlayPreference':'Fully hide relevant roof and roof shadow on entry; fully reveal interior. Ghost18 is optional review-only.','fixedGhostAlternatives':['assets/roof-auditorium-ghost18.png','assets/roof-foyer-ghost18.png','assets/shadows-roof-ghost18.png'],'fixedGhostRule':'Each ghost has baked18% native alpha. Show either opaque or ghost or neither, never opaque and ghost together. Do not apply another18% layer opacity.','permanentLogicRule':'Collision, silent tiles, areas and furniture functionality are independent from all decorative visibility groups.','tileSize':32,'worldPixels':[W,H],'layerOpacitySemantics':'Store native alpha. Do not flatten roofs or shadows into foundation; manage layer visibility/opacity independently. Roofs are complete full-room covers, not patches.','suggestedDrawOrder':['garden-topdown','shadows-exterior-cast','hall-base','foyer-base','terrace-base','foyer-shadows-contact','terrace-shadows-contact','hall-walls-raised','foyer-walls-raised','PLAYER_RUNTIME','hall-above','foyer-above','terrace-above','roof-auditorium-shadow','roof-auditorium-full','roof-foyer-shadow','roof-foyer-full'],'stateIntent':{'outsideClosed':{'roof-auditorium-full':1,'roof-foyer-full':1},'insideRevealed':{'roof-auditorium-full':0,'roof-foyer-full':0},'stageFocus':{'roof-auditorium-full':0,'roof-foyer-full':0,'surroundings':'Hide garden, foyer, terrace and their matching decorative layers; preserve hall plus hall furniture depth. Parent implements exact trigger/API.'}},'layers':meta,'sourceCrops':{'gardenTopRight':{'source':'source/garden-topdown-master-v2.png','cropXYXY':[256,0,1280,1024],'destinationXY':[1536,0],'scale':1},'wallTrimXYXY':wb,'roofTrimXYXY':rb,'roofPolishTrimXYXY':rpb,'roofNativeResize':'Full ridge/eave master resampled once to each fixed footprint; no source tiling in final roof','wallNativeResize':[320,80]}})
# Invariants concern immutable underlying hall art and exact gameplay metadata, not optional covers.
checks={'originalStageAndAll210ChairsBaseByteExact':foundation.crop((0,0,1536,944)).tobytes()==base.crop((0,0,1536,944)).tobytes(),'originalHallAboveByteExact':above.crop((0,0,1536,944)).tobytes()==rgba(V3/'assets/runtime-above.png').crop((0,0,1536,944)).tobytes(),'socialAnchors':len(cfg['socialAnchors']),'meetingSquares':len(cfg['groupBays']),'collisionGridByteEqual':sha(S/'collision-grid.json')==sha(V3/'source/collision-grid.json'),'quietGridByteEqual':sha(S/'quiet-grid.json')==sha(V3/'source/quiet-grid.json'),'runtimeLayoutByteEqual':sha(S/'runtime-layout.json')==sha(V3/'source/runtime-layout.json'),'furnitureFullByteEqual':sha(S/'runtime-furniture-full.png')==sha(V3/'source/runtime-furniture-full.png'),'wallPixelsOutsideExistingBlockedCells':int(np.sum((np.asarray(walls.getchannel('A'))>0)&(np.asarray(blocked)==0))),'gregReferenceSHA256':sha(S/'v03-greg-reference.png'),'gardenNativeScale':1,'roofFootprintsXYXY':[[32,0,1504,976],[8,976,1528,1776]],'runtimeCompiled':False,'published':False}
assert all(checks[k] for k in ['originalStageAndAll210ChairsBaseByteExact','originalHallAboveByteExact','collisionGridByteEqual','quietGridByteEqual','runtimeLayoutByteEqual','furnitureFullByteEqual']);assert checks['wallPixelsOutsideExistingBlockedCells']==0
write(S/'art-verification.json',checks);print(json.dumps(checks,indent=2))
