"""Isolated native-pixel gameplay trial. Existing campus TMJ/assets/runtime untouched."""
from pathlib import Path
from PIL import Image
import numpy as np,json,bisect,copy,hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]; O=P/'playable';O.mkdir(exist_ok=True)
m=json.loads((R/'campus.tmj').read_text()); base=copy.deepcopy(m)
X,Y,W,H=1664,2048,4864,3712
canvas=Image.new('RGBA',(W,H))
for name,px,py in json.loads((P/'panels.json').read_text()):
 if name.startswith('facade-'):continue
 im=Image.open(P/name).convert('RGBA');assert im.size in [(1536,1024),(1024,1024)]
 canvas.alpha_composite(im,(px-X,py-Y))
# Keep the latest corrected café authoritative; hard native joins inside overlaps.
canvas.alpha_composite(Image.open(P/'counter-floor-edit-2.png').convert('RGBA').crop((0,0,1408,896)),(1984-X,3712-Y))
canvas.save(P/'assembled-native.png')
full_art=canvas.copy()
for name,px,py in json.loads((P/'panels.json').read_text()):
 if name.startswith('facade-'):full_art.alpha_composite(Image.open(P/name).convert('RGBA'),(px-X,py-Y))
# Native raster corrections from built-in image editing; crop and register, never resize.
for filename,box,world in [('cafe-proportion-2.png',(0,0,1408,896),(1984,3712)),('nook-proportion-3.png',(0,0,1536,768),(1664,2944)),('stage-proportion-1.png',(480,208,1136,480),(5472,3152))]:
 full_art.alpha_composite(Image.open(P/filename).convert('RGBA').crop(box),(world[0]-X,world[1]-Y))
