from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent
old=Image.open(R/'fountain-edit-target.png').convert('RGBA');new=Image.open(R/'fountain-ring-edit-native01.png').convert('RGBA')
# Keep source water, spout and physical round stone bowl pixels at their exact
# original positions. Only the surrounding authored paving source is replaced.
protect=Image.new('L',old.size);d=ImageDraw.Draw(protect)
d.ellipse((164,143,428,335),fill=255)
d.polygon([(278,136),(280,118),(313,118),(315,143)],fill=255)
# Protect ALL nontransparent existing animated pixels, not just one rectangle.
alpha=np.asarray(protect).copy()
for p in sorted((R.parent/'effects').glob('fountain-water-*.png')):
 a=np.asarray(Image.open(p).convert('RGBA'))[:,:,3]
 # effect origin816,1344 minus court448,1120 minus crop192,64 =>176,160
 alpha[160:160+a.shape[0],176:176+a.shape[1]]=np.maximum(alpha[160:160+a.shape[0],176:176+a.shape[1]],np.where(a>0,255,0).astype('uint8'))
protect=Image.fromarray(alpha);out=Image.composite(old,new,protect)
# Limit the new authored pixels to the ring and the two relocated bench pockets.
region=Image.new('L',old.size);rd=ImageDraw.Draw(region)
rd.ellipse((48,58,538,411),fill=255)
rd.rounded_rectangle((78,40,212,146),radius=14,fill=255)
rd.rounded_rectangle((44,192,115,306),radius=12,fill=255)
region=region.filter(ImageFilter.GaussianBlur(3))
out=Image.composite(out,old,region)
# Reassert the exact source bowl and animated support after edge blending.
out=Image.composite(old,out,protect)
# Exact unchanged crop edge through a short transition, preserving adjacent panels.
edge=np.zeros((448,608),np.uint8)
for y in range(448):
 for x in range(608):edge[y,x]=round(255*min(1,min(x,y,607-x,447-y)/12))
out=Image.composite(out,old,Image.fromarray(edge));out.save(R/'fountain-ring-registered01.png');protect.save(R/'protected-original-basin-mask.png')
a,b=np.asarray(out),np.asarray(old);assert np.array_equal(a[alpha==255],b[alpha==255])
report={'nativeSize':list(out.size),'worldCropOrigin':[640,1184],'originalBasinPixelsProtected':int((alpha==255).sum()),'allAnimatedSourcePixelsUnchanged':True,'cropEdgePixelsUnchanged':True,'changedPixels':int(np.any(a!=b,axis=2).sum()),'noArtScaleChange':True,'status':'candidate source composite, collision not yet adopted'}
(R/'fountain-ring-registration01.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
