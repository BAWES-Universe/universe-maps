from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];P=R/'celestial-transit-garden-calm-draft'
# These runtime-base/above products are independently checked byte-exact against decoded atlases by final_proofs.py.
base=Image.open(P/'source/runtime-base.png').convert('RGBA');above=Image.open(P/'source/runtime-above.png').convert('RGBA');sheet=Image.open(R/'source/greg-reference.png').convert('RGBA')
j=json.load(open(P/'validation/conifer-detour-native.json'));rows=[r for r in j['rows']if not r['id'].endswith('-approach')]
card=Image.new('RGB',(1408,380),'#131a2b');d=ImageDraw.Draw(card);F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14);d.text((16,14),'Native lower-loop crossings · both directions · 32 px frames · foliage-only foreground',font=FB,fill='#ede9dc');proof=[]
for k,r in enumerate(rows):
 west='west' in r['id'];cx=848 if west else 1200;cy=1024;positions=r['positions'];ii=min(range(len(positions)),key=lambda i:(positions[i][0]-cx)**2+(positions[i][1]-cy)**2);x,y=map(round,positions[ii]);prev=positions[max(0,ii-1)];dx=x-prev[0];dy=y-prev[1];frame=(7 if dx>0 else 4)if abs(dx)>abs(dy)else(1 if dy>0 else 10);sprite=sheet.crop((frame%3*32,frame//3*32,frame%3*32+32,frame//3*32+32));out=base.copy();out.alpha_composite(sprite,(x-16,y-16));out.alpha_composite(above);box=(cx-160,cy-112,cx+160,cy+144);card.paste(out.crop(box),(k*352+16,52));d.text((k*352+16,320),r['id'],font=FB,fill='#ede9dc');d.text((k*352+16,344),f'Actual native frame {ii}: ({x}, {y})',font=F,fill='#b9c4d7');proof.append(dict(route=r['id'],frame=ii,actualPosition=positions[ii],roundedRendering=[x,y],minRouteY=r['minY'],passNative=r['pass']))
card.save(P/'review/lower-loop-native-crossings.png');(P/'validation/lower-loop-crossing-frames.json').write_text(json.dumps(dict(scope='Frames sampled from unchanged source-native movement, foreground re-applied after native sprite. No synthetic teleport positions.',frames=proof,allPass=all(p['passNative']and p['minRouteY']>=992 for p in proof)),indent=2))
