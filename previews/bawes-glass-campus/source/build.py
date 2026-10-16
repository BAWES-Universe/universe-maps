"""Reproducible architectural blockout, not accepted final art. Python + Pillow."""
import json
import re
import xml.etree.ElementTree as ET
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
rect((10,17,24,14),'#302c3c',EDGE)
rect((11,18,22,12),'#3e384b')
rect((42,17,17,14),'#302c3c',EDGE) # reserved future StudentHub courtyard
rect((44,19,13,10),'#393545')
for x in range(0,W,2):
    d.line((x*T,32*T,x*T,38*T), fill='#504a59')
for y in range(32,39,2):
    d.line((6*T,y*T,59*T,y*T), fill='#504a59')
# Permanent wall footprint does not belong to the revealable facade.
for box in [(10,17,24,1),(10,18,1,13),(33,18,1,13),(11,30,8,1),(25,30,8,1)]:
    block(box);rect(box, '#1e1b28', '#8b809e')
for box in [(0,0,W,1),(0,H-1,W,1),(0,1,1,H-2),(W-1,1,1,H-2)]:
    block(box)
    rect(box, '#100e18')

backs = Image.new('RGBA', SIZE)
bd = ImageDraw.Draw(backs)
def chair(x,y):
    # Reachable native tile; only the near backrest overlaps a standing Woka.
    seats.append([x,y])
    d.rounded_rectangle((x*T+5,y*T+6,x*T+27,y*T+27),5,fill='#7c7198',outline='#b9aad8')
    bd.rounded_rectangle((x*T+4,y*T+23,x*T+28,y*T+30),3,fill='#554768',outline='#b4a2cd')
def table(x,y,w,h):
    block((x,y,w,h))
    rect((x,y,w,h),'#211d2b')
    d.rounded_rectangle((x*T+2,y*T+2,(x+w)*T-3,(y+h)*T-6),8,fill='#61576e',outline='#c4b5fd',width=2)
    d.line((x*T+8,y*T+9,(x+w)*T-9,y*T+9),fill='#827490',width=2)

# Daily work and social groups sit at the arrival-facing edge; quieter work at rear.
for x,y,w,h in [(13,26,3,1),(27,26,3,1),(13,20,4,2),(26,20,4,2),(9,40,3,1),(48,40,3,1)]:
    table(x,y,w,h)
    for sx in range(x,x+w): chair(sx,y+2)
for box in [(4,28,3,3),(36,28,3,3),(37,40,3,3),(54,40,3,3)]:
    block(box);rect(box,'#343d3c','#6e7772')
    x,y,w,h=box
    for dx,dy in [(1,1),(.4,.5),(1.9,1.5)]:
        d.ellipse(((x+dx)*T,(y+dy)*T,(x+dx+1)*T,(y+dy+1)*T),fill='#53675e')
# Thin gold threshold detail, never a text label or a blocking wayfinding object.
d.line((19*T,31*T,25*T,31*T),fill='#e9c74c',width=3)

# Preserve exact four folded paths from the supplied modern mark. Architecture is
# the mark itself, with glass panels bounded by those folds, not a logo sign.
glass = Image.new('RGBA', SIZE)
gd = ImageDraw.Draw(glass)
tree = ET.parse(ROOT/'source/lettermark.svg')
polys = []
colors = [(134,41,252,92),(65,86,246,88),(153,133,226,80),(196,181,253,76)]
for node,color in zip(tree.findall('.//{http://www.w3.org/2000/svg}path'),colors):
    nums = list(map(float,re.findall(r'-?\d+(?:\.\d+)?',node.attrib['d'])))
    points = [(12*T+nums[i]*2,4*T+nums[i+1]*2) for i in range(0,len(nums),2)]
    polys.append(points)
    gd.polygon(points,fill=color)
    gd.line(points+[points[0]],fill=(220,213,247,230),width=4)
    # Horizontal mullions are clipped to each exact glass facet.
    mask=Image.new('L',SIZE);ImageDraw.Draw(mask).polygon(points,fill=255)
    lines=Image.new('RGBA',SIZE);ld=ImageDraw.Draw(lines)
    for y in range(5*T,30*T,2*T):ld.line((12*T,y,31*T,y),fill=(196,181,253,75),width=2)
    lines.putalpha(Image.composite(lines.getchannel('A'),Image.new('L',SIZE),mask))
    glass=Image.alpha_composite(glass,lines);gd=ImageDraw.Draw(glass)

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
logic=Image.new('RGBA',(64,32));logic.save(ROOT/'logic.png')
logicgid=gid;gid+=2
tilesets.append(dict(firstgid=logicgid,name='logic',image='logic.png',imagewidth=64,imageheight=32,tilewidth=32,tileheight=32,tilecount=2,columns=2,tiles=[dict(id=0,properties=[dict(name='collides',type='bool',value=True)])]))
layer('persistent-collision',[logicgid if (x,y) in blocked else 0 for y in range(H) for x in range(W)])
layer('start',[logicgid+1 if (x,y)==(22,34) else 0 for y in range(H) for x in range(W)])
layer('tower-interior',[logicgid+1 if 11<=x<33 and 18<=y<30 else 0 for y in range(H) for x in range(W)])
layers.append(dict(id=len(layers)+1,type='objectgroup',name='floorLayer',x=0,y=0,opacity=1,visible=True,objects=[]))
layer('seat-backs',atlas('seat-backs',backs))
layer('tower-glass-cover',atlas('tower-glass',glass))
mapdata=dict(type='map',version='1.10',tiledversion='1.11.2',orientation='orthogonal',renderorder='right-down',infinite=False,width=W,height=H,tilewidth=T,tileheight=T,nextlayerid=len(layers)+1,nextobjectid=1,layers=layers,tilesets=tilesets,properties=[dict(name='script',type='string',value='runtime.js'),dict(name='mapCopyright',type='string',value='Original BAWES campus architectural blockout; mark supplied by BAWES Universe.')])
(ROOT/'campus.tmj').write_text(json.dumps(mapdata,separators=(',',':'))+'\n')
layout=dict(status='experimental architectural blockout; not gameplay accepted',grid=[W,H,T],spawn=[22,34],entrance=[19,30,6,1],interior=[11,18,22,12],studenthub_reserve=[42,17,17,14],seats=seats,main_route_width_px=192,glass_alpha_range=[76,92],folded_facets=polys)
(ROOT/'source/layout.json').write_text(json.dumps(layout,indent=2)+'\n')
for name,img in [('layout',floor),('outside',Image.alpha_composite(Image.alpha_composite(floor,backs),glass)),('inside',Image.alpha_composite(floor,backs))]:
    img.save(ROOT/'review'/(name+'.png'))
print('Built campus.tmj, separate ground/seat/glass/logic assets and review blockouts.')
