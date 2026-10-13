from pathlib import Path
from PIL import Image
import numpy as np,json,math
R=Path(__file__).resolve().parents[1];O=R/'timber-mixed-six-mat-instructor-facing-r3';layout=json.loads((O/'source/layout.json').read_text());g=np.array(layout['collision']);proof=json.loads((O/'source/SOURCE-PRESERVATION.json').read_text());rows=[]
for m in proof['records']:
 for p in m['props']:
  x,y=p['destination'];b=p['sourceBox'];w=b[2]-b[0];h=b[3]-b[1];box=[math.floor(x*.5),math.floor(y*.5),math.ceil((x+w)*.5),math.ceil((y+h)*.5)]
  x0,y0,x1,y1=box;cells={(xx//32,yy//32) for yy in range(y0,y1) for xx in range(x0,x1)};bad=[list(c) for c in cells if not g[c[1],c[0]]];rows.append(dict(mat=m['id'],prop=p['kind'],nativeBounds=box,solidCells=[list(c) for c in sorted(cells)],unblockedCells=bad));assert not bad,(m,p,bad)
# Entire conservative projected bounding rectangles are blocked, including all
# pixels of the equipment, rear structural feet, and main entry posts.
solids={'rear rower':[67,94,164,127],'exercise bike':[651,75,704,132],'west weights':[38,146,100,229],'east weights':[664,146,716,229],'left rear pillar and pot':[302,66,335,111],'right rear pillar and pot':[437,66,466,111],'left entry pillar':[266,360,352,448],'right entry pillar':[416,360,494,448],'shifted west south-wall foliage base':[144,384,204,402],'shifted east south-wall foliage base':[558,384,624,402],'west bench and side table':[134,307,224,338],'east refreshment furniture':[558,304,666,339],'west lowered cap':[264,352,291,374],'east lowered cap':[474,352,502,374]}
solidrows=[]
for name,(x0,y0,x1,y1) in solids.items():
 cells={(xx//32,yy//32) for yy in range(y0,y1) for xx in range(x0,x1)};bad=[list(c) for c in cells if not g[c[1],c[0]]];solidrows.append(dict(name=name,bounds=[x0,y0,x1,y1],unblockedCells=bad))
assert not any(r['unblockedCells'] for r in solidrows), solidrows
# Whole projected bounding boxes are a deliberately conservative coverage gate.
wam=json.loads((O/'map32/map.wam').read_text());membership=[]
for a in layout['anchors']:
 if a['kind'] not in ['instructor','mat']:continue
 x,y=a['anchor'];hits=[]
 for z in wam['areas']:
  if z['x']<=x<=z['x']+z['width'] and z['y']<=y+16<=z['y']+z['height']:hits.extend(p['type'] for p in z['properties'])
 expected='speakerMegaphone' if a['kind']=='instructor' else 'listenerMegaphone';assert expected in hits,(a,hits);membership.append(dict(anchor=a['name'],expectedRole=expected,matches=hits))
out=dict(props=rows,allTwelvePropBoundingBoxesSolid=True,sourceSolidBoundingBoxes=solidrows,allFourteenSceneryBaseBoundingBoxesSolid=True,roleMembership=membership,allSevenRoleAnchorsMatch=True,scope='Prop projected bounding-box solidity and actual native companion area membership; boundary rectangle diagnostics are not a substitute for shape/visual review.')
(O/'SCENERY-CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print('All 12 props solid. All 7 instructor/mat role memberships match.');print('Boundary diagnostic overlaps:',[(r['name'],r['unblockedCells']) for r in solidrows if r['unblockedCells']])
