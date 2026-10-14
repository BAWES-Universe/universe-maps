from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/design.json').read_text());L=json.loads((R/'source/layout.json').read_text());G=L['collision'];rows=[]
def body(x,y):
 return all(0<=yy<len(G) and 0<=xx<len(G[0])and G[yy][xx]==0 for yy in range(math.floor(y/32),math.floor((y+16-1e-8)/32)+1)for xx in range(math.floor((x-8)/32),math.floor((x+8-1e-8)/32)+1))
for p in D['visiblePaths']:
 points=p['origins'];bad=[];n=0
 for a,b in zip(points,points[1:]):
  steps=max(1,math.ceil(math.dist(a,b)/.5))
  for k in range(steps+1):
   x=a[0]+(b[0]-a[0])*k/steps;y=a[1]+(b[1]-a[1])*k/steps;n+=1
   if not body(x,y):bad.append([x,y])
 rows.append(dict(name=p['name'],samples=n,**{'pass':not bad},firstFailure=bad[:1]))
for p in D['fixtureNegatives']:assert G[p['point'][1]//32][p['point'][0]//32],p
out=dict(scope='Author explicitly inventoried full visible floor and width lines, sampled with full native16x16 body at<=0.5px; native routing tested separately. No independent visual/live acceptance.',**{'pass':all(x['pass']for x in rows)},paths=rows,negativeCount=len(D['fixtureNegatives']));(R/'validation/full-floor.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['pass']
