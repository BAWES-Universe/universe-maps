from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter
import numpy as np
import hashlib,json,math
R=Path(__file__).resolve().parents[1]
A=Path('/workspace/shared/grand-auditorium-07-clean')
WORLD=(2816,2432);SHIFT=(128,256);ORIGIN=(576,1762);SIZE=(640,320)
MASTER=R/'masters/entrance-generated-master-01.png'
# Translation only for accepted A. No accepted asset is resized or retouched.
base=Image.open(A/'assets/runtime-base.png').convert('RGBA')
above=Image.open(A/'assets/runtime-above.png').convert('RGBA')
reference=Image.open(A/'assets/greg-reference.png').convert('RGBA')
master=Image.open(MASTER).convert('RGBA')
crop=master.crop((0,104,1536,872));crop.save(R/'masters/entrance-proportional-crop.png')
# Remove generated diffuse nonstructural alpha halo. This changes alpha only;
# the stored master is intact. Pixels alpha>=128 retain original RGB and alpha.
a=np.array(crop);alpha=a[:,:,3];solid=alpha>=128
# Generated isolated alpha specks do not belong to the connected facade.
from scipy.ndimage import label
labs,n=label(solid);counts=np.bincount(labs.ravel());counts[0]=0;structure=labs==int(counts.argmax())
a[:,:,3]=np.where(structure,alpha,0)
clean=Image.fromarray(a);clean.save(R/'masters/entrance-structural-alpha-crop.png')
native=clean.resize(SIZE,Image.Resampling.LANCZOS)
native.save(R/'assets/entrance-complete-native.png')
# The generated floor inside the portal belongs to the revealable frontage.
# It is NOT a permanent new floor patch over A's foyer.
na=np.array(native); yy,xx=np.indices((SIZE[1],SIZE[0]));vis=na[:,:,3]>0
base_mask=(yy>=266)&(yy<270)&(xx>=256)&(xx<384)&vis
# Roof/pediment/eave share one reveal channel. Exact integer partition ensures
# no doubled-alpha seams between roof and wall.
roof_mask=(((xx>=183)&(xx<458)&(yy<144))|((yy<103)&~((xx>=183)&(xx<458))))&vis&~base_mask
front_mask=vis&~base_mask&~roof_mask
parts={}
for name,m in [('base',base_mask),('foreground',front_mask),('roof',roof_mask)]:
 out=na.copy();out[:,:,3]=np.where(m,na[:,:,3],0);parts[name]=Image.fromarray(out)
 parts[name].save(R/'assets'/f'entrance-{name}-native.png')
 Image.fromarray(np.where(m,na[:,:,3],0).astype('uint8')).save(R/'masks'/f'entrance-{name}-alpha.png')
# A deliberately restrained ground contact shadow is generated from the
# actual native footprint, with only translation, attenuation and blur.
footprint_mask=(yy>=270)&~((xx>=256)&(xx<384))&vis
contact=Image.fromarray(np.where(footprint_mask,na[:,:,3],0).astype('uint8'))
shifted=Image.new('L',SIZE);shifted.paste(contact,(7,7));shifted=shifted.filter(ImageFilter.GaussianBlur(2.5)).point(lambda x:round(x*.24))
shadow=Image.new('RGBA',SIZE,(23,30,20,0));shadow.putalpha(shifted);parts['shadow']=shadow
shadow.save(R/'assets/entrance-shadow-native.png');shifted.save(R/'masks/entrance-shadow-alpha.png')
# Blank expansion is transparent. No new exterior paving is invented here.
bg=Image.new('RGBA',WORLD,(0,0,0,0));bg.alpha_composite(base,SHIFT)
bga=Image.new('RGBA',WORLD);bga.alpha_composite(above,SHIFT)
# Exact source layer copies at translated position are included as local
# prototype inputs, not runtime/TMJ assets.
bg.save(R/'assets/translated-A-base.png');bga.save(R/'assets/translated-A-above.png')
frames={name:reference.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32)) for name,i in [('north',10),('south',1),('east',7),('west',4)]}

