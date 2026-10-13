from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json
R=Path(__file__).resolve().parents[1];S=R/'market-study'
old=Image.open(S/'market-shore-native.png').convert('RGBA');new=Image.open(S/'shore-edit-native01.png').convert('RGBA')
# Generated paving is used only in the circulation strip. Existing facade and
# right-hand water pixels stay in their separate source modules unchanged.
mask=Image.new('L',old.size);d=ImageDraw.Draw(mask)
d.polygon([(112,0),(300,0),(320,120),(320,416),(184,416),(152,344),(112,288)],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(4));a=np.asarray(mask).copy();a[:,0:112]=0;a[:,320:]=0
# The16px lower receiver is actual visible paving in the new local source.
patch=new.copy();patch.putalpha(Image.fromarray(a));patch.save(S/'shore-paving-patch09.png')
paths=[[[128,0],[192,0],[200,80],[224,144],[256,208],[288,272],[310,352],[316,416],[224,416],[212,344],[192,280],[160,224],[136,176],[128,112]]]
meta={'worldOrigin':[2448,1872],'nativeSize':[384,448],'gardenTranslation':[-16,-16],'walkablePolygons':paths,'notes':['Only visible new paving is opened; final collision must be sampled against composed pixels.','Existing market facade and river remain preserved source pixels outside the edit mask.','Bottom16px paving connects shifted garden to unchanged market forecourt.'],'status':'assembly proposal, exact native route validation pending'};(S/'shore-patch09.json').write_text(json.dumps(meta,indent=2)+'\n')
