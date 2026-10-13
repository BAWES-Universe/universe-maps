"""Bounded source-only native doorway candidate. Full concept remains untouched."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageFont
import numpy as np,json,hashlib
from scipy.ndimage import gaussian_filter
def font_load(name,size):
 try:return ImageFont.truetype(name,size)
 except OSError:return ImageFont.load_default()
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
def poisson(arr,box,donor):
 x0,y0,x1,y1=box;h=y1-y0;w=x1-x0;n=h*w
 m=diags([np.full(n,4.),np.full(n-1,-1.),np.full(n-1,-1.),np.full(n-w,-1.),np.full(n-w,-1.)],[0,-1,1,-w,w],format='lil')
 for y in range(1,h):m[y*w,y*w-1]=0;m[y*w-1,y*w]=0
 b=np.zeros((h,w,3))
 for y in range(h):
  for x in range(w):
   for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
    nx=x+dx;ny=y+dy
    if 0<=nx<w and 0<=ny<h:b[y,x]+=donor[y,x]-donor[ny,nx]
    else:b[y,x]+=arr[y0+ny,x0+nx]
 a=spsolve(m.tocsr(),b.reshape(n,3)).reshape(h,w,3);arr[y0:y1,x0:x1]=np.clip(a,0,255)
R=Path(__file__).resolve().parents[1];src=Image.open(R/'previews/instructor-facing-concept.png').convert('RGB').resize((768,512),Image.Resampling.LANCZOS);ar=np.asarray(src).astype(float);out=ar.copy()
# Keep source plant shapes. Moving doorway-side foliage aside makes one clear
# landing in each nook, rather than allowing pathfinding through a visible plant.
plants=[dict(box=(199,349,259,393),shift=(-55,9),side='west'),dict(box=(503,349,568,393),shift=(55,9),side='east')]
for p in plants:
 x0,y0,x1,y1=p['box'];crop=src.crop(p['box']).convert('RGBA');a=np.asarray(crop).copy();rgb=a[:,:,:3].astype(float)
 # Select original green/gold leafy silhouette against brown wood and gray stone.
 mask=(rgb[:,:,1]>rgb[:,:,0]*.77)&(rgb[:,:,1]>rgb[:,:,2]*1.25)&((rgb[:,:,1]-rgb[:,:,2])>18)
 # Any isolated holes remain transparent, retaining source-leaf edges.
 a[:,:,3]=mask.astype('uint8')*255;p['sprite']=Image.fromarray(a)
 # Fill only the cleared walkway-facing foliage region from the opposite nook
 # floor, preserving the lower wall below y383.
 donorx=139 if p['side']=='west' else 609
 donor=ar[y0:384,donorx:donorx+x1-x0].copy();poisson(out,(x0,y0,x1,384),donor)
# Clear one 32px-tall doorway + landing. Adjacent hall is source floor donor.
for box,dx in [((224,320,294,352),96),((474,320,544,352),-96)]:
 x0,y0,x1,y1=box;patch=ar[y0:y1,350:350+x1-x0].copy();poisson(out,box,patch)
im=Image.fromarray(np.clip(out,0,255).astype('uint8')).convert('RGBA')
# Retain the original stone-foot and cap graphics, moving them to the new
# opening edges rather than leaving freshly cut flat pillar ends.
for b,xy in [((224,325,282,340),(224,304)),((488,325,543,340),(488,304)),((264,343,291,365),(264,352)),((474,343,502,365),(474,352))]:
 im.alpha_composite(src.crop(b).convert('RGBA'),xy)
for p in plants:
 x0,y0,x1,y1=p['box'];dx,dy=p['shift'];im.alpha_composite(p['sprite'],(x0+dx,y0+dy))
im.save(R/'previews/runtime-doorway-candidate.png')
card=Image.new('RGB',(1248,528),'#182620');d=ImageDraw.Draw(card);font=font_load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
d.text((18,14),'BEFORE: retained half-scale nooks',font=font,fill='#ead4a3');d.text((646,14),'R2: source-only native32 door repair',font=font,fill='#ead4a3')
for a,x in [(src,0),(im,624)]:
 card.paste(a.crop((104,282,664,420)).resize((560,138)),(x+32,48));card.paste(a.crop((210,301,306,386)).resize((288,255)),(x+12,213));card.paste(a.crop((467,301,563,386)).resize((288,255)),(x+324,213))
d.text((18,494),'Approved runtime doorway repair. Retained original and six-mat orientation concept stay unchanged.',font=font,fill='white');card.save(R/'previews/runtime-doorway-before-after.png')

# Exact immutable-source comparison for this bounded runtime repair.
a=np.asarray(src);b=np.asarray(im.convert('RGB'));changed=np.any(a!=b,axis=2);allowed=np.zeros(changed.shape,bool);boxes=[[144,304,294,403],[474,304,624,403]]
for x0,y0,x1,y1 in boxes:allowed[y0:y1,x0:x1]=1
assert not (changed&~allowed).any()
proof=dict(scope='Native doorway and landing repair only; original and full-resolution orientation concept are unchanged',nativeResolution=[768,512],changedPixels=int(changed.sum()),changedPercent=round(float(changed.mean()*100),4),allowedPatchBoundsExclusive=boxes,changedPixelsOutsidePatches=int((changed&~allowed).sum()),sourceMatAndMedallionRegionExact=bool(np.array_equal(a[128:269],b[128:269])),doorClearFloorBand=[320,352],jambFootShiftY=-21,opposingStoneCapShiftY=9,doorwayFoliageShift={'west':[-55,9],'east':[55,9]},method='Original stone feet and caps moved; original foliage moved upright; same-Y source wood gradients with Poisson boundary lighting; no generation',nativeCandidateSha256=hashlib.sha256((R/'previews/runtime-doorway-candidate.png').read_bytes()).hexdigest())
(R/'previews/RUNTIME-DOORWAY-PATCH.json').write_text(json.dumps(proof,indent=2)+'\n')
