from PIL import Image,ImageDraw
from pathlib import Path
p=Path(__file__).parent
im=Image.new('RGB',(1024,1024),'#244332'); d=ImageDraw.Draw(im)
# Final native receiver agreed with campus lead. World origin (2176,1920).
d.polygon([(835,0),(860,128),(884,260),(900,448),(876,608),(850,768),(875,1024),(1024,1024),(1024,0)],fill='#296f72')
d.line([(834,0),(859,128),(883,260),(899,448),(875,608),(849,768),(874,1024)],fill='#a59b7b',width=24)
d.line([(0,288),(400,288),(688,288),(704,800)],fill='#b99c70',width=96,joint='curve')
d.line([(400,288),(320,528),(400,740),(644,740)],fill='#b99c70',width=96,joint='curve')
d.ellipse((284,316,708,740),fill='#b99c70',outline='#d7bd8f',width=10)
for r in [(416,384,576,416),(352,480,384,608),(608,480,640,608),(416,656,576,688)]:d.rectangle(r,fill='#6b513b')
d.ellipse((448,486,544,570),fill='#8f856a',outline='#403828',width=10)
d.ellipse((472,508,520,552),fill='#e39b4a')
for x,y,r in [(210,80,95),(500,75,85),(160,540,70),(180,820,100),(445,940,125),(738,930,65),(754,145,55)]:d.ellipse((x-r,y-r,x+r,y+r),fill='#356d43')
for x,y in [(240,237),(750,350),(278,623),(768,755)]:d.ellipse((x-12,y-12,x+12,y+12),fill='#ffcc76')
im.save(p/'garden-layout-guide.png')
