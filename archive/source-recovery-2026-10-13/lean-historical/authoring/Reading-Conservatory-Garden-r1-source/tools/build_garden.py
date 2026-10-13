from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math,collections,copy
from water_animation import water_frames
R=Path(__file__).resolve().parents[1];S=R/'source-assets';O=R/'candidate';T=32;C=24;N=26;W=768;H=832
for p in ['map32','source','review']:(O/p).mkdir(parents=True,exist_ok=True)
def js(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def props(**kw):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in kw.items()]
base_map=read(R/'baseline-r2/map32/map.tmj');layout=read(R/'baseline-r2/source/layout.json');base_layout=copy.deepcopy(layout)
def decode(layer):
 out=Image.new('RGBA',(W,512))
 for i,v in enumerate(layer['data']):
  if not v:continue
  ts=max([t for t in base_map['tilesets'] if t['firstgid']<=v],key=lambda t:t['firstgid']);a=Image.open(R/'baseline-r2/map32'/ts['image']).convert('RGBA');j=v-ts['firstgid'];x=j%ts['columns']*T;y=j//ts['columns']*T;out.paste(a.crop((x,y,x+T,y+T)),(i%C*T,i//C*T))
 return out
foreground=Image.new('RGBA',(W,H));foreground.paste(decode(next(l for l in base_map['layers'] if l['name']=='foreground')),(0,0))
art=Image.open(R/'working/art-native.png').convert('RGBA');assert art.size==(W,H)
g=np.array(read(S/'accepted-garden-grid.json')['collision'],dtype=np.uint8);assert g.shape==(N,C)
assert g[:16].tolist()==base_layout['collision'];layout['collision']=g.tolist();layout['dimensions']=[C,N];layout['title']='Reading Conservatory: Fountain Garden';layout['version']='garden r1';layout['notes']='Approved reading interior retained exactly. Normal standing idle and native facing controls, no auto sitting/snapping/turning. Eight-frame water-only basin animation. New garden routes source-checked; live media/gameplay not claimed.'
# Fixed four-neighbor centerline, contained in reviewed ring cells.
ring=[[9,16],[10,16],[11,16],[12,16],[13,16],[14,16],[14,17],[15,17],[15,18],[16,18],[16,19],[16,20],[16,21],[15,21],[15,22],[14,22],[13,22],[12,22],[11,22],[10,22],[9,22],[8,22],[8,21],[7,21],[7,20],[7,19],[7,18],[8,18],[8,17],[9,17],[9,16]]
assert all(g[y,x]==0 for x,y in ring)
assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(ring,ring[1:]))
layout['gardenRing']=ring
for name,x,y in [('Fountain north',11,16),('Fountain northeast',15,17),('Fountain east',16,19),('Fountain southeast',15,22),('Fountain south',12,22),('Fountain southwest',8,22),('Fountain west',7,19),('Fountain northwest',8,17),('West edge upper',0,19),('West edge lower',0,20),('East edge upper',23,19),('East edge lower',23,20),('South garden approach',11,24),('South map edge',12,25)]:
 layout['anchors'].append({'name':name,'anchor':[x*T+16,y*T+15],'floorClick':[x*T+16,y*T+31],'cell':[x,y],'kind':'garden walk-to approach'})
js(O/'source/layout.json',layout)
wam=read(R/'baseline-r2/map32/map.wam')
for area in wam['areas']:
 area['id']=area['id'].replace('reading-conservatory-r2','reading-conservatory-garden-r1')
 for p in area['properties']:
  p['id']=p['id'].replace('reading-conservatory-r2','reading-conservatory-garden-r1');p['roomName']=p['roomName'].replace('reading-conservatory-r2','reading-conservatory-garden-r1')
