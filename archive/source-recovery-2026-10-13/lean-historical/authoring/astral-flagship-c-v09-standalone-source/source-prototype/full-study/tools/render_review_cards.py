from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from frozen_inputs import review_font
r=Path(__file__).resolve().parents[1];bold=lambda s:ImageFont.truetype(review_font(True),s);font=lambda s:ImageFont.truetype(review_font(),s)
for name,title in [('south','SOUTH ENTRANCE / FOYER OWNER'),('hall-east','HALL / GARDEN ENTRY / HALL OWNER'),('foyer-east','FOYER / TERRACE ENTRY / FOYER OWNER')]:
 ims=[Image.open(r/'review'/f'{name}-{state}-native.png')for state in ['outside','approach','inside']];w,h=ims[0].size
 card=Image.new('RGB',(w*3+64,h+132),'#123036');d=ImageDraw.Draw(card);d.text((16,12),title+' / NATIVE1:1',font=bold(23),fill='#f6dda6');d.text((16,47),'Original32px Greg; A interior + frozen B exterior. Independent shell owners; constant source collision. Static proof.',font=font(17),fill='#c9dcd8')
 for i,(im,label) in enumerate(zip(ims,['OUTSIDE','APPROACH / OWNER REVEALED','INSIDE / OWNER REVEALED'])):
  x=16+i*(w+16);d.text((x,79),label,font=bold(17),fill='#edc878');card.paste(im,(x,111))
 card.save(r/'review'/f'{name}-approach-sequence-native.png')
card=Image.new('RGB',(1472,1424),'#123036');d=ImageDraw.Draw(card);d.text((20,16),'C / INDEPENDENT SEMANTIC REVEAL STATES',font=bold(27),fill='#f6dda6');d.text((20,56),'Quarter-scale review panels. All source assets remain native and proportionate.',font=font(18),fill='#c9dcd8')
for i,(file,title) in enumerate([('full-outside-occupied-native.png','OUTSIDE / BOTH CLOSED'),('foyer-only-revealed-occupied-native.png','FOYER OPEN / HALL CLOSED'),('hall-only-revealed-occupied-native.png','HALL OPEN / FOYER ROOF ALSO HIDDEN'),('full-revealed-occupied-native.png','BOTH OPEN / EXACT A CORE + B EXTERIOR')]):
 x=20+(i%2)*728;y=124+(i//2)*646;d.text((x,y-30),title,font=bold(16),fill='#edc878');im=Image.open(r/'review'/file);card.paste(im.resize((704,608),Image.Resampling.LANCZOS),(x,y))
card.save(r/'review/semantic-reveal-states-overview.png')
print('Native B-integrated contact sheets and independent-state review saved')
