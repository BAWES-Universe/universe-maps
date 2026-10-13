from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib
R=Path(__file__).resolve().parents[1];D=json.load(open(R/'source/design.json'));L=json.load(open(R/'source/layout.json'));M=json.load(open(R/'map32/map.tmj'));W,H=D['world'];g=np.array(L['collision'],bool);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Decode every actual emitted state; never use the author scene as proof input.
sets=M['tilesets'];atl={s['image']:Image.open(R/'map32'/s['image']).convert('RGBA')for s in sets};dec={}
for l in M['layers']:
 if l['type']!='tilelayer'or l.get('opacity',1)==0:continue
 out=Image.new('RGBA',(W,H))
 for i,v in enumerate(l['data']):
  if not v:continue
  s=max((s for s in sets if s['firstgid']<=v),key=lambda s:s['firstgid']);t=v-s['firstgid'];x=t%s['columns']*32;y=t//s['columns']*32;out.paste(atl[s['image']].crop((x,y,x+32,y+32)),(i%M['width']*32,i//M['width']*32))
 dec[l['name']]=out
states=[];ims=[]
for packed in [False,True]:
 im=dec['ground-and-architecture'].copy()
 if packed:im=Image.alpha_composite(im,dec['packed-panniers'])
 im=Image.alpha_composite(im,dec['foreground']);ims.append(im);scales=[]
 for num,den in [(1,2),(2,3),(3,4),(1,1),(5,4),(3,2)]:
  z=im.resize((W*num//den,H*num//den),Image.Resampling.BILINEAR);scales.append({'scale':[num,den],'size':list(z.size),'opaque':z.getchannel('A').getextrema()==(255,255),'rasterSHA256':hashlib.sha256(z.tobytes()).hexdigest()})
 states.append({'packed':packed,'pixelSHA256':hashlib.sha256(im.tobytes()).hexdigest(),'staticScales':scales,'opaque':im.getchannel('A').getextrema()==(255,255)})
changed=np.any(np.asarray(ims[0])!=np.asarray(ims[1]),axis=2);ys,xs=np.where(changed);assert len(xs)>1000;assert all(g[y//32,x//32]for x,y in zip(xs,ys));assert all(s['opaque']and all(v['opaque']for v in s['staticScales'])for s in states)
(R/'validation/legal-states.json').write_text(json.dumps({'scope':'Both possible emitted raster sets. Static rational fixed-origin bilinear rasters only, not a live GPU/atlas filtering, camera or device acceptance.','pass':True,'tmjSHA256':sha(R/'map32/map.tmj'),'stateCollisionInvariant':True,'changedPixels':len(xs),'changedBounds':[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1],'allChangedPixelsInsideBlockedFixtureCells':True,'states':states},indent=2))
# Check actual native lower-body alpha touches each authored cushion independently.
actors=json.load(open(R/'source/ACTOR-PROVENANCE.json'))['actors'];proof=json.load(open(R/'validation/actor-proof.json'));contacts=[]
for i,s in enumerate(L['seats']):
 p=proof[i];assert p['exactArrival']and p['arrival']==s['anchor'];sheet=Image.open(R/'source/actors'/p['actor']).convert('RGBA');f=p['frame'];sp=sheet.crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32));aa=np.asarray(sp)[:,:,3];yy,xx=np.where(aa[24:32,:]>0);xx=xx+s['anchor'][0]-16;yy=yy+8+s['anchor'][1];x,y,u,v=s['cushionBounds'];on=(xx>=x)&(xx<=u)&(yy>=y)&(yy<=v);assert len(xx)>0 and on.all();contacts.append({'name':s['name'],'origin':s['anchor'],'frame':f,'lowerBodyAlphaPixels':len(xx),'pixelsOnCushion':int(on.sum()),'pass':True,'claim':'Exact unchanged standing-frame contact, not autositting/facing.'})
(R/'validation/seat-contact-author.json').write_text(json.dumps({'pass':True,'contacts':contacts},indent=2))
# Inventory every admitted/blocked boundary cell against full art-selected floor and whole physical envelope masks.
walk=Image.new('L',(W,H));hard=Image.new('L',(W,H));wd=ImageDraw.Draw(walk);hd=ImageDraw.Draw(hard)
for room in D['rooms']:
 ox,oy=room['offset']
 for p in room['walkPolygons']:wd.polygon([(x+ox,y+oy)for x,y in p],fill=255)
 for p in room['fullFixturePolygons']:hd.polygon([(x+ox,y+oy)for x,y in p],fill=255)
a=np.asarray(walk)>0;b=np.asarray(hard)>0;front=[]
for y in range(g.shape[0]):
 for x in range(g.shape[1]):
  if g[y,x]and any(0<=x+dx<g.shape[1]and 0<=y+dy<g.shape[0]and not g[y+dy,x+dx]for dx,dy in[(0,1),(0,-1),(1,0),(-1,0)]):
   floor=int(a[y*32:y*32+32,x*32:x*32+32].sum());physical=int(b[y*32:y*32+32,x*32:x*32+32].sum());reason='physical-base/architectural-envelope'if physical else'coarse mixed floor/fringe or doorway portal limit'if floor else'outside art-selected bounded circulation';front.append({'cell':[x,y],'floorPixels':floor,'hardPixels':physical,'reason':reason});assert physical or floor<1024
out=ims[0].copy();dr=ImageDraw.Draw(out)
for f in front:
 x,y=f['cell'];dr.rectangle((x*32,y*32,x*32+31,y*32+31),outline='#ff33bb',width=2)
for room,q in json.load(open(R/'source/visible-floor.json'))['rooms'].items():
 for path in q['visiblePaths']:dr.line([tuple(p)for p in path['origins']],fill='#00ffe0',width=2)
out.save(R/'review/full-floor-frontier.png');(R/'validation/blocked-frontier.json').write_text(json.dumps({'scope':'Complete enumerated blocked frontier against art-selected floor and whole-base source masks. Visual completeness still independently reviewable. Coarse native32 mixed-edge fringe is not claimed wholly walkable.','tmjSHA256':sha(R/'map32/map.tmj'),'cells':front,'count':len(front),'unexplainedWhollyClearCells':0},indent=2))
# Final readable plate: both states enlarged, both authored full scenes with complete frontier and width probes.
plate=Image.new('RGB',(2496,1600),'#18252d');plate.paste(out.crop((0,0,1248,1248)),(0,0));plate.paste(out.crop((0,1568,1248,2080)),(1248,0));dr=ImageDraw.Draw(plate)
for i,im in enumerate(ims):
 box=(1020,400,1190,600);plate.paste(im.crop(box).resize((510,600),Image.Resampling.NEAREST),(1248+i*550,600));dr.text((1254+i*550,604),['EMPTY','PACKED: provisions and three seals'][i],fill='white')
for i,s in enumerate(L['seats']):
 x,y=s['anchor'];oc=Image.open(R/'review/occupied-native-arrival.png');plate.paste(oc.crop((x-64,y-48,x+64,y+64)).resize((384,336),Image.Resampling.NEAREST),(i*400,1250));dr.text((i*400+5,1255),s['name']+' exact native contact',fill='white')
plate.save(R/'review/final-author-plate.png')
print(json.dumps({'states':2,'changedPixels':len(xs),'seatContacts':contacts,'frontierCells':len(front)},indent=2))
