from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
r=Path(__file__).resolve().parents[1]
s=4
im=Image.new('RGBA',(256*s,384*s),(245,245,238,255));d=ImageDraw.Draw(im)
def rect(b,c,o=None,w=1):d.rectangle(tuple(v*s for v in b),fill=c,outline=o,width=w*s)
def line(p,c,w=1):d.line(tuple(v*s for v in p),fill=c,width=w*s)
f=lambda z:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',z*s)
# All desired physical positions in the same plan-oblique projection as A.
# route is an annotation only, to become genuine transparency.
rect((24,224,232,320),'#d8f6ff')
for y in (224,320):line((16,y,240,y),'#1b91b0')
# west wall continuing behind canopy: end feet represent wall plane x64.
rect((32,32,64,224),'#d6c397','#756951')
rect((32,208,64,352),'#d6c397','#756951')
# 112px elevation of 32px posts. ground north y192..224 south y320..352.
for x in (48,144):
 for y in (192,320):
  rect((x,y-112,x+32,y+32),'#e4d3aa','#756951')
  rect((x,y-112,x+32,y-80),'#f3e2bb','#756951')
# canopy top at height112. Roof footprint y192..352 => projected80..240.
rect((56,80,176,240),'#1e6064','#bd8e37',3)
for x in (72,104,136,168):line((x,80,x,240),'#bd8e37',2)
# roof front fascia shallow
rect((56,240,176,248),'#174d52','#bd8e37',1)
# ground plane and threshold dashed yellow, annotations to remove
for y in range(224,321,8):line((64,y,64,min(y+4,320)),'#ff3172',1)
d.text((11*s,6*s),'GEOMETRY GUIDE / NOT FINISHED ART',font=f(9),fill='#172c31')
d.text((214*s,250*s),'E',font=f(15),fill='#172c31')
d.text((12*s,360*s),'96px N/S clear at x64; route E/W',font=f(9),fill='#172c31')
im.save(r/'review/side-porch-geometry-guide.png')
