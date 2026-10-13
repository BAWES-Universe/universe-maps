from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,heapq,math
R=Path(__file__).resolve().parent
# Native crop origin world640,1184. Deliberate conservative contour inside visible paving.
outer=[(86,201),(102,166),(137,137),(164,112),(202,90),(248,80),(294,79),(346,83),(392,98),(433,119),(469,153),(492,192),(504,238),(504,280),(489,325),(462,361),(417,387),(360,401),(297,409),(232,403),(176,389),(126,364),(92,332),(77,294),(76,254)]
# Permanent actual obstacle footprints of the two relocated benches and garden pots.
obstacles=[{'id':'stone-basin','type':'ellipse','box':[164,143,428,335]},
 {'id':'bench-northwest','type':'polygon','points':[(91,99),(169,69),(187,103),(111,137)]},
 {'id':'bench-west','type':'polygon','points':[(57,216),(79,212),(100,284),(78,296)]},
 {'id':'rim-north-flowers','type':'ellipse','box':[282,140,310,156]},
 {'id':'east-border-planter','type':'ellipse','box':[503,288,536,318]},
 {'id':'southwest-edge-planter','type':'ellipse','box':[52,302,89,330]}]
im=Image.new('1',(608,448));d=ImageDraw.Draw(im);d.polygon(outer,fill=1)
# Public avenue receiver below the loop remains open, and right path receiver.
d.rectangle((0,396,607,415),fill=1);d.rectangle((544,0,607,447),fill=1);d.polygon([(475,327),(548,327),(576,372),(576,415),(400,415)],fill=1)
for o in obstacles:
 if o['type']=='ellipse':d.ellipse(o['box'],fill=0)
 else:d.polygon(o['points'],fill=0)
a=np.asarray(im,np.uint8);g=1-a.reshape(14,32,19,32).min((1,3));
# Full cardinal winding route on32px grid around unchanged basin. Native body anchor at cell center x / tile top y+8 gives8px minimum vertical margin.
start=(9,12,0);target=(9,12,1);q=[(0,start)];dist={start:0};prev={};path=[]
while q:
 cost,s=heapq.heappop(q)
 if cost!=dist[s]:continue
 if s==target:
  while s!=start:path.append(s[:2]);s=prev[s]
  path.append(start[:2]);path=path[::-1];break
 x,y,w=s
 for nx,ny in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if not(0<=nx<19 and 0<=ny<14) or g[ny,nx]:continue
  dw=0
  if x==nx and x*32+16>296:
   if y*32+16<239<=ny*32+16:dw=1
   elif ny*32+16<239<=y*32+16:dw=-1
  nw=w+dw
  if not(-1<=nw<=1):continue
  ns=(nx,ny,nw);nc=cost+1
  if nc<dist.get(ns,99999):dist[ns]=nc;prev[ns]=s;heapq.heappush(q,(nc,ns))
art=Image.open(R/'fountain-ring-registered01.png').convert('RGBA');overlay=Image.new('RGBA',art.size);d=ImageDraw.Draw(overlay)
for y in range(14):
 for x in range(19):d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(255,40,30,42)if g[y,x]else(10,210,240,38),outline=(255,255,255,50))
if path:d.line([(x*32+16,y*32+8)for x,y in path],fill=(0,250,255),width=2)
Image.alpha_composite(art,overlay).save(R/'registered-ring-grid32.png');im.save(R/'ring-walkable-fine.png')
report={'status':'source-art collision proposal; no browser runtime','grid':32,'worldOrigin':[640,1184],'outer':outer,'obstacles':obstacles,'completeCycleFound':bool(path),'pathCells':path,'pathBodyCenters':[[640+x*32+16,1184+y*32+8]for x,y in path],'minimumGridLane':32,'blockedCells':[[int(x),int(y)]for y,x in np.argwhere(g)]}
(R/'ring-geometry01.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'completeCycleFound':bool(path),'steps':len(path)}))
