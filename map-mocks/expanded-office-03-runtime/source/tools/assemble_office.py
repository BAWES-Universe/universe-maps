from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageFilter
import json,shutil,random,hashlib
R=Path(__file__).resolve().parents[1];D=json.loads((R/'geometry-work/source-coordinate-geometry.json').read_text());W,H=2496,1408;OX=OY=32
for f in ['layers','materials','docs']: (R/f).mkdir(exist_ok=True)
def prep(src,name,size):
 p=Path(src);shutil.copyfile(p,R/'art-source'/f'{name}-master.png');a=Image.open(p).convert('RGBA');b=a.getchannel('A').point(lambda n:255 if n>=32 else 0).getbbox();im=a.crop(b).convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA');im.save(R/'materials'/f'{name}.png');return im,b
plant,pb=prep('authoring-session/generated_images/exec-fe7385ad-185d-48b7-a996-b7129e48a3ce.png','low-planter',(96,48))
rug,rb=prep('authoring-session/generated_images/exec-c47ce8a3-8a0d-4af5-a5fe-77044f8cb8b0.png','pod-rug',(320,320))
wall=Image.open(R/'art-source/north-wall-master.png').convert('RGBA');wb=wall.getchannel('A').point(lambda n:255 if n>=64 else 0).getbbox();wall=wall.crop(wb).convert('RGBa').resize((128,64),Image.Resampling.LANCZOS).convert('RGBA');wall.save(R/'materials/north-wall-128x64.png')
station=Image.open('../universe-native-team-fixture/art-source/single-station-native.png').convert('RGBA');Image.Image.save(station,R/'materials/workstation.png')
backs=Image.open('../universe-native-team-fixture/art-source/fixture-chair-backs-native.png').convert('RGBA').crop((144,112,240,240));backs.save(R/'materials/workstation-back.png')
stone=Image.open(R/'materials/stone-floor-native.png').convert('RGBA');L={k:Image.new('RGBA',(W,H)) for k in ['ground','rugs','architecture','objects','chair-backs','plants-foreground','glass','signs']}
def paste(layer,im,x,y):L[layer].alpha_composite(im,(int(x+OX),int(y+OY)))
inside=lambda x,y:any(e['x']<=x<e['x']+e['width'] and e['y']<=y<e['y']+e['height'] for e in D['floor']['envelopes'])
# Authored16 stone materials are shuffled deterministically; no diagonal checker motif.
rng=random.Random(9231)
for y in range(0,1344,32):
 for x in range(0,2432,32):
  if inside(x,y):
   i=rng.randrange(16);piece=stone.crop(((i%4)*32,(i//4)*32,(i%4+1)*32,(i//4+1)*32));paste('ground',piece,x,y)
for pod in D['pods']:
 if pod['kind']=='team-pod':paste('rugs',rug,pod['x']+16,pod['y']+48)
# Original window/stone wall art is below avatars on rear edges; glass is independent.
for x in range(0,1984,128):paste('architecture',wall.crop((0,0,min(128,1984-x),64)),x,-32)
paste('architecture',wall,1984,416);paste('architecture',wall,2112,416);paste('architecture',wall,2240,416);paste('architecture',wall.crop((0,0,64,64)),2368,416)
# Short material pieces form continuous thick edge walls, never large floor rectangles above avatars.
brick=wall.crop((0,8,16,40))
for edge in D['permanentWalls']:
 x,y,w,h=[edge[k] for k in ['x','y','width','height']]
 if 'north' in edge['id'] or edge.get('material')=='permanent-glass-wall':continue
 for yy in range(y,y+h,32):
  for xx in range(x,x+w,16):paste('architecture',brick.crop((0,0,min(16,x+w-xx),min(32,y+h-yy))),xx,yy)
for s in D['stations']:
 a=s['assetCanvas'];paste('objects',station,a['x'],a['y']);paste('chair-backs',backs,a['x'],a['y'])
for p in D['lowDividers']:
 paste('objects',plant,p['x'],p['y']-16)
 fg=plant.copy();m=Image.new('L',plant.size);ImageDraw.Draw(m).rectangle((0,0,95,31),fill=255);fg.putalpha(ImageChops.multiply(fg.getchannel('A'),m));paste('plants-foreground',fg,p['x'],p['y']-16)
# Glazing has transparent surfaces, slim structural brass/wood frames and real open doors.
gd=ImageDraw.Draw(L['glass'])
for p in D['permanentWalls']:
 if p.get('material')!='permanent-glass-wall':continue
 x,y,w,h=[p[k] for k in ['x','y','width','height']];x+=OX;y+=OY
 gd.rectangle((x,y-20,x+w-1,y+h-1),fill=(47,116,127,25));gd.rectangle((x,y-22,x+w-1,y-19),fill=(134,113,70,240));gd.rectangle((x,y+h-5,x+w-1,y+h-1),fill=(118,96,60,248))
 if w>h:
  for xx in range(x,x+w,64):gd.rectangle((xx,y-20,xx+2,y+h-1),fill=(121,102,65,245))
 else:
  gd.rectangle((x,y-20,x+2,y+h-1),fill=(121,102,65,245));gd.rectangle((x+w-3,y-20,x+w-1,y+h-1),fill=(121,102,65,245))
# Reception and comfortable two-seat sofa retain exact native assets, with clear approaches.
a=R/'art-reception-lounge/native'
for file,x,y,fg in [('reception.png',1200,1168,'reception-front-occluder.png'),('sofa.png',256,1104,'sofa-foreground.png'),('coffee-table.png',288,1216,'coffee-table-front-occluder.png')]:
 paste('objects',Image.open(a/file).convert('RGBA'),x,y);paste('chair-backs',Image.open(a/fg).convert('RGBA'),x,y)
# A second light rug grounds the lounge, with all routes outside furniture contact.
paste('rugs',rug,208,1088)
# Measured named areas; signs are code-native typography, never AI text.
sd=ImageDraw.Draw(L['signs']);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for p in D['pods']:
 label=p['name'];x=p['x']+p['width']//2+OX;y=p['y']+18+OY;b=sd.textbbox((0,0),label,font=font);ww=b[2]-b[0]+24;sd.rounded_rectangle((x-ww//2,y-4,x+ww//2,y+22),4,fill=(242,225,181,244),outline=(128,100,56,255),width=1);sd.text((x,y+8),label,font=font,anchor='mm',fill=(37,69,73,255))
for label,x,y in [('Reception',1280,1264),('Lounge',368,1300),('Meeting A',2272,494),('Meeting B',2272,718),('Conference',2272,948)]:sd.text((x+OX,y+OY),label,font=font,anchor='mm',fill=(37,69,73,255),stroke_width=1,stroke_fill=(241,223,183,230))
# Original shared light/overhead shade will be added as independent authored planes next.
preview=Image.new('RGBA',(W,H),(14,31,39,255))
for n in ['ground','rugs','architecture','objects']:preview.alpha_composite(L[n])
greg=Image.open('../universe-native-team-fixture/assets/greg-reference.png').convert('RGBA').crop((32,96,64,128))
for s in D['stations'][:2]:preview.alpha_composite(greg,(s['seat']['x']+OX-16,s['seat']['y']+OY-16))
for n in ['chair-backs','plants-foreground','glass','signs']:preview.alpha_composite(L[n])
for n,im in L.items():im.save(R/'layers'/f'office-{n}.png')
preview.save(R/'docs/office-interior-assembly-01-native.png');preview.resize((1248,704),Image.Resampling.LANCZOS).save(R/'docs/office-interior-assembly-01-overview.png');preview.crop((32,32,1056,736)).save(R/'docs/office-first-teams-native.png')
(R/'docs/assembly-status.json').write_text(json.dumps({'status':'Full interior assembly in progress','native_canvas':[W,H],'geometry_translation':[OX,OY],'stations':28,'provisional_capacity':True,'working_art':['native workstations','reception','two-seat sofa','coffee table','shared stone floor','pod rugs','sandstone window walls','planted dividers','translucent meeting partitions'],'pending':['meeting furniture','common light/shade pass','TMJ compilation','final runtime routes and foreground validation'],'artifact':'Source compositor, not yet browser capture'},indent=2));print('Rendered full office source assembly',W,H)
