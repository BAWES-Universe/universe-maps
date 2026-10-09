from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];D=json.loads((R/'fixture-plan.json').read_text());im=Image.new('RGB',(512,384),'#eff4f5');d=ImageDraw.Draw(im)
for x in range(0,513,32):d.line((x,0,x,384),fill='#dae0e2')
for y in range(0,385,32):d.line((0,y,512,y),fill='#dae0e2')
for lane in D['walkable_lanes']:
 r=lane['rect'];d.rectangle((r['x'],r['y'],r['x']+r['width']-1,r['y']+r['height']-1),fill='#d6eee3')
for s in D['workstations']:
 r=s['desk']['planned_visible_bounds'];d.rectangle((r['x'],r['y'],r['x']+63,r['y']+63),fill='#a78d69',outline='#443e38')
 d.rectangle((r['x'],r['y'],r['x']+63,r['y']+47),fill='#d3be9a',outline='#706855')
 c=s['chair']['planned_visible_bounds'];d.rounded_rectangle((c['x'],c['y'],c['x']+29,c['y']+35),radius=5,fill='#629f9f',outline='#275d65')
 b=s['chair']['back_above_player_bounds'];d.rounded_rectangle((b['x'],b['y'],b['x']+27,b['y']+23),radius=6,fill='#317984',outline='#153d49')
 d.text((r['x'],r['y']-15),'64 x 64 DESK',fill='#1b3640')
 d.line((s['occupant']['center'][0],s['occupant']['center'][1]+32,s['approach_center'][0],s['approach_center'][1]),fill='#4c8375',width=2)
d.text((12,10),'NATIVE GEOMETRY GUIDE 512 x 384',fill='#123140');d.text((12,27),'Retain exact furniture positions; no labels/grid in artwork.',fill='#123140');d.text((162,296),'64px clear shared aisle',fill='#205347')
im.save(R/'docs/geometry-guide.png');im.resize((1024,768),Image.Resampling.NEAREST).save(R/'art-source/geometry-guide-2x.png')
