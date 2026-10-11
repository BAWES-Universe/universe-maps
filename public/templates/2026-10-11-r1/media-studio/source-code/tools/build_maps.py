from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np,json,math,random,hashlib,shutil,zipfile
from collections import deque
R=Path(__file__).resolve().parents[1]; S=R/'source'; T=32
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
jw=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
rgba=lambda p:Image.open(p).convert('RGBA')
def props(**kw):return [dict(name=k,type='bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'float' if isinstance(v,float) else 'string',value=v) for k,v in kw.items()]
def material(name,size):
 src=rgba(S/(name+'-master-native.png')); seams={'deck':[26,53,80,107,135,162,189,216,243,270,297,324,351,378,405,432,459,486,513,540,567,594,621],'stone':[40,88,131,179,224,271,318,367]}[name]
 rng=random.Random(449);out=Image.new('RGBA',size);y=0
 while y<size[1]:
  k=rng.randrange(len(seams)-1);row=src.crop((0,seams[k],src.width,seams[k+1]));off=rng.randrange(src.width);rib=Image.new('RGBA',(size[0]+src.width*2,row.height))
  for x in range(0,rib.width,src.width):rib.paste(row if x//src.width%2==0 else ImageOps.mirror(row),(x,0))
  out.paste(rib.crop((off,0,off+size[0],min(row.height,size[1]-y))),(0,y));y+=row.height
 return out
class Map:
 def __init__(self,slug,title,w,h,category,style):
  self.slug,self.title,self.W,self.H,self.category,self.style=slug,title,w,h,category,style;self.C,self.N=w//32,h//32;self.r=R/slug
  for f in ['map32','source','review','validation','integration']:(self.r/f).mkdir(parents=True,exist_ok=True)
  self.base=Image.new('RGBA',(w,h));self.above=Image.new('RGBA',(w,h));self.grid=np.ones((self.N,self.C),np.uint8);self.quiet=np.zeros_like(self.grid);self.anchors=[];self.areas=[];self.objects=[];self.used=set();self.spawn=(w//2,h-80);self.fixtures=[];self.foreground_candidate=Image.new('L',(w,h))
 def rect(self,box,block=True):
  x,y,x2,y2=box;self.grid[y//32:math.ceil(y2/32),x//32:math.ceil(x2/32)]=int(block)
 def floor(self,box,kind='deck',radius=0):
  x,y,x2,y2=box;mask=Image.new('L',(self.W,self.H));d=ImageDraw.Draw(mask);d.rounded_rectangle((x,y,x2-1,y2-1),radius=radius,fill=255)
  sh=Image.new('RGBA',(self.W,self.H),(6,25,27,110));sh.putalpha(mask.filter(ImageFilter.GaussianBlur(8)));self.base.alpha_composite(sh)
  field=material(kind,(self.W,self.H));self.base.paste(field,(0,0),mask);self.rect(box,False)
  d=ImageDraw.Draw(self.base);d.rounded_rectangle((x+2,y+2,x2-3,y2-3),radius=radius,outline='#947f56',width=3)
 def asset(self,name,x,y,solid=None,scale=None):
  a=rgba(S/(name+'.png'));self.used.add(name+'.png')
  if scale:a=a.resize((round(a.width*scale),round(a.height*scale)),Image.Resampling.LANCZOS)
  self.base.alpha_composite(a,(x,y));self.objects.append(dict(asset=name,xy=[x,y],size=list(a.size),collision=solid))
  if solid:self.rect(solid)
  return a
 def protect(self,name,box):
  self.rect(box);self.fixtures.append(dict(name=name,solidXYXY=box,rule='Whole depicted fixture/edge conservatively protected; not a depth-only substitute'))
 def label(self,text,x,y,w=160):
  d=ImageDraw.Draw(self.base);d.rounded_rectangle((x,y,x+w,y+22),radius=4,fill='#143a3d',outline='#c9ac67',width=1);font=ImageFont.truetype(FB,10);bb=d.textbbox((0,0),text,font=font);d.text((x+(w-bb[2])/2,y+4),text,font=font,fill='#fae9bd')
 def anchor(self,id,x,y,direction='north',kind='social'):
  self.anchors.append(dict(id=id,x=x,y=y,direction=direction,kind=kind))
 def pair(self,id,x,y):
  # Accepted native lounge chair geometry. Anchor y is 17 px before the blocked rear cell.
  self.asset('low-lounge-table',x-32,y-79,solid=(x-32,y-96,x+32,y-64))
  for suffix,xx in [('left',x-28),('right',x+28)]:
   a=rgba(S/'lounge-chair-north.png');self.used.add('lounge-chair-north.png');px,py=xx-24,y-16
   # Small foreground patch never intrudes into a reachable head position.
   top=a.copy();fg=Image.new('RGBA',a.size);ar=np.asarray(a).copy();sel=np.zeros(ar.shape[:2],bool);sel[25:,:]=True
   for yy in range(a.height):
    for xxx in range(a.width):
     if not(xx-8<=px+xxx<xx+8 and y+1<=py+yy<y+33):sel[yy,xxx]=False
   fa=ar.copy();fa[~sel]=0;ba=ar.copy();ba[sel]=0
   self.base.alpha_composite(a,(px,py))
   # Block tile directly behind the chair, preserving the seated body and exit.
   tx=xx//32;ty=(y+17)//32;self.grid[ty,tx]=1;self.anchor(id+'-'+suffix,xx,y)
 def tree(self,x,y):self.asset('citrus-tree',x,y,solid=(x,y,x+64,y+96))
 def garden(self):
  rng=np.random.default_rng(445);noise=rng.normal(0,2,(self.H,self.W));yy,xx=np.indices((self.H,self.W));v=3*np.sin(xx/61)+2*np.cos(yy/43)+noise
  ar=np.empty((self.H,self.W,4),np.uint8)
  for c,base in enumerate([55,91,55]):ar[:,:,c]=np.clip(base+v,0,255)
  ar[:,:,3]=255;self.base=Image.fromarray(ar)
  d=ImageDraw.Draw(self.base);rng=random.Random(312)
  for i in range(self.W*self.H//220):
   x=rng.randrange(self.W);y=rng.randrange(self.H);c=rng.choice(['#537549','#638351','#3d663e']);d.line((x,y,x+2,y-3),fill=c,width=1)
 def pond(self,box):
  x,y,x2,y2=box;w=x2-x;h=y2-y;yy,xx=np.indices((h,w));rng=np.random.default_rng(387);waves=3*np.sin(xx/18+yy/31)+2*np.sin(xx/37-yy/12)+rng.normal(0,.65,(h,w));ar=np.zeros((h,w,4),np.uint8)
  for c,b in enumerate([34,100,108]):ar[:,:,c]=np.clip(b+waves*(1+c*.4),0,255)
  ar[:,:,3]=255;im=Image.fromarray(ar);d=ImageDraw.Draw(im);r=random.Random(919)
  for i in range(w*h//1800):
   xx=r.randrange(w);yy=r.randrange(h);d.arc((xx,yy,xx+r.randrange(12,50),yy+5),0,150,fill=(101,159,159,85),width=1)
  self.base.alpha_composite(im,(x,y))
 def zone(self,id,name,box,purpose):
  x,y,x2,y2=box;self.areas.append(dict(id=id,name=name,x=x,y=y,width=x2-x-1,height=y2-y-1,purpose=purpose))
 def finish(self):
  sx,sy=self.spawn;self.rect((sx//32*32-32,sy//32*32-32,sx//32*32+64,sy//32*32+64),False);self.quiet[sy//32:sy//32+1,sx//32:sx//32+1]=1
  self.partition_foreground()
  self.anchor('spawn',sx,sy,'north','spawn');self.base.save(self.r/'source/runtime-base.png');self.above.save(self.r/'source/runtime-above.png')
  jw(self.r/'source/layout.json',dict(title=self.title,category=self.category,style=self.style,world=[self.W,self.H],start=self.spawn,grid=self.grid.tolist(),quiet=self.quiet.tolist(),anchors=self.anchors,areas=self.areas,objects=self.objects,protectedFixtures=self.fixtures))
  self.compile();self.validate();self.render()
 def partition_foreground(self):
  g=self.grid;blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((self.H,self.W));xa=np.maximum(0,X-8);xb=np.minimum(self.W,X+8);yb=np.minimum(self.H,Y+16);v=ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa];clear=(v==0)&(X>=8)&(X+8<=self.W)&(Y+16<=self.H)
  sp=np.asarray(rgba(S/'greg-reference.png'));head=np.zeros((14,32),bool)
  for r in range(4):
   for c in range(3):head|=sp[r*32:r*32+14,c*32:c*32+32,3]>32
  unsafe=np.zeros((self.H,self.W),bool)
  for yy,xx in np.argwhere(head):
   dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(self.W,self.W-dx);y0=max(0,-dy);y1=min(self.H,self.H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
  candidate=np.asarray(self.foreground_candidate)>32;safe=candidate&~unsafe;original=np.array(self.base);lo=original.copy();hi=np.zeros_like(lo);hi[safe]=lo[safe];lo[safe]=0;self.base=Image.fromarray(lo);self.above=Image.fromarray(hi)
  assert Image.alpha_composite(self.base,self.above).tobytes()==Image.fromarray(original).tobytes()
  jw(self.r/'validation/depth-partition.json',dict(candidatePixels=int(candidate.sum()),foregroundSafePixels=int(safe.sum()),originalCompositeByteExact=True,headSafety='Safe against upper14px union of12 native Greg frames at every body-clear integer position'))
 def compile(self):
  out=self.r/'map32';sets=[];layers=[];gid=1;atlaschecks=[]
  for old in out.iterdir():
   if old.is_file() and old.suffix in ['.png','.tmj','.wam']:old.unlink()
  def layer(name,data,opacity=1):return dict(id=0,name=name,type='tilelayer',width=self.C,height=self.N,x=0,y=0,visible=True,opacity=opacity,data=list(map(int,data)))
  for name,im in [('ground-and-objects',self.base),('foreground',self.above)]:
   if name=='foreground':layers.append(dict(id=0,name='floorLayer',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=[]))
   a=np.array(im);a[a[:,:,3]==0]=0;im=Image.fromarray(a);cells=[];lookup={};data=[]
   for y in range(0,self.H,32):
    for x in range(0,self.W,32):
     t=im.crop((x,y,x+32,y+32));b=t.tobytes()
     if not t.getchannel('A').getbbox():data.append(0);continue
     if b not in lookup:lookup[b]=len(cells);cells.append(t)
     data.append(gid+lookup[b])
   rec=Image.new('RGBA',im.size)
   for i,v in enumerate(data):
    if v:rec.paste(cells[v-gid],((i%self.C)*32,(i//self.C)*32))
   assert rec.tobytes()==im.tobytes()
   for page,start in enumerate(range(0,len(cells),1024)):
    part=cells[start:start+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*32,math.ceil(len(part)/cols)*32))
    for i,t in enumerate(part):atlas.paste(t,((i%cols)*32,(i//cols)*32))
    fn=f'{name}-{page}.png';atlas.save(out/fn);sets.append(dict(firstgid=gid+start,name=fn[:-4],image=fn,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,columns=cols,tilecount=len(part),margin=0,spacing=0))
   layers.append(layer(name,data));atlaschecks.append(dict(layer=name,uniqueTiles=len(cells),pixelExact=True));gid+=len(cells)
  Image.new('RGBA',(32,32)).save(out/'markers.png')
  sets.append(dict(firstgid=gid,name='collision',image='markers.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,margin=0,spacing=0,tiles=[dict(id=0,properties=props(collides=True))]));layers.insert(1,layer('collision-permanent',[gid if v else 0 for v in self.grid.flat],0));gid+=1
  sets.append(dict(firstgid=gid,name='quiet',image='markers.png',imagewidth=32,imageheight=32,tilewidth=32,tileheight=32,columns=1,tilecount=1,margin=0,spacing=0));l=layer('silent-spawn-only',[gid if v else 0 for v in self.quiet.flat]);l['properties']=props(silent=True);layers.insert(2,l)
  sx,sy=self.spawn;areas=[dict(id=1,name='start',type='area',**{'class':'area'},x=sx-16,y=sy-16,width=32,height=32,rotation=0,visible=True,properties=props(start=True))]
  for i,a in enumerate(self.areas):areas.append(dict(id=i+2,name=a['id'],type='area',**{'class':'area'},x=a['x'],y=a['y'],width=a['width'],height=a['height'],rotation=0,visible=True,properties=props(editorLabel=a['name'],setupStatus='Unconfigured editor-ready area',purpose=a['purpose'])))
  layers.append(dict(id=0,name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=areas))
  for i,l in enumerate(layers):l['id']=i+1
  m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=self.C,height=self.N,tilewidth=32,tileheight=32,nextlayerid=len(layers)+1,nextobjectid=len(areas)+1,layers=layers,tilesets=sets,properties=props(name=self.title,wokaScale=1,status='Local template; live playtest and service configuration pending'))
  jw(out/(self.slug+'.tmj'),m)
  wamAreas=[dict(id=self.slug+'-spawn',name='Safe arrival',x=sx-4,y=sy-4,width=8,height=8,visible=True,properties=[dict(id=self.slug+'-default-start',type='start',isDefault=True)])]
  for a in self.areas:wamAreas.append(dict(id=a['id'],name=a['name'],x=a['x'],y=a['y'],width=a['width'],height=a['height'],visible=True,properties=[]))
  jw(out/(self.slug+'.wam'),dict(version='2.0.0',mapUrl='./'+self.slug+'.tmj',entities={},entityCollections=[],areas=wamAreas))
  jw(self.r/'validation/atlas-roundtrip.json',atlaschecks)
 def validate(self):
  g=self.grid;reach=np.zeros_like(g,bool);q=deque([(self.spawn[0]//32,self.spawn[1]//32)])
  while q:
   x,y=q.popleft()
   if not(0<=x<self.C and 0<=y<self.N) or g[y,x] or reach[y,x]:continue
   reach[y,x]=True;q.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
  blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((self.H,self.W));xa=np.maximum(0,X-8);xb=np.minimum(self.W,X+8);yb=np.minimum(self.H,Y+16);v=ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa];clear=(v==0)&(X>=8)&(X+8<=self.W)&(Y+16<=self.H)&reach[Y//32,X//32]
  greg=np.asarray(rgba(S/'greg-reference.png'));head=np.zeros((14,32),bool)
  for r in range(4):
   for c in range(3):head|=greg[r*32:r*32+14,c*32:c*32+32,3]>32
  fg=np.asarray(self.above)[:,:,3]>32;danger=np.zeros((self.H,self.W),bool)
  for yy,xx in np.argwhere(head):
   dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(self.W,self.W-dx);y0=max(0,-dy);y1=min(self.H,self.H-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
  badanchors=[]
  for a in self.anchors:
   x,y=a['x'],a['y'];a['bodyClear']=bool(clear[y,x]);a['headClear']=not bool(danger[y,x]);a['reachable']=bool(reach[y//32,x//32]);a['silent']=bool(self.quiet[y//32,x//32])
   if not a['bodyClear'] or not a['headClear'] or not a['reachable'] or (a['kind']=='social' and a['silent']):badanchors.append(a)
  report=dict(scope='Static native32 geometry: exhaustive integer body positions, union of all 12 Greg upper-head masks, cardinal tile connectivity. Not live gameplay or engine route replay.',walkableCells=int((g==0).sum()),reachableCells=int(reach.sum()),unreachableCells=int(((g==0)&~reach).sum()),safeBodyPlacements=int(clear.sum()),headConflicts=int((clear&danger).sum()),anchorCount=len(self.anchors),badAnchors=badanchors,quietCells=int(self.quiet.sum()),allPass=not badanchors and not (clear&danger).any() and not ((g==0)&~reach).any(),anchors=self.anchors)
  jw(self.r/'validation/geometry.json',report);print(self.slug,{k:v for k,v in report.items() if k not in ['anchors','scope']})
 def render(self):
  m=json.loads((self.r/'map32'/(self.slug+'.tmj')).read_text());sets=[]
  for ts in m['tilesets']:sets.append((ts,rgba(self.r/'map32'/ts['image'])))
  under=Image.new('RGBA',(self.W,self.H));over=Image.new('RGBA',(self.W,self.H));dest=under
  for l in m['layers']:
   if l['name']=='floorLayer':dest=over
   if l['type']!='tilelayer' or l['opacity']==0:continue
   for i,gid in enumerate(l['data']):
    if not gid:continue
    ts,im=max((t for t in sets if t[0]['firstgid']<=gid),key=lambda t:t[0]['firstgid']);j=gid-ts['firstgid'];x=j%ts['columns']*32;y=j//ts['columns']*32;dest.alpha_composite(im.crop((x,y,x+32,y+32)),((i%self.C)*32,(i//self.C)*32))
  empty=under.copy();empty.alpha_composite(over);empty.save(self.r/'review/empty-native.png');occ=under.copy();greg=rgba(S/'greg-reference.png');dirs={'north':10,'south':1,'west':4,'east':7}
  for a in self.anchors:
   if a['kind']=='social' or a['id']=='spawn':
    f=dirs[a['direction']];occ.alpha_composite(greg.crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32)),(a['x']-16,a['y']-16))
  occ.alpha_composite(over);occ.save(self.r/'review/occupied-native.png')
  overlay=empty.copy();sh=Image.new('RGBA',overlay.size);d=ImageDraw.Draw(sh)
  for y,x in np.argwhere(self.grid):d.rectangle((int(x)*32,int(y)*32,int(x)*32+31,int(y)*32+31),fill=(210,35,70,70))
  for a in self.anchors:d.ellipse((a['x']-3,a['y']-3,a['x']+3,a['y']+3),fill='#42ffc2')
  overlay.alpha_composite(sh);overlay.save(self.r/'review/collision-native.png')
  card=Image.new('RGB',(self.W+64,self.H+160),'#142e32');card.paste(occ,(32,100),occ);d=ImageDraw.Draw(card);d.text((32,22),self.title.upper(),font=ImageFont.truetype(FB,24),fill='#f5d799');d.text((32,60),self.category+'  /  '+self.style,font=ImageFont.truetype(F,15),fill='#c0d5ca');d.text((32,self.H+122),'Compiled native32 occupied render • Static source proof; live room testing pending',font=ImageFont.truetype(F,14),fill='#c0d5ca');card.save(self.r/'review/overview.png')
def cafe():
 m=Map('willow-quay-tea-garden','Willow Quay Tea Garden',1536,1024,'Social / café','Lush pond pavilion, curved timber quay and flowering garden patios')
 m.base=rgba(S/'tea-garden-clear-landing-master.png');m.used.add('tea-garden-clear-landing-master.png')
 mask=Image.new('L',(m.W,m.H));d=ImageDraw.Draw(mask)
 d.polygon([(160,136),(608,136),(624,288),(600,320),(512,320),(480,360),(288,360),(256,320),(160,280)],fill=255)
 d.rectangle((288,288,480,416),fill=255)
 d.polygon([(704,152),(736,160),(752,200),(784,224),(896,224),(960,248),(1088,264),(1120,288),(1120,352),(1184,368),(1248,400),(1280,448),(1248,512),(1120,512),(1088,464),(1024,416),(960,400),(928,416),(832,416),(800,384),(768,384),(736,448),(640,480),(544,480),(512,448),(512,400),(640,368),(704,352)],fill=255)
 d.line([(416,432),(560,432)],fill=255,width=96)
 d.line([(392,384),(400,456),(424,536),(488,600),(576,656),(656,704),(680,784),(700,880)],fill=255,width=96,joint='curve')
 d.line([(220,592),(240,660),(300,708),(432,752),(480,816),(568,888)],fill=255,width=80,joint='curve')
 for x,y,r in [(224,592,78),(432,752,82),(696,906,155)]:d.ellipse((x-r,y-r,x+r,y+r),fill=255)
 d.rectangle((560,944,832,1023),fill=255)
 d.line([(1104,288),(1176,264),(1232,240),(1304,224),(1360,184)],fill=255,width=64,joint='curve')
 d.ellipse((1304,104,1440,240),fill=255)
 d.line([(1120,264),(1184,240),(1248,208),(1312,176),(1376,160)],fill=255,width=64,joint='curve')
 pix=np.asarray(mask)>0
 for y in range(m.N):
  for x in range(m.C):m.grid[y,x]=0 if pix[y*32:(y+1)*32,x*32:(x+1)*32].mean()>.63 else 1
 mask.save(m.r/'source/authored-walkable-mask.png')
 for name,box in [('pavilion-west-furnishings',(128,128,192,288)),('pavilion-north-counter',(256,32,576,144)),('pavilion-east-wall',(608,64,704,352)),('stairs-left-flowers',(240,288,320,384)),('stairs-right-flowers',(480,288,544,384)),('quay-west-entry-lamp',(480,416,544,512)),('quay-north-post',(768,160,832,224)),('quay-north-planter',(928,192,992,256)),('quay-south-lamp',(928,352,1024,448)),('east-quay-lamp',(1248,352,1312,448)),('bridge-west-north-lamp',(1088,192,1152,256)),('bridge-north-rail-low',(1152,224,1184,256)),('bridge-north-rail-high',(1216,192,1248,224)),('garden-path-west-lamp',(384,576,448,672)),('arrival-northwest-lamp',(576,704,640,832)),('arrival-northeast-lamp',(768,704,832,832)),('arrival-west-planter',(480,880,576,992)),('arrival-east-planter',(800,880,896,992))]:m.protect(name,box)
 m.pair('pavilion-west',304,239);m.pair('pavilion-east',496,239);m.pair('quay',880,335);m.pair('water-view',1184,463);m.anchor('gazebo-west',1360,143);m.anchor('gazebo-east',1392,143);m.pair('rose-patio',224,623);m.pair('jasmine-patio',432,783)
 m.label('TEA PAVILION',320,16,160);m.label('WILLOW QUAY',960,914,160)
 m.anchor('tea-counter-front',416,207,'north','landmark');m.anchor('bridge-entry',1168,271,'east','landmark');m.anchor('garden-junction',560,655,'north','landmark')
 m.zone('pavilion-social','Tea pavilion',(160,144,624,320),'Social proximity space; no ordering or payment integration')
 m.zone('rose-patio','Rose conversation patio',(160,544,288,656),'Social proximity pair; no acoustic isolation')
 m.zone('gazebo-social','Waterside gazebo',(1312,128,1440,240),'Social proximity pair; no acoustic isolation')
 m.spawn=(688,975);m.finish();return m


def mask_grid(m,mask,threshold=.63):
 pix=np.asarray(mask)>0
 for y in range(m.N):
  for x in range(m.C):m.grid[y,x]=0 if pix[y*32:(y+1)*32,x*32:(x+1)*32].mean()>threshold else 1
 mask.save(m.r/'source/authored-walkable-mask.png')
def bazaar():
 m=Map('lantern-souk-bazaar','Lantern Souk Bazaar',1536,1024,'Event / social commerce','Lantern-lit Arabian stalls, fountain ring and seller demo courts')
 m.base=rgba(S/'bazaar-environment-safe-ring-master.png');m.used.add('bazaar-environment-safe-ring-master.png');mask=Image.new('L',(m.W,m.H));d=ImageDraw.Draw(mask)
 for b in [(384,208,1152,304),(384,272,560,672),(976,272,1152,672),(384,608,1152,704),(672,768,864,1024),(624,704,912,800),(288,176,544,224),(688,160,896,224),(1024,176,1216,224),(144,368,384,432),(144,592,384,656),(1152,368,1408,432),(1152,592,1408,656),(128,816,448,896),(1088,816,1408,896)]:d.rectangle(b,fill=255)
 d.polygon([(384,672),(512,672),(640,736),(640,784),(448,768),(448,864),(384,864)],fill=255)
 d.polygon([(1024,672),(1152,672),(1152,864),(1088,864),(1088,768),(896,784),(896,736)],fill=255)
 d.rectangle((320,352,416,384),fill=255);d.rectangle((1120,352,1216,384),fill=255)
 d.rectangle((352,736,448,864),fill=255);d.rectangle((1088,736,1184,864),fill=255)
 mask_grid(m,mask)
 # The fountain, raised planting and market furniture are permanent solid scenery.
 for b in [(576,288,960,608),(352,256,384,320),(352,384,384,416),(1152,256,1184,320),(1152,384,1184,416)]:m.rect(b)
 for name,box in [('entry-west-turret',(640,768,704,960)),('entry-east-turret',(832,768,896,960)),('fountain-and-raised-garden',(576,256,960,608)),('west-high-lantern',(352,240,384,320)),('east-high-lantern',(1152,240,1184,320))]:m.protect(name,box)
 m.pair('fountain-social',768,687)
 stalls=[('tea-spices','TEA & SPICES',432,207,(320,176,544,224)),('ceramics','CERAMICS',784,191,(688,160,896,224)),('textiles','TEXTILES',1104,207,(1024,176,1216,224)),('artisan-west','ARTISAN GOODS',240,399,(144,368,352,432)),('bookshop','BOOKS',240,623,(144,592,352,656)),('bot-display','BOT DISPLAY • SETUP',1296,399,(1184,368,1408,432)),('fabric-east','DESIGN GOODS',1296,623,(1184,592,1408,656))]
 for id,name,x,y,box in stalls:
  m.anchor(id+'-customer',x,y,'north','social');m.zone(id,name,box,'Seller/demo approach placeholder; no payment, bot, checkout or external website configured')
 # Two genuinely separate seller demonstration rooms have edited, visible north-side passages.
 for id,x in [('seller-demo-west',288),('seller-demo-east',1248)]:
  m.anchor(id+'-host',x,847,'south','social');m.anchor(id+'-visitor',x+48,879,'north','social');m.zone(id,'Seller demo / configure service',(x-96,816,x+96,896),'Unconfigured seller demo room; service integration and privacy require explicit setup')
 m.label('SELLER DEMO • SETUP',208,770,176);m.label('SELLER DEMO • SETUP',1184,770,176);m.label('LANTERN SOUK',688,24,160)
 for id,x,y in [('west-ring',464,495),('east-ring',1072,495),('north-ring',752,239),('south-ring',768,751),('west-demo-door',400,751),('east-demo-door',1136,751)]:m.anchor(id,x,y,'north','landmark')
 m.spawn=(784,975);m.finish();return m

def media():
 m=Map('resonance-media-house','Resonance Media House',1536,1024,'Sandbox / media creation','Walnut studio workshop, preview salon and acoustic recording spaces')
 m.base=rgba(S/'media-environment-clean-seats-master.png');m.used.add('media-environment-clean-seats-master.png');mask=Image.new('L',(m.W,m.H));d=ImageDraw.Draw(mask)
 for b in [(160,192,880,384),(640,320,880,800),(688,800,848,1024),(128,544,544,768),(544,528,688,608),(960,528,1408,768),(880,528,1024,608),(960,160,1344,288),(944,240,1408,368),(848,240,1008,288)]:d.rectangle(b,fill=255)
 mask_grid(m,mask)
 # Console fronts, microphone and reception joinery remain fixed collision.
 m.rect((1120,128,1216,224));m.rect((1120,288,1184,352));m.rect((928,704,1088,800))
 def task_chair(id,x,y):
  art=rgba(S/'industrial-chair40-native.png');m.used.add('industrial-chair40-native.png');m.base.alpha_composite(art,(x-20,y-24));m.grid[(y+17)//32,x//32]=1;m.anchor(id,x,y)
  ca=Image.new('L',art.size);alpha=np.asarray(art)[:,:,3];arr=np.zeros_like(alpha);arr[23:39,6:34]=alpha[23:39,6:34];m.foreground_candidate.paste(Image.fromarray(arr),(x-20,y-24))
 def contemporary_pair(id,x,y):
  m.asset('congress-low-table',x-40,y-79,solid=(x-40,y-79,x+40,y-33));task_chair(id+'-left',x-28,y);task_chair(id+'-right',x+28,y)
 for i,x in enumerate([272,528,752]):task_chair('editor-'+str(i+1),x,207)
 contemporary_pair('preview-west',268,655);contemporary_pair('preview-east',460,655);contemporary_pair('music-listening',1228,655)
 m.anchor('recording-mic',1232,239,'west','social');m.anchor('music-keyboard-1',1088,559,'north','social');m.anchor('music-keyboard-2',1312,559,'north','social');m.anchor('studio-host',768,559,'south','social')
 zones=[('imagine-editor','Imagine / editor-ready',(160,192,864,352),'Unconfigured creative editor area; no Imagine backend, account, generation or export integration'),('voice-recording','Voice recording / setup',(976,160,1344,288),'Recording-themed map zone only; no recording or live media capture'),('imagine-music','ImagineMusic / editor-ready',(1008,528,1408,768),'Unconfigured music editor area; no ImagineMusic backend, synthesis or streaming'),('preview-room','Preview room / setup',(128,544,544,768),'Blank preview screen; media source and access require room configuration')]
 for args in zones:m.zone(*args)
 m.label('IMAGINE • EDITOR SETUP',384,28,240);m.label('VOICE • SETUP',1104,32,160);m.label('PREVIEW • SETUP',240,416,192);m.label('IMAGINEMUSIC • SETUP',1104,408,240)
 for id,x,y in [('preview-door',608,559),('music-door',912,559),('recording-door',912,271),('lobby',768,815)]:m.anchor(id,x,y,'north','landmark')
 for name,box in [('recording-microphone',(1120,96,1216,224)),('recording-corridor-planter',(1120,288,1184,352)),('preview-east-north-jamb',(576,384,640,528)),('preview-east-south-jamb',(544,608,640,800)),('music-west-north-jamb',(880,384,960,528)),('music-west-south-jamb',(880,608,1088,800)),('arrival-west-open-door',(624,784,704,928)),('arrival-east-open-door',(832,784,928,928))]:m.protect(name,box)
 m.spawn=(784,975);m.finish();return m

def portal():
 m=Map('celestial-transit-garden','Celestial Transit Garden',1536,1024,'Portal / destination hub','Moonlit radial courtyard, five configurable destination alcoves')
 m.base=rgba(S/'portal-environment-garden-boundaries-master.png');m.used.add('portal-environment-garden-boundaries-master.png');mask=Image.new('L',(m.W,m.H));d=ImageDraw.Draw(mask)
 d.ellipse((544,304,992,576),fill=255)
 d.rectangle((720,176,816,960),fill=255);d.rectangle((656,928,880,1024),fill=255);d.ellipse((688,768,848,928),fill=255)
 for a,b in [((352,272),(592,384)),((1184,272),(944,384)),((320,656),(592,496)),((1216,656),(944,496))]:d.line([a,b],fill=255,width=96,joint='curve')
 for b in [(688,160,848,240),(272,224,432,320),(1104,224,1264,320),(224,608,416,704),(1104,608,1312,704)]:d.ellipse(b,fill=255)
 # Outer rear strips are visibly planted; broad inner garden arcs remain accessible.
 for b in [(544,160,608,224),(608,192,640,256),(640,224,704,256),(672,256,736,288),(928,160,992,224),(896,192,928,256),(832,224,896,256),(800,256,864,288)]:d.rectangle(b,fill=255)
 # Lower garden paths are hand-traced around planting and portal bases.
 for pts in [[(240,672),(336,720),(464,752),(560,752),(640,768),(736,800)],[(1280,672),(1184,720),(1056,752),(960,752),(880,768),(800,800)]]:d.line(pts,fill=255,width=64,joint='curve')
 mask_grid(m,mask,.56)
 # Portal architecture is solid; only the visible aprons are configurable destination targets.
 for b in [(672,0,864,160),(224,80,384,224),(1120,80,1312,224),(176,448,352,608),(1168,448,1344,608)]:m.rect(b)
 for name,box in [('rotunda-west-raised-bed',(448,384,576,448)),('rotunda-east-raised-bed',(960,384,1088,448)),('lower-west-raised-garden',(480,800,672,896)),('lower-east-raised-garden',(864,800,1056,896)),('arrival-west-vase',(624,880,704,976)),('arrival-east-vase',(832,880,912,976)),('north-west-arch-planter',(640,96,704,192)),('north-east-arch-planter',(832,96,896,192)),('northwest-arch-left-foot',(224,192,288,288)),('northwest-arch-right-planter',(384,192,448,256)),('northeast-arch-left-planter',(1088,192,1152,256)),('northeast-arch-right-foot',(1248,192,1312,288)),('southwest-arch-left-foot',(176,544,256,656)),('southwest-arch-right-planter',(352,544,448,640)),('southeast-arch-left-planter',(1088,544,1184,640)),('southeast-arch-right-foot',(1280,544,1360,656))]:m.protect(name,box)
 destinations=[('destination-north','DESTINATION 01',768,207,(720,176,816,240)),('destination-northwest','DESTINATION 02',352,287,(288,256,416,320)),('destination-northeast','DESTINATION 03',1184,287,(1120,256,1248,320)),('destination-southwest','DESTINATION 04',320,655,(256,624,384,688)),('destination-southeast','DESTINATION 05',1216,655,(1152,624,1280,688))]
 for id,label,x,y,box in destinations:
  m.anchor(id,x,y,'north','social');m.zone(id,label+' / unconfigured',box,'Destination not configured. No exitUrl, teleport, website or external service is enabled.')
 # Labels attached to blocked arch fronts; all text is explicit that destinations need setup.
 for text,x,y in [('01 • SET DESTINATION',688,112),('02 • SET DESTINATION',240,176),('03 • SET DESTINATION',1136,176),('04 • SET DESTINATION',192,560),('05 • SET DESTINATION',1184,560)]:m.label(text,x,y,160)
 m.anchor('central-compass',768,431,'south','social');m.anchor('west-spoke',528,335,'east','landmark');m.anchor('east-spoke',1008,335,'west','landmark');m.anchor('south-spoke',768,687,'north','landmark')
 m.anchor('northwest-garden-lookout',576,191,'north','landmark');m.anchor('northeast-garden-lookout',960,191,'north','landmark')
 m.spawn=(784,975);m.finish();return m

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--map',default='willow-quay-tea-garden');a=ap.parse_args()
 {'willow-quay-tea-garden':cafe,'lantern-souk-bazaar':bazaar,'resonance-media-house':media,'celestial-transit-garden':portal}[a.map]()
