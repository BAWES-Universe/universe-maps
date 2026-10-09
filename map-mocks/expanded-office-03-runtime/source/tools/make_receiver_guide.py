from PIL import Image,ImageDraw
from pathlib import Path
R=Path(__file__).resolve().parents[1];im=Image.new('RGB',(1024,704),'#e8e2d5');d=ImageDraw.Draw(im)
d.rectangle((0,0,1023,31),fill='#a9bfc4');d.rectangle((0,32,31,703),fill='#a9bfc4')
for px in [64,544]:
 # Low built-in U, physical fixtures around the occupied bench. Gray center is reserved floor only.
 d.rectangle((px+32,96,px+319,143),fill='#c29c6d')
 d.rectangle((px+32,144,px+63,335),fill='#c29c6d')
 d.rectangle((px+288,144,px+319,335),fill='#c29c6d')
 d.rectangle((px+112,208,px+239,303),fill='#a8abb5')
 for xx in [px+144,px+208]:
  d.ellipse((xx-16,176,xx+16,208),fill='#ffffff',outline='#195967')
  d.ellipse((xx-16,288,xx+16,320),fill='#ffffff',outline='#195967')
 # Open front and protected surrounding path.
 d.line((px+176,416,px+176,352),fill='#1b887c',width=5)
d.rectangle((32,448,1023,703),fill='#d7e4df')
d.text((40,464),'CLEAR SHARED AISLE — floor/light only, no solid objects',fill='#124c52')
d.text((40,40),'GEOMETRY GUIDE: brown = low built-ins; gray = reserved furniture footprint; white = avatar positions',fill='#273d45')
im.save(R/'art-source/receiver-panel-control.png')
