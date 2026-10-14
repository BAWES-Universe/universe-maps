from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'source-assets';O=R/'working';O.mkdir(exist_ok=True)
base=Image.open(S/'validated-interior-native.png').convert('RGBA')
new=Image.open(S/'generated-grid-paving-repair.png').convert('RGBA').resize((768,800),Image.Resampling.LANCZOS)
im=Image.new('RGBA',(768,832));im.paste(new,(0,32));im.paste(base,(0,0));original_garden=im.copy()
plate=Image.open(S/'generated-empty-court.png').convert('RGBA').resize((768,832),Image.Resampling.LANCZOS)
m=Image.new('L',im.size);d=ImageDraw.Draw(m);d.ellipse((261,528,507,715),fill=255);m=m.filter(ImageFilter.GaussianBlur(3));im=Image.composite(plate,im,m)
islandmask=Image.new('L',im.size);d=ImageDraw.Draw(islandmask);d.ellipse((270,544,499,701),fill=255);d.polygon([(377,557),(377,540),(384,534),(391,544),(392,559)],fill=255)
island=original_garden.copy();island.putalpha(islandmask);island=island.crop((267,533,503,704)).resize((184,133),Image.Resampling.LANCZOS);im.alpha_composite(island,(292,555))
p=Image.open(S/'generated-side-lane-repair.png').convert('RGBA').resize((768,352),Image.Resampling.LANCZOS);full=im.copy();full.paste(p,(0,480));m=Image.new('L',im.size);d=ImageDraw.Draw(m)
for box in [(60,599,200,652),(568,599,708,652)]:d.rectangle(box,fill=255)
a=np.array(m);a=np.minimum(a,np.array(m.filter(ImageFilter.GaussianBlur(2))));im=Image.composite(full,im,Image.fromarray(a))
# Whole outer garden patches remove path-edge trees and widen both exit lanes.
side=Image.open(S/'generated-two-tile-side-paths.png').convert('RGBA').resize((768,352),Image.Resampling.LANCZOS)
full=im.copy();full.paste(side,(0,480));alpha=np.zeros((832,768),np.uint8)
for y in range(512,832):
 for x in range(768):
  weight=max(0,min(1,(216-x)/16)) if x<384 else max(0,min(1,(x-552)/16))
  alpha[y,x]=round(255*weight*min(1,(y-512)/8))
im=Image.composite(full,im,Image.fromarray(alpha))
assert im.crop((0,0,768,512)).tobytes()==base.tobytes()
im.save(O/'art-native.png');im.save(R/'garden-layout-candidate.png')
(O/'ART-INVARIANTS.json').write_text(json.dumps({'interior_unchanged_bounds':[0,0,768,512],'native_dimensions':[768,832],'garden_source_downward_offset':32,'island_source_crop':[267,533,503,704],'island_destination':[292,555,184,133],'side_repair_envelopes':[[60,599,200,652],[568,599,708,652]],'base_sha256':hashlib.sha256((S/'validated-interior-native.png').read_bytes()).hexdigest()},indent=2))
