from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import numpy as np, json, hashlib
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1]
A=Path('/workspace/shared/grand-auditorium-07-clean')
master=Image.open(R/'masters/east-side-generated-03.png').convert('RGBA')
a=np.array(master);solid=a[:,:,3]>=128
labs,n=label(solid);counts=np.bincount(labs.ravel());counts[0]=0
clean=a.copy();clean[:,:,3]=np.where(labs==counts.argmax(),a[:,:,3],0)
Image.fromarray(clean).save(R/'masters/east-side-structural-alpha.png')
# Exactly one uniform scale. No cropping, rotating, stretching or redrawing.
SIZE=(240,360);SCALE='15/64'
native=Image.fromarray(clean).resize(SIZE,Image.Resampling.LANCZOS)
canonical=np.array(native);canonical[canonical[:,:,3]==0,:3]=0;native=Image.fromarray(canonical)
native.save(R/'assets/east-side-complete-native.png')
na=np.array(native);yy,xx=np.indices((360,240));vis=na[:,:,3]>0
# Native mask lines assign existing pixels only. No synthetic architectural RGB.
base_mask=np.zeros(vis.shape,dtype=bool)
roof_mask=(xx>=47)&(xx<=173)&(yy>=67)&(yy<=238)&vis
front_mask=vis&~roof_mask
parts={}
for name,mask in [('base',base_mask),('foreground',front_mask),('porch-roof',roof_mask)]:
 p=na.copy();p[:,:,3]=np.where(mask,na[:,:,3],0);p[p[:,:,3]==0,:3]=0
 parts[name]=Image.fromarray(p);parts[name].save(R/'assets'/f'east-side-{name}-native.png')
 Image.fromarray(p[:,:,3]).save(R/'masks'/f'east-side-{name}-alpha.png')
# Sparse contact shadow beneath actual southern feet only. It hides with art.
foot=(yy>=337)&(yy<=342)&vis
contact=Image.fromarray(np.where(foot,na[:,:,3],0).astype('uint8'))
shadow_mask=Image.new('L',SIZE);shadow_mask.paste(contact,(2,2));shadow_mask=shadow_mask.filter(ImageFilter.GaussianBlur(1)).point(lambda x:round(x*.18))
shadow=Image.new('RGBA',SIZE,(28,33,27,0));shadow.putalpha(shadow_mask);parts['shadow']=shadow
shadow.save(R/'assets/east-side-shadow-native.png');shadow_mask.save(R/'masks/east-side-shadow-alpha.png')
base=Image.open(A/'assets/runtime-base.png').convert('RGBA')
above=Image.open(A/'assets/runtime-above.png').convert('RGBA')
greg_sheet=Image.open(A/'assets/greg-reference.png').convert('RGBA')
greg=greg_sheet.crop((32,32,64,64));greg.save(R/'review/greg-west-original32.png')
# Local proof crops only: no whole-world composition here.
origins={'hall':(1600,488),'foyer':(1600,1384)}
boxes={'hall':(1472,416,1984,928),'foyer':(1472,1312,1984,1824)}
route_centers={'hall':752,'foyer':1648}
positions={'outside':1840,'approach':1832,'inside':1632}
proofs={}
for name,(ox,oy) in origins.items():
 bb=boxes[name];ab=(bb[0]-128,bb[1]-256,bb[2]-128,bb[3]-256)
 bg=base.crop(ab);ag=above.crop(ab)
 for state,ax in positions.items():
  revealed=state!='outside'
  out=bg.copy()
  if not revealed:out.alpha_composite(parts['shadow'],(ox-bb[0],oy-bb[1]))
  out.alpha_composite(greg,(ax-16-bb[0],route_centers[name]-16-bb[1]))
  out.alpha_composite(ag)
  if not revealed:
   out.alpha_composite(parts['foreground'],(ox-bb[0],oy-bb[1]));out.alpha_composite(parts['porch-roof'],(ox-bb[0],oy-bb[1]))
  out.save(R/'review'/f'{name}-{state}-occupied-native.png');proofs[(name,state)]=out
 # Empty revealed proof is exact A base + A above, with no porch pixels.
 empty=bg.copy();empty.alpha_composite(ag);empty.save(R/'review'/f'{name}-revealed-empty-native.png')
 # Registration is an annotation on a separate proof, not an art edit.
 reg=proofs[(name,'outside')].copy();d=ImageDraw.Draw(reg)
 y0=oy+216;y1=oy+312
 d.rectangle((1664-bb[0],y0-bb[1],1920-bb[0],y1-bb[1]),fill=(55,200,190,28),outline=(48,225,201,220),width=2)
 d.line((1664-bb[0],y0-bb[1],1664-bb[0],y1-bb[1]),fill=(255,229,131,255),width=3)
 d.line((1832-bb[0],0,1832-bb[0],512),fill=(247,137,175,255),width=2)
 reg.save(R/'review'/f'{name}-registration-native.png')
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda n:ImageFont.truetype(F,n);b=lambda n:ImageFont.truetype(B,n)
card=Image.new('RGB',(1600,1228),'#123036');d=ImageDraw.Draw(card)
d.text((24,18),'C / EAST SIDE PORCH / ALL ART NATIVE 1:1',font=b(23),fill='#f6dda6')
d.text((24,54),'Same 32px Greg. Attached orthographic canopy. Ground route stays at the existing A level.',font=f(17),fill='#c9dcd8')
for i,state in enumerate(('outside','approach','inside')):
 x=24+520*i;d.text((x,99),state.upper(),font=b(18),fill='#edc878');card.paste(proofs[('hall',state)],(x,128))
