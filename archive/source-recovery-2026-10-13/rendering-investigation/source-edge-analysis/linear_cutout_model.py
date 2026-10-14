from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).parent
out={}
for n,base_name,box in [('reading-r4','architecture-and-furniture',(445,295,490,332)),('studio-r8','environment',(246,552,293,590))]:
 def load(name):return np.array(Image.open(R/f'{n}-{name}-plane.png')).astype(float)/255
 b,f=load(base_name),load('foreground')
 assert np.all(b[:,:,3]+f[:,:,3]==1)
 def premul(a):
  a=a.copy();a[:,:,:3]*=a[:,:,3,None];return a
 def sample(a):return (a[:-1,:-1]+a[1:,:-1]+a[:-1,1:]+a[1:,1:])/4
 bs,fs=sample(premul(b)),sample(premul(f))
 sep=fs+bs*(1-fs[:,:,3,None]);full=sample(premul(f)+premul(b))
 bg=np.array([20,18,30])/255
 visual=lambda a:Image.fromarray(np.uint8(np.clip(a[:,:,:3]+bg*(1-a[:,:,3,None]),0,1)*255+.5))
 separate,whole=visual(sep),visual(full)
 x,y= (462,309) if n.startswith('reading') else (269,571)
 out[n]={'model':'Premultiplied bilinear sample at source coordinate + (0.5,0.5), then foreground source-over base. Ideal contiguous planes, no atlas bleed or geometry gaps simulated. Not GPU evidence.','complementaryAlphaExact':True,'outputSamplesBelowOpaque':int((sep[:,:,3]<1).sum()),'minimumCompositedAlpha':float(sep[:,:,3].min()),'exampleWorldSample':[x+.5,y+.5],'exampleAlpha':float(sep[y,x,3]),'exampleIndependentRGBOverDark':list(separate.getpixel((x,y))),'exampleCompositeFirstRGB':list(whole.getpixel((x,y))),'proofBox':box}
 for label,im in [('independent',separate),('composite-first',whole)]:im.crop(box).resize(((box[2]-box[0])*8,(box[3]-box[1])*8),Image.Resampling.NEAREST).save(R/f'{n}-conditional-linear-{label}.png')
(R/'conditional-linear-model.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