# Reuse the registered island alpha to clip panel sky at the accepted silhouette.
# Only the existing mask is resized; generated artwork remains native 1:1 pixels.
canvas=full_art.copy()
site_alpha=Image.open(R/'source/campus-site-cutout.png').convert('RGBA').getchannel('A').resize((4608,3072),Image.Resampling.LANCZOS)
registered_alpha=Image.new('L',(W,H));registered_alpha.paste(site_alpha,(1792-X,2048-Y))
a=np.array(canvas);a[:,:,3]=np.minimum(a[:,:,3],np.array(registered_alpha));canvas=Image.fromarray(a)
ca_native=np.array(canvas);ca_native[ca_native[:,:,3]==0]=0;canvas=Image.fromarray(ca_native)
canvas.save(P/'assembled-islands.png')
# Never cover the accepted interior, reveal apertures or gate with painted scenery.
canvas.paste((0,0,0,0),(2896-X,2128-Y,5136-X,3040-Y))
sets=base['tilesets'];starts=[s['firstgid'] for s in sets];cache={};fg=Image.new('L',(W,H))
for layer in m['layers']:
 if layer['name'] not in ['cafe-foreground','campus-chair-fronts','campus-bench-fronts','alcove-foreground','audience-fronts']:continue
 for ty in range(Y//16,(Y+H)//16):
  for tx in range(X//16,(X+W)//16):
   xx,yy=tx*16-X,ty*16-Y
   if not canvas.getpixel((xx,yy))[3]:continue
   k=ty*m['width']+tx;gid=layer['data'][k]
   if not gid:continue
   s=sets[bisect.bisect_right(starts,gid)-1];key=s['image']
   if key not in cache:cache[key]=Image.open(R/key).convert('RGBA')
   n=gid-s['firstgid']; sx=s.get('margin',0)+(n%s['columns'])*(16+s.get('spacing',0));sy=s.get('margin',0)+(n//s['columns'])*(16+s.get('spacing',0))
   tile=cache[key].crop((sx,sy,sx+16,sy+16)).getchannel('A');old=np.array(fg.crop((xx,yy,xx+16,yy+16)))
   fg.paste(Image.fromarray(np.maximum(old,np.array(tile))),(xx,yy));layer['data'][k]=0
# Rebuild depth masks against the corrected furniture, not the old oversized silhouettes.
for box in [(2304,4256,3152,4416),(2512,4176,2944,4272),(1968,3136,2352,3344),(5472,3152,6128,3424)]:
 fg.paste(0,(box[0]-X,box[1]-Y,box[2]-X,box[3]-Y))
for cx in [584,680,792,888]:fg.paste(255,(1984+cx-14-X,3712+506-Y,1984+cx+14-X,3712+526-Y))
# Low sofa fronts, below heads and upper torsos.
for bx,by,bw,bh in [(2352,4330,112,6),(2960,4330,112,6),(2100,3242,80,8),(2340,4362,40,20),(3044,4362,40,20)]:fg.paste(255,(bx-X,by-Y,bx+bw-X,by+bh-Y))
# Rear-facing theater chairs: head/shoulders rise above their low back.
for row,top in enumerate([232,292,354,416]):
 for cx in [536,600,664,728,888,952,1016,1080]:
  fg.paste(255,(4992+cx-18-X,2944+top-Y,4992+cx+18-X,2944+top+36-Y))
# Eastern bridge lamp: foreground depth above its solid plinth.
from PIL import ImageDraw
ImageDraw.Draw(fg).polygon([(5256-X,3032-Y),(5320-X,3032-Y),(5312-X,3152-Y),(5336-X,3184-Y),(5328-X,3216-Y),(5248-X,3216-Y),(5248-X,3184-Y),(5272-X,3152-Y)],fill=255)
# Release only the front-of-counter strip needed by the new visible seat row.
collision=next(l for l in m['layers'] if l['name']=='persistent-collision')
for ty in range(4192//16,4272//16):
 for tx in range(2512//16,2928//16):collision['data'][ty*m['width']+tx]=0
# Open the illustrated nook floor and eastern descending entry, preserving table support.
for bx,by,bw,bh in [(2016,3232,288,112),(2288,3248,96,64)]:
 for ty in range(by//16,(by+bh)//16):
  for tx in range(bx//16,(bx+bw)//16):collision['data'][ty*m['width']+tx]=0
oldcoll=next(l for l in base['layers'] if l['name']=='persistent-collision')
for ty in range(3280//16,3296//16):
 for tx in range(2160//16,2208//16):collision['data'][ty*m['width']+tx]=oldcoll['data'][ty*m['width']+tx]
# The old bridge collision extended onto the illustrated front balustrades.
# Keep a 96px clear floor route above them; block only the two rail strips.
bridge_rail_rects=[(2688,3216,608,112),(4960,3216,432,112),(5248,3200,96,32)]
solid_gid=next(g for g in oldcoll['data'] if g)
for bx,by,bw,bh in bridge_rail_rects:
 for ty in range(by//16,(by+bh)//16):
  for tx in range(bx//16,(bx+bw)//16):collision['data'][ty*m['width']+tx]=solid_gid
layout=json.loads((R/'source/layout.json').read_text())
for seat,cx in zip([s for s in layout['seats'] if s['group']=='cafe-bar'],[584,680,792,888]):seat.update(x=1984+cx,y=3712+480,facing='up')
for seat in layout['seats']:
 if seat['group']=='audience':seat['y']-=16
 if seat['group']=='cafe-bar':seat['y']=4208
for i,x,y,facing in [(51,2392,4320,'down'),(52,2424,4320,'down'),(53,3000,4320,'down'),(54,3032,4320,'down'),(55,2360,4352,'right'),(56,3064,4352,'left'),(63,2120,3232,'down'),(64,2152,3232,'down'),(65,2152,3232,'down')]:layout['seats'][i].update(x=x,y=y,facing=facing)
# The native 80px nook sofa supports two 32px sprites without overlap.
del layout['seats'][65]
# Clear vacated old table supports and register the new low table footprints.
furniture_rects=[(2320,4288,208,128),(2944,4288,208,128),(2048,3200,192,144)]
for bx,by,bw,bh in furniture_rects:
 for ty in range(by//16,(by+bh)//16):
  for tx in range(bx//16,(bx+bw)//16):collision['data'][ty*m['width']+tx]=0
for bx,by,bw,bh in [(2400,4368,32,16),(3008,4368,32,16),(2128,3280,16,16)]:
 for ty in range(by//16,(by+bh)//16):
  for tx in range(bx//16,(bx+bw)//16):collision['data'][ty*m['width']+tx]=solid_gid
(P/'candidate-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
front=canvas.copy();front.putalpha(Image.fromarray(np.minimum(np.array(fg),np.array(canvas.getchannel('A')))));ff=np.array(front);ff[ff[:,:,3]==0]=0;front=Image.fromarray(ff);front.save(P/'foreground-trial.png')
for s in m['tilesets']:
 if 'image' in s:s['image']='../../../'+s['image']
for prop in m.get('properties',[]):
 if prop['name']=='script':prop['value']='./runtime.js'
nextgid=max(s['firstgid']+s['tilecount'] for s in m['tilesets']);nextid=max(l['id'] for l in m['layers'])+1

def pack(name,im):
 global nextgid,nextid
 data=[0]*(m['width']*m['height'])
 for py in range(0,H,1024):
  for px in range(0,W,1024):
   page=im.crop((px,py,min(px+1024,W),min(py+1024,H)))
   if not page.getchannel('A').getbbox():continue
   nc,nr=page.width//16,page.height//16;filename=f'{name}-{px}-{py}.png';padded=Image.fromarray(np.pad(np.array(page),((1,1),(1,1),(0,0)),mode='edge'));padded.save(O/filename)
   first=nextgid;nextgid+=nc*nr;m['tilesets'].append(dict(firstgid=first,name=filename[:-4],image=filename,imagewidth=page.width+2,imageheight=page.height+2,margin=1,spacing=0,tilewidth=16,tileheight=16,tilecount=nc*nr,columns=nc))
   alpha=np.array(page.getchannel('A')).reshape(nr,16,nc,16).max(axis=(1,3))
   for ry in range(nr):
    for rx in range(nc):
     if alpha[ry,rx]:data[((Y+py)//16+ry)*m['width']+(X+px)//16+rx]=first+ry*nc+rx
 layer=dict(id=nextid,name=name,type='tilelayer',x=0,y=0,width=m['width'],height=m['height'],visible=True,opacity=1,data=data);nextid+=1;return layer
# Update only opaque exterior artwork; all original transparency/occupant apertures survive.
cover=Image.new('RGBA',(W,H));cover_layer=next(l for l in m['layers'] if l['name']=='office-cover')
for ty in range(Y//16,(Y+H)//16):
 for tx in range(X//16,(X+W)//16):
  gid=cover_layer['data'][ty*m['width']+tx]
  if not gid:continue
  st=sets[bisect.bisect_right(starts,gid)-1];key=st['image']
  if key not in cache:cache[key]=Image.open(R/key).convert('RGBA')
  k=gid-st['firstgid'];sx=st.get('margin',0)+(k%st['columns'])*(16+st.get('spacing',0));sy=st.get('margin',0)+(k//st['columns'])*(16+st.get('spacing',0))
  cover.alpha_composite(cache[key].crop((sx,sy,sx+16,sy+16)),(tx*16-X,ty*16-Y))
ca=np.array(cover);old_alpha=ca[:,:,3].copy();fresh=np.array(full_art);eligible=(old_alpha>=240)&(fresh[:,:,3]>0)
ca[:,:,:3][eligible]=fresh[:,:,:3][eligible];assert np.array_equal(ca[:,:,3],old_alpha)
new_cover=pack('native-office-cover',Image.fromarray(ca));cover_layer['data']=new_cover['data']
full_art.resize((1536,round(H*1536/W)),Image.Resampling.LANCZOS).save(P/'assembled-review.png')
layer=pack('native-cafe-region',canvas);i=next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer');m['layers'].insert(i,layer);m['layers'].append(pack('native-cafe-foreground',front));m['nextlayerid']=nextid
(O/'runtime.js').write_text((R/'runtime.js').read_text()+'\n'+(P/'seat-runtime.js').read_text().replace('__SEATS_JSON__',json.dumps(layout['seats'])))
(O/'campus.tmj').write_text(json.dumps(m,separators=(',',':')))
unchanged={name: next(l for l in base['layers'] if l['name']==name)==next(l for l in m['layers'] if l['name']==name) for name in ['start','office-floor','office-furniture','office-front-door','office-front-leaves']}
assert all(unchanged.values())
(P/'candidate-checks.json').write_text(json.dumps({'nativeScale':1,'resampling':False,'worldOrigin':[X,Y],'regionSize':[W,H],'panels':json.loads((P/'panels.json').read_text()),'horizontalJoinWorldX':3392,'verticalJoinWorldY':4608,'unchangedLayers':unchanged,'exteriorAlphaUnchanged':True,'exteriorOpaquePixelsUpdated':int(eligible.sum()),'baseMapSha256':hashlib.sha256((R/'campus.tmj').read_bytes()).hexdigest(),'runtimeSha256':hashlib.sha256((R/'runtime.js').read_bytes()).hexdigest(),'foreground':'lounge masks retained; moved stool fronts registered at native anchors; runtime visual review required','collisionEditRects':[[2512,4192,416,80],[2016,3232,288,112],[2288,3248,96,64],*bridge_rail_rects,*furniture_rects],'status':'full outdoor native candidate; gameplay and silhouette joins under review','skyIntegration':'original registered island alpha; existing continuous background retained'},indent=2)+'\n')
print('Candidate built; counter-front clearance updated; spawn, accepted office and gate unchanged.')
