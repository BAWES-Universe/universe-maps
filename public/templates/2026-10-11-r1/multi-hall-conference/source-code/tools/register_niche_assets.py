from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];im=Image.open(R/'source/generated/planter-coffee-kit-master.png').convert('RGBA');out=[]
for name,r,w in [('congress-low-planter.png',(0,0,1536,510),192),('congress-espresso.png',(350,510,1200,1024),64)]:
 a=im.crop(r);b=a.getchannel('A').point(lambda z:255 if z>128 else 0).getbbox();b=(b[0]-2,b[1]-2,b[2]+2,b[3]+2);a=a.crop(b);sz=(w,round(a.height*w/a.width));a.resize(sz,Image.Resampling.LANCZOS).save(R/'assets'/name);out.append({'name':name,'region':r,'cropLocal':b,'size':sz,'uniformScale':w/a.width})
# Two bounded stair widths come from one source by uniform resizing, never stretch.
a=Image.open(R/'assets/congress-stage-steps.png')
for w in [192,160]:a.resize((w,round(a.height*w/a.width)),Image.Resampling.LANCZOS).save(R/'assets'/f'congress-stage-steps-{w}.png')
(R/'source/niche-asset-registration.json').write_text(json.dumps(out,indent=2)+'\n')
