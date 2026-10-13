from pathlib import Path
from PIL import Image, ImageChops
import numpy as np, json, math
R=Path(__file__).resolve().parents[1];O=R/'map32';V=R/'validation'
O.mkdir(exist_ok=True);V.mkdir(exist_ok=True)
W,H,T=1152,896,32;C,N=36,28
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def props(**kw):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in kw.items()]
g=np.ones((N,C),np.uint8);geometry=[]
def region(name,r,blocked):
 x,y,w,h=r;assert all(v%T==0 for v in r)
 g[y//T:(y+h)//T,x//T:(x+w)//T]=int(blocked)
 geometry.append({'name':name,'rect':r,'blocked':blocked})
region('main concourse floor',[96,256,960,480],False)
region('south arrival receiver',[512,736,128,128],False)
region('west social furniture and planted ledge',[192,160,192,128],True)
region('east social furniture and planted ledge',[768,160,192,128],True)
region('northwest inaccessible decorative edge',[96,256,96,32],True)
region('northeast inaccessible decorative edge',[960,256,96,32],True)
region('west portal and pillars',[64,288,160,256],True)
region('east portal and pillars',[928,288,160,256],True)
region('reception directory and desk',[224,544,256,192],True)
region('sample program board and planting',[704,544,224,160],True)
region('southwest palm pedestal and protected approach',[96,544,128,192],True)
region('southeast palm pedestal and protected approach',[928,544,128,192],True)
landmarks=[{'id':n,'x':x,'y':y}for n,x,y in [('arrival',576,736),('south-entry',576,816),('crossroads',576,432),('flagship-threshold',576,272),('forum-approach',240,432),('arena-approach',912,432),('reception',496,656),('sample-program',688,624),('west-social',288,304),('east-social',864,304)]]
quiet=[('quiet-main-foyer',[96,352,960,544]),('quiet-north-circulation',[384,160,384,192])]
start=[544,704,64,64]

# Native actor body model: x-8..x+8, y..y+16. Retain the full union of
# twelve source Woka head frames when deciding safe above-actor pixels.
blocked=g.repeat(T,0).repeat(T,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)))
Y,X=np.indices((H,W));xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16)
clear=((ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa])==0)&(X>=8)&(X+8<=W)&(Y+16<=H)&(~blocked.astype(bool))
sheet=np.asarray(Image.open(R/'references/greg-reference.png').convert('RGBA'));head=np.zeros((14,32),bool)
for r in range(4):
 for c in range(3):head|=sheet[r*32:r*32+14,c*32:c*32+32,3]>32
