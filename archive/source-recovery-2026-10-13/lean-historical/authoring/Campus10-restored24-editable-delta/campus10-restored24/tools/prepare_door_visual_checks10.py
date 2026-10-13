from pathlib import Path
from PIL import Image
import json,numpy as np,sys
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'validation/door-check'; F=ROOT; clears=[]
ls={n:Image.open(ROOT/f'layers/campus-{n}.png').convert('RGBA')for n in ['base','foreground','glass','shade']}
above=Image.new('RGBA',ls['base'].size)
for n in ['foreground','glass','shade']:above.alpha_composite(ls[n])
above.save(R/'regression/layers/campus-above.png');flat=ls['base'].copy();flat.alpha_composite(above)
for name,box in [('classroom',(512,1440,704,1632)),('stage',(512,2048,736,2208)),('office-main',(1152,912,1376,1056)),('gallery',(1760,912,1984,1056)),('internal',(1664,688,1872,864))]:flat.crop(box).save(R/(name+'-integrated-native.png'))
sheet=np.array(Image.open(F/'validation/greg.png').convert('RGBA'));a=np.array(above)[:,:,3];OPAQUE=a>=224;TRANS=(a>0)&(a<224)
boxes={'classroom':[520,1440,184,192],'stage':[520,2048,208,160],'office-gallery-internal':[1648,704,224,128],'office-main':[1184,912,160,176],'gallery-public':[1792,912,128,176],'conference-control':[1856,640,112,160]}
V=R/'visual-input';V.mkdir(exist_ok=True);meta=[]
for name,(x,y,w,h)in boxes.items():
 allcounts=[]
 for direction,frames in enumerate([[0,1,2],[3,4,5],[6,7,8],[9,10,11]]):
  full=np.zeros((32,32),bool)
  for frame in frames:full|=sheet[(frame//3)*32:(frame//3+1)*32,(frame%3)*32:(frame%3+1)*32,3]>0
  head=full.copy();head[14:]=False
  for alpha in [OPAQUE,TRANS]:
   crop=alpha[y-16:y+h+16,x-16:x+w+16]
   for mask in [head,full]:
    count=np.zeros((h,w),np.uint16)
    for sy,sx in np.argwhere(mask):count+=crop[sy:sy+h,sx:sx+w]
    allcounts.append(count)
 data=np.stack(allcounts).astype('<u2');data.tofile(V/(name+'.bin'));meta.append({'id':name,'box':[x,y,w,h],'file':str(V/(name+'.bin')),'shape':list(data.shape)})
(R/'visual-input/manifest.json').write_text(json.dumps({'metricOrderPerDirection':['opaqueHead','opaqueWholeAvatar','translucentHead','translucentWholeAvatar'],'directions':['down','left','right','up'],'spritePolicy':'Conservative union of three native32 animation frames in movement direction; original alpha silhouettes, head first14px. Both floor and ceil integer placements sampled for subpixel position.','opaqueThreshold':224,'aboveSources':sys.argv[1] if len(sys.argv)>1 else 'Isolated corrected source layers with exterior semantic floor/object ownership masks, before runtime compile.','rois':meta,'exteriorClearMasks':clears},indent=2))
print(json.dumps({'rois':len(meta),'lookupBytes':sum((V/(m['id']+'.bin')).stat().st_size for m in meta),'clearMasks':clears}))
