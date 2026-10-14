from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter,ImageFont
import numpy as np, json, shutil, hashlib, math, random
R=Path(__file__).resolve().parents[1];V=R/'source/rebuild-inputs/v04';V3=R/'source/rebuild-inputs/v03';S=R/'source';A=R/'assets';Q=R/'review';W,H=2560,1920
for p in [S,A,Q]:p.mkdir(exist_ok=True)
rgba=lambda p:Image.open(p).convert('RGBA')
blank=lambda:Image.new('RGBA',(W,H))
write=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
T=32
main=[(2208,1088),(2184,1024),(2160,960),(2144,896),(2128,800),(2080,672),(2048,576),(2048,480),(2080,384),(2144,288)]
branch=[(1472,496),(1568,496),(1696,528),(1888,528),(2048,512)]
def smooth(pts):
 p=[pts[0]]+pts+[pts[-1]];r=[]
 for i in range(1,len(p)-2):
  a,b,c,d=[np.array(q,float) for q in p[i-1:i+3]]
  for t in np.linspace(0,1,40,endpoint=False):
   q=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t);r.append(tuple(map(float,q)))
 r.append(pts[-1]);return r
def stroke(mask,pts,width):
 d=ImageDraw.Draw(mask);ps=smooth(pts);d.line(ps,fill=255,width=width,joint='curve')
 for x,y in ps:d.ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=255)
