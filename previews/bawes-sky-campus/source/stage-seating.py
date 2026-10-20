"""Material-adapt complete matching timber armchair views; preserve alpha and grain."""
# Rear view faces the actual stage; front view is retained for visual QA.
stage_fronts=Image.new('RGBA',(656,272));stage_shadows=Image.new('RGBA',(656,272))
for view,src in [('up','chair-rear'),('down','chair-front')]:
 im=Image.open(R/'source/cafe-candidates/extracted'/(src+'.png')).convert('RGBA');a=np.asarray(im).copy();rgb=a[:,:,:3].astype('float32')
 lum=(rgb[:,:,0]*.299+rgb[:,:,1]*.587+rgb[:,:,2]*.114)/255
 # Walnut/tobacco palette removes cream and red while retaining source highlights,
 # slatted timber contours, joints and individual complete legs.
 v=lum**.78
 a[:,:,:3]=np.stack([8+145*v,6+103*v,4+67*v],axis=2).astype('uint8')
 dark=Image.fromarray(a);out=Image.new('RGBA',(48,64));out.alpha_composite(dark,(0,8));sprites['audience-'+view]=out;out.save(A/('audience-'+view+'.png'))
for bx in (5504,5856):
 for row in range(4):
  for col in range(4):
   x=bx+col*64;y=3152+row*64
   item('audience-up',x,y)
   seats.append(dict(x=x+24,y=y+32,group='audience',facing='up'))
   im=sprites['audience-up'].copy();ar=np.array(im);ar[:40,:,3]=0;stage_fronts.alpha_composite(Image.fromarray(ar),(x-5472,y-3152))
   ImageDraw.Draw(stage_shadows).ellipse((x-5472+3,y-3152+45,x-5472+47,y-3152+59),fill=(51,34,19,65))
stage_shadows=stage_shadows.filter(ImageFilter.GaussianBlur(2))
