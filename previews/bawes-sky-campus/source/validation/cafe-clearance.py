"""Check a continuous 96px swept square through the cafe's main turn."""
from pathlib import Path
import json,collections
r=Path(__file__).resolve().parents[2];m=json.loads((r/'campus.tmj').read_text());w=m['width'];d=next(l['data'] for l in m['layers'] if l['name']=='persistent-collision')
safe={(x,y) for y in range(265,280) for x in range(150,196) if all(not d[b*w+a] for a in range(x-3,x+3) for b in range(y-3,y+3))}
start=(178,270);target=(160,272);seen={start};q=collections.deque([start])
while q:
 x,y=q.popleft()
 for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if p in safe and p not in seen:seen.add(p);q.append(p)
checks={'sweptSquarePixels':96,'start':[2848,4320],'target':[2560,4352],'startClear':start in safe,'continuousRoute':target in seen,'pedestalFootBlocked':bool(d[(4432//16)*w+2680//16]),'behindLanternHeadWalkable':not d[(4384//16)*w+2680//16]}
(r/'review/cafe-clearance.json').write_text(json.dumps(checks,indent=2)+'\n');print(checks);assert all(checks[k] for k in ['startClear','continuousRoute','pedestalFootBlocked','behindLanternHeadWalkable'])
