from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,sys,hashlib
R=Path(__file__).resolve().parents[1];slug=sys.argv[1];P=R/slug;lay=json.load(open(P/'source/layout.json'));g=np.array(lay['grid']);q=np.array(lay['quiet']);m=json.load(open(P/'map32'/(slug+'.tmj')));wam=json.load(open(P/'map32'/(slug+'.wam')))
def clear(x,y):
 if not(8<=x<=m['width']*32-8 and 0<=y<=m['height']*32-16):return False
 return all(g[yy,xx]==0 for yy in range(y//32,(y+15)//32+1) for xx in range((x-8)//32,(x+7)//32+1))
tiled=next(a for l in m['layers'] if l['type']=='objectgroup' for a in l['objects'] if a['name']=='start');wa=next(a for a in wam['areas'] if any(p['type']=='start' and p.get('isDefault') for p in a['properties']))
domains=[]
for name,a,margin in [('Tiled start',tiled,16),('WAM default',wa,0),('WAM named conservative reverse-range superset',wa,16)]:
 xs=sorted([a['x']+margin,a['x']+a['width']-margin]);ys=sorted([a['y']+margin,a['y']+a['height']-margin]);positions=[(x,y) for x in range(xs[0],xs[1]+1) for y in range(ys[0],ys[1]+1)];bad=[(x,y) for x,y in positions if not clear(x,y) or not q[y//32,x//32]];domains.append(dict(name=name,margin=margin,xRange=xs,yRange=ys,conservativeIntegerPositions=len(positions),unsafeOrAudible=bad,allPass=not bad))
assert all(d['allPass'] for d in domains)
report=dict(scope='Source-derived exhaustive conservative integer spawn-domain test. Tiled/named-area start uses margin16; default WAM start uses margin0. Reversed named-WAM bounds are tested as the inclusive min/max superset. Full native StartPositionCalculator and MathUtils are bundled.',domains=domains,allPass=True)
(P/'validation/spawn-domains.json').write_text(json.dumps(report,indent=2)+'\n')
# Cover every floor boundary tile at four admitted native body positions. These are visual audit evidence,
# not a claim that an algorithm can identify the depicted objects from their colors.
pts=[]
for y in range(g.shape[0]):
 for x in range(g.shape[1]):
  if g[y,x] or not any(not(0<=xx<g.shape[1] and 0<=yy<g.shape[0]) or g[yy,xx] for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):continue
  for dx,dy in [(8,0),(24,0),(8,16),(24,16)]:
   px,py=x*32+dx,y*32+dy
   if clear(px,py):pts.append(dict(tile=[x,y],x=px,y=py,offset=[dx,dy]))
base=Image.open(P/'review/empty-native.png').convert('RGBA');repo=Path(__import__('os').environ.get('WOKA_REPO','/workspace/shared/native32-replan-baseline')); sheets=sorted((repo/'play/public/resources/characters/pipoya').glob('Female 0[134]-1.png')); sprites=[Image.open(f).convert('RGBA').crop((32,0,64,32)) for f in sheets]
for phase in range(4):
 out=base.copy()
 for i,p in enumerate(pts):
  if i%4==phase:out.alpha_composite(sprites[i%len(sprites)],(p['x']-16,p['y']-16))
 out.save(P/'review'/f'boundary-sweep-{phase}-native.png')
(P/'validation/boundary-sweep.json').write_text(json.dumps(dict(scope='Every boundary tile, four body-admissible edge offsets; inspect the native evidence images against actual scenery. Mathematical clearance alone does not certify visual floor alignment.',points=pts,pointCount=len(pts),protectedFixtures=lay.get('protectedFixtures',[])),indent=2)+'\n')
print(slug,'spawn domains pass;',len(pts),'boundary probe placements')
