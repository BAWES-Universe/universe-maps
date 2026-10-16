"""Reproducible campus asset compiler; owner visual acceptance remains open. Python + Pillow."""
import json
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
W, H, T = 64, 48, 32
SIZE = (W*T, H*T)
INK, RAISED, EDGE = '#14121e', '#292535', '#575069'
floor = Image.new('RGBA', SIZE, INK)
d = ImageDraw.Draw(floor)
blocked = set()
seats = []
tables = []
def rect(box, color, outline=None):
    x,y,w,h=box
    d.rectangle((x*T,y*T,(x+w)*T-1,(y+h)*T-1),fill=color,outline=outline)
def block(box):
    x,y,w,h=box
    blocked.update((i,j) for j in range(y,y+h) for i in range(x,x+w))

# Campus paving stays continuous; contrasting raised planes identify useful places.
rect((1,1,62,46),'#201d2b')
rect((7,31,51,12),'#353140',EDGE)
rect((19,27,6,17),'#55505f')  # continuous 192px arrival spine
rect((6,32,53,6),'#484250')  # 192px cross-campus promenade
# The occupied footprint covers the FULL projected shell, including its crown.
rect((10,12,24,19),'#302c3c',EDGE)
rect((11,13,22,17),'#3e384b')
# Connected rear terrace and side paths remain outside that footprint.
rect((4,5,36,7),'#484250',EDGE)
rect((4,12,6,20),'#484250')
rect((34,12,6,20),'#484250')
rect((42,17,17,14),'#302c3c',EDGE) # reserved future StudentHub courtyard
rect((44,19,13,10),'#393545')
for x in range(0,W,2):
    d.line((x*T,32*T,x*T,38*T), fill='#504a59')
for y in range(32,39,2):
    d.line((6*T,y*T,59*T,y*T), fill='#504a59')
# Native paving texture: quiet stone seams, distinct from the raised furniture.
rng=random.Random(41)
for yy in range(13*T,30*T,32):
    for xx in range(11*T,33*T,32):
        d.line((xx,yy,xx+31,yy),fill='#484154')
        for _ in range(9):
            px,py=xx+rng.randrange(32),yy+rng.randrange(32)
            d.point((px,py),fill=rng.choice(['#413b4e','#393344','#453e51']))
for yy in range(31*T,43*T,32):
    for xx in range(7*T,58*T,64):
        d.line((xx,yy,xx+63,yy),fill='#514a5a')
        d.line((xx,yy,xx,yy+31),fill='#2e2a38')
# Permanent wall footprint does not belong to the revealable facade.
for box in [(10,12,9,1),(25,12,9,1),(10,13,1,18),(33,13,1,18),(11,30,8,1),(25,30,8,1)]:
    block(box);rect(box, '#1e1b28', '#8b809e')
for box in [(0,0,W,1),(0,H-1,W,1),(0,1,1,H-2),(W-1,1,1,H-2)]:
    block(box)
    rect(box, '#100e18')

backs = Image.new('RGBA', SIZE)
bd = ImageDraw.Draw(backs)
def chair(x,y):
    # Reachable native tile; only the near backrest overlaps a standing Woka.
    seats.append([x,y])
    d.ellipse((x*T+2,y*T+8,x*T+30,y*T+23),fill='#24212d')
    d.rounded_rectangle((x*T+5,y*T-5,x*T+27,y*T+16),5,fill='#7c7198',outline='#b9aad8')
    bd.rounded_rectangle((x*T+4,y*T+9,x*T+28,y*T+17),3,fill='#554768',outline='#b4a2cd')
    d.line((x*T+9,y*T-2,x*T+23,y*T-2),fill='#9e90b8')
    d.line((x*T+6,y*T+1,x*T+6,y*T+10),fill='#50455f')
    d.line((x*T+26,y*T+1,x*T+26,y*T+10),fill='#50455f')
    bd.line((x*T+8,y*T+12,x*T+24,y*T+12),fill='#76658b')
