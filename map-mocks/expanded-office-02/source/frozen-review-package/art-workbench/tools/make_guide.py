from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
im=Image.new('RGBA',(160,128));d=ImageDraw.Draw(im)
# Geometry diagram only. Native table origin is16,16, visible128x96.
d.rounded_rectangle((16,16,143,109),2,fill='#99632f')
d.rectangle((19,108,23,111),fill='#99632f');d.rectangle((136,108,140,111),fill='#99632f')
d.rounded_rectangle((16,16,143,103),2,fill='#cb9147')
for cx in [48,112]:
 # North user's keyboard and small mouse, followed by correctly oriented monitor rear and forward stand.
 d.rounded_rectangle((cx-12,24,cx+11,30),1,fill='#215b65')
 d.rounded_rectangle((cx+16,24,cx+20,30),1,fill='#215b65')
 d.rectangle((cx-5,39,cx+5,43),fill='#ad884a')
 d.rounded_rectangle((cx-14,44,cx+13,59),1,fill='#174550')
 # South user's screen and its near stand, then keyboard and mouse.
 d.rounded_rectangle((cx-14,65,cx+13,81),1,fill='#174550')
 d.rectangle((cx-11,68,cx+10,77),fill='#207f8d')
 d.rectangle((cx-5,82,cx+5,85),fill='#ad884a')
 d.rounded_rectangle((cx-12,91,cx+11,98),1,fill='#215b65')
 d.rounded_rectangle((cx+16,91,cx+20,98),1,fill='#215b65')
im.resize((2560,2048),Image.Resampling.NEAREST).save(R/'guides/workbench-geometry.png')
im.save(R/'guides/workbench-geometry-native.png')
