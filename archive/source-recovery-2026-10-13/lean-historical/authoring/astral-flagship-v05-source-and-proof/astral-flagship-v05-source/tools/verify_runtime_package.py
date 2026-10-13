"""Offline package checks. Explicit exceptions remain enabled under Python -O."""
from pathlib import Path
from PIL import Image
import json, hashlib
import numpy as np

R=Path(__file__).resolve().parents[1]
M=R/'map32'
checks=[]
def check(name,value):
    checks.append({'name':name,'pass':bool(value)})
    if not value: raise RuntimeError(name)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
m=load(M/'grand-auditorium.tmj'); w=load(M/'grand-auditorium.wam')
check('native orthogonal32 map',m['tilewidth']==m['tileheight']==32 and m['orientation']=='orthogonal' and (m['width'],m['height'])==(80,60))
check('no script or focus or layer transition map properties',not any(p['name'] in ['script','focusable','zoomMargin','exitSceneUrl','exitUrl'] for p in m.get('properties',[])))
check('no toggle groups',not any(l['type']=='group' for l in m['layers']))
check('relative companion TMJ resolves',w['mapUrl']=='./grand-auditorium.tmj')
refs={'grand-auditorium.tmj','grand-auditorium.wam'}
for ts in m['tilesets']:
    name=ts['image']; p=M/name
    check('local image '+name, '/' not in name and p.is_file())
    refs.add(name)
    im=Image.open(p)
    check('atlas dimensions '+name,im.size==(ts['imagewidth'],ts['imageheight']))
check('exact nine-file runtime closure',len(refs)==9 and {p.name for p in M.iterdir() if p.is_file()}==refs)
check('review avatar absent from runtime',not any('greg' in n.lower() for n in refs))
grid=load(R/'source/collision-grid.json'); quiet=load(R/'source/quiet-grid.json'); old=load(R/'source/v04-collision-grid.json')
g=np.array(grid['grid']); og=np.array(old['grid']); q=np.array(quiet['grid'])
adjust=load(R/'source/garden-layout.json').get('runtimeRouteAdjustments',{})
closed={(int(x),int(y)) for y,x in np.argwhere((og==0)&(g!=0))}
check('only declared visible low wings close prior floor',closed=={tuple(v) for v in adjust.get('closedCells',[])})
check('quiet geometry preserved',quiet==load(R/'source/v04-quiet-grid.json') and int(q.sum())==333)
check('210 seat records preserved',load(R/'source/seats.json')==load(R/'source/v04-seats.json') and len(load(R/'source/seats.json'))==210)
check('24 original social anchors preserved',grid['socialAnchors'][:24]==old['socialAnchors'])
check('four outdoor casual anchors added',len(grid['socialAnchors'])==28 and all(x['id'].startswith('garden-pair-') for x in grid['socialAnchors'][24:]))
oldw=load(R/'source/v04-area-template.wam')
normalized=json.loads(json.dumps(w).replace('astral-flagship-v05','astral-flagship-v04').replace('Flagship v05','Flagship v04'))
check('all existing communication geometry preserved',normalized==oldw)
for name,source in [('hall-base','runtime-base.png'),('hall-above','runtime-above.png')]:
    l=next(l for l in m['layers'] if l['name']==name)
    result=Image.new('RGBA',(2560,1920))
    atlases=[(t,Image.open(M/t['image']).convert('RGBA')) for t in m['tilesets']]
    for i,gid in enumerate(l['data']):
        if not gid:continue
        t,im=next((t,im) for t,im in reversed(atlases) if t['firstgid']<=gid)
        tile=gid-t['firstgid']; x=(tile%t['columns'])*32; y=(tile//t['columns'])*32
        result.paste(im.crop((x,y,x+32,y+32)),((i%80)*32,(i//80)*32))
    original=np.array(Image.open(R/'assets'/source).convert('RGBA')); original[original[:,:,3]==0]=0
    check('visible RGBA atlas roundtrip '+name,np.array_equal(np.array(result),original))
collision=next(l for l in m['layers'] if l['name']=='collision-permanent')
check('permanent collision visible and untoggled',collision['visible'] is True and collision['opacity']==0)
check('collision tile geometry exact',np.array_equal(np.array(collision['data']).reshape(60,80)>0,g>0))
silent=next(l for l in m['layers'] if l['name']=='quiet-arrival-and-main-circulation')
check('sole TMJ silence exact',silent['properties']==[{'name':'silent','type':'bool','value':True}] and np.array_equal(np.array(silent['data']).reshape(60,80)>0,q>0))
check('quiet marker completely transparent',Image.open(M/'quiet-marker.png').convert('RGBA').getchannel('A').getbbox() is None)
geometry=load(R/'validation/geometry.json')
check('exhaustive static geometry passes',geometry['allPass'])
files=[{'path':n,'bytes':(M/n).stat().st_size,'sha256':sha(M/n)} for n in sorted(refs)]
report={'status':'offline package checks only; not browser or live media acceptance','checks':checks,'allPass':all(c['pass'] for c in checks),'runtimeFiles':files,'runtimeBytes':sum(f['bytes'] for f in files)}
(R/'validation/package-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'allPass':report['allPass'],'checks':len(checks),'runtimeFiles':len(files),'runtimeBytes':report['runtimeBytes']},indent=2))
