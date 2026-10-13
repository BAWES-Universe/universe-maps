"""Revision08: native reconstruction from preserved lush sources. No source resampling."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R/'sources';OFF=R.parent/'office-work';W,H,CELL=2944,2624,8
read=lambda p:json.loads(Path(p).read_text())
write=lambda p,d:Path(p).write_text(json.dumps(d,indent=2)+'\n')
props=lambda **kw:[{'name':k,'type':'bool'if isinstance(v,bool)else'int'if isinstance(v,int)else'string','value':v}for k,v in kw.items()]
for folder in ['layers','docs','map','map16','sources/office08']:(R/folder).mkdir(exist_ok=True)
can={n:Image.new('RGBA',(W,H))for n in ['base','foreground','glass','shade']};grid=np.ones((H//8,W//8),np.uint8);audit=[];mods=[];joins=[]
def place(p,name,origin,crop=None):
 im=Image.open(p).convert('RGBA');box=crop or(0,0,*im.size);im=im.crop(box);at=(origin[0]+box[0],origin[1]+box[1]);can[name].alpha_composite(im,at)
 audit.append({'source':str(p.relative_to(R)),'target':name,'origin':origin,'crop':box,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
def gridplace(a,origin,crop=None):
 x,y=origin;hh,ww=a.shape
 if crop:
  l,t,r,b=crop;a=a[t//8:b//8,l//8:r//8];x+=l;y+=t;hh,ww=a.shape
 assert x%8==y%8==0 and x>=0 and y>=0 and x+ww*8<=W and y+hh*8<=H
 grid[y//8:y//8+hh,x//8:x//8+ww]=a

def mask(size,polys,obs):
 im=Image.new('1',size);d=ImageDraw.Draw(im)
 for poly in polys:d.polygon([tuple(p)for p in poly],fill=1)
 for o in obs:
  t=o.get('type','rect')
  if t=='rect':d.rectangle((o['x'],o['y'],o['x']+o['width']-1,o['y']+o['height']-1),fill=0)
  elif t=='polygon':d.polygon([tuple(p)for p in o['points']],fill=0)
  else:
   x=o.get('cx',o.get('x'));y=o.get('cy',o.get('y'));rx=o.get('rx',o.get('radius'));ry=o.get('ry',o.get('radius'));d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=0)
 return 1-np.asarray(im,np.uint8).reshape(size[1]//8,8,size[0]//8,8).min((1,3))
def module(name,origin,size,crop=None):mods.append({'id':name,'origin':origin,'size':size,'crop':crop,'scale':1})
# Recovered foundation planting fills only old scene gaps; it is an underlay.
p=S/'joins/garden-foundation-joins.png';im=Image.open(p).convert('RGBA').crop((256,656,3200,3072));can['base'].alpha_composite(im,(0,0))
# Preserved native foliage closes only nonwalkable source gaps. It does not open a single collision cell.
terrain=S/'terrain08/terrain-underlay-native.png'
if terrain.exists():place(terrain,'base',(0,0))
# Original west garden, shortened only at the lower margin to meet the civic building.
o=(0,0);m=read(S/'west-garden/module.json');crop=(0,0,512,1136)
for f,t in [('west-base.png','base'),('west-canopy.png','foreground')]:place(S/'west-garden'/f,t,o,crop)
gridplace(mask((512,1536),m['walkablePolygons'],m['obstacles']),o,crop);module('west-garden',o,[512,1136])
# Civic interior remains exactly native size and geometry.
o=(0,1136);m=read(S/'civic/module.json')
for f,t in [('architecture','base'),('furniture','base'),('foreground','foreground'),('glass','glass'),('shadow','shade')]:place(S/f'civic/{f}-native.png',t,o)
polys=[[[64,144],[576,144],[576,1088],[64,1088]],[[576,344],[640,344],[640,424],[576,424]],[[576,952],[640,952],[640,1032],[576,1032]]]
gridplace(mask((640,1152),polys,m['blockers']),o);module('civic',o,[640,1152])
# Court and avenue retain the entire fountain ring; only unused far-left planting is cropped.
o=(448,1120);m=read(S/'court/module.json');crop=(192,0,1472,704)
for f,t in [('court-base.png','base'),('court-canopy.png','foreground')]:place(S/'court'/f,t,o,crop)
a=mask((1472,704),m['walkablePolygons'],m['obstacles'])
for x,y in [(41,16),(40,17)]:a[y*2:y*2+2,x*2:x*2+2]=0
assert a[18*2:18*2+2,40*2:40*2+2].any(),'retain real planter'
gridplace(a,o,crop);module('court',o,[1472,704],crop)
o=(448,1824);m=read(S/'avenue/avenue-manifest.json');crop=(192,0,1472,576)
for f,t in [('avenue-base.png','base'),('avenue-foliage-foreground.png','foreground')]:place(S/'avenue'/f,t,o,crop)
gridplace(mask((1472,576),m['walkable'],m['obstacles']),o,crop);module('avenue',o,[1472,576],crop)
# The approved firepit, water and four permanent bench positions are preserved.
o=(1920,1264);m=read(S/'garden/collision-grid-8px.json')
for f,t in [('garden-base.png','base'),('bench-and-foliage-fixed-foreground.png','foreground')]:place(S/'garden'/f,t,o)
gridplace(np.array(m['blocked'],np.uint8).reshape(m['height'],m['width']),o);module('garden',o,[1024,1024])
# Eight ordinary work seats, two service positions; no floor labels.
o=(704,64)
for f,t in [('office-base.png','base'),('office-foreground.png','foreground'),('office-glass.png','glass'),('office-overhead-shade.png','shade')]:
 dst=S/'office08'/f;shutil.copy2(OFF/f,dst);place(dst,t,o)
for f in ['collision-grid.json','module.json','anchors.json','routes.json','compositing-manifest.json']:shutil.copy2(OFF/f,S/'office08'/f)
m=read(S/'office08/collision-grid.json');a=np.ones((m['height'],m['width']),np.uint8)
if 'blockedIndices'in m:a.fill(0);a.flat[m['blockedIndices']]=1
elif 'blocked'in m:a=np.array(m['blocked'],np.uint8).reshape(m['height'],m['width'])
else:raise ValueError(m.keys())
gridplace(a.repeat(m['cellSize']//8,0).repeat(m['cellSize']//8,1),o);module('office08',o,[1536,960])
# Market below the fire garden. Original shop fronts, permanently corrected duplicate fascia.
o=(1824,1968);m=read(S/'market/module.json');place(S/'market/market-base.png','base',o)
fg=Image.open(S/'market/market-canopy.png').convert('RGBA')
for x in [208,416]:fg.paste((0,0,0,0),(x,160,x+144,176))
p=S/'market/market-canopy-fixed.png';fg.save(p);place(p,'foreground',o)
gridplace(mask((768,320),m['walkablePolygons'],m['obstacles']),o);module('market',o,[768,320])
# Small native paving receivers. Every opened cell is visible paving, never foliage.
market=Image.open(S/'market/market-base.png').convert('RGBA');court=Image.open(S/'court/court-base.png').convert('RGBA')
def openrect(x,y,w,h):
 assert all(v%8==0 for v in [x,y,w,h]);grid[y//8:(y+h)//8,x//8:(x+w)//8]=0

def connector(name,im,at,rects,src):
 can['base'].alpha_composite(im,at)
 for x,y,w,h in rects:openrect(x,y,w,h)
 joins.append({'id':name,'origin':at,'size':im.size,'source':src,'openRects':rects})
# A short front promenade links the obvious main entrance and separate meeting door.
for x in range(416,1920,704):
 n=min(704,1920-x);connector('office-front-'+str(x),market.crop((0,224,n,320)),(x,1024),[(x,1024,n,96)],'market floor, excludes columns')
for x in [1184,1792]:connector('office-threshold-'+str(x),court.crop((736,520,864,552)),(x,992),[(x,992,128,32)],'court clear vertical paving')
# Main court threshold is96px wide; preserve its actual stone posts.
connector('office-court-porch',court.crop((752,520,848,616)),(1200,1024),[(1200,1024,96,96)],'court vertical paving')
connector('classroom-cloister',court.crop((752,376,784,504)),(608,1480),[(608,1488,32,120)],'court clear paving outside fountain artwork')
connector('stage-cloister',court.crop((48,396,144,492)),(608,2080),[(608,2088,96,80)],'court clear horizontal paving')
# The civic approach joins the original east-west court path. No strip is painted over its west bench or garden wall.
# Shore path continues to a small market forecourt; no hidden stall-wall entrance.
for x in range(1760,2880,704):
 n=min(704,2880-x);connector('market-forecourt-'+str(x),market.crop((0,224,n,320)),(x,2288),[(x,2288,n,96)],'market clear floor')
# Replace only the duplicate32px decorative stripe on the market forecourt; geometry is unchanged.
forecourt=S/'terrain08/market-forecourt-proposed.png'
if forecourt.exists():place(forecourt,'base',(1760,2288))
# Physical direction board on the blocked northeast bed. Its stem is below actors at the public path edge.
sign=S/'wayfinding08/court-sign.png'
if sign.exists():place(sign,'base',(1312,1376))
# Native source effect images translated with their fixed gardens/court.
e=read(R/'effects/effects.json')
if not e.get('revision08Translated'):
 for item in e['effects']:item['origin']=[item['origin'][0]-256,item['origin'][1]-656]
 e['revision08Translated']=True;write(R/'effects/effects.json',e)
# Boundaries and renderer inputs.
grid[0,:]=1;grid[-1,:]=1;grid[:,0]=1;grid[:,-1]=1
above=Image.new('RGBA',(W,H));flat=Image.new('RGBA',(W,H),(12,32,41,255))
for name,im in can.items():im.save(R/f'layers/campus-{name}.png');flat.alpha_composite(im)
for name in ['foreground','glass','shade']:above.alpha_composite(can[name])
above.save(R/'layers/campus-above.png');flat.save(R/'docs/campus08-overview-native.png');flat.resize((1472,1312),Image.Resampling.LANCZOS).save(R/'docs/campus08-overview-half.png')
Image.fromarray(grid*255).resize((W,H),Image.Resampling.NEAREST).save(R/'docs/permanent-collision-mask.png')
write(R/'map/collision-grid.json',{'width':W//8,'height':H//8,'tileSize':8,'blockedIndices':np.flatnonzero(grid).tolist(),'permanent':True})
objects=[{'id':1,'name':'start','class':'area','type':'area','x':920,'y':1552,'width':32,'height':32,'visible':True,'properties':props(start=True)}]
for name,rect in [('StudentHub',(704,64,1536,960)),('Classroom',(64,1280,512,384)),('Event hall',(64,1776,512,544)),('Fountain court',(640,1120,1280,704)),('Riverside',(1920,1264,1024,1024)),('Market',(1824,1968,768,320))]:
 x,y,w,h=rect;objects.append({'id':len(objects)+1,'name':name,'class':'area','type':'area','x':x,'y':y,'width':w,'height':h,'visible':True,'properties':props(liveServiceConfigured=False)})
write(R/'map/magical-campus.tmj',{'width':W//8,'height':H//8,'tilewidth':8,'tileheight':8,'layers':[{'id':1,'name':'campus-areas','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':objects}],'nextobjectid':len(objects)+1,'infinite':False,'orientation':'orthogonal','renderorder':'right-down','tiledversion':'1.11.2','type':'map','version':'1.10','backgroundcolor':'#0c2029'})
write(R/'map/compile-manifest.json',{'status':'Revision08 source assembled; native compile and gameplay acceptance pending','world':[W,H],'tileSize':8,'sourceAudit':audit,'modules':mods,'connectors':joins,'avatar':{'frame':[32,32],'scale':1,'body':[-8,0,16,16]},'separateGateMap':True,'liveRoomURLsAssigned':False,'noArtRescaling':True,'noFloorLabels':True,'noDynamicCollision':True,'noAvatarDependentMask':True,'nativeAudioBridgeEnabled':False})
print(json.dumps({'world':[W,H],'modules':len(mods),'officeWorkSeats':8,'receptionStaff':2,'blockedCells':int(grid.sum()),'sourcePieces':len(audit),'connectors':len(joins)}))
