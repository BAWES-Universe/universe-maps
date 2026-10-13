"""Decode the actual runtime atlases for state/native review; no art resampling."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];M=R/'map32';m=json.loads((M/'grand-auditorium.tmj').read_text());W,H=m['width']*32,m['height']*32
sets=[]
for s in m['tilesets']:sets.append((s,Image.open(M/s['image']).convert('RGBA')))
def flat(layers,prefix=''):
 out=[]
 for l in layers:
  if l['type']=='group':out.extend(flat(l['layers'],prefix+l['name']+'/'))
  else:out.append((prefix+l['name'],l))
 return out
layers=[]
for name,l in flat(m['layers']):
 if l['type']!='tilelayer':layers.append((name,l,None));continue
 im=Image.new('RGBA',(W,H))
 for n,gid in enumerate(l['data']):
  if not gid:continue
  s,a=next((s,a)for s,a in reversed(sets)if s['firstgid']<=gid);v=gid-s['firstgid'];x=v%s['columns']*32;y=v//s['columns']*32;tile=a.crop((x,y,x+32,y+32));im.paste(tile,((n%m['width'])*32,(n//m['width'])*32))
 layers.append((name,l,im))
font=lambda s,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold'if b else'')+'.ttf',s)
greg=Image.open(R/'assets/greg-reference.png').convert('RGBA');dirs={'north':10,'south':1,'west':4,'east':7};frames={d:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for d,i in dirs.items()}
c=json.loads((R/'source/reveal-contract.json').read_text());cfg=json.loads((R/'source/runtime-layout.json').read_text())
states={'outside':[], 'foyer':['foyer'], 'hall':['hall'], 'both':['hall','foyer']}
def render(state,actors=[]):
 hidden=set(g for o in c['runtimeOwners']if o['id']in states[state]for g in o['hide']);out=Image.new('RGBA',(W,H))
 for name,l,im in layers:
  if name=='floorLayer':
   for x,y,d in actors:out.alpha_composite(frames[d],(round(x)-16,round(y)-16))
  if im is None or l.get('opacity',1)==0 or name.split('/')[0]in hidden:continue
  out.alpha_composite(im)
 return out
actors={'outside':[(896,2176,'north'),(1888,752,'west'),(1888,1648,'west')],'foyer':[(896,2032,'north'),(1176,1807,'south'),(1176,1856,'north')]+[(a['x'],a['y'],a.get('direction','north'))for a in cfg['socialAnchors']if a.get('group')],'hall':[(896,520,'south'),(336,687,'north'),(1456,1071,'north')],'both':[(896,520,'south'),(688,1248,'north'),(1104,1296,'south')]}
for st in states:
 render(st).save(R/'review'/f'building-c-{st}-empty-native.png');render(st,actors[st]).save(R/'review'/f'building-c-{st}-occupied-native.png')
# Overview is explicitly reduced; assets and native crops are not.
card=Image.new('RGB',(1736,1580),'#123039');d=ImageDraw.Draw(card);d.text((24,18),'BUILDING C / COMPILED NATIVE32 CANDIDATE',font=font(28,True),fill='#f3d398');d.text((24,60),'Proportional architecture • Garden B materials • Independent room reveal',font=font(19),fill='#d4e3dc')
for i,(st,title)in enumerate([('outside','OUTSIDE / façade restored'),('foyer','FOYER / hall still covered'),('both','HALL + FOYER / safe cutaway')]):
 x=24+i*572;d.text((x,112),title,font=font(17,True),fill='#efd092');im=render(st,actors[st]);card.paste(im.resize((563,486),Image.Resampling.LANCZOS),(x,148))
for i,(st,xy,box,title)in enumerate([('outside',(896,2176,'north'),(512,1696,1280,2304),'Outside approach'),('foyer',(896,2112,'north'),(512,1696,1280,2304),'Foyer entry reveal')]):
 x=24+i*864;d.text((x,668),title+' • native1:1',font=font(22,True),fill='#efd092');card.paste(render(st,[xy]).crop(box),(x,710))
d.text((24,1370),'Decoded from the TMJ atlases. Ordinary exterior camera; native hall focus is separate.',font=font(20),fill='#d4e3dc');d.text((24,1404),'Source route/state results are documented separately. These panels are not live gameplay.',font=font(20),fill='#d4e3dc');card.save(R/'review/building-c-compiled-overview.png')
for name,box,pts in [('south',(512,1696,1280,2304),[('outside',(896,2176,'north')),('foyer',(896,2112,'north')),('foyer',(896,2016,'north'))]),('hall-east',(1472,416,2048,992),[('outside',(1888,752,'west')),('hall',(1832,752,'west')),('hall',(1664,752,'west'))]),('foyer-east',(1472,1312,2048,1888),[('outside',(1888,1648,'west')),('foyer',(1832,1648,'west')),('foyer',(1664,1648,'west'))])]:
 cw,ch=box[2]-box[0],box[3]-box[1];sheet=Image.new('RGB',(cw*3+48,ch+106),'#123039');draw=ImageDraw.Draw(sheet);draw.text((12,12),name.upper()+' / OUTSIDE → REVEAL → INSIDE / NATIVE1:1',font=font(22,True),fill='#f3d398')
 for i,(state,actor)in enumerate(pts):sheet.paste(render(state,[actor]).crop(box),(12+i*(cw+12),70))
 sheet.save(R/'review'/f'building-c-{name}-sequence-native.png')
print('Compiled state and native crops rendered')
