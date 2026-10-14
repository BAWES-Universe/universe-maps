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
  sx,sy=self.spawn;self.quiet[sy//32:sy//32+1,sx//32:sx//32+1]=1
  self.partition_foreground()
  self.anchor('spawn',sx,sy,'north','spawn');self.base.save(self.r/'source/runtime-base.png');self.above.save(self.r/'source/runtime-above.png')
  jw(self.r/'source/layout.json',dict(title=self.title,category=self.category,style=self.style,world=[self.W,self.H],start=self.spawn,grid=self.grid.tolist(),quiet=self.quiet.tolist(),anchors=self.anchors,areas=self.areas,objects=self.objects,protectedFixtures=self.fixtures))
  self.compile();self.validate();self.render()
 def partition_foreground(self):
  g=self.grid;blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices((self.H,self.W));xa=np.maximum(0,X-8);xb=np.minimum(self.W,X+8);yb=np.minimum(self.H,Y+16);v=ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa];clear=(v==0)&(X>=8)&(X+8<=self.W)&(Y+16<=self.H)
  sp=np.asarray(rgba(S/'greg-reference.png'));head=np.zeros((14,32),bool)
  for r in range(4):
   for c in range(3):head|=sp[r*32:r*32+14,c*32:c*32+32,3]>32
  head=np.array(json.loads((S/'head-union.json').read_text()),bool)
  unsafe=np.zeros((self.H,self.W),bool)
  for yy,xx in np.argwhere(head):
   dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(self.W,self.W-dx);y0=max(0,-dy);y1=min(self.H,self.H-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
  candidate=np.asarray(self.foreground_candidate)>32;safe=candidate&~unsafe;original=np.array(self.base);lo=original.copy();hi=np.zeros_like(lo);hi[safe]=lo[safe];lo[safe]=0;self.base=Image.fromarray(lo);self.above=Image.fromarray(hi)
  assert Image.alpha_composite(self.base,self.above).tobytes()==Image.fromarray(original).tobytes()
  jw(self.r/'validation/depth-partition.json',dict(candidatePixels=int(candidate.sum()),foregroundSafePixels=int(safe.sum()),originalCompositeByteExact=True,headSafety='Safe against upper14px union of40 native Woka frames at every body-clear integer position'))
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
  sx,sy=self.spawn;areas=[dict(id=1,name='start',type='area',**{'class':'area'},x=sx-16,y=sy-16,width=31,height=31,rotation=0,visible=True,properties=props(start=True))]
  for i,a in enumerate(self.areas):areas.append(dict(id=i+2,name=a['id'],type='area',**{'class':'area'},x=a['x'],y=a['y'],width=a['width'],height=a['height'],rotation=0,visible=True,properties=props(editorLabel=a['name'],setupStatus='Unconfigured editor-ready area',purpose=a['purpose'])))
  layers.append(dict(id=0,name='map-areas',type='objectgroup',x=0,y=0,visible=True,opacity=1,draworder='topdown',objects=areas))
  for i,l in enumerate(layers):l['id']=i+1
  m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=self.C,height=self.N,tilewidth=32,tileheight=32,nextlayerid=len(layers)+1,nextobjectid=len(areas)+1,layers=layers,tilesets=sets,properties=props(name=self.title,wokaScale=1,status='Local template; live playtest and service configuration pending'))
  jw(out/(self.slug+'.tmj'),m)
  wamAreas=[]
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
  head=np.array(json.loads((S/'head-union.json').read_text()),bool)
  fg=np.asarray(self.above)[:,:,3]>32;danger=np.zeros((self.H,self.W),bool)
  for yy,xx in np.argwhere(head):
   dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(self.W,self.W-dx);y0=max(0,-dy);y1=min(self.H,self.H-dy);danger[y0:y1,x0:x1]|=fg[y0+dy:y1+dy,x0+dx:x1+dx]
  badanchors=[]
  for a in self.anchors:
   x,y=a['x'],a['y'];a['bodyClear']=bool(clear[y,x]);a['headClear']=not bool(danger[y,x]);a['reachable']=bool(reach[y//32,x//32]);a['silent']=bool(self.quiet[y//32,x//32])
   if not a['bodyClear'] or not a['headClear'] or not a['reachable'] or (a['kind']=='social' and a['silent']):badanchors.append(a)
  report=dict(scope='Static native32 geometry: exhaustive integer body positions, union of40 actual native Woka idle upper-head masks, cardinal tile connectivity. Not live gameplay or engine route replay.',walkableCells=int((g==0).sum()),reachableCells=int(reach.sum()),unreachableCells=int(((g==0)&~reach).sum()),safeBodyPlacements=int(clear.sum()),headConflicts=int((clear&danger).sum()),anchorCount=len(self.anchors),badAnchors=badanchors,quietCells=int(self.quiet.sum()),allPass=not badanchors and not (clear&danger).any() and not ((g==0)&~reach).any(),anchors=self.anchors)
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