def table(x,y,w,h):
    tables.append([x,y,w,h])
    block((x,y,w,h))
    rect((x,y,w,h),'#211d2b')
    d.rounded_rectangle((x*T+2,y*T+2,(x+w)*T-3,(y+h)*T-6),8,fill='#61576e',outline='#c4b5fd',width=2)
    d.line((x*T+8,y*T+9,(x+w)*T-9,y*T+9),fill='#827490',width=2)
    for xx in range(x*T+7,(x+w)*T-7,13):
        d.line((xx,y*T+13,xx,(y+h)*T-10),fill='#6c617b')
    # Cup, paper and task pad remain below avatar depth and inside table collision.
    d.rectangle((x*T+11,y*T+12,x*T+24,y*T+21),fill='#c7c2cf')
    d.line((x*T+14,y*T+15,x*T+21,y*T+15),fill='#736a82')
    d.ellipse(((x+w)*T-22,y*T+13,(x+w)*T-16,y*T+19),fill='#e0d8ca',outline='#a89c8e')
    d.ellipse(((x+w)*T-20,y*T+14,(x+w)*T-17,y*T+17),fill='#463c49')

# Daily work and social groups sit at the arrival-facing edge; quieter work at rear.
for x,y,w,h in [(13,14,4,2),(26,14,4,2),(13,7,3,1),(27,7,3,1),(13,26,3,1),(27,26,3,1),(13,20,4,2),(26,20,4,2),(9,40,3,1),(48,40,3,1),(46,21,2,1),(52,21,2,1),(46,26,2,1),(52,26,2,1)]:
    table(x,y,w,h)
    for sx in range(x,x+w): chair(sx,y+2)
for box in [(4,28,3,3),(36,28,3,3),(37,40,3,3),(54,40,3,3)]:
    block(box);rect(box,'#343d3c','#6e7772')
    x,y,w,h=box
    for dx,dy in [(1,1),(.4,.5),(1.9,1.5)]:
        d.ellipse(((x+dx)*T,(y+dy)*T,(x+dx+1)*T,(y+dy+1)*T),fill='#53675e')
# Layered foliage with a single light direction, wholly inside its planter footprint.
for x,y in [(4,28),(36,28),(54,40)]:
    d.rounded_rectangle((x*T+3,y*T+5,(x+3)*T-4,(y+3)*T-3),10,fill='#252c2f',outline='#768278',width=2)
    for cx,cy in [(x*T+26,y*T+32),(x*T+56,y*T+51),(x*T+68,y*T+25)]:
        d.ellipse((cx-17,cy-15,cx+20,cy+24),fill='#20352f')
        for j in range(27):
            a=rng.random()*math.tau;rr=rng.random()*18
            lx,ly=cx+math.cos(a)*rr,cy+math.sin(a)*rr
            col=rng.choice(['#466757','#527963','#5d8068','#6e8d70'])
            d.ellipse((lx-4,ly-3,lx+4,ly+3),fill=col)
# Thin gold threshold detail, never a text label or a blocking wayfinding object.
d.line((19*T,31*T,25*T,31*T),fill='#e9c74c',width=3)

# Permanent interior details remain after reveal: rear counters, monitors, ceiling-free plan.
for x in [13,15,26,28]:
    d.rounded_rectangle((x*T+6,20*T+8,x*T+26,20*T+22),3,fill='#171922',outline='#756d91')
    d.rectangle((x*T+9,20*T+11,x*T+23,20*T+18),fill='#6b64ad')
for x in range(11,34,2):
    d.line((x*T,13*T,x*T,30*T-1),fill='#443d50')
# Architectural base, canopy edge and discreet floor lighting frame the open route.
for x in [18,25]:
    d.rectangle((x*T+4,29*T,x*T+12,31*T-1),fill='#201c2d',outline='#82739d')
    d.rectangle((x*T+7,29*T+10,x*T+9,30*T+20),fill='#e9c74c')