def compose(revealed=False,actors=()):
 out=bg.copy()
 out.alpha_composite(parts['base'],ORIGIN)
 if not revealed:out.alpha_composite(parts['shadow'],ORIGIN)
 for x,y,face in actors:out.alpha_composite(frames[face],(x-16,y-16))
 out.alpha_composite(bga)
 if not revealed:
  out.alpha_composite(parts['foreground'],ORIGIN);out.alpha_composite(parts['roof'],ORIGIN)
 return out

BOX=(512,1728,1280,2176)
outside=compose(False,[(896,2144,'north')]);approach=compose(True,[(896,2112,'north')]);inside=compose(True,[(896,2016,'north'),(1176,1807,'south'),(1176,1856,'north')])
for name,im in [('outside-empty',compose(False)),('outside-occupied',outside),('approach-revealed',approach),('inside-revealed',inside)]:
 im.crop(BOX).save(R/'review'/f'{name}-native.png')
# The entrance module is directly compared with accepted artwork at exactly
# one image pixel per world pixel. Greg is always an original 32x32 frame.
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
card=Image.new('RGB',(1600,1110),'#123036');d=ImageDraw.Draw(card)
d.text((24,18),'C  /  SOUTH ENTRANCE PROTOTYPE • NATIVE 1:1',font=bold(24),fill='#f6dda6')
d.text((24,55),'New proportional facade. Same 32px Greg and unchanged A interior. Static source proof only.',font=font(18),fill='#c9dcd8')
for name,x,y,label in [('outside-occupied',24,124,'OUTSIDE • tall frontage / flush 128px route'),('approach-revealed',808,124,'APPROACH • reveal by center y=2112'),('inside-revealed',24,620,'INSIDE • foyer appears before head overlap')]:
 d.text((x,y-29),label,font=bold(16),fill='#edc878');card.paste(Image.open(R/'review'/f'{name}-native.png'),(x,y))
d.text((808,591),'ACCEPTED ART / SAME NATIVE SCALE',font=bold(16),fill='#edc878')
accepted=Image.open(A/'review/flagship-a-occupied-native.png').convert('RGBA')
for bb,pos in [((864,1440,1456,1712),(808,620)),((176,400,400,560),(808,916)),((624,256,992,400),(1052,916))]:card.paste(accepted.crop(bb),pos)
card.save(R/'review/entrance-native-review-sheet.png')
card.resize((3200,2220),Image.Resampling.NEAREST).save(R/'review/entrance-review-sheet-2x-nearest.png')
# Full context explicitly depicts just the south module; whole-building roof
# and long facade wings are intentionally not authored at this stage.
ctx=Image.new('RGB',(1728,1728),'#123036');d=ImageDraw.Draw(ctx)
d.text((28,22),'C  /  PROPORTIONAL SOUTH ENTRY IN A CONTEXT',font=bold(25),fill='#f6dda6')
d.text((28,62),'640px entrance module only; roof and full facade wings remain future work. Garden stays right.',font=font(18),fill='#c9dcd8')
# Uniform half-scale review overview. Artwork itself remains native.
context=outside.crop((128,256,2688,2176));context=context.resize((1280,960),Image.Resampling.LANCZOS)
ctx.paste(context,(224,112))
d.text((28,1106),'FOYER REVEAL DETAIL / 1:1 CROP',font=bold(20),fill='#edc878')
ctx.paste(inside.crop((544,1648,1504,2176)),(28,1148))
d.text((1016,1150),'REGISTRATION',font=bold(18),fill='#f6dda6')
lines=['A source → prototype: +128x, +256y','Interior dimensions and furniture stay exact.','','Portal: x832–960, y2032 threshold','Nominal clear width: 128px','32px-frame center corridor: x848–944','','Immediate hide on approach by y2112','South re-close proposal: y2144','41px safety incl. antialiased fringe','','Gray/teal empty border = unbuilt world','This is NOT a runtime screenshot.']
for i,line in enumerate(lines):d.text((1016,1186+i*29),line,font=font(17),fill='#c9dcd8')
ctx.save(R/'review/full-context-compositing-preview.png')
# Geometry illustration is separate from unmarked art acceptance images.
geom=outside.crop(BOX).convert('RGBA');gd=ImageDraw.Draw(geom)
def rect(b,fill,out):
 q=(b[0]-BOX[0],b[1]-BOX[1],b[2]-BOX[0],b[3]-BOX[1]);gd.rectangle(q,fill=fill,outline=out,width=2)
