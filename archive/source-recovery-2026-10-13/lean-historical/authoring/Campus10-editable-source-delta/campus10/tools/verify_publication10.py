"""Independent decoded-pixel/property equivalence of the lean hosted derivative."""
from pathlib import Path
from PIL import Image
from bisect import bisect_right
from urllib.parse import urljoin
import json,hashlib,copy
R=Path(__file__).resolve().parents[1];A=R/'map32';B=R/'publication/v10/map32'
OLD=Path('/workspace/shared/magical-campus-standard32-09/map32')
canonical='https://bawes-universe.github.io/universe-maps/butterfly-town/v10/map32/magical-campus.tmj'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(root):
 m=json.loads((root/'magical-campus.tmj').read_text());sets=[]
 for s in m['tilesets']:
  path=OLD/s['image'][len('../../v9/map32/'):] if s['image'].startswith('../../v9/map32/') else root/s['image']
  assert path.is_file();assert not s.get('tileoffset') and not s.get('properties')
  sets.append((s,Image.open(path).convert('RGBA'),{t['id']:t for t in s.get('tiles',[])}))
 sets.sort(key=lambda s:s[0]['firstgid']);return m,sets,[s[0]['firstgid']for s in sets]
a,aa,ai=load(A);b,bb,bi=load(B)
def entry(gid,sets,starts):
 assert gid<0x10000000,'Tiled transform flags must be preserved explicitly'
 ts,image,meta=sets[bisect_right(starts,gid)-1];local=gid-ts['firstgid'];assert 0<=local<ts['tilecount']
 tilemeta=meta.get(local,{});frames=tilemeta.get('animation',[{'tileid':local,'duration':0}]);out=[]
 for f in frames:
  idx=f['tileid'];x=idx%ts['columns']*32;y=idx//ts['columns']*32
  out.append((f['duration'],image.crop((x,y,x+32,y+32)).tobytes()))
 return out,{k:v for k,v in tilemeta.items()if k not in ['id','animation']}
cells=frames=0;cache=set()
for left,right in zip(a['layers'],b['layers']):
 assert left.keys()==right.keys()
 if left['type']!='tilelayer':
  q=copy.deepcopy(right)
  for o in q.get('objects',[]):
   for p in o.get('properties',[]):
    if p['name']=='playAudio':p['value']=p['value'].removeprefix('../../v9/map32/')
  assert left==q;continue
 assert {k:v for k,v in left.items()if k!='data'}=={k:v for k,v in right.items()if k!='data'}
 assert len(left['data'])==len(right['data'])
 for x,y in zip(left['data'],right['data']):
  assert bool(x)==bool(y)
  if not x:continue
  cells+=1
  if (x,y) in cache:continue
  old,oldmeta=entry(x,aa,ai);new,newmeta=entry(y,bb,bi)
  assert oldmeta==newmeta and old==new,(left['name'],x,y)
  cache.add((x,y));frames+=len(old)
assert {k:v for k,v in a.items()if k not in ['layers','tilesets']}=={k:v for k,v in b.items()if k not in ['layers','tilesets']}
refs=[s['image'] for s in b['tilesets']]+[p['value']for l in b['layers']for o in l.get('objects',[])for p in o.get('properties',[])if p['name']=='playAudio']
resolved=sorted({urljoin(canonical,p)for p in refs})
assert all(u.startswith('https://bawes-universe.github.io/universe-maps/butterfly-town/v')for u in resolved)
report={'pass':True,'testedStandaloneSHA256':sha(A/'magical-campus.tmj'),'publicationSHA256':sha(B/'magical-campus.tmj'),
 'cellsCompared':cells,'uniqueTilePairsDecoded':len(cache),'framesDecodedRGBACompared':frames,
 'allFrameDurationsAndRGBAIdentical':True,'tilePropertiesAndTransformFlagsPreserved':True,
 'collisionGridAndLayerSemanticsIdentical':True,'objectPropertiesIdenticalExceptEquivalentAudioURLs':True,
 'relativeURLsResolveFromActualHostedLocation':resolved,'browserOrHTTPAcceptance':False}
(R/'publication/v10/publication-equivalence-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
