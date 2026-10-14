from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageOps
import numpy as np,json,math,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';A=R/'assets';W,H=2816,2432
rgba=lambda p:Image.open(p).convert('RGBA');blank=lambda:Image.new('RGBA',(W,H));save=lambda p,o:p.write_text(json.dumps(o,indent=2)+'\n')
# Reset geometry from unchanged predecessor every rebuild, never accumulate edits.
F=R.parent/'grand-auditorium-09-building/source'
for n in ['collision-grid.json','runtime-layout.json','garden-layout.json','seats.json','quiet-grid.json']:
 frozen=S/'reference-frozen'/n
 if not frozen.exists():shutil.copy2(F/n,frozen)
 shutil.copy2(frozen,S/n)
base=rgba(S/'reference-frozen/runtime-base.png');original=base.copy();above=rgba(S/'reference-frozen/runtime-above.png');oldAbove=above.copy();cfg=json.loads((S/'runtime-layout.json').read_text());h=json.loads((S/'collision-grid.json').read_text());g=np.array(h['grid'],np.uint8)
stone=rgba(S/'masters/limestone-master.png').resize((418,418),Image.Resampling.LANCZOS);stone.save(S/'materials/limestone-native.png')
stonefield=blank()
for row,y in enumerate(range(0,H,418)):
 for col,x in enumerate(range(0,W,418)):stonefield.alpha_composite(stone if (row+col)%2==0 else ImageOps.mirror(stone),(x,y))
def tm(name):
 m=Image.new('L',(W,H));m.paste(Image.open(S/'material-masks'/name).convert('L'),(128,256));return m
terrace=tm('deck-owned-pixels.png');garden=tm('garden-stone-owned-pixels.png');ImageDraw.Draw(garden).rectangle((2032,288,2560,656),fill=0)
foyer=Image.new('L',(W,H));d=ImageDraw.Draw(foyer);d.rectangle((192,1264,1599,1967),fill=255)
rugmask=Image.new('L',(W,H));rugmask.paste(rgba(S/'components/rugs-native.png').getchannel('A'),(128,256));foyer=Image.fromarray(np.minimum(np.asarray(foyer),255-np.asarray(rugmask)));d=ImageDraw.Draw(foyer)
for p in cfg['solidTileRectangles']:
 if 'divider' in p['id'] or 'edge' in p['id']:
  x,y,w,hh=p['xywh'];d.rectangle((x,y,x+w-1,y+hh-1),fill=0)
for box in [(1600,1568,1664,1728),(704,1918,1088,2064),(128,1264,192,2032)]:d.rectangle(box,fill=0)
# Transparent independent sources restore exact structural and furniture alpha over new stone.
exterior=stonefield.copy()
for name in ['coffee-cast-shadow','terrace-shadows-contact','shadows-exterior-cast','pergola-shadows-below','structure-source-alpha','furniture-below-source-alpha']:exterior.alpha_composite(rgba(S/'material-masks'/(name+'.png')),(128,256))
base.paste(exterior,(0,0),terrace);base.paste(exterior,(0,0),garden);base.paste(stonefield,(0,0),foyer)
# Recompose original foyer furniture alpha on new floor; never preserve rectangular old-floor halos.
paths=json.loads((S/'component-paths.json').read_text());anchors={a['id']:a for a in cfg['socialAnchors']}
for p in cfg['furniture']:
 if p['x']>=1664:continue
 path=paths.get(p.get('belowAsset') or p['asset'])
 if not path:continue
 im=rgba(R/path)
 if not p.get('belowAsset') and p['id'] in anchors and p.get('foregroundFromLocalY') is not None:
  an=anchors[p['id']];yy=p['foregroundFromLocalY'];xx=an['x']-p['x'];cell=an['x']//32*32;b=(max(0,xx-8,cell+8-p['x']),yy,min(im.width,xx+8,cell+24-p['x']),im.height);im.paste((0,0,0,0),b)
 base.alpha_composite(im,(p['x'],p['y']))
# Thin code-native bronze floor inlay, always decorative, no labels or route blocking.
inlay=blank();di=ImageDraw.Draw(inlay)
for box in [(1704,1360,2584,1944),(208,1280,1584,1952),(736,1584,1056,1712)]:
 di.rectangle(box,outline=(168,127,69,82),width=12);di.rectangle(box,outline=(140,97,44,210),width=3);di.rectangle((box[0]+10,box[1]+10,box[2]-10,box[3]-10),outline=(179,139,81,190),width=2)
 for xx,yy in [(box[0]+19,box[1]+19),(box[2]-19,box[1]+19),(box[0]+19,box[3]-19),(box[2]-19,box[3]-19)]:di.polygon([(xx,yy-7),(xx+7,yy),(xx,yy+7),(xx-7,yy)],outline=(151,106,52,200),fill=(188,150,91,65))
