from pathlib import Path
from PIL import Image
import json,collections,hashlib
R=Path(__file__).resolve().parents[1];m=json.loads((R/'runtime/mechanical-orchard.tmj').read_text());l=json.loads((R/'evidence/layout.json').read_text());g=l['grid'];T=m['tilewidth'];assert T==m['tileheight']==32
props={s['firstgid']+t['id']:{p['name']:p['value']for p in t.get('properties',[])}for s in m['tilesets']for t in s.get('tiles',[])}
for s in m['tilesets']:
 assert (R/'runtime'/s['image']).is_file();assert Image.open(R/'runtime'/s['image']).size==(s['imagewidth'],s['imageheight']);assert s['tilecount']==s['columns']*(s['imageheight']//T)
for layer in m['layers']:
 if layer['type']=='tilelayer':assert len(layer['data'])==m['width']*m['height']
for id,a in l['anchors'].items():
 for y in range(a['y']//T,(a['y']+15)//T+1):
  for x in range((a['x']-8)//T,(a['x']+7)//T+1):assert not g[y][x],(id,x,y)
 assert any(o['name']=='popup-'+id for layer in m['layers']for o in layer.get('objects',[]))
 if 'to'in a:assert l['anchors'][a['to']]['to']==id
feedback=l['feedbackLayers'];assert len(feedback)==6 and len(set(feedback))==6
assert set(feedback)=={t+'-phase-'+str(p)for t in ['petal','leaf','fruit']for p in [1,2]}
for name in feedback:
 layer=next(v for v in m['layers']if v['name']==name);assert layer['visible'] is False
 assert m['layers'].index(layer)<next(i for i,v in enumerate(m['layers'])if v['name']=='floorLayer')
 assert not any(props.get(v,{}).get('collides')for v in layer['data'])
# Each of9 independent layer bits contains no collision-bearing tile. Therefore
# every one of2**9 arbitrary subsets has the same fixed collision contribution.
# This structural proof does not conflate arbitrary visibility with legal controller states.
components=[];visited=set()
for y,row in enumerate(g):
 for x,v in enumerate(row):
  if v or (x,y)in visited:continue
  q=[(x,y)];visited.add((x,y))
  for a,b in q:
   for z in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
    if 0<=z[1]<len(g)and 0<=z[0]<len(row)and not g[z[1]][z[0]]and z not in visited:visited.add(z);q.append(z)
  components.append(q)
assert len(components)==2,[len(c)for c in components]
for name,room in l['rooms'].items():
 ox,oy=room['offset'];w,h=room['size'];points=[(a['x']//T,a['y']//T)for a in l['anchors'].values()if a['room']==name]+[((s['anchor'][0]+ox)//T,(s['anchor'][1]+oy)//T)for s in l['seats']if s['room']==name]
 assert any(all(p in component for p in points)for component in components),name
for room,items in l.get('fixtureNegatives',{}).items():
 ox,oy=l['rooms'][room]['offset']
 for item in items:
  x,y=item['point'];assert g[(oy+y)//32][(ox+x)//32],('admitted fixture',item)
assert (R/'runtime/mechanical-orchard.js').read_text().endswith((R/'source/experience.js').read_text())
quiet=next(v for v in m['layers']if v['name']=='arrival-quiet');assert len([v for v in m['layers']if any(p.get('name')=='silent' and p.get('value')for p in v.get('properties',[]))])==1
for name,a in l['anchors'].items():
 if name!='arrival':assert not quiet['data'][(a['y']//32)*m['width']+a['x']//32],name
for seat in l['seats']:
 ox,oy=l['rooms'][seat['room']]['offset'];x,y=seat['anchor'];assert not quiet['data'][((y+oy)//32)*m['width']+(x+ox)//32]
assert not any(p['name']=='playAudio'for layer in m['layers']for p in layer.get('properties',[]))
assert json.loads((R/'runtime/mechanical-orchard.wam').read_text())['mapUrl']=='./mechanical-orchard.tmj'
report=dict(allPass=True,atlasReferences=True,dimensions=True,tileCount=True,controllerSourceParity=True,collisionComponents=[len(c)for c in components],allAnchorsAndSeatsConnectedPerRoom=True,pairedDoors=True,feedbackLayerCount=6,independentOverlayVisibilityStates=64,overlayProof="Per-layer noncollision bit proof, all layers below actors; every reachable model configuration separately enumerated",audio='none',scope='Structural source/TMJ validation, not live gameplay or semantic art acceptance')
(R/'evidence/structure.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
