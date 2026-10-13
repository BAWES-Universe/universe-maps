from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];m=json.load(open(R/'map32/esports-arena.tmj'));W=m['width']*32;H=m['height']*32;tiles={};report=[]
for ts in m['tilesets']:
 a=Image.open(R/'map32'/ts['image']).convert('RGBA')
 for i in range(ts['tilecount']):x=i%ts['columns']*32;y=i//ts['columns']*32;tiles[ts['firstgid']+i]=a.crop((x,y,x+32,y+32))
ims={}
for l in m['layers']:
 if l['name']not in ['runtime-base','runtime-above']:continue
 im=Image.new('RGBA',(W,H))
 for i,t in enumerate(l['data']):
  if t:im.paste(tiles[t],((i%m['width'])*32,(i//m['width'])*32))
 expected=Image.open(R/'assets'/(l['name']+'.png')).convert('RGBA');assert im.tobytes()==expected.tobytes();ims[l['name']]=im;report.append({'layer':l['name'],'pixelExact':True,'decodedFromActualRuntimeAtlases':True})
empty=Image.alpha_composite(ims['runtime-base'],ims['runtime-above']);empty.save(R/'review/COMPILED-empty-native.png');oc=ims['runtime-base'].copy();greg=Image.open(R/'assets/greg-reference.png').convert('RGBA');frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1)]};h=json.load(open(R/'source/collision-grid.json'));actors=json.load(open(R/'source/seats.json'))+h['socialAnchors']+h['landmarks']
for a in actors:oc.alpha_composite(frames[a.get('facing','north'if a.get('kind')in['spectator','team','caster']else'south')],(a['x']-16,a['y']-16))
oc.alpha_composite(ims['runtime-above']);oc.save(R/'review/COMPILED-occupied-native.png');assert oc.tobytes()==Image.open(R/'review/runtime-occupied-native.png').convert('RGBA').tobytes()
for name,box in [('west-team',(96,128,544,736)),('caster',(704,112,1344,480)),('spectator',(720,608,1328,1024)),('arrival-social',(1376,1056,1920,1376))]:oc.crop(box).save(R/f'review/COMPILED-native32-{name}.png')
(R/'validation/compiled-render.json').write_text(json.dumps({'pass':True,'layers':report,'occupiedMatchesSource':True,'actorFrameSize':[32,32],'runtimeContainsActors':False,'scope':'Offline raster decode of actual TMJ/PNG. Not a browser/device screenshot.'},indent=2)+'\n');print('Actual compiled raster reconstruction: PASS')
