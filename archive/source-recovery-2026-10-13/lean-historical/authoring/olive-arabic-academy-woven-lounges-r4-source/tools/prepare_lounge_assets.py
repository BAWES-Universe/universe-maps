from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];a=Image.open(R/'source-assets/warm-lounge-sprite-sheet.png').convert('RGBA')
# Bounds isolate each image-generated sprite. Alpha is preserved: the RGB backdrop is invisible.
boxes={'cedar-tea-table':(445,45,1090,434),'woven-camel':(119,451,443,704),'woven-oat':(600,451,927,704),'woven-clay':(1090,451,1418,704),'woven-oat-bottom':(118,730,448,985),'woven-camel-bottom':(600,730,930,985),'woven-ochre':(1090,730,1420,985)}
for name,box in boxes.items():
 im=a.crop(box);bounds=im.getchannel('A').point(lambda p:255 if p>10 else 0).getbbox();im=im.crop(bounds)
 im.thumbnail((84,50) if name=='cedar-tea-table' else (32,26),Image.Resampling.LANCZOS)
 im.save(R/'source-assets'/f'{name}-native.png')
