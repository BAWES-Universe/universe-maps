from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
import build_templates as b
R=Path(__file__).resolve().parents[1];A=R/'source-assets';D=128
b.C,b.N,b.W,b.H=48,36,1536,1152
m=b.Map('inventors-sandbox-workshop','Inventor’s Workshop','Sandbox',dict(b.P,outer='#243b27'))
old=Image.open(A/'workshop-shell-open.png').convert('RGBA');north=Image.open(A/'north-garden-master.png').convert('RGBA').resize((1536,1152),Image.Resampling.LANCZOS).crop((0,0,1536,D));m.base.paste(north,(0,0));ext=Image.open(A/'exterior-clearance-master.png').convert('RGBA');old.paste(ext.crop((0,0,192,1024)),(0,0));old.paste(ext.crop((1344,0,1536,1024)),(1344,0));m.base.paste(old,(0,D));m.spawn=(23,34)
def floor(x,y,w,h):m.block(x,y+4,w,h,0)
# Connected indoor circulation, no walking through illustrated furniture/walls.
for r in [(9,7,24,13),(33,9,1,6),(34,12,6,2),(35,8,5,3),(36,11,3,3),(34,14,3,1),(34,17,6,3),(32,18,4,2),(14,20,4,4),(23,0,2,8),(4,4,2,20),(4,3,4,1),(5,13,4,2),(14,3,27,1),(23,2,2,2),(41,3,3,1),(43,4,2,20),(5,23,38,2),(8,25,32,3),(22,28,4,4),(5,22,1,2),(42,22,1,2),(43,24,2,1)]:floor(*r)
m.block(23,1,2,3,0)
m.block(9,23,1,1) # substantial southwest plant canopy/base
# North material shelf access routes around protected storage footprint.
floor(7,3,7,1);m.block(8,7,6,1)
# Solid illustrated bases at room doorway returns and garden beds.
for r in [(34,12,2,1),(39,12,1,1),(32,19,2,1),(6,23,2,1),(8,27,4,1),(37,27,3,1),(8,25,4,3),(37,25,3,3)]:m.block(r[0],r[1]+4,r[2],r[3])
m.block(6,28,2,3)
m.block(7,30,6,3)
m.block(39,28,3,3)
m.block(36,31,4,2)
m.block(6,17,1,1)
m.block(6,7,2,1) # protect old wall cap and border greenery
from scenery_footprints import apply
scenery=apply(m)
# Native object sprites, generated separately and all substantial pixels inside solids.
def sprite(name,w,h=None):
 im=Image.open(A/(name+'-master.png')).convert('RGBA');box=im.getchannel('A').point(lambda v:255 if v>32 else 0).getbbox();im=im.crop(box);im=im.resize((w,h or round(w*im.height/im.width)),Image.Resampling.LANCZOS);im.save(A/(name+'-native.png'));return im
