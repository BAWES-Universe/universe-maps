"""Registered, bounded material replacement. Source coordinates use PX/PY and S=3."""
CX,CY,CW,CH=2176,4192,1120,352
# Trace stays inside the existing stone rim; right stone bridge/landing is excluded.
deck=[(138,759),(148,754),(163,750),(181,746),(190,746),(198,748),(204,747),(205,741),(217,739),(228,742),(239,741),(250,744),(257,741),(276,737),(298,733),(320,730),(344,726),(366,722),(375,722),(381,724),(385,721),(396,722),(406,726),(419,730),(431,736),(443,742),(452,749),(458,758),(459,765),(454,773),(445,780),(430,786),(410,790),(386,794),(359,796),(330,797),(305,797),(275,797),(250,797),(228,796),(206,793),(185,792),(166,789),(151,785),(139,779),(134,772),(134,766)]
# Continuous front silhouette: lamps, plants and balustrade, including left foliage
# discovered outside the earlier approximate (262,758) envelope during tracing.
front=[(130,780),(145,786),(165,793),(195,798),(224,799),(230,797),(232,790),(236,789),(239,794),(241,788),(244,786),(246,789),(244,796),(249,796),(252,791),(256,794),(260,796),(263,796),(265,794),(269,794),(273,797),(278,793),(280,789),(282,785),(285,786),(289,790),(289,782),(287,779),(290,776),(294,774),(293,772),(295,770),(299,770),(301,773),(300,775),(305,778),(307,780),(305,783),(305,789),(309,790),(310,794),(313,792),(315,793),(316,796),(320,797),(321,796),(324,795),(328,797),(340,799),(350,795),(354,799),(366,799),(371,796),(377,800),(386,798),(394,798),(401,797),(410,795),(420,791),(429,788),(437,784),(444,779),(449,773),(454,769),(458,766),(462,763),(468,760),(480,758),(480,826),(130,826)]
def trace(points):
 mask=Image.new('L',(CW*2,CH*2));ImageDraw.Draw(mask).polygon([((PX+x*S-CX)*2,(PY+y*S-CY)*2) for x,y in points],fill=255)
 return mask.resize((CW,CH),Image.Resampling.LANCZOS)
foot=trace(deck);fgmask=trace(front)
# Feather only one native pixel; exclude the complete foreground silhouette.
fgmask=fgmask.filter(ImageFilter.GaussianBlur(.55))
# Remove pale floor fringes only along the traced upper foliage/lantern edge.
# Interior opaque lamp highlights and the stone balustrade are preserved.
original=sky.crop((CX,CY,CX+CW,CY+CH));rgb=np.asarray(original)[:,:,:3].astype('int16')
pale=(rgb[:,:,0]>180)&(rgb[:,:,1]>145)&(rgb[:,:,2]>105)&((rgb[:,:,0]-rgb[:,:,2])<125)
upper=np.indices((CH,CW))[0] < (PY+791*S-CY)
fa=np.asarray(fgmask);eroded=np.asarray(fgmask.filter(ImageFilter.MinFilter(7)))
fgmask=Image.fromarray(np.where(pale&upper,eroded,fa).astype('uint8'))
alpha=np.asarray(foot).astype('float32')*(1-np.asarray(fgmask).astype('float32')/255)
mask=Image.fromarray(alpha.astype('uint8'))
material=Image.open(R/'source/cafe-candidates/cafe-ground-candidate.png').convert('RGBA').crop((480,460,820,500))
wood=Image.new('RGBA',(CW,CH))
for yy in range(0,CH,40):
 for xx in range(0,CW,340):
  sample=material.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if (xx//340)%2 else material
  if (yy//40)%2:sample=sample.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  wood.alpha_composite(sample,(xx,yy))
# Fine native board joints: continuous horizontal courses, staggered ends.
wd2=ImageDraw.Draw(wood)
for yy in range(12,CH,24):
 wd2.line((0,yy,CW,yy),fill=(145,84,35,105),width=1)
 for xx in range((yy//24%2)*96,CW,192):wd2.line((xx,yy,xx,yy+23),fill=(154,91,40,95),width=1)
wood.putalpha(mask);cafe_ground=wood
original=sky.crop((CX,CY,CX+CW,CY+CH));cafe_foreground=original.copy();cafe_foreground.putalpha(fgmask)
mask.save(R/'source/cafe-candidates/registered-deck-mask.png');fgmask.save(R/'source/cafe-candidates/registered-foreground-mask.png')
restored=original.copy();restored.alpha_composite(cafe_ground);restored.alpha_composite(cafe_foreground)
a=np.asarray(original);b=np.asarray(restored);outside=np.asarray(mask)==0
assert np.array_equal(a[outside],b[outside])
restored.save(R/'review/cafe-registered-ground.png')
(R/'review/cafe-registration.json').write_text(json.dumps(dict(worldPatch=[CX,CY,CW,CH],transform=dict(origin=[PX,PY],scale=S),deckTrace=deck,foregroundTrace=front,materialSample=[480,460,820,500],materialScale=1,wholeCandidatePasted=False,outsideMaskPixelsUnchanged=True,changedPixels=int(np.any(a!=b,axis=2).sum()),foregroundExtendedLeftForFoliage=True),indent=2)+'\n')
