"""Standard32px candidate: native artwork and conservative4x4 authored collision coalescing."""
from pathlib import Path
from PIL import Image,ImageChops
import numpy as np,json,math,hashlib
R=Path(__file__).resolve().parents[1];O=R/'map32';O.mkdir(exist_ok=True);W,H=json.loads((R/'map/compile-manifest.json').read_text())['world'];T=32;C,N=W//T,H//T
read=lambda p:json.loads(Path(p).read_text())
def props(**kw):return [{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string','value':v} for k,v in kw.items()]
def layer(name,data):return {'id':0,'name':name,'type':'tilelayer','x':0,'y':0,'width':C,'height':N,'visible':True,'opacity':1,'data':data}
src=read(R/'map/magical-campus.tmj');g=read(R/'map/collision-grid.json');b=np.zeros((H//8,W//8),np.uint8);b.flat[g['blockedIndices']]=1;coarse=b.reshape(N,4,C,4).max((1,3));gid=1;sets=[];layers=[];audit=[]
for name in ['base','above']:
 if name=='above':layers.append({'id':0,'name':'floorLayer','type':'objectgroup','x':0,'y':0,'visible':True,'opacity':1,'draworder':'topdown','objects':[]})
 im=Image.open(R/f'layers/campus-{name}.png').convert('RGBA');cells=[];lookup={};data=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   tile=im.crop((x,y,x+T,y+T));blob=tile.tobytes()
   if tile.getchannel('A').getbbox() is None:data.append(0);continue
   if blob not in lookup:lookup[blob]=len(cells);cells.append(tile)
   data.append(gid+lookup[blob])
 restored=Image.new('RGBA',(W,H))
 for i,v in enumerate(data):
  if v:restored.paste(cells[v-gid],((i%C)*T,(i//C)*T))
 bg=Image.new('RGBA',(W,H),(12,32,41,255));assert not ImageChops.difference(Image.alpha_composite(bg,im).convert('RGB'),Image.alpha_composite(bg,restored).convert('RGB')).getbbox()
 for page,start in enumerate(range(0,len(cells),1024)):
  parts=cells[start:start+1024];cols=min(32,max(1,len(parts)));rows=math.ceil(len(parts)/cols);atlas=Image.new('RGBA',(cols*T,rows*T))
  for i,cell in enumerate(parts):atlas.paste(cell,((i%cols)*T,(i//cols)*T))
  page_name=f'campus-{name}-p{page}';atlas.save(O/f'{page_name}.png');assert atlas.width<=1024 and atlas.height<=1024
  sets.append({'firstgid':gid+start,'name':page_name,'image':f'{page_name}.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':cols,'tilecount':len(parts)})
 layers.append(layer(f'campus-{name}',data));audit.append({'layer':name,'nativePixelRoundTrip':True,'tileCount':len(cells)});gid+=len(cells)
from pack_effects import pack_effect
effect_data={name:[0]*(C*N) for name in ['below','above']}
for effect in read(R/'effects/effects.json')['effects']:
 group=effect.get('layer','below')
 if group not in effect_data:raise ValueError('Effect layer must be below or above')
 pages,cells,gid,summary=pack_effect(effect,R,O,gid,(W,H),T)
 sets.extend(pages);audit.append(summary)
 for cell,value in cells.items():
  if effect_data[group][cell]:raise ValueError(f'Overlapping {group} effects at cell {cell}')
  effect_data[group][cell]=value
layers.insert(1,layer('campus-native-effects',effect_data['below']))
if any(effect_data['above']):layers.append(layer('campus-overhead-effects',effect_data['above']))
Image.new('RGBA',(T,T),(224,36,64,100)).save(O/'collision-cell.png');sets.append({'firstgid':gid,'name':'exact-collision','image':'collision-cell.png','imagewidth':T,'imageheight':T,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':props(collides=True)}]});collision=layer('collision-permanent',[gid if v else 0 for v in coarse.flat]);collision['opacity']=0;layers.insert(2,collision)
layers+= [l for l in src['layers'] if l['type']=='objectgroup' and l['name']!='floorLayer']
for i,l in enumerate(layers):l['id']=i+1
m=dict(src);m.update(width=C,height=N,tilewidth=T,tileheight=T,layers=layers,tilesets=sets,nextlayerid=len(layers)+1);m['properties']=props(nativeWorldWidth=W,nativeWorldHeight=H,artScale=1,wokaScale=1,status='Standard32px map candidate; source-route checks complete, live client acceptance pending')
return_metadata=R/'sources/campus-return/prepare_metadata.py'
if False and return_metadata.exists():
 import importlib.util,shutil
 spec=importlib.util.spec_from_file_location('campus_return_metadata',return_metadata);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);m=module.prepare(m);(O/'scripts').mkdir(exist_ok=True);shutil.copy2(return_metadata.parent/'campus-return.js',O/'scripts/campus-return.js')
(O/'asset-manifest.json').write_text(json.dumps({'tilesets':[{'name':ts['name'],'image':ts['image'],'size':[ts['imagewidth'],ts['imageheight']]} for ts in sets]},indent=2)+'\n');assert all(ts['imagewidth']<=2048 and ts['imageheight']<=2048 for ts in sets)
(O/'magical-campus.tmj').write_text(json.dumps(m,separators=(',',':'))+'\n');(O/'collision-grid.json').write_text(json.dumps({'width':C,'height':N,'tileSize':T,'blockedIndices':[i for i,v in enumerate(coarse.flat) if v],'permanent':True},separators=(',',':'))+'\n')
manifest=read(R/'map/compile-manifest.json');manifest.update(artifactArtState='Preserved lush08 materials plus bounded fountain/shore repairs; exact source-to-native32 atlas round trip',status='Standard32px map candidate; source-route checks complete, live client acceptance pending',tileSize=32,layerAudit=audit,coalescing={'sourceCell':8,'targetCell':32,'policy':'Solid if any of sixteen8px cells is solid; no collision erasure','original8pxWorldPixelsBlocked':int(b.sum())*64,'additionalBlockedWorldPixels':int(coarse.sum())*1024-int(b.sum())*64,'noArtRescaling':True},nativeTileLayerCount=sum(x['type']=='tilelayer' for x in layers),phaserTileObjects=C*N*sum(x['type']=='tilelayer' for x in layers));(O/'compile-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'tileSize':T,'tileObjects':manifest['phaserTileObjects'],'coalescing':manifest['coalescing'],'audit':audit},indent=2))