bench=sprite('workbench',64);stool=sprite('stool',24,20);table=sprite('collaboration-table',64,32)
objects=[]
def addseat(name,px,py,direction='north'):
 py+=D;m.base.alpha_composite(stool,(px-12,py-10));m.seats.append(dict(name=name,cell=[px//32,(py+16)//32],anchor=[px,py],floorClick=[px,py+16],direction=direction))
def solid(name,im,x,y,w,h):
 m.block(x,y+4,w,h);left=x*32+(w*32-im.width)//2;top=(y+h)*32-im.height+D;m.base.alpha_composite(im,(left,top));objects.append(dict(name=name,rect=[left,top,im.width,im.height],solidCells=[x,y+4,w,h]))
# Three two-person benches: native32 working position directly at counter edge.
for i,x in enumerate([10,17,28]):
 solid('indoor-workbench-'+str(i+1),bench,x,7,2,1)
 for j in range(2):addseat(f'workbench-{i*2+j+1}',(x+j)*32+16,8*32)
# Four inward-facing collaboration seats; table is fully enclosed by its two tile rows.
solid('collaboration-table',table,36,18,2,1)
for j,x in enumerate([36,37]):
 addseat('collaboration-north-'+str(j+1),x*32+16,17*32+15,'south')
 addseat('collaboration-south-'+str(j+1),x*32+16,19*32,'north')
floor(36,17,2,1)
# One outdoor workbench, leaving testing pads fully walkable.
solid('courtyard-workbench',bench,34,25,2,1)
for j in range(2):addseat('courtyard-workbench-'+str(j+1),(34+j)*32+16,26*32)
for name,x,y in [('south arrival',23,30),('south workshop doorway',15,22),('west doorway',6,14),('north doorway',23,5),('north materials rack',16,3),('east garden path',43,19),('coral creation pad',17,11),('sage creation pad',27,11),('ochre creation pad',22,17),('idea board',37,9),('idea board doorway',37,12),('collaboration entrance',34,18),('courtyard coral test pad',17,26),('courtyard sage test pad',28,26)]:m.anchor(name,x,y+4)
m.anchor('north garden landing',23,2)
for name,x,y,w,h,kind in [('Indoor collaboration',34,16,6,4,'meeting'),('Coral creation pad',14,9,6,5,'placeholder'),('Sage creation pad',24,9,6,5,'placeholder'),('Ochre creation pad',19,14,7,6,'placeholder'),('Outdoor test court',9,25,23,3,'placeholder'),('Courtyard workbench',33,24,4,4,'placeholder')]:m.zone(name,x,y+4,w,h,kind)
# Projecting north masonry caps sit above players using the paved path behind them.
for box in [(682,252,712,256),(810,252,838,256),(1070,250,1096,256),(1306,252,1334,256)]:
 x0,y0,x1,y1=box;m.above.paste(m.base.crop(box),(x0,y0))
# Architectural fronts only; all chairs are low backless stools below players.
for box in [(192,648,424,744),(592,648,1336,744),(1056,472,1312,544)]:
 x0,y0,x1,y1=box;m.above.paste(m.base.crop((x0,y0+D,x1,y1+D)),(x0,y0+D))
# Transfer head-unsafe foreground below characters, exact composite preserved.
blocked=np.array(m.g,dtype=bool).repeat(32,0).repeat(32,1);Y,X=np.indices(blocked.shape);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));xa=np.maximum(0,X-8);xb=np.minimum(b.W,X+8);yb=np.minimum(b.H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=b.W)&(Y+16<=b.H)
head=np.array(json.loads((A/'reference-head-mask.json').read_text())['headMask'],bool) if False else np.zeros((14,32),bool)
# Derive union from local proof references, or licensed redistribution-safe cached union.
cache=json.loads((A/'reference-head-mask.json').read_text());head=np.array(cache,bool)
swept=np.zeros_like(clear)
for yy,xx in np.argwhere(head):
 dx,dy=int(xx)-16,int(yy)-16;x0=max(0,-dx);x1=min(b.W,b.W-dx);y0=max(0,-dy);y1=min(b.H,b.H-dy);swept[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
fg=np.array(m.above);fg[(fg[:,:,3]>0)&swept]=0;m.above=Image.fromarray(fg)
m.cropboxes=[('indoor-benches',(288,336,1024,448)),('collaboration',(1056,608,1312,800)),('courtyard',(992,896,1216,1040))]
m.finish();out=R/m.slug;b.js(out/'source/scenery-footprints.json',scenery);b.js(out/'source/furniture-footprints.json',objects)
# Varied native review-only characters, no sprite-sheet redistribution.
occupied=m.base.copy()
for i,s in enumerate(m.seats):
 p=A/f'woka-proof-{i%8}.png';im=Image.open(p if p.exists() else A/'greg-reference.png').convert('RGBA');row=0 if s['direction']=='south' else 3;x,y=s['anchor'];occupied.alpha_composite(im.crop((32,row*32,64,row*32+32)),(x-16,y-16))
occupied.alpha_composite(m.above);occupied.save(out/'review/all-seats-occupied-native.png')
for name,box in m.cropboxes:occupied.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3),Image.Resampling.NEAREST).save(out/'review'/(name+'-occupied-3x.png'))