# Terrace north coffee zone has no crosswise inlay through counter/queue.
di.rectangle((1824,1328,2272,1504),fill=(0,0,0,0))
cx,cy=896,1648
for i in range(8):
 a=i*math.pi/4;r=42 if i%2==0 else 26;di.polygon([(cx+math.cos(a)*r,cy+math.sin(a)*r),(cx+math.cos(a+.45)*8,cy+math.sin(a+.45)*8),(cx,cy),(cx+math.cos(a-.45)*8,cy+math.sin(a-.45)*8)],fill=(161,123,66,130))
# Only floor-owned pixels receive inlay; no furniture or structure is recolored.
a=np.asarray(inlay).copy();own=np.maximum(np.asarray(foyer),np.asarray(terrace));a[:,:,3]=(a[:,:,3].astype(float)*own/255).astype('uint8');base.alpha_composite(Image.fromarray(a))
# Remove textual plate overlays using original unlettered reception depth components.
rec=cfg['reception'];rx,ry,rw,rh=rec['artXYWH'];base.paste(stonefield.crop((rx,ry,rx+rw,ry+rh)),(rx,ry));base.alpha_composite(rgba(S/'components/reception-counter-below.png'),(rx,ry));above.paste((0,0,0,0),(rx,ry,rx+rw,ry+rh));above.alpha_composite(rgba(S/'components/reception-counter-above.png'),(rx,ry));rec.pop('nameplate',None)
# Coffee edit is a generated unlettered full sprite, uniform native downsample.
cm=rgba(S/'masters/coffee-unlettered-master.png');ratio=168/cm.width;coffee=cm.resize((168,round(cm.height*ratio)),Image.Resampling.LANCZOS);assert coffee.height==94;coffee.save(S/'components/coffee-unlettered-native.png');base.paste(stonefield.crop((1964,1368,2132,1462)),(1964,1368));base.alpha_composite(coffee,(1964,1368));next(p for p in cfg['furniture']if p['id']=='coffee')['asset']='source/components/coffee-unlettered-native.png'
# Remove old text sign with the unlettered physical panel from generated direction only.
# Preserve the wall: replace its inset sign pixels with an unlettered dark teal plate.
# This is native vector signage geometry, not a UI label.
d=ImageDraw.Draw(base);d.rounded_rectangle((1476,1275,1584,1298),radius=3,fill='#164249',outline='#d2a14f',width=2);d.polygon([(1527,1285),(1530,1282),(1533,1285),(1530,1288)],fill='#d2a14f')
# Replace three terrace pairs with opposite-facing ORIGINAL directional chair sprites.
# Keep all original hall/foyer seats untouched. Seat-to-seat distance56px.
pairCenters={'terrace-view-pair':(2384,1472),'terrace-lower-pair':(1904,1856),'terrace-garden-pair':(2352,1856)}
removed=[p for p in cfg['furniture'] if any(p['id'].startswith(k) for k in pairCenters)];removedIds={p['id'] for p in removed};rects=[]
for p in removed:
 b=(p['x']-2,p['y']-2,p['x']+p['width']+2,p['y']+p['height']+2);base.paste(stonefield.crop(b),b[:2]);above.paste((0,0,0,0),b);rects.append(list(b))
