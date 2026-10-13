from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'source-assets'
old=Image.open(A/'chair-north32-native.png').convert('RGBA');master=Image.open(A/'chair-lowback-master.png').convert('RGBA');box=master.getchannel('A').point(lambda v:255 if v>32 else 0).getbbox();src=master.crop(box)
# New lumbar shell only. Original wheel/post pixels and baseline are retained.
shell=src.crop((0,0,src.width,round(src.height*.53))).resize((32,17),Image.Resampling.LANCZOS)
full=Image.new('RGBA',old.size);full.paste(old.crop((0,21,32,old.height)),(0,21));full.alpha_composite(shell,(0,8))
fg=Image.new('RGBA',full.size);fg.paste(full.crop((4,14,28,24)),(4,14));below=full.copy();below.paste((0,0,0,0),(4,14,28,24))
assert Image.alpha_composite(below,fg).tobytes()==full.tobytes()
for name,im in [('chair-lowback-full-native',full),('chair-lowback-below-native',below),('chair-lowback-rail-native',fg)]:im.save(A/(name+'.png'))
full.resize((320,370),Image.Resampling.NEAREST).save(R/'chair-lowback-10x.png')
