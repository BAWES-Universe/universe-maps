"""Cohesive environment-first templates; geometry prototypes preserved separately."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
import build_templates as b
b.C,b.N,b.W,b.H=48,32,1536,1024
R=b.R

def foreground_polygon(m,points):
 mask=Image.new('L',(b.W,b.H));ImageDraw.Draw(mask).polygon(points,fill=255);patch=m.base.copy();patch.putalpha(mask);m.above.alpha_composite(patch)

def academy():
 m=b.Map('olive-arabic-academy','Olive Arabic Academy','Knowledge',b.P);m.base=b.A['academy-environment-final'].copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(20,30)
 # Whole-tile conservative walkable floors fitted to the authored architecture.
 for r in [(5,5,24,9),(16,13,4,1),(17,14,2,3),(5,17,25,8),(18,24,5,1),(19,25,3,7),(28,15,3,5),(30,3,4,22),(34,5,2,3),(36,5,8,3),(34,13,2,3),(36,12,8,4),(32,20,12,5)]:m.block(*r,0)
 m.block(19,26,1,3)  # solid left entry door leaf; retain64px center opening
 # Flower beds, olive trunks and masonry stay solid; outer canopy uses foreground.
 for r in [(7,20,6,4),(23,20,6,4),(5,17,8,1),(22,17,7,1),(30,3,1,12),(34,8,2,5)]:m.block(*r)
 # Broad doorway approaches: three-tile study openings, two-tile classroom doors.
 for r in [(31,4,3,15),(34,5,3,3),(34,13,3,3),(28,17,4,3)]:m.block(*r,0)
 m.block(15,4,6,1,0)
 for y in [8,10,12]:
  for x in [11,13,15,19,21,23]:m.seat(x,y)
 # Teacher stands behind the lecture stand, facing the students southwards.
 m.base.alpha_composite(b.A['podium-below'],(520,144));m.above.alpha_composite(b.A['podium-above'],(520,144));m.block(16,5,3,2);m.anchor('teacher',17,4);m.zone('Teacher presentation',15,4,5,1,'speaker');m.zone('Classroom audience',9,8,17,6,'listener')
 for name,x,y in [('Study A',39,5),('Study B',39,13)]:
  m.smalltable(x,y);m.seat(x,y+2);m.seat(x+1,y+2);m.zone(name,x-2,y,6,3);m.anchor(name+' entry',36,y+1)
 m.anchor('classroom door',17,15);m.anchor('fountain',6,22);m.anchor('court center',18,21);m.anchor('court west loop',6,19);m.anchor('court east loop',29,22);m.anchor('reading veranda',39,22);m.anchor('arrival',20,30)
 # Southern masonry faces are real foreground, never a phantom collision reveal.
 foreground_polygon(m,[(66,449),(435,449),(435,486),(67,486)])
 foreground_polygon(m,[(690,450),(850,450),(850,487),(690,487)])
 # Canopy foreground selected by foliage chroma within bounded trees; trunks remain solid.
 import numpy as np
 pix=np.array(m.base);mask=np.zeros((b.H,b.W),dtype=np.uint8)
 for x0,y0,x1,y1 in [(205,540,451,702),(715,536,958,707)]:
  p=pix[y0:y1,x0:x1,:3].astype(int);green=(p[:,:,1]>p[:,:,0]*.84)&(p[:,:,1]>p[:,:,2]*1.08)&(p[:,:,1]<180);mask[y0:y1,x0:x1]=green*255
 foliage=m.base.copy();foliage.putalpha(Image.fromarray(mask));m.above.alpha_composite(foliage)
 m.cropboxes=[('classroom',(256,128,832,448)),('study',(1056,96,1440,544)),('court',(128,512,1024,800))]
 m.finish();return m

def desk(m,x,y,name):
 # One detailed 63px desk, centered on its native32 seat column.
 m.base.alpha_composite(b.A['light-desk'],(x*32-16,y*32-8));m.block(x-1,y,3,1);m.seat(x,y+1,name)

def cowork():
 m=b.Map('timber-design-studio','Timber & Stone Design Studio','Work',b.P);m.base=b.A['cowork-environment-final'].copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(24,29)
 for rr in [(5,5,38,9),(4,6,41,8),(21,5,6,22),(19,18,11,5),(6,18,11,6),(31,18,12,6),(17,19,4,3),(27,19,5,3),(22,24,4,8)]:m.block(*rr,0)
 for i,(x,y) in enumerate([(7,7),(15,7),(7,11),(15,11),(31,7),(39,7),(31,11),(39,11)]):desk(m,x,y,'desk-'+str(i+1))
 for name,x in [('Meeting A',10),('Meeting B',36)]:
  m.smalltable(x,19);m.seat(x,21);m.seat(x+1,21);m.zone(name,x-3,18,9,6);m.anchor(name+' approach',x+3,21)
 m.anchor('west studio entry',19,10);m.anchor('east studio entry',29,10);m.anchor('materials gallery',24,6);m.anchor('central hall',24,20);m.anchor('arrival',24,29)
 foreground_polygon(m,[(96,448),(579,448),(579,487),(96,487)])
 foreground_polygon(m,[(965,448),(1442,448),(1442,487),(965,487)])
 m.cropboxes=[('desk-west',(160,192,608,448)),('desk-east',(928,192,1376,448)),('meeting',(192,544,1376,768))];m.finish();return m

def observatory():
 m=b.Map('quiet-orbit-observatory','Quiet Orbit Observatory','Knowledge',dict(b.P,outer='#101d2a'));m.base=b.A['observatory-environment-ring'].copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(24,29)
 # Conservative inscribed floor of the round observatory.
 for y in range(4,16):
  for x in range(14,34):
   if all(((xx-768)/286)**2+((yy-330)/190)**2<1 for xx in [x*32,(x+1)*32] for yy in [y*32,(y+1)*32]):m.block(x,y,1,1,0)
 for rr in [(22,14,4,16),(4,16,16,7),(28,16,17,7),(20,18,2,4),(26,18,2,4),(22,29,4,3)]:m.block(*rr,0)
 m.block(15,16,6,2);m.block(27,16,6,2) # curved rail wall footprints
 m.block(21,9,6,4);m.block(22,6,5,3) # plinth plus projected instrument, solid physical obstacles
 for i,(x,y) in enumerate([(7,17),(15,17),(7,20),(15,20)]):desk(m,x,y,'research-'+str(i+1))
 for y in [18,21]:
  for x in [32,35,38,41]:m.seat(x,y,'seminar-'+str(len(m.seats)-3))
 m.anchor('telescope west',19,9);m.anchor('telescope east',29,9);m.anchor('observation ring',24,14);m.anchor('north telescope loop',24,5);m.anchor('northwest telescope loop',20,7);m.anchor('northeast telescope loop',28,7);m.anchor('research entry',20,19);m.anchor('seminar speaker',36,16);m.anchor('seminar entry',28,19);m.anchor('arrival',24,29);m.zone('Seminar speaker',30,16,13,1,'speaker');m.zone('Seminar audience',30,17,13,6,'listener')
 foreground_polygon(m,[(497,432),(649,486),(680,532),(640,552),(495,493)])
 foreground_polygon(m,[(872,490),(1048,426),(1048,485),(903,550),(854,535)])
 m.cropboxes=[('research',(128,480,640,768)),('seminar',(928,480,1408,768)),('telescope',(448,96,1088,512))];m.finish();return m

def taskseat(m,x,y,name):
 px,py=x*32+16,y*32+15;im=b.A['industrial-chair40-native'];m.base.alpha_composite(im,(px-20,py-24));m.above.alpha_composite(im.crop((6,23,34,39)),(px-14,py-1));m.block(x,y+1,1,1);m.seats.append(dict(name=name,cell=[x,y],anchor=[px,py],floorClick=[px,py+16],direction='north'))

def clip_foreground_heads(m):
 import numpy as np
 blocked=np.array(m.g,dtype=bool).repeat(32,0).repeat(32,1);Y,X=np.indices(blocked.shape);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));xa=np.maximum(0,X-8);xb=np.minimum(b.W,X+8);yb=np.minimum(b.H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=b.W)&(Y+16<=b.H)
 greg=np.array(b.A['greg-reference']);head=np.zeros((14,32),bool)
 head|=np.array(json.loads((R/'source-assets/reference-head-mask.json').read_text()),dtype=bool)
 for rr in range(4):
  for cc in range(3):head|=greg[rr*32:rr*32+14,cc*32:cc*32+32,3]>32
 swept=np.zeros_like(clear)
 for yy,xx in np.argwhere(head):
  dx,dy=int(xx)-16,int(yy)-16;x0=max(0,-dx);x1=min(b.W,b.W-dx);y0=max(0,-dy);y1=min(b.H,b.H-dy);swept[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
 fg=np.array(m.above);unsafe=(fg[:,:,3]>0)&swept;before=Image.alpha_composite(m.base,m.above);transfer=fg.copy();transfer[~unsafe]=0;m.base.alpha_composite(Image.fromarray(transfer));fg[unsafe]=0;m.above=Image.fromarray(fg);assert Image.alpha_composite(m.base,m.above).tobytes()==before.tobytes()
 return dict(transferredPixels=int(unsafe.sum()),combinedArtworkByteExact=True,scope='Only reachable-head-unsafe chair foreground pixels transferred below avatars; all other backrail pixels preserved')

def command():
 m=b.Map('mission-control-center','Mission Control Center','Work',dict(b.P,outer='#111b23'));m.base=b.A['command-environment-clear'].copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(24,29)
 for rr in [(21,14,6,16),(5,22,12,5),(31,22,12,5),(17,24,5,3),(27,24,4,3),(21,29,6,2)]:m.block(*rr,0)
 floor_mask=Image.new('L',(b.W,b.H));ImageDraw.Draw(floor_mask).polygon([(385,173),(1153,173),(1274,287),(1279,397),(1200,477),(330,477),(252,398),(250,298)],fill=255)
 for yy in range(5,15):
  for xx in range(7,41):
   if floor_mask.crop((xx*32,yy*32,(xx+1)*32,(yy+1)*32)).getextrema()==(255,255):m.block(xx,yy,1,1,0)
 for rr in [(13,6,4,3),(22,6,4,3),(31,6,4,3),(16,10,3,3),(22,10,4,3),(29,10,4,3),(9,23,4,3)]:m.block(*rr)
 for i,(x,y) in enumerate([(15,9),(24,9),(32,9),(17,13),(24,13),(30,13)]):taskseat(m,x,y,'operator-'+str(i+1))
 for x in [10,11]:taskseat(m,x,26,'briefing-'+str(x-9))
 m.zone('Briefing room',5,22,13,6);m.anchor('briefing entry',18,25);m.anchor('briefing screen',10,22);m.anchor('incident review',36,24);m.anchor('main control west',10,12);m.anchor('main control east',37,12);m.anchor('central command aisle',21,11);m.anchor('arrival',24,29)
 m.cropboxes=[('operators',(384,192,1152,480)),('briefing',(128,672,608,896)),('incident',(992,672,1408,896))];safety=clip_foreground_heads(m);m.finish();b.js(R/m.slug/'source/foreground-safety.json',safety);return m

if __name__=='__main__':
 makers={'academy':academy,'cowork':cowork,'observatory':observatory,'command':command}
 if len(sys.argv)>1:makers[sys.argv[1]]()
 else:
  for fn in makers.values():fn()
