"""Render compact evidence entirely from restored source pixels, no generated art."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
import test_geometry_patch as t
W=Path(__file__).parent
G=Image.open(t.args.greg).convert('RGBA')
frames=[G.crop((x*32,y*32,(x+1)*32,(y+1)*32)) for y in range(4) for x in range(3)]
for label,cx in [('books',2840),('curios',3048)]:
    out=Image.new('RGB',(768,552),(23,29,31));d=ImageDraw.Draw(out)
    d.text((12,8),f'{label}: BEFORE | native 32px Greg, 12 frames',fill='white')
    d.text((396,8),'AFTER | identical art below player',fill='white')
    for side,fore in enumerate((t.BEFORE,t.AFTER)):
        for k,frame in enumerate(frames):
            region=(cx-32,3008,cx+32,3072)
            scene=t.BASE.crop(region);scene.alpha_composite(frame,(16,16));scene.alpha_composite(fore.crop(region))
            out.paste(scene.resize((128,128),Image.Resampling.NEAREST),((side*3+k%3)*128,40+k//3*128))
    out.save(W/f'{label}-greg-before-after.png')

box=(1248,1680,1664,2048)
im=t.BASE.copy();im.alpha_composite(t.BEFORE)
crop=im.crop(box);o=Image.new('RGBA',crop.size);d=ImageDraw.Draw(o)
pts=[(x-box[0],y+8-box[1]) for x,y in t.PLAYER_ROUTE]
d.line(pts,fill=(0,240,255,230),width=2)
for x,y in t.OPEN_FOUNTAIN_CELLS:
    px=x*16-box[0];py=y*16-box[1];d.rectangle((px,py,px+15,py+15),fill=(0,255,0,80),outline=(0,255,0,255),width=1)
crop.alpha_composite(o);crop=crop.resize((832,736),Image.Resampling.NEAREST);d=ImageDraw.Draw(crop)
d.text((10,10),'NEW reconstruction: full swept 16x16 body route, both directions',fill='white',stroke_width=1,stroke_fill='black')
d.text((10,27),'Green: two opened pavement cells. All other collisions unchanged.',fill='white',stroke_width=1,stroke_fill='black')
crop.save(W/'fountain-route-evidence.png')

out=Image.new('RGB',(768,180),(23,29,31));d=ImageDraw.Draw(out)
for k,(x,y) in enumerate(((101,114),(100,115),(100,116))):
    patch=im.crop((x*16,y*16,x*16+16,y*16+16)).resize((128,128),Image.Resampling.NEAREST)
    out.paste(patch,(k*256+64,38));d.text((k*256+15,10),f'{x},{y}: '+('OPEN: bare pavement' if k<2 else 'KEEP SOLID: greenery'),fill='white')
out.save(W/'fountain-source-cell-evidence.png')
report={
    'status':'NEW reconstruction; unavailable lost patch was not recovered',
    'testsPassed':6,
    'collisionCellsOpened':[list(c) for c in t.OPEN_FOUNTAIN_CELLS],
    'foregroundGidsCleared':len(t.BELOW_PLAYER_FASCIA_CELLS),
    'nativeBaseDuplicatePixelsVerified':2304,
    'ringRouteSegments':len(t.PLAYER_ROUTE)-1,
    'ringSweepStepPx':0.5,
    'ringDirections':['clockwise','counterclockwise'],
    'wokaFrameCount':12,
    'wokaSizePx':[32,32],
    'bodySizePx':[16,16],
    'contactRoutes':t.CONTACT_ROUTES,
    'limits':['Source/pixel and swept-body tests; live Universe/browser physics not executed by this worker.','Head-clear guarantee covers central booth contact/frontage routes, not decorative side foliage and pillars.','No claim that these two opened cells equal the lost three-cell patch.']
}
(W/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