rect((832,1936,960,2176),(70,210,196,45),'#48d9c5')
gd.line((0,2112-BOX[1],768,2112-BOX[1]),fill='#8ce4b8',width=2)
gd.line((832-BOX[0],2032-BOX[1],960-BOX[0],2032-BOX[1]),fill='#fff1ae',width=3)
gd.text((14,2112-BOX[1]+6),'REVEAL BY y2112 / 80px before threshold',font=bold(15),fill='#fff1ae')
gd.text((328,2032-BOX[1]+6),'128px clear',font=bold(15),fill='#fff1ae')
geom.save(R/'review/entrance-registration-native.png')
# Numerical proof, not a claim of room/gameplay verification.
reveal_alpha=np.maximum(np.array(parts['foreground'])[:,:,3],np.array(parts['roof'])[:,:,3])
opaque=(reveal_alpha>=128)
ymax=int(np.where(opaque)[0].max())+ORIGIN[1]
# Across the full module, a 32px conservative frame at trigger has its top
# south of every opaque facade pixel. Instant removal then avoids fade risk.
trigger_y=2112;head_top=trigger_y-16;safety=head_top-(ymax+1)
all_alpha_max_y=int(np.where(reveal_alpha>0)[0].max())+ORIGIN[1]
all_alpha_safety=head_top-(all_alpha_max_y+1)
# Test all 32px frame rectangles inside the clear route after reveal, against
# architecture remaining ABOVE actors. The flush threshold is rendered below
# actors and does not represent collision or occlusion. No new above art remains.
base_alpha=np.zeros((SIZE[1],SIZE[0]),dtype='uint8');route_hits=[]
for cx in range(848,945,8):
 for cy in range(1968,2177,8):
  l=max(0,cx-16-ORIGIN[0]);r=min(SIZE[0],cx+16-ORIGIN[0]);t=max(0,cy-16-ORIGIN[1]);b=min(SIZE[1],cy+16-ORIGIN[1])
  if l<r and t<b and (base_alpha[t:b,l:r]>=128).any():route_hits.append([cx,cy])
