from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];s=Image.open(R/'art-source/room-shell-original.png').convert('RGBA')
# Extract actual material and structural pieces from the original empty-room master.
# Every crop retains source pixels at >= world resolution; none carries furniture.
floor=Image.open(R/'art-source/parquet-original.png').convert('RGBA').resize((384,384),Image.Resampling.LANCZOS)
floor.save(R/'assets/parquet-texture.png')
back=s.crop((125,95,1414,285)).resize((768,113),Image.Resampling.LANCZOS);back.save(R/'assets/back-wall.png')
side=s.crop((110,304,146,680)).resize((20,208),Image.Resampling.LANCZOS);side.save(R/'assets/side-wall.png')
front=s.crop((157,726,552,877)).resize((220,84),Image.Resampling.LANCZOS);front.save(R/'assets/front-wall.png')
column=s.crop((559,716,634,892)).resize((42,98),Image.Resampling.LANCZOS);column.save(R/'assets/stone-column.png')
W,H=960,768;g=Image.new('RGBA',(W,H),(13,26,36,255));b=Image.new('RGBA',(W,H));t=Image.new('RGBA',(W,H));collisions=[]
# Larger usable floor by material tiling, with structural artwork independent.
x,y=96,48;fw,fh=768,592
for yi,yy in enumerate(range(y+100,y+fh,384)):
 for xi,xx in enumerate(range(x,x+fw,384)):
  tile=floor.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if xi%2 else floor
  if yi%2:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  clip=tile.crop((0,0,min(384,x+fw-xx),min(384,y+fh-yy)));g.alpha_composite(clip,(xx,yy))
light=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(light)
for cx in [264,480,704]:ld.polygon([(cx-14,y+96),(cx+14,y+96),(cx+62,y+244),(cx-55,y+244)],fill=(255,196,85,28))
g.alpha_composite(light.filter(ImageFilter.GaussianBlur(22)))
g.alpha_composite(floor.crop((0,0,192,96)),(x+352,y+fh))
g.alpha_composite(back,(x,y))
for yy in range(y+110,y+fh,208):
 h=min(208,y+fh-yy);b.alpha_composite(side.crop((0,0,20,h)),(x-10,yy));b.alpha_composite(side.transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,0,20,h)),(x+fw-10,yy))
for xx in [x,x+220,x+548]:
 width=220 if xx!=x+220 else 108
 a=front.crop((0,0,width,84));b.alpha_composite(a.crop((0,60,width,84)),(xx,y+fh+60));t.alpha_composite(a.crop((0,0,width,60)),(xx,y+fh))
for xx in [x-15,x+326,x+522,x+fw-27]:
 b.alpha_composite(column.crop((0,74,42,98)),(xx,y+fh+62));t.alpha_composite(column.crop((0,0,42,74)),(xx,y+fh-12))
# Foreground only real masonry, never floor threshold. Actual supports are collidable.
collisions += [[x-16,y,32,fh+88],[x+fw-16,y,32,fh+88],[x,y,fw,112],[x,y+fh,352,88],[x+544,y+fh,224,88]]
def prop(name,xx,yy,solid=True,cut=24):
 im=Image.open(R/'assets'/f'{name}.png');w,h=im.size;k=max(0,h-cut)
 # Gentle contact shadow lives below the player, independent of visible object.
 sh=Image.new('RGBA',(w+20,24));ImageDraw.Draw(sh).ellipse((2,3,w+18,22),fill=(15,12,9,85));sh=sh.filter(ImageFilter.GaussianBlur(4));g.alpha_composite(sh,(xx-10,yy+h-12))
 b.alpha_composite(im.crop((0,k,w,h)),(xx,yy+k));t.alpha_composite(im.crop((0,0,w,k)),(xx,yy))
 if solid:collisions.append([xx,yy+max(0,h-24),w,min(h,24)])
# 6-person meeting atleft; independentchairs accessible around table, no mergedsprite.
prop('meeting_table',210,282)
for xx in [220,280]:prop('chair_s',xx,230);prop('chair_n',xx,394)
prop('chair_e',158,304);prop('chair_w',375,304)
# Workstations against back wall, standard64px desks.
for xx in [524,676]:prop('desk',xx,180);prop('chair_n',xx+18,256)
# Separate convivial carpet grouping with a full96px approach aisle.
g.alpha_composite(Image.open(R/'assets/rug.png'),(525,356));prop('couch_s',585,342);prop('couch_e',506,405);prop('couch_w',758,405);prop('coffee',616,430)
prop('bookshelf',120,149);prop('plant',786,161);prop('plant',132,558)
prop('lamp',458,174);prop('lamp',787,527)
prop('reception',408,525)
# Evidence views: same unchanged32px acceptedWoka at frontdesk.
greg=Image.open(R/'qa/greg.png').crop((32,0,64,32));view=g.copy();view.alpha_composite(b);view.alpha_composite(greg,(463,639));view.alpha_composite(t)
for name,im in [('refined-floor',g),('refined-bases',b),('refined-front',t),('HQ-refined-native',view)]:im.save(R/'evidence'/f'{name}.png')
view.resize((W*2,H*2),Image.Resampling.NEAREST).save(R/'evidence/HQ-refined-2x.png')
json.dump({'width':W,'height':H,'collisions':collisions,'safePositions':{'entry':[480,704],'reception':[480,656],'meetingSouth':[252,450],'meetingWest':[176,368],'meetingNorth':[336,216],'workspace':[562,312],'commons':[636,520]}},open(R/'evidence/refined-layout.json','w'),indent=2)
