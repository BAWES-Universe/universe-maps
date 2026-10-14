from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];A=R/'source-assets'
src=Image.open(A/'command-environment-r3.png').convert('RGBA')
clean=Image.open(A/'console-clean-floor-master.png').convert('RGBA').resize(src.size)
out=src.copy();masks=[]
# Exact existing console pixels retained; generated clean plate used only under old silhouette.
for i,(cx,ty) in enumerate([(490,217),(768,217),(1048,217),(560,349),(768,349),(984,349)]):
 poly=[(cx-18,ty-1),(cx+18,ty-1),(cx+18,ty+7),(cx+43,ty+7),(cx+46,ty+12),(cx+46,ty+52),(cx+43,ty+55),(cx-43,ty+55),(cx-46,ty+52),(cx-46,ty+12),(cx-43,ty+7),(cx-18,ty+7)]
 mask=Image.new('L',src.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
 # Anti-aliased drop-shadow collar retained with the object, not a floor rectangle.
 mask=mask.filter(ImageFilter.GaussianBlur(1.2));masks.append(mask)
 clear=mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2));out=Image.composite(clean,out,clear)
for i,mask in enumerate(masks):
 piece=src.copy();piece.putalpha(mask);out.alpha_composite(piece,(0,15 if i<3 else 12))
out.save(A/'command-environment-clear.png')
json.dump({'consoleTranslation':{'upperRow':[0,15],'lowerRow':[0,12]},'chairTranslation':[0,15],'count':6,'method':'Original console RGBA silhouette retained; generated clean floor only at former six silhouettes'},open(A/'console-translation.json','w'),indent=2)