# Before any architecture overlay the accepted A crop must be identical.
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
translated_equal=ImageChops.difference(bg.crop((128,256,2688,2176)),base).getbbox() is None
above_equal=ImageChops.difference(bga.crop((128,256,2688,2176)),above).getbbox() is None
# Alpha partition equality checks exact reconstruction after masks.
rebuild=Image.new('RGBA',SIZE)
for key in ['base','foreground','roof']:rebuild.alpha_composite(parts[key])
partition_diff=ImageChops.difference(rebuild,native).getbbox()
manifest={
 'status':'Bounded native entrance art prototype; no runtime build or publication',
 'generator':'built-in image_gen; new raster master, not v06 raster reuse',
 'sourceMaster':str(MASTER.relative_to(R)), 'sourceMasterPixels':list(master.size),
 'cropXYXY':[0,104,1536,872], 'croppedMasterPixels':[1536,768], 'nativePixels':list(SIZE),
 'scaleX':'5/12','scaleY':'5/12','anisotropicScaling':False,
 'resample':'Pillow LANCZOS one time from cropped master',
 'structuralAlphaExtraction':'Largest 4-connected alpha>=128 component; master unmodified; RGB preserved before uniform reduction',
 'translationXY':list(SHIFT),'prototypeWorldPixels':list(WORLD),'moduleOriginXY':list(ORIGIN),
 'thresholdY':2032,'clearRouteXYXY':[832,1936,960,2224],'clearRouteWidth':128,
 'safe32FrameCenterX':[848,944],
 'existingArrivalOpeningTranslated':[768,1968,1024,2032],
 'doorClearWidthMeasuredApproximately':140,'doorHeightApproximately':125,
 'facadeWallRiseApproximately':184,'facadeFinialRiseApproximately':252,
 'unchangedHallFoyerBodySource':[0,0,1536,1728],'preservedArrivalOpeningExtendsToSourceY':1776,
 'noteAbout1728':'User approximate 1536×1728 reference: A exact southern opening ends y1776; no contraction was used.',
 'existingApproachWidth':256,
 'proposedLandingXYXY':[704,2032,1088,2224],
 'landingStatus':'Wider 384×192 landing is coordinate proposal only; previews retain A exterior paving.',
 'revealProposal':{'entryRectXYXY':[512,1696,1280,2112],'hide':'instant opacity 0 for foreground and roof, before entering from south','recloseSouthY':2144,'headFramePixels':[32,32],'opaqueForegroundMaxY':ymax,'allAlphaForegroundMaxY':all_alpha_max_y,'frameTopAtTrigger':head_top,'opaqueSafetyPixels':safety,'allAlphaSafetyPixels':all_alpha_safety,'collision':'A grid is the unchanged source proposal; facade is visual only and never drives or toggles collision. Full 256px approach remains; 128px is the facade clear portal, not a new invisible collision throat.'},
 'layerPolicy':{'base':'4px-deep flush threshold strip, below actors; all structural jambs/plinths hide to expose exact A low-wall footprint','foreground':'Tall walls, jambs, doors, and temporary portal interior; all hide together','roof':'Local entrance pediment/eave only; hides together with foreground','shadow':'Native footprint contact shadow, restrained 7px offset; hides with facade; no architecture-shaped giant floor shadow'},
 'preservedSources':{str(p.relative_to(A)):sha(p)for p in [A/'assets/runtime-base.png',A/'assets/runtime-above.png',A/'assets/greg-reference.png',A/'source/collision-grid.json']},
 'sourceTranslationPixelExact':translated_equal and above_equal,'layerPartitionPixelExact':partition_diff is None,
 'revealed32FrameRouteOpaqueForegroundHits':route_hits,
 'proofLimitation':'Static image and source geometry only. Not authenticated gameplay, camera, pathfinding, audio, collision or engine acceptance.',
 'notPerformed':['TMJ/runtime compile','WAM edit','audio configuration','engine edits','GitHub or Library publication','whole-building roof generation','side-entry asset generation']}
(R/'proportional-scale-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'validation/source-proof.json').write_text(json.dumps({'translatedABasePixelExact':translated_equal,'translatedAAbovePixelExact':above_equal,'architectureMaskPartitionPixelExact':partition_diff is None,'opaqueFacadeMaximumY':ymax,'opaqueHeadClearanceAtRevealPixels':safety,'allAlphaHeadClearanceAtRevealPixels':all_alpha_safety,'revealed128pxRouteHasZeroNewOpaqueForegroundIntersections':not route_hits,'checkedConservative32pxFramePositions':len(range(848,945,8))*len(range(1968,2177,8)),'runtimeVerified':False},indent=2)+'\n')
print(json.dumps({'module':SIZE,'origin':ORIGIN,'safeMarginAllAlpha':all_alpha_safety,'routeHits':len(route_hits),'sourcePreserved':translated_equal and above_equal,'partitionExact':partition_diff is None},indent=2))
