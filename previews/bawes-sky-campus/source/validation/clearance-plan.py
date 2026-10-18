"""Native-pixel clearance drawing from current TMJ tiles; not a client screenshot."""
from pathlib import Path
from PIL import Image
import json,base64,html
r=Path(__file__).resolve().parents[2];m=json.loads((r/'campus.tmj').read_text());l=json.loads((r/'source/layout.json').read_text());x,y,w,h=l['office'];tiles={};im=Image.new('RGBA',(w,h))
sets=m['tilesets']
for layer in m['layers']:
 if layer['name'] not in ['office-floor','office-walls','office-furniture','office-chair-fronts']:continue
 for yy in range(y//16,(y+h)//16):
  for xx in range(x//16,(x+w)//16):
   gid=layer['data'][yy*m['width']+xx]
   if not gid:continue
   if gid not in tiles:
    ts=next(t for t in reversed(sets) if t['firstgid']<=gid);a=Image.open(r/ts['image']).convert('RGBA');i=gid-ts['firstgid'];tx=ts.get('margin',0)+(i%ts['columns'])*(16+ts.get('spacing',0));ty=ts.get('margin',0)+(i//ts['columns'])*(16+ts.get('spacing',0));tiles[gid]=a.crop((tx,ty,tx+16,ty+16))
   im.alpha_composite(tiles[gid],(xx*16-x,yy*16-y))
p=r/'review/interior-native-plan.png';im.save(p)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -48 {w+32} {h+96}"><rect x="-16" y="-48" width="{w+32}" height="{h+96}" fill="#101b29"/><text x="0" y="-18" fill="white" font-size="22">Native-pixel furniture bounds — hover each outline for measured clearance</text>',f'<image width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"/>',f'<rect width="{w}" height="{h}" fill="none" stroke="#35e288" stroke-width="4"/>']
audit=json.loads((r/'review/footprint-audit.json').read_text())
for o in audit['furniture']:
 title=html.escape(f"{o['object']} {o['kind']} — wall clearance {o['clearanceToBuildingPixels']}");color='#ffbe55' if o['kind']=='sofa' else '#74cfff'
 svg.append(f'<rect x="{o["x"]-x}" y="{o["y"]-y}" width="{o["width"]}" height="{o["height"]}" fill="transparent" stroke="{color}" stroke-width="1.5"><title>{title}</title></rect>')
svg.append(f'<text x="0" y="{h+32}" fill="white" font-size="18">Green: actual interior boundary. Blue: every furniture extent. Amber: sofas, with 64px minimum front clearance. Woka scale 1.</text></svg>')
(r/'review/furniture-clearances.svg').write_text(''.join(svg))
