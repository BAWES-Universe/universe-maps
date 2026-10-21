from pathlib import Path
from PIL import Image
import json,bisect
R=Path(__file__).resolve().parent;root=R/'compact';m=json.loads((root/'campus.tmj').read_text());seats=json.loads((R.parent/'source/native-cafe-trial/candidate-layout.json').read_text())['seats'];sets=m['tilesets'];starts=[s['firstgid'] for s in sets];images={};cache={};layers=m['layers'][next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer')+1:]
def alpha(g):
 if g not in cache:
  s=sets[bisect.bisect_right(starts,g)-1];n=g-s['firstgid'];name=s['image']
  if name not in images:images[name]=Image.open(root/name).convert('RGBA')
  x=s.get('margin',0)+(n%s['columns'])*(16+s.get('spacing',0));y=s.get('margin',0)+(n//s['columns'])*(16+s.get('spacing',0));cache[g]=images[name].crop((x,y,x+16,y+16)).getchannel('A')
 return cache[g]
results=[]
for i,s in enumerate(seats):
 inside=2944<=s['x']<5088 and 2448<=s['y']<3040;green=s['group']=='greenhouse';hits=[]
 for l in layers:
  if l['type']!='tilelayer':continue
  visible=l['visible']
  if l['name']=='office-cover':visible=not inside
  if l['name'] in ['office-chair-fronts','office-glazing']:visible=inside
  if l['name'] in ['greenhouse-chair-fronts']:visible=green
  if not visible:continue
  covered=0
  for y in range(s['y']-16,s['y']-4):
   for x in range(s['x']-10,s['x']+10):
    g=l['data'][(y//16)*m['width']+x//16]
    if g and alpha(g).getpixel((x%16,y%16))>127:covered+=1
  if covered:hits.append({'layer':l['name'],'pixels':covered})
 results.append({'seat':i,'group':s['group'],'headBoxCoveredPixels':sum(h['pixels'] for h in hits),'layers':hits})
report={'method':'16-to-4 pixels above anchor, 20px wide head region; active foreground alpha >127','seats':results,'pass':all(x['headBoxCoveredPixels']==0 for x in results)}
(R/'evidence/seat-head-occlusion.json').write_text(json.dumps(report,indent=2)+'\n');print({'pass':report['pass'],'occluded':[x for x in results if x['headBoxCoveredPixels']]})
