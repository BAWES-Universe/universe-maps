from pathlib import Path
import json
r=Path(__file__).resolve().parents[2];l=json.loads((r/'source/layout.json').read_text());m=json.loads((r/'campus.tmj').read_text());x,y,w,h=l['office'];rows=[]
for i,o in enumerate(l['objects']):
 if o['zone']!='office':continue
 a,b,c,d=o['x'],o['y'],o['width'],o['height'];clear=[a-x,b-y,x+w-a-c,y+h-b-d]
 assert min(clear)>=0,(i,o,clear)
 if o['kind']=='in-sofa':assert clear[3]>=64
 rows.append({'object':i,**o,'clearanceToBuildingPixels':dict(zip(['left','back','right','front'],clear))})
for layer in m['layers']:
 if layer['name'] not in ['office-floor','office-walls','office-furniture','office-chair-fronts','office-glazing','meeting-1-glass','meeting-2-glass']:continue
 for i,gid in enumerate(layer['data']):
  if gid:assert x<=i%m['width']*16<x+w and y<=i//m['width']*16<y+h,(layer['name'],i)
assert l['cutaway']==l['office']
assert not any(d['id']=='office-rear' for d in l['doors'])
report={'floor':l['office'],'exteriorCanvas':l['exterior'],'cutawayEqualsFloor':True,'allInteriorLayerTilesContained':True,'unsafeRearExitRemoved':True,'furniture':rows,'minimumSofaFrontClearance':min(o['clearanceToBuildingPixels']['front'] for o in rows if o['kind']=='in-sofa')}
(r/'review/footprint-audit.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='furniture'})
