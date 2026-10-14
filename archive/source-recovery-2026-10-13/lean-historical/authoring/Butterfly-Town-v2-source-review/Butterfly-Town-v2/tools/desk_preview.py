"""One review-only TMJ furniture arrangement. Does not alter the map or generator.

The generated PNG's genuine alpha is preserved. Cropping, resizing and splitting
below are deterministic sprite packing, not repainting. Run this module to make
the review assets; call arrangement() from the map generator after review.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art-source/v2/desk-review'
TILE = 32


def packed_sprite(source, box, canvas, max_art):
    art = source.crop(box)
    art.thumbnail(max_art, Image.Resampling.LANCZOS)
    result = Image.new('RGBA', canvas)
    result.alpha_composite(art, ((canvas[0]-art.width)//2, canvas[1]-art.height))
    return result


def arrangement():
    """Return full-room feet/canopy alpha and replacement local collision boxes.

    Replace only studenthub furniture index 0. Keep every other furniture slot.
    Collision is conservative and TMJ-compatible. The chair is parked furniture;
    the reachable work position is standing north of the desk, not sitting.
    """
    source = Image.open(OUT / 'generated-source.png').convert('RGBA')
    desk = packed_sprite(source, (45,161,1040,850), (64,64), (64,48))
    # Same art-to-world scale as the desk (about 0.064); avoid an oversized chair.
    chair = packed_sprite(source, (1124,230,1482,841), (32,64), (32,40))
    feet = Image.new('RGBA', (448,288))
    canopy = Image.new('RGBA', (448,288))
    for sprite, x, y in [(desk,96,128),(chair,64,128)]:
        canopy.alpha_composite(sprite.crop((0,0,sprite.width,32)), (x,y))
        feet.alpha_composite(sprite.crop((0,32,sprite.width,64)), (x,y+32))
    return {
        'desk': desk, 'chair': chair, 'feet': feet, 'canopy': canopy,
        'collisions': [(96,160,64,32),(64,128,32,64)],
        'standing': (128,136),
        'approach': [(224,264),(224,232),(176,232),(176,136),(128,136)],
    }


def review_grid(data):
    m = json.loads((ROOT/'map/butterfly-town.tmj').read_text())
    raw = next(l for l in m['layers'] if l['name']=='permanent-collisions')['data']
    grid = [[bool(raw[(608//32+y)*m['width']+2464//32+x]) for x in range(14)] for y in range(9)]
    # Remove just the old left table-and-four-chairs footprint.
    for x in range(2,5):
        grid[6][x] = False
    for x,y,w,h in data['collisions']:
        for yy in range(y//32,(y+h)//32):
            for xx in range(x//32,(x+w)//32):
                grid[yy][xx] = True
    return grid


def route_exists(grid, start, end):
    queue = deque([start]); seen = {start}
    while queue:
        p = queue.popleft()
        if p == end:
            return True
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            q = (p[0]+dx,p[1]+dy)
            if 0 <= q[0] < 14 and 0 <= q[1] < 9 and not grid[q[1]][q[0]] and q not in seen:
                seen.add(q); queue.append(q)
    return False


def path_body_checks(grid, points):
    """Conservative body offsets used by the existing map tests: x±8,y+8..23."""
    checks = 0
    for (ax,ay),(bx,by) in zip(points, points[1:]):
        steps = max(abs(bx-ax),abs(by-ay))
        for t in range(steps+1):
            x=ax+(bx-ax)*t/max(steps,1); y=ay+(by-ay)*t/max(steps,1)
            for dx in (-8,0,7):
                for dy in (8,16,23):
                    assert not grid[int((y+dy)//32)][int((x+dx)//32)], f'Approach body overlaps collision at {(x,y)}'
            checks += 1
    return checks


def render_review(data):
    ground = Image.open(ROOT/'map/tilesets/studenthub-interior.png').convert('RGBA')
    feet = Image.open(ROOT/'map/tilesets/studenthub-furniture-feet.png').convert('RGBA')
    canopy = Image.open(ROOT/'map/tilesets/studenthub-furniture-canopies.png').convert('RGBA')
    clear = (64,128,160,224)
    feet.paste((0,0,0,0), clear); canopy.paste((0,0,0,0), clear)
    feet.alpha_composite(data['feet']); canopy.alpha_composite(data['canopy'])
    # Exact 32px reference sprite already used in the project's QA; unchanged.
    greg = Image.open(ROOT/'qa/greg.png').convert('RGBA').crop((32,0,64,32))
    frames = []
    for label,position in [('Clear standing approach',(176,136)),('At the work position',data['standing']),('Passing in front',(128,208))]:
        panel = Image.new('RGBA', ground.size, (13,26,31,255))
        panel.alpha_composite(ground); panel.alpha_composite(feet)
        panel.alpha_composite(greg, (position[0]-16,position[1]-16))
        panel.alpha_composite(canopy)
        crop = panel.crop((32,96,224,256)).resize((576,480),Image.Resampling.NEAREST)
        frame = Image.new('RGB',(576,536),(13,26,31)); frame.paste(crop,(0,44))
        draw = ImageDraw.Draw(frame)
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
        draw.text((16,12),label,fill=(255,233,190),font=font)
        frames.append(frame)
    sheet = Image.new('RGB',(1728,576),(13,26,31))
    for i,frame in enumerate(frames): sheet.paste(frame,(i*576,0))
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
    draw.text((16,546),'One desk review • standing workspace; parked chair • unchanged 32px QA character • no sitting behavior',font=font,fill=(211,218,217))
    sheet.save(OUT/'standing-workspace-review.png')
    # Keep a native-size local scene for independent QA / nearest-neighbor zoom.
    native = Image.new('RGBA', ground.size, (13,26,31,255))
    native.alpha_composite(ground); native.alpha_composite(feet); native.alpha_composite(canopy)
    native.save(OUT/'studenthub-one-desk-native.png')
    grid = review_grid(data)
    overlay=native.copy(); draw=ImageDraw.Draw(overlay,'RGBA')
    for y,row in enumerate(grid):
        for x,solid in enumerate(row):
            if solid: draw.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(219,63,69,70),outline=(255,107,113,180))
    draw.line(data['approach'],fill=(77,238,195,255),width=2)
    x,y=data['standing']; draw.ellipse((x-4,y-4,x+4,y+4),fill=(77,238,195,255))
    overlay.resize((896,576),Image.Resampling.NEAREST).save(OUT/'standing-approach-collision-review.png')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    data=arrangement()
    for key,name in [('desk','desk-64x64.png'),('chair','chair-32x64.png'),('feet','replacement-feet.png'),('canopy','replacement-canopy.png')]: data[key].save(OUT/name)
    grid=review_grid(data)
    reachable=route_exists(grid,(7,8),(4,4))
    assert reachable, 'Standing workspace must be reachable from the entrance.'
    assert not grid[4][4] and not grid[4][5], 'Work position and east approach must remain walkable.'
    assert grid[5][3] and grid[5][4], 'Desk support footprint must remain solid.'
    assert not any(grid[6][x] for x in range(2,5)), 'Old blocked front-chair row must be released.'
    body_checks=path_body_checks(grid,data['approach'])
    manifest={
        'scope':'Preview only: replace StudentHub left table group, furniture index 0.',
        'roomOrigin':[2464,608], 'roomSize':[448,288],
        'desk':{'origin':[96,128],'canvas':[64,64],'solid':[96,160,64,32]},
        'chair':{'origin':[64,128],'canvas':[32,64],'solid':[64,128,32,64],'purpose':'Parked chair; not an interactive seat.'},
        'replaceOldCollision':[64,192,96,32],
        'newCollisions':data['collisions'], 'standingCenter':data['standing'],
        'standingWorld':[2592,744], 'intendedFacing':'Down / south toward desk',
        'approachCenters':data['approach'], 'gridConnectivityPassed':reachable,
        'approachBodySamplesPassed':body_checks,
        'depthContract':'Same as TMJ: top32 foreground, bottom32 ground. This deliberately supports a north-side standing workspace; no claim of 360-degree object Y-sorting or sitting.',
        'referenceAvatar':'Existing unchanged qa/greg.png, 32px frame; scale reference, not the owner\'s customized avatar.',
        'runtimeVerification':'Static review only. Integration must still be walked in Phaser and the real fork.'
    }
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    render_review(data)
    print(json.dumps(manifest,indent=2))


if __name__=='__main__': main()
