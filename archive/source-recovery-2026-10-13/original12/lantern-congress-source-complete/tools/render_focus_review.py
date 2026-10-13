from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];proof=json.loads((R/'validation/focus/focus-results.json').read_text());src=Image.open(R/'review/occupied-native.png').convert('RGB');font=lambda n,b=False:ImageFont.truetype(str(R/'assets/fonts'/('DejaVuSans-Bold.ttf'if b else'DejaVuSans.ttf')),n)
card=Image.new('RGB',(1226,1014),'#172d27');d=ImageDraw.Draw(card);d.text((16,16),'THREE-HALL FOCUS / SOURCE-CALCULATED PORTRAIT ENTRY',font=font(20,True),fill='#e6d5b4');d.text((16,49),'390 ×844 initial viewport. This illustrates native camera math, not a browser/device screenshot.',font=font(14),fill='#ccd8c9')
for i,r in enumerate(proof['rooms']):
 row=next(x for x in r['fresh']if x['label']=='portrait'and x['dpr']==1);v=row['worldView'];im=src.transform((390,844),Image.Transform.EXTENT,(v['x'],v['y'],v['x']+v['width'],v['y']+v['height']),resample=Image.Resampling.NEAREST,fillcolor='#233c32');x=16+i*402;d.text((x,83),r['id'].upper(),font=font(17,True),fill='#e6d5b4');card.paste(im,(x,112))
d.text((16,975),'Full stage/speakers fit. Avatars≈9.4CSS px. Manual zoom available; focused rotation remains a known limit.',font=font(14),fill='#ccd8c9');card.save(R/'review/focus-source-calculated.png')
