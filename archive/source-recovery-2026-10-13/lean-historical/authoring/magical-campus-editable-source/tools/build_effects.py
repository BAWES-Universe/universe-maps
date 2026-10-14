"""Compile existing garden preview motion into ordinary native-pixel Tiled frames.
No source art is altered; effects use integer translations and scalar alpha only.
"""
from PIL import Image,ImageChops,ImageDraw
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];S=R.parent/'universe-riverside-garden/layers';O=R/'effects';O.mkdir(exist_ok=True)
effects=[]
for name,box,world in [('river-water',(864,0,1024,1024),(3040,1920)),('fire-flame',(456,472,528,552),(2632,2392)),('fountain-water',(368,224,608,376),(1072,2000))]:
 source=(R.parent/'universe-campus-courtyard/layers/court-water.png') if name=='fountain-water' else S/('garden-water.png' if name=='river-water' else 'garden-fire.png');original=Image.open(source).convert('RGBA');base=original.crop(box);mask=base.getchannel('A');frames=[]
 if name=='river-water':
  stripes=Image.new('L',base.size);d=ImageDraw.Draw(stripes)
  for y in range(64,1024,96):d.rectangle((0,y,159,y+7),fill=255)
  mask=ImageChops.multiply(mask,stripes)
 for i in range(8):
  phase=i*math.tau/8;dy=round(math.sin(phase)*(.7 if name=='fire-flame' else 1.15));frame=Image.new('RGBA',base.size);frame.paste(base,(0,dy));a=ImageChops.multiply(frame.getchannel('A'),mask)
  gain=(.35+.12*math.sin(phase)) if name=='fire-flame' else (.7+.08*math.sin(phase))
  a=a.point(lambda x:round(x*gain));frame.putalpha(a);p=O/f'{name}-{i:02}.png';frame.save(p);frames.append(str(p.relative_to(R)))
 effects.append({'name':name,'origin':world,'size':base.size,'frames':frames,'duration':100 if name=='fire-flame' else 180,'source':str(source),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceCrop':box,'transform':'integer native-pixel vertical translation inside fixed original mask and scalar alpha','nativeAudioEnabled':False,'coverage':'Fixed sparse native river ripple bands' if name=='river-water' else 'Original source mask'})
(R/'effects/effects.json').write_text(json.dumps({'effects':effects},indent=2)+'\n');print('Prepared',len(effects),'fixed-position native effects')