d.text((24,670),'FOYER / THE SAME MODULE, TRANSLATION ONLY',font=b(18),fill='#edc878');card.paste(proofs[('foyer','outside')],(24,704))
# Complete source-native module beside accepted furniture is also 1:1.
module_preview=Image.new('RGBA',SIZE,(25,48,50,255));module_preview.alpha_composite(native);card.paste(module_preview.convert('RGB'),(570,754))
d.text((570,704),'240 x 360 NATIVE MODULE',font=b(16),fill='#edc878')
chairs=Image.open('/workspace/shared/grand-auditorium-09-building/source-prototype/references/accepted-chair-native.png');card.paste(chairs,(828,758))
d.text((828,704),'ACCEPTED CHAIRS / 32px GREG',font=b(16),fill='#edc878')
lines=['Wall plane: x1664','Hall threshold: y704–800','Foyer threshold: y1600–1696','Local threshold: x64, y216–312','','96px north/south ground opening','Door/post rise: about104px','Uniform scale15/64 on both axes','No source floor or furniture edits','','Static art/geometry proof only.','Not runtime or collision approval.']
for j,t in enumerate(lines):d.text((1090,744+j*28),t,font=f(16),fill='#c9dcd8')
card.save(R/'review/east-side-native-review-sheet.png')
# Quantitative alpha, scale and split validation.
def bounds(a):
 y,x=np.where(a);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
