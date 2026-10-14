exec(open('/workspace/shared/magical-campus-standard32-09/fountain-study/test_phase.py').read().split('rows=[]')[0])
from itertools import combinations

def geom(skip):
 im=Image.new('1',(1472,704));d=ImageDraw.Draw(im)
 for p in m['walkablePolygons']:d.polygon([tuple(v)for v in p],fill=1)
 for o in m['obstacles']:
  if o['id'] in skip:continue
  if o['type']=='polygon':d.polygon([tuple(v)for v in o['points']],fill=0)
  else:
   x,y=o['cx'],o['cy'];rx=o.get('rx',o.get('radius'));ry=o.get('ry',o.get('radius'));d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=0)
 a=np.zeros((736,1504),bool);a[:704,:1472]=np.asarray(im,bool);return ~a.reshape(23,32,47,32).all((1,3))
obs=[o['id']for o in m['obstacles'] if o['id']!='fountain-stone-basin'];rows=[]
for n in range(len(obs)+1):
 for skip in combinations(obs,n):
  g=geom(skip);path=solve(g,488,303)
  if path:rows.append({'hypotheticalMovedObstacles':skip,'path':path})
 if rows:break
(R/'obstacle-relocation-lower-bound.json').write_text(json.dumps({'scope':'Diagnostic hypothetical removal to identify source components that require real visible relocation; NOT proposed collision removal','minimumCount':n,'options':rows},indent=2)+'\n');print(json.dumps({'minimumCount':n,'optionCount':len(rows),'options':rows[:4]}))
