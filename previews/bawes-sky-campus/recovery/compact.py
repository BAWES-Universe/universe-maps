"""Lower Tile-object memory without resizing pixels or changing collision/interactive layers."""
from pathlib import Path
from PIL import Image
import json,bisect,hashlib,copy
R=Path(__file__).resolve().parent;src=R/'package';out=R/'compact';(out/'art').mkdir(parents=True,exist_ok=True)
m=json.loads((src/'campus.tmj').read_text());original=copy.deepcopy(m);sets=m['tilesets'];starts=[s['firstgid'] for s in sets];images={};cache={}
def tile(g):
 if not g:return Image.new('RGBA',(16,16))
 if g not in cache:
  s=sets[bisect.bisect_right(starts,g)-1];n=g-s['firstgid'];name=s['image']
  if name not in images:images[name]=Image.open(src/name).convert('RGBA')
  x=s.get('margin',0)+(n%s['columns'])*(16+s.get('spacing',0));y=s.get('margin',0)+(n//s['columns'])*(16+s.get('spacing',0))
  cache[g]=images[name].crop((x,y,x+16,y+16))
 return cache[g]
group={'scenery-and-campus','cafe-timber','alcove-floor','audience-shadows','campus-furniture','native-cafe-region'}
layers=[l for l in m['layers'] if l['name'] in group];byname={l['name']:l for l in m['layers']}
# Verify compositing does not cross any interactive or dynamically visible artwork.
for i,l in enumerate(m['layers']):
 if l['name'] not in group:continue
 for other in m['layers'][:i]:
  if other['type']!='tilelayer' or other['name'] in group:continue
  for a,b in zip(l['data'],other['data']):
   if a and b:
    from PIL import ImageChops
    assert not ImageChops.multiply(tile(a).getchannel('A'),tile(b).getchannel('A')).getbbox(),(l['name'],other['name'])
first=max(s['firstgid']+s['tilecount'] for s in sets);newtiles=[];composite_cache={};data=[]
for values in zip(*(l['data'] for l in layers)):
 active=tuple(g for g in values if g)
 if not active:data.append(0);continue
 if len(active)==1 or tile(active[-1]).getchannel('A').getextrema()==(255,255):data.append(active[-1]);continue
 if active not in composite_cache:
  im=Image.new('RGBA',(16,16))
  for g in active:im.alpha_composite(tile(g))
  composite_cache[active]=first+len(newtiles);newtiles.append(im)
 data.append(composite_cache[active])
for offset in range(0,len(newtiles),4096):
 batch=newtiles[offset:offset+4096];rows=(len(batch)+63)//64;atlas=Image.new('RGBA',(1024,rows*16))
 for i,im in enumerate(batch):atlas.paste(im,((i%64)*16,(i//64)*16))
 name=f'art/composite-{offset}.png';atlas.save(out/name)
 m['tilesets'].append(dict(firstgid=first+offset,name=f'composite-{offset}',image=name,imagewidth=1024,imageheight=rows*16,tilewidth=16,tileheight=16,tilecount=len(batch),columns=64))
empty={'campus-chair-fronts','cafe-foreground','alcove-foreground','audience-fronts','campus-bench-fronts','reception-activity'}
for name in empty:assert not any(byname[name]['data'])
unused={'beverage-steam-0','beverage-steam-1','beverage-steam-2'}
runtime=(src/'runtime.js').read_text()
for name in unused:assert not byname[name]['visible'] and name not in runtime
m['layers']=[l for l in m['layers'] if l['name'] not in empty|unused|(group-{'scenery-and-campus'})]
byname['scenery-and-campus']['data']=data
used={g for l in m['layers'] if l['type']=='tilelayer' for g in l['data'] if g}
kept=[]
for s in m['tilesets']:
 if not any(s['firstgid']<=g<s['firstgid']+s['tilecount'] for g in used):continue
 kept.append(s)
 if (src/s['image']).exists():(out/s['image']).write_bytes((src/s['image']).read_bytes())
m['tilesets']=kept
(out/'campus.tmj').write_text(json.dumps(m,separators=(',',':')));(out/'runtime.js').write_text(runtime)
report={'sourceLayers':len(original['layers']),'packagedLayers':len(m['layers']),'removedEmptyLayers':sorted(empty),'removedInactiveUnreferencedLayers':sorted(unused),'mergedBackgroundLayers':sorted(group),'interleavingPixelsDisjoint':True,'compositedEdgeTiles':len(newtiles),'nativeTileSize':16,'runtimeIdentical':True,'unchangedInteractiveLayers':all(l==next(x for x in original['layers'] if x['name']==l['name']) for l in m['layers'] if l['name']!='scenery-and-campus')}
(R/'evidence/compact-equivalence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