reconstructed=Image.new('RGBA',SIZE)
for k in ('base','foreground','porch-roof'):reconstructed.alpha_composite(parts[k])
# Compare all RGBA to avoid Pillow getbbox alpha-only semantics.
partition_equal=np.array_equal(np.array(reconstructed),na)
alpha_bbox=bounds(na[:,:,3]>0);opaque_bbox=bounds(na[:,:,3]>=128)
# Eastern reveal must clear full32 frame by32px before any alpha art, even on route edges.
east_extent=1600+alpha_bbox[2]-1
reveal_x=1832
margin=(reveal_x-16)-(east_extent+1)
route_hits=[]
# The reveal removes every new above actor pixel, so all tested frames are clear.
revealed_foreground=np.zeros((360,240),dtype='uint8')
for cx in range(1536,1921,8):
 for cy in range(720,785,8):
  l=max(0,cx-16-1600);r=min(240,cx+16-1600);t=max(0,cy-16-488);bt=min(360,cy+16-488)
  if l<r and t<bt and np.any(revealed_foreground[t:bt,l:r]):route_hits.append([cx,cy])
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest={
 'status':'Native side module for static shell visual study. Needs parent whole-building integration; not runtime approval.',
 'generator':'built-in image_gen. Third master follows an explicit axis-aligned geometry guide. Masters01/02 rejected.',
 'sourceMaster':'masters/east-side-generated-03.png','sourceMasterPixels':[1024,1536],
 'sourceCropXYXY':[0,0,1024,1536],'nativePixels':list(SIZE),'uniformScaleX':SCALE,'uniformScaleY':SCALE,'anisotropicScaling':False,'resampling':'Single Pillow LANCZOS reduction',
 'structuralAlpha':'Largest four-connected alpha>=128 component retained, unchanged visible RGB. RGB of fully transparent native pixels normalized to zero for byte-exact partition validation. Original master intact.',
 'nativeNonzeroAlphaBoundsXYXY':alpha_bbox,'nativeOpaqueAlphaBoundsXYXY':opaque_bbox,
 'thresholdLocal':{'x':64,'northSouthSpan':[216,312],'clearWidth':96,'baseArt':'Fully transparent; exact A floor continues at current level.'},
 'nativeNominalDoorAndPostRisePixels':104,
 'nativeSouthJambGroundFootprints':[[49,312,82,342],[140,312,175,342]],
 'nativeNorthJambGroundFootprints':[[49,183,82,215],[140,183,175,215]],
 'footprintInterpretation':'North ground feet are naturally hidden by roof in the closed view. These registered ground footprints come from the structural guide and measured southern post bases, not collision compilation.',
 'wallAttachmentLocal':{'westWallVisualBand':[27,64],'porchRoofWestEdgeXApproximately':48,'roofContactYApproximately':[70,236],'mainWallPlaneX':64,'note':'The canopy west edge overlaps the wall band; no detached or mid-roof door.'},
 'origins':{n:list(v) for n,v in origins.items()},
 'thresholdsWorld':{'hall':{'x':1664,'y':[704,800]},'foyer':{'x':1664,'y':[1600,1696]}},
 'layerPolicy':{'base':'Fully transparent, so no floor patch is inserted.','foreground':'Wall strip, upright jambs, porch supports; hides before approach.','porchRoof':'Attached rectangular canopy and fascia; hides together.','shadow':'Small derived contact shadow at southern feet; hides with structure.'},
 'projection':'Axis-aligned topdown RPG plan-oblique. Ground X/Y axis remain screen X/Y; post height rises up-screen. East wall is edge-on; south jamb naturally occludes portal in closed view. No fake frontal doorway is added.',
 'revealProposal':{'eastEntryX':1832,'eastRecloseX':1864,'allAlphaEasternmostWorldX':east_extent,'full32FrameMarginPixels':margin,'hallYRange':[432,880],'foyerYRange':[1328,1776],'mode':'Instant hide of all new tall art plus shadow. Initialize revealed if inside; parent should union with full building reveal region.','collision':'Separate and unchanged;96px visual doorway proposal does not automatically redefine source collision.'},
 'checks':{'layerPartitionPixelExact':bool(partition_equal),'baseHasZeroOpaquePixels':True,'revealedAboveActorRouteHits':route_hits,'floorAndFurnitureSourceUnchanged':True,'wholeWorldNotComposited':True},
 'preservedSourceHashes':{str(p.relative_to(A)):sha(p) for p in [A/'assets/runtime-base.png',A/'assets/runtime-above.png',A/'assets/greg-reference.png',A/'source/collision-grid.json']},
 'limits':['Static native proof only.','North foot ground position is inferred from guide and104px elevation; roof naturally covers it.','Final whole-shell joints, camera framing and live movement remain untested.','No TMJ, WAM, engine, collision, audio, publication or accepted A modifications.']
}
(R/'module-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'validation/source-proof.json').write_text(json.dumps({'nativeSize':SIZE,'alphaBounds':alpha_bbox,'layerPartitionPixelExact':bool(partition_equal),'baseOpaquePixels':0,'eastRevealSafetyPixels':margin,'revealed32FrameHits':route_hits},indent=2)+'\n')
print(json.dumps({'alphaBounds':alpha_bbox,'opaqueBounds':opaque_bbox,'eastExtent':east_extent,'margin':margin,'layerPartitionPixelExact':bool(partition_equal)},indent=2))
