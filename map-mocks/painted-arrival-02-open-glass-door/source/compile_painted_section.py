"""Compile independently authored painted plates + explicit vector gameplay masks.
No new raster art is synthesized here: transforms are one native downsample, semantic
pixel assignment, alpha compositing, and native32px atlas/animation packing.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'town-map';(O/'tilesets').mkdir(parents=True,exist_ok=True)
W=H=1024;N=32
D=json.loads((R/'mask-work/semantic-mask-proposal.json').read_text())
def native(p):
 im=Image.open(p).convert('RGBA');assert im.width>=W and im.height>=H
 return im.convert('RGBa').resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
ground=native(R/'art-source/ground-clean-pass.png');objects=native(R/'art-source/objects-door-alpha.png')
L={'campus-ground':ground,'campus-objects':objects.copy()};ALPHA=objects.getchannel('A');assigned=Image.new('L',(W,H))
def poly_mask(points):
 m=Image.new('L',(W,H));ImageDraw.Draw(m).polygon([tuple(p) for p in points],fill=255);return m
def assign(name,mask):
 global assigned
 alpha=ImageChops.multiply(ALPHA,mask);im=objects.copy();im.putalpha(alpha)
 if name in L:L[name].alpha_composite(im)
 else:L[name]=im
 assigned=ImageChops.lighter(assigned,mask)
# Genuine source pixels only. Near backrests intentionally cover lower body and preserve head.
for s in D['seats'][:4]:
 pts=s.get('near_rim_candidate')
 if pts:
  pts=[[x, min(y,198) if i<2 else y] for i,(x,y) in enumerate(pts)]
  assign('campus-chair-backs',poly_mask(pts))
for f in D['foreground']:
 ident=f['id']
 if ident.startswith('chair-'):continue
 mask=poly_mask(f['points'])
 if ident=='main-arch-and-jambs':
  upper=Image.new('L',(W,H));ImageDraw.Draw(upper).rectangle((448,348,578,439),fill=255)
  assign('campus-entry-cover',ImageChops.multiply(mask,upper));assign('campus-front-structure',ImageChops.subtract(mask,upper))
 elif ident.startswith('meeting-'):assign('campus-glass-frames',mask)
 else:assign('campus-canopy-and-rims',mask)
L['campus-objects'].putalpha(ImageChops.multiply(ALPHA,ImageChops.invert(assigned)))
# Code-native transparent material planes are separate from the painted frames/background.
glazing=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(glazing)
for p in D.get('glazing',[]):gd.polygon([tuple(v) for v in p['points']],fill=tuple(p['rgba']))
L['campus-glazing']=glazing
shade=Image.new('RGBA',(W,H))
for s in D['shade']:
 m=poly_mask(s['points']).filter(ImageFilter.GaussianBlur(4));m=m.point(lambda a:round(a*s['rgba'][3]/255));p=Image.new('RGBA',(W,H),tuple(s['rgba'][:3])+(0,));p.putalpha(m);shade.alpha_composite(p)
L['campus-broad-shade']=shade
# Four original imagegen water phases; no stone/basin pixels are animated.
strip=Image.open(R/'art-source/fountain-motion-strip.png').convert('RGBA');water=[]
for frame in range(4):
 cell=strip.crop((round(frame*strip.width/4),0,round((frame+1)*strip.width/4),strip.height))
 canvas=Image.new('RGBA',(W,H))
 glints=cell.crop((25,478,440,650)).convert('RGBa').resize((222,122),Image.Resampling.LANCZOS).convert('RGBA');glints.putalpha(glints.getchannel('A').point(lambda a:round(a*.32)));canvas.alpha_composite(glints,(167,661))
 jet=cell.crop((165,208,306,548)).convert('RGBa').resize((34,82),Image.Resampling.LANCZOS).convert('RGBA');jet.putalpha(jet.getchannel('A').point(lambda a:round(a*.45)));canvas.alpha_composite(jet,(262,610))
 # Actual receiver-water ellipse and jet only; central masonry never receives the overlay.
 mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask);md.ellipse((177,662,392,790),fill=255);md.ellipse((249,662,312,729),fill=0);md.polygon([(265,609),(293,609),(294,667),(278,688),(262,667)],fill=255)
 canvas.putalpha(ImageChops.multiply(canvas.getchannel('A'),mask));water.append(canvas)
# Permanent32px reviewed footprints, independent of every visibility layer.
blocked=set(D['collision_grid']['blocked_indices']);collision=[1 if i in blocked else 0 for i in range(N*N)]
# Main map packing de-duplicates actual tiles only; independent semantically empty tiles stay empty.
atlases=[];atlas=Image.new('RGBA',(1024,1024));counter=0;seen={};data={};meta={}
def gid(im):
 global atlas,counter
 if not im.getchannel('A').getbbox():return 0
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h in seen:return seen[h]
 idx=counter%1024
 if idx==0 and counter:atlases.append(atlas);atlas=Image.new('RGBA',(1024,1024))
 atlas.alpha_composite(im,((idx%32)*32,(idx//32)*32));counter+=1;seen[h]=counter;return counter
for name,im in L.items():data[name]=[gid(im.crop((x*32,y*32,x*32+32,y*32+32))) for y in range(N) for x in range(N)]
marker=Image.new('RGBA',(32,32));marker.putpixel((0,0),(1,1,1,1));solid=gid(marker);atlases.append(atlas)
sets=[]
for i,im in enumerate(atlases):
 name=f'painted-{i}';im.save(O/'tilesets'/f'{name}.png');ts={'firstgid':i*1024+1,'name':name,'image':f'tilesets/{name}.png','imagewidth':1024,'imageheight':1024,'tilewidth':32,'tileheight':32,'tilecount':1024,'columns':32}
 if (solid-1)//1024==i:ts['tiles']=[{'id':(solid-1)%1024,'properties':[{'name':'collides','type':'bool','value':True}]}]
 sets.append(ts)
# Each animation frame stays in the SAME tileset, native tile-ID animation semantics.
watlas=Image.new('RGBA',(1024,1024));wf=len(atlases)*1024+1;wd=[0]*(N*N);tiles=[];ww,hh=8,7;count=ww*hh
for frame,im in enumerate(water):
 for yy in range(hh):
  for xx in range(ww):
   cell=yy*ww+xx;i=frame*count+cell;piece=im.crop((160+xx*32,608+yy*32,192+xx*32,640+yy*32));watlas.alpha_composite(piece,((i%32)*32,(i//32)*32))
   if frame==0:
    wd[(19+yy)*N+5+xx]=wf+cell;tiles.append({'id':cell,'animation':[{'tileid':f*count+cell,'duration':260} for f in range(4)]})
watlas.save(O/'tilesets/water-motion.png');sets.append({'firstgid':wf,'name':'painted-water-motion','image':'tilesets/water-motion.png','imagewidth':1024,'imageheight':1024,'tilewidth':32,'tileheight':32,'tilecount':1024,'columns':32,'tiles':tiles})
layers=[]
def layer(name,ds,props=None):
 p=[{'name':'sceneOwner','type':'string','value':'campus'}]+(props or [])
 layers.append({'id':len(layers)+1,'name':name,'type':'tilelayer','width':N,'height':N,'x':0,'y':0,'opacity':1,'visible':True,'data':ds,'properties':p})
layer('permanent-collisions',[solid if b else 0 for b in collision]);layer('campus-ground',data['campus-ground']);layer('campus-objects',data['campus-objects']);layer('campus-water-motion',wd)
layers.append({'id':len(layers)+1,'name':'floorLayer','type':'objectgroup','objects':[],'opacity':1,'visible':True})
for name in ['campus-canopy-and-rims','campus-front-structure','campus-chair-backs','campus-glazing','campus-glass-frames','campus-broad-shade','campus-entry-cover']:
 layer(name,data[name],[{'name':'revealArea','type':'string','value':'commons-inside'}] if name=='campus-entry-cover' else None)
objs=[]
def obj(name,x,y,w=0,h=0,area=False):
 d={'id':len(objs)+1,'name':name,'x':x,'y':y,'width':w,'height':h,'rotation':0,'visible':True}
 if area:d['class']='area';d['type']='area'
 if not w and not h:d['point']=True
 objs.append(d)
obj('campus-bounds',0,0,W,H);obj('campus-spawn',512,968);obj('campus-return',464,992,96,32)
obj('commons-inside',192,152,724,264,True);obj('team-shared-work',224,152,546,120,True);obj('reception',560,300,64,90,True);obj('glass-meeting',782,220,130,165,True);obj('arrival-court',64,544,896,448,True)
layers.append({'id':len(layers)+1,'name':'areas','type':'objectgroup','objects':objs,'opacity':1,'visible':True})
mapdata={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','width':N,'height':N,'tilewidth':32,'tileheight':32,'infinite':False,'nextlayerid':len(layers)+1,'nextobjectid':len(objs)+1,'layers':layers,'tilesets':sets}
(O/'town.tmj').write_text(json.dumps(mapdata,separators=(',',':')))
way=[('Garden arrival',512,968,None),('Fountain path',464,744,None),('Living canopy shade',592,700,'shadow'),('StudentHub threshold',512,480,None),('Reception west approach',590,344,None),('West team chair',304,194,'chair'),('Shared aisle',512,272,None),('Visible glass doorway',752,240,None),('Meeting room entry',804,238,None),('Meeting glass view',850,358,'glass'),('Meeting doorway return',752,240,None),('Commons return',512,344,None),('Court return',512,576,None),('Gate path return',512,968,None)]
layout={'campus':{'bounds':{'x':0,'y':0,'width':1024,'height':1024},'spawn':{'x':512,'y':968},'return':{'x':464,'y':992,'width':96,'height':32}},'roofReveals':[{'area':'commons-inside','layers':['campus-entry-cover']}],'layers':{'chair':['campus-chair-backs'],'glass':['campus-glazing'],'shadow':['campus-broad-shade']},'requiredForegroundRoles':['chair','glass','shadow'],'waypoints':[dict(name=n,x=x,y=y,**({'role':r} if r else {})) for n,x,y,r in way],
'glassDoor':{'outside':{'x':752,'y':240},'inside':{'x':804,'y':238},'corridor':{'x':742,'y':232,'width':72,'height':32}},'probes':[{'name':'Meeting front sill','start':{'x':850,'y':338},'direction':{'x':0,'y':1},'durationMs':650,'expectStop':{'axis':'y','min':367.5,'max':368.5}}],
'rooms':[{'id':'StudentHub shared team','bounds':{'x':192,'y':152,'width':724,'height':264}},{'id':'Arrival court','bounds':{'x':64,'y':544,'width':896,'height':448}}]}
# Geometry supplied by the audio worker is already in combined-world coordinates.
a=json.loads((R/'audio-work/proposed-layout-audio.json').read_text());layout['audio']=a.get('audio',a);layout['audio']['coordinateSpace']='world'
(O/'layout.json').write_text(json.dumps(layout,indent=2))
for n,im in L.items():im.save(R/'layers'/f'{n}.png')
# Offline preview uses exactly the compiled source layer order and unchanged Woka.
preview=ground.copy();preview.alpha_composite(L['campus-objects']);preview.alpha_composite(water[0]);g=Image.open(R/'runtime-work/greg.png').crop((32,96,64,128));preview.alpha_composite(g,(288,178))
for n in ['campus-canopy-and-rims','campus-front-structure','campus-chair-backs','campus-glazing','campus-glass-frames','campus-broad-shade']:preview.alpha_composite(L[n])
preview.save(R/'docs/assembled-chair-native.png')
print(json.dumps({'tiles':counter,'atlases':len(sets),'collision':len(blocked),'native':[W,H],'status':'compiled source; runtime verification pending'}))