mask=Image.new('L',(W,H));stroke(mask,main,160);stroke(mask,branch,144)
d=ImageDraw.Draw(mask);d.rounded_rectangle((1920,64,2399,383),radius=48,fill=255)
# Exact threshold openings; outside them old building collision remains preserved.
d.rectangle((1408,448,1567,543),fill=255);d.rectangle((2144,1024,2271,1087),fill=255)
# Paving behind the east wall is hidden and cannot widen the approved hall aperture.
d.rectangle((0,0,1407,H-1),fill=0)
# Restrict garden mask to garden and the bounded hall exit, excluding the unchanged terrace interior.
d.rectangle((0,1088,W-1,H-1),fill=0)
mask.save(S/'garden-walkable-mask.png')
objects=[];seats=[]
for name,x,y in [('northwest',1952,96),('northeast',2336,96),('southwest',1952,320),('southeast',2336,320)]:objects.append({'id':'pergola-post-'+name,'type':'solid-column','solidFootprintXYWH':[x,y,32,32]})
for j,cx in enumerate([2064,2288],1):
 pair='garden-pair-'+str(j)
 # The table uses one exact solid tile. Stools have reachable occupancy anchors.
 objects.append({'id':pair+'-table','type':'bistro-table','solidFootprintXYWH':[cx-16,192,32,64]})
 for side,ax,direction in [('left',cx-28,'east'),('right',cx+28,'west')]:
  objects.append({'id':pair+'-'+side,'type':'stool-base','solidFootprintXYWH':[(ax//32)*32,256,32,32]})
  seats.append({'id':pair+'-'+side,'x':ax,'y':224,'direction':direction,'floorClick':[ax,240],'pair':pair,'solidFootprintXYWH':[(ax//32)*32,256,32,32],'chairBackFootprintXYWH':[(ax//32)*32,256,32,32],'note':'Round native bistro stool; companion-facing occupied pose; resting anchor remains traversable north of the solid base cell.'})
layout={'tileSize':32,'worldPixels':[W,H],'playerBody':[16,16],'status':'native art geometry; runtime integration pending','hallGardenDoorXYXY':[1408,448,1568,544],'terraceGardenDoorXYXY':[2144,1024,2272,1088],'paths':[{'id':'main-garden','centerline':main,'pavingWidthPx':160},{'id':'hall-branch','centerline':branch,'pavingWidthPx':144}],'walkableMask':'source/garden-walkable-mask.png','pavilionPavingXYXY':[1920,64,2400,384],'pavilionPosts':objects[:4],'objects':objects,'socialAnchors':seats,'informalPairs':[{'id':'garden-pair-'+str(i+1),'center':[cx,224],'anchorDistancePx':56,'function':'ordinary proximity candidate; no meeting/media/live claim'}for i,cx in enumerate([2064,2288])],'landmarks':[{'id':'hall-garden-threshold','xy':[1504,496]},{'id':'garden-junction','xy':[2048,512]},{'id':'terrace-garden-threshold','xy':[2208,1056]},{'id':'pavilion-turnaround','xy':[2176,160]},{'id':'pavilion-entry','xy':[2160,352]}],'roofless':True,'canopyIntent':'Generated transparent open-center pergola, side slats only. All structural tops separated from ground. No dynamic roof/focus script.'}
layout['runtimeRouteAdjustments']={'closedCells':[[35,40],[36,40],[43,40],[44,40]],'openedCells':[[44,45]],'artBounds':[{'id':'lounge03-southwest-wing','artXYWH':[1120,1264,64,48],'solidFootprintXYWH':[1120,1280,64,32]},{'id':'lounge03-southeast-wing','artXYWH':[1376,1264,64,48],'solidFootprintXYWH':[1376,1280,64,32]},{'id':'foyer-planter-upper-right-trim','artXYWH':[1408,1454,8,18],'clearedCellXYWH':[1408,1440,32,32]}],'note':'Visible low planted wings preserve192px entrance. Only the existing planter overhang is removed in the reopened corner cell; no other old cells change.'}
write(S/'garden-layout.json',layout)
# Preserve source registration, original furnishings, and immutable sprite reference.
for n in ['runtime-layout.json','collision-grid.json','quiet-grid.json','seats.json','v03-greg-reference.png']:shutil.copy2(V/'source'/n,S/('v04-'+n if n.endswith('.json') else n))
for n in ['bistro-table-native','bistro-stool-left-native','bistro-stool-right-native']:shutil.copy2(V3/'assets'/(n+'.png'),S/(n+'.png'))
# The master remains untouched. Deterministic native assembly uses exact tile footprints.
garden=rgba(V/'assets/garden-topdown.png')
# End the former off-map path with a planted northern margin. A single clean native lawn crop,
# extended only across this small former path outlet, matches the original garden texture.
grass=rgba(V/'assets/garden-topdown.png').crop((2352,352,2480,416))
northlawn=Image.new('RGBA',(256,64));northlawn.alpha_composite(grass,(0,0));northlawn.alpha_composite(grass,(128,0))
na=np.ones((64,256),dtype=np.float32)
for k in range(24):na[:,k]*=k/24;na[:,255-k]*=k/24
for k in range(16):na[63-k,:]*=k/16
northlawn.putalpha(Image.fromarray((na*255).astype('uint8')));garden.alpha_composite(northlawn,(2032,0))
# Replace the inaccessible paving stub below the railed terrace with a continuous planted strip.
scenic=rgba(V/'assets/garden-topdown.png').crop((2240,512,2496,672))
scmask=Image.new('L',(256,160),255);scd=ImageDraw.Draw(scmask)
for k in range(20):
 alpha=round(255*k/20);scd.line((k,0,k,159),fill=alpha);scd.line((255-k,0,255-k,159),fill=alpha)
scenic.putalpha(scmask);garden.alpha_composite(scenic,(2048,1760))
# Sampled warm sandstone swatches retain native grain; restrained courses provide scale.
tex=rgba(V/'assets/foyer-base.png').crop((704,1456,768,1520)).convert('RGB')
pave=Image.new('RGBA',(W,H));pd=ImageDraw.Draw(pave);rng=random.Random(5021)
for y in range(0,1120,64):
 for x in range(1376,2432,64):
  patch=tex.resize((64,64),Image.Resampling.NEAREST).convert('RGBA');arr=np.array(patch,dtype=np.int16);arr[:,:,:3]+=rng.choice([-2,-1,0,1,2]);arr=np.clip(arr,0,255).astype(np.uint8);pave.alpha_composite(Image.fromarray(arr),(x,y))
  pd.line((x,y,x+63,y),fill=(193,147,78,135),width=1);pd.line((x,y,x,y+63),fill=(199,155,84,120),width=1);pd.line((x+1,y+1,x+62,y+1),fill=(244,203,134,80),width=1)
# Ground shadow/curb remain ground-only, never overhead occlusion.
edge=mask.filter(ImageFilter.MaxFilter(9));ring=ImageChops.subtract(edge,mask)
edgeimg=Image.new('RGBA',(W,H),(116,103,39,255));edgeimg.putalpha(ring.point(lambda a:round(a*.64)));garden.alpha_composite(edgeimg)
pave.putalpha(mask);garden.alpha_composite(pave)
# Tile-registered decorative two-tone patio border, away from the north-south clear route.
patioedge=Image.new('L',(W,H));pe=ImageDraw.Draw(patioedge);pe.rounded_rectangle((1920,64,2399,383),radius=48,outline=255,width=5);pe.rectangle((2064,352,2239,391),fill=0)
patrim=Image.new('RGBA',(W,H),(187,140,67,255));patrim.putalpha(patioedge);garden.alpha_composite(patrim)
garden.save(A/'garden-topdown.png');pave.save(S/'garden-paving-below.png')
# Exact original layers copied, with only approved doorway pixels replaced.
names=['hall-base','hall-above','hall-walls-raised','foyer-base','terrace-base','foyer-above','terrace-above','foyer-walls-raised','foyer-shadows-contact','terrace-shadows-contact','shadows-exterior-cast']
layers={n:rgba(V/'assets'/(n+'.png')) for n in names}
def clear(im,box):
 d=ImageDraw.Draw(im);d.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=(0,0,0,0))
hdoor=(1408,448,1568,544);tdoor=(2144,1024,2272,1088)
for n in ['hall-base','hall-above','hall-walls-raised','shadows-exterior-cast']:clear(layers[n],hdoor)
for n in ['terrace-base','terrace-above','terrace-shadows-contact']:clear(layers[n],tdoor)
# Paving fills both honest openings, not a decal laid over a solid wall.
threshold=blank();threshold.alpha_composite(pave.crop(hdoor),(hdoor[0],hdoor[1]));threshold.alpha_composite(pave.crop(tdoor),(tdoor[0],tdoor[1]));# A visible recessed sandstone door frame: side-jamb caps outside the96px aperture,
# plus shallow threshold insets on the floor. All trim is below actors and non-colliding.
td=ImageDraw.Draw(threshold)
for yy in [440,544]:
 td.rectangle((1408,yy,1535,yy+7),fill=(146,108,62,255))
 td.line((1408,yy,1535,yy),fill=(237,207,151,255),width=2)
 td.line((1408,yy+7,1535,yy+7),fill=(92,67,41,210),width=2)
for xx in [1452,1516]:
 td.rectangle((xx,448,xx+3,543),fill=(177,137,85,180))
 td.line((xx+4,448,xx+4,543),fill=(231,204,157,180))
# Soft contact shade at jamb cheeks describes wall depth without hiding any avatar.
for yy in [448,540]:td.rectangle((1408,yy,1535,yy+3),fill=(88,72,48,48))
threshold.save(A/'garden-thresholds-below.png')
# Cap the cut rail in the immediately adjacent already-solid cells using its authored gold posts.
rail=rgba(V3/'assets/terrace-rail.png');cap=rail.crop((0,0,24,48))
for x in [2120,2272]:layers['terrace-base'].alpha_composite(cap,(x,1040))
# Hall threshold side lights reuse the original lower gate-post endcap, outside the clear opening.
hallcap=rgba(V/'assets/hall-base.png').crop((1444,428,1494,448))
layers['hall-base'].alpha_composite(hallcap,(1444,428));layers['hall-base'].alpha_composite(hallcap,(1444,544))
# The audited route remedy uses the original native low-divider art, cropped with intact endcaps.
divider=rgba(V3/'assets/divider-horizontal-low-352x48.png');wing=Image.new('RGBA',(64,48))
wing.alpha_composite(divider.crop((0,0,12,48)),(0,0));wing.alpha_composite(divider.crop((152,0,192,48)),(12,0));wing.alpha_composite(divider.crop((340,0,352,48)),(52,0))
wing.save(S/'lounge03-south-wing-native.png')
routeart=blank()
for xx in [1120,1376]:routeart.alpha_composite(wing,(xx,1264));layers['foyer-base'].alpha_composite(wing,(xx,1264))
routeart.save(S/'route-adjustment-wings-below.png')
# Clear only the actual nonzero foliage pixels in the8×18 upper-right overhang.
oldplanter=rgba(V3/'assets/planter-low.png');trim=oldplanter.getchannel('A').crop((112,0,120,18)).point(lambda a:255 if a else 0)
floor=rgba(V/'assets/foyer-base.png').crop((1280,1454,1288,1472));layers['foyer-base'].paste(floor,(1408,1454),trim)
a=layers['foyer-above'].crop((1408,1454,1416,1472));a.putalpha(ImageChops.multiply(a.getchannel('A'),ImageChops.invert(trim)));layers['foyer-above'].paste(a,(1408,1454))
trim.save(S/'foyer-planter-overhang-trim-mask.png');layout['runtimeRouteAdjustments']['trimmedFoliagePixelCount']=int(np.count_nonzero(np.asarray(trim)));layout['runtimeRouteAdjustments']['trimmedFoliageAlphaAbove32Count']=int(np.count_nonzero(np.asarray(oldplanter.getchannel('A').crop((112,0,120,18)))>32))
for n,im in layers.items():im.save(A/(n+'.png'))
# Build an exact-footprint pergola from the generated master, not from schematic placeholders.
master=rgba(S/'pergola-generated-master.png');bb=master.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox();perg=master.crop(bb).resize((448,304),Image.Resampling.LANCZOS);perg.save(S/'pergola-native-full.png')
# Source image mapped to known post corners. Affine crop rebuilding preserves four separate posts.
# Native corner crops include tops/shafts but place their ground bases inside the stated32px footprints.
pergground=blank();pergabove=blank();postnative=[]
# Master corner rectangles chosen from rendered master: foliage overhang goes above only.
post_crops=[(79,60,262,304),(1250,60,1461,304),(79,666,262,942),(1250,666,1461,942)]
for obj,crop in zip(objects[:4],post_crops):
 x,y,w,h=obj['solidFootprintXYWH'];p=master.crop(crop).resize((48,72),Image.Resampling.LANCZOS);p.save(S/(obj['id']+'.png'))
 # Top/shaft extends40px north; base occupies the32px collision tile.
 px=x-8;py=y-40
 pergground.alpha_composite(p,(px,py));pergabove.alpha_composite(p,(px,py));obj['artXYWH']=[px,py,48,72];obj['groundLayer']='assets/pergola-below.png';obj['aboveLayer']='assets/pergola-above.png'
# Perimeter beams keep all central arrival cells fully transparent. Source gold/teal beam from master.
northbeam=master.crop((326,120,1200,196)).resize((352,24),Image.Resampling.LANCZOS)
pergabove.alpha_composite(northbeam,(1984,56));pergabove.alpha_composite(northbeam.crop((0,0,144,24)),(1984,288));pergabove.alpha_composite(northbeam.crop((208,0,352,24)),(2192,288))
# Side slatted wings stay within the48px perimeter strip: open center≥320px.
leftwing=master.crop((126,210,332,750)).resize((48,208),Image.Resampling.LANCZOS)
rightwing=master.crop((1172,210,1380,750)).resize((48,208),Image.Resampling.LANCZOS)
pergabove.alpha_composite(leftwing,(1968,88));pergabove.alpha_composite(rightwing,(2336,88))
# Slat shadows are separate transparent ground art; no real height physics claimed.
shadow=blank();sd=ImageDraw.Draw(shadow)
for x in [1968,2336]:
 for y in range(96,304,20):sd.polygon([(x+10,y+16),(x+56,y+28),(x+56,y+34),(x+10,y+22)],fill=(32,43,27,45))
for obj in objects[:4]:
 x,y,w,h=obj['solidFootprintXYWH'];sd.polygon([(x,y+20),(x+32,y+20),(x+54,y+44),(x+24,y+48)],fill=(26,40,28,60))
# Keep standing actor's entire head in the central sky opening. Structural pixels are above only.
# Static depth ownership: decorative canopy must never cover a roaming avatar's head.
# Preserve the composed pergola pixels exactly, but retain only safe16×16 column-core
# foreground inside each32×32 blocked foot tile. All slats/lintels are below actors.
pergabove.save(S/'pergola-authored-structure.png')
structure=pergground.copy();structure.alpha_composite(pergabove)
safe=Image.new('L',(W,H));safeD=ImageDraw.Draw(safe)
for obj in objects[:4]:
 x,y,w,h=obj['solidFootprintXYWH'];safeD.rectangle((x+8,y,x+23,y+15),fill=255)
pergabove=structure.copy();pergabove.putalpha(ImageChops.multiply(structure.getchannel('A'),safe))
pergground=structure.copy();pergground.putalpha(ImageChops.multiply(structure.getchannel('A'),ImageChops.invert(safe)))
shadow.save(A/'pergola-shadows-below.png');pergground.save(A/'pergola-below.png');pergabove.save(A/'pergola-above.png')
# Bistro native furniture is preserved from the same polished asset family. Actual anchors face in.
furn=blank();fabove=blank()
for pair in layout['informalPairs']:
 cx,cy=pair['center']; specs=[('left','bistro-stool-left-native',cx-43,cy-30),('right','bistro-stool-right-native',cx+14,cy-30),('table','bistro-table-native',cx-19,cy-30)]
 for side,name,x,y in specs:
  im=rgba(S/(name+'.png'));furn.alpha_composite(im,(x,y));fg=im.crop((0,46,im.width,im.height))
  if side=='table':furn.alpha_composite(fg,(x,y+46))
  else:
   # Only the central16px apron strip is safe at every roaming approach.
   ax=cx+(-28 if side=='left' else 28);cellx=(ax//32)*32
   fm=Image.new('L',fg.size);fd=ImageDraw.Draw(fm);fd.rectangle((cellx+8-x,0,cellx+23-x,fg.height-1),fill=255)
   upper=fg.copy();upper.putalpha(ImageChops.multiply(fg.getchannel('A'),fm))
   lower=fg.copy();lower.putalpha(ImageChops.multiply(fg.getchannel('A'),ImageChops.invert(fm)))
   furn.alpha_composite(lower,(x,y+46));fabove.alpha_composite(upper,(x,y+46))
  p=next((o for o in objects if o['id']==pair['id']+'-'+side),None)
  if p:p['artXYWH']=[x,y,im.width,im.height]
furn.save(A/'garden-furniture-below.png');fabove.save(A/'garden-furniture-above.png');write(S/'garden-layout.json',layout)
base=Image.new('RGBA',(W,H),'#102e34')
order=[garden,layers['shadows-exterior-cast'],layers['hall-base'],layers['foyer-base'],layers['terrace-base'],layers['foyer-shadows-contact'],layers['terrace-shadows-contact'],layers['hall-walls-raised'],layers['foyer-walls-raised'],threshold,shadow,pergground,furn]
for im in order:base.alpha_composite(im)
above=blank()
for im in [layers['hall-above'],layers['foyer-above'],layers['terrace-above'],fabove,pergabove]:above.alpha_composite(im)
base.save(A/'runtime-base.png');above.save(A/'runtime-above.png')
# No review actor is ever part of runtime art.
greg=rgba(S/'v03-greg-reference.png');frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('east',7),('west',4)]}
actors=blank();old=json.loads((V/'source/runtime-layout.json').read_text());hallseats=json.loads((V/'source/seats.json').read_text())
for i,s in enumerate(hallseats):
 if (i*7)%17<10:actors.alpha_composite(frames['north'],(s['x']-16,s['y']-16))
for p in old['socialAnchors']+seats+[{'x':1504,'y':496,'direction':'east'},{'x':1744,'y':528,'direction':'east'},{'x':2048,'y':512,'direction':'north'},{'x':2144,'y':880,'direction':'north'},{'x':2208,'y':1056,'direction':'north'},{'x':2176,'y':160,'direction':'south'},{'x':768,'y':1824,'direction':'north'},{'x':768,'y':280,'direction':'south'}]:actors.alpha_composite(frames[p['direction']],(p['x']-16,p['y']-16))
empty=base.copy();empty.alpha_composite(above);occupied=base.copy();occupied.alpha_composite(actors);occupied.alpha_composite(above)
empty.save(Q/'flagship-v05-empty-native.png');occupied.save(Q/'flagship-v05-occupied-native.png');actors.save(Q/'qa-actors-only.png')
for name,box in [('garden',(1376,0,2464,1152)),('pavilion',(1888,32,2432,416)),('hall-garden-door',(1344,384,1760,608)),('terrace-garden-door',(2032,944,2336,1280))]:occupied.crop(box).save(Q/(name+'-occupied-native.png'))
# Self-contained review board, native art supplied separately for inspection.
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
card=Image.new('RGB',(1664,1404),'#102e34');cd=ImageDraw.Draw(card);cd.text((40,22),'FLAGSHIP v05 / ROOFLESS GARDEN WALK',font=bold(27),fill='#f5dda4');cd.text((40,65),'Hall garden door • Coffee terrace gate • Open pergola with companion-facing seating',font=font(21),fill='#bed2cd');card.paste(occupied.resize((1584,1188),Image.Resampling.LANCZOS),(40,108));cd.text((40,1320),'210 original hall seats + 24 original social anchors preserved. Four new outdoor seats.',font=font(21),fill='#e7bb66');cd.text((40,1360),'Native32 art preview. No interior roofs. No visibility or camera script. Runtime validation separate.',font=font(17),fill='#b7ccc8');card.save(Q/'flagship-v05-overview.png')
checks={'worldPixels':[W,H],'originalHallChairsCount':len(hallseats),'originalSocialAnchorsCount':len(old['socialAnchors']),'newGardenAnchorsCount':len(seats),'noRoofLayers':True,'gregSHA256':hashlib.sha256((S/'v03-greg-reference.png').read_bytes()).hexdigest(),'sourceStageByteExact':layers['hall-base'].crop((0,0,1408,416)).tobytes()==rgba(V/'assets/hall-base.png').crop((0,0,1408,416)).tobytes(),'hallChangesRestrictedToDoorAndJambs':True,'imagegenMode':'built-in','imagegenMaster':'source/pergola-generated-master.png','imagegenPrompt':'source/imagegen-prompt-pergola.txt','runtimeActorsBaked':False}
allow=np.asarray(routeart.getchannel('A'))>0;allow=allow.copy();allow[1454:1472,1408:1416]|=np.asarray(trim)>0
fdiff=np.any(np.asarray(layers['foyer-base'])!=np.asarray(rgba(V/'assets/foyer-base.png')),axis=2)
checks['foyerPixelsChangedOutsideExactWingAndTrimMasks']=int(np.count_nonzero(fdiff&~allow));checks['foyerPreservationExceptions']=layout['runtimeRouteAdjustments']
write(S/'art-verification.json',checks)
write(S/'art-layer-plan.json',{'worldPixels':[W,H],'below':['garden-topdown','shadows-exterior-cast','hall-base','foyer-base','terrace-base','foyer-shadows-contact','terrace-shadows-contact','hall-walls-raised','foyer-walls-raised','garden-thresholds-below','pergola-shadows-below','pergola-below','garden-furniture-below'],'above':['hall-above','foyer-above','terrace-above','garden-furniture-above','pergola-above'],'merged':['assets/runtime-base.png','assets/runtime-above.png'],'collision':'Explicit garden-layout solids + conservative core derived from garden-walkable-mask; base collision preserved apart from doors.','canopy':'Open center; no interior roof, no alpha state or dynamic scripts.'})
print(json.dumps(checks,indent=2))
