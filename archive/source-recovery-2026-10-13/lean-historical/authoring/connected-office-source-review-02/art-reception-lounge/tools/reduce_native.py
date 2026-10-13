from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1]
out={}
for name,canvas,size in [('reception',(160,96),(128,64)),('sofa',(160,96),(128,64)),('coffee-table',(96,64),(64,32))]:
 source=R/f'source/{name}-master.png';im=Image.open(source).convert('RGBA');a=im.getchannel('A');crop=a.point(lambda p:255 if p>=5 else 0).getbbox()
 # One premultiplied resampling operation from original meaningful-alpha crop.
 obj=im.crop(crop).convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
 obj.putalpha(obj.getchannel('A').point(lambda p:0 if p<=4 else p))
 native=Image.new('RGBA',canvas);native.alpha_composite(obj,(16,16));native.save(R/f'native/{name}.png');native.getchannel('A').save(R/f'native/{name}-object-alpha.png')
 native.resize((canvas[0]*8,canvas[1]*8),Image.Resampling.NEAREST).save(R/f'proofs/{name}-native-inspection-8x.png')
 out[name]={'source':str(source.relative_to(R)),'source_size':im.size,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'meaningful_source_crop_xyxy':crop,'native_asset':f'native/{name}.png','canvas':canvas,'target_visible_size':size,'native_alpha_bounds_xyxy':{str(t):native.getchannel('A').point(lambda p:255 if p>=t else 0).getbbox() for t in [1,5,64,128,240]},'native_sha256':hashlib.sha256((R/f'native/{name}.png').read_bytes()).hexdigest(),'transform':'Source alpha>=5 bounding box cropped then exactly one premultiplied Lanczos downsample to target object size; placed at (16,16); final alpha<=4 traces zeroed. No painted pixels synthesized, no avatar scaling.'}
(R/'reduction-manifest.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
