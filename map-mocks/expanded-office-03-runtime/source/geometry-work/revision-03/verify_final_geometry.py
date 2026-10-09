#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from itertools import combinations
import jsonschema
ROOT=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
g=load(ROOT/'source-coordinate-geometry.json');src=load(ROOT/'collision-grid-source.json');full=load(ROOT/'collision-grid.json')
checks=[]
def check(name,passed,detail=None):checks.append(dict(name=name,passed=bool(passed),detail=detail))
def contains(a,b):return a['x']<=b['x'] and a['y']<=b['y'] and b['x']+b['width']<=a['x']+a['width'] and b['y']+b['height']<=a['y']+a['height']
def overlap(a,b):return a['x']<b['x']+b['width'] and b['x']<a['x']+a['width'] and a['y']<b['y']+b['height'] and b['y']<a['y']+a['height']
for n,h in load(ROOT.parent/'revision-02/frozen-baseline-sha256.json').items():check(f'frozen baseline unchanged: {n}',hashlib.sha256((ROOT.parent/n).read_bytes()).hexdigest()==h)
check('revision02 geometry unchanged',hashlib.sha256(Path(g['baselineProvenance']['revision02Geometry']).read_bytes()).hexdigest()==g['baselineProvenance']['sha256'])
check('source/full grid cell and dimensions',src['tileSize']==full['tileSize']==16 and [src['width'],src['height']]==[152,84] and [full['width'],full['height']]==[156,88])
S=set(src['blockedIndices']);F=set(full['blockedIndices'])
check('full-canvas interior exactly equals source translated32px',all(((y*152+x) in S)==(((y+2)*156+x+2) in F) for y in range(84) for x in range(152)))
check('full-canvas outer margin blocked',all(y*156+x in F for y in range(88) for x in range(156) if x<2 or x>=154 or y<2 or y>=86))
check('all colliders conservatively represented in source16px cells',all(y*152+x in S for r in g['allCollisionRectangles'] for y in range(r['y']//16,(r['y']+r['height']+15)//16) for x in range(r['x']//16,(r['x']+r['width']+15)//16)))
check('narrow sofa arms retain source12px geometry',sum(r['kind']=='sofa-floor' and r['width']==12 for r in g['furnitureCollisionRectangles'])==8)
check('north-sofa rear floor begins local48, not visual33',any(r['id']=='foyer-north-facing-sofa-part-0' and r['y']==1264 and r['height']==32 for r in g['furnitureCollisionRectangles']))
check('all28 team seats preserved',len(g['stations'])==28 and len(g['workbenches'])==7)
pods={p['id']:p for p in g['pods']};claims={p['id']:p for p in g['claimPlots']}
for b in g['workbenches']:
 p=pods[b['podId']]
 check(f'{b["id"]}: authorized exact32px east move',b['table']==dict(x=p['x']+144,y=p['y']+144,width=128,height=96))
 check(f'{b["id"]}: fixed unowned nonentity',b['ownerId'] is None and b['movableWamEntity'] is False)
for s in g['stations']:
 p=claims[s['claimPlotId']]
 check(f'{s["id"]}: body and full chair canvas in own plot',contains(p,s['seat']['bodyBounds']) and contains(p,s['chairAssetCanvas']))
 check(f'{s["id"]}: plot inside original bay',contains(pods[s['podId']],p))
 check(f'{s["id"]}: exact approach and contact sequence populated',bool(s.get('approach')) and bool(s.get('contactApproach')))
check('claim plots nonoverlapping',all(not overlap(a,b) for a,b in combinations(claims.values(),2)))
for door in g['doorOpenings']:check(f'{door["id"]}: actual opening clear',not any(overlap(door,r) for r in g['allCollisionRectangles']))
for goal in g['goals']:check(f'{goal["id"]}: source body clear',not any(overlap(goal['bodyBounds'],r) for r in g['allCollisionRectangles']))
wam=load(ROOT/'personal-areas.offline-draft.wam')
check('offline WAM uses full-canvas translated areas',all(a['x']==claims[a['id']]['x']+32 and a['y']==claims[a['id']]['y']+32 for a in wam['areas']))
check('offline WAM no owners or bench entities',wam['entities']=={} and all(a['properties'][0]['ownerId'] is None for a in wam['areas']))
try:
 jsonschema.validate(wam,load(Path('../universe-audio-fix/docs/schema/2.0.0/wam.json')));check('offline WAM valid2.0.0 schema',True)
except Exception as e:check('offline WAM valid2.0.0 schema',False,str(e))
routes=load(ROOT/'route-validation.json')
check('all122 route pairs and62 source anchors pass',routes['status']=='passed' and routes['routeCount']==122 and routes['directionalTestCount']==244 and routes['endpointCount']==62)
check('all45 exact contact checks pass',routes['contactTestCount']==45 and all(t['sourceApproachPassed'] and t['onePixelTowardTableBlocked'] for t in routes['contactChecks']))
failed=[c for c in checks if not c['passed']]
report=dict(status='failed' if failed else 'passed',testCount=len(checks),failedCount=len(failed),checks=checks,
            colliderCount=len(g['allCollisionRectangles']),sourceBlockedCellCount=len(S),fullCanvasBlockedCellCount=len(F),
            sourceToGridPolicy='All physical source rectangles covered conservatively by16px cells; all54 occupancy anchors and244 routes pass with that exact coverage.',
            visualAudit='See assembled-head-clearance.json. It is separate from this physical freeze.')
(ROOT/'geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],testCount=len(checks),failures=failed),indent=2))
raise SystemExit(bool(failed))
