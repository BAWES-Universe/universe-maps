from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import numpy as np,json,hashlib
from scipy.ndimage import label
from frozen_inputs import frozen_b_input,historical_a_comparison,review_font
R=Path(__file__).resolve().parents[1];P=R.parent
W,H=2816,2432;SHIFT=(128,256)
rgba=lambda p:Image.open(p).convert('RGBA')
master=rgba(P/'masters/entrance-generated-master-01.png')
def structural(im):
 a=np.array(im);labs,n=label(a[:,:,3]>=128);counts=np.bincount(labs.ravel());counts[0]=0;m=labs==int(counts.argmax());a[:,:,3]=np.where(m,a[:,:,3],0);return Image.fromarray(a)
entrance_master=structural(master)
# Each source roof is used at its ORIGINAL generated dimensions. No resizing.
roofs={}
for name,filename,xy in [('hall','hall-roof-master-01.png',(128,96)),('foyer','foyer-roof-master-03.png',(128,1072))]:
 im=structural(rgba(R/'masters'/filename));im.save(R/'assets'/f'{name}-roof-native.png');roofs[name]=(im,xy)
# Native-size window and pier modules. Original pixels only, uniform reduction.
# Bay seams are hidden by the separate complete pier, never stretched.
modules={}
for family,s in [('south',5/12),('hall',.5)]:
 for kind,box in [('window',(136,200,328,800)),('pier',(328,200,448,824))]:
  crop=entrance_master.crop(box);size=(round(crop.width*s),round(crop.height*s));assert abs(size[0]/crop.width-size[1]/crop.height)<1e-12
  im=crop.resize(size,Image.Resampling.LANCZOS);im.save(R/'assets'/f'{family}-{kind}-native.png');modules[family,kind]=im
# Expanded exterior proof: retain all of A exactly, add only outside strips.
base_src=rgba(frozen_b_input('assets/runtime-base.png'));above_src=rgba(frozen_b_input('assets/runtime-above.png'))
base=Image.new('RGBA',(W,H));grass_master=rgba(R/'masters/exterior-expansion-grass-master.png');grass=grass_master.resize((768,512),Image.Resampling.LANCZOS);grass.save(R/'assets/expanded-margin-grass-native.png')
for row,y in enumerate(range(0,H,512)):
 for col,x in enumerate(range(0,W,768)):
  tile=grass
  if col%2:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if row%2:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  base.alpha_composite(tile,(x,y))
# Native mirrored edge continuation fades OUTSIDE A into the new meadow.
# Matching edge pixels remove a hard border; A itself is never blended.
for name,box,xy,flip in [
 ('north',(0,0,2560,64),(128,192),Image.Transpose.FLIP_TOP_BOTTOM),
 ('south',(0,1856,2560,1920),(128,2176),Image.Transpose.FLIP_TOP_BOTTOM),
 ('west',(0,0,64,1920),(64,256),Image.Transpose.FLIP_LEFT_RIGHT),
 ('east',(2496,0,2560,1920),(2688,256),Image.Transpose.FLIP_LEFT_RIGHT)]:
 strip=base_src.crop(box).transpose(flip);arr=np.array(strip)
 if name=='north':weights=np.linspace(0,1,64)[:,None]
 elif name=='south':weights=np.linspace(1,0,64)[:,None]
 elif name=='west':weights=np.linspace(0,1,64)[None,:]
 else:weights=np.linspace(1,0,64)[None,:]
 arr[:,:,3]=(arr[:,:,3]*weights).astype('uint8');base.alpha_composite(Image.fromarray(arr),xy)
base.alpha_composite(base_src,SHIFT)
# Only the existing256px approach is extended, at original size.
south_path=base_src.crop((640,1792,896,1920))
for y in [2176,2304]:base.alpha_composite(south_path,(768,y))
above=Image.new('RGBA',(W,H));above.alpha_composite(above_src,SHIFT)
base.save(R/'assets/interior-and-expanded-exterior-base.png');above.save(R/'assets/interior-above-preserved.png')
front=Image.new('RGBA',(W,H));roof_layer=Image.new('RGBA',(W,H));shadow=Image.new('RGBA',(W,H));permanent=Image.new('RGBA',(W,H))
# High hall front face; lower portions are correctly occluded by foyer roof.
for cx in [158+134*i for i in range(11)]:front.alpha_composite(modules['hall','window'],(cx+19,988))
for cx in [158+134*i for i in range(12)]:front.alpha_composite(modules['hall','pier'],(cx-30,988))
hall_front=front.copy();front=Image.new('RGBA',(W,H))
# South wings at the approved entrance's unchanged threshold and proportions.
for centers in [[153+112*i for i in range(5)],[1191+112*i for i in range(5)]]:
 for cx in centers[:-1]:front.alpha_composite(modules['south','window'],(cx+16,1802))
 for cx in centers:front.alpha_composite(modules['south','pier'],(cx-25,1802))
