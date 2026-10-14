from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/layout-definition.json').read_text());L=json.loads((R/'evidence/layout.json').read_text());g=L['grid'];rows=[];front=[]
# Explicit whole-width floor bands traced from the complete r5 artwork. These are
# separate from path anchors, include both broad crossovers and both island aisles.
# Their continuous 64px strips are checked cell-by-cell, not by toe probes.
regions=[('west upper clear crossover','orchard',[256,192,416,256]),('west-middle north crossover','orchard',[448,224,672,288]),('cam-house broad stair landing','orchard',[736,192,800,256]),('east-middle north crossover','orchard',[896,224,1088,288]),('east upper crossover','orchard',[1120,192,1280,256]),('west inter-island clear aisle','orchard',[544,320,608,512]),('east inter-island clear aisle','orchard',[960,320,1024,512]),('south central crossover','orchard',[352,608,1184,672]),('wicket broad passage','orchard',[736,800,832,864]),('cam house center clear work floor','house',[192,192,576,288]),('house wide door throat','house',[320,320,448,384])]
for name,room,box in regions:
 ox,oy=L['rooms'][room]['offset'];x0,y0,x1,y1=box;bad=[]
 for y in range(y0,y1):
  for x in range(x0,x1):
   if g[(y+oy)//32][(x+ox)//32]:bad.append([x,y])
 rows.append(dict(name=name,room=room,box=box,minimumWidth=min(x1-x0,y1-y0),blockedPixels=len(bad),firstBlocked=bad[:4],**{'pass':not bad}))
# Enumerate EVERY blocked-frontier cell for human source review. This does not
# claim that the author's polygons substitute for independent image tracing.
for room,v in L['rooms'].items():
 ox,oy=v['offset'];w,h=v['size']
 for y in range(oy//32,(oy+h)//32):
  for x in range(ox//32,(ox+w)//32):
   if g[y][x] and any(0<=ny<len(g)and 0<=nx<len(g[0])and g[ny][nx]==0 for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):front.append(dict(room=room,cell=[x,y],bounds=[x*32,y*32,x*32+31,y*32+31]))
report=dict(allPass=all(v['pass']for v in rows),scope='Author full-width bare-floor bands, each pixel checked against emitted collision. Exact native fitting extrema and full continuous body routes are separately tested for every admitted tile. All blocked-frontier cells enumerated for independent semantic review; no live renderer claim.',bands=rows,blockedFrontierCells=front,frontierCount=len(front));(R/'evidence/full-floor.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='blockedFrontierCells'},indent=2));assert report['allPass']
