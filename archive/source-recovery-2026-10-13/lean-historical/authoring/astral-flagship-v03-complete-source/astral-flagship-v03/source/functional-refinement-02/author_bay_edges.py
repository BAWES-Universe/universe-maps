from pathlib import Path
from PIL import Image
import json,hashlib
S=Path(__file__).resolve().parent;R=S.parents[1];A=R/'assets';W,H=2560,1920
rgba=lambda p:Image.open(p).convert('RGBA')
crops=[]
def author(name,master,box,size):
 im=rgba(master).crop(box);bb=im.getchannel('A').point(lambda x:255 if x>8 else 0).getbbox();im=im.crop(bb).resize(size,Image.Resampling.LANCZOS);p=A/(name+'.png');im.save(p)
 crops.append({'id':name,'asset':str(p.relative_to(R)),'source':str(master.relative_to(R)),'sourceCrop':list(box),'meaningfulAlphaTrim':list(bb),'alphaThreshold':8,'nativeSize':list(size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 return im
v=author('divider-vertical-low-32x256',S/'vertical-planter-master.png',(0,0,1024,1536),(32,256))
h352=author('divider-horizontal-low-352x48',R/'source/functional-refinement-01/south-dividers-master.png',(0,520,1536,1024),(352,48))
# Existing224px and320px complete horizontal dividers remain byte-for-byte unchanged.
placements=[]
def add(i,asset,x,y,fp):placements.append({'id':i,'asset':asset,'x':x,'y':y,'collisionFootprintXYWH':fp})
for gid,x0,x1,y in [('lounge-01',64,448,1056),('lounge-02',608,864,1056),('lounge-03',1088,1440,1056),('lounge-04',64,448,1440)]:
 for side,x in [('W',x0),('E',x1)]:add(gid+'-'+side,'assets/divider-vertical-low-32x256.png',x,y,[x,y,32,256])
for gid,x,y,w,asset in [('lounge-01',96,1056,352,'divider-horizontal-low-352x48'),('lounge-02',640,1056,224,'divider-lounge-02-south'),('lounge-03',1120,1056,320,'divider-lounge-03-south'),('lounge-04',96,1664,352,'divider-horizontal-low-352x48')]:
 add(gid+('-S' if gid=='lounge-04' else '-N'),'assets/'+asset+'.png',x,y-16,[x,y,w,32])
layout=json.loads((R/'source/art-layout.json').read_text());excluded=['lounge-01-planter','lounge-03-planter','lounge-04-planter','west-entry-edge']
base=rgba(R/'source/architecture-native.png');base.alpha_composite(rgba(R/'source/rugs-native.png'))
for item in layout['furniture']:
 if item['id'] in excluded:continue
 base.alpha_composite(rgba(R/item['asset']),(item['x'],item['y']))
for p in placements:base.alpha_composite(rgba(R/p['asset']),(p['x'],p['y']))
foreground=rgba(R/'source/foreground-native.png'); empty=base.copy();empty.alpha_composite(foreground)
greg=rgba(A/'greg-reference.png');frames={}
for n,fr in [('south',1),('north',10),('west',4),('east',7)]:frames[n]=greg.crop((fr%3*32,fr//3*32,fr%3*32+32,fr//3*32+32))
occupied=base.copy();seats=json.loads((R.parent/'grand-auditorium-01/source/seats.json').read_text())
for i,s in enumerate(seats):
 if(i*7)%17<10:occupied.alpha_composite(frames['north'],(s['x']-16,s['y']-16))
for a in layout['reviewActors']:occupied.alpha_composite(frames[a['direction']],(a['x']-16,a['y']-16))
occupied.alpha_composite(foreground)
occupied.save(S/'bay-edges-full-context-occupied-native.png');empty.save(S/'bay-edges-full-context-empty-native.png')
occupied.crop((0,928,2560,1856)).save(S/'bay-edges-foyer-terrace-occupied-native.png');occupied.crop((32,1008,1504,1744)).save(S/'bay-edges-foyer-occupied-native.png')
manifest={'status':'Supplemental art and placement preview only; frozen artwork and runtime untouched','generation':'Original built-in imagegen, exact prompt retained','components':crops,'placements':placements,'replaceExistingDecorationIDs':excluded,'openingIntent':'North-row bays fully open SOUTH. Lower-left bay fully open NORTH. These are low soft planted edges, not boxed room walls.','horizontalRegistration':'48px art sits16px north of the supplied32px collision base. All exact collision rectangles came from parent; parent integrates and tests.','verticalRegistration':'32×256 art lies within the exact supplied32×256 footprint. Originally generated overhead orientation; never flat-rotated from a horizontal sprite.','contextPreview':'Built from frozen art checkpoint positions, not a claim of final runtime registration, collisions, live depth or media.'}
(S/'bay-edge-kit.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
