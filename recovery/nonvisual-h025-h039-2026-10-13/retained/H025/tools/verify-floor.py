from pathlib import Path
import json,math,hashlib
r=Path(__file__).resolve().parents[1];l=json.load(open(r/'source/layout.json'));g=l['collision'];m=json.load(open(r/'map32/map.tmj'));assert [int(bool(v))for v in next(x for x in m['layers']if x['name']=='collision')['data']]==sum(g,[]);v=json.load(open(r/'source/visible-floor.json'));rows=[]
def safe(x,y):return all(0<=yy<len(g)and 0<=xx<len(g[0])and not g[yy][xx]for yy in range(math.floor(y/32),math.ceil((y+16)/32))for xx in range(math.floor((x-8)/32),math.ceil((x+8)/32)))
for room,q in v['rooms'].items():
 for path in q['visiblePaths']:
  bad=[];n=0
  for a,b in zip(path['origins'],path['origins'][1:]):
   steps=max(1,math.ceil(math.dist(a,b)/.5))
   for z in range(steps+1):
    p=[a[i]+(b[i]-a[i])*z/steps for i in range(2)];n+=1
    if not safe(*p)and len(bad)<10:bad.append(p)
  rows.append({'room':room,'name':path['name'],'samples':n,'pass':not bad,'firstBlocked':bad})
out={'scope':'Author manually selected H025 whole-scene visible-floor polylines against actual TMJ-derived collision. Fresh independent floor/art review remains required.','tmjSHA256':hashlib.sha256((r/'map32/map.tmj').read_bytes()).hexdigest(),'paths':rows,'allPass':all(a['pass']for a in rows)};(r/'validation/visible-floor-regression.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['allPass']
