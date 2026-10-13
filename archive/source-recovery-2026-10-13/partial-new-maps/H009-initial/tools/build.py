from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/layout-definition.json').read_text());O=R/'runtime';T=D['tileSize'];W,H=D['worldTiles'];ROOMS=D['rooms'];SEATS=D['seats'];props=lambda **d:[dict(name=k,type='bool'if isinstance(v,bool)else'string',value=v)for k,v in d.items()]
for folder in ['runtime','evidence','review']:(R/folder).mkdir(exist_ok=True)
m=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,tilewidth=T,tileheight=T,width=W,height=H,backgroundcolor='#29251f',layers=[],tilesets=[],properties=props(name=D['title'],script=D['slug']+'.js',status='Unpublished draft; independent and live acceptance pending'));grid=[[1]*W for _ in range(H)];gid=1

def addimage(name,im,offset=(0,0),visible=True):
 global gid
 im=im.convert('RGBA');im.save(O/(name+'.png'));iw,ih=im.size;assert iw%T==ih%T==0;first=gid;cols=iw//T;cnt=cols*(ih//T);gid+=cnt;m['tilesets'].append(dict(firstgid=first,name=name,image=name+'.png',imagewidth=iw,imageheight=ih,tilewidth=T,tileheight=T,columns=cols,tilecount=cnt,margin=0,spacing=0));data=[0]*(W*H)
 for y in range(ih//T):
  for x in range(cols):
   if im.crop((x*T,y*T,x*T+T,y*T+T)).getbbox():data[(y+offset[1]//T)*W+x+offset[0]//T]=first+y*cols+x
 m['layers'].append(dict(name=name,type='tilelayer',width=W,height=H,data=data,visible=visible,opacity=1,x=0,y=0))
for name,room in ROOMS.items():
 im=Image.open(R/room['source']).convert('RGBA').resize(tuple(room['size']),Image.Resampling.LANCZOS);addimage(name,im,room['offset']);ox,oy=[v//T for v in room['offset']]
 for row,spans in room['rows'].items():
  for l,r in spans:
   for x in range(l,r+1):grid[oy+int(row)][ox+x]=0
 for x,y in D.get('blockedCells',{}).get(name,[]):grid[oy+y][ox+x]=1
# Full hard footprints reject every touched collision cell, without overriding for seats.
for room,items in D.get('physicalFootprints',{}).items():
 ox,oy=[v//T for v in ROOMS[room]['offset']];size=tuple(ROOMS[room]['size']);mask=Image.new('1',size);draw=ImageDraw.Draw(mask)
 for f in items:draw.polygon([tuple(p)for p in f['polygon']],fill=1)
 for y in range(size[1]//T):
  for x in range(size[0]//T):
   if mask.crop((x*T,y*T,x*T+T,y*T+T)).getbbox():grid[oy+y][ox+x]=1
logic=gid;gid+=1;Image.new('RGBA',(T,T)).save(O/'logic.png');m['tilesets'].append(dict(firstgid=logic,name='collision',image='logic.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,columns=1,tilecount=1,tiles=[dict(id=0,properties=props(collides=True))]));m['layers'].append(dict(name='collision-permanent',type='tilelayer',width=W,height=H,data=[logic if v else 0 for row in grid for v in row],visible=True,opacity=0))
quiet=gid;gid+=1;m['tilesets'].append(dict(firstgid=quiet,name='quiet',image='logic.png',imagewidth=T,imageheight=T,tilewidth=T,tileheight=T,columns=1,tilecount=1));q=[0]*(W*H);x0,y0,x1,y1=D['quietRect']
for y in range(y0,y1):
 for x in range(x0,x1):q[y*W+x]=quiet
m['layers'].append(dict(name='arrival-quiet',type='tilelayer',width=W,height=H,data=q,visible=True,opacity=0,properties=props(silent=True)))
# Original imagegen sculpture phases, registered on opaque planted-island patches.
# No floor pixels, avatars, collision, or scenery outside an island are touched.
feedback=[];F=D['feedback'];room=ROOMS['orchard'];dx,dy=F['phaseOffset']
for phase,src in F['sourcePhases'].items():
 original=Image.open(R/src).convert('RGBA')
 for tree,poly in F['patches'].items():
  mask=Image.new('L',original.size);ImageDraw.Draw(mask).polygon([tuple(p)for p in poly],fill=255)
  patch=original.copy();patch.putalpha(mask);im=Image.new('RGBA',tuple(room['size']));im.alpha_composite(patch,(dx,dy));name=tree+'-phase-'+phase;addimage(name,im,room['offset'],False);feedback.append(name)
m['layers'].append(dict(name='floorLayer',type='objectgroup',objects=[],visible=True,opacity=1))
for name,polys in D.get('foregroundPolygons',{}).items():
 room=ROOMS[name];im=Image.open(O/(name+'.png')).convert('RGBA');mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
 for poly in polys:d.polygon([tuple(p)for p in poly],fill=255)
 im.putalpha(mask);addimage(name+'-foreground',im,room['offset'])
# Branch backs retain only actual dark wood pixels; no paving strip is foreground.
room=ROOMS['orchard'];im=Image.open(O/'orchard.png').convert('RGBA');fg=Image.new('RGBA',im.size)
for x0,y0,x1,y1 in D['benchBackRegions']:
 for y in range(y0,y1):
  for x in range(x0,x1):
   r,g,b,a=im.getpixel((x,y))
   if r<130 and g<105 and b<80 and r>g:fg.putpixel((x,y),(r,g,b,a))
addimage('orchard-branch-backs',fg,room['offset'])
anchors={}
for id,a in D['anchors'].items():
 ox,oy=ROOMS[a['room']]['offset'];anchors[id]={**a,'x':ox+a['point'][0],'y':oy+a['point'][1]}
objects=[dict(id=i+1,name='popup-'+id,type='',x=a['x']-148,y=a['y']-148,width=296,height=120,rotation=0,visible=True)for i,(id,a)in enumerate(anchors.items())];start=anchors['arrival'];objects.append(dict(id=len(objects)+1,name='start',type='area',x=start['x']-8,y=start['y']-8,width=16,height=16,visible=True,properties=props(start=True)));m['layers'].append(dict(name='objects',type='objectgroup',objects=objects,visible=True,opacity=1))
for i,l in enumerate(m['layers']):l.update(id=i+1,x=0,y=0)
m.update(nextlayerid=len(m['layers'])+1,nextobjectid=len(objects)+1);(O/(D['slug']+'.tmj')).write_text(json.dumps(m,separators=(',',':')));(O/(D['slug']+'.wam')).write_text(json.dumps(dict(version='2.0.0',mapUrl='./'+D['slug']+'.tmj',entities={},entityCollections=[],areas=[]),indent=2));(O/(D['slug']+'.js')).write_text('globalThis.'+D['globalLayout']+' = '+json.dumps(dict(anchors=anchors),separators=(',',':'))+';\n'+(R/'source/experience.js').read_text())
layout=dict(title=D['title'],tileSize=T,width=W,height=H,world=[W*T,H*T],start=[start['x'],start['y']],grid=grid,anchors=anchors,rooms={k:{n:v for n,v in r.items()if n!='rows'}for k,r in ROOMS.items()},seats=SEATS,scenicBoundaries=D['scenic'],fixtureNegatives=D.get('fixtureNegatives',{}),feedbackLayers=feedback);(R/'evidence/layout.json').write_text(json.dumps(layout,indent=2));print('Built original orchard, cam-house, six registered sculpture phases and semantic branch backs.')
