from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
S=Path(__file__).resolve().parent;R=S.parent;old=Image.open(S/'original-native.png').convert('RGBA');new=Image.open(S/'edit-native01.png').convert('RGBA')
mask=Image.new('L',old.size);d=ImageDraw.Draw(mask);d.rectangle((76,132,560,216),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(6));a=np.asarray(mask).copy();a[:120]=0;a[224:]=0;a[:,:76]=0;a[:,560:]=0
# Preserve original architecture and every reception furnishing pixel. Broad protected
# boxes intentionally include a little background; the generated repair only affects floor.
protected=[(0,0,76,384),(0,214,640,384),(426,0,560,158),(428,208,560,384),(176,182,256,224),(246,174,267,224),(264,182,340,224)]
for x,y,X,Y in protected:a[y:Y,x:X]=0
registered=Image.composite(new,old,Image.fromarray(a));registered.save(S/'registered-native.png')
base=Image.open(S/'office-base-before.png').convert('RGBA');before=np.asarray(base).copy();base.paste(registered,(544,512));base.save(R/'office-input/office-base.png')
after=np.asarray(base);changed=np.any(before!=after,axis=2);bounds=Image.fromarray(changed.astype('uint8')*255).getbbox()
for x,y,X,Y in protected:assert np.array_equal(np.asarray(old)[y:Y,x:X],np.asarray(registered)[y:Y,x:X])
report={'status':'Bounded generated floor seam repair; original object pixels restored','cropOfficeOrigin':[544,512],'changedPixels':int(changed.sum()),'changedOfficeBBox':list(bounds),'protectedRectanglesInCrop':protected,'objectsPreservedExact':True,'collisionSha256':hashlib.sha256((R/'office-input/collision-grid.json').read_bytes()).hexdigest(),'foregroundSha256':hashlib.sha256((R/'office-input/office-foreground.png').read_bytes()).hexdigest(),'projectionAndScaleUnchanged':True};(S/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