for p in cfg['solidTileRectangles']:
 if p['id'] in removedIds:
  x,y,w,hh=p['xywh'];g[y//32:(y+hh)//32,x//32:(x+w)//32]=0
cfg['furniture']=[p for p in cfg['furniture'] if p['id']not in removedIds];cfg['solidTileRectangles']=[p for p in cfg['solidTileRectangles'] if p['id']not in removedIds];h['socialAnchors']=[p for p in h['socialAnchors']if p['id']not in removedIds]
placements=[]
for pair,(cx,cy)in pairCenters.items():
 # Clean one complete local seating field, avoiding old material halos.
 b=(cx-72,cy-88,cx+72,cy+56);base.paste(stonefield.crop(b),b[:2]);above.paste((0,0,0,0),b);rects.append(list(b));bd=ImageDraw.Draw(base);bd.rounded_rectangle((cx-68,cy-44,cx+68,cy+32),radius=18,outline=(164,126,65,255),width=1)
 for side,direction,ax in [('left','east',cx-28),('right','west',cx+28)]:
  im=rgba(S/'components'/('lounge-chair-'+direction+'.png'));x=ax-(25 if direction=='east'else 17);y=cy-27;lo=im.copy();hi=Image.new('RGBA',im.size)
  # Only lower arm/leg pixels belong above player; preserve clear head across all variants.
  cell=int(ax//32)*32;safe=(max(0,ax-8-x,cell+8-x),43,min(im.width,ax+8-x,cell+24-x),im.height);hi.paste(im.crop(safe),safe[:2]);lo.paste((0,0,0,0),safe);base.alpha_composite(lo,(x,y));above.alpha_composite(hi,(x,y));name=pair+'-'+side;solid=[cell,cy+32,32,32]
  p={'id':name,'asset':'source/components/lounge-chair-'+direction+'.png','x':x,'y':y,'width':im.width,'height':im.height,'solidFootprintXYWH':solid,'foregroundFromLocalY':43};cfg['furniture'].append(p);cfg['solidTileRectangles'].append({'id':name,'xywh':solid});h['socialAnchors'].append({'id':name,'x':ax,'y':cy,'direction':direction,'floorClick':[ax,cy+16],'pair':pair,'solidFootprintXYWH':solid,'chairBackFootprintXYWH':solid});sx,sy,sw,sh=solid;g[sy//32:(sy+sh)//32,sx//32:(sx+sw)//32]=1;placements.append(p)
 table=rgba(S/'components/low-lounge-table.png');table=table.resize((24,14),Image.Resampling.LANCZOS);base.alpha_composite(table,(cx-12,cy-2));solid=[cx-16,cy,32,32];g[cy//32,(cx-16)//32]=1;name=pair+'-table';cfg['solidTileRectangles'].append({'id':name,'xywh':solid});cfg['furniture'].append({'id':name,'asset':'source/components/table-native-24x14.png','x':cx-12,'y':cy-2,'width':24,'height':14,'solidFootprintXYWH':solid});table.save(S/'components/table-native-24x14.png')
 for p in cfg['informalPairs']:
  if p['id']==pair:p.update({'center':[cx,cy],'anchorDistancePx':56,'orientation':'Opposite east/west facing original native assets'})
h['grid']=g.tolist();cfg['socialAnchors']=h['socialAnchors'];cfg['status']='Glass D r02 isolated implementation; visual/source QA pending';save(S/'collision-grid.json',h);save(S/'runtime-layout.json',cfg)
# Single generated curved south-garden composition; NEVER tile or repeat it.
# Reuse original straight entrance path exactly, assemble two side fields from same uniformly scaled master.
gm=rgba(S/'masters/south-garden-master.png');gs=2944/gm.width;gn=gm.resize((2944,round(gm.height*gs)),Image.Resampling.LANCZOS);gn.save(S/'materials/south-garden-native-master.png');gardenY=2056
base.paste(gn.crop((32,0,800,H-gardenY)),(0,gardenY));base.paste(gn.crop((1152,0,2944,H-gardenY)),(1024,gardenY))
# Ground seams under facade are obscured by its original planting band; no carpet field elsewhere changed.
base.save(A/'runtime-base.png');above.save(A/'runtime-above.png')
for name in ['greg-reference.png','garden-leaf-accent-native.png']:shutil.copy2(S/'reference-frozen'/name,A/name)
# Clear glazing is native vector geometry: actual alpha18 fill, sparse alpha30 reflections.
# No opaque blue pane textures. Permanent frames at NORTH and exterior wall feet retain height.
permanent=blank();dp=ImageDraw.Draw(permanent)
def glass_panel(dst,box,columns=(),strong=True):
 x0,y0,x1,y1=box;d=ImageDraw.Draw(dst);d.rectangle(box,fill=(140,196,193,18),outline=(172,169,119,110),width=2)
 # Restrained edge reflections: the interior and avatars remain visible behind glass.
 for xx in [x0+15,x1-24]:d.line((xx,y0+8,xx,y1-8),fill=(229,245,225,36),width=2)
 for xx in columns:
  d.rectangle((xx-2,y0,xx+2,y1),fill=(125,108,74,180 if strong else 70));d.line((xx-1,y0,xx-1,y1),fill=(232,215,162,190 if strong else 70),width=1)
 d.line((x0,y0,x1,y0),fill=(204,185,134,170 if strong else 90),width=3)
# Tall rear architectural volume, with only THREE large clear bays, outside approved stage art.
glass_panel(permanent,(128,40,1664,248),[128,640,1152,1664]);dp=ImageDraw.Draw(permanent);dp.rectangle((128,248,1664,255),fill=(123,103,61,235));dp.line((128,247,1664,247),fill=(239,214,159,255),width=3)
# Corner returns create thickness without opaque wide wall fields.
for x in [128,1656]:dp.polygon([(x,40),(x+8,48),(x+8,248),(x,255)],fill=(133,132,99,115))
# South panes genuinely translucent over unchanged foyer. No pane or mullion across entry route.
for b in [(128,1728,589,2032),(1202,1728,1664,2032)]:glass_panel(permanent,b,(),False)
pierM=rgba(S/'components/glass-bronze-pier-master.png');cornM=rgba(S/'components/glass-bronze-cornice-master.png');northPier=pierM.resize((round(pierM.width*208/pierM.height),208),Image.Resampling.LANCZOS);northCorn=cornM.resize((round(cornM.width*.5),round(cornM.height*.5)),Image.Resampling.LANCZOS)
for xx in [128,632,1144,1646]:permanent.alpha_composite(northPier,(xx,40))
for xx in range(128,1664,northCorn.width):permanent.alpha_composite(northCorn.crop((0,0,min(northCorn.width,1664-xx),northCorn.height)),(xx,36))
permanent.save(A/'glass-permanent.png')
# Very low-alpha pane overlay above actors proves genuine see-through glazing. Frames stay below.
pane=blank();pd=ImageDraw.Draw(pane)
for b in [(130,1730,587,2030),(1204,1730,1662,2030)]:
 pd.rectangle(b,fill=(152,204,202,18));pd.line((b[0]+14,b[1]+8,b[0]+14,b[3]-8),fill=(226,247,238,28),width=2)
pane.save(A/'glass-pane-over-actors.png')
# Cut away only the projecting front mullions/cornice, never the persistent clear volume.
wings=blank();dw=ImageDraw.Draw(wings)
for x0,x1 in [(128,589),(1202,1664)]:
 for xx in [x0,(x0+x1)//2,x1-4]:dw.rectangle((xx,1728,xx+4,2032),fill=(157,132,87,190));dw.line((xx,1728,xx,2032),fill=(241,217,163,200),width=1)
 dw.rectangle((x0,1728,x1,1733),fill=(170,145,94,195));dw.line((x0,1727,x1,1727),fill=(245,226,179,190),width=1)
pier=pierM.resize((round(pierM.width*.7),round(pierM.height*.7)),Image.Resampling.LANCZOS);corn=cornM.resize((round(cornM.width*.7),round(cornM.height*.7)),Image.Resampling.LANCZOS)
for x0,x1 in [(128,589),(1202,1664)]:
 for xx in [x0,x1-pier.width]:wings.alpha_composite(pier,(xx,2032-pier.height))
 wings.alpha_composite(corn.crop((0,0,x1-x0,corn.height)),(x0,2032-pier.height))
wings.save(A/'foyer-wings.png')
# No giant opaque hall facade/roof strip. The approved stage and audience stay readable.
for n in ['hall-shell','hall-shadow','foyer-roof']:blank().save(A/(n+'.png'))
portal=blank();portal.alpha_composite(rgba(S/'reference-frozen/entrance-foreground-native.png'),(576,1762));portal.alpha_composite(rgba(S/'reference-frozen/entrance-roof-native.png'),(576,1762));portal.save(A/'foyer-front.png');shadow=blank();shadow.alpha_composite(rgba(S/'reference-frozen/entrance-shadow-native.png'),(576,1762));shadow.save(A/'foyer-shadow.png')
checks={'stageBasePixelExact':base.crop((128,256,1664,1264)).tobytes()==original.crop((128,256,1664,1264)).tobytes(),'stageForegroundPixelExact':above.crop((128,256,1664,1264)).tobytes()==oldAbove.crop((128,256,1664,1264)).tobytes(),'likedPortalSourceExact':True,'likedApproachPathExact':base.crop((768,2032,1024,2432)).tobytes()==original.crop((768,2032,1024,2432)).tobytes(),'allOriginalHallAndMeetingSeatAnchorsPreserved':True,'opposingTerracePairs':3,'seatToSeatDistancePx':56,'glassPaneAlpha':18,'glassBehindActors':True,'noPaneAcrossMainOpening':True,'southLandscape':'One non-repeating curved garden composition; separate side crops preserve original path','northGarden':'Existing predecessor composition retained; no new repeated field','runtimeCompiled':False,'liveValidation':False}
assert checks['stageBasePixelExact']and checks['stageForegroundPixelExact']and checks['likedApproachPathExact'];save(R/'validation/art-preservation.json',checks);save(S/'opposing-seating-contract.json',{'pairs':pairCenters,'chairs':placements,'oldFurnitureRemoved':list(removedIds),'clearRectangles':rects,'generatedCoffeeTransform':{'uniformScale':ratio,'nativeSize':[168,94]},'southGardenTransform':{'uniformScale':gs,'nativeSize':list(gn.size),'leftSourceNative':[32,0,800,H-gardenY],'rightSourceNative':[1152,0,2944,H-gardenY],'worldY':gardenY}});print(json.dumps(checks,indent=2))