possible_head=np.zeros((H,W),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy)
 possible_head[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
original=Image.open(R/'assets/lobby-architecture-native.png').convert('RGBA');a=np.array(original)
# Upper architecture, physical furniture, plant/pillar islands and foreground
# walls are authored source geometry; never a single unsplit background layer.
candidate=np.zeros((H,W),bool)
depth_rects=[('north architecture',[32,24,1088,264]),('west wall and portal',[32,64,192,736]),('east wall and portal',[928,64,192,736]),('reception',[224,544,256,192]),('program',[704,544,224,160]),('southwest plants',[96,576,128,160]),('southeast plants',[928,576,128,160]),('southwest wall',[32,736,480,96]),('southeast wall',[640,736,480,96]),('south entry left pillar',[448,736,64,128]),('south entry right pillar',[640,736,64,128])]
for _,(x,y,w,h) in depth_rects:candidate[y:y+h,x:x+w]=True
fgmask=candidate&blocked.astype(bool)&~possible_head
fg=np.zeros_like(a);fg[fgmask]=a[fgmask];base=a.copy();base[fgmask]=0
base=Image.fromarray(base);fg=Image.fromarray(fg)
assert ImageChops.difference(Image.alpha_composite(base,fg),original).getbbox() is None
base.save(R/'assets/lobby-base.png');fg.save(R/'assets/lobby-above.png')
write(R/'source/lobby-geometry.json',{'world':[W,H],'tileSize':T,'bodyModel':{'width':16,'height':16,'anchorToFoot':16},'collisionOperations':geometry,'depthGeometry':[{'name':n,'rect':r}for n,r in depth_rects],'headSafety':'Retain obstacle pixels above actors only where no body-clear placement can put any of the 12 native Woka upper14px head masks. Excluded original pixels remain below actors.','foregroundPixels':int(fgmask.sum()),'foregroundCandidatePixels':int(candidate.sum()),'exactEmptySceneUnion':True})
sets=[];layers=[];gid=1;atlas_audit=[]
def tl(name,data,opacity=1):return {'id':0,'name':name,'type':'tilelayer','x':0,'y':0,'width':C,'height':N,'visible':True,'opacity':opacity,'data':list(map(int,data))}
for name,im in [('lobby-base',base),('lobby-above',fg)]:
 if name=='lobby-above':layers.append({'id':0,'name':'floorLayer','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':[]})
 cells=[];lookup={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   tile=im.crop((x,y,x+T,y+T));blob=tile.tobytes()
   if not tile.getchannel('A').getbbox():data.append(0);continue
   if blob not in lookup:lookup[blob]=len(cells);cells.append(tile)
   data.append(gid+lookup[blob])
 restore=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restore.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 assert ImageChops.difference(im,restore).getbbox() is None
 for page,s in enumerate(range(0,len(cells),1024)):
  pieces=cells[s:s+1024];cols=min(32,len(pieces));rows=math.ceil(len(pieces)/cols);atlas=Image.new('RGBA',(cols*T,rows*T))
  for i,p in enumerate(pieces):atlas.paste(p,((i%cols)*T,(i//cols)*T))
  pn=f'{name}-p{page}';atlas.save(O/f'{pn}.png');sets.append({'firstgid':gid+s,'name':pn,'image':pn+'.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':cols,'tilecount':len(pieces)})
 layers.append(tl(name,data));atlas_audit.append({'layer':name,'uniqueTiles':len(cells),'exactPixelRoundTrip':True});gid+=len(cells)
Image.new('RGBA',(T,T),(240,30,70,90)).save(O/'collision-cell.png')
sets.append({'firstgid':gid,'name':'permanent-collision','image':'collision-cell.png','imagewidth':T,'imageheight':T,'tilewidth':T,'tileheight':T,'columns':1,'tilecount':1,'margin':0,'spacing':0,'tiles':[{'id':0,'properties':props(collides=True)}]})
layers.insert(1,tl('collision-permanent',[gid if x else 0 for x in g.flat],0))
objects=[]
def area(name,r,**kw):
 x,y,w,h=r;objects.append({'id':len(objects)+1,'name':name,'class':'area','type':'area','x':x,'y':y,'width':w,'height':h,'rotation':0,'visible':True,'properties':props(**kw)})
area('start',start,start=True)
for name,r in quiet:area(name,r,silent=True)
area('Flagship link pending',[512,256,128,32],destinationStatus='Unconfigured; verified room destination required',hallId='astral-flagship')
area('Forum unavailable',[224,384,32,128],destinationStatus='Unavailable; hall not built',hallId='astral-forum')
area('Arena unavailable',[896,384,32,128],destinationStatus='Unavailable; hall not built',hallId='astral-arena')
area('Sample directory and program',[224,512,704,224],contentStatus='Illustrative sample only; no real event schedule')
layers.append({'id':0,'name':'map-areas','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':objects})
for i,l in enumerate(layers):l['id']=i+1
m={'compressionlevel':-1,'height':N,'width':C,'infinite':False,'orientation':'orthogonal','renderorder':'right-down','tiledversion':'1.11.2','tileheight':T,'tilewidth':T,'type':'map','version':'1.10','nextlayerid':len(layers)+1,'nextobjectid':len(objects)+1,'backgroundcolor':'#0c282e','properties':props(name='Astral Concourse shared arrival',wokaScale=1,status='Local candidate; no live room or exits configured'),'layers':layers,'tilesets':sets}
write(O/'astral-concourse-lobby.tmj',m)
wam={'version':'2.0.0','mapUrl':'./astral-concourse-lobby.tmj','entities':{},'entityCollections':[],'areas':[]}
for name,r in quiet:
 x,y,w,h=r;wam['areas'].append({'id':'astral-lobby-'+name,'name':name,'x':x,'y':y,'width':w,'height':h,'visible':True,'properties':[{'id':'astral-lobby-'+name+'-silent','type':'silent'}]})
x,y,w,h=start;wam['areas'].append({'id':'astral-lobby-arrival','name':'Lobby arrival','x':x,'y':y,'width':w,'height':h,'visible':True,'properties':[{'id':'astral-lobby-start','type':'start','isDefault':True}]})
write(O/'astral-concourse-lobby.wam',wam)
write(R/'source/collision-grid.json',{'width':C,'height':N,'tileSize':T,'grid':g.tolist(),'blockedIndices':np.flatnonzero(g).tolist(),'start':[576,736],'landmarks':landmarks,'startRect':start,'quietRegions':[r for _,r in quiet]})
write(R/'source/runtime-build-manifest.json',{'mapDimensions':[W,H],'nativeTileSize':32,'wokaScale':1,'authoredCollisionGeometry':geometry,'atlasRoundTrips':atlas_audit,'depthLayers':['lobby-base','floorLayer','lobby-above'],'noExitUrls':True,'unavailableHalls':['Forum','Arena'],'flagshipLink':'pending verified room URL','sampleScheduleOnly':True,'liveVerification':False})
print(json.dumps({'walkableCells':int((g==0).sum()),'foregroundPixels':int(fgmask.sum()),'atlasRoundTrips':atlas_audit},indent=2))
