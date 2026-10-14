import json,bisect
from pathlib import Path
from PIL import Image,ImageDraw
SOURCE=Path('/workspace/shared/recovered-campus06/public/butterfly-town/v6/map16')
WORK=Path(__file__).parent
m=json.loads((SOURCE/'magical-campus.tmj').read_text())
atlases={t['firstgid']:Image.open(SOURCE/t['image']).convert('RGBA') for t in m['tilesets']}
firsts=sorted(atlases)
sets={t['firstgid']:t for t in m['tilesets']}
def tile(gid):
 if not gid:return None
 assert gid<0x20000000
 f=firsts[bisect.bisect_right(firsts,gid)-1];t=sets[f];n=gid-f;x=(n%t['columns'])*16;y=(n//t['columns'])*16
 return atlases[f].crop((x,y,x+16,y+16))
def render(names,mapobj=m):
 out=Image.new('RGBA',(m['width']*16,m['height']*16))
 for l in mapobj['layers']:
  if l['name'] not in names:continue
  for i,g in enumerate(l['data']):
   if g:out.alpha_composite(tile(g),(i%m['width']*16,i//m['width']*16))
 return out
if __name__=='__main__':
 names=[l['name'] for l in m['layers'] if l['type']=='tilelayer' and l['name']!='collision-permanent']
 full=render(names); full.save(WORK/'source-map.png');full.resize((1280,1152)).save(WORK/'source-overview.png')
 for name in ['base','fixed-foreground','campus-effects']:
  render([name]).save(WORK/(name+'.png'))
 print('rendered')
