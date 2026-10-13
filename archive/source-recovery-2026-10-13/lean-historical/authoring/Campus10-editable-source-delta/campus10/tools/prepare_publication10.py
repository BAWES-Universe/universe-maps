"""Reuse preserved09 pixel-identical native tiles for a lean additive10 URL.

The independently runnable map32 bundle remains unchanged. This publication
derivative references the preserved09 assets and is exhaustively equivalent
per cell/frame, including collision membership and native audio configuration.
"""
from pathlib import Path
from PIL import Image
import json, hashlib, copy, math, shutil

R=Path(__file__).resolve().parents[1]
B=Path('/workspace/shared/magical-campus-standard32-09/map32')
S=R/'map32';P=R/'publication/v10';O=P/'map32';O.mkdir(parents=True,exist_ok=True)
old=json.loads((B/'magical-campus.tmj').read_text());current=json.loads((S/'magical-campus.tmj').read_text())
result=copy.deepcopy(current);T=32
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
blob=lambda b:hashlib.sha256(b).digest()

old_sets=[t for t in old['tilesets'] if t['name'].startswith(('campus-base-','campus-above-')) or t['name']=='exact-collision']
pool={};old_images={}
for ts in old_sets:
 im=Image.open(B/ts['image']).convert('RGBA');old_images[ts['name']]=im
 if ts['name']=='exact-collision':continue
 for i in range(ts['tilecount']):
  x=i%ts['columns']*T;y=i//ts['columns']*T;b=im.crop((x,y,x+T,y+T)).tobytes()
  pool.setdefault(blob(b),(ts['firstgid']+i,ts['name'],b))
new_start=max(t['firstgid']+t['tilecount'] for t in old_sets)
current_images={t['name']:Image.open(S/t['image']).convert('RGBA') for t in current['tilesets']}
current_sets=sorted(current['tilesets'],key=lambda t:t['firstgid'])
cache={}
def source_tile(gid):
 if gid not in cache:
  ts=next(t for t in reversed(current_sets) if gid>=t['firstgid']);i=gid-ts['firstgid']
  assert i<ts['tilecount'];x=i%ts['columns']*T;y=i//ts['columns']*T
  cache[gid]=current_images[ts['name']].crop((x,y,x+T,y+T)).tobytes()
 return cache[gid]

new_tiles=[];new_pool={};used_old=set();static_cell_checks=0
for layer in result['layers']:
 if layer['name'] not in ['campus-base','campus-above']:continue
 for i,gid in enumerate(layer['data']):
  if not gid:continue
  b=source_tile(gid);h=blob(b)
  if h in pool:
   target,name,expected=pool[h];assert expected==b;used_old.add(name)
  else:
   if h not in new_pool:new_pool[h]=len(new_tiles);new_tiles.append(b)
   index=new_pool[h];assert new_tiles[index]==b;target=new_start+index
  layer['data'][i]=target;static_cell_checks+=1

sets=[];dependencies=[]
for ts in old_sets:
 if ts['name'] not in used_old and ts['name']!='exact-collision':continue
 q=copy.deepcopy(ts);q['image']='../../v9/map32/'+ts['image'];sets.append(q)
 dependencies.append({'url':q['image'],'servedPath':'butterfly-town/v9/map32/'+ts['image'],
                      'localPath':str(B/ts['image']),'sha256':sha(B/ts['image']),'bytes':(B/ts['image']).stat().st_size})
for page,start in enumerate(range(0,len(new_tiles),1024)):
 parts=new_tiles[start:start+1024];cols=min(32,len(parts));image=Image.new('RGBA',(cols*T,math.ceil(len(parts)/cols)*T))
 for i,b in enumerate(parts):image.paste(Image.frombytes('RGBA',(T,T),b),(i%cols*T,i//cols*T))
 name=f'campus10-changed-p{page}';image.save(O/(name+'.png'))
 sets.append({'firstgid':new_start+start,'name':name,'image':name+'.png','imagewidth':image.width,'imageheight':image.height,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':cols,'tilecount':len(parts)})
next_gid=new_start+len(new_tiles)
effect_layer=next(l for l in result['layers'] if l['name']=='campus-native-effects')
original_effects=list(effect_layer['data']);animation_frames=0
for ts in current_sets:
 if not any('animation' in q for q in ts.get('tiles',[])):continue
 q=copy.deepcopy(ts);q['firstgid']=next_gid;sets.append(q);shutil.copy2(S/ts['image'],O/ts['image'])
 for i,gid in enumerate(original_effects):
  if ts['firstgid']<=gid<ts['firstgid']+ts['tilecount']:
   local=gid-ts['firstgid'];effect_layer['data'][i]=next_gid+local
   animation=next(t['animation'] for t in ts['tiles'] if t['id']==local)
   assert next(t['animation'] for t in q['tiles'] if t['id']==local)==animation
   animation_frames+=len(animation)
 assert (S/ts['image']).read_bytes()==(O/q['image']).read_bytes()
 next_gid+=ts['tilecount']
collision=next(t for t in old_sets if t['name']=='exact-collision')
layer=next(l for l in result['layers'] if l['name']=='collision-permanent')
layer['data']=[collision['firstgid'] if g else 0 for g in layer['data']]
assert [bool(g) for g in layer['data']]==[bool(g) for g in next(l for l in current['layers'] if l['name']==layer['name'])['data']]
for layer in result['layers']:
 for obj in layer.get('objects',[]):
  for prop in obj.get('properties',[]):
   if prop['name']=='playAudio':
    rel=prop['value'];assert sha(S/rel)==sha(B/rel);prop['value']='../../v9/map32/'+rel
    if not any(d['url']==prop['value'] for d in dependencies):dependencies.append({'url':prop['value'],'servedPath':'butterfly-town/v9/map32/'+rel,'localPath':str(B/rel),'sha256':sha(B/rel),'bytes':(B/rel).stat().st_size})
result['tilesets']=sorted(sets,key=lambda q:q['firstgid'])
(O/'magical-campus.tmj').write_text(json.dumps(result,separators=(',',':'))+'\n')
assert len({g for t in sets for g in range(t['firstgid'],t['firstgid']+t['tilecount'])})==sum(t['tilecount'] for t in sets)
report={'sourceTestedMapSHA256':sha(S/'magical-campus.tmj'),'publicationMapSHA256':sha(O/'magical-campus.tmj'),
 'staticCellPixelChecks':static_cell_checks,'animationFrameReferencesPreserved':animation_frames,
 'collisionMembershipIdentical':True,'objectGeometryAndPropertiesUnchangedExceptAudioURLs':True,
 'sharedPreserved09Files':dependencies,'newStaticTiles':len(new_tiles),'newStaticAtlasPages':math.ceil(len(new_tiles)/1024),
 'definedRgbaTextureBytes':sum(t['imagewidth']*t['imageheight']*4 for t in sets),
 'newRuntimeFiles':[{'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(O.iterdir())if p.is_file()]}
(P/'equivalence-and-dependencies.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['sharedPreserved09Files','newRuntimeFiles']},indent=2))
print(json.dumps({'sharedFiles':len(dependencies),'sharedBytes':sum(r['bytes']for r in dependencies),'newFiles':len(report['newRuntimeFiles']),'newBytes':sum(r['bytes']for r in report['newRuntimeFiles'])}))
