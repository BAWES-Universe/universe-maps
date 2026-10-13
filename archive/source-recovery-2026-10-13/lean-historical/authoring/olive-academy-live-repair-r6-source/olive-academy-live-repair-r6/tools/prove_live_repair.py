from pathlib import Path
import json,sys,hashlib
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'));from build_contexts import decode
p=R/'maps/olive-academy-live-repair-r6';old=R/'final/olive-academy-context-r5b';out=p/'review';J=lambda f:json.loads(f.read_text());m=J(p/'map32/map.tmj');l=J(p/'source/layout.json');g=l['collision'];actors=Image.open(R/'source-assets/r6-proof-actors.png').convert('RGBA');sprite=actors.crop((1216,319,1248,351));probes=[('floor-border',400,751),('west-canopy',304,783),('east-canopy',816,783),('classroom-corner',880,687),('lounge-corner',1072,463),('lounge-wall',1168,431),('upper-pier-base',1072,607),('lower-pier-base',1072,847)]
def clear(x,y):return all(not g[yy][xx] for yy in range(y//32,(y+15)//32+1) for xx in range((x-8)//32,(x+7)//32+1))
assert all(clear(x,y) for _,x,y in probes)
for name,x,y in probes:
 panels=[]
 for tag,root in [('before',old),('after',p)]:
  b,a=decode(root,J(root/'map32/map.tmj'));b.alpha_composite(sprite,(x-16,y-16));b.alpha_composite(a)
  box=(x-96,y-80,x+96,y+80);crop=b.crop(box).resize((576,480),Image.Resampling.NEAREST)
  panel=Image.new('RGB',(576,514),'#17212a');panel.paste(crop,(0,34));ImageDraw.Draw(panel).text((12,10),tag.upper()+' | '+name+' | native player ('+str(x)+','+str(y)+')',fill='white');panels.append(panel)
 proof=Image.new('RGB',(1152,514));proof.paste(panels[0],(0,0));proof.paste(panels[1],(576,0));proof.save(out/(name+'-before-after.png'))
# Quantify actual head opacity, not a binary threshold incorrectly treating translucent foliage as invisibility.
geo=np.load(R/'geometry-checks/olive-academy-live-repair-r6/geometry-masks.npz');clearpos=geo['clear'];above=np.array(decode(p,m)[1])[:,:,3];head=np.array(J(R/'source-assets/native-head-geometry.json'),bool);maxalpha=np.zeros_like(above)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(1536,1536-dx);y0=max(0,-dy);y1=min(1216,1216-dy);maxalpha[y0:y1,x0:x1]=np.maximum(maxalpha[y0:y1,x0:x1],above[y0+dy:y1+dy,x0+dx:x1+dx])
result={'bodyClearIntegerPositions':int(clearpos.sum()),'opaqueHeadConflictPositions':int((clearpos&(maxalpha>=128)).sum()),'translucentFoliageHeadPositions':int((clearpos&(maxalpha>0)&(maxalpha<128)).sum()),'maxForegroundAlphaAtReachableHeads':int(maxalpha[clearpos].max()),'allProbeBodiesClear':True,'probes':[{'name':n,'position':[x,y]} for n,x,y in probes],'scope':'Native32 pinned motion replay plus exact-TMJ static layer compositing. No live browser, keyboard physics, device or multi-user assertion.'}
(p/'DEPTH-REPAIR-CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

Image.open(R/'geometry-checks/olive-academy-live-repair-r6/collision-overlay.png').crop((32,576,1024,800)).save(out/'classroom-wall-collision-overlay.png')
