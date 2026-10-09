#!/usr/bin/env python3
"""Explicit left/right entrances into each facing-sofa seat, others occupied."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
g=json.loads((ROOT/'source-coordinate-geometry.json').read_text());grid=json.loads((ROOT/'collision-grid-source.json').read_text())
blocked=set(grid['blockedIndices']);width=grid['width']
def overlap(a,b):return a['x']<b['x']+b['width'] and b['x']<a['x']+a['width'] and a['y']<b['y']+b['height'] and b['y']<a['y']+a['height']
def body(p):return dict(x=p[0]-8,y=p[1],width=16,height=16)
routes=[];checks=[]
for t in g['goals']:
 if not t['id'].startswith('foyer-') or t['kind']!='lounge-seat':continue
 for side,x_entry,x_lane in [('west',288,344),('east',480,424)]:
  if t['facing']=='south':points=[[x_entry,1184],[t['x'],1184],[t['x'],t['y']]]
  else:points=[[x_entry,1184],[x_lane,1184],[x_lane,1232],[t['x'],1232],[t['x'],t['y']]]
  rid=f'{side}-approach-to-{t["id"]}'
  routes.append(dict(id=rid,targetId=t['id'],points=[dict(x=p[0],y=p[1]) for p in points],alsoTestReverse=True))
  obstacles=g['allCollisionRectangles']+[dict(a['bodyBounds'],id=a['id']) for a in g['goals'] if a['kind']!='checkpoint' and a['id']!=t['id']]
  for reverse in [False,True]:
   pts=list(reversed(points)) if reverse else points;issues=[];sample_count=0
   for a,b in zip(pts,pts[1:]):
    assert a[0]==b[0] or a[1]==b[1]
    n=max(abs(a[0]-b[0]),abs(a[1]-b[1]))
    for i in range(n+1):
     p=[a[k]+(b[k]-a[k])*i/max(1,n) for k in range(2)];r=body(p);sample_count+=1
     source=[o['id'] for o in obstacles if overlap(r,o)]
     cells=[(int(y)*width+int(x)) for y in range(int(r['y']//16),int((r['y']+16-0.001)//16)+1) for x in range(int(r['x']//16),int((r['x']+16-0.001)//16)+1)]
     if source or any(c in blocked for c in cells):issues.append(dict(point=p,source=source,gridBlocked=any(c in blocked for c in cells)))
   checks.append(dict(id=rid+('-reverse' if reverse else ''),passed=not issues,sampledPositions=sample_count,issues=issues[:3]))
report=dict(status='passed' if all(t['passed'] for t in checks) else 'failed',coordinateSpace='source office pixels',renderTranslation=dict(x=32,y=32),routeCount=len(routes),directionalTests=len(checks),
            note='North-facing seats use the genuine16px grid-safe slot between the table and rounded sofa arm, then the row y1232. Actual back-floor starts1264. No art moved.',routes=routes,checks=checks)
(ROOT/'foyer-seat-access-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],routes=len(routes),directionalTests=len(checks),failures=[t for t in checks if not t['passed']]),indent=2))
raise SystemExit(report['status']!='passed')
