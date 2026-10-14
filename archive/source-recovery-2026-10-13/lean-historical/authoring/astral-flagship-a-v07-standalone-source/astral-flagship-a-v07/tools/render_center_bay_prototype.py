from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,copy,numpy as np
R=Path(__file__).resolve().parents[1];V=R/'source/reuse-v03';B=R/'source/reuse-v05/assets';cfg=json.loads((V/'runtime-layout.json').read_text());W,H=2560,1920
rgba=lambda p:Image.open(p).convert('RGBA')
def render(c):
 b=rgba(V/'architecture-native.png');b.alpha_composite(rgba(V/'rugs-native.png'));f=Image.new('RGBA',(W,H));anchors={q['id']:q for q in c['socialAnchors']}
 for p in c['furniture']:
  im=rgba(V/p['asset']);lo=im.copy();hi=Image.new('RGBA',im.size);an=anchors.get(p['id'])
  if an:
   y=p['foregroundFromLocalY'];x=an['x']-p['x'];cell=an['x']//32*32;box=(max(0,x-8,cell+8-p['x']),y,min(im.width,x+8,cell+24-p['x']),im.height);hi.paste(im.crop(box),(box[0],box[1]));lo.paste((0,0,0,0),box)
  b.alpha_composite(lo,(p['x'],p['y']));f.alpha_composite(hi,(p['x'],p['y']))
 opaque=Image.new('RGBA',(W,H),'#102e34');opaque.alpha_composite(b)
 return opaque,f
old,_=render(cfg);c=copy.deepcopy(cfg)
for p in c['furniture']:
 if p['id']=='lounge02-west-low-divider':p['x']=576
 if p['id']=='lounge02-east-low-divider':p['x']=896
 if p['id']=='lounge02-north-low-divider':p['x']=608;p['width']=288;p['asset']='assets/divider-native-288x48.png'
div=rgba(V/'assets/divider-horizontal-low-352x48.png');new=Image.new('RGBA',(288,48));new.alpha_composite(div.crop((0,0,144,48)),(0,0));new.alpha_composite(div.crop((208,0,352,48)),(144,0));new.save(V/'assets/divider-native-288x48.png');new,_=render(c)
base=rgba(B/'runtime-base.png');above=rgba(B/'runtime-above.png');box=(576,1040,928,1312)
assert old.crop(box).tobytes()==base.crop(box).tobytes(),'Existing base does not reconstruct exactly in planned patch'
base.paste(new.crop(box),box[:2]);base.save(R/'assets/runtime-base.png');above.save(R/'assets/runtime-above.png');rgba(B/'greg-reference.png').save(R/'assets/greg-reference.png')
actor=rgba(B/'greg-reference.png');frames={n:actor.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('east',7),('west',4)]}
def occupied(b):
 b=b.copy()
 for a in cfg['socialAnchors']:
  if a.get('group')=='lounge-02':b.alpha_composite(frames[a['direction']],(a['x']-16,a['y']-16))
 for x,y,d in [(560,1184,'north'),(976,1184,'south'),(768,1336,'north'),(624,1232,'north'),(880,1232,'north')]:b.alpha_composite(frames[d],(x-16,y-16))
 b.alpha_composite(above);return b
nativebox=(480,1008,1056,1392);before=occupied(rgba(B/'runtime-base.png')).crop(nativebox);after=occupied(base).crop(nativebox)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15);out=Image.new('RGB',(1184,452),'#123036');d=ImageDraw.Draw(out);d.text((16,10),'CENTER BAY / NATIVE1:1 COLLISION-FIRST STUDY',font=font,fill='#efc271');d.text((16,38),'BEFORE: narrow side strips',font=font,fill='white');d.text((608,38),'AFTER: same chairs/rug; dividers32px farther out',font=font,fill='white');out.paste(before,(16,62));out.paste(after,(608,62));out.save(R/'review/center-bay-before-after-native.png')
Image.alpha_composite(base,above).save(R/'review/runtime-empty-native.png')
a=np.asarray(rgba(B/'runtime-base.png'));z=np.asarray(base);diff=np.any(a!=z,axis=2);allow=np.zeros(diff.shape,bool);allow[1040:1312,576:928]=1
(R/'validation/center-bay-art-prototype.json').write_text(json.dumps({'changedPixels':int(diff.sum()),'changesOutsideDeclaredRectangle':int((diff&~allow).sum()),'repairRectangleXYXY':box,'nativeComponentsUnscaled':True,'acceptedChairPositionsUnchanged':True,'noRuntimeActorsBaked':True},indent=2)+'\n')
print('center bay art saved')
