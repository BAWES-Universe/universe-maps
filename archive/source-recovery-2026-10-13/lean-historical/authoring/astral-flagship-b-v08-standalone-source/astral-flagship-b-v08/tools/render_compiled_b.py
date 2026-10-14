from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];M=R/'map32';Q=R/'review';m=json.loads((M/'grand-auditorium.tmj').read_text());W,H=m['width']*32,m['height']*32
rgba=lambda p:Image.open(p).convert('RGBA');fonts='/usr/share/fonts/truetype/dejavu/';font=lambda n:ImageFont.truetype(fonts+'DejaVuSans.ttf',n);bold=lambda n:ImageFont.truetype(fonts+'DejaVuSans-Bold.ttf',n)
tiles={}
for t in m['tilesets']:
 im=rgba(M/t['image'])
 for n in range(t['tilecount']):tiles[t['firstgid']+n]=im.crop((n%t['columns']*32,n//t['columns']*32,n%t['columns']*32+32,n//t['columns']*32+32))
actors=rgba(R/'source/qa-actors-final-b.png');frames=[];records=[]
for frame in range(4):
 lo=Image.new('RGBA',(W,H));hi=Image.new('RGBA',(W,H));above=False
 for l in m['layers']:
  if l['name']=='floorLayer':above=True
  if l['type']!='tilelayer'or l.get('opacity',1)==0 or l.get('visible',True)==False:continue
  target=hi if above else lo
  for i,g in enumerate(l['data']):
   if not g:continue
   if l['name']=='garden-native-animation':g+=frame
   target.alpha_composite(tiles[g],((i%m['width'])*32,(i//m['width'])*32))
 empty=Image.alpha_composite(lo,hi);out=Image.alpha_composite(Image.alpha_composite(lo,actors),hi);frames.append(out)
 if frame==0:
  empty.save(Q/'flagship-b-runtime-empty-native.png');out.save(Q/'flagship-b-runtime-occupied-native.png')
  for name,box in [('pavilion',(1888,32,2432,416)),('terrace',(1504,1024,2528,1792)),('gate',(2048,960,2368,1216))]:out.crop(box).save(Q/f'flagship-b-runtime-{name}-native.png')
 # Three exact native foliage crops; no magnification.
 card=Image.new('RGBA',(768,288),'#123036');d=ImageDraw.Draw(card)
 for i,(x,y)in enumerate([(51,24),(58,5),(75,27)]):card.alpha_composite(out.crop((x*32-112,y*32-112,x*32+144,y*32+144)),(i*256,32));d.text((i*256+8,10),'Native32 garden leaf accent',font=font(13),fill='#f0d092')
 records.append(card.convert('RGB'))
records[0].save(Q/'flagship-b-animation-native.gif',save_all=True,append_images=records[1:],duration=[350,450,350,650],loop=0,disposal=2)
board=Image.new('RGB',(1664,1400),'#123036');d=ImageDraw.Draw(board);d.text((40,22),'FLAGSHIP B / GARDEN AND COFFEE',font=bold(29),fill='#f6d394');d.text((40,70),'Outdoor limestone and timber • Paired pavilion seating • Three gentle native animated accents',font=font(20),fill='#bfd5d0');board.paste(frames[0].convert('RGB').resize((1584,1188),Image.Resampling.LANCZOS),(40,112));d.text((40,1321),'Compiled native32 map artwork. Accepted hall, meeting rooms and corrected reception retained.',font=font(20),fill='#f3cc80');d.text((40,1356),'Static first-frame overview. Source/fixture checks are separate from live room and media testing.',font=font(18),fill='#b8ccc6');board.save(Q/'flagship-b-runtime-overview.png')
# The art layers round-trip separately in the compiler; this proof additionally includes native animation GIDs.
(R/'validation/compiled-render.json').write_text(json.dumps({'tmjSHA256':hashlib.sha256((M/'grand-auditorium.tmj').read_bytes()).hexdigest(),'frameCount':4,'animatedPlacements':3,'native32':True,'actorsBakedIntoRuntime':False,'renderedFromActualEmbeddedAtlasGIDs':True,'liveScreenshot':False},indent=2)+'\n')
print('Rendered all four compiled animation states and native occupied previews')
