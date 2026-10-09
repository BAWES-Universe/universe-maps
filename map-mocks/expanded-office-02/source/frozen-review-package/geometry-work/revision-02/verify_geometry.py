#!/usr/bin/env python3
"""Exact revision-02 checks, including immutable baseline and fixed-bench semantics."""
import hashlib
import json
from itertools import combinations
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
load = lambda p: json.loads(p.read_text())
g = load(ROOT/'source-coordinate-geometry.json')
base = load(BASE/'source-coordinate-geometry.json')
wam = load(ROOT/'personal-areas.offline-draft.wam')
checks=[]
def check(name, condition, detail=None):
    checks.append(dict(name=name,passed=bool(condition),detail=detail))
def overlaps(a,b):
    return a['x']<b['x']+b['width'] and b['x']<a['x']+a['width'] and a['y']<b['y']+b['height'] and b['y']<a['y']+a['height']
def contains(a,b):
    return a['x']<=b['x'] and a['y']<=b['y'] and b['x']+b['width']<=a['x']+a['width'] and b['y']+b['height']<=a['y']+a['height']
def no_overlaps(name,items):
    issues=[[a['id'],b['id']] for a,b in combinations(items,2) if overlaps(a,b)]
    check(name,not issues,issues)
frozen=load(ROOT/'frozen-baseline-sha256.json')
for name,digest in frozen.items():
    check(f'frozen baseline unchanged: {name}',hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest)
for key in ['pods','protectedSpines','permanentWalls','lowDividers','doorOpenings','rooms','reservations','namedAreas']:
    check(f'baseline {key} unchanged',g[key]==base[key])
check('world dimensions unchanged',g['coordinateSystem']['mapEnvelope']==base['coordinateSystem']['mapEnvelope'])
check('native32px avatar unchanged',g['coordinateSystem']['avatarFrame']==base['coordinateSystem']['avatarFrame'] and g['coordinateSystem']['avatarBody']==base['coordinateSystem']['avatarBody'] and g['coordinateSystem']['avatarScale']==1)
check('actual TMJ collision packaging specified16px',g['packaging']['tmjTileWidth']==16 and g['packaging']['tmjTileHeight']==16 and g['packaging']['widthTiles']*16==2432 and g['packaging']['heightTiles']*16==1344)
check('seven shared fixed workbenches',len(g['workbenches'])==7)
check('28 provisional seats and compact claims',len(g['stations'])==len(g['claimPlots'])==28)
check('growth bay remains empty',all(s['podId']!='studenthub-pod-growth' for s in g['stations']))
check('receiver cabinet masks explicitly pending',g['pendingObstacleMasks']['authoritativeCollisionRectangles'] is None)
pods={p['id']:p for p in g['pods']}
plots={p['id']:p for p in g['claimPlots']}
benches={b['id']:b for b in g['workbenches']}
collisions=g['permanentWalls']+g['lowDividers']+g['furnitureCollisionRectangles']
no_overlaps('all claim rectangles nonoverlapping, touching edges allowed',list(plots.values()))
no_overlaps('furniture and permanent collision rectangles nonoverlapping',collisions)
check('all collisions exactly fit16px TMJ cells',all(all(r[k]%16==0 for k in ['x','y','width','height']) for r in collisions))
check('furniture collision list contains only seven shared tables',len(g['furnitureCollisionRectangles'])==7 and all(r['width']==128 and r['height']==96 for r in g['furnitureCollisionRectangles']))
for b in benches.values():
    pod=pods[b['podId']]
    table=b['table']
    check(f'{b["id"]}: exact pod offset',table==dict(x=pod['x']+112,y=pod['y']+144,width=128,height=96))
    check(f'{b["id"]}: full composite canvas fits bay',contains(pod,b['compositeAssetCanvas']))
    check(f'{b["id"]}: fixed shared unowned fixture',b['ownerId'] is None and not b['movableWamEntity'] and not b['wholeTableClaim'])
    own=[p for p in plots.values() if p['workbenchId']==b['id']]
    check(f'{b["id"]}: four separated claim quadrants',len(own)==4 and all(p['width']==64 and p['height']==112 for p in own))
    check(f'{b["id"]}: no claim owns entire shared table',not any(contains(p,table) for p in own))
for s in g['stations']:
    sid=s['id']; p=plots[s['claimPlotId']]; b=benches[s['sharedWorkbenchId']]; table=b['table']
    check(f'{sid}: plot in own pod',contains(pods[s['podId']],p))
    check(f'{sid}: seat body in own plot',contains(p,s['seat']['bodyBounds']))
    check(f'{sid}: full chair canvas in own plot',contains(p,s['chairAssetCanvas']))
    check(f'{sid}: body clear of physical geometry',not any(overlaps(s['seat']['bodyBounds'],r) for r in collisions))
    check(f'{sid}: claim clear of existing walls/dividers',not any(overlaps(p,r) for r in g['permanentWalls']+g['lowDividers']))
    expected_y=table['y']-16 if s['seat']['facing']=='south' else table['y']+96
    check(f'{sid}: exact table-edge body contact',s['seat']['y']==expected_y)
    check(f'{sid}: unassigned and unscaled',s['ownerId'] is None and s['headcountEvidence'] is None and s['assetScale']==1 and s['seat']['spriteBounds']['width']==32)
for spine in g['protectedSpines']:
    check(f'{spine["id"]}: fully clear',not any(overlaps(spine,r) for r in collisions+g['claimPlots']+g['reservations']))
for opening in g['doorOpenings']:
    check(f'{opening["id"]}: actual collision opening',not any(overlaps(opening,r) for r in collisions))
ids=[a['id'] for a in wam['areas']]+[a['properties'][0]['id'] for a in wam['areas']]
check('WAM area/property IDs unique',len(ids)==len(set(ids)))
check('WAM has no editable bench entities',wam['entities']=={} and wam['entityCollections']==[])
check('all WAM claim properties draft unassigned',all(len(a['properties'])==1 and a['properties'][0]['type']=='personalAreaPropertyData' and a['properties'][0]['accessClaimMode']=='dynamic' and a['properties'][0]['allowedTags']==[] and a['properties'][0]['ownerId'] is None for a in wam['areas']))
check('WAM areas match exact proposed64×112 plots',all(all(a[k]==plots[a['id']][k] for k in ['x','y','width','height','name']) for a in wam['areas']))
try:
    jsonschema.validate(wam,load(Path('../universe-audio-fix/docs/schema/2.0.0/wam.json')))
    check('offline WAM passes source2.0.0 schema',True)
except jsonschema.ValidationError as e:
    check('offline WAM passes source2.0.0 schema',False,e.message)
failed=[c for c in checks if not c['passed']]
report=dict(status='failed' if failed else 'passed',testCount=len(checks),failedCount=len(failed),checks=checks,
            scope='Workbench-only source geometry; revised painted receiver/cabinet collision masks are excluded until integration.',
            limitations=g['limitations'])
(ROOT/'geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],tests=len(checks),failures=failed),indent=2))
raise SystemExit(bool(failed))
