"""Code-authored alpha-only art. No environment pixels are edited or resampled."""
from PIL import Image, ImageDraw
import math, hashlib
T=32

def frame(spec,p,k):
    im=Image.new('RGBA',(T,T)); cx,cy=p['center']; rgb=tuple(spec['color'])
    if spec['kind']=='water':
        d=ImageDraw.Draw(im)
        # Sparse, staggered 1px ripple arcs. Slow shape and alpha motion; not a waterfall.
        phase=k*math.pi/4
        width=p['width']+round(2*math.sin(phase))
        yy=cy+round(math.sin(phase))
        alpha=[20,27,34,29,22,15,18,24][k]
        d.arc((cx-width/2,yy-2,cx+width/2,yy+2),10,154,fill=rgb+(alpha,),width=1)
        d.arc((cx-width/2+4,yy-7,cx+width/2-1,yy-4),194,313,fill=rgb+(max(7,alpha-9),),width=1)
        # The sparkle is a two-pixel reflection, not a flashing starburst.
        sx=cx+round(3*math.sin(phase)); sy=cy-3
        d.point((sx,sy),fill=rgb+([18,24,34,42,30,16,10,13][k],))
        d.point((sx+1,sy),fill=rgb+([8,12,17,21,15,8,5,6][k],))
    else:
        # A small amber variation within the already-lit glass, never over the cap or floor.
        rx,ry=p['radii']; strength=[14,20,17,29,22,16,25,18][k]
        px=im.load()
        for y in range(1,31):
            for x in range(1,31):
                r=((x-cx)/rx)**2+((y-cy)/ry)**2
                if r<1: px[x,y]=rgb+(round(strength*(1-r)**1.2),)
    # Canonical fully transparent pixels, no concealed RGB or boundary bleed.
    px=im.load()
    for y in range(T):
        for x in range(T):
            if x in (0,31) or y in (0,31) or px[x,y][3]==0: px[x,y]=(0,0,0,0)
    return im

def build_atlas(spec):
    ps=spec['placements'];out=Image.new('RGBA',(8*T,len(ps)*T));rows=[]
    for i,p in enumerate(ps):
        hs=[];counts=[];alphas=[]
        for k in range(8):
            im=frame(spec,p,(k+p['phase'])%8);out.paste(im,(k*T,i*T));hs.append(hashlib.sha256(im.tobytes()).hexdigest())
            a=list(im.getchannel('A').getdata());counts.append(sum(v>0 for v in a));alphas.append(max(a))
        assert len(set(hs))==8, 'All eight frames must be genuinely distinct'
        rows.append(dict(cell=p['cell'],frameSHA256=hs,distinctFrames=8,changedPixelsPerFrame=counts,maxAlphaPerFrame=alphas))
    return out,rows
