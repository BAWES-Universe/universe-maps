"""Compile preserved artwork at native resolution with preserved32px physical footprints.
No generated/repainted art. Four near-side chairs move down8px; foreground fragments contain exact original pixels.
Run from this file's location; original32 source build remains under source/tools.
"""
from pathlib import Path
from PIL import Image
import json,hashlib,math,os
R=Path(__file__).resolve().parents[1];W,H,T=960,768,32
P=Path(os.environ.get('OUTDOOR_OFFICE_SOURCE',R/'source/archive-inputs')); A=P/'source/assets'; G=R/'source/generated'; G.mkdir(parents=True,exist_ok=True);layers={n:Image.open(A/f'layer-{n}.png').convert('RGBA') for n in ['ground','furniture','glass','structure']}
for item in json.loads((R/'source/inputs.json').read_text())['files']:
 assert hashlib.sha256((P/item['path']).read_bytes()).hexdigest()==item['sha256'], 'Pinned input differs: '+item['path']
old=json.loads((P/'map/studenthub-outdoor-office.tmj').read_text());oldc=next(l['data'] for l in old['layers'] if l['name']=='permanent-collisions');C=[[bool(oldc[y*30+x]) for x in range(30)] for y in range(24)]
footprints=[{'kind':'preserved-full-table-blocker','rect':[x,320,128,64]} for x in [352,672]]
placements=json.loads((P/'source/docs/asset-placements.json').read_text())
original=Image.new('RGBA',(W,H));moved=Image.new('RGBA',(W,H));relocations=[]
for p in placements:
 if p['layer']!='furniture':continue
 im=Image.open(A/(p['asset']+'.png')).convert('RGBA');assert im.size==(p['width'],p['height'])
 original.alpha_composite(im,(p['x'],p['y']));y=p['y']
 if p['asset']=='light-chair_n' and y==363:
  y+=8;relocations.append({'asset':p['asset'],'x':p['x'],'fromY':p['y'],'toY':y})
 moved.alpha_composite(im,(p['x'],y))
assert original.tobytes()==layers['furniture'].tobytes(), 'Original furniture reconstruction differs'
layers['furniture']=moved;moved.save(G/'layer-furniture-repositioned.png')
# Exact original tabletop pixels become foreground for far-side occupants.
# No broad rectangle paint; original alpha is retained.
fg=Image.new('RGBA',(W,H));table=Image.open(A/'light-meeting_table.png').convert('RGBA')
for x in [352,672]:fg.alpha_composite(table.crop((0,0,table.width,58)),(x,302))
chair=Image.open(A/'light-chair_n.png').convert('RGBA');seats=[]
for x0 in [352,672]:
 for dx in [24,80]:
  x=x0+dx
  seats.append({'id':f'table-{x0}-far-{dx}','x':x,'y':296,'facing':'down','egress':[{'x':x,'y':264}],'foreground':'original tabletop; head above y302'})
  seats.append({'id':f'table-{x0}-near-{dx}','x':x,'y':384,'facing':'up','egress':[{'x':x,'y':408}],'foreground':'original chair backrest pixels only'})
 for cx in [x0+10,x0+68]:fg.alpha_composite(chair.crop((0,8,chair.width,24)),(cx,379))
# Move selected existing pixels between layers instead of drawing them twice.
originalFurniture=layers['furniture'].copy(); mask=fg.getchannel('A').point(lambda a:255 if a else 0)
fg=Image.new('RGBA',(W,H));fg.paste(originalFurniture,(0,0),mask)
layers['furniture'].paste((0,0,0,0),(0,0,W,H),mask)
layers['furniture'].save(G/'layer-furniture-base.png')
layers['seat-foreground']=fg;fg.save(G/'layer-seat-foreground.png')
# Exact no-avatar reconstruction proves this is a layer split, not repainted art.
recombined=Image.alpha_composite(layers['furniture'],fg)
assert recombined.tobytes()==originalFurniture.tobytes(), 'Furniture pixels changed during layer split'

# Native32 cells retain the engine's normal pathfinding/body relationship.
cells={};tiles=[];data={}
for name,im in layers.items():
 arr=[]
 for y in range(0,H,T):
  for x in range(0,W,T):
   cell=im.crop((x,y,x+T,y+T));key=cell.tobytes()
   if not cell.getchannel('A').getbbox():arr.append(0);continue
   if key not in cells:cells[key]=len(tiles)+1;tiles.append(cell)
   arr.append(cells[key])
 data[name]=arr
marker=len(tiles)+1;tiles.append(Image.new('RGBA',(T,T)));columns=32;rows=math.ceil(len(tiles)/columns);atlas=Image.new('RGBA',(columns*T,rows*T))
for i,tile in enumerate(tiles):atlas.alpha_composite(tile,((i%columns)*T,(i//columns)*T))
(R/'map/tilesets').mkdir(exist_ok=True);atlas.save(R/'map/tilesets/native32.png')
ls=[]
def tl(name,arr):ls.append({'id':len(ls)+1,'name':name,'type':'tilelayer','width':W//T,'height':H//T,'x':0,'y':0,'visible':True,'opacity':1,'data':arr})
tl('permanent-collisions',[marker if c else 0 for row in C for c in row]);tl('ground',data['ground']);tl('furniture',data['furniture']);ls.append({'id':4,'name':'floorLayer','type':'objectgroup','objects':[],'visible':True,'opacity':1})
for n in ['seat-foreground','glass','structure']:tl(n,data[n])
areas=next(l for l in old['layers'] if l['name']=='areas');areas['id']=len(ls)+1
for o in areas['objects']:o['visible']=True
ls.append(areas)
m={**old,'layers':ls,'width':W//T,'height':H//T,'tilewidth':T,'tileheight':T,'nextlayerid':len(ls)+1,'tilesets':[{'firstgid':1,'name':'native32','image':'tilesets/native32.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':T,'tileheight':T,'columns':columns,'tilecount':len(tiles),'margin':0,'spacing':0,'tiles':[{'id':marker-1,'properties':[{'name':'collides','type':'bool','value':True}]}]}]}
(R/'map/studenthub-outdoor-office.tmj').write_text(json.dumps(m,separators=(',',':')))
(R/'source/seat-contract.json').write_text(json.dumps({'worldSize':[W,H],'avatarFrame':[32,32],'nativeBody':[16,16],'bodyOffsetFromAnchor':[-8,0],'seats':seats,'physicalFootprints':footprints,'chairRelocations':relocations,'maskSource':'Exact original table y0..58 and chair_n y8..24 pixels moved to foreground; four near-side chairs moved down8px.','limits':['No sitting API or pose change.','Desk and lounge seating not advertised as authored seats.','Fixed foreground; no arbitrary per-object y sorting.']},indent=2))
print(json.dumps({'tiles':len(tiles),'mapSize':[W//T,H//T],'worldSize':[W,H],'authoredSeats':len(seats)}))
