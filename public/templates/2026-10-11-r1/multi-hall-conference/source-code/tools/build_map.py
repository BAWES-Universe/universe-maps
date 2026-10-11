from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,math,random
R=Path(__file__).resolve().parents[1];A=R/'assets';S=R/'source';Q=R/'review';O=R/'map32';O.mkdir(exist_ok=True);(R/'validation').mkdir(exist_ok=True)
W,H,T=3072,2048,32;C,N=W//T,H//T
F=str(A/'fonts/DejaVuSans.ttf');FB=str(A/'fonts/DejaVuSans-Bold.ttf');font=lambda n,b=False:ImageFont.truetype(FB if b else F,n)
jw=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n');load=lambda f:Image.open(A/f).convert('RGBA')
# New proportional room modules. No orientation rotations or unequal-axis scaling.
reg=json.loads((S/'asset-registration.json').read_text());reg['assets']=[a for a in reg['assets']if a['source']!='room-kit-master.png'];master=Image.open(S/'generated/room-kit-master.png').convert('RGBA')
for name,rect,width in [('congress-wall-left.png',(0,0,300,1024),56),('congress-wall-right.png',(1230,0,1536,1024),56),('congress-screen.png',(300,0,1230,520),256),('congress-lectern.png',(400,520,1100,1024),48)]:
 im=master.crop(rect);b=im.getchannel('A').point(lambda v:255 if v>128 else 0).getbbox();b=(b[0]-2,b[1]-2,b[2]+2,b[3]+2);im=im.crop(b);sz=(width,round(im.height*width/im.width));im.resize(sz,Image.Resampling.LANCZOS).save(A/name);reg['assets'].append({'asset':name,'source':'room-kit-master.png','region':rect,'opaqueCropLocal':b,'size':sz,'uniformScale':width/im.width})
jw(S/'asset-registration.json',reg)
base=Image.new('RGBA',(W,H),'#233c32');above=Image.new('RGBA',(W,H));g=np.ones((N,C),dtype=np.uint8);quiet=np.zeros_like(g);floor=load('terrazzo-native-256.png')
for y in range(64,1984,256):
 for x in range(64,2944,256):base.alpha_composite(floor,(x,y))
