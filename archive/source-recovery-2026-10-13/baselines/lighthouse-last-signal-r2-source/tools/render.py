from PIL import Image
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];m=json.loads((R/'runtime/lighthouse-last-signal.tmj').read_text());(R/'review').mkdir(exist_ok=True)
cache={}
for t in m['tilesets']:
 a=Image.open(R/'runtime'/t['image']).convert('RGBA')
 for i in range(t['tilecount']):cache[t['firstgid']+i]=a.crop(((i%t['columns'])*32,(i//t['columns'])*32,(i%t['columns'])*32+32,(i//t['columns'])*32+32))
for state in ['start','complete']:
 out=Image.new('RGBA',(1536,1024))
 for l in m['layers']:
  if l['type']!='tilelayer' or (not l.get('visible',True)and not(state=='complete'and l['name'].startswith('signal-'))):continue
  for j,gid in enumerate(l['data']):
   if gid:out.alpha_composite(cache[gid],((j%48)*32,(j//48)*32))
 out.convert('RGB').save(R/'review'/f'runtime-{state}.png')
 if state=='complete':out.crop((192,0,480,352)).resize((576,704)).convert('RGB').save(R/'review'/'beacon-closeup.png')
print('Rendered actual TMJ tiles; static proof, not game screenshots.')
