from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil,json,hashlib
R=Path(__file__).resolve().parents[1];S=Path('/workspace/shared/grand-auditorium-03-foyer-terrace/assets');A=R/'assets';Q=R/'review'
for n in ['lounge-chair-north','lounge-chair-south','lounge-chair-east','lounge-chair-west','rug-wide','wall-horizontal','wall-left','wall-right','sandstone-tile','wood-deck-tile','low-lounge-table','planter-low','coffee-counter-native']:
 shutil.copy2(S/f'{n}.png',A/f'{n}.png')
load=lambda n:Image.open(A/f'{n}.png').convert('RGBA')
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
bold=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n)
W,H=832,544;base=Image.new('RGBA',(W,H));floor=load('sandstone-tile')
for y in range(0,H,64):
 for x in range(0,W,64):base.alpha_composite(floor,(x,y))
# Left suite, broad threshold to its south, open circulation to the east.
base.alpha_composite(load('rug-wide'),(64,96));base.alpha_composite(load('wall-horizontal'),(24,8));base.alpha_composite(load('wall-horizontal'),(248,8))
for y in [56,232]:base.alpha_composite(load('wall-left'),(16,y))
base.alpha_composite(load('planter-low'),(512,64))
# Competition desk is new source art, native192px, no scores or integration.
base.alpha_composite(load('esports-desk-native'),(144,128));above=Image.new('RGBA',(W,H))
# Native north-facing chairs. Each anchor is source placement top+16; lower back starts+25.
chair=load('lounge-chair-north');actors=[]
for x in [176,240,304]:
 y=236;base.alpha_composite(chair,(x-24,y-16));above.alpha_composite(chair.crop((0,25,48,44)),(x-24,y+9));actors.append((x,y,'north'))
# Spectator bank demonstration to the right of the clear ring passage.
for y in [272,368]:
 for x in [576,640,704]:
  base.alpha_composite(chair,(x-24,y-16));above.alpha_composite(chair.crop((0,25,48,44)),(x-24,y+9));actors.append((x,y,'north'))
base.alpha_composite(load('low-lounge-table'),(672,96))
# Layered native threshold/bar brass inlay, not debugging rectangles.
d=ImageDraw.Draw(base)
d.line((72,356,408,356),fill='#826332',width=4);d.line((72,352,408,352),fill='#eed18d',width=2)
d.rounded_rectangle((162,63,318,82),radius=3,fill='#0b363c',outline='#d7ac5c',width=2);d.text((177,65),'TEAM WEST',font=bold(11),fill='#f4d18b')
d.rounded_rectangle((556,206,724,227),radius=3,fill='#0b363c',outline='#d7ac5c',width=2);d.text((571,210),'SPECTATOR COURT',font=bold(10),fill='#f4d18b')
# Two moving guests show real 32px scale in the loop and suite threshold.
actors += [(464,288,'south'),(240,386,'north')]
greg=load('greg-reference');frames={n:greg.crop((i%3*32,i//3*32,i%3*32+32,i//3*32+32))for n,i in [('north',10),('south',1),('west',4),('east',7)]}
occupied=base.copy()
for x,y,n in actors:occupied.alpha_composite(frames[n],(x-16,y-16))
occupied.alpha_composite(above);base.save(Q/'bounded-source-base-native.png');above.save(Q/'bounded-source-above-native.png');occupied.save(Q/'bounded-occupied-native32.png')
board=Image.new('RGB',(864,654),'#10292f');d=ImageDraw.Draw(board);d.text((16,14),'ESPORTS / NATIVE32 OCCUPIED ART SAMPLE',font=bold(18),fill='#eacb8e');d.text((16,42),'New three-station desk + original native chairs. Greg v3 remains exactly 32 px.',font=font(13),fill='#d6ded6');board.paste(occupied,(16,74));d.text((16,628),'Bounded source composition, 1:1 pixels. No runtime, media or live-game claim.',font=font(13),fill='#d6ded6');board.save(Q/'REVIEW-FIRST-native32.png')
proof=occupied.copy();d=ImageDraw.Draw(proof,'RGBA');d.rectangle((424,64,519,511),fill=(75,206,190,40),outline=(71,229,210,230));d.text((435,451),'96 px',font=bold(12),fill='white')
for x,y,n in actors:d.rectangle((x-8,y,x+7,y+15),outline=(255,230,131,255));d.rectangle((x-16,y-16,x+15,y+15),outline=(255,255,255,210))
proof.save(Q/'bounded-native32-geometry-overlay.png')
prov={'originalProjectAssets':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in A.glob('*.png')if p.name not in ['esports-desk-native.png']],'newAsset':{'generator':'built-in imagegen','master':'source/esports-desk-generated-master.png','prompt':'source/imagegen-prompt-esports-desk.txt','native':'assets/esports-desk-native.png','nativeSize':list(load('esports-desk-native').size),'operation':'Alpha crop and uniform aspect-preserving reduction; no anisotropic stretch.'},'greg':'Project-authored Greg Gulf-outfit v3, unchanged, QA only, not runtime.'}
(R/'PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n')
