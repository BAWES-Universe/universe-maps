from pathlib import Path
import json,math
import numpy as np
r=Path(__file__).resolve().parents[1];p=r/'celestial-transit-garden';j=json.loads((p/'source/layout.json').read_text());g=np.array(j['grid']);repair=json.loads((r/'source/scenery-collision-repair.json').read_text());rows=[]
fixtures=[{'name':x['name'],'box':x['solidXYXY']} for x in j['protectedFixtures']]+repair['portalPlinthFootprints']
fixtures += [{'name':'west-exterior-lamp-and-railing-ground-group','box':[256,384,432,1152]},{'name':'east-exterior-lamp-and-railing-ground-group','box':[1616,384,1792,1152]},{'name':'northwest-exterior-lamp-and-terrace-base-group','box':[640,256,800,384]},{'name':'northeast-exterior-lamp-and-terrace-base-group','box':[1248,256,1408,384]},{'name':'south-arrival-lamp-and-outer-edge-bases','box':[768,1280,1280,1440]}]
for f in fixtures:
 x,y,x2,y2=f['box'];cells=g[y//32:math.ceil(y2/32),x//32:math.ceil(x2/32)];rows.append(dict(**f,allGroundCellsBlocked=bool(cells.all()),coveredNativeCells=int(cells.size)))
routes=json.loads((p/'validation/native-routes.json').read_text())['rows'];wam=json.loads((p/'map32/celestial-transit-garden.wam').read_text());areaChecks=[]
for area in j['areas']:
 w=next(a for a in wam['areas'] if a['id']==area['id']);legs=[x for x in routes if x['id']=='spawn-to-'+area['id']];ends=[]
 for leg in legs:
  x,y=leg['final'];inside=area['x']<=x<area['x']+area['width'] and area['y']<=y<area['y']+area['height'];wi=w['x']<=x<w['x']+w['width'] and w['y']<=y<w['y']+w['height'];ends.append({'input':leg['input'],'actualNativeFinal':[x,y],'insideAuthoredArea':inside,'insideWAMArea':wi,'nativePass':leg['pass']})
 areaChecks.append({'id':area['id'],'arrivals':ends,'allPass':len(ends)>=2 and {a['input'] for a in ends}=={'desktop','touch'} and all(a['insideAuthoredArea'] and a['insideWAMArea'] and a['nativePass'] for a in ends)})
out={'scope':'Whole physical foot/base boxes for all five portal structures and their nearby planter/pedestal groups, plus inaccessible exterior lamp/rail ground groups. Ground boxes deliberately exclude upper caps/flames and the documented conifer projection exception. Ponds/raised garden silhouettes are separately covered by exact-collision-delta and original visual regressions.','fixtureGroups':rows,'portalTriggerAreaAccess':areaChecks,'allPass':all(x['allGroundCellsBlocked'] for x in rows) and all(x['allPass'] for x in areaChecks)};(p/'validation/full-portal-fixture-audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));assert out['allPass']
