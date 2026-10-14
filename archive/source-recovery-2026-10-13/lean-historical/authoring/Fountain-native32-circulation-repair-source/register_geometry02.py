from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,heapq,math
R=Path(__file__).resolve().parent
# Native crop origin world640,1184. Deliberate conservative contour inside visible paving.
outer=[(60,188),(88,144),(130,105),(180,78),(232,64),(296,58),(352,65),(409,83),(456,113),(492,153),(514,196),(523,240),(512,288),(488,333),(450,367),(402,391),(344,407),(280,414),(216,403),(160,384),(112,353),(76,311),(56,267)]
# Permanent actual obstacle footprints of the two relocated benches and garden pots.
obstacles=[{'id':'stone-basin','type':'ellipse','box':[164,143,428,335]},
 {'id':'bench-northwest','type':'polygon','points':[(68,70),(126,41),(142, 74)]},
 {'id':'bench-west','type':'polygon','points':[(19,211),(39,207),(58,260),(36,274)]},
 {'id':'rim-north-flowers','type':'ellipse','box':[282,140,310,156]},
 {'id':'east-border-planter','type':'ellipse','box':[523,290,548,315]},
 {'id':'southwest-edge-planter','type':'ellipse','box':[27,284,58,308]}]
source=json.loads((R.parent/'map/collision-grid.json').read_text())
coarse8=np.zeros((source['height'],source['width']),np.uint8);coarse8.flat[source['blockedIndices']]=1
oldFine=(1-coarse8[1184//8:1632//8,640//8:1248//8]).repeat(8,0).repeat(8,1)
im=Image.fromarray(oldFine*255).convert('1');d=ImageDraw.Draw(im);d.polygon(outer,fill=1)
# Public avenue receiver below the loop remains open, and right path receiver.
# Outside the edited ring, retain the exact old fine geometry; no new path over the eastern garden curb.
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
art=Image.open(R/'fountain-ring-registered02.png').convert('RGBA');overlay=Image.new('RGBA',art.size);d=ImageDraw.Draw(overlay)
for y in range(14):
 for x in range(19):d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(255,40,30,42)if g[y,x]else(10,210,240,38),outline=(255,255,255,50))
if path:d.line([(x*32+16,y*32+8)for x,y in path],fill=(0,250,255),width=2)
Image.alpha_composite(art,overlay).save(R/'registered-ring-grid32-v2.png');im.save(R/'ring-walkable-fine-v2.png')
report={'status':'source-art collision proposal; no browser runtime','grid':32,'worldOrigin':[640,1184],'outer':outer,'obstacles':obstacles,'completeCycleFound':bool(path),'pathCells':path,'pathBodyCenters':[[640+x*32+16,1184+y*32+8]for x,y in path],'minimumGridLane':32,'blockedCells':[[int(x),int(y)]for y,x in np.argwhere(g)]}
(R/'ring-geometry02.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'completeCycleFound':bool(path),'steps':len(path)}))