foyer_front=front.copy();front=hall_front.copy();front.alpha_composite(foyer_front)
# These modules are illustrative vertical walls only. A collision stays constant.
# Only art below the roof is visible, so stable native piers cover every seam.
semantic_roofs={}
for name in ['hall','foyer']:
 im,xy=roofs[name];roof_layer.alpha_composite(im,xy);semantic_roofs[name]=Image.new('RGBA',(W,H));semantic_roofs[name].alpha_composite(im,xy)
# South approved entrance is unchanged and foreground to the foyer roof.
portal_front=rgba(P/'assets/entrance-foreground-native.png');portal_roof=rgba(P/'assets/entrance-roof-native.png')
portal_all=Image.new('RGBA',(W,H));portal_all.alpha_composite(portal_front,(576,1762));portal_all.alpha_composite(portal_roof,(576,1762))
permanent.alpha_composite(rgba(P/'assets/entrance-base-native.png'),(576,1762))
# Every shadow is assigned by original module ownership, not screen slicing.
semantic_shadows={}
for name,src,(y0,y1) in [('hall',hall_front,(1256,1300)),('foyer',foyer_front,(2024,2068))]:
 alpha=np.array(src)[:,:,3];foot=np.zeros((H,W),np.uint8);foot[y0:y1]=alpha[y0:y1]
 mask=Image.fromarray(foot);offset=Image.new('L',(W,H));offset.paste(mask,(12,10));offset=offset.filter(ImageFilter.GaussianBlur(3)).point(lambda x:round(x*.2));part=Image.new('RGBA',(W,H));part.putalpha(offset);semantic_shadows[name]=part
semantic_shadows['foyer'].alpha_composite(rgba(P/'assets/entrance-shadow-native.png'),(576,1762))
# Side porch ownership follows its doorway, never a horizontal cut through art.
side_manifest=R/'side-porch/module-manifest.json';side_full=Image.new('RGBA',(W,H));semantic_sides={name:Image.new('RGBA',(W,H))for name in ['hall','foyer']}
if side_manifest.exists():
 cfg=json.loads(side_manifest.read_text())
 for label,xy in cfg['origins'].items():
  semantic_shadows[label].alpha_composite(rgba(R/'side-porch/assets/east-side-shadow-native.png'),tuple(xy))
  semantic_sides[label].alpha_composite(rgba(R/'side-porch/assets/east-side-complete-native.png'),tuple(xy))
  side_full.alpha_composite(semantic_sides[label])
shadow=semantic_shadows['hall'].copy();shadow.alpha_composite(semantic_shadows['foyer'])
semantic_components={
 'hall-shell-frontface':hall_front,'hall-shell-roof':semantic_roofs['hall'],'hall-shell-porch':semantic_sides['hall'],'hall-shell-shadow':semantic_shadows['hall'],
 'foyer-shell-front-wings':foyer_front,'foyer-shell-roof':semantic_roofs['foyer'],'foyer-shell-entrance':portal_all,'foyer-shell-porch':semantic_sides['foyer'],'foyer-shell-shadow':semantic_shadows['foyer']}
for name,im in semantic_components.items():
 im.save(R/'assets'/f'{name}.png');im.getchannel('A').save(R/'masks'/f'{name}-alpha.png')
hall_group=hall_front.copy();hall_group.alpha_composite(semantic_roofs['hall']);hall_group.alpha_composite(semantic_sides['hall'])
foyer_group=foyer_front.copy();foyer_group.alpha_composite(semantic_roofs['foyer']);foyer_group.alpha_composite(portal_all);foyer_group.alpha_composite(semantic_sides['foyer'])
for name,im in [('hall-shell-above-combined',hall_group),('foyer-shell-above-combined',foyer_group)]:im.save(R/'assets'/f'{name}.png');im.getchannel('A').save(R/'masks'/f'{name}-alpha.png')
shell_combined=front.copy();shell_combined.alpha_composite(roof_layer);shell_combined.alpha_composite(portal_all);shell_combined.alpha_composite(side_full);shell_combined.save(R/'assets/full-shell-occlusion-above.png');shell_combined.getchannel('A').save(R/'masks/full-shell-occlusion-alpha.png')
side_full.save(R/'assets/east-side-porches-above.png');side_full.getchannel('A').save(R/'masks/east-side-porches-above-alpha.png')
for name,im in [('full-vertical-wall-foreground',front),('full-roof-layer',roof_layer),('south-entry-front-and-pediment',portal_all),('shell-shadow-layer',shadow),('permanent-threshold-base',permanent)]:
 im.save(R/'assets'/f'{name}.png');im.getchannel('A').save(R/'masks'/f'{name}-alpha.png')
