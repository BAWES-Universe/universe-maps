from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,heapq
R=Path('/workspace/shared/magical-campus-standard32-09/fountain-study');S=Path('/workspace/shared/magical-campus-return-08/office-divider-study/campus-visible-divider-candidate/sources/court')
m=json.loads((S/'module.json').read_text());im=Image.new('1',(1472,704));d=ImageDraw.Draw(im)
for p in m['walkablePolygons']:d.polygon([tuple(v) for v in p],fill=1)
for o in m['obstacles']:
 t=o['type']
 if t=='polygon':d.polygon([tuple(v) for v in o['points']],fill=0)
 else:
  x,y=o['cx'],o['cy'];rx=o.get('rx',o.get('radius'));ry=o.get('ry',o.get('radius'));d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=0)
fine=np.asarray(im,bool)
def solve(grid,cx,cy):
 h,w=grid.shape;start=(round(cx/32),14,0);target=(*start[:2],1);dist={start:0};prev={};q=[(0,start)]
 while q:
  cost,s=heapq.heappop(q)
  if cost!=dist[s]:continue
  if s==target:
   path=[]
   while s!=start:path.append(list(s[:2]));s=prev[s]
   path.append(list(start[:2]));return path[::-1]
  x,y,wind=s
  for nx,ny in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(6<=nx<24 and 3<=ny<=16) or grid[ny,nx]:continue
   dw=0
   if x==nx and x*32+16>cx:
    if y*32+16<cy<=ny*32+16:dw=1
    elif ny*32+16<cy<=y*32+16:dw=-1
   nw=wind+dw
   if not(-1<=nw<=1):continue
   nxt=(nx,ny,nw);new=cost+1
   if new<dist.get(nxt,99999):dist[nxt]=new;prev[nxt]=s;heapq.heappush(q,(new,nxt))
 return None
rows=[]
for dy in[0,8,16,24]:
 for dx in[0,8,16,24]:
  a=np.zeros((736,1504),bool);a[dy:dy+704,dx:dx+1472]=fine;g=~a.reshape(23,32,47,32).all((1,3));p=solve(g,488+dx,303+dy)
  rows.append({'shift':[dx,dy],'cycleFound':p is not None,'path':p})
(R/'phase-test.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
