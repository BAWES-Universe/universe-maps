"""Bounded independent artifact/source integrity and fixed-mask validation."""
from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,argparse
ap=argparse.ArgumentParser();ap.add_argument('--map-dir',default='map16');args=ap.parse_args()
R=Path(__file__).resolve().parents[1];checks=[]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(name,passed,detail=None):checks.append({'name':name,'pass':bool(passed),'detail':detail})
m=read(R/args.map_dir/'magical-campus.tmj');g=read(R/args.map_dir/'collision-grid.json');manifest=read(R/args.map_dir/'compile-manifest.json');route=read(R/args.map_dir/'route-plan.json')
check('finite native 3200x3072 map',not m['infinite'] and m['width']*m['tilewidth']==3200 and m['height']*m['tileheight']==3072)
check('permanent native collision contract',m['tilewidth']==m['tileheight']==g['tileSize'])
valid=set()
for ts in m['tilesets']:
 p=R/args.map_dir/ts['image'];im=Image.open(p)
 check(ts['name']+' atlas dimensions',im.size==(ts['imagewidth'],ts['imageheight']))
 if args.map_dir=='map16':check(ts['name']+' bounded atlas',max(im.size)<=2048)
 valid.update(range(ts['firstgid'],ts['firstgid']+ts['tilecount']))
for l in m['layers']:
 if l['type']=='tilelayer':
  check(l['name']+' finite aligned layer',l['x']==l['y']==0 and l['width']==m['width'] and l['height']==m['height'] and len(l['data'])==m['width']*m['height'])
  check(l['name']+' valid tile IDs',all(v==0 or v in valid for v in l['data']))
collision=next(l for l in m['layers'] if l['name']=='collision-permanent');actual={i for i,v in enumerate(collision['data']) if v}
check('TMJ contains exact standalone physical grid',actual==set(g['blockedIndices']))
check('collision independent of foreground',collision['visible'] and collision['opacity']==0)
native_solid=np.zeros((g['height'],g['width']),np.uint8);native_solid.flat[g['blockedIndices']]=1
source8=read(R/'map/collision-grid.json');solid=np.zeros((384,400),np.uint8);solid.flat[source8['blockedIndices']]=1
if g['tileSize']==16:check('exact conservative16px coalescing',np.array_equal(native_solid,solid.reshape(192,2,200,2).max((1,3))))
og=read(R/'sources/office/collision-grid.json');source=np.zeros((og['height'],og['width']),np.uint8);source.flat[og['blockedIndices']]=1;promoted=source.repeat(2,0).repeat(2,1);integrated=solid[288//8:(288+1408)//8,480//8:(480+2496)//8];diff=integrated!=promoted;expected=np.zeros_like(promoted);expected[(1664-288)//8:(1696-288)//8,(1440-480)//8:(1568-480)//8]=1
expected[:,0:4]=1
check('only author-approved office padding changes',np.array_equal(diff,expected),{'changed8pxCells':int(diff.sum()),'expectedPaddingCells':int(expected.sum())})
garden=read(R/'sources/garden/collision-grid-8px.json');gg=np.array(garden['blocked']).reshape(128,128)
check('garden permanent grid copied unchanged',np.array_equal(solid[1920//8:(1920+1024)//8,2176//8:400],gg))
for x in manifest['sourceAudit']:check('copied source hash: '+x['copy'],sha(R/x['copy'])==x['sha256'])
portable={x['path']:x['sha256'] for x in read(R/'docs/portable-runtime-files.json')['files']}
for name in ['fork-primitives.js','phaser.js']:
 original=R.parent/'universe-expanded-office/runtime-work/vendor'/name;expected=sha(original) if original.exists() else portable['runtime/vendor/'+name];check('unchanged runtime '+name,sha(R/'runtime/vendor'/name)==expected)
original=R.parent/'universe-expanded-office/runtime-work/assets/greg.png';expected=sha(original) if original.exists() else portable['runtime/assets/greg.png'];check('unchanged native Greg sprite',sha(R/'runtime/assets/greg.png')==expected)
check('continuous offline route passes',route['status']=='pass',{'destinations':len(route['legs']),'samples':route['bodySweepSamples']})
check('every author destination connects',all(x['pass'] for x in route['allDestinationChecks']),len(route['allDestinationChecks']))
# Explicitly inspect all three animation frames of each authored facing.
fg=Image.open(R/'layers/campus-foreground.png').convert('RGBA');sheet=Image.open(R/'runtime/assets/greg.png').convert('RGBA');headchecks=[]
for z in route['allGoals']:
 if not z.get('facing'):continue
 row={'down':0,'left':1,'right':2,'up':3}[z['facing']];x,y=z['target'].values()
 for frame in range(3):
  spr=sheet.crop((frame*32,row*32,frame*32+32,row*32+32));a=np.asarray(spr)[:14,:,3]>32;b=np.asarray(fg.crop((x-16,y-16,x+16,y+16)))[:14,:,3]>32;n=int((a&b).sum());headchecks.append({'id':z['id'],'frame':row*3+frame,'foregroundHeadOverlapPixels':n,'pass':n==0})
check('fixed foreground clears all authored heads',all(x['pass'] for x in headchecks),len(headchecks))
(R/'docs/assembled-head-check.json').write_text(json.dumps({'scope':'Fixed structural foreground vs opaque top14px of unchanged Greg frames. Shade/glass excluded from solid-occluder test.','checks':headchecks,'pass':all(x['pass'] for x in headchecks)},indent=2))
result={'pass':all(x['pass'] for x in checks),'checks':checks,'scope':'Static source/artifact checks. Browser physics, native animation, live service behavior and design acceptance are separate.'};(R/f'docs/artifact-verification-{g["tileSize"]}px.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'pass':result['pass'],'checks':len(checks),'failures':[x for x in checks if not x['pass']]},indent=2))
