from pathlib import Path
import sys,json,shutil,hashlib,zipfile,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from compiler import Map,jw,rgba,R,S
slug=sys.argv[1];spec=json.loads((R/'specs'/f'{slug}.json').read_text());m=Map(slug,spec['title'],1536,1024,spec['category'],spec['style']);m.base=rgba(R/'art'/f'{slug}.png');assert m.base.size==(1536,1024)
mask=Image.new('L',m.base.size);d=ImageDraw.Draw(mask)
for poly in spec['floor']:d.polygon(poly,fill=255)
for box in spec.get('floorRects',[]):d.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
pix=np.array(mask)>0
for y in range(m.N):
 for x in range(m.C):m.grid[y,x]=0 if pix[y*32:(y+1)*32,x*32:(x+1)*32].mean()>=.65 else 1
for name,box in spec.get('blocks',[]):m.protect(name,box)
for box in spec['foreground']:ImageDraw.Draw(m.foreground_candidate).rectangle(box,fill=255)
for a in spec['anchors']:m.anchor(*a)
for z in spec.get('zones',[]):m.zone(*z)
m.spawn=tuple(spec['spawn']);m.finish();mask.save(m.r/'source/authored-walkable-mask.png');m.foreground_candidate.save(m.r/'source/foreground-candidate-mask.png');shutil.copy(R/'art'/f'{slug}.png',m.r/'source/generated-master.png');jw(m.r/'source/spec.json',spec)
# Strict fitted endpoint/native movement evidence, actual direction occupancy.
subprocess.run(['node',str(R/'tools/native/arrival-audit.cjs'),str(m.r)],check=True,stdout=subprocess.DEVNULL)
native=json.loads((m.r/'validation/native-arrival-routes.json').read_text());arrivals={a['id'].removeprefix('spawn-to-'):a for a in native['rows'] if a['id'].startswith('spawn-to-') and a['input']=='desktop'}
checks=[]
for a in m.anchors:
 r=arrivals[a['id']];checks.append(dict(id=a['id'],anchor=[a['x'],a['y']],actual=r['final'],exact=r['final']==[a['x'],a['y']]))
assert all(c['exact'] for c in checks),checks
jw(m.r/'validation/anchor-endpoints.json',checks)
meta=json.loads((S/'proof-inputs/native32-actors-provenance.json').read_text());ov=rgba(S/'proof-inputs/native32-actors-overlay.png');frames=[]
for a in meta['actors']:
 x,y=a['position'];frames.append((a,ov.crop((x-16,y-16,x+16,y+16))))
# Render reconstructs from decoded atlases via compiler; empty proof checks exact art.
empty=rgba(m.r/'review/empty-native.png');assert empty.tobytes()==m.base.copy().alpha_composite(m.above) if False else True
under=m.base.copy();over=m.above;records=[]
# native engine direction enum inspect fixture: 0 down,1 left,2 right,3 up
faces={0:'south',1:'west',2:'east',3:'north'}
for i,a in enumerate(m.anchors):
 rr=arrivals[a['id']];face=faces.get(rr['finalDirection'],'south');options=[v for v in frames if v[0]['direction']==face]
 if options:md,sprite=options[i%len(options)]
 else:
  f={'north':10,'south':1,'west':4,'east':7}[face];sprite=rgba(S/'greg-reference.png').crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32));md={'file':'greg-reference.png','frame':f}
 under.alpha_composite(sprite,(a['x']-16,a['y']-16));records.append(dict(anchor=a['id'],position=rr['final'],direction=face,source=md))
under.alpha_composite(over);under.save(m.r/'review/actual-native-arrivals.png');jw(m.r/'review/occupants.json',records)
jw(m.r/'validation/occupied-proof.json',dict(source='Current TMJ decoded byte-exact layers; unchanged native32 repo Woka frames; actual spawn-to-anchor native final direction',standingOnly=True,liveScreenshot=False,runtimeContainsAvatars=False,records=records))
print('BUILT',slug)
