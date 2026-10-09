from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1]
source=Image.open(R/'art-source/garden-master-v3.png').convert('RGBA')
# Map-renderer asset sampling: source art is reduced uniformly to the requested native receiver.
base=source.resize((1024,1024),Image.Resampling.LANCZOS);base.save(R/'layers/garden-base.png')
woka=Path('authoring-session/lantern-input/greg-gulf-woka-v3.png');shutil.copy2(woka,R/'preview/greg-gulf-woka-v3.png')
sheet=Image.open(woka).convert('RGBA')
def greg(im,x,y,row=0):
 d=ImageDraw.Draw(im); d.ellipse((x-8,y-4,x+8,y+2),fill=(9,24,23,92));im.alpha_composite(sheet.crop((32,row*32,64,row*32+32)),(int(x-16),int(y-32)))
proof=base.copy();greg(proof,550,444,0);proof.save(R/'docs/riverside-native-greg.png')
proof=base.copy()
for x,y,row in [(492,438,0),(492,590,3),(420,520,2),(568,520,1)]:greg(proof,x,y,row)
proof.crop((280,290,712,738)).save(R/'docs/four-cardinal-approaches-native.png')
shutil.copy2(R/'docs/riverside-native-greg.png',R/'docs/first-beautiful-native-composition.png')
meta={'nativeSize':[1024,1024],'sourceSize':list(source.size),'renderSampling':'uniform reduction with Lanczos; no avatar scaling','gregFrame':[32,32],'gregHash':hashlib.sha256(woka.read_bytes()).hexdigest(),'worldOrigin':[2176,1920],'generationTool':'built-in image_gen','selectedSource':'art-source/garden-master-v3.png','attempts':[{'version':1,'status':'rejected for northward geometry drift; preserved'},{'version':2,'status':'court improved; west entrance too narrow/north; preserved'},{'version':3,'status':'selected, west entry widened and shifted; as-built collision geometry follows actual painting'}]}
(R/'docs/asset-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
