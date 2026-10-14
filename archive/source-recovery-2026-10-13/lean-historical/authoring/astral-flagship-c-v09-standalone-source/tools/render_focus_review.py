"""Source-calculated viewport illustration; not a browser screenshot."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];proof=json.loads((R/'validation/focus/focus-results.json').read_text());source=Image.open(R/'review/building-c-hall-occupied-native.png').convert('RGB')
font=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold'if b else'')+'.ttf',n)
shots={}
for row in proof['fresh']:
 if row['dpr']!=1:continue
 v=row['worldView'];w,h=row['viewport']['width'],row['viewport']['height'];im=source.transform((w,h),Image.Transform.EXTENT,(v['x'],v['y'],v['x']+v['width'],v['y']+v['height']),resample=Image.Resampling.NEAREST,fillcolor='#102c32');shots[row['label']]=im;im.save(R/'review'/f'building-c-focus-{row["label"]}-source-calculated.png')
card=Image.new('RGB',(1886,1080),'#123039');d=ImageDraw.Draw(card);d.text((20,18),'C / WHOLE-HALL FOCUS • SOURCE-CALCULATED VIEWPORTS',font=font(26,True),fill='#f3d398');d.text((20,57),'Initial entry fit; ordinary exterior follow. These are source-math illustrations, not browser captures.',font=font(20),fill='#d4e3dc');card.paste(shots['desktop'],(20,112));card.paste(shots['portrait'],(1480,112));d.text((20,1027),'1440×900 desktop • stage, audience and exits fit',font=font(20),fill='#d4e3dc');d.text((1480,984),'390×844 portrait',font=font(19),fill='#d4e3dc');d.text((1480,1015),'Avatar ≈7 CSS px at hall fit',font=font(17),fill='#d4e3dc');d.text((1480,1041),'Manual zoom remains available',font=font(17),fill='#d4e3dc');card.save(R/'review/building-c-focus-source-calculated-sheet.png')
print('Source-calculated hall focus views rendered')
