from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[1]
class MapRenderer:
 def __init__(self,path):
  self.path=Path(path);self.m=json.loads(self.path.read_text());self.sets=self.m['tilesets'];self.images={}
  for s in self.sets:
   p=self.path.parent/s['image']
   if not p.exists():p=(R/'dependencies/public/butterfly-town/gate-b/v3'/s['image']).resolve()
   self.images[s['name']]=Image.open(p).convert('RGBA')
  self.anims={s['firstgid']+t['id']:(s,t['animation'])for s in self.sets for t in s.get('tiles',[])if 'animation'in t}
 def tile(self,gid,ms=0):
  flags=gid&0xf0000000;gid&=0x0fffffff
  if gid in self.anims:
   s,frames=self.anims[gid];tick=ms%sum(f['duration']for f in frames)
   for f in frames:
    if tick<f['duration']:gid=s['firstgid']+f['tileid'];break
    tick-=f['duration']
  s=next(s for s in reversed(self.sets)if s['firstgid']<=gid);j=gid-s['firstgid'];x=j%s['columns']*32;y=j//s['columns']*32;t=self.images[s['name']].crop((x,y,x+32,y+32))
  if flags&0x20000000:t=t.transpose(Image.Transpose.TRANSPOSE)
  if flags&0x80000000:t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if flags&0x40000000:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  return t
 def compose(self,ms=0,player=None,draw_foreground=True):
  im=Image.new('RGBA',(960,1440),self.m['backgroundcolor']);playerDrawn=False
  for l in self.m['layers']:
   if l['name']=='floorLayer'and player:
    self.draw_woka(im,player);playerDrawn=True
   if l['type']!='tilelayer'or not l.get('visible',True):continue
   if l['name']=='gate-balcony-foreground'and not draw_foreground:continue
   for i,g in enumerate(l['data']):
    if not g:continue
    t=self.tile(g,ms)
    if l.get('opacity',1)!=1:t.putalpha(t.getchannel('A').point(lambda a:round(a*l['opacity'])))
    im.alpha_composite(t,(i%30*32,i//30*32))
  if player and not playerDrawn:self.draw_woka(im,player)
  return im
 def draw_woka(self,im,p):
  w=Image.open(R/'validation/greg.png').convert('RGBA').crop((32,96,64,128));im.alpha_composite(w,(round(p['x'])-16,round(p['y'])-16))
