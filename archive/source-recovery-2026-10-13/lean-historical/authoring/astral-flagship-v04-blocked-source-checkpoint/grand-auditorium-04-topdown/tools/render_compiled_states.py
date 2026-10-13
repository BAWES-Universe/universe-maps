"""Render actual TMJ atlases in Tiled order for offline state/depth review."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
R=Path(__file__).resolve().parents[1];O=R/'map32';Q=R/'review';m=json.loads((O/'grand-auditorium.tmj').read_text());W,H=m['width']*32,m['height']*32
blank=lambda:Image.new('RGBA',(W,H),(16,44,50,255))
tiles={}
for ts in m['tilesets']:
 im=Image.open(O/ts['image']).convert('RGBA')
 for i in range(ts['tilecount']):tiles[ts['firstgid']+i]=im.crop(((i%ts['columns'])*32,(i//ts['columns'])*32,(i%ts['columns'])*32+32,(i//ts['columns'])*32+32))
greg=Image.open(R/'source/v03-greg-reference.png').convert('RGBA');cfg=json.loads((R/'source/runtime-layout.json').read_text())
def flatten(ls,prefix=''):
 for l in ls:
  if l['type']=='group':yield from flatten(l['layers'],prefix+l['name']+'/')
  else:yield prefix+l['name'],l
flat=list(flatten(m['layers']))
cache={}
for name,l in flat:
 if l['type']!='tilelayer':continue
 im=Image.new('RGBA',(W,H))
 for i,gid in enumerate(l['data']):
  if gid:im.alpha_composite(tiles[gid],((i%m['width'])*32,(i//m['width'])*32))
 if l.get('opacity',1)!=1:im.putalpha(im.getchannel('A').point(lambda a:round(a*l['opacity'])))
 cache[name]=im

def actor(im,x,y,frame=10):im.alpha_composite(greg.crop(((frame%3)*32,(frame//3)*32,(frame%3+1)*32,(frame//3+1)*32)),(int(x)-16,int(y)-16))
def render(hidden,actors=()):
 im=blank()
 for name,l in flat:
  if name=='floorLayer':
   for a in actors:actor(im,*a)
  elif l['type']=='tilelayer'and not any(name==h or name.startswith(h+'/')for h in hidden):im.alpha_composite(cache[name])
 return im
allactors=[]
for a in cfg['socialAnchors']:
 suffix=a['id'].rsplit('-',1)[-1];frame={'N':1,'S':10,'W':7,'E':4}.get(suffix,10);allactors.append((a['x'],a['y'],frame))
allactors += [(768,1824,10),(768,1392,1),(1504,1392,7),(1876,1240,10),(768,264,1)]
hallseats=json.loads((R/'source/seats.json').read_text());allactors +=[(s['x'],s['y'],10)for s in hallseats]
states={
 'outside-closed':(set(),[(768,1824,10)]),
 'foyer-revealed':({'v04-foyer-roof'},allactors),
 'hall-focused':({'v04-hall-roof','v04-foyer-roof','v04-surroundings-below','v04-surroundings-above'},[(768,264,1)]+[(s['x'],s['y'],10)for s in hallseats]),
 'architecture-overview':({'v04-hall-roof','v04-foyer-roof'},allactors),
}
ims={}
for name,(hidden,actors)in states.items():
 im=render(hidden,actors);im.save(Q/f'runtime-{name}-native.png');ims[name]=im
ims['foyer-revealed'].crop((32,960,1536,1808)).save(Q/'runtime-foyer-occupied-native.png')
ims['foyer-revealed'].crop((1472,1024,2560,1800)).save(Q/'runtime-terrace-occupied-native.png')
ims['hall-focused'].crop((96,176,1440,944)).save(Q/'runtime-hall-occupied-native.png')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda n,b=False:ImageFont.truetype(bold if b else font,n)
contact=Image.new('RGB',(1664,1496),(16,44,50));d=ImageDraw.Draw(contact);d.text((32,24),'FLAGSHIP v04 / COMPILED NATIVE LAYER STATES',font=f(28,True),fill='#f6e2ae')
for i,(name,label)in enumerate([('outside-closed','Outside: both roofs visible'),('foyer-revealed','In foyer: full foyer reveal'),('hall-focused','In auditorium: focused hall, surrounding art hidden'),('architecture-overview','Architecture review: both roofs omitted')]):
 x=32+(i%2)*824;y=92+(i//2)*660;d.text((x,y),label,font=f(18,True),fill='#ddb36b');contact.paste(ims[name].convert('RGB').resize((792,594),Image.Resampling.LANCZOS),(x,y+32))
d.text((32,1430),'Rendered from compiled TMJ atlases. Offline preview, not a live browser capture. Review actors are not baked into runtime.',font=f(17),fill='#bfd4cb');d.text((32,1458),'Full reveal is immediate. No translucent roof overlay during play. Map visibility does not hide remote participants or change media roles.',font=f(16),fill='#bfd4cb');d.text((32,1480),'RELEASE BLOCKED: native visibility-triggered tap replanning can select an adjacent tile. Visual/source review only.',font=f(15,True),fill='#eab57b');contact.save(Q/'runtime-layer-states.png')
# Preserve full context at a user-reviewable scale; no claim this all-open view is a live state.
ov=Image.new('RGB',(1664,1392),(16,44,50));d=ImageDraw.Draw(ov);d.text((40,24),'FLAGSHIP v04 / TOP-DOWN GARDEN AND LAYERED HALL',font=f(28,True),fill='#f6e2ae');d.text((40,68),'210 hall chairs + 16 lounge seats + 8 casual seats. Same native32 circulation and furniture geometry.',font=f(21),fill='#bfd4cb');ov.paste(ims['architecture-overview'].convert('RGB').resize((1584,1188),Image.Resampling.LANCZOS),(40,108));d.text((40,1320),'Architecture overview: roofs omitted for review. Actual entry/reveal states are shown separately.',font=f(20),fill='#ddb36b');d.text((40,1354),'Visual candidate only. Dynamic reveal runtime is blocked by a native tap-path fallback bug.',font=f(17,True),fill='#eab57b');ov.save(Q/'runtime-overview.png')
print('Rendered compiled atlases:',len(cache),'layers, four states and native occupied crops')
