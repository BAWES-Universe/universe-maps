"""Uniformly calibrated matching outdoor furniture; native32 occupants."""
bench_fronts=Image.new('RGBA',(1744,1120))
for n in ('lounge-front','table-cups','stool-front','bench-front'):
 im=Image.open(R/'source/cafe-candidates/extracted'/(n+'.png')).convert('RGBA')
 out=Image.new('RGBA',(48,64) if n=='stool-front' else (math.ceil(im.width/16)*16,math.ceil(im.height/16)*16));out.alpha_composite(im,(8,8) if n=='stool-front' else (0,0))
 sprites['out-'+n]=out

def new_cafe_item(n,x,y,block=None):
 item('out-'+n,x,y,block)
 if n=='table-cups':return
 im=sprites['out-'+n];a=np.array(im);row={'lounge-front':60,'stool-front':28,'bench-front':44}[n];a[:row,:,3]=0;piece=Image.fromarray(a)
 if n=='bench-front':bench_fronts.alpha_composite(piece,(x-3504,y-3136))
 else:cafe_foreground.alpha_composite(piece,(x-CX,y-CY))
# Native curves retain three separate seat positions, accessible from their open face.
for x,y in [(2352,4352),(2928,4336)]:
 new_cafe_item('lounge-front',x,y,(x,y,176,16))
 for dx in (40,88,136):seats.append(dict(x=x+dx,y=y+48,group='cafe-lounge',facing='down'))
for x,y in [(2544,4352),(2816,4336)]:new_cafe_item('table-cups',x,y,(x,y+16,64,32))
# Bar stools stay along the existing counter; they do not replace or move its artwork.
for x,y in [(2592,4288),(2704,4272),(2816,4256),(2928,4256)]:
 new_cafe_item('stool-front',x,y)
 seats.append(dict(x=x+24,y=y+16,group='cafe-bar',facing='up'))
# Registered foreground lamp/planter obstacle and original scenic counter.
rectwalk((2656,4368,64,80),0)
rectwalk((PX+140*S,PY+650*S,250*S,87*S),0)
