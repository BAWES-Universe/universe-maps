"""Compile isolated v03 using the reviewed native art; original versions read-only."""
from pathlib import Path
from PIL import Image
import numpy as np,json,math,hashlib,copy
R=Path(__file__).resolve().parents[1]; V1=R/'source/reuse-inputs/v01';O=R/'map32';W,H=2560,1920;T=32;C,N=W//T,H//T
jw=lambda p,x:Path(p).write_text(json.dumps(x,indent=2)+'\n')
def props(**kw):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in kw.items()]
a=json.loads((R/'source/art-layout.json').read_text());cfg=copy.deepcopy(a);changes=[]
removed={'lounge-01-planter','lounge-03-planter','lounge-04-planter','west-entry-edge'}
cfg['furniture']=[p for p in cfg['furniture']if p['id']not in removed]
for name,x,y in [('lounge01-west',64,1056),('lounge01-east',448,1056),('lounge02-west',608,1056),('lounge02-east',864,1056),('lounge03-west',1088,1056),('lounge03-east',1440,1056),('lounge04-west',64,1440),('lounge04-east',448,1440)]:
 cfg['furniture'].append({'id':name+'-low-divider','asset':'assets/divider-vertical-low-32x256.png','x':x,'y':y,'width':32,'height':256,'foregroundFromLocalY':None,'solidFootprintXYWH':[x,y,32,256]})
for name,x,y,w,asset in [('lounge01-north',96,1056,352,'divider-horizontal-low-352x48'),('lounge02-north',640,1056,224,'divider-lounge-02-south'),('lounge03-north',1120,1056,320,'divider-lounge-03-south'),('lounge04-south',96,1664,352,'divider-horizontal-low-352x48')]:
 cfg['furniture'].append({'id':name+'-low-divider','asset':'assets/'+asset+'.png','x':x,'y':y-16,'width':w,'height':48,'foregroundFromLocalY':None,'solidFootprintXYWH':[x,y,w,32]})
changes.append({'id':'low-three-sided-bay-edges','replaces':sorted(removed),'reason':'Visible low planted edges prevent through shortcuts; all upper bays open south and lower-left bay opens north to the concourse'})
cfg['zonesNote']='Companion WAM encodes four unique native meeting rooms; a plain Custom TMJ room does not automatically import them. Activate in the actual room editor and test media. The tile quiet route is present in TMJ itself.'
for bay in cfg['groupBays']:bay['type']='Companion WAM meeting-room candidate; actual room setup/live test pending'

# Native tile registration keeps visible scale while giving furniture solid back/foot tiles.
for p in cfg['furniture']:
 if p['id'].endswith('-S') and p['id'].startswith('lounge-'):p['y']-=16;changes.append({'id':p['id'],'dx':0,'dy':-16,'reason':'Native32 rear-foot collision and lower-back depth'})
 if any(p['id'].startswith(q['id']+'-') for q in cfg['informalPairs']):p['x']+=16;changes.append({'id':p['id'],'dx':16,'dy':0,'reason':'Solid central table tile with56px pair spacing'})
 if p['id'].startswith('lounge-') and p['id'].endswith(('-W','-E')):p['foregroundFromLocalY']=43
for q in cfg['socialAnchors']:
 if q['id'].endswith('-S') and q.get('group'):q['y']-=16;q['floorClick'][1]-=16
 if q.get('pair'):q['x']+=16;q['floorClick'][0]+=16
for q in cfg['informalPairs']:q['center'][0]+=16
# Keep lounge chair back strips centered on their protecting collision column.
for q in cfg['socialAnchors']:
 if q.get('group'):
  oldx=q['x']; nominal=oldx+(16 if q['group']=='lounge-03' else 0); newx=round((nominal-16)/32)*32+16; dx=newx-oldx
  q['x']=newx;q['floorClick'][0]+=dx
  p=next(p for p in cfg['furniture']if p['id']==q['id']);p['x']+=dx
  if dx:changes.append({'id':q['id'],'dx':dx,'dy':0,'reason':'Chair-back column centered on native32 collision support'})