# clip clean boundary; whole venue has continuous flooring, rooms subdivide it.
d=ImageDraw.Draw(base);d.rectangle((2944,0,W,H),fill='#233c32');d.rectangle((0,1984,W,H),fill='#233c32');g[4:61,3:91]=0
solids=[];landmarks=[];seats=[];rooms=[];social=[];furniture=[];doors=[]
def solid(id,box):
 x,y,w,h=map(int,box);assert x%32==y%32==w%32==h%32==0,(id,box);g[y//32:(y+h)//32,x//32:(x+w)//32]=1;solids.append({'id':id,'rect':box})
def openbox(box):
 x,y,w,h=box;assert x%32==y%32==w%32==h%32==0;g[y//32:(y+h)//32,x//32:(x+w)//32]=0
# Use interior portions for seamless repeated long runs, retaining genuine end caps.
wall=load('congress-window-wall.png');wl=load('congress-wall-left.png');wr=load('congress-wall-right.png')
def wall_h(id,x,y,w,gaps=[]):
 # physical wall occupies final32px; vertical face projects north, never changes ground geometry.
 isSouth='south'in id or id=='venue-north'; wallpiece=wall.crop((0,0,wall.width,32)) if isSouth else wall; top=y-(wallpiece.height-32)
 for xx in range(x,x+w,wall.width-12):
  piece=wallpiece.crop((6,0,6+min(wall.width-12,x+w-xx),wallpiece.height));base.alpha_composite(piece,(xx,top))
 solid(id,[x,y,w,32]);sh=Image.new('RGBA',(w,12));sd=ImageDraw.Draw(sh)
 for sy in range(12):sd.line((0,sy,w,sy),fill=(35,28,18,max(0,45-sy*4)))
 base.alpha_composite(sh,(x,y+32))
 for a,b in gaps:
  # restore the continuous terrazzo through each entrance and add a shallow oak sill.
  for yy in range(top,y+32):
   for xx in range(a,b):base.putpixel((xx,yy),floor.getpixel(((xx-64)%256,(yy-64)%256)))
  dd=ImageDraw.Draw(base);dd.rectangle((a,y+18,b-1,y+22),fill='#b79c6f');dd.rectangle((a,y+23,b-1,y+25),fill='#66593e');openbox([a,y,b-a,32]);doors.append({'id':id+'-door','rect':[a,y,b-a,32],'anchor':[(a+b)//2,y]});base.alpha_composite(load('congress-jamb-left.png'),(a-32,y+32-load('congress-jamb-left.png').height));base.alpha_composite(load('congress-jamb-right.png'),(b,y+32-load('congress-jamb-right.png').height))
def wall_v(id,x,y,h,right=False,gaps=[]):
 im=wr if right else wl
 for yy in range(y,y+h,im.height-40):base.alpha_composite(im.crop((0,20,im.width,20+min(im.height-40,y+h-yy))),(x-12,yy))
 solid(id,[x,y,32,h])
 for a,b in gaps:
  for yy in range(a,b):
   for xx in range(x-12,x+44):base.putpixel((xx,yy),floor.getpixel(((xx-64)%256,(yy-64)%256)))
  dd=ImageDraw.Draw(base);dd.rectangle((x+15,a,x+21,b-1),fill='#b79c6f');openbox([x,a,32,b-a]);doors.append({'id':id+'-door','rect':[x,a,32,b-a],'anchor':[x+16,(a+b)//2]})
def carpet(box,color):
 x,y,w,h=box;im=Image.new('RGBA',(w,h),color);ar=np.array(im);rng=np.random.default_rng(x+y);noise=rng.integers(-2,3,(h,w,1));ar[:,:,:3]=np.clip(ar[:,:,:3].astype(int)+noise,0,255);im=Image.fromarray(ar);z=ImageDraw.Draw(im);z.rounded_rectangle((4,4,w-5,h-5),radius=10,outline='#aca58a',width=2);base.alpha_composite(im,(x,y))
def sign(txt,x,y,w=160):
 z=ImageDraw.Draw(base);z.rounded_rectangle((x,y,x+w,y+24),radius=3,fill='#244638',outline='#bda982',width=1);bb=z.textbbox((0,0),txt,font=font(13,True));z.text((x+(w-bb[2])/2,y+3),txt,font=font(13,True),fill='#f2ecd9')
def asset(name,x,y):base.alpha_composite(load(name),(int(x),int(y)))
def chair(id,anchor,dr='north',kind='audience',room=None):
 ax,ay=anchor;im=load('congress-chair-'+dr+'.png');ox,oy={'north':(24,16),'south':(24,36),'east':(30,28),'west':(18,28)}[dr];x,y=ax-ox,ay-oy
 if dr=='north':cut=29
 elif dr=='south':cut=im.height
 else:cut=im.height-7
 base.alpha_composite(im.crop((0,0,im.width,cut)),(x,y));above.alpha_composite(im.crop((0,cut,im.width,im.height)),(x,y+cut))
 # Back/leg guard cells are outside the occupied native16px body; all click destinations remain open.
 if dr=='north':box=[(ax//32)*32,ay+32,32,32]
 elif dr=='south':box=[ax-16,ay-64,32,32]
 elif dr=='east':box=[ax-48,ay,32,32]
 else:box=[ax+16,ay,32,32]
 # Side seat anchors are tile-centered; lateral guard uses aligned native cells.
 assert box[0]%32==0,(id,box);solid(id+'-back',box)
 rec={'id':id,'anchor':anchor,'floorClick':[ax,ay+16],'direction':dr,'kind':kind,'room':room,'art':[x,y,im.width,im.height],'solid':box,'aboveFromLocalY':cut}
 furniture.append(rec);(seats if kind=='audience' else social).append(rec)
def lowtable(id,cx,cy):
 im=load('congress-low-table.png');asset('congress-low-table.png',cx-40,cy-22);solid(id,[cx-32,cy,64,32]);furniture.append({'id':id,'kind':'table','art':[cx-40,cy-22,80,im.height],'solid':[cx-32,cy,64,32]})
def screen(id,cx,y,txt):
 asset('congress-screen.png',cx-128,y);z=ImageDraw.Draw(base);z.text((cx-94,y+24),txt,font=font(19,True),fill='#e2dfc5');z.line((cx-94,y+55,cx+86,y+55),fill='#789584',width=2);z.text((cx-94,y+66),'CONFERENCE TEMPLATE',font=font(10),fill='#9db19f');solid(id,[cx-128,((y+load('congress-screen.png').height-1)//32)*32,256,32])
def podium(id,cx,y):
 lectern=load('congress-lectern.png');base.alpha_composite(lectern.crop((0,0,lectern.width,14)),(cx-24,y));above.alpha_composite(lectern.crop((0,14,lectern.width,lectern.height)),(cx-24,y+14));solid(id,[cx-16,y+32,32,32]);landmarks.append({'id':id+'-speaker','anchor':[cx,y+8],'floorClick':[cx,y+24],'kind':'speaker'})
# Continuous circulation is framed by restrained oak/copper inlays and soft edge shadows.
z=ImageDraw.Draw(base)
for xx in [1312,1560]:z.rectangle((xx,256,xx+3,1808),fill='#b59d74')
for yy in [1008,1128]:z.rectangle((160,yy,2832,yy+3),fill='#baa785')
# Room carpet and wall ownership.
carpet([192,256,1024,608],'#435e4d');carpet([1664,256,1024,480],'#77735c');carpet([1664,1280,1024,544],'#536765')
wall_h('summit-north',128,192,1152);wall_v('summit-west',128,224,768);wall_v('summit-east',1248,224,768,True,[(864,960)]);wall_h('summit-south',128,960,1152,[(608,800)])
wall_h('forum-north',1600,192,1152);wall_v('forum-west',1600,224,672,False,[(768,864)]);wall_v('forum-east',2720,224,672,True);wall_h('forum-south',1600,864,1152,[(2112,2304)])
wall_h('lab-north',1600,1216,1152);wall_v('lab-west',1600,1248,640,False,[(1440,1632)]);wall_v('lab-east',2720,1248,640,True);wall_h('lab-south',1600,1856,1152)
# Networking foyer is open at north and east; no fourth sealed box.
wall_v('foyer-west',128,1216,736);wall_h('foyer-south',128,1920,1152);wall_h('foyer-north-short',128,1216,416);wall_h('foyer-north-short2',864,1216,416)
# Exterior perimeter keeps unused margins visible but inaccessible.
wall_h('venue-north',64,96,2880);wall_v('venue-west',64,128,1856);wall_v('venue-east',2912,128,1856,True);wall_h('venue-south',64,1952,2880,[(1376,1504)])
# Bounded exterior threshold apron: an actual short walkable arrival, not a fake portal.
openbox([1376,1952,128,64]);base.alpha_composite(floor.crop((0,0,128,64)),(1376,1952))
# Stages read as low timber floors. These are flat2D decorative rises with open full-width approaches.
for id,box in [('summit',[224,256,992,160]),('forum',[1728,256,928,160]),('lab',[1728,1280,928,128])]:
 x,y,w,h=box;plank=load('congress-oak-plank.png')
 for yy in range(y,y+h,plank.height):
  for xx in range(x,x+w,plank.width):base.alpha_composite(plank.crop((0,0,min(plank.width,x+w-xx),min(plank.height,y+h-yy))),(xx,yy))
 z=ImageDraw.Draw(base);z.rectangle((x,y,x+w-1,y+h-1),outline='#6e5639',width=4);z.rectangle((x,y+h-10,x+w-1,y+h-1),fill='#765a3b');z.line((x,y+h-12,x+w-1,y+h-12),fill='#e0c49b',width=3);step=load('congress-stage-steps-160.png'if id=='lab'else'congress-stage-steps-192.png');trim=round(step.width*.095);step=step.crop((trim,0,step.width-trim,step.height));base.alpha_composite(step,(1984+trim if id=='lab'else x+w//2-step.width//2,y+h-10))
# Screen footprints are at rear, speakers in front. Native roles never overlap another hall.
screen('summit-screen',704,228,'SUMMIT');podium('summit-lectern',720,352)
screen('forum-screen',2176,228,'FORUM');podium('forum-lectern',2192,352)
screen('lab-screen',2176,1252,'LAB');podium('lab-lectern',1936,1344)
for row,ay in enumerate([512,608,704,800]):
 for bank in range(3):
  for col in range(4):chair(f'summit-r{row+1}-b{bank+1}-s{col+1}',[304+bank*320+col*64,ay],room='summit')
for row,ay in enumerate([480,576,672]):
 for col,ax in enumerate([1968,2096,2224,2352]):chair(f'forum-front-{row}-{col}',[ax,ay],room='forum')
for side,ax,dr in [('west',1776,'east'),('east',2608,'west')]:
 for row,ay in enumerate([416,480,544,608,672,736]):chair(f'forum-{side}-{row}',[ax,ay],dr,room='forum')
# Workshop uses closer four-person islands. Every seat is inside the Lab audience, no per-table call zones.
for row,cy in enumerate([1504,1728]):
 for col,cx in enumerate([1856,2176,2496]):
  lowtable(f'lab-table-{row}-{col}',cx,cy)
  for k,ax,ay,dr in [('north',cx+16,cy-64,'south'),('south',cx+16,cy+64,'north'),('west',cx-80,cy,'east'),('east',cx+112,cy,'west')]:chair(f'lab-{row}-{col}-{k}',[ax,ay],dr,room='lab')
# Meeting bays have three low planted/wood boundary sides, wide south opening, no through shortcuts.
for i,bx in enumerate([192,704],1):
 carpet([bx,1280,384,288],'#3b5849');roomid=f'congress-lounge-{i}';rooms.append({'id':roomid,'rect':[bx+32,1312,319,223]})
 z=ImageDraw.Draw(base)
 for j,b in enumerate([[bx,1280,384,32],[bx,1312,32,256],[bx+352,1312,32,256],[bx+32,1536,64,32],[bx+288,1536,64,32]]):
  x,y,w,h=b;z.rounded_rectangle((x,y,x+w-1,y+h-1),radius=5,fill='#a0855e',outline='#66573f',width=3);z.rectangle((x+5,y+5,x+w-6,y+h-6),fill='#516b4e');solid(f'lounge-{i}-divider-{j}',b)
 # Planted oak top edges anchor each lounge niche without changing the proven divider footprints.
 asset('congress-low-planter.png',bx,1270);asset('congress-low-planter.png',bx+192,1270)
 lowtable(f'lounge-{i}-table',bx+192,1440)
 for k,ax,ay,dr in [('north',bx+208,1376,'south'),('south',bx+208,1504,'north'),('west',bx+112,1440,'east'),('east',bx+304,1440,'west')]:chair(f'lounge-{i}-{k}',[ax,ay],dr,'group',roomid)
# Casual pairs are close enough for default native proximity; no claim of private audio isolation.
for i,cx in enumerate([272,592,912]):
 for j,ax in enumerate([cx-28,cx+28]):chair(f'casual-{i}-{j}',[ax,1600],'north','casual')
 lowtable(f'casual-side-table-{i}',((cx+112)//32)*32,1600)
# Reception and coffee: visible counter matches explicit U footprint; access from broad concourse.
for id,x,txt in [('coffee',192,'COFFEE'),('registration',896,'REGISTRATION')]:
 y=1696;asset('congress-reception.png',x,y);solid(id+'-front',[x,y+32,192,64]);solid(id+'-left-wing',[x,y,32,32]);solid(id+'-right-wing',[x+160,y,32,32]);sign(txt,x+16,y-40,160);landmarks.extend([{'id':id+'-staff','anchor':[x+96,y+8],'floorClick':[x+96,y+24],'kind':'service'},{'id':id+'-customer','anchor':[x+96,y+192],'floorClick':[x+96,y+208],'kind':'service'}])
asset('congress-espresso.png',312,1688);solid('coffee-espresso-base',[320,1696,32,32])
# Planted markers do not obstruct corridors/doors.
for i,(x,y) in enumerate([(352,1056),(1024,1056),(1760,928),(2608,928),(1328,320),(2800,1312),(1152,1728)]):
 asset('congress-olive-planter.png',x,y-48);solid('olive-'+str(i),[((x+16)//32)*32,y,32,32])
sign('SUMMIT',592,1024,208);sign('FORUM',2096,928,224);sign('LAB',1664,1152,128);sign('NETWORKING',240,1160,224);sign('LANTERN CONGRESS',1296,1840,272)
# Small south arrival, no broad silent corridors. WAM start does not own silence.
start=[1440,1888];quiet[58:60,43:47]=1
landmarks += [{'id':'arrival','anchor':start,'floorClick':[1440,1904],'kind':'arrival'},{'id':'cross-concourse','anchor':[1440,1056],'floorClick':[1440,1072],'kind':'route'},{'id':'summit-threshold','anchor':[704,1024],'floorClick':[704,1040],'kind':'route'},{'id':'forum-threshold','anchor':[2192,928],'floorClick':[2192,944],'kind':'route'},{'id':'lab-threshold','anchor':[1552,1536],'floorClick':[1552,1552],'kind':'route'}]
# Explicit level-tread approach/return anchors prove the stage steps are walkable 2D floor.
for rid,x,yt,yb in [('summit',784,384,480),('forum',2256,384,464),('lab',2064,1376,1456)]:
 for suffix,yy,role in [('top',yt,'podium'),('bottom',yb,'audience')]:landmarks.append({'id':rid+'-steps-'+suffix,'anchor':[x,yy],'floorClick':[x,yy+16],'kind':'stage-route','expectedRole':'lantern-'+rid+'-'+role})
# Native roles in feet-coordinate rectangles. Each of three halls has its own independent link.
areas=[]
for id,pod,aud,focus in [('summit',[192,320,1023,127],[160,448,1087,383],[128,160,1152,832]),('forum',[1664,320,1023,95],[1632,432,1087,335],[1600,160,1152,736]),('lab',[1664,1344,1023,95],[1632,1456,1087,383],[1600,1184,1152,704])]:
 pid='lantern-'+id+'-podium';areas.extend([{'id':pid,'name':id.title()+' Podium','x':pod[0],'y':pod[1],'width':pod[2],'height':pod[3],'visible':True,'properties':[{'id':pid+'-broadcast','type':'speakerMegaphone','name':'lantern-'+id,'chatEnabled':False}]},{'id':'lantern-'+id+'-audience','name':id.title()+' Audience','x':aud[0],'y':aud[1],'width':aud[2],'height':aud[3],'visible':True,'properties':[{'id':'lantern-'+id+'-listen','type':'listenerMegaphone','speakerZoneName':pid,'chatEnabled':False}]}])
for room in rooms:
 x,y,w,h=room['rect'];areas.append({'id':room['id'],'name':room['id'].replace('-',' ').title(),'x':x,'y':y,'width':w,'height':h,'visible':True,'properties':[{'id':room['id']+'-call','type':'livekitRoomProperty','roomName':room['id'],'livekitRoomConfig':{'startWithAudioMuted':False,'startWithVideoMuted':False,'disableChat':False}}]})
wam={'version':'2.0.0','mapUrl':'./conference.tmj','entities':{},'entityCollections':[],'areas':areas};jw(O/'conference.wam',wam)
# Derive conservative lower-back ownership from actual native body clearance and all12 head poses.
# Pixels unsafe above a freely walking head remain visually identical below actors.
fg=np.array(above); gregmask=np.array(load('greg-reference.png')); hm=np.zeros((14,32),bool)
for ii in range(12):hm|=gregmask[(ii//3)*32:(ii//3)*32+14,(ii%3)*32:(ii%3+1)*32,3]>32
bodyclear=np.ones((H,W),bool)
for ddy in [0,15]:
 for ddx in [-8,7]:
  ys=np.clip((np.arange(H)+ddy)//32,0,N-1);xs=np.clip((np.arange(W)+ddx)//32,0,C-1);bodyclear &= g[ys[:,None],xs[None,:]]==0
bodyclear[:,:8]=False;bodyclear[:,W-7:]=False;bodyclear[H-15:]=False
headcoverage=np.zeros((H,W),bool)
for hy,hx in zip(*np.where(hm)):
 dy=hy-16;dx=hx-16;sy0=max(0,-dy);sy1=min(H,H-dy);sx0=max(0,-dx);sx1=min(W,W-dx);headcoverage[sy0+dy:sy1+dy,sx0+dx:sx1+dx]|=bodyclear[sy0:sy1,sx0:sx1]
move=headcoverage & (fg[:,:,3]>0);moved=fg.copy();moved[~move]=0;fg[move]=0;base=Image.alpha_composite(base,Image.fromarray(moved));above=Image.fromarray(fg)
jw(S/'foreground-ownership.json',{'method':'Move potentially head-covering pixels below actors, preserving combined artwork exactly','foregroundPixelsRetained':int((fg[:,:,3]>32).sum()),'pixelsMovedBelow':int(move.sum()),'all12NativeHeadMasks':True})
# Preserve complete geometry in a standalone source contract.
jw(S/'layout.json',{'name':'Lantern Congress','world':[W,H],'nativeTile':32,'start':start,'spawnRect':[1408,1888,64,32],'seats':seats,'social':social,'landmarks':landmarks,'solids':solids,'doors':doors,'meetingRooms':rooms,'stageSteps':{'physics':'single permanent2D floor; tread artwork walkable','endCaps':'cropped away to avoid solid-looking posts without collision','routeAnchors':[a['id']for a in landmarks if a['kind']=='stage-route']},'furniture':furniture,'focus':[{'id':'summit','rect':[128,160,1152,832]},{'id':'forum','rect':[1600,160,1152,736]},{'id':'lab','rect':[1600,1184,1152,704]}]})
jw(S/'collision-grid.json',{'tileSize':32,'width':C,'height':N,'start':start,'grid':g.tolist()});jw(S/'quiet-grid.json',{'tileSize':32,'grid':quiet.tolist()});base.save(A/'runtime-base.png');above.save(A/'runtime-above.png')
# Native32 lossless atlas compile; permanent geometry and quiet own their own nonvisual layers.
props=lambda **d:[{'name':k,'type':'bool'if isinstance(v,bool)else'int'if isinstance(v,int)else'float'if isinstance(v,float)else'string','value':v}for k,v in d.items()]
sets=[];layers=[];gid=1;roundtrips=[]
def tl(name,data,opacity=1):return dict(id=0,name=name,type='tilelayer',x=0,y=0,width=C,height=N,visible=True,opacity=opacity,data=list(map(int,data)))
for name,im in [('architecture-furniture',base),('seat-backs',above)]:
 if name=='seat-backs':layers.append(dict(id=0,name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
 ar=np.array(im);ar[ar[:,:,3]==0]=0;im=Image.fromarray(ar);look={};cells=[];data=[]
 for y in range(0,H,32):
  for x in range(0,W,32):
   t=im.crop((x,y,x+32,y+32));b=t.tobytes()
   if not t.getchannel('A').getbbox():data.append(0);continue
   if b not in look:look[b]=len(cells);cells.append(t)
   data.append(gid+look[b])
 restored=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restored.paste(cells[v-gid],((i%C)*32,(i//C)*32))
 assert restored.tobytes()==im.tobytes();roundtrips.append({'name':name,'uniqueTiles':len(cells),'pixelExact':True})
 for page,k in enumerate(range(0,len(cells),1024)):
  part=cells[k:k+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*32,math.ceil(len(part)/cols)*32))
  for j,t in enumerate(part):atlas.paste(t,((j%cols)*32,(j//cols)*32))
  fn=f'{name}-{page}.png';atlas.save(O/fn);sets.append(dict(firstgid=gid+k,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=cols,tilecount=len(part)))
 layers.append(tl(name,data));gid+=len(cells)
Image.new('RGBA',(32,32),(255,0,0,255)).save(O/'collision.png');Image.new('RGBA',(32,32)).save(O/'quiet.png')
sets.append(dict(firstgid=gid,name='collision',image='collision.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1,tiles=[{'id':0,'properties':props(collides=True)}]));layers.insert(1,tl('collision-permanent',[gid if v else 0 for row in g for v in row],0));gid+=1
sets.append(dict(firstgid=gid,name='quiet',image='quiet.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=1,tilecount=1));ql=tl('quiet-arrival-only',[gid if v else 0 for row in quiet for v in row]);ql['properties']=props(silent=True);layers.insert(2,ql)
objs=[dict(id=1,name='start',type='area',x=1408,y=1888,width=64,height=32,rotation=0,visible=True,properties=props(start=True))]
for i,(id,rect) in enumerate([('summit',[128,160,1152,832]),('forum',[1600,160,1152,736]),('lab',[1600,1184,1152,704])],2):objs.append(dict(id=i,name=id+'-presentation-focus',type='area',x=rect[0],y=rect[1],width=rect[2],height=rect[3],rotation=0,visible=True,properties=props(focusable=True,zoomMargin=.15)))
for o in objs:o['class']='area'
layers.append(dict(id=0,name='native-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=objs))
for i,l in enumerate(layers):l['id']=i+1
m=dict(compressionlevel=-1,height=N,width=C,infinite=False,orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=32,tilewidth=32,type='map',version='1.10',nextlayerid=len(layers)+1,nextobjectid=5,backgroundcolor='#233c32',properties=props(name='Lantern Congress / Three Halls',hallSeats=96,groupSeats=8,casualSeats=6),layers=layers,tilesets=sets);jw(O/'conference.tmj',m)
# Native occupied source preview, then a reduced overview clearly marked.
greg=load('greg-reference.png');fr={'north':10,'south':1,'east':7,'west':4};occupied=base.copy()
for r in seats+social:
 ax,ay=r['anchor'];i=fr[r['direction']];occupied.alpha_composite(greg.crop(((i%3)*32,(i//3)*32,(i%3+1)*32,(i//3+1)*32)),(ax-16,ay-16))
for r in landmarks:
 if r['kind']in('speaker','arrival','service'):
  ax,ay=r['anchor'];occupied.alpha_composite(greg.crop((32,0,64,32)),(ax-16,ay-16))
occupied.alpha_composite(above);occupied.save(Q/'occupied-native.png');Image.alpha_composite(base,above).save(Q/'empty-native.png');ov=occupied.resize((1536,1024),Image.Resampling.LANCZOS);board=Image.new('RGB',(1568,1100),'#172d27');bd=ImageDraw.Draw(board);bd.text((16,12),'LANTERN CONGRESS / THREE-HALL CONFERENCE / 50% OVERVIEW',font=font(21,True),fill='#e6d5b4');bd.text((16,43),'96 hall seats · 2 group lounges · 6 casual seats · source-composited occupied view',font=font(15),fill='#c7d4c8');board.paste(ov,(16,70));board.save(Q/'overview.png')
for name,box in [('summit',(480,192,960,608)),('forum',(1632,288,2304,832)),('workshop',(1696,1344,2400,1856)),('networking',(128,1248,1280,1888))]:occupied.crop(box).save(Q/(name+'-occupied-native32.png'))
jw(R/'RUNTIME-MANIFEST.json',{'status':'compiled candidate; route/independent review pending','files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()],'atlasRoundTrips':roundtrips,'quietCells':int(quiet.sum()),'hallSeats':len(seats),'groupSeats':sum(s['kind']=='group'for s in social),'casualSeats':sum(s['kind']=='casual'for s in social),'liveMediaVerified':False})
print(json.dumps({'seats':len(seats),'social':len(social),'quiet':int(quiet.sum()),'openCells':int((g==0).sum())}))
