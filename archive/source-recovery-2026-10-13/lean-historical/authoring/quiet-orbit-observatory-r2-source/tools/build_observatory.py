"""Bounded r2: new north strip and regroup eight existing seminar chairs only."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
import build_templates as b
import build_environments as e
R=Path(__file__).resolve().parents[1]
# Build original accepted map in memory; change only eight chair placements.
original_finish=b.Map.finish;b.Map.finish=lambda self:None
original_seat=b.Map.seat
seminar=0
def seat(self,x,y,name=None):
 global seminar
 if name and name.startswith('seminar-'):
  x=35+seminar%4;y=19+(seminar//4)*2;seminar+=1
 original_seat(self,x,y,name)
b.Map.seat=seat
m=e.observatory();b.Map.seat=original_seat;b.Map.finish=original_finish
# Only generated pixels above the original canvas are used. Registration source:
# native1536 -> generated1254, scale .8164, original north edge generated y317.
D=384
master=Image.open(R/'source-assets/north-extension-generated-master.png').convert('RGBA')
strip=master.crop((0,0,1254,317)).resize((1536,D),Image.Resampling.LANCZOS)
# North-only seam registration outside the accurately matched central arch.
# Match boundary colors over24px; preserve generated arch geometry unblended.
edge=m.base.crop((0,0,1536,1)).resize((1536,24))
mask=Image.new('L',(1536,24));md=ImageDraw.Draw(mask)
for yy in range(24):
 for xx in range(1536):
  side=(min(1,max(0,(520-xx)/60)) if xx<768 else min(1,max(0,(xx-1016)/60)))
  md.point((xx,yy),fill=round(255*(yy/23)**2*side))
strip.paste(Image.composite(edge,strip.crop((0,D-24,1536,D)),mask),(0,D-24))
strip.save(R/'source-assets/north-strip-registered.png')
base=Image.new('RGBA',(1536,1024+D));base.paste(strip,(0,0));base.paste(m.base,(0,D));m.base=base
above=Image.new('RGBA',base.size);above.paste(m.above,(0,D));m.above=above
m.g=[[1]*48 for _ in range(D//32)]+m.g
m.spawn=(m.spawn[0],m.spawn[1]+D//32)
for s in m.seats:
 s['cell'][1]+=D//32;s['anchor'][1]+=D;s['floorClick'][1]+=D
for a in m.anchors:a['cell'][1]+=D//32
for z in m.zones:z['rect'][1]+=D
m.cropboxes=[(n,(x0,y0+D,x1,y1+D)) for n,(x0,y0,x1,y1) in m.cropboxes]
b.C,b.N,b.W,b.H=48,44,1536,1408
m.finish()
(R/m.slug/'source/revision.json').write_text(json.dumps(dict(baseline='quiet-orbit-observatory-r1',northExtensionPixels=D,originalOffset=[0,D],originalScale=1,chairCount=8,audienceRows=[[35,36,37,38],[35,36,37,38]],audienceRowY=[31,33],stageSemantics='Unchanged native speakerMegaphone/listenerMegaphone pair; source-verified status inhibits proximity bubbles',generation='Built-in image tool; generated master only contributes pixels above original canvas'),indent=2)+'\n')
