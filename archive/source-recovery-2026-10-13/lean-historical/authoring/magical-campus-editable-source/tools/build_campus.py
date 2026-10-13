"""Finite native campus assembly. Source art is copied/cropped, never rescaled.
Only writes universe-campus-connected. Tile physics derives from frozen module contracts.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import numpy as np
import hashlib,json,math,shutil
ROOT=Path(__file__).resolve().parents[1]; SHARED=ROOT.parent
W,H,CELL=3200,3072,8; COLS,ROWS=W//CELL,H//CELL
for d in ('sources','layers','map','docs'): (ROOT/d).mkdir(exist_ok=True)
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def props(**kw):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in kw.items()]
canvas={k:Image.new('RGBA',(W,H)) for k in ('base','foreground','glass','shade','labels')}; sources=[]; connectors=[]; modules=[]
blocked=np.ones((ROWS,COLS),np.uint8)
def art(module,source,target,origin):
 p=Path(source);im=Image.open(p).convert('RGBA');canvas[target].alpha_composite(im,origin)
 dst=ROOT/'sources'/module/p.name;dst.parent.mkdir(exist_ok=True);shutil.copy2(p,dst)
 sources.append({'module':module,'source':str(p),'copy':str(dst.relative_to(ROOT)),'sha256':sha(p),'origin':origin,'size':im.size,'targetLayer':target,'scale':1})
def snapshot(module,p):
 p=Path(p);dst=ROOT/'sources'/module/p.name;dst.parent.mkdir(exist_ok=True);shutil.copy2(p,dst)
 sources.append({'module':module,'source':str(p),'copy':str(dst.relative_to(ROOT)),'sha256':sha(p),'metadata':True})
def set_grid(arr,origin):
 x,y=origin; assert x%CELL==y%CELL==0
 h,w=arr.shape;blocked[y//CELL:y//CELL+h,x//CELL:x//CELL+w]=arr

def mask_grid(size,polygons,obstacles):
 w,h=size;mask=Image.new('1',size,0);d=ImageDraw.Draw(mask)
 for poly in polygons:d.polygon([tuple(p) for p in poly],fill=1)
 for o in obstacles:
  typ=o.get('type','rect')
  if typ=='rect':d.rectangle((o['x'],o['y'],o['x']+o['width']-1,o['y']+o['height']-1),fill=0)
  elif typ=='polygon':d.polygon([tuple(p) for p in o['points']],fill=0)
  else:
   x=o.get('cx',o.get('x'));y=o.get('cy',o.get('y'));rx=o.get('rx',o.get('radius'));ry=o.get('ry',o.get('radius'))
   d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=0)
 a=np.asarray(mask,dtype=np.uint8);return 1-a.reshape(h//CELL,CELL,w//CELL,CELL).min((1,3))
# Office: full canvas grid already includes original 32 px source translation.
office=SHARED/'universe-expanded-office';origin=(480,288);revision=office/'revisions/04-social-reception'; geometry=office/'geometry-work/revision-04-social-egress';freeze=read(geometry/'assembled-art-source-integrity.json')
for f in freeze['files']:assert sha(f['path'])==f['sha256'], f['path']+' has changed since frozen source'
for layer in ['floor','environment','rugs','objects','foreground','glass','overhead-shade','labels']:
 art('office',revision/f'layers/office-v4-{layer}.png',{'foreground':'foreground','glass':'glass','overhead-shade':'shade','labels':'labels'}.get(layer,'base'),origin)
grid=read(geometry/'collision-grid.json');og=np.zeros((grid['height'],grid['width']),np.uint8);og.flat[grid['blockedIndices']]=1
set_grid(og.repeat(2,0).repeat(2,1),origin)
for f in ['collision-grid.json','checkpoint-manifest-full-canvas.json','source-coordinate-geometry.json','personal-areas.offline-draft.wam','social-egress-route-manifest-full-canvas.json','reception-social-route-manifest.json','social-source-contract.json','social-distance-and-group-validation.json']:
 snapshot('office',geometry/f)
snapshot('office',geometry/'assembled-art-source-integrity.json');snapshot('office',geometry/'DELIVERY.json');modules.append({'id':'office','origin':origin,'size':[2496,1408],'sourceGrid':16,'losslessGridPromotion':True,'revision':'04-social-reception'})
# Civic, exact physical module rectangles plus finite bounds. Empty padding stays solid.
civic=SHARED/'universe-civic-rooms';origin=(0,1792);c=read(civic/'module.json')
for f,t in [('architecture','base'),('furniture','base'),('foreground','foreground'),('glass','glass'),('shadow','shade')]:art('civic',civic/f'assets/{f}-native.png',t,origin)
polys=[[[64,144],[576,144],[576,1088],[64,1088]],[[576,344],[640,344],[640,424],[576,424]],[[576,952],[640,952],[640,1032],[576,1032]]]
set_grid(mask_grid((640,1152),polys,c['blockers']),origin);snapshot('civic',civic/'module.json');modules.append({'id':'civic','origin':origin,'size':c['size'],'sourceRectangles':len(c['blockers'])})
# Fountain court uses author walk polygons, physical obstacles and fixed canopy.
court=SHARED/'universe-campus-courtyard';origin=(704,1776);c=read(court/'module.json')
for f,t in [('court-base.png','base'),('court-canopy.png','foreground')]:art('court',court/'layers'/f,t,origin)
set_grid(mask_grid(tuple(c['size']),c['walkablePolygons'],c['obstacles']),origin);snapshot('court',court/'module.json');modules.append({'id':'court','origin':origin,'size':c['size']})
# Garden exact permanent 8 px physical grid, fixed structural foreground.
garden=SHARED/'universe-riverside-garden';native=garden/'native-integration';origin=(2176,1920);g=read(native/'collision-grid-8px.json')
art('garden',garden/'layers/garden-base.png','base',origin);art('garden',native/'masks/bench-and-foliage-fixed-foreground.png','foreground',origin)
set_grid(np.array(g['blocked'],np.uint8).reshape(g['height'],g['width']),origin)
for f in ['native-manifest.json','collision-grid-8px.json','SOURCE.sha256']:snapshot('garden',native/f)
modules.append({'id':'garden','origin':origin,'size':[1024,1024],'sourceGrid':8,'permanentCollision':True,'avatarDependentMask':False})
# Avenue source cells are a standability sample, NOT physical cells. Rasterize source geometry.
avenue=SHARED/'universe-campus-avenue';origin=(704,2480);a=read(avenue/'avenue-manifest.json')
for f,t in [('avenue-base.png','base'),('avenue-foliage-foreground.png','foreground')]:art('avenue',avenue/'layers'/f,t,origin)
set_grid(mask_grid((1472,576),a['walkable'],a['obstacles']),origin);snapshot('avenue',avenue/'avenue-manifest.json');modules.append({'id':'avenue','origin':origin,'size':[1472,576]})
# Parent-approved, lossless native connector crops. No arbitrary outdoor tiling.
source=Image.open(court/'layers/court-base.png').convert('RGBA')
def connector(name,box,dest,open_rects):
 im=source.crop(box);canvas['base'].alpha_composite(im,dest)
 for x,y,w,h in open_rects:
  assert all(v%8==0 for v in (x,y,w,h));blocked[y//8:(y+h)//8,x//8:(x+w)//8]=0
 connectors.append({'id':name,'source':'sources/court/court-base.png','sourceCrop':box,'destination':dest,'size':im.size,'transform':'translation only; native pixels','physicalOpenings':open_rects})
connector('office-porch',(736,520,864,632),(1440,1664),[(1440,1664,128,112)])
connector('classroom-cloister',(736,376,864,504),(608,2136),[(608,2144,96,72),(640,2144,64,120),(640,2176,96,88)])
connector('stage-cloister',(48,396,144,492),(608,2736),[(608,2744,96,80)])
# The only removed office cells are its deliberately artificial outer padding at the main portal.
entry_exception={'x':1440,'y':1664,'width':128,'height':32,'reason':'Remove artificial closed-map padding only at authored main portal to connect parent-approved porch','originalSourceUnchanged':True}
# Original bounded west garden and backmarket. Protect the office interior and top padding.
for ident,folder,prefix in [('west-garden','universe-campus-west-garden','west'),('market','universe-campus-market','market')]:
 root=SHARED/folder
 if not (root/'module.json').exists():continue
 m=read(root/'module.json');origin=tuple(m['worldOrigin'])
 for f,t in [(prefix+'-base.png','base'),(prefix+'-canopy.png','foreground')]:art(ident,root/'layers'/f,t,origin)
 incoming=mask_grid(tuple(m['size']),m['walkablePolygons'],m.get('obstacles',[]));ox,oy=origin
 for iy,row in enumerate(incoming):
  for ix,v in enumerate(row):
   wx,wy=ox+ix*8,oy+iy*8
   inside_office=480<=wx<2976 and 288<=wy<1696
   allowed_left=480<=wx<512 and 288<=wy<1696 and ident=='west-garden' and v==0
   if not inside_office or allowed_left:blocked[wy//8,wx//8]=v
 snapshot(ident,root/'module.json');modules.append({'id':ident,'origin':origin,'size':m['size']})
# Lossless source path joins between west garden, market, and civic public cloister.
# The continuous public cloister is outside civic's physical east wall and outside the court canvas.
connector('market-west-join',(48,400,96,488),(488,216),[(464,224,80,64)])
# Horizontal path receiver at the west garden's south end.
for x in range(416,704,96):connector('west-front-link-'+str(x),(48,400,144,488),(x,1720),[(x,1728,96,64)])
for y in range(1792,2136,64):
 height=min(64,2136-y);connector('civic-public-cloister-'+str(y),(752,520,848,520+height),(608,y),[(608,y,96,height)])
# Keep civic authored east walls solid while joining its transparent outer margin.
# No new entrance is cut through office or civic interior architecture.
# Full source overview retains honest finite footprint and exposed void.
flat=Image.new('RGBA',(W,H),(12,32,41,255))
for name,im in canvas.items():im.save(ROOT/f'layers/campus-{name}.png');flat.alpha_composite(im)
join_source=SHARED/'universe-campus-joins/layers/garden-foundation-joins.png'
if join_source.exists():
 art('joins',join_source,'base',(0,0));canvas['base'].save(ROOT/'layers/campus-base.png');flat.alpha_composite(Image.open(join_source).convert('RGBA'))
flat.save(ROOT/'docs/campus-source-overview.png');flat.resize((1600,1536),Image.Resampling.LANCZOS).save(ROOT/'docs/campus-source-overview-half.png')
mask=Image.fromarray(blocked*255).resize((W,H),Image.Resampling.NEAREST);mask.save(ROOT/'docs/permanent-collision-mask.png')
review=flat.copy();tint=Image.new('RGBA',(W,H),(228,38,74,0));tint.putalpha(mask.point(lambda x:64 if x else 0));review.alpha_composite(tint);review.resize((1600,1536)).save(ROOT/'docs/collision-overview-half.png')
del flat,mask,review,tint
# Lossless 8 px Tiled atlases with full pixel round-trip verification.
gid=1;tilesets=[];layers=[];audit=[]
above=Image.new('RGBA',(W,H))
for name in ('foreground','glass','shade','labels'):above.alpha_composite(canvas[name])
above.save(ROOT/'layers/campus-above.png')
packed={'base':canvas['base'],'above':above}
del canvas; import gc;gc.collect()
for name,im in packed.items():
 if name=='above':layers.append({'id':len(layers)+1,'name':'floorLayer','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':[]})
 cells=[];index={};data=[]
 for y in range(0,H,CELL):
  for x in range(0,W,CELL):
   tile=im.crop((x,y,x+CELL,y+CELL))
   if tile.getchannel('A').getbbox() is None:data.append(0);continue
   blob=tile.tobytes()
   if blob not in index:index[blob]=len(cells);cells.append(tile)
   data.append(gid+index[blob])
 columns=min(128,max(1,len(cells)));nrows=max(1,math.ceil(len(cells)/columns));atlas=Image.new('RGBA',(columns*CELL,nrows*CELL))
 for i,tile in enumerate(cells):atlas.paste(tile,((i%columns)*CELL,(i//columns)*CELL))
 atlas.save(ROOT/f'map/campus-{name}-atlas.png')
 restored=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restored.paste(cells[v-gid],((i%COLS)*CELL,(i//COLS)*CELL))
 bg=Image.new('RGBA',(W,H),(12,32,41,255));assert not ImageChops.difference(Image.alpha_composite(bg,im).convert('RGB'),Image.alpha_composite(bg,restored).convert('RGB')).getbbox()
 tilesets.append({'firstgid':gid,'name':f'campus-{name}','image':f'campus-{name}-atlas.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':CELL,'tileheight':CELL,'margin':0,'spacing':0,'columns':columns,'tilecount':len(cells)})
 layers.append({'id':len(layers)+1,'name':f'campus-{name}','type':'tilelayer','x':0,'y':0,'width':COLS,'height':ROWS,'visible':True,'opacity':1,'data':data})
 audit.append({'layer':name,'nativePixelRoundTrip':True,'sourceHash':sha(ROOT/f'layers/campus-{name}.png'),'distinctTiles':len(cells),'occupiedCells':sum(bool(v) for v in data)});gid+=len(cells)
# Native Tiled animations, consumed by the fork's unchanged AnimatedTiles plugin.
effects=[]; effect_data=[0]*(COLS*ROWS)
if (ROOT/'effects/effects.json').exists():effects=read(ROOT/'effects/effects.json')['effects']
for e in effects:
 frames=[Image.open(ROOT/f).convert('RGBA') for f in e['frames']];ew,eh=frames[0].size;ex,ey=e['origin'];assert all(v%8==0 for v in (ew,eh,ex,ey))
 tiles=[];animations=[];data=[0]*(COLS*ROWS);changed=0;alpha_values=set()
 for yy in range(0,eh,8):
  for xx in range(0,ew,8):
   parts=[f.crop((xx,yy,xx+8,yy+8)) for f in frames]
   if all(p.getchannel('A').getbbox() is None for p in parts):continue
   ids=[]
   for part in parts:ids.append(len(tiles));tiles.append(part);alpha_values.update(part.getchannel('A').getdata())
   animations.append({'id':ids[0],'animation':[{'tileid':i,'duration':e['duration']} for i in ids]})
   data[((ey+yy)//8)*COLS+(ex+xx)//8]=gid+ids[0]
   if any(parts[0].tobytes()!=p.tobytes() for p in parts[1:]):changed+=1
 columns=min(128,max(1,len(tiles)));rows=math.ceil(len(tiles)/columns);atlas=Image.new('RGBA',(columns*8,rows*8))
 for i,part in enumerate(tiles):atlas.paste(part,((i%columns)*8,(i//columns)*8))
 name=e['name'];atlas.save(ROOT/f'map/{name}-atlas.png')
 tilesets.append({'firstgid':gid,'name':name,'image':f'{name}-atlas.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':8,'tileheight':8,'columns':columns,'tilecount':len(tiles),'margin':0,'spacing':0,'tiles':animations})
 layer={'id':0,'name':name,'type':'tilelayer','x':0,'y':0,'width':COLS,'height':ROWS,'visible':True,'opacity':1,'data':data,'properties':props(reducedMotionHide=True)}
 for i,v in enumerate(data):
  if v:
   assert not effect_data[i], 'Animated effect areas overlap';effect_data[i]=v
 audit.append({'layer':name,'animatedCells':len(animations),'varyingCells':changed,'alphaValues':sorted(alpha_values),'source':e,'nativePixelRoundTrip':'integer translated source effect frames'})
 gid+=len(tiles)
if effects:layers.insert(next(i for i,l in enumerate(layers) if l['name']=='floorLayer'),{'id':0,'name':'campus-native-effects','type':'tilelayer','x':0,'y':0,'width':COLS,'height':ROWS,'visible':True,'opacity':1,'data':effect_data,'properties':props(reducedMotionHide=True)})
Image.new('RGBA',(CELL,CELL),(230,45,78,160)).save(ROOT/'map/collision-cell.png')
tilesets.append({'firstgid':gid,'name':'exact-collision','image':'collision-cell.png','imagewidth':CELL,'imageheight':CELL,'tilewidth':CELL,'tileheight':CELL,'margin':0,'spacing':0,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':props(collides=True)}]})
layers.insert(1,{'id':0,'name':'collision-permanent','type':'tilelayer','x':0,'y':0,'width':COLS,'height':ROWS,'visible':True,'opacity':0,'data':[gid if int(v) else 0 for v in blocked.flat],'properties':props(permanent=True,independentOfForeground=True)})
# Static metadata is descriptive: no live room URLs, permissions, broadcasts or claims.
objects=[{'id':1,'name':'start','type':'area','class':'area','x':1488,'y':2896,'width':32,'height':32,'visible':True,'rotation':0,'properties':props(start=True)}]
for z in read(civic/'module.json')['zones']:objects.append({'id':len(objects)+1,'name':z['id'],'type':'campus-zone','x':z['x'],'y':z['y']+1792,'width':z['width'],'height':z['height'],'visible':True,'rotation':0,'properties':props(liveServiceConfigured=False)})
layers.append({'id':0,'name':'campus-zones-offline','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':objects})
for i,l in enumerate(layers):l['id']=i+1
status='finite source assembly; runtime acceptance pending'
tmj={'compressionlevel':-1,'width':COLS,'height':ROWS,'infinite':False,'layers':layers,'nextlayerid':len(layers)+1,'nextobjectid':len(objects)+1,'orientation':'orthogonal','renderorder':'right-down','tiledversion':'1.11.2','tilewidth':CELL,'tileheight':CELL,'tilesets':tilesets,'type':'map','version':'1.10','backgroundcolor':'#0c2029','properties':props(nativeWorldWidth=W,nativeWorldHeight=H,artScale=1,wokaScale=1,status=status)}
(ROOT/'map/magical-campus.tmj').write_text(json.dumps(tmj,separators=(',',':'))+'\n')
physics=dict(tmj);physics['layers']=[next(l for l in layers if l['name']=='collision-permanent')];physics['tilesets']=[tilesets[-1]];physics['nextlayerid']=2
(ROOT/'map/campus-physics.tmj').write_text(json.dumps(physics,separators=(',',':'))+'\n')
write(ROOT/'map/collision-grid.json',{'width':COLS,'height':ROWS,'tileSize':CELL,'blockedIndices':[i for i,v in enumerate(blocked.flat) if int(v)],'permanent':True})
manifest={'status':status,'world':[W,H],'tileSize':CELL,'avatar':{'frame':[32,32],'scale':1,'body':[-8,0,16,16],'immovable':True},'modules':modules,'sourceAudit':sources,'layerAudit':audit,'connectors':connectors,'officePaddingException':entry_exception,'noArtRescaling':True,'noDynamicCollision':True,'noAvatarDependentMask':True,'semanticSourceLayersPreserved':True,'fixedAboveComposition':['foreground','glass','shade','labels'],'officeLeftPaddingException':{'x':480,'y':288,'width':32,'height':1408,'onlyWhereWestPathIsOpen':True},'voidCollides':True,'separateGateMap':True,'liveRoomURLsAssigned':False,'nativeAudioBridgeEnabled':False}
write(ROOT/'map/compile-manifest.json',manifest)
print(json.dumps({'status':status,'modules':[x['id'] for x in modules],'world':[W,H],'blockedCells':int(blocked.sum()),'distinctArtCells':gid-1,'roundTripLayers':len(audit)},indent=2))
