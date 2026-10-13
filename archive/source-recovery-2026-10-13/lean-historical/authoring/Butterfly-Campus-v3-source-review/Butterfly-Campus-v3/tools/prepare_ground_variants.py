from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
from pathlib import Path
import random
R=Path(__file__).resolve().parents[1]
# Standard material quilting of our own generated texture, not new scenery paint.
master=Image.open(R/'art-source/ground-original.png').convert('RGBA')
master.crop((0,0,768,1024)).resize((192,256),Image.Resampling.LANCZOS).save(R/'assets/limestone-texture.png')
master.crop((768,0,1536,1024)).resize((192,256),Image.Resampling.LANCZOS).save(R/'assets/grass-texture.png')
s=master.crop((768,0,1536,1024)).resize((384,512),Image.Resampling.LANCZOS)
s=ImageEnhance.Brightness(s).enhance(.77)
mask=Image.new('L',(128,128));d=ImageDraw.Draw(mask);d.rectangle((12,12,115,115),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(12))
for i in range(8):
 rng=random.Random(1051+i);im=Image.new('RGBA',(256,256),(45,66,32,255))
 for y in range(-32,257,64):
  for x in range(-32,257,64):
   sx=rng.randrange(0,256);sy=rng.randrange(0,384);patch=s.crop((sx,sy,sx+128,sy+128));patch.putalpha(mask);im.alpha_composite(patch,(x,y))
 im.save(R/'assets'/f'grass-material-{i}.png')
# Native-size planted border pieces remain separate from ground.
p=Image.open(R/'assets/planter.png');p.thumbnail((64,32),Image.Resampling.LANCZOS);p.save(R/'assets/border-planter.png')
