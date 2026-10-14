exec(open('/workspace/shared/magical-campus-standard32-09/fountain-study/test_phase.py').read().split('rows=[]')[0])
from itertools import combinations
# Actual outer paving contour re-registration candidate, pending visual inspection.
ring=[[232,400],[228,344],[236,288],[252,240],[280,200],[328,168],[384,144],[448,136],[512,144],[576,164],[632,200],[672,240],[696,288],[708,344],[712,384],[736,400]]
obs=[o['id']for o in m['obstacles']if o['id']!='fountain-stone-basin']
def geom(skip):
 im=Image.new('1',(1472,704));d=ImageDraw.Draw(im)
 for p in m['walkablePolygons']:d.polygon([tuple(v)for v in p],fill=1)
 d.polygon([tuple(v)for v in ring],fill=1)
 for o in m['obstacles']:
  if o['id'] in skip:continue
  if o['type']=='polygon':d.polygon([tuple(v)for v in o['points']],fill=0)
  else:
   x,y=o['cx'],o['cy'];rx=o.get('rx',o.get('radius'));ry=o.get('ry',o.get('radius'));d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=0)
 a=np.zeros((736,1504),bool);a[:704,:1472]=np.asarray(im,bool);return ~a.reshape(23,32,47,32).all((1,3))
rows=[]
for n in range(len(obs)+1):
 for skip in combinations(obs,n):
  p=solve(geom(skip),488,303)
  if p:rows.append({'hypotheticalMovedObstacles':skip,'path':p})
 if rows:break
print(json.dumps({'minimumCount':n,'options':rows[:8]}))
(R/'visible-boundary-diagnostic.json').write_text(json.dumps({'scope':'Actual paving re-registration candidate plus hypothetical obstacle relocation. Visual review required; NOT implemented','ringOuter':ring,'minimumCount':n,'options':rows},indent=2)+'\n')