for y in range(32,44,2):
    for x in [19,24]:d.rectangle((x*T+12,y*T+8,x*T+17,y*T+14),fill='#b8aacd')
# Pond/rill beyond circulation; twelve? no, 24 equally spaced frames loop continuously.
water=Image.new('RGBA',(768,576))
for frame in range(48):
    waterframe=Image.new('RGBA',(96,96));wd=ImageDraw.Draw(waterframe)
    ox=0
    wd.rounded_rectangle((ox,0,ox+95,95),12,fill='#252338',outline='#7d7395',width=3)
    wd.rounded_rectangle((ox+7,7,ox+88,88),9,fill='#243b52',outline='#586e87',width=2)
    for row in range(4):
        yy=19+row*18
        pts=[(ox+12+j,yy+3*math.sin(j/10+frame*math.tau/48+row)) for j in range(72)]
        wd.line(pts,fill=(112,153,191,160),width=1)
    water.alpha_composite(waterframe,((frame%8)*96,(frame//8)*96))
water.save(ROOT/'water.png')
block((37,40,3,3))

# Compile generated, source-retained architecture into the authored 32px layer.
# Floor-level openings are true alpha holes; a restrained independent glass tint
# provides predictable Woka visibility instead of baked interior occupants.
art=Image.open(ROOT/'source/tower-cutout-original.png').convert('RGBA')
art=art.crop((37,14,1432,1086)).resize((768,590),Image.Resampling.LANCZOS)
glass=Image.new('RGBA',SIZE)
gd=ImageDraw.Draw(glass)
for x0,x1 in [(11*T,19*T),(25*T,33*T)]:
    gd.rectangle((x0,27*T,x1-1,30*T-1),fill=(111,101,190,45))
glass.alpha_composite(art,(10*T,31*T-590))

# Keep a seven-tile-deep outdoor area behind the entire building.
Y_SHIFT=4
for box in [(0,Y_SHIFT,64,1),(0,45,64,1)]:
    block(box);rect(box,'#15131f','#4a4359')
floor=floor.crop((0,Y_SHIFT*T,W*T,46*T))
backs=backs.crop((0,Y_SHIFT*T,W*T,46*T))
glass=glass.crop((0,Y_SHIFT*T,W*T,46*T))
blocked={(x,y-Y_SHIFT) for x,y in blocked if Y_SHIFT<=y<46}
seats=[[x,y-Y_SHIFT] for x,y in seats]
tables=[[x,y-Y_SHIFT,w,h] for x,y,w,h in tables]
H=46-Y_SHIFT;SIZE=(W*T,H*T)

# Tile atlases are faithful layer exports; no picture-derived collision inference.
layers=[];tilesets=[];gid=1
def atlas(name,img):
    global gid
    img.save(ROOT/(name+'.png'))
    tilesets.append(dict(firstgid=gid,name=name,image=name+'.png',imagewidth=SIZE[0],imageheight=SIZE[1],tilewidth=T,tileheight=T,tilecount=W*H,columns=W,margin=0,spacing=0))
    data=[gid+i if img.crop(((i%W)*T,(i//W)*T,(i%W+1)*T,(i//W+1)*T)).getbbox() else 0 for i in range(W*H)]
    gid+=W*H
    return data
def layer(name,data,opacity=1):
    layers.append(dict(id=len(layers)+1,type='tilelayer',name=name,x=0,y=0,width=W,height=H,opacity=opacity,visible=True,data=data))
layer('ground-and-furniture',atlas('ground',floor))
watergid=gid;gid+=432
tilesets.append(dict(firstgid=watergid,name='water',image='water.png',imagewidth=768,imageheight=576,tilewidth=32,tileheight=32,tilecount=432,columns=24,tiles=[dict(id=ry*24+rx,animation=[dict(tileid=(frame//8*3+ry)*24+(frame%8)*3+rx,duration=40) for frame in range(48)]) for ry in range(3) for rx in range(3)]))
layer('pond-motion',[watergid+(y-(40-Y_SHIFT))*24+x-37 if 37<=x<40 and 40-Y_SHIFT<=y<43-Y_SHIFT else 0 for y in range(H) for x in range(W)])
logic=Image.new('RGBA',(64,32));logic.save(ROOT/'logic.png')
logicgid=gid;gid+=2
tilesets.append(dict(firstgid=logicgid,name='logic',image='logic.png',imagewidth=64,imageheight=32,tilewidth=32,tileheight=32,tilecount=2,columns=2,tiles=[dict(id=0,properties=[dict(name='collides',type='bool',value=True)])]))
layer('persistent-collision',[logicgid if (x,y) in blocked else 0 for y in range(H) for x in range(W)])
layer('start',[logicgid+1 if (x,y)==(22,34-Y_SHIFT) else 0 for y in range(H) for x in range(W)])
layer('tower-interior',[logicgid+1 if 11<=x<33 and 13-Y_SHIFT<=y<30-Y_SHIFT else 0 for y in range(H) for x in range(W)])
layers.append(dict(id=len(layers)+1,type='objectgroup',name='floorLayer',x=0,y=0,opacity=1,visible=True,objects=[]))
layer('seat-backs',atlas('seat-backs',backs))
layer('tower-glass-cover',atlas('tower-glass',glass))
mapdata=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=W,height=H,tilewidth=T,tileheight=T,nextlayerid=len(layers)+1,nextobjectid=1,layers=layers,tilesets=tilesets,properties=[dict(name='script',type='string',value='runtime.js'),dict(name='mapCopyright',type='string',value='Original BAWES campus architectural blockout; mark supplied by BAWES Universe.')])
(ROOT/'campus.tmj').write_text(json.dumps(mapdata,separators=(',',':'))+'\n')
layout=dict(status='geometry correction in progress; prior client evidence superseded; visual reference pending',grid=[W,H,T],spawn=[22,34-Y_SHIFT],entrance=[19,30-Y_SHIFT,6,1],rear_entrance=[19,12-Y_SHIFT,6,1],interior=[11,13-Y_SHIFT,22,17],building_footprint=[10,12-Y_SHIFT,24,19],rear_terrace=[4,5-Y_SHIFT,36,7],studenthub_reserve=[42,17-Y_SHIFT,17,14],seats=seats,tables=tables,source_y_offset_tiles=Y_SHIFT,main_route_width_px=192,podium_tint_alpha=45,brand_reference_paths='source/lettermark.svg',tower_asset_bounds=[320,31*T-590-Y_SHIFT*T,768,590])
(ROOT/'source/layout.json').write_text(json.dumps(layout,indent=2)+'\n')
preview_floor=floor.copy();preview_floor.alpha_composite(water.crop((0,0,96,96)),(37*T,(40-Y_SHIFT)*T))
for name,img in [('layout',preview_floor),('outside',Image.alpha_composite(Image.alpha_composite(preview_floor,backs),glass)),('inside',Image.alpha_composite(preview_floor,backs))]:
    img.save(ROOT/'review'/(name+'.png'))
print('Built campus.tmj, separate runtime layers and offline review exports.')

runtime = """/* Local shell reveal: permanent floor, furniture and collision remain. */
(async () => {
    await WA.onInit();
    const cover = 'tower-glass-cover';
    const inside = ({x,y}) => x >= 352 && x < 1056 && y >= %d && y < %d;
    const apply = value => value ? WA.room.hideLayer(cover) : WA.room.showLayer(cover);
    apply(inside(await WA.player.getPosition()));
    WA.room.onEnterLayer('tower-interior').subscribe(() => apply(true));
    WA.room.onLeaveLayer('tower-interior').subscribe(() => apply(false));
})().catch(error => console.error('Campus reveal initialization failed', error));
""" % ((13-Y_SHIFT)*T, (30-Y_SHIFT)*T)
(ROOT/'runtime.js').write_text(runtime)
