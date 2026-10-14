from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'market-study'
old=Image.open(S/'shore-assembled09-native.png').convert('RGBA');new=Image.open(S/'shore-edit-native02.png').convert('RGBA')
a=np.zeros((512,384),np.uint8)
# Keep the market facade and all upper reference pixels; only lower authored join is adopted.
for y in range(352,512):
 for x in range(384):
  a[y,x]=round(255*min(1,(y-352)/24)*min(1,x/12,(383-x)/6))
patch=new.copy();patch.putalpha(Image.fromarray(a));patch.save(S/'shore-join-patch02.png')
registered=old.copy();registered.alpha_composite(patch);registered.save(S/'shore-assembled09-join02-native.png')
meta={'worldOrigin':[2464,1840],'nativeSize':[384,512],'mask':'lower join y352..512,24px top blend, left12px/right6px preservation','source':'shore-edit-master02.png','sourceMasterSize':list(Image.open(S/'shore-edit-master02.png').size),'preservedUpperRows':352,'notes':['Generated raster repair confined to paving/waterfront join; existing source geometry remains authority.','Conservative32 coast cells protect new curved stone edge; no water is made walkable.'],'blockedRects':[[2816,2272,64,112],[2784,2272,32,48]]};(S/'shore-join-patch02.json').write_text(json.dumps(meta,indent=2)+'\n')
