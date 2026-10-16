import json,collections
from pathlib import Path
D=Path('/workspace/coastal-pavilion');m=json.loads((D/'azure.tmj').read_text());g=json.loads((D/'geometry.json').read_text());blocked=g['blocked'];C=m['width'];R=m['height'];free={i for i,b in enumerate(blocked) if not b};seen={next(iter(free))};q=list(seen)
for i in q:
 x,y=i%C,i//C
 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  j=yy*C+xx
  if 0<=xx<C and 0<=yy<R and j in free and j not in seen:seen.add(j);q.append(j)
assert seen==free
# Every free tile must be represented by both row and column maximal continuous runs.
runs=[]
for axis in ['horizontal','vertical']:
 for k in range(R if axis=='horizontal' else C):
  start=None
  for t in range((C if axis=='horizontal' else R)+1):
   x,y=(t,k) if axis=='horizontal' else (k,t)
   yes=x<C and y<R and y*C+x in free
   if yes and start is None:start=t
   if not yes and start is not None:
    runs.append(dict(axis=axis,fixed=k,first=start,last=t-1,length=t-start));start=None
covered={a:set() for a in ['horizontal','vertical']}
for r in runs:
 for t in range(r['first'],r['last']+1):
  x,y=(t,r['fixed']) if r['axis']=='horizontal' else (r['fixed'],t);covered[r['axis']].add(y*C+x)
assert all(s==free for s in covered.values())
record={'walkableTiles':len(free),'connectedWalkableTiles':len(seen),'allFreeTilesCoveredByHorizontalAndVerticalRuns':True,'maximalRuns':runs,'note':'Static coverage is not gameplay acceptance. Actual browser traversal of every exposed corridor still required.'}
Path('/workspace/coastal-runtime/geometry-audit.json').write_text(json.dumps(record,indent=2)+'\n')
print(len(free),'connected tiles;',len(runs),'maximal row/column runs')
# Both tile-center and tile-edge route audit figure with original art linked separately.
