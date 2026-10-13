from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];V3=Path('/workspace/shared/grand-auditorium-03-foyer-terrace');V5=Path('/workspace/shared/grand-auditorium-05-roofless-garden');A=R/'assets';Q=R/'review'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
load=lambda p:Image.open(p).convert('RGBA')
greg=load(V5/'assets/greg-reference.png'); actor=greg.crop((32,0,64,32));actor.save(A/'greg-south-32.png')
# Empty existing foyer floor crop is native and unresized; only benchmark cutout.
floor=load(V5/'assets/foyer-base.png').crop((864,1344,1216,1584))
chair=load(V3/'assets/lounge-chair-south.png');table=load(V3/'assets/low-lounge-table.png')
oldleft=load(V3/'assets/bistro-stool-left-native.png');oldright=load(V3/'assets/bistro-stool-right-native.png');oldtable=load(V3/'assets/bistro-table-native.png')
for name in ['lounge-chair-south','low-lounge-table','bistro-stool-left-native','bistro-stool-right-native','bistro-table-native']:
 shutil.copy2(V3/f'assets/{name}.png',A/f'{name}.png')
def compose(specs,anchors):
 im=floor.copy();fg=Image.new('RGBA',im.size)
 for asset,x,y,cut in specs:
  im.alpha_composite(asset.crop((0,0,asset.width,cut)),(x,y));fg.alpha_composite(asset.crop((0,cut,asset.width,asset.height)),(x,y+cut))
 for ax,ay in anchors:im.alpha_composite(actor,(ax-16,ay-16))
 im.alpha_composite(fg);return im
# Identical avatar anchors for the direct occupied comparison.
anchors=[(116,118),(172,118)]
before=compose([(oldleft,101,88,46),(oldright,158,88,46),(oldtable,125,88,46)],anchors)
after=compose([(chair,92,90,39),(chair,148,90,39),(table,260,108,28)],anchors)
before.save(Q/'seating-before-occupied-native.png');after.save(Q/'seating-after-occupied-native.png')
board=Image.new('RGB',(752,340),'#112e34');d=ImageDraw.Draw(board)
d.text((16,12),'CASUAL PAIR / NATIVE 1:1 OCCUPIED BENCHMARK',font=bold,fill='#f3d69b')
d.text((16,44),'BEFORE: narrow stools + tall central table',font=font,fill='white');d.text((392,44),'AFTER: accepted chairs + low table to side',font=font,fill='white')
board.paste(before,(16,70));board.paste(after,(392,70));d.text((16,316),'32 px Greg; 56 px anchor spacing in both. Assets shown at native size, unchanged.',font=font,fill='#bfd0c9');board.save(Q/'seating-benchmark-native-1x.png')
large=board.resize((1504,680),Image.Resampling.NEAREST);ld=ImageDraw.Draw(large);ld.rectangle((0,0,1503,43),fill='#112e34');ld.text((32,12),'2x NEAREST-NEIGHBOR INSPECTION ONLY | art scale stays native in the benchmark',font=bold,fill='#f3d69b');large.save(Q/'seating-benchmark-2x-nearest.png')
