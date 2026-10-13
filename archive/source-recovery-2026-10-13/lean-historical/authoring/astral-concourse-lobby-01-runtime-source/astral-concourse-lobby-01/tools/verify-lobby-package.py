from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];M=R/'map32';m=json.loads((M/'astral-concourse-lobby.tmj').read_text());w=json.loads((M/'astral-concourse-lobby.wam').read_text());h=json.loads((R/'source/collision-grid.json').read_text())
checks=[]
def check(n,ok):checks.append({'check':n,'pass':bool(ok)})
check('finite orthogonal native32',not m['infinite']and m['orientation']=='orthogonal'and m['tilewidth']==m['tileheight']==32 and(m['width'],m['height'])==(36,28))
check('local WAM target resolves',w['mapUrl']=='./astral-concourse-lobby.tmj'and(M/w['mapUrl']).is_file())
check('native actor boundary layer',sum(l['name']=='floorLayer'for l in m['layers'])==1)
check('real below and above art',any(l['name']=='lobby-base'and any(l.get('data',[]))for l in m['layers'])and any(l['name']=='lobby-above'and any(l.get('data',[]))for l in m['layers']))
for ts in m['tilesets']:
 p=M/ts['image'];check('local texture '+ts['name'],p.is_file()and '://'not in ts['image']and '..'not in Path(ts['image']).parts)
 if p.is_file():check('texture size '+ts['name'],Image.open(p).size==(ts['imagewidth'],ts['imageheight']))
properties=[]
def walk(v):
 if isinstance(v,dict):
  if 'properties'in v:properties.extend(v['properties'])
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(m);walk(w)
forbidden={'exitUrl','exitSceneUrl','openTab','openWebsite','openWebsiteUrl','playAudio','jitsiRoom','script','speakerMegaphone','listenerMegaphone'}
check('no configured exits embeds ambient audio or scripts',not any(p.get('name',p.get('type'))in forbidden or p.get('type')in forbidden for p in properties))
urls=[p.get('value')for p in properties if isinstance(p.get('value'),str)and('://'in p['value']or p['value'].startswith('/@/'))]
check('no guessed http or room URLs',not urls)
flat=[c for row in h['grid']for c in row];collision=next(l for l in m['layers']if l['name']=='collision-permanent')
check('compiled collision agrees with source geometry',[bool(v)for v in collision['data']]==[bool(v)for v in flat])
for name,x,y in [('Flagship',576,272),('Forum',240,432),('Arena',912,432)]:check(name+' approach is walkable',h['grid'][y//32][x//32]==0)
for name,x,y in [('Flagship',576,208),('Forum',128,432),('Arena',1024,432)]:check(name+' portal body remains blocked',h['grid'][y//32][x//32]==1)
check('physical unavailable plaques authored',all(s in (R/'source/lobby-runtime-art.svg').read_text()for s in ['UNAVAILABLE','LINK PENDING']))
for name in ['geometry.json','native-routes.json','schema-silence.json']:
 p=R/'validation'/name;report=json.loads(p.read_text())if p.exists()else {};check('validation '+name,p.exists()and report.get('allPass',report.get('allPassed'))is True)
result={'allPass':all(c['pass']for c in checks),'checks':checks,'scope':'Local package, compiled/source geometry, exact local assets and absent/unavailable portal target audit. No room installation, live playthrough or external publication.'}
(R/'validation/package-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['allPass']
