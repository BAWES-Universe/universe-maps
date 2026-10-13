from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];assert len(list((R/'source/wokas').glob('woka-proof-*.png')))==8, 'Optional licensed Pipoya fixtures are excluded from delivery; restore authorized sheets per source/wokas/WOKA-PROOF.json before this preview/varied check';M=R/'map32';m=json.loads((M/'grand-auditorium.tmj').read_text());W,H=m['width']*32,m['height']*32
sets=[(t,Image.open(M/t['image']).convert('RGBA')) for t in m['tilesets']]
def flat(ls,p=''):
 for l in ls:
  if l['type']=='group':yield from flat(l['layers'],p+l['name']+'/')
  else:yield p+l['name'],l
layers=[]
for name,l in flat(m['layers']):
 im=None
 if l['type']=='tilelayer':
  im=Image.new('RGBA',(W,H))
  for i,g in enumerate(l['data']):
   if g:
    t,a=next((t,a)for t,a in reversed(sets) if t['firstgid']<=g);v=g-t['firstgid'];x=v%t['columns']*32;y=v//t['columns']*32;im.paste(a.crop((x,y,x+32,y+32)),((i%m['width'])*32,(i//m['width'])*32))
 layers.append((name,l,im))
fonts=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else'')+'.ttf',n)
sheets=[Image.open(p).convert('RGBA')for p in sorted((R/'source/wokas').glob('woka-proof-*.png'))];dirs={'north':10,'south':1,'west':4,'east':7};c=json.loads((R/'source/reveal-contract.json').read_text());cfg=json.loads((R/'source/runtime-layout.json').read_text());seats=json.loads((R/'source/seats.json').read_text())
def render(owners,actors):
 hidden={g for o in c['runtimeOwners'] if o['id'] in owners for g in o['hide']};out=Image.new('RGBA',(W,H))
 for name,l,im in layers:
  if name=='floorLayer':
   for i,(x,y,d)in enumerate(actors):
    k=dirs[d];sp=sheets[i%len(sheets)];frame=sp.crop((k%3*32,k//3*32,k%3*32+32,k//3*32+32));out.alpha_composite(frame,(round(x)-16,round(y)-16))
  if im is not None and l.get('opacity',1)!=0 and name.split('/')[0]not in hidden:out.alpha_composite(im)
 return out
social=[(p['x'],p['y'],p.get('direction','north')) for p in cfg['socialAnchors']];audience=[(q['x'],q['y'],'north')for q in seats[::9]];actors=social+audience+[(896,520,'south'),(896,2176,'north'),(1176,1807,'south'),(1176,1856,'north'),(896,1616,'north'),(1888,1648,'west'),(2208,816,'south')]
states=[('outside',[],[(896,2176,'north'),(1888,752,'west'),(1888,1648,'west')]),('inside',['hall','foyer'],actors)]
for name,owners,aa in states:
 im=render(owners,aa);im.save(R/'review'/f'glass-d-{name}-varied-native.png');im.convert('RGB').resize((1408,1216),Image.Resampling.LANCZOS).save(R/'review'/f'glass-d-{name}-preview.jpg',quality=94)
 for title,box in [('foyer-terrace',(96,1248,2688,2112)),('entrance',(480,1664,1344,2272)),('north-height',(96,0,1728,672))]:im.crop(box).save(R/'review'/f'glass-d-{name}-{title}-native.png')
# Review board uses decoded actual map layers, exact native Wokas; not a concept illustration.
board=Image.new('RGB',(1800,1710),'#102e34');d=ImageDraw.Draw(board);d.text((32,24),'GLASS D / COMPILED NATIVE32 CANDIDATE',font=fonts(32,True),fill='#f5d99a');d.text((32,73),'Stage + foyer layout preserved | Ivory stone continuity | Tall glass remains after entry',font=fonts(22),fill='#d9e4dd')
for i,(name,title) in enumerate([('outside','OUTSIDE / preserved portal, taller glazing'),('inside','INSIDE / varied Wokas, clear routes')]):
 x=32+i*884;d.text((x,124),title,font=fonts(19,True),fill='#efcf8c');im=Image.open(R/'review'/f'glass-d-{name}-varied-native.png');board.paste(im.convert('RGB').resize((850,734),Image.Resampling.LANCZOS),(x,158))
d.text((32,934),'LOWER FOYER + TERRACE / actual map detail',font=fonts(26,True),fill='#efcf8c');im=Image.open(R/'review/glass-d-inside-foyer-terrace-native.png');board.paste(im.convert('RGB').resize((1736,579),Image.Resampling.LANCZOS),(32,982));d.text((32,1595),'Static decoded TMJ preview. Eight original32px Woka variants. No gameplay or multiplayer claim.',font=fonts(20),fill='#d9e4dd');d.text((32,1636),'Open entrance fallback: no trapping auto-close. Source route/head validation is separate.',font=fonts(20),fill='#d9e4dd');board.save(R/'review/glass-d-review.jpg',quality=94)
print('Varied native32 previews rendered')
