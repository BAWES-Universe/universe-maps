"""Package generated artwork; no painted pixels are synthesized here.
Each source region is downsampled once directly from the preserved 2004×785 master.
Guide geometry, extraction masks and previews are production metadata, not raster art.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json, hashlib
import numpy as np
P=Path(__file__).resolve().parents[1]
master=Image.open(P/'art-source/avenue-master-03-layout.png').convert('RGB')
source_x=[0,1032,1178,2004]; target_x=[0,736,864,1472]
source_y=[0,320,424,785]; target_y=[0,256,352,576]
base=Image.new('RGB',(1472,576))
regions=[]
for yi in range(3):
 for xi in range(3):
  src=(source_x[xi],source_y[yi],source_x[xi+1],source_y[yi+1])
  dst=(target_x[xi],target_y[yi],target_x[xi+1],target_y[yi+1])
  size=(dst[2]-dst[0],dst[3]-dst[1])
  assert src[2]-src[0]>=size[0] and src[3]-src[1]>=size[1],(src,dst)
  base.paste(master.crop(src).resize(size,Image.Resampling.LANCZOS),dst[:2])
  regions.append({'source':list(src),'destination':list(dst),'scale':[size[0]/(src[2]-src[0]),size[1]/(src[3]-src[1])]})
base.save(P/'layers/avenue-base.png')
# Extract original leaf pixels only, near the path-facing crowns and planting edges.
# Geometry is not used as a solid foreground slab; hue and saturation retain organic edges.
region=Image.new('L',base.size,0);d=ImageDraw.Draw(region)
d.rectangle((0,205,735,255),fill=255)
d.rectangle((692,0,735,255),fill=255)
d.rectangle((692,352,735,538),fill=255)
d.rectangle((864,0,924,538),fill=255)
hsv=np.asarray(base.convert('HSV'));rgb=np.asarray(base);reg=np.asarray(region)>0
h,s,v=[hsv[:,:,i] for i in range(3)]
leaf=reg & (h>=22) & (h<=140) & (s>=70) & (v>=35) & ((rgb[:,:,1].astype(int)-rgb[:,:,2].astype(int))>8)
alpha=Image.fromarray((leaf.astype('uint8')*255),'L').filter(ImageFilter.GaussianBlur(.35))
fore=base.convert('RGBA');fore.putalpha(alpha);fore.save(P/'layers/avenue-foliage-foreground.png');alpha.save(P/'layers/avenue-foreground-mask.png')
# Native preview uses the exact supplied Greg frame at 32×32, not a generated character.
greg=Image.open(P/'assets/greg-reference.png').convert('RGBA').crop((32,0,64,32))
preview=base.convert('RGBA');preview.alpha_composite(greg,(784,416));preview.alpha_composite(fore)
preview.save(P/'docs/avenue-native-greg.png')
proof=base.convert('RGBA'); dr=ImageDraw.Draw(proof)
dr.rectangle((736,0,863,575),outline=(125,249,242,255),width=1)
dr.rectangle((0,256,799,351),outline=(125,249,242,255),width=1)
for x,y in [(800,16),(800,432),(800,544),(16,304),(448,304)]:proof.alpha_composite(greg,(x-16,y-16))
proof.save(P/'docs/avenue-native-geometry.png')
court=Image.open('../universe-campus-courtyard/layers/court-base.png').convert('RGBA')
seam=Image.new('RGBA',(1472,768));seam.alpha_composite(court.crop((0,512,1472,704)),(0,0));seam.alpha_composite(preview,(0,192));seam.save(P/'docs/courtyard-avenue-seam-native.png')
registration={'source':'art-source/avenue-master-03-layout.png','masterSize':list(master.size),'nativeSize':list(base.size),'resampling':'Each of nine regions is downsampled once directly from the original generated master with Lanczos. No region is enlarged. This registers original painted lane shoulders, without repainting or tiling.','regions':regions,'mainPath':{'registeredOuterWidth':128,'approximateCentralTileWidthAtNorth':96,'includes':'Low flush paving shoulders/curbs within the nominal corridor; no vegetation in body route.'},'branch':{'centerY':304,'registeredWidth':96},'foreground':'Original source pixel extraction restricted to path-facing foliage; no newly generated overlay props.'}
(P/'art-source/registration.json').write_text(json.dumps(registration,indent=2)+'\n')
print(json.dumps({'master':list(master.size),'native':list(base.size),'maxScale':max(v for r in regions for v in r['scale']),'foregroundNonzeroPixels':int((np.asarray(alpha)>0).sum())},indent=2))
