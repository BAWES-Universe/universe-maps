from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];m=json.loads((R/'runtime/moonlit.tmj').read_text());checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
L={l['name']:l for l in m['layers']};W,H=m['width'],m['height']
check('native32 finite map',m['tilewidth']==m['tileheight']==32 and not m['infinite'])
check('all layer arrays match map',all(len(l['data'])==W*H for l in L.values() if l['type']=='tilelayer'))
check('door fail-open at authoring',not L['door-collision']['visible'] and L['door-frame-4']['visible'])
check('closed door exactly two threshold cells',sum(bool(x) for x in L['door-collision']['data'])==2)
check('no transport/external script assets',all(p['name'] not in ('exitUrl','exitSceneUrl') for p in m['properties']))
for ts in m['tilesets']:check('local asset '+ts['image'],(R/'runtime'/ts['image']).is_file() and '://' not in ts['image'])
check('roof starts hidden',all(not L['roof-alpha-'+str(i)]['visible'] for i in range(1,5)))
roof_gids=set(L['roof-alpha-4']['data'])-{0};colliding={ts['firstgid']+t['id'] for ts in m['tilesets'] for t in ts.get('tiles',[]) if any(p.get('name')=='collides' and p.get('value') for p in t.get('properties',[]))}
check('decorative roof does not collide',not roof_gids&colliding)
check('audio metadata does not collide',not set(L['native-audio']['data'])&colliding)
check('silent audio default',not any(p['name']=='playAudio' for l in m['layers'] for p in l.get('properties',[])))
check('glass never uses roof layers',L['persistent-glass-frame']['visible'])
check('native water has four frames',len(next(t for t in m['tilesets'] if t['name']=='water-motion')['tiles'][0]['animation'])==4)
check('no sit/teleport API claim in runtime','WA.player.teleport' not in (R/'runtime/moonlit.js').read_text() and '.sit(' not in (R/'runtime/moonlit.js').read_text())
(R/'tests/structure-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2));print(len(checks),'structure checks passed')