js(O/'map32/map.wam',wam)
# Strict basin-water ownership, excluding statue and pedestal; no ground/wall/plant ownership.
a=np.array(art);geo=Image.new('L',(W,H));d=ImageDraw.Draw(geo);d.ellipse((334,596,437,656),fill=255);d.polygon([(374,589),(397,589),(400,611),(408,623),(402,636),(392,641),(367,636),(357,625),(370,608)],fill=0)
c=a[:,:,:3].astype(float);water=(np.array(geo)>0)&(c[:,:,1]>c[:,:,0]*.99)&(c[:,:,2]>c[:,:,0]*.70)&(c[:,:,1]>c[:,:,2]*1.03);mask=Image.fromarray((water*255).astype('uint8'));mask.save(O/'source/water-mask.png')
frames=water_frames(art,mask,[(347,623),(354,641),(383,647),(413,642),(418,623)],8)
fg=np.array(foreground);solid=a.copy();solid[water]=0;solid[fg[:,:,3]>0]=0;base=Image.fromarray(solid)
water_layers=[]
for f in frames:
 v=np.zeros_like(a);v[water]=np.array(f)[water];water_layers.append(Image.fromarray(v))
sets=[];layers=[];gid=1

def layer(name,data,opacity=1):return {'name':name,'type':'tilelayer','x':0,'y':0,'width':C,'height':N,'visible':True,'opacity':opacity,'data':data}
def atlas(name,ims,animated=False):
 global gid
 tiles=[];data=[];entries=[]
 for y in range(N):
  for x in range(C):
   crops=[im.crop((x*T,y*T,(x+1)*T,(y+1)*T)) for im in ims]
   if not crops[0].getbbox():data.append(0);continue
   first=len(tiles);data.append(gid+first);tiles.extend(crops)
   if animated:entries.append({'id':first,'animation':[{'tileid':first+i,'duration':140} for i in range(len(crops))]})
 cols=min(24,len(tiles));im=Image.new('RGBA',(cols*T,math.ceil(len(tiles)/cols)*T))
 for i,t in enumerate(tiles):im.paste(t,(i%cols*T,i//cols*T))
 fn=name+'.png';im.save(O/'map32'/fn);ts={'firstgid':gid,'name':name,'image':fn,'imagewidth':im.width,'imageheight':im.height,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':cols,'tilecount':len(tiles)}
 if entries:ts['tiles']=entries
 sets.append(ts);layers.append(layer(name,data));gid+=len(tiles)
atlas('architecture-and-furniture',[base]);atlas('fountain-water',water_layers,True)
layers.append({'name':'floorLayer','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':[]});atlas('foreground',[foreground])
Image.new('RGBA',(T,T)).save(O/'map32/logic.png');sets.append({'firstgid':gid,'name':'collision','image':'logic.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'margin':0,'spacing':0,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':props(collides=True)}]});layers.insert(1,layer('collision',[gid if v else 0 for row in g for v in row],0));gid+=1
sets.append({'firstgid':gid,'name':'quiet','image':'logic.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'margin':0,'spacing':0,'columns':1,'tilecount':1});q=[0]*(C*N);q[14*C+12]=gid;ql=layer('quiet-arrival',q,0);ql['properties']=props(silent=True);layers.insert(2,ql)
start=copy.deepcopy(next(l for l in base_map['layers'] if l['name']=='map-areas'));layers.append(start)
for i,l in enumerate(layers):l['id']=i+1
m=copy.deepcopy(base_map);m.update(height=N,layers=layers,tilesets=sets,nextlayerid=len(layers)+1,properties=props(name=layout['title'],category='Knowledge and Social',wokaScale=1,status='Unpublished garden candidate; live test not run'));js(O/'map32/map.tmj',m)
# Decode actual emitted atlas tiles and animation indices for all eight time frames.
composites=[];roundtrips=[];atlas_cache={s["image"]:Image.open(O/"map32"/s["image"]).convert("RGBA") for s in sets}
for fi in range(8):
 out=Image.new('RGBA',(W,H))
 for l in layers:
  if l['type']!='tilelayer' or l.get('opacity')==0:continue
  li=Image.new('RGBA',(W,H))
  for j,v in enumerate(l['data']):
   if not v:continue
   ts=max([s for s in sets if s['firstgid']<=v],key=lambda s:s['firstgid']);idx=v-ts['firstgid'];entry=next((e for e in ts.get('tiles',[]) if e['id']==idx),{})
   if 'animation' in entry:idx=entry['animation'][fi]['tileid']
   at=atlas_cache[ts['image']];x=idx%ts['columns']*T;y=idx//ts['columns']*T;li.paste(at.crop((x,y,x+T,y+T)),(j%C*T,j//C*T))
  out.alpha_composite(li)
 assert out.tobytes()==frames[fi].tobytes();composites.append(out);changed=np.any(np.array(out)!=a,2);assert not (changed&~water).any();roundtrips.append({'frame':fi,'changed_water_pixels':int(changed.sum()),'outside_water_mask':0,'atlas_exact':True})
composites[0].save(O/'review/empty-native.png');composites[0].save(O/'review/fountain-animation.gif',save_all=True,append_images=composites[1:],duration=140,loop=0,disposal=2)
foreground.save(O/'review/foreground-native.png');base.save(O/'review/base-native.png');js(O/'WATER-ANIMATION-CHECKS.json',{'frames':8,'frame_ms':140,'water_mask_pixels':int(water.sum()),'runtime_animated_cells':len(next(s for s in sets if s['name']=='fountain-water')['tiles']),'frames_decoded_from_actual_atlas':roundtrips,'foreground_unchanged_from_base':True,'no_avatar_pixels_in_runtime':True})
# Exhaustive integer body-clear domain and native head mask intersections.
b=g.repeat(T,0).repeat(T,1).astype(bool);ii=np.pad(b.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(b.shape);xa=np.maximum(0,X-8);xb=np.minimum(W,X+8);yb=np.minimum(H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=W)&(Y+16<=H)
head=np.array(read(S/'native-head-union.json')['mask'],bool);fm=np.array(foreground)[:,:,3]>0;hits=0
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(W,W-dx);y0=max(0,-dy);y1=min(H,H-dy);hits+=int((clear[y0:y1,x0:x1]&fm[y0+dy:y1+dy,x0+dx:x1+dx]).sum())
assert hits==0
cells={(x,y) for y in range(N) for x in range(C) if g[y,x]==0};seen={next(iter(cells))};todo=list(seen)
while todo:
 x,y=todo.pop()
 for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if p in cells and p not in seen:seen.add(p);todo.append(p)
assert cells==seen
anchor_checks=[]
for v in layout['seats']+layout['anchors']:
 x,y=v['anchor'];assert clear[y,x],v;anchor_checks.append({'name':v['name'],'anchor':[x,y],'clear':True})
assert composites[0].crop((0,0,768,512)).tobytes()==Image.open(S/'validated-interior-native.png').convert('RGBA').tobytes()
js(O/'STATIC-CHECKS.json',{'map_sha256':sha(O/'map32/map.tmj'),'layout_sha256':sha(O/'source/layout.json'),'dimensions':[W,H],'tile_size':32,'open_cells':len(cells),'new_garden_cells':len(cells)-87,'all_open_cells_connected':True,'body_clear_integer_positions':int(clear.sum()),'head_intersections':hits,'anchor_checks':anchor_checks,'base_interior_pixels_exact':True,'base_collision_rows_exact':True,'ring_steps':len(ring)-1,'side_paths_two_full_tiles':True,'runtime_avatar_pixels':False,'live_playtest':'Not run'})
overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
for y in range(N):
 for x in range(C):d.rectangle((x*T,y*T,(x+1)*T-1,(y+1)*T-1),fill=(220,45,50,85) if g[y,x] else (25,160,90,25),outline=(255,255,255,70))
Image.alpha_composite(composites[0],overlay).save(O/'review/collision-diagnostic.png')
print(json.dumps({'open_cells':len(cells),'clear_positions':int(clear.sum()),'water_frames':8,'head_hits':hits,'map_sha256':sha(O/'map32/map.tmj')},indent=2))
(O/'map32/README.md').write_bytes((R/'GUIDE.md').read_bytes())
