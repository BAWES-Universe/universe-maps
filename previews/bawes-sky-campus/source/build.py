"""Native sky campus compiler. All coordinates are world pixels; 16px cells, 32px Wokas."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,math,numpy as np
R=Path(__file__).resolve().parents[1]; A=R/'assets';A.mkdir(exist_ok=True)
T=16; W,H=8192,7168; COL,ROW=W//T,H//T; PX,PY=1792,2048; S=3
OX,OY,OW,OH=2896,1664,2240,1440
layers=[];tilesets=[];gid=1;walk=Image.new('L',(COL,ROW));wd=ImageDraw.Draw(walk);seats=[];objects=[];doors=[];rooms=[]
def rectwalk(box,value=255):
 x,y,w,h=box;wd.rectangle((math.ceil(x/T),math.ceil(y/T),math.floor((x+w)/T)-1,math.floor((y+h)/T)-1),fill=value)
def polywalk(points):wd.polygon([(round((PX+x*S)/T),round((PY+y*S)/T)) for x,y in points],fill=255)
def layer(name,data):layers.append(dict(id=len(layers)+1,name=name,type='tilelayer',x=0,y=0,width=COL,height=ROW,visible=True,opacity=1,data=data))
def image_layer(name,im,x=0,y=0):
 global gid
 # Tight source rectangles; image chunks stay below GPU texture limits.
 x=int(x);y=int(y)
 data=[0]*(COL*ROW)
 for cy in range(0,im.height,1024):
  for cx in range(0,im.width,1024):
   crop=im.crop((cx,cy,min(cx+1024,im.width),min(cy+1024,im.height))).convert('RGBA')
   if not crop.getchannel('A').getbbox():continue
   ww=math.ceil(crop.width/T)*T;hh=math.ceil(crop.height/T)*T
   page=Image.new('RGBA',(ww,hh));page.alpha_composite(crop)
   filename=f'{name}-{cx//1024}-{cy//1024}.png';page.save(A/filename,compress_level=3)
   nc=ww//T;nr=hh//T;first=gid;gid+=nc*nr
   tilesets.append(dict(firstgid=first,name=filename[:-4],image='assets/'+filename,imagewidth=ww,imageheight=hh,tilewidth=T,tileheight=T,tilecount=nc*nr,columns=nc))
   alpha=np.asarray(page.getchannel('A')).reshape(nr,T,nc,T).max(axis=(1,3))
   for ry in range(nr):
    for rx in range(nc):
     tx=(x+cx)//T+rx;ty=(y+cy)//T+ry
     if alpha[ry,rx] and 0<=tx<COL and 0<=ty<ROW:data[ty*COL+tx]=first+ry*nc+rx
 layer(name,data)
# Original arrangement scaled once. Feather only source sky-edge pixels into overscan scenery.
sky=Image.open(R/'source/sky-original.png').convert('RGBA').resize((W,H),Image.Resampling.LANCZOS)
concept=Image.open(R/'source/campus-cleaned-original.png').convert('RGBA').resize((4608,3072),Image.Resampling.LANCZOS)
mask=Image.new('L',concept.size,0);ImageDraw.Draw(mask).rectangle((40,40,4567,3031),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(22));concept.putalpha(mask)
sky.alpha_composite(concept,(PX,PY))
# Native paths conservatively track visible stone floors, not cliffs or distant islands.
for polygon in [
 [(340,350),(1138,350),(1138,410),(1000,432),(795,448),(670,448),(480,423),(340,405)],
 [(300,360),(490,360),(490,397),(300,397)],[(1055,360),(1215,360),(1215,409),(1055,409)],
 [(70,352),(300,350),(308,414),(264,449),(115,449),(54,413)],
 [(1200,328),(1475,328),(1484,450),(1410,480),(1240,470),(1192,424)],
 [(704,435),(778,435),(778,694),(704,694)],
 [(490,704),(660,680),(815,680),(939,727),(919,797),(590,803),(491,775)],
 [(433,731),(600,731),(600,777),(433,777)],[(868,739),(1028,739),(1028,786),(868,786)],
 [(118,720),(410,712),(480,748),(462,801),(195,808),(105,785)],
 [(990,728),(1195,713),(1385,747),(1395,807),(1295,840),(1040,822),(962,781)],
 [(1220,710),(1348,710),(1348,782),(1220,782)]]:polywalk(polygon)
# Office occupies a complete independently furnished floor. 128px exterior ring connects rear route.
rectwalk((OX-128,OY-128,OW+256,OH+256))
base=Image.open(R/'source/floor-original.png').convert('RGBA').crop((105,100,1440,850))
floor=base.resize((OW,OH),Image.Resampling.LANCZOS)
rim=base.crop((625,70,689,134)).resize((128,128),Image.Resampling.LANCZOS)
for yy in range(OY-128,OY+OH+128,128):
 for xx in range(OX-128,OX+OW+128,128):sky.alpha_composite(rim,(xx,yy))
# Independent foundation edge: cliff below the office terrace, greenery outside routes.
plinth=Image.open(R/'source/island-plinth-original.png').convert('RGBA')
cliff=plinth.crop((170,475,1610,887)).resize((OW+256,304),Image.Resampling.LANCZOS)
sky.alpha_composite(cliff,(OX-128,OY+OH+128))
back=plinth.crop((200,0,1570,135)).resize((OW+256,112),Image.Resampling.LANCZOS)
sky.alpha_composite(back,(OX-128,OY-240))
# The cliff is not a walking terrace. Restore the original uninterrupted central bridge over it.
rectwalk((OX-128,OY+OH+128,OW+256,304),0)
bridge=Image.open(R/'source/campus-cleaned-original.png').convert('RGBA').crop((704,395,778,560)).resize((222,495),Image.Resampling.LANCZOS)
sky.alpha_composite(bridge,(PX+704*S,PY+395*S))
rectwalk((PX+704*S,OY+OH+128,222,360))
# Clear the concept's stage audience into its own native chair layer.
paving=base.crop((625,70,689,134))
def pave(box):
 x,y,w,h=box
 for yy in range(y,y+h,64):
  for xx in range(x,x+w,64):sky.alpha_composite(paving.crop((0,0,min(64,x+w-xx),min(64,y+h-yy))),(xx,yy))
pave((PX+1200*S,PY+370*S,864,288))
# Foreground sprite source atlas: own layers, no authored furniture baked into office floor.
kit=Image.open(R/'source/furniture-original.png').convert('RGBA')
spec={'desk':((48,105,390,440),(64,64)),'red-chair':((475,105,735,435),(32,40)),'amber-chair':((805,140,1090,430),(32,40)),'meeting':((1138,120,1760,435),(128,64)),'cafe':((75,500,355,830),(64,64)),'sofa':((390,490,880,830),(128,80)),'planter':((900,490,1300,830),(80,64)),'glass':((1325,540,1740,815),(96,48))}
sprites={}
for name,(box,size) in spec.items():
 im=kit.crop(box);bbox=im.getchannel('A').point(lambda a:255 if a>35 else 0).getbbox();im=im.crop(bbox).resize(size,Image.Resampling.LANCZOS);sprites[name]=im;im.save(A/(name+'.png'))
for name in ('red-chair','amber-chair'):
 padded=Image.new('RGBA',(48,64));padded.alpha_composite(sprites[name],(8,8));sprites[name]=padded
# Furniture placement is editable and explicit in world pixels.
placements=[];fronts=[]
def item(name,x,y,block=None):
 placements.append((name,int(x),int(y)))
 if block:rectwalk(block,0)
 objects.append(dict(kind=name,x=x,y=y,width=sprites[name].width,height=sprites[name].height,collision=block))
def chair(x,y,facing='up',group='office'):
 x=(x//16)*16+8;y=round(y/16)*16
 name='red-chair' if facing=='up' else 'amber-chair';item(name,x-24,y-32)
 seats.append(dict(x=x,y=y,group=group,facing=facing))
 # Small front edge, entirely below torso at the exact floor anchor.
 fronts.append((name,x-24,y,48,16))
# Teams: eight stations near arrival; eight rear focus stations. Desks64, pitch160.
for by in (256,800):
 for bx in (160,512):
  for dx in (0,160):
   for dy in (0,160):
    x=OX+bx+dx;y=OY+by+dy
    item('desk',x,y,(x,y+8,64,48));chair(x+32,y+96)
# Quiet review table and generous circulation in upper-right wing.
for x in (OX+1456,OX+1776):
 item('meeting',x,OY+320,(x,OY+328,128,48))
 for dx in (32,96):chair(x+dx,OY+416);chair(x+dx,OY+288,'down')
# Meeting walls and full-footprint outer wall keep collision separate from covers.
walls=Image.new('RGBA',(OW,OH));wallD=ImageDraw.Draw(walls)
def wall(x,y,w,h):
 rectwalk((x,y,w,h),0)
 wallD.rectangle((x-OX,y-OY,x-OX+w-1,y-OY+h-1),fill='#635442',outline='#e5d0a6',width=3)
 if h<=32:wallD.line((x-OX+2,y-OY+2,x-OX+w-3,y-OY+2),fill='#fff2d6',width=3)
# Front/rear 192px openings.
for yy in (OY,OY+OH-16):
 wall(OX,yy,1024,16);wall(OX+1216,yy,OW-1216,16)
wall(OX,OY+16,16,OH-32);wall(OX+OW-16,OY+16,16,OH-32)
for i,(xx,yy) in enumerate([(1376,736),(1760,736),(1376,1024),(1760,1024)]):
 x=OX+xx;y=OY+yy;w=272;h=192
 wall(x,y,w,16);wall(x,y+h-16,w,16);wall(x+w-16,y+16,16,h-32)
 # 96px opening at west, with short wall returns.
 wall(x,y,16,48);wall(x,y+144,16,48)
 door=dict(id=f'meeting-{i+1}',box=[x,y+48,16,96],inside=[x+16,y+16,w-32,h-32],lock=f'meetingLock{i+1}')
 doors.append(door);rooms.append(dict(id=door['id'],box=door['inside']))
 item('meeting',x+80,y+64,(x+80,y+72,128,48));chair(x+112,y+144);chair(x+176,y+32,'down')
# Native welcoming lounges; positions avoid the central spine and entrances.
for x in (OX+160,OX+544):
 item('sofa',x,OY+1216,(x,OY+1216,128,32))
 for dx in (32,96):seats.append(dict(x=x+dx,y=OY+1264,group='lounge',facing='up'))
for x in (OX+32,OX+OW-112):
 for y in (OY+96,OY+544,OY+1280):item('planter',x,y,(x,y+16,80,48))
for edge,yy in [('front',OY+OH-16),('rear',OY)]:doors.append(dict(id='office-'+edge,box=[OX+1024,yy,192,16],inside=[OX+16,OY+16,OW-32,OH-32]))
# Stage keeps original artwork/backdrop; 32 individually placed audience chairs, 56x64 pitch.
for bx in (PX+1200*S+32,PX+1200*S+432):
 for row in range(4):
  for col in range(4):chair(bx+col*56,PY+380*S+row*64,group='audience')
item('desk',PX+1340*S,PY+320*S,(PX+1340*S,PY+324*S,64,48))
# Mark original stage rear, furniture and planted margins impassable; stage front remains accessible.
rectwalk((PX+1205*S,PY+282*S,280*S,45*S),0)
# Native cafe tables/seats on the existing terrace; original bar remains scenic blocked counter.
for sx,sy in [(195,768),(350,770),(430,767)]:
 x=round((PX+sx*S)/16)*16;y=round((PY+sy*S)/16)*16
 item('cafe',x,y-32,(x,y-24,64,48));chair(x-32,y+16,'down','cafe');chair(x+96,y+16,'up','cafe')
rectwalk((PX+140*S,PY+650*S,250*S,87*S),0)
# Portal arch is scenery only; no invented URL. Keep the arch landing freely accessible.
# Explicit obstacle masks for planters at the bridge ends and garden borders.
for sx,sy,sw,sh in [(685,649,17,37),(778,648,19,39),(620,661,51,36),(812,661,43,37),(1038,695,45,36),(1100,692,46,35),(1350,745,35,42),(90,353,40,38)]:rectwalk((PX+sx*S,PY+sy*S,sw*S,sh*S),0)
# Baked western conservatory furniture is decorative, never a walk-through prop.
# Exact inspected source bounds: curved lounge/table, entrance dining set, central planter strip.
# Keep only the clear eastern approach and stair landing open; no narrow path behind the painted lounge.
for sx,sy,sw,sh in [(52,350,158,105),(185,342,65,38)]:
 box=(PX+sx*S,PY+sy*S,sw*S,sh*S);rectwalk(box,0)
 objects.append(dict(kind='scenic-obstacle',x=box[0],y=box[1],width=box[2],height=box[3],collision=box))
# Full-footprint translucent glass cover. Actual alpha is retained; window band softened for visible occupants.
shell=Image.open(R/'source/office-shell-original.png').convert('RGBA');bounds=shell.getchannel('A').point(lambda a:255 if a>90 else 0).getbbox();shell=shell.crop(bounds).resize((OW,OH),Image.Resampling.LANCZOS)
sa=np.array(shell);sa[int(OH*.73):,:,3]=(sa[int(OH*.73):,:,3]*.48).astype('uint8')
# The actual opening agrees with the collision doorway; not an opaque painted fake door.
sa[OH-208:OH,1024:1216,3]=0;shell=Image.fromarray(sa)
# Serialize base layers first, then overlay depth boundary.
sky.resize((2048,1792),Image.Resampling.LANCZOS).save(R/'review/campus-context.png')
preview=sky.copy();preview.alpha_composite(floor,(OX,OY));preview.alpha_composite(walls,(OX,OY))
for n,x,y in placements:preview.alpha_composite(sprites[n],(x,y))
preview.crop((OX-160,OY-160,OX+OW+160,OY+OH+160)).resize((1280,880)).save(R/'review/office-plan.png')
preview.alpha_composite(shell,(OX,OY));preview.resize((2048,1792),Image.Resampling.LANCZOS).save(R/'review/campus-exterior.png');del preview
image_layer('scenery-and-campus',sky);del sky
image_layer('office-floor',floor,OX,OY);image_layer('office-walls',walls,OX,OY)
# Pack all authored sprites into a 512x256 atlas and place native tile portions.
atlas=Image.new('RGBA',(512,256));sprite_meta={};ax=ay=0
for n,im in sprites.items():
 sw=math.ceil(im.width/16)*16;sh=math.ceil(im.height/16)*16
 if ax+sw>512:ax=0;ay+=96
 atlas.alpha_composite(im,(ax,ay));sprite_meta[n]=(ax//16,ay//16,sw//16,sh//16);ax+=sw
atlas.save(A/'furniture-atlas.png');fg=gid;gid+=512
# All placement coordinates must be 16px aligned. Anchors are declared independently for fine pitch.
tilesets.append(dict(firstgid=fg,name='furniture',image='assets/furniture-atlas.png',imagewidth=512,imageheight=256,tilewidth=16,tileheight=16,tilecount=512,columns=32))
def placement_data(parts):
 data=[0]*(COL*ROW)
 for n,x,y in parts:
  ax,ay,sw,sh=sprite_meta[n]
  for ry in range(sh):
   for rx in range(sw):data[(round(y/16)+ry)*COL+round(x/16)+rx]=fg+(ay+ry)*32+ax+rx
 return data
layer('furniture',placement_data(placements))
# Collision map: every sky/cliff cell is blocked, independently of visual alpha.
logic=Image.new('RGBA',(32,16));logic.save(A/'logic.png');lg=gid;gid+=2
tilesets.append(dict(firstgid=lg,name='logic',image='assets/logic.png',imagewidth=32,imageheight=16,tilewidth=16,tileheight=16,tilecount=2,columns=2,tiles=[dict(id=0,properties=[dict(name='collides',type='bool',value=True)])]))
grid=np.asarray(walk);layer('persistent-collision',[0 if v else lg for v in grid.flat])
spawn=[OX+1120,OY+OH+80];start=[0]*(COL*ROW);start[(spawn[1]//16)*COL+spawn[0]//16]=lg+1;layer('start',start)
inside=[0]*(COL*ROW)
for y in range((OY+16)//16,(OY+OH-16)//16):
 for x in range((OX+16)//16,(OX+OW-16)//16):inside[y*COL+x]=lg+1
layer('office-interior',inside)
variables=[dict(id=i+1,name=d['lock'],type='variable',point=True,x=d['box'][0],y=d['box'][1],width=0,height=0,rotation=0,visible=True,properties=[dict(name='default',type='bool',value=False),dict(name='persist',type='bool',value=False)]) for i,d in enumerate(doors) if d.get('lock')]
layers.append(dict(id=len(layers)+1,type='objectgroup',name='floorLayer',x=0,y=0,visible=True,opacity=1,objects=variables))
# Reuse shallow foreground sections from sprites, not a full overlay of chair backs.
front_atlas=Image.new('RGBA',(96,16))
for i,n in enumerate(['red-chair','amber-chair']):front_atlas.alpha_composite(sprites[n].crop((0,40,48,48)),(i*48,8))
front_atlas.save(A/'chair-fronts.png');cf=gid;gid+=6
tilesets.append(dict(firstgid=cf,name='chair-fronts',image='assets/chair-fronts.png',imagewidth=96,imageheight=16,tilewidth=16,tileheight=16,tilecount=6,columns=6))
frontdata=[0]*(COL*ROW)
for n,x,y,w,h in fronts:
 for rx in range(3):frontdata[(round(y/16))*COL+round(x/16)+rx]=cf+(0 if n=='red-chair' else 3)+rx
layer('chair-fronts',frontdata)
# Door collision lives only in its own removable layer.
doorim=Image.new('RGBA',(16,16),(142,83,35,125));ImageDraw.Draw(doorim).rectangle((0,0,15,15),outline=(234,182,91,220),width=2);doorim.save(A/'door.png');dg=gid;gid+=1
tilesets.append(dict(firstgid=dg,name='door',image='assets/door.png',imagewidth=16,imageheight=16,tilewidth=16,tileheight=16,tilecount=1,columns=1,tiles=[dict(id=0,properties=[dict(name='collides',type='bool',value=True)])]))
for d in doors:
 data=[0]*(COL*ROW);x,y,w,h=d['box']
 for yy in range(y//16,(y+h)//16):
  for xx in range(x//16,(x+w)//16):data[yy*COL+xx]=dg
 layer(d['id']+'-door',data)
image_layer('office-cover',shell,OX,OY)
mapdata=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=COL,height=ROW,tilewidth=16,tileheight=16,nextlayerid=len(layers)+1,nextobjectid=10,layers=layers,tilesets=tilesets,properties=[dict(name='script',type='string',value='runtime.js')])
(R/'campus.tmj').write_text(json.dumps(mapdata,separators=(',',':'))+'\n')
layout=dict(world=[W,H],tile=16,woka=32,conceptOrigin=[PX,PY],conceptScale=3,office=[OX,OY,OW,OH],spawn=spawn,seats=seats,objects=objects,doors=doors,rooms=rooms,waypoints={'spawn':spawn,'office-center':[OX+1120,OY+700],'rear':[OX+1120,OY-64],'cafe':[PX+400*S,PY+752*S],'stage':[PX+1320*S,PY+335*S],'audience':[PX+1320*S,PY+430*S],'portal':[PX+1280*S,PY+775*S],'lower-square':[PX+740*S,PY+755*S],'west-terrace':[PX+230*S,PY+405*S]})
(R/'source/layout.json').write_text(json.dumps(layout,indent=2)+'\n');walk.resize((COL*2,ROW*2)).save(R/'review/walkable.png')
print('Built sky campus:',W,H,'native Woka32; seats',len(seats),'walkable',int(np.count_nonzero(grid)))

(R/'runtime.js').write_text((R/'source/runtime.template.js').read_text().replace('__LAYOUT__',json.dumps(dict(office=layout['office'],doors=layout['doors']),separators=(',',':'))))
