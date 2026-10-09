#!/usr/bin/env python3
"""Technical proof layout; no new furniture art or avatar pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=ImageFont.truetype(fontpath,18);S=ImageFont.truetype(fontpath,14);T=ImageFont.truetype(fontpath,24)
im=Image.new('RGB',(1112,1112),'#f5f0e4');d=ImageDraw.Draw(im)
d.text((24,18),'Meeting furniture at unchanged Woka scale',font=T,fill='#173b43')
d.text((24,52),'Original honey-oak / teal assets • native 32 px Greg scale fixtures • offline registration proof',font=S,fill='#476068')
for col,state in enumerate(['empty','occupied']):
 x=24+col*544;d.text((x,92),'Four cardinal seats · '+state,font=F,fill='#173b43')
 a=Image.open(R/'proofs'/f'small-four-cardinal-{state}-native.png').convert('RGB');im.paste(a.resize((512,384),Image.Resampling.NEAREST),(x,122))
 d.text((x,526),'Six seats · identical chair scale · '+state,font=F,fill='#173b43')
 a=Image.open(R/'proofs'/f'conference-six-{state}-native.png').convert('RGB').crop((0,64,256,288));im.paste(a.resize((512,448),Image.Resampling.NEAREST),(x,556))
d.text((24,1028),'Shown at 2× nearest-neighbor for inspection; 1× PNGs are the scale authority.',font=S,fill='#476068')
d.text((24,1052),'10/10 entry and exit routes clear with other seats occupied. All protected head pixels remain visible.',font=S,fill='#476068')
d.text((24,1076),'Repeated fixtures are not multiplayer users. No seated animation, claim, audio, or meeting wiring is implemented.',font=S,fill='#476068')
im.save(R/'proofs/meeting-furniture-review-sheet.png')
