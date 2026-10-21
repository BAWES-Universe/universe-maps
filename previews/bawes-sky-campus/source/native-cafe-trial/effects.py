"""Small procedural overlay sprites: eleven reused animations, never per-map-cell definitions."""
from PIL import Image, ImageDraw
import math

def add_effects(m, output):
    size=16; frames=4; kinds=11
    atlas=Image.new('RGBA',(frames*size,kinds*size))
    for kind in range(kinds):
        for frame in range(frames):
            tile=Image.new('RGBA',(size,size));d=ImageDraw.Draw(tile)
            if kind<5:
                # Sparse descending highlights; phase variants avoid marching rows.
                for x,start in [(3+kind%3,kind*3),(11-kind%3,8+kind*2)]:
                    y=(start+frame*4)%16
                    for j in range(5):
                        d.point((x,(y+j)%16),fill=(218,248,255,105-j*15))
            elif kind<9:
                r=2+(frame+kind)%4
                d.arc((8-r,8-r//2,8+r,8+r//2),0,175,fill=(179,239,244,90-frame*12))
            else:
                strength=[30,44,52,38][(frame+kind)%4]
                for y in range(16):
                    for x in range(16):
                        a=int(strength*max(0,1-math.hypot(x-7.5,y-7.5)/8))
                        tile.putpixel((x,y),(255,202,99,a))
            atlas.alpha_composite(tile,(frame*16,kind*16))
    atlas.save(output/'water-light-motion.png')
    first=max(s['firstgid']+s['tilecount'] for s in m['tilesets'])
    m['tilesets'].append(dict(firstgid=first,name='water-light-motion',image='water-light-motion.png',imagewidth=64,imageheight=176,tilewidth=16,tileheight=16,columns=4,tilecount=44,tiles=[dict(id=k*4,animation=[dict(tileid=k*4+f,duration=130 if k<5 else 240) for f in range(4)]) for k in range(11)]))
    data=[0]*(m['width']*m['height'])
    def place(x,y,kind):data[(y//16)*m['width']+x//16]=first+kind*4
    # Center ribbons stay inside the painted water rather than covering rocks/sky.
    for x0,y0,x1,y1 in [(2416,3584,2448,3840),(2448,4720,2496,5008),(5744,4768,5792,5280)]:
        for y in range(y0,y1,16):
            for x in range(x0,x1,16):place(x,y,(x//16+y//16)%5)
    for i,(x,y) in enumerate([(2224,4512),(2288,4528),(2384,4560),(2512,4592),(2544,4512),(2288,4480),(2480,4544),(2576,4560)]):place(x,y,5+i%4)
    for i,(x,y) in enumerate([(2320,3024),(2560,3024),(2240,3344),(2128,4032),(2680,4400),(3248,4288),(5304,3040),(4768,3216)]):place(x,y,9+i%2)
    layer=dict(id=m['nextlayerid'],name='water-and-lantern-motion',type='tilelayer',x=0,y=0,width=m['width'],height=m['height'],visible=True,opacity=1,data=data)
    m['nextlayerid']+=1;m['layers'].append(layer)
    return {'animationDefinitions':11,'animatedCells':sum(bool(x) for x in data),'frameCount':4}
