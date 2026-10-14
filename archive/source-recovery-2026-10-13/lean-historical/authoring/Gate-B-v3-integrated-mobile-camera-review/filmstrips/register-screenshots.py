from PIL import Image,ImageOps
import numpy as np,json
from scipy.signal import fftconvolve
from pathlib import Path
root=Path(__file__).parent
art=Image.open('/workspace/shared/gate-water-visibility-audit/gate-reduced-static.png').convert('L')
patches=[('landing-ornament',(418,972,558,1063)),('lower-diamond',(414,1150,559,1248)),('middle-ornament',(422,664,548,707))]
results=[]
for fname in ['IMG_2655.jpeg','IMG_2656.jpeg','IMG_2657.jpeg']:
 im=Image.open('/workspace/shared/gate-user-mobile-feedback/'+fname).convert('L');im=im.resize((355,768),Image.Resampling.LANCZOS);a=np.asarray(im,dtype=float);rows=[]
 for label,box in patches:
  raw=art.crop(box);best=None
  for scale in np.arange(.72,2.22,.015):
   factor=scale/2;patch=raw.resize((round(raw.width*factor),round(raw.height*factor)),Image.Resampling.LANCZOS);t=np.asarray(patch,dtype=float);t-=t.mean();th,tw=t.shape;ones=np.ones_like(t);sm=fftconvolve(a,ones,mode='valid');sq=fftconvolve(a*a,ones,mode='valid');num=fftconvolve(a,t[::-1,::-1],mode='valid');den=np.sqrt(np.maximum(sq-sm*sm/t.size,1)*np.sum(t*t));corr=num/den;corr[:39,:]=-1;corr[max(1,645-th):,:]=-1
   iy,ix=np.unravel_index(corr.argmax(),corr.shape);score=float(corr[iy,ix]);v={'landmark':label,'sourceBox':box,'scaleImagePixelsPerWorldPixel':float(scale),'imageTopLeft':[int(ix*2),int(iy*2)],'correlation':score,'translation':[float(ix*2-box[0]*scale),float(iy*2-box[1]*scale)]}
   if best is None or score>best['correlation']:best=v
  rows.append(best)
 results.append({'screenshot':fname,'registration':rows})
(root/'SCREENSHOT-REGISTRATION.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
