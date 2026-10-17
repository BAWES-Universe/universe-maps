from pathlib import Path
import json,collections
r=Path(__file__).resolve().parents[2];m=json.loads((r/'campus.tmj').read_text());l=json.loads((r/'source/layout.json').read_text());w=m['width'];h=m['height'];d=next(a['data'] for a in m['layers'] if a['name']=='persistent-collision');start=tuple(v//16 for v in l['spawn']);seen={start};q=collections.deque([start])
while q:
 x,y=q.popleft()
 for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=a<w and 0<=b<h and not d[b*w+a] and (a,b) not in seen:seen.add((a,b));q.append((a,b))
checks={'dimensions':[w*16,h*16],'connectedWalkableCells':len(seen),'totalWalkableCells':d.count(0),'waypoints':{n:tuple(v//16 for v in p) in seen for n,p in l['waypoints'].items()},'reachableSeats':sum((s['x']//16,s['y']//16) in seen for s in l['seats']),'totalSeats':len(l['seats']),'missingAssets':[t['image'] for t in m['tilesets'] if not (r/t['image']).exists()]}
checks['allLayersNativeDimensions']=all(a.get('type')!='tilelayer' or len(a['data'])==w*h for a in m['layers'])
checks['walkableBoundsPixels']=[min(x for x,y in seen)*16,min(y for x,y in seen)*16,(max(x for x,y in seen)+1)*16,(max(y for x,y in seen)+1)*16]
(r/'review/geometry.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2));assert len(seen)==d.count(0) and all(checks['waypoints'].values()) and checks['reachableSeats']==checks['totalSeats'] and not checks['missingAssets'] and checks['allLayersNativeDimensions']
