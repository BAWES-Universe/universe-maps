"""Deterministic local water refraction/ripple frames. No geometry/ground/avatar motion."""
from PIL import Image
import numpy as np, math

def water_frames(image,mask,impact_points,count=8):
 a=np.array(image.convert('RGBA'));m=np.array(mask.convert('L'))>0;h,w=m.shape;yy,xx=np.indices((h,w));out=[]
 # Constrain every sample to water ownership; boundary pixels remain immutable.
 safe=m.copy()
 for dy in range(-2,3):
  for dx in range(-2,3):safe &= np.roll(np.roll(m,dy,0),dx,1)
 for f in range(count):
  t=2*math.pi*f/count
  dx=np.rint(1.2*np.sin(yy*.61+t)+.35*np.sin(xx*.37-t)).astype(int)
  dy=np.rint(.9*np.sin(xx*.47-t)+.3*np.sin(yy*.31+t)).astype(int)
  sx=np.clip(xx+dx,0,w-1);sy=np.clip(yy+dy,0,h-1);b=a.copy();b[safe]=a[sy[safe],sx[safe]]
  ripple=np.zeros((h,w))
  for cx,cy in impact_points:
   radius=np.sqrt((xx-cx)**2+((yy-cy)*1.9)**2)
   ripple+=np.cos(radius*1.35-t)*np.exp(-radius/12)*5
  color=b[:,:,:3].astype(float)+ripple[:,:,None]*np.array([.7,1,1.05]);b[:,:,:3][safe]=np.clip(color[safe],0,255).astype('uint8')
  assert np.array_equal(b[~m],a[~m]);out.append(Image.fromarray(b))
 assert len({q.tobytes() for q in out})==count
 return out
