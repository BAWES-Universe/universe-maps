"""Collision-only experiment. Do not publish; divider artwork has not moved yet."""
from pathlib import Path
import json,copy,shutil
R=Path(__file__).resolve().parents[1];S=R/'source/baseline-v05';Q=R/'source';O=R/'map32'
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
for name in ['runtime-layout.json','collision-grid.json','seats.json','garden-layout.json']:shutil.copy2(S/name,Q/name)
h=load(Q/'collision-grid.json');old=copy.deepcopy(h['grid']);g=h['grid']
for y in range(34,41):g[y][19]=0;g[y][27]=0
for y in range(33,41):g[y][18]=1;g[y][28]=1
for x in range(19,28):g[33][x]=1
m=load(O/'grand-auditorium.tmj');l=next(l for l in m['layers']if l['name']=='collision-permanent');gid=next(v for v in l['data']if v);l['data']=[gid if v else 0 for row in g for v in row];save(O/'grand-auditorium.tmj',m);save(Q/'collision-grid.json',h)
quiet=next(l for l in m['layers']if l['name']=='quiet-spawn-receiver');q=load(S/'quiet-grid.json');q['grid']=[[int(v>0)for v in quiet['data'][y*80:(y+1)*80]]for y in range(60)];q['rectangles']=[{'id':'spawn-receiver','xywh':[704,1760,128,128]}];save(Q/'quiet-grid.json',q)
a=load(Q/'runtime-layout.json');a['quietTileRectangles']=q['rectangles'];a['status']='Collision-only center-bay prototype; baseline divider art intentionally not updated'
for p in a['solidTileRectangles']:
 if p['id']=='lounge02-west-low-divider':p['xywh'][0]=576
 if p['id']=='lounge02-east-low-divider':p['xywh'][0]=896
 if p['id']=='lounge02-north-low-divider':p['xywh']=[608,1056,288,32]
for p in a['furniture']:
 if p['id']=='lounge02-west-low-divider':p['x']=576;p['solidFootprintXYWH'][0]=576
 if p['id']=='lounge02-east-low-divider':p['x']=896;p['solidFootprintXYWH'][0]=896
 if p['id']=='lounge02-north-low-divider':p['x']=608;p['width']=288;p['solidFootprintXYWH']=[608,1056,288,32]
save(Q/'runtime-layout.json',a)
changes=[{'cell':[x,y],'before':old[y][x],'after':g[y][x]}for y in range(60)for x in range(80)if old[y][x]!=g[y][x]]
save(R/'validation/center-bay-collision-prototype.json',{'status':'Collision-only candidate; native art and final route acceptance pending','delta':changes,'acceptedChairAndRugCoordinatesUnchanged':True,'bayInteriorWidth':288,'previousBayWidth':224,'westHallApproachWidth':64,'eastHallApproachWidth':96})
shutil.copy2('/workspace/shared/grand-auditorium-05-roofless-garden/validation/head-danger.bin',R/'validation/head-danger.bin')
print('changed cells',len(changes))
