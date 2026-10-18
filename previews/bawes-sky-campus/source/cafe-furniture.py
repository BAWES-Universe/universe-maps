"""Uniformly calibrated matching outdoor furniture; native32 occupants."""
bench_fronts=Image.new('RGBA',(1744,1120))
for n in ('lounge-front','table-cups','stool-front','bench-front','chair-right','chair-left'):
 im=Image.open(R/'source/cafe-candidates/extracted'/(n+'.png')).convert('RGBA')
 out=Image.new('RGBA',(48,64) if n=='stool-front' else (math.ceil(im.width/16)*16,math.ceil(im.height/16)*16));out.alpha_composite(im,(8,8) if n=='stool-front' else (0,0))
 sprites['out-'+n]=out

im=Image.open(R/'source/cafe-candidates/extracted/lounge-front.png').convert('RGBA');im=im.resize((144,round(im.height*144/im.width)),Image.Resampling.LANCZOS)
out=Image.new('RGBA',(144,64));out.alpha_composite(im);sprites['out-cafe-curve']=out

def new_cafe_item(n,x,y,block=None):
 item('out-'+n,x,y,block)
 if n=='table-cups':return
 im=sprites['out-'+n];a=np.array(im);row={'lounge-front':60,'stool-front':28,'bench-front':44,'cafe-curve':46,'chair-right':48,'chair-left':48}[n];a[:row,:,3]=0;piece=Image.fromarray(a)
 if n=='bench-front':bench_fronts.alpha_composite(piece,(x-3504,y-3136))
 else:cafe_foreground.alpha_composite(piece,(x-CX,y-CY))
# Restore two intimate table groups. Curves face their nearby tables; side
# armchairs face inward. The clear approaches are east of the left group and
# west of the right group, rather than behind a lounge against the planted rim.
for x,y in [(2320,4304),(2944,4288)]:
 new_cafe_item('cafe-curve',x,y,(x,y,144,16))
 for dx in (40,104):seats.append(dict(x=x+dx,y=y+32,group='cafe-lounge',facing='down'))
for x,y in [(2400,4352),(2976,4368)]:new_cafe_item('table-cups',x,y,(x,y+16,64,32))
for n,x,y,facing in [('chair-right',2336,4352,'right'),('chair-left',3072,4352,'left')]:
 new_cafe_item(n,x,y);seats.append(dict(x=x+24,y=y+32,group='cafe-armchair',facing=facing))
# Bar stools stay along the existing counter; they do not replace or move its artwork.
for x,y in [(2592,4288),(2704,4272),(2816,4256),(2928,4256)]:
 new_cafe_item('stool-front',x,y)
 seats.append(dict(x=x+24,y=y+16,group='cafe-bar',facing='up'))
# Registered foreground lamp/planter obstacle and original scenic counter.
rectwalk((2656,4416,64,48),0) # Physical pedestal foot; foreground lantern head can overlap a walker.
rectwalk((PX+140*S,PY+650*S,250*S,87*S),0)
