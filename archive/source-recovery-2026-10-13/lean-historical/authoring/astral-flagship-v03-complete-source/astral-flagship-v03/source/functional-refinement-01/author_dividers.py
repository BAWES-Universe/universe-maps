from pathlib import Path
from PIL import Image
import json,hashlib
S=Path(__file__).resolve().parent; R=S.parents[1]; A=R/'assets'
master=Image.open(S/'south-dividers-master.png').convert('RGBA')
rec=[]
for name,box,size,xy in [('divider-lounge-02-south',(0,0,1536,520),(224,48),(640,1280)),('divider-lounge-03-south',(0,520,1536,1024),(320,48),(1120,1280))]:
 im=master.crop(box);bb=im.getchannel('A').point(lambda x:255 if x>8 else 0).getbbox();im=im.crop(bb).resize(size,Image.Resampling.LANCZOS)
 path=A/(name+'.png');im.save(path)
 rec.append({'id':name,'asset':'assets/'+name+'.png','size':list(size),'placement':list(xy),'worldBounds':[xy[0],xy[1],xy[0]+size[0],xy[1]+size[1]],'sourceCrop':list(box),'meaningfulAlphaTrim':list(bb),'alphaTrimThreshold':8,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'intent':'Continuous full-width low planter box; native collision and foreground ownership to be assigned by compiler. Side entrances remain open.'})
manifest={'status':'Supplemental art kit only; frozen art checkpoint untouched','generation':'built-in image_gen','master':'source/functional-refinement-01/south-dividers-master.png','prompt':'source/functional-refinement-01/imagegen-prompt-south-dividers.txt','components':rec}
(S/'divider-kit.json').write_text(json.dumps(manifest,indent=2))
# Separate comparison only, never overwrite frozen artwork or source layers.
review=Image.open(R/'review/flagship-v03-occupied-native.png').convert('RGBA')
for r in rec:review.alpha_composite(Image.open(R/r['asset']).convert('RGBA'),tuple(r['placement']))
review.crop((608,1200,1472,1376)).save(S/'south-dividers-placement-native.png')
kit=Image.new('RGBA',(352,144));kit.alpha_composite(Image.open(A/'divider-lounge-02-south.png'),(16,8));kit.alpha_composite(Image.open(A/'divider-lounge-03-south.png'),(16,88));kit.save(S/'south-dividers-native-kit.png')
print(json.dumps(manifest,indent=2))
