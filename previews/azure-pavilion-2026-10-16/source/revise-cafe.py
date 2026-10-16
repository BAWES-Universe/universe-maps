import json,math
from pathlib import Path
D=Path('/workspace/coastal-pavilion');m=json.loads((D/'azure.tmj').read_text());g=json.loads((D/'geometry.json').read_text());C,R=40,32
blocked=[not((4<=x<36 and 12<=y<25)or(15<=x<25 and 25<=y<30)or(10<=x<30 and 4<=y<12)) for y in range(R) for x in range(C)]
def mark(x,y,w,h):
 for j in range(math.floor(y/32),math.ceil((y+h)/32)):
  for i in range(math.floor(x/32),math.ceil((x+w)/32)):blocked[j*C+i]=True
structure=[[320,128,640,32],[320,160,32,224],[928,160,32,224],[320,352,96,32],[864,352,96,32],[352,160,128,32],[800,160,128,32],[576,512,128,128],[192,448,64,64],[1024,448,64,64],[192,672,64,64],[1024,672,64,64],[352,224,32,128],[896,224,32,128],[512,160,64,64],[704,160,64,64]]
tables=[[448,256,32,32],[800,256,32,32],[608,864,64,32],[320,544,64,64],[896,544,64,64],[608,224,64,64]]
for b in structure+tables:mark(*b)
seats=[dict(id=n,x=x,y=y,approach='north',facing='down') for n,x,y in [('lounge-west-outer',408,272),('lounge-west-inner',504,272),('lounge-east-inner',760,272),('lounge-east-outer',856,272),('overlook-west',568,880),('overlook-east',696,880),('cafe-west-left',296,592),('cafe-west-right',408,592),('cafe-east-left',872,592),('cafe-east-right',984,592),('settee-left',600,216),('settee-middle',632,216),('settee-right',664,216)]]
for s in seats:
 assert not blocked[int(s['y']//32)*C+int(s['x']//32)],s
 assert not blocked[int((s['y']-32)//32)*C+int(s['x']//32)],s
m['layers'][1]['data']=[2562 if b else 0 for b in blocked];m['tilesets'][0]['image']='coastal-cafe.png';g.update(blocked=blocked,seats=seats,tables=tables,structure=structure)
(D/'azure.tmj').write_text(json.dumps(m,separators=(',',':'))+'\n');(D/'geometry.json').write_text(json.dumps(g,indent=2)+'\n')
p=D/'scene.js';s=p.read_text();start=s.index('const seats=');end=s.index(';',start);s=s[:start]+'const seats='+json.dumps(seats,separators=(',',':'))+s[end:];p.write_text(s)
print('Updated',len(seats),'occupancy positions,',len(tables),'table blockers; fractional tile bounds corrected')
