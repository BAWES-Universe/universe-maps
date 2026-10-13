from PIL import Image
import numpy as np
from scipy.signal import fftconvolve
A=Image.open('/workspace/shared/overnight-learning-work/source-assets/observatory-environment-ring.png').convert('L')
B=Image.open('/workspace/scratch/41c8dbf833be/generated_images/exec-64b577f1-081e-4401-95bc-7af8640a2ffe.png').convert('L')
b=np.asarray(B,dtype=float);ones=None
for box in [(570,0,875,150),(390,150,530,310),(1090,390,1300,515),(655,900,860,1010)]:
 results=[]
 for s in np.arange(.75,.871,.01):
  t=np.asarray(A.crop(box).resize((round((box[2]-box[0])*s),round((box[3]-box[1])*s))),dtype=float);t-=t.mean();o=np.ones(t.shape);count=t.size
  norm=np.sqrt(np.maximum(fftconvolve(b*b,o,'valid')-fftconvolve(b,o,'valid')**2/count,1)*np.sum(t*t));corr=fftconvolve(b,t[::-1,::-1],'valid')/norm;y,x=np.unravel_index(corr.argmax(),corr.shape);results.append((float(corr[y,x]),s,x,y,x-box[0]*s,y-box[1]*s))
 print(box,sorted(results,reverse=True)[:2])