for p in cfg['furniture']:
 if p['id']=='lounge-03-table':p['x']+=16;changes.append({'id':p['id'],'dx':16,'dy':0,'reason':'Keep table centered between registered chairs'})

for q in cfg['socialAnchors']:
 click=q['y']+16;mod=click%32;newclick=click-1 if mod==0 else click+(16-mod) if mod<16 else click
 if newclick!=click:
  changes.append({'id':q['id'],'anchorDy':newclick-click,'reason':'Exact native click-fit anchor inside walkable tile'})
  q['y']+=newclick-click;q['floorClick'][1]=newclick
cfg['nativeRegistrationChanges']=changes
base=Image.open(R/'source/architecture-native.png').convert('RGBA');base.alpha_composite(Image.open(R/'source/rugs-native.png').convert('RGBA'));fg=Image.new('RGBA',(W,H));fg.alpha_composite(Image.open(R/'source/v01-runtime-above.png').convert('RGBA').crop((0,0,1536,944)),(0,0));original=base.copy();original.alpha_composite(fg);full=Image.new('RGBA',(W,H));lowfull=Image.new('RGBA',(W,H));highfull=Image.new('RGBA',(W,H));anchors={p['id']:p for p in cfg['socialAnchors']}
for p in cfg['furniture']:
 im=Image.open(R/p['asset']).convert('RGBA');lo=im.copy();hi=Image.new('RGBA',im.size);an=anchors.get(p['id'])
 if an:
  y=p['foregroundFromLocalY'];x=an['x']-p['x'];cell=an['x']//32*32;box=(max(0,x-8,cell+8-p['x']),y,min(im.width,x+8,cell+24-p['x']),im.height);hi.paste(im.crop(box),(box[0],box[1]));lo.paste((0,0,0,0),box)
 merged=np.asarray(Image.alpha_composite(lo,hi)); raw=np.asarray(im); assert np.array_equal(merged[raw[:,:,3]>0],raw[raw[:,:,3]>0])
 full.alpha_composite(im,(p['x'],p['y']));lowfull.alpha_composite(lo,(p['x'],p['y']));highfull.alpha_composite(hi,(p['x'],p['y']))
