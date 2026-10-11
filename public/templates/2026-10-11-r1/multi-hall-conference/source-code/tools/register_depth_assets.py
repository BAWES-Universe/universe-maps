from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];A=R/'assets';S=R/'source';im=Image.open(S/'generated/architectural-depth-kit-master.png').convert('RGBA');out=[]
for name,rect,width in [('congress-window-wall.png',(0,0,1536,480),576),('congress-jamb-left.png',(0,480,240,980),32),('congress-jamb-right.png',(320,480,480,980),32),('congress-stage-steps.png',(700,560,1536,950),256)]:
 a=im.crop(rect);b=a.getchannel('A').point(lambda z:255 if z>128 else 0).getbbox();b=(b[0]-2,b[1]-2,b[2]+2,b[3]+2);a=a.crop(b);size=(width,round(a.height*width/a.width));a.resize(size,Image.Resampling.LANCZOS).save(A/name);out.append({'name':name,'region':rect,'cropLocal':b,'size':size,'uniformScale':width/a.width,'sha256':hashlib.sha256((A/name).read_bytes()).hexdigest()})
# Texture crop comes from the level top tread, never the shaded vertical face.
wood=im.crop((832,670,1392,742));wood.resize((280,36),Image.Resampling.LANCZOS).save(A/'congress-oak-plank.png');out.append({'name':'congress-oak-plank.png','region':[832,670,1392,742],'uniformScale':.5})
(S/'depth-asset-registration.json').write_text(json.dumps({'source':'generated/architectural-depth-kit-master.png','assets':out,'discarded':'Diamond-topped corner pier excluded because its diagonal projection is inappropriate.'},indent=2)+'\n')
