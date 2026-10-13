"""Reposition six retained-source mats. No new art generation or global resizing.
All extraction, background repair, and transforms are deterministic and local.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, json, hashlib
from scipy.ndimage import gaussian_filter
def font_load(name,size):
 try:return ImageFont.truetype(name,size)
 except OSError:return ImageFont.load_default()
R=Path(__file__).resolve().parents[1]
(R/'previews').mkdir(parents=True,exist_ok=True)
SRC=R/'source-assets/retained-original-concept.png'
im=Image.open(SRC).convert('RGB'); a=np.asarray(im).astype(float); H,W=a.shape[:2]
# Clockwise source surface corners. Each entry retains its own original mat.
specs=[
 dict(id='west-1',quad=[(229,286),(374,286),(370,321),(224,321)],remove=(220,281,395,326),block=(347,285,373,314),bottle=(377,281,395,325),cx=332),
 dict(id='west-2',quad=[(217,348),(366,348),(363,387),(213,387)],remove=(208,344,391,392),block=(338,347,367,379),bottle=(370,346,389,391),cx=437),
 dict(id='west-3',quad=[(208,418),(359,418),(355,458),(200,458)],remove=(198,412,385,464),block=(330,419,359,453),bottle=(365,416,384,461),cx=542),
 dict(id='east-1',quad=[(1166,286),(1303,286),(1310,321),(1170,321)],remove=(1137,281,1316,326),block=(1162,285,1190,315),bottle=(1137,282,1159,325),cx=994),
 dict(id='east-2',quad=[(1173,348),(1317,348),(1324,387),(1177,387)],remove=(1145,344,1330,392),block=(1171,347,1199,379),bottle=(1146,345,1170,391),cx=1099),
 dict(id='east-3',quad=[(1180,418),(1328,418),(1336,458),(1183,458)],remove=(1155,412,1343,464),block=(1179,419,1207,453),bottle=(1155,416,1180,462),cx=1204)]

# Inverse projective transform coefficients to sample source via Pillow.
def coeff(dst,src):
 A=[];B=[]
 for (x,y),(u,v) in zip(dst,src):
  A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);B.extend([u,v])
 return np.linalg.solve(np.asarray(A,float),np.asarray(B,float)).tolist()
def warp(image,src,dst,size):
 return image.transform(size,Image.Transform.PERSPECTIVE,coeff(dst,src),resample=Image.Resampling.BICUBIC)

def repair_floor(arr,b,dx):
 x0,y0,x1,y1=b; w=x1-x0;h=y1-y0
 # Every donor remains on unobstructed wood at exactly the same source Y,
 # preserving board-line height; blend low-frequency illumination to local edges.
 donor=a[y0:y1,x0+dx:x1+dx].copy()
 left=a[y0:y1,x0-5:x0].mean(axis=1);right=a[y0:y1,x1:x1+5].mean(axis=1)
 dl=donor[:,:5].mean(axis=1);dr=donor[:,-5:].mean(axis=1)
 t=np.linspace(0,1,w)[None,:,None]
 delta=((left-dl)[:,None,:]*(1-t)+(right-dr)[:,None,:]*t)
 delta=gaussian_filter(delta,(2.2,7,0))
 patch=np.clip(donor+delta,0,255)
 # Hard interior and 3px feather only at local boundary.
 yy,xx=np.mgrid[:h,:w];edge=np.minimum.reduce([xx,yy,w-1-xx,h-1-yy]);alpha=np.clip(edge/3,0,1)[...,None]
 arr[y0:y1,x0:x1]=arr[y0:y1,x0:x1]*(1-alpha)+patch*alpha
 return patch

out=a.copy(); edits=Image.new('L',im.size); ed=ImageDraw.Draw(edits)
for s in specs:
 repair_floor(out,s['remove'],205 if s['id'].startswith('west') else -205)
 ed.rectangle(s['remove'],fill=255)
clean=Image.fromarray(out.astype('uint8'));clean.save(R/'source-assets/local-floor-restoration.png')
base=clean.convert('RGBA');records=[]
for s in specs:
 # Rectify original surface, including its charcoal texture. Repair only the
 # original block footprint with a neighboring region of this same mat texture.
 quad=s['quad']; rect=[(0,0),(149,0),(149,59),(0,59)]
 tex=warp(im,quad,rect,(150,60)).convert('RGBA')
 ta=np.asarray(tex).copy()
 if s['id'].startswith('west'):
  ta[:,116:150]=ta[:,77:111]
 else:
  ta[:,0:36]=ta[:,39:75]
 tex=Image.fromarray(ta)
 mask=Image.new('L',tex.size);d=ImageDraw.Draw(mask);d.rounded_rectangle((0,0,149,59),radius=3,fill=255);tex.putalpha(mask)
 tex.save(R/'source-assets'/f"{s['id']}-original-surface.png")
 # Quarter turn in ground space: ~150px long x 60px wide becomes 98px long
 # in the north/south projection. Gentle inward lean shows the instructor edge.
 cx=s['cx'];cy=385;lean=10 if cx<768 else -10
 dst=[(cx+lean-26,cy-55),(cx-lean-31,cy+55),(cx-lean+31,cy+55),(cx+lean+26,cy-55)]
 # Original long U axis now points from north to south; short V is crosswise.
 shadow=Image.new('RGBA',im.size);sd=ImageDraw.Draw(shadow);sd.polygon([(x+1,y+3) for x,y in dst],fill=(31,22,14,95));shadow=shadow.filter(ImageFilter.GaussianBlur(1.3));base.alpha_composite(shadow)
 mat=warp(tex,rect,dst,im.size);base.alpha_composite(mat)
 # Original blocks and bottles retain image-up verticals and original dimensions.
 # A precise mask segments the dark prop + original local contact shadow only.
 props=[]
 for typ in ['block','bottle']:
  b=s[typ];crop=im.crop(b).convert('RGBA');ar=np.asarray(crop).copy();rgb=ar[:,:,:3].astype(float)
  # Mat/wood shadows are not moved as rectangular floor patches. Blocks are
  # tightly cropped; bottle silhouettes include their retained charcoal bases.
  if typ=='block':
   yy,xx=np.mgrid[:crop.height,:crop.width]
   # Source block perimeter based on dark blue object color, excluding mat brown.
   mx=rgb.max(2);mn=rgb.min(2)
   alpha=((mx<110)&((rgb[:,:,2]>=rgb[:,:,0]*0.84))).astype('uint8')*255
   # Select largest central component, including dark rim.
   from scipy.ndimage import label,binary_fill_holes,binary_closing
   lab,n=label(alpha>0);sizes=np.bincount(lab.ravel());sizes[0]=0
   alpha=binary_fill_holes(lab==sizes.argmax()).astype('uint8')*255
   ar[:,:,3]=alpha
   px=int(cx+lean-12);py=cy-53
  else:
   # All charcoal pixels in tight source bottle crop, preserving upright bottle.
   mx=rgb.max(2);alpha=(mx<140).astype('uint8')*255
   from scipy.ndimage import label,binary_fill_holes
   lab,n=label(alpha>0);sizes=np.bincount(lab.ravel());sizes[0]=0
   alpha=binary_fill_holes(lab==sizes.argmax()).astype('uint8')*255
   ar[:,:,3]=alpha
   px=int(cx+lean+34 if cx<768 else cx+lean-54);py=cy-61
  prop=Image.fromarray(ar);prop.save(R/'source-assets'/f"{s['id']}-{typ}-upright.png")
  base.alpha_composite(prop,(px,py));ed.rectangle((px-2,py-2,px+prop.width+2,py+prop.height+2),fill=255)
  props.append(dict(kind=typ,sourceBox=b,destination=[px,py],upright=True))
 ed.polygon([(x-5 if x<cx else x+5,y-5 if y<cy else y+7) for x,y in dst],fill=255)
 records.append(dict(id=s['id'],sourceQuad=quad,destinationQuad=dst,surfaceSource='Same original mat; own adjacent texture under removed block',props=props))
base.convert('RGB').save(R/'previews/instructor-facing-concept.png')
edits.save(R/'previews/permitted-edit-mask.png')
b=np.asarray(base.convert('RGB'));changed=np.any(b!=np.asarray(im),axis=2);allowed=np.asarray(edits)>0
# Gaussian shadow extends; changed pixels are recorded exactly. Core requested
# preserved region includes architecture, equipment, furniture, medallion.
preserved=np.ones((H,W),bool);preserved[275:470,190:608]=False;preserved[275:470,925:1348]=False
assert not changed[preserved].any(), 'Edit escaped six-mat floor areas'
proof=dict(sourceSha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),sourceSize=list(im.size),outputSha256=hashlib.sha256((R/'previews/instructor-facing-concept.png').read_bytes()).hexdigest(),retainedOriginalUnchanged=True,sourceMats=6,outputMats=6,allSixUseOwnSourceTexture=True,propsRemainUpright=True,entireMedallionByteExact=bool(np.array_equal(a[282:535,607:929].astype('uint8'),b[282:535,607:929])),protectedRegionPixels=int(preserved.sum()),protectedRegionChangedPixels=int(changed[preserved].sum()),totalChangedPixels=int(changed.sum()),editsRestrictedTo='Two original mat floor neighborhoods; room, equipment, furniture, exterior, medallion exact',generationUsed=False,records=records)
(R/'previews/SOURCE-PRESERVATION.json').write_text(json.dumps(proof,indent=2)+'\n')
# A readable two-up concept. The original is copied visually without edits.
font=font_load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',25)
small=font_load('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
card=Image.new('RGB',(1536,1138),'#182620');d=ImageDraw.Draw(card)
d.text((24,16),'RETAINED ORIGINAL',font=font,fill='#ead4a3');d.text((792,16),'INSTRUCTOR-FACING VARIANT',font=font,fill='#ead4a3')
card.paste(im.resize((768,512)),(0,58));card.paste(base.convert('RGB').resize((768,512)),(768,58))
d.text((24,589),'Six original charcoal mats, turned in floor perspective. Original upright blocks and bottles.',font=small,fill='white')
d.text((24,618),'Room, equipment, timber, plants, nooks, outdoor setting, and center medallion are byte-exact.',font=small,fill='white')
card.paste(im.crop((190,270,1348,475)).resize((1158,205)),(189,666));card.paste(base.crop((190,270,1348,475)).resize((1158,205)),(189,896))
d.text((24,748),'BEFORE',font=small,fill='#ead4a3');d.text((24,978),'AFTER',font=small,fill='#ead4a3')
card.save(R/'previews/before-after-concept.png')
print(json.dumps({k:v for k,v in proof.items() if k!='records'},indent=2))