base.alpha_composite(lowfull);fg.alpha_composite(highfull);base.save(R/'assets/runtime-base.png');fg.save(R/'assets/runtime-above.png');full.save(R/'source/runtime-furniture-full.png');lowfull.save(R/'source/runtime-furniture-below.png');highfull.save(R/'source/runtime-furniture-above.png');empty=Image.alpha_composite(base,fg);expected=original.copy();expected.alpha_composite(full);assert empty.tobytes()==expected.tobytes();empty.save(R/'review/runtime-empty-native.png')
old=Image.alpha_composite(Image.open(R/'source/v01-runtime-base.png').convert('RGBA'),Image.open(R/'source/v01-runtime-above.png').convert('RGBA'));assert empty.crop((0,0,1536,944)).tobytes()==old.crop((0,0,1536,944)).tobytes()
g=np.ones((N,C),np.uint8);oldg=np.array(json.loads((V1/'source/collision-grid.json').read_text())['grid'],np.uint8);g[:30,:48]=oldg[:30]
def rect(x,y,w,h,value):assert all(v%32==0 for v in[x,y,w,h]),[x,y,w,h];g[y//32:(y+h)//32,x//32:(x+w)//32]=value
def boundsbox(box):x0,y0,x1,y1=box;return [math.floor(x0/32)*32,math.floor(y0/32)*32,math.ceil(x1/32)*32-math.floor(x0/32)*32,math.ceil(y1/32)*32-math.floor(y0/32)*32]
for box in [(64,1024,1408,672),(512,928,96,128),(928,928,96,128),(640,1696,256,224),(1536,1088,928,608),(1472,1312,64,160)]:rect(*box,0)
solids=[]
for p in cfg['furniture']:
 an=anchors.get(p['id'])
 if 'solidFootprintXYWH' in p:box=p['solidFootprintXYWH']
 elif an:box=[an['x']//32*32,math.ceil((an['y']+16)/32)*32,32,32]
 elif any(p['id']==q['id']+'-table' for q in cfg['informalPairs']):cx=next(q['center'][0]for q in cfg['informalPairs']if p['id']==q['id']+'-table');box=[cx//32*32,math.floor(p['y']/32)*32,32,math.ceil((p['y']+p['height'])/32)*32-math.floor(p['y']/32)*32]
 else:box=boundsbox([p['x'],p['y'],p['x']+p['width'],p['y']+p['height']])
 rect(*box,1);solids.append({'id':p['id'],'xywh':box})
for name,box in [('pergola-west-post',[1696,1088,32,160]),('pergola-east-post',[2112,1088,32,160]),('pergola-north-beam',[1696,1088,448,32])]:rect(*box,1);solids.append({'id':name,'xywh':box})
quiet=np.zeros((N,C),np.uint8);quietrects=[{'id':'west-hall-approach','xywh':[512,1024,96,320]},{'id':'east-hall-approach','xywh':[928,1024,96,320]},{'id':'cross-concourse-to-terrace','xywh':[512,1344,1952,96]},{'id':'arrival','xywh':[672,1440,192,480]}]
for q in quietrects:x,y,w,h=q['xywh'];quiet[y//32:(y+h)//32,x//32:(x+w)//32]=1
assert not np.any(quiet&g),'Quiet path crosses a physical obstacle'
sets=[];layers=[];gid=1;audit=[]
def tl(name,data,opacity=1):return {'id':0,'name':name,'type':'tilelayer','x':0,'y':0,'width':C,'height':N,'visible':True,'opacity':opacity,'data':list(map(int,data))}
for name,im in [('hall-base',base),('hall-above',fg)]:
 if name=='hall-above':layers.append({'id':0,'name':'floorLayer','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':[]})
 cells=[];look={};data=[]
 for y in range(0,H,32):
  for x in range(0,W,32):
   tile=im.crop((x,y,x+32,y+32));blob=tile.tobytes()
   if not tile.getchannel('A').getbbox():data.append(0);continue
   if blob not in look:look[blob]=len(cells);cells.append(tile)
   data.append(gid+look[blob])
 restore=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restore.paste(cells[v-gid],((i%C)*32,(i//C)*32))
 assert restore.tobytes()==im.tobytes()
 for page,start in enumerate(range(0,len(cells),1024)):
  part=cells[start:start+1024];cols=min(32,len(part));atlas=Image.new('RGBA',(cols*32,math.ceil(len(part)/cols)*32))
  for i,tile in enumerate(part):atlas.paste(tile,((i%cols)*32,(i//cols)*32))
  pn=f'{name}-p{page}';atlas.save(O/f'{pn}.png');sets.append({'firstgid':gid+start,'name':pn,'image':pn+'.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':32,'tileheight':32,'margin':0,'spacing':0,'columns':cols,'tilecount':len(part)})
 layers.append(tl(name,data));audit.append({'name':name,'uniqueTiles':len(cells),'pixelExactRoundTrip':True});gid+=len(cells)
Image.new('RGBA',(32,32),(240,30,70,90)).save(O/'collision-cell.png');sets.append({'firstgid':gid,'name':'permanent-collision','image':'collision-cell.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'margin':0,'spacing':0,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':props(collides=True)}]});layers.insert(1,tl('collision-permanent',[gid if v else 0 for v in g.flat],0));gid+=1
Image.new('RGBA',(32,32)).save(O/'quiet-marker.png');sets.append({'firstgid':gid,'name':'quiet-marker-noncolliding','image':'quiet-marker.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'margin':0,'spacing':0,'columns':1,'tilecount':1});ql=tl('quiet-arrival-and-main-circulation',[gid if v else 0 for v in quiet.flat]);ql['properties']=props(silent=True);layers.insert(2,ql)
objects=[{'id':1,'name':'start','class':'area','type':'area','x':736,'y':1792,'width':64,'height':64,'rotation':0,'visible':True,'properties':props(start=True)}];layers.append({'id':0,'name':'map-areas','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':objects})
for i,l in enumerate(layers):l['id']=i+1
m={'compressionlevel':-1,'height':N,'width':C,'infinite':False,'orientation':'orthogonal','renderorder':'right-down','tiledversion':'1.11.2','tileheight':32,'tilewidth':32,'type':'map','version':'1.10','nextlayerid':len(layers)+1,'nextobjectid':2,'backgroundcolor':'#102c32','properties':props(name='Astral Concourse / Flagship v03 Foyer and Terrace',visualSeats=210,loungeSeats=16,casualSeats=8,wokaScale=1,status='Local candidate; room WAM setup and live acceptance pending'),'layers':layers,'tilesets':sets};jw(O/'grand-auditorium.tmj',m)
prefix='astral-flagship-v03';wam={'version':'2.0.0','mapUrl':'./grand-auditorium.tmj','entities':{},'entityCollections':[],'areas':[{'id':prefix+'-podium','name':'Flagship v03 Podium','x':256,'y':208,'width':1024,'height':128,'visible':True,'properties':[{'id':prefix+'-broadcast','type':'speakerMegaphone','name':prefix+'-stage','chatEnabled':False}]},{'id':prefix+'-audience','name':'Flagship v03 Audience','x':128,'y':384,'width':1280,'height':623,'visible':True,'properties':[{'id':prefix+'-receive','type':'listenerMegaphone','speakerZoneName':prefix+'-podium','chatEnabled':False}]},{'id':prefix+'-spawn','name':'Flagship v03 arrival','x':736,'y':1792,'width':64,'height':64,'visible':True,'properties':[{'id':prefix+'-start','type':'start','isDefault':True}]}]}
for q in cfg['groupBays']:
 x,y,x1,y1=q['bounds'];name=prefix+'-'+q['id'];wam['areas'].append({'id':name,'name':'Foyer '+q['id'],'x':x,'y':y,'width':x1-x-1,'height':y1-y-1,'visible':True,'properties':[{'id':name+'-call','type':'livekitRoomProperty','roomName':name,'livekitRoomConfig':{'startWithAudioMuted':False,'startWithVideoMuted':False,'disableChat':False}}]})
jw(O/'grand-auditorium.wam',wam);cfg['quietTileRectangles']=quietrects;cfg['solidTileRectangles']=solids;cfg['spawn']=[768,1824];cfg['spawnRectangle']=[736,1792,64,64];cfg['status']='compiled local candidate';jw(R/'source/runtime-layout.json',cfg)
landmarks=[{'id':p['id'],'x':p['x'],'y':p['y']}for p in cfg['reviewActors'] if not p.get('group')and not p.get('pair')];landmarks += [{'id':'outside-entry','x':768,'y':1888},{'id':'left-stage-steps','x':288,'y':336},{'id':'right-stage-steps','x':1248,'y':336}];seats=json.loads((R/'source/seats.json').read_text());jw(R/'source/collision-grid.json',{'width':C,'height':N,'tileSize':32,'grid':g.tolist(),'start':[768,1824],'speaker':[768,264],'anchors':[[q['id'],q['x'],q['y']]for q in seats],'socialAnchors':cfg['socialAnchors'],'landmarks':landmarks});jw(R/'source/quiet-grid.json',{'width':C,'height':N,'tileSize':32,'grid':quiet.tolist(),'coordinateSystem':'Player x,y directly; WAM checks use y+16','rectangles':quietrects});jw(R/'source/build-manifest.json',{'title':'Flagship v03: Grand Foyer and Coffee Terrace','world':[W,H],'nativeTileSize':32,'visualAuditoriumSeats':210,'loungeAnchors':16,'casualAnchors':8,'protectedRectXYXY':[0,0,1536,944],'protectedPixelsExact':True,'atlasRoundTrips':audit,'runtimeActorsBakedIn':False,'silentOwner':'One noncolliding transparent TMJ tile layer; no WAM silent areas','liveMediaVerified':False,'sceneryWalkable':False,'publication':False,'nativeRegistrationChanges':changes})
print(json.dumps({'world':[W,H],'walkableCells':int((g==0).sum()),'quietCells':int(quiet.sum()),'runtimeFiles':len(list(O.iterdir())),'atlasRoundTrips':audit},indent=2))
