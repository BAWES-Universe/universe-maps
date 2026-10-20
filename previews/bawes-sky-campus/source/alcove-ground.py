"""Bounded recessed stone alcove. All geometry is measured in native world pixels."""
LX,LY,LW,LH=1968,3136,384,256
# Verified clear floor trace excludes current northern planters, left pillar,
# lower lamps/railing and the southeast flower bed.
trace=[(76,378),(91,372),(112,369),(132,370),(151,374),(166,383),(175,394),(182,394),(182,416),(173,417),(162,420),(155,427),(146,429),(132,432),(113,432),(96,430),(84,427),(80,418),(74,411),(73,400),(73,387)]
valid=Image.new('L',(LW,LH));ImageDraw.Draw(valid).polygon([(PX+x*3-LX,PY+y*3-LY) for x,y in trace],fill=255)
valid=valid.filter(ImageFilter.GaussianBlur(.6))
stone=Image.open(R/'source/interior-candidates/clean-floor.png').convert('RGBA').crop((640,192,880,432))
texture=Image.new('RGBA',(LW,LH))
for yy in range(0,LH,240):
 for xx in range(0,LW,240):texture.alpha_composite(stone,(xx,yy))
outer=(24,24,344,198);inner=(48,48,320,174)
base=Image.new('RGBA',(LW,LH));bd=ImageDraw.Draw(base)
# A curved side face below the cap provides actual illustrated depth.
face=texture.copy();fa=np.asarray(face).copy();fa[:,:,:3]=(fa[:,:,:3]*.68).astype('uint8');face=Image.fromarray(fa)
fm=Image.new('L',(LW,LH));ImageDraw.Draw(fm).ellipse((24,40,344,216),fill=255);face.putalpha(fm);base.alpha_composite(face)
cap=Image.new('L',(LW,LH));cd=ImageDraw.Draw(cap);cd.ellipse(outer,fill=255);cd.ellipse(inner,fill=0)
captex=texture.copy();captex.putalpha(cap);base.alpha_composite(captex)
# Lower inner floor is inset and shaded, not a large flat patch over the terrace.
inside=Image.new('L',(LW,LH));ImageDraw.Draw(inside).ellipse(inner,fill=255)
wall=texture.copy();wa=np.asarray(wall).copy();wa[:,:,:3]=(wa[:,:,:3]*.63).astype('uint8');wall=Image.fromarray(wa);wall.putalpha(inside);base.alpha_composite(wall)
lower=Image.new('L',(LW,LH));ImageDraw.Draw(lower).ellipse((48,66,320,192),fill=255)
lower=Image.fromarray(np.minimum(np.asarray(lower),np.asarray(inside)))
floor=texture.copy();arr=np.asarray(floor).copy();arr[:,:,:3]=(arr[:,:,:3]*.90).astype('uint8');floor=Image.fromarray(arr);floor.putalpha(lower);base.alpha_composite(floor)
bd=ImageDraw.Draw(base)
bd.ellipse(outer,outline='#d8b88f',width=1);bd.ellipse((26,27,342,197),outline='#bd9b70',width=1)
bd.ellipse(inner,outline='#8c6b45',width=4);bd.arc((51,51,317,176),180,355,fill='#b89c75',width=5)
# Jointed cap stones follow the curve instead of an outlined rectangle.
for degrees in range(0,360,20):
 t=math.radians(degrees);p=(184+160*math.cos(t),111+87*math.sin(t));q=(184+136*math.cos(t),111+63*math.sin(t));bd.line((p,q),fill='#af8c62',width=1)
# East-facing access: three treads and distinct risers, 64px clear width.
for i in range(3):
 x=288+i*24;y=96
 patch=texture.crop((x,y,x+24,y+64));pa=np.asarray(patch).copy();pa[:,:,:3]=(pa[:,:,:3]*(.84+i*.08)).astype('uint8');patch=Image.fromarray(pa);base.alpha_composite(patch,(x,y))
 bd.rectangle((x,y,x+23,y+63),outline='#bc9a6d',width=1)
 bd.line((x,y,x,y+63),fill='#795a38',width=3);bd.line((x+3,y+1,x+3,y+62),fill='#ddc29a',width=1)
# Bounded contact shadow and softened cut edge; preserve native stone detail.
alpha=base.getchannel('A');soft=alpha.filter(ImageFilter.GaussianBlur(2))
shadow=Image.new('RGBA',base.size,(70,48,28,0));shadow.putalpha(soft.point(lambda a:round(a*.28)))
edge=Image.fromarray(np.minimum(np.asarray(alpha),np.asarray(soft)).astype('uint8'))
base.putalpha(edge);shadow.alpha_composite(base);base=shadow
# Blend the final 8px of the east landing into its registered underlying floor.
a=np.asarray(base).copy();under=np.asarray(sky.crop((LX,LY,LX+LW,LY+LH)))
for x in range(352,360):
 t=(x-352)/7;a[96:160,x,:3]=(a[96:160,x,:3]*(1-t)+under[96:160,x,:3]*t).astype('uint8')
base=Image.fromarray(a)
# Apply the verified mask; all inherited plants/railing pixels stay untouched.
a=np.asarray(base).copy();a[:,:,3]=np.minimum(a[:,:,3],np.asarray(valid));base=Image.fromarray(a)
alcove_ground=base
# Front cap and side face sit above native occupants. The east opening stays clear.
fmask=Image.new('L',(LW,LH));fd=ImageDraw.Draw(fmask);fd.ellipse((24,40,344,216),fill=255);fd.ellipse(inner,fill=0);fd.rectangle((0,0,LW,150),fill=0);fd.rectangle((288,96,383,160),fill=0)
fg=base.copy();a=np.asarray(fg).copy();a[:,:,3]=np.minimum(a[:,:,3],np.asarray(fmask));alcove_foreground=Image.fromarray(a)
# Existing foreground plants/lamp silhouettes remain above the new recessed floor.
original=sky.crop((LX,LY,LX+LW,LY+LH));mask=np.asarray(valid)
copy_mask=Image.fromarray(np.where(np.indices((LH,LW))[0]>=160,255-mask,0).astype('uint8'));oldfore=original.copy();oldfore.putalpha(copy_mask);alcove_foreground.alpha_composite(oldfore)
preview=original.copy();preview.alpha_composite(base);preview.alpha_composite(alcove_foreground);preview.save(R/'review/alcove-ground.png')
valid.save(R/'source/alcove-registered-mask.png')
orig=np.asarray(original);now=np.asarray(preview);outside=np.asarray(valid)==0
assert np.array_equal(orig[outside],now[outside])
(R/'review/alcove-registration.json').write_text(json.dumps(dict(worldPatch=[LX,LY,LW,LH],referenceEnvelope=[60,366,182,444],floorTrace=trace,outerEllipse=outer,innerEllipse=inner,stepWorldBox=[LX+288,LY+96,72,64],outsideMaskPixelsUnchanged=True,depth='illustrated recess with 2D collision; no engine elevation change'),indent=2)+'\n')