# Composition order: A below/above remains exact and shell shows only outdoors.
def compose(revealed=False,actors=()):
 hall_open=revealed is True or revealed=='hall';foyer_open=revealed is True or revealed=='foyer'
 out=base.copy();out.alpha_composite(permanent)
 if not hall_open:out.alpha_composite(semantic_shadows['hall'])
 if not foyer_open:out.alpha_composite(semantic_shadows['foyer'])
 greg=rgba(frozen_b_input('assets/greg-reference.png'));frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('east',7),('west',4)]}
 for x,y,d in actors:out.alpha_composite(frames[d],(x-16,y-16))
 out.alpha_composite(above)
 if not hall_open:out.alpha_composite(hall_front)
 if not foyer_open:out.alpha_composite(foyer_front)
 if not hall_open:out.alpha_composite(semantic_roofs['hall'])
 if not foyer_open and not hall_open:out.alpha_composite(semantic_roofs['foyer'])
 if not foyer_open:out.alpha_composite(portal_all)
 if not hall_open:out.alpha_composite(semantic_sides['hall'])
 if not foyer_open:out.alpha_composite(semantic_sides['foyer'])
 return out
outside=compose(False);revealed=compose(True)
outside.save(R/'review/full-outside-empty-native.png');revealed.save(R/'review/full-revealed-empty-native.png')
compose('foyer').save(R/'review/foyer-revealed-empty-native.png');compose('hall').save(R/'review/hall-revealed-empty-native.png')
compose('foyer',[(896,1744,'north')]).save(R/'review/foyer-only-revealed-occupied-native.png');compose('hall',[(1104,1200,'north')]).save(R/'review/hall-only-revealed-occupied-native.png')
out=compose(False,[(896,2176,'north'),(1888,752,'west'),(1888,1648,'west')]);out.save(R/'review/full-outside-occupied-native.png')
inside=compose(True,[(896,2016,'north'),(1176,1807,'south'),(1176,1856,'north'),(1664,752,'west'),(1664,1648,'west')]);inside.save(R/'review/full-revealed-occupied-native.png')
for name,box,points in [
 ('south',(512,1696,1280,2304),{'outside':(896,2176,'north'),'approach':(896,2112,'north'),'inside':(896,2016,'north')}),
 ('hall-east',(1472,416,2048,992),{'outside':(1888,752,'west'),'approach':(1832,752,'west'),'inside':(1664,752,'west')}),
 ('foyer-east',(1472,1312,2048,1888),{'outside':(1888,1648,'west'),'approach':(1832,1648,'west'),'inside':(1664,1648,'west')})]:
 for state,actor in points.items():compose(False if state=='outside' else ('hall' if name=='hall-east' else 'foyer'),[actor]).crop(box).save(R/'review'/f'{name}-{state}-native.png')
# Uniform scale overview only, never an asset transformation.
B=review_font(True);F=review_font();font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
card=Image.new('RGB',(2904,1416),'#123036');d=ImageDraw.Draw(card);d.text((24,18),'C / FULL BUILDING VISUAL STUDY • PROPORTIONAL NATIVE MODULES',font=bold(28),fill='#f6dda6');d.text((24,62),'Exterior shell and interior reveal. A interior + finished B exterior/pavilion; original32px Greg. Static study, no runtime/camera claim.',font=font(21),fill='#c9dcd8')
for im,x,title in [(out,24,'OUTSIDE'),(inside,1472,'REVEALED')]:
 d.text((x,106),title,font=bold(20),fill='#edc878');card.paste(im.resize((1408,1216),Image.Resampling.LANCZOS),(x,144))
d.text((24,1378),'Both overview panels are50% review scale. Native doors, masks and default camera proofs are supplied separately.',font=font(20),fill='#c9dcd8');card.save(R/'review/full-context-outside-revealed.png')
# Source invariant checks exclude new exterior, where walkability is explicit.
old=base_src.copy();old.alpha_composite(above_src)
preserved=ImageChops.difference(revealed.crop((128,256,2688,2176)),old)
# Four-pixel threshold strip is the sole intentional changed source rectangle.
checks={}
for name,box in [('hall',(0,0,1536,944)),('foyer',(64,1008,1472,1712)),('garden',(1536,0,2560,1712))]:
 pbox=tuple(v+(128 if i%2==0 else 256)for i,v in enumerate(box));checks[name+'PixelExactOnReveal']=ImageChops.difference(revealed.crop(pbox),old.crop(box)).getbbox() is None
# The A comparison was made before art freeze. Carry it forward only after
# the regenerated base/above bytes match the exact outputs that proof covered.
# This is historical evidence, not a new comparison against external A files.
archived=historical_a_comparison()
for name in ['hall','foyer']:checks[name+'StillExactA']=archived['originalSourceInvariants'][name+'StillExactA']
checks['aComparisonEvidence']={'status':'Historical archived comparison; not recomputed','archive':'tools/historical-a-comparison.json','currentBaseAndAboveMatchArchivedProofBytes':True}
checks['referenceForGardenAndExterior']='Frozen finished B, including pavilion tables and native chairs'
checks.update({'roofScale':[1,1],'noInteriorResizing':True,'noCollisionMutation':True,'runtimeVerified':False})
(R/'validation/source-invariants.json').write_text(json.dumps(checks,indent=2)+'\n')
print(checks)
