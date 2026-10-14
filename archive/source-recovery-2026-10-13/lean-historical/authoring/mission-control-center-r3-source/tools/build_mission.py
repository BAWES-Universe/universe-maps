from pathlib import Path
import json
from PIL import Image,ImageDraw
import build_templates as b
import build_environments as e
R=Path(__file__).resolve().parents[1]
# Native-size rear-facing sprite, one uniform authoring reduction from alpha art.
master=Image.open(R/'source-assets/chair-north-generated-master.png').convert('RGBA')
alpha=master.getchannel('A').point(lambda v:255 if v>24 else 0);box=alpha.getbbox();chair=master.crop(box);chair=chair.resize((32,round(chair.height*32/chair.width)),Image.Resampling.LANCZOS);chair.save(R/'source-assets/chair-north32-native.png')
(R/'mission-control-center/source').mkdir(parents=True,exist_ok=True)
oldfinish=b.Map.finish;b.Map.finish=lambda self:None
oldtask=e.taskseat
def task(self,x,y,name):
 direction='north'
 if name=='briefing-1':y=22;direction='south'
 px,py=x*32+16,y*32+(1 if direction=='north' else 15)
 if name.startswith('operator-'):
  px=[492,776,1048,560,776,984][int(name.split('-')[-1])-1];py=y*32
 if direction=='north':
  im=chair;left,top=px-16,py-12 if name.startswith('operator-') else py+1
  self.base.alpha_composite(im,(left,top))
  # Entire rear backrest safely below the seated head, natural lower-body overlap.
  fg=im.crop((0,0,im.width,min(21,im.height)));self.above.alpha_composite(fg,(left,top))
  self.block(x,y+1,1,1)
 else:
  im=b.A['industrial-chair40-native'];left,top=px-20,py-24
  self.base.alpha_composite(im,(left,top))
  # Front-facing chair is wholly below avatars; no rear rail across the face.
 self.seats.append(dict(name=name,cell=[px//32,y],anchor=[px,py],floorClick=[max(px//32*32+8,min(px//32*32+24,px)),py+16],direction=direction))
e.taskseat=task
m=e.command();b.Map.finish=oldfinish;e.taskseat=oldtask
for a in m.anchors:
 if a['name']=='briefing screen':a['cell']=[8,22]
D=384
master=Image.open(R/'source-assets/north-generated-master.png').convert('RGBA');strip=master.crop((0,0,1122,405)).resize((1536,D),Image.Resampling.LANCZOS)
# Match only the added strip boundary to preserve all accepted interior pixels.
edge=m.base.crop((0,0,1536,1)).resize((1536,16));mask=Image.new('L',(1536,16));md=ImageDraw.Draw(mask)
for yy in range(16):md.line((0,yy,1535,yy),fill=round(255*(yy/15)**2))
strip.paste(Image.composite(edge,strip.crop((0,D-16,1536,D)),mask),(0,D-16));strip.save(R/'source-assets/north-strip-registered.png')
# Root-requested seam fix: generated terrain only in formerly-black exterior
# triangles beside the upper walls. Existing architecture/interior remain exact.
import numpy as np
seam=Image.open(R/'source-assets/north-seam-generated-master.png').convert('RGBA').resize((1536,768),Image.Resampling.LANCZOS)
strip=seam.crop((0,0,1536,D));strip.save(R/'source-assets/north-strip-registered.png')
base=Image.new('RGBA',(1536,1024+D));base.paste(strip,(0,0));base.paste(m.base,(0,D))
pix=np.array(m.base);mask=np.zeros((1024,1536),np.uint8)
for yy in range(384):
 fade=min(1,max(0,(384-yy)/64))
 for xx in list(range(340))+list(range(1196,1536)):
  if max(pix[yy,xx,:3])<=3:mask[yy,xx]=round(255*fade)
Image.fromarray(mask).save(R/'source-assets/exterior-seam-mask.png')
base.paste(seam.crop((0,D,1536,768)),(0,D),Image.fromarray(mask[:384]))
m.base=base
above=Image.new('RGBA',base.size);above.paste(m.above,(0,D));m.above=above;m.g=[[1]*48 for _ in range(12)]+m.g;m.spawn=(m.spawn[0],m.spawn[1]+12)
for s in m.seats:s['cell'][1]+=12;s['anchor'][1]+=D;s['floorClick'][1]+=D
for a in m.anchors:a['cell'][1]+=12
for z in m.zones:z['rect'][1]+=D
m.cropboxes=[(n,(x0,y0+D,x1,y1+D)) for n,(x0,y0,x1,y1) in m.cropboxes]
b.C,b.N,b.W,b.H=48,44,1536,1408
m.finish()
(R/m.slug/'source/revision.json').write_text(json.dumps({'baseline':'mission-control-center-r1','originalOffset':[0,D],'originalScale':1,'northChairNativeSize':chair.size,'northChairAlphaCrop':box,'changedSeats':'Six rear-facing operator chairs and opposing north/south briefing pair; all furniture and architecture otherwise preserved','previewOnlyDirection':'Character art preview respects chair direction; native walk-to seats, no invented sitting action'},indent=2)+'\n')
