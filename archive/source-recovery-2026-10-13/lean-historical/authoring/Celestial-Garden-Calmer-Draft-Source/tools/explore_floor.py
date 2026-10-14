from PIL import Image,ImageDraw
import numpy as np
from scipy import ndimage as nd
from pathlib import Path
R=Path(__file__).resolve().parents[1];(R/'review').mkdir(exist_ok=True);im=Image.open(R/'source/calm-master-native.png').convert('RGB');a=np.asarray(im).astype(float);r,g,b=a.transpose(2,0,1);mask=(r>120)&(g>100)&(b>75)&(r>b*1.12)&(g>b*1.06)&((r-b)<105)
# Only main island; foreground/backdrop never made traversable.
outer=Image.new('L',im.size);d=ImageDraw.Draw(outer);d.polygon([(520,505),(563,491),(695,526),(757,574),(802,581),(784,542),(742,493),(761,416),(907,401),(960,404),(1088,404),(1138,405),(1262,417),(1292,492),(1260,554),(1238,584),(1339,528),(1458,494),(1537,507),(1544,544),(1460,581),(1397,622),(1398,671),(1445,709),(1449,819),(1504,885),(1526,942),(1431,1013),(1315,1053),(1228,1090),(1120,1145),(1144,1280),(1137,1300),(905,1300),(911,1215),(910,1145),(813,1100),(715,1058),(587,1007),(515,942),(535,884),(602,839),(612,744),(708,693),(711,634),(668,602),(538,572)],fill=255)
d.rectangle((704,384,1344,640),fill=255)
mask &= np.asarray(outer)>0
mask=nd.binary_closing(mask,iterations=3)
void,nv=nd.label(~mask)
areas=np.bincount(void.ravel());mask|=np.isin(void,np.flatnonzero(areas<2400))
# Compass is painted paving, include it.
compass=Image.new('L',im.size);ImageDraw.Draw(compass).ellipse((874,610,1176,793),fill=255);mask|=np.asarray(compass)>0
labs,n=nd.label(mask);seed=labs[720,1024];mask=labs==seed
Image.fromarray((mask*255).astype('uint8')).save(R/'review/color-floor-diagnostic.png')
over=Image.new('RGBA',im.size);p=np.asarray(over).copy();p[mask]=[40,255,150,90];out=im.convert('RGBA');out.alpha_composite(Image.fromarray(p));out.save(R/'review/color-floor-overlay.png')
grid=np.ones((48,64),dtype=np.uint8)
for y in range(48):
 for x in range(64):
  if mask[y*32:(y+1)*32,x*32:(x+1)*32].mean()>.93:grid[y,x]=0
print('floorcells',int((grid==0).sum()))
np.save(R/'source/diagnostic-grid.npy',grid)
