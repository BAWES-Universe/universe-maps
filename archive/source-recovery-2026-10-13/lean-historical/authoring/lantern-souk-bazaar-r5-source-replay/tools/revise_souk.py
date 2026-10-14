from pathlib import Path
import sys,json,hashlib,shutil
import numpy as np
from PIL import Image
import build_maps as B
R=Path(__file__).resolve().parents[1];S=R/'source';slug='lantern-souk-bazaar-r5';DX=DY=192
B.R=R;B.S=S
m=B.Map(slug,'Lantern Souk Bazaar',1920,1280,'Social / market','Unlabelled lantern-lit courtyard with expanded twilight skyline')
# Generated border is context only; the entire accepted courtyard is pasted byte-exact.
m.base=B.rgba(S/'generated-panorama.png').resize((1920,1280),Image.Resampling.LANCZOS)
original=B.rgba(S/'bazaar-environment-clear-entry-master.png');m.base.paste(original,(DX,DY))
old=json.loads((S/'layout.json').read_text());g=np.array(old['grid'],np.uint8)
# Clear retired north-facing chairs and old table only within the rug/approach.
g[19:23,21:27]=0
# Table and actual side-facing backrests, protecting their visible solid bounds.
g[19:21,23:25]=1;g[19:21,21]=1;g[19:21,26]=1
m.grid[6:38,6:54]=g
m.spawn=(old['start'][0]+DX,old['start'][1]+DY)
for a in old['anchors']:
 if a['id']=='spawn' or a['id'].startswith('fountain-social'):continue
 a={k:v for k,v in a.items() if k in ['id','x','y','direction','kind']};a['x']+=DX;a['y']+=DY;a['id']=a['id'].replace('seller-demo-','court-').replace('-demo-door','-court-door').replace('bot-display','east-stall');m.anchors.append(a)
# No setup labels, named demo areas, arbitrary service defaults, or seller/bot placeholders.
m.areas=[]
for f in old['protectedFixtures']:
 f['solidXYXY']=[v+(DX if i%2==0 else DY) for i,v in enumerate(f['solidXYXY'])];m.fixtures.append(f)
m.asset('low-lounge-table',736+DX,630+DY)
m.asset('lounge-chair-east',686+DX,623+DY)
m.asset('lounge-chair-west',808+DX,623+DY)
m.anchor('fountain-social-left',712+DX,647+DY,'east')
m.anchor('fountain-social-right',824+DX,647+DY,'west')
m.fixtures.extend([dict(name='carpet-low-table',solidXYXY=[736+DX,608+DY,800+DX,672+DY],rule='Protect table whole visible footprint'),dict(name='left-seat-back',solidXYXY=[672+DX,608+DY,704+DX,672+DY],rule='Backrest protected; upholstered seat remains accessible'),dict(name='right-seat-back',solidXYXY=[832+DX,608+DY,864+DX,672+DY],rule='Backrest protected; upholstered seat remains accessible')])
m.finish()
# The source court must remain byte exact outside the three requested furniture placements.
actual=np.array(Image.alpha_composite(m.base,m.above).crop((DX,DY,DX+1536,DY+1024)));ref=np.array(original);allowed=np.zeros(ref.shape[:2],bool)
for n,x,y in [('low-lounge-table',736,630),('lounge-chair-east',686,623),('lounge-chair-west',808,623)]:
 art=B.rgba(S/(n+'.png'));allowed[y:y+art.height,x:x+art.width]=True
changed=np.any(actual!=ref,axis=2);assert not np.any(changed&~allowed)
B.jw(m.r/'validation/preservation.json',dict(originalCourtOffset=[DX,DY],originalCourtSize=[1536,1024],canvas=[1920,1280],expandedLeft=192,expandedRight=192,expandedTop=192,expandedBottom=64,courtyardUnchangedOutsideFurniture=True,changedOriginalPixels=int(changed.sum()),carpetUnderlyingMasterUnchanged=True,removedLabelsFromSource=True,editorDemoAreasRemoved=True,opposedSeats=['east','west'],generatedBorderOnly=True))
for f in S.iterdir():
 if f.is_file():shutil.copy2(f,m.r/'source'/f.name if f.name!='layout.json' else m.r/'source/baseline-layout.json')
print(m.r)
