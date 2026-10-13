from PIL import Image,ImageFilter
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.optimize import least_squares
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=R/'source'
old=Image.open(S/'portal-environment-garden-boundaries-master.png').convert('RGB');new=Image.open(S/'generated-wide-context.png').convert('RGB')
a=np.asarray(old.filter(ImageFilter.GaussianBlur(5))).astype(float)/255;b=np.asarray(new.filter(ImageFilter.GaussianBlur(3))).astype(float)/255
y,x=np.mgrid[30:980:12,30:1500:12];ref=a[y,x];
def res(p):
 sx,sy,tx,ty=p;coords=np.array([y*sy+ty,x*sx+tx]);sample=np.stack([map_coordinates(b[:,:,c],coords,order=1,mode='nearest') for c in range(3)],axis=-1);return (sample-ref).ravel()
r=least_squares(res,[.64,.63,232,204],bounds=([.56,.54,180,160],[.72,.72,290,260]),loss='soft_l1',f_scale=.10,max_nfev=160,diff_step=.0005)
sx,sy,tx,ty=r.x;print(r.x,np.mean(res(r.x)**2));context=new.transform((2048,1536),Image.Transform.AFFINE,(sx,0,tx-sx*256,0,sy,ty-sy*256),Image.Resampling.BICUBIC);context.save(S/'expanded-context.png');preview=context.copy();preview.paste(old,(256,256));preview.save(R/'registered-preview.png');(S/'registration.json').write_text(json.dumps({'scaleXY':[sx,sy],'translationXY':[tx,ty],'outputOffset':[256,256],'residualMSE':float(np.mean(res(r.x)**2))},indent=2))
