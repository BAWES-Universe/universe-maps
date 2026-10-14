#!/usr/bin/env python3
"""Build bounded, original code-native gate effects without touching source art.

Every effect is a native 32px Tiled tile animation, and every animation belongs to
one <=1024px atlas. The original TMJ is the immutable input; this script may be
rerun before the separate stage/camera-layout transformation, never after it.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import copy
import hashlib
import json
import math
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'source-inputs'
TILE = 32
ATLAS_TILES = 1024
PREFIX = 'gate-journey-'
TAU = math.tau


@dataclass
class Effect:
    name: str
    frames: list[Image.Image]
    x: int
    y: int
    duration: int
    animated: bool = True
    visible: bool = True
    extra: tuple = ()


def blank(size):
    return Image.new('RGBA', size, (0, 0, 0, 0))


def smoothstep(x):
    x = max(0., min(1., x))
    return x * x * (3 - 2 * x)


def dot(draw, x, y, r, color):
    draw.ellipse((round(x-r), round(y-r), round(x+r), round(y+r)), fill=color)


def butterfly(phase, strength, cool=False):
    """A small original four-wing silhouette, supersampled only downwards."""
    scale = 3
    im = blank((60 * scale, 60 * scale))
    d = ImageDraw.Draw(im)
    cx, cy = 30 * scale, 30 * scale
    spread = 0.22 + 0.78 * abs(math.sin(phase))
    gold = (255, 211, 107) if not cool else (129, 233, 242)
    cream = (255, 246, 198) if not cool else (209, 255, 252)
    alpha = round(222 * strength)
    # Wings have a forward shoulder and tapered tail, rather than two dots.
    for side in (-1, 1):
        def p(x, y): return (cx + side * x * spread * scale, cy + y * scale)
        d.polygon([p(1, 0), p(4, -5.5), p(9, -4), p(8, -.5), p(4, 2)], fill=gold+(alpha,))
        d.polygon([p(1, 1), p(6.3, 1), p(5.2, 5), p(2, 4)], fill=gold+(round(alpha*.8),))
        d.line([p(1, 0), p(7, -3.8)], fill=cream+(alpha,), width=scale)
        d.line([p(1, 1), p(4.2, 3.7)], fill=cream+(round(alpha*.6),), width=scale)
    d.line((cx, cy-3*scale, cx, cy+4*scale), fill=cream+(alpha,), width=2*scale)
    d.line((cx, cy-2*scale, cx-2*scale, cy-5*scale), fill=gold+(round(alpha*.7),), width=scale)
    d.line((cx, cy-2*scale, cx+2*scale, cy-5*scale), fill=gold+(round(alpha*.7),), width=scale)
    return im.resize((60, 60), Image.Resampling.LANCZOS)


def butterfly_path(u, index):
    # Upper lane gets tighter, visibly drawing each arrival toward the aperture.
    lanes = [-80, 68, -32, 108, -103, 36, 2]
    phase = index * 1.73
    x = 512 + lanes[index] * (1-u)**1.2
    x += math.sin(u*TAU*1.55 + phase) * (24*(1-u)+5)
    y = 3000 - 852*u + math.sin(u*TAU*2+phase) * 7 * (1-u)
    return x, y


def make_butterflies():
    frames = []
    origin = (352, 2112)
    n = 96
    for f in range(n):
        im = blank((352, 928))
        light = blank(im.size)
        ld = ImageDraw.Draw(light)
        d = ImageDraw.Draw(im)
        sprites = []
        for i in range(7):
            u = (f/n + i/7) % 1
            fade = smoothstep(u/.065) * smoothstep((1-u)/.085)
            if fade < .004:
                continue
            x, y = butterfly_path(u, i)
            x -= origin[0]; y -= origin[1]
            brightness = (.62 + .38*u) * fade
            cool = i in (2, 5)
            color = (255, 198, 77) if not cool else (91, 222, 240)
            # Short diminishing tails follow the actual route, never a straight
            # screen-space wipe. Each traveler fades before the looping seam.
            for j in range(1, 6):
                pu = max(0, u-j*.0055)
                tx, ty = butterfly_path(pu, i)
                tx -= origin[0]; ty -= origin[1]
                tail_alpha = round((55-j*8) * brightness)
                dot(d, tx, ty, .7 if j > 2 else 1, color+(tail_alpha,))
            dot(ld, x, y, 6 + 2*u, color+(round(40*brightness),))
            sprite = butterfly(f*.79 + i*1.2, brightness, cool)
            # A restrained banking angle supplies natural wing motion.
            angle = math.sin(u*TAU*1.55+i*1.73)*13
            sprite = sprite.rotate(angle, Image.Resampling.BICUBIC)
            sprites.append((sprite, (round(x-30), round(y-30))))
        im = Image.alpha_composite(light.filter(ImageFilter.GaussianBlur(3)), im)
        for sprite, pos in sprites:
            im.alpha_composite(sprite, pos)
        frames.append(im)
    return Effect('gate-butterflies', frames, *origin, 75,
                  extra=(('journeyDurationMs', 'int', 7200),
                         ('direction', 'string', 'arrival-to-portal')))


PORTAL_ORIGIN = (384, 1856)
PORTAL_SIZE = (256, 352)


def aperture_mask():
    # Conservative contour traced INSIDE the inspected original aperture.
    points = [(512,1866),(480,1906),(443,1946),(418,1992),
              (415,2116),(435,2177),(590,2177),(608,2116),
              (607,1992),(580,1946),(544,1906)]
    m = Image.new('L', PORTAL_SIZE)
    ImageDraw.Draw(m).polygon([(x-384,y-1856) for x,y in points], fill=255)
    # Blur inward only; no pixels ever extend outside the conservative contour.
    return ImageChops.multiply(m, m.filter(ImageFilter.GaussianBlur(2)))


def inside_portal(im, mask):
    im.putalpha(ImageChops.multiply(im.getchannel('A'), mask))
    return im


def make_portal_shimmer():
    frames = []
    mask = aperture_mask()
    for f in range(30):
        im = blank(PORTAL_SIZE)
        soft = blank(PORTAL_SIZE)
        d, sd = ImageDraw.Draw(im), ImageDraw.Draw(soft)
        t = f/30
        # Fine upward star streams echo the painted waterfalls and magic veins.
        for i, xx in enumerate((61, 92, 126, 160, 190)):
            u = (t + i*.193) % 1
            y = 313-u*248
            x = xx + math.sin(u*TAU+i)*5
            fade = smoothstep(u/.15)*smoothstep((1-u)/.2)
            a = round(125*fade)
            d.line((round(x),round(y+3),round(x),round(y+21)), fill=(87,230,244,round(a*.32)), width=1)
            d.line((round(x-2),round(y),round(x+2),round(y)), fill=(157,248,246,a), width=1)
            d.line((round(x),round(y-4),round(x),round(y+3)), fill=(197,255,246,a), width=1)
            dot(sd,x,y,4,(74,220,236,round(a*.30)))
        # Gold dust is confined to the aperture, quieter than the live travelers.
        for i in range(6):
            u = (t*.5+i*.142857) % 1
            x = 45 + (i*39)%169 + math.sin(t*TAU+i)*3
            y = 295-u*238
            a = round(85*(.35+.65*math.sin((t+i*.21)*TAU)**2))
            dot(d,x,y,.6,(245,215,126,a))
        im = Image.alpha_composite(soft.filter(ImageFilter.GaussianBlur(2)), im)
        frames.append(inside_portal(im,mask))
    return Effect('gate-portal-shimmer',frames,*PORTAL_ORIGIN,120)


def make_portal_ripples():
    frames=[]
    mask=aperture_mask()
    for f in range(28):
        im=blank(PORTAL_SIZE); d=ImageDraw.Draw(im)
        t=f/28
        for k in range(3):
            u=(t+k/3)%1
            # Water arcs breathe from the painted inner stairs toward the lip.
            y=256+u*67
            rx=13+u*78
            ry=2+u*9
            a=round(104*math.sin(math.pi*u)**1.2)
            d.arc((128-rx,y-ry,128+rx,y+ry),5,174,fill=(118,241,244,a),width=2)
            d.arc((128-rx*.88,y-ry-3,128+rx*.88,y+ry-3),192,312,fill=(181,249,231,round(a*.42)),width=1)
        frames.append(inside_portal(im,mask))
    return Effect('gate-portal-ripples',frames,*PORTAL_ORIGIN,120)


def make_water():
    frames=[]
    # Original painting coordinates at its 960x1440 in-map scale.
    falls=[(168,704,20,52),(150,853,24,58),(175,1092,18,84),
           (137,1304,22,60),(816,700,20,55),(826,850,22,58),
           (792,1089,24,78)]
    for f in range(24):
        im=blank((960,1440));d=ImageDraw.Draw(im)
        for ix,(x,y,w,h) in enumerate(falls):
            for stream in range(max(3,w//5)):
                u=(f/24+stream*.237+ix*.087)%1
                yy=y+u*(h-8)
                a=round(97*math.sin(math.pi*u)**.7)
                xx=x+2+stream*4
                d.line((xx,round(yy),xx,round(yy+7)),fill=(131,226,243,a),width=1)
                d.point((xx,round(yy+2)),fill=(180,245,251,round(a*.7)))
        frames.append(im)
    return Effect('gate-water',frames,32,1664,120)


def make_lanterns():
    # Only four existing large lanterns beside the threshold and upper stairs.
    # This is a low-amplitude amber breathing halo, with no white flash.
    points=[(405,2192),(619,2192),(373,2302),(650,2302)]
    origin=(352,2176);frames=[]
    for f in range(12):
        im=blank((320,160));d=ImageDraw.Draw(im)
        for i,(x,y) in enumerate(points):
            a=round(11+10*(.5+.5*math.sin(f/12*TAU+i*.7)))
            dot(d,x-origin[0],y-origin[1],9,(255,181,68,a))
        frames.append(im.filter(ImageFilter.GaussianBlur(4)))
    return Effect('gate-lantern-pulse',frames,*origin,300)


def make_threshold():
    origin=(384,2144)
    glow=blank((256,160));gd=ImageDraw.Draw(glow)
    gd.ellipse((28,35,229,127),fill=(42,205,221,27))
    gd.ellipse((51,56,207,122),fill=(255,203,94,29))
    glow=glow.filter(ImageFilter.GaussianBlur(12))
    d=ImageDraw.Draw(glow)
    d.arc((37,56,219,128),5,175,fill=(155,246,239,94),width=2)
    d.arc((53,71,204,124),12,170,fill=(255,220,138,111),width=2)
    for x,y in [(68,97),(188,95),(104,79),(157,74)]:
        d.line((x-2,y,x+2,y),fill=(244,232,158,105),width=1)
        d.line((x,y-3,x,y+3),fill=(162,241,231,100),width=1)
    return Effect('gate-threshold-charge',[glow],*origin,0,False,False,
                  (('transitOnly','bool',True),))


class Atlas:
    def __init__(self, number):
        self.number=number
        self.cells=[]
        self.lookup={}
        self.animations=[]

    def key(self,im):
        return hashlib.sha256(im.tobytes()).digest()

    def additions(self,seq,animated):
        # Every animated map cell receives an independent tile definition. The
        # displayed frames, including blank delays, can share pixels locally.
        return len({self.key(im) for im in seq}-{*self.lookup}) + int(animated)

    def add(self,seq,duration,animated):
        ids=[]
        for im in seq:
            key=self.key(im)
            if key not in self.lookup:
                self.lookup[key]=len(self.cells)
                self.cells.append(im)
            ids.append(self.lookup[key])
        if not animated:
            return ids[0]
        start=len(self.cells)
        self.cells.append(seq[0])
        # RLE identical frames preserves total time while avoiding huge blank
        # sequences. It does not stretch the visible motion frames.
        animation=[]
        for local in ids:
            if animation and animation[-1]['tileid']==local:
                animation[-1]['duration']+=duration
            else:
                animation.append({'tileid':local,'duration':duration})
        # AnimatedTiles locates its current frame by looking for the map
        # cell's initial GID inside this sequence. The unique start anchor must
        # therefore be the first frame, not merely an identical spare tile.
        # Its pixels equal seq[0], so the RLE duration remains unchanged.
        animation[0]['tileid']=start
        self.animations.append({'id':start,'animation':animation})
        return start


def tile_sequences(effect):
    first=effect.frames[0]
    for cy in range(math.ceil(first.height/32)):
        for cx in range(math.ceil(first.width/32)):
            rect=(cx*32,cy*32,cx*32+32,cy*32+32)
            seq=[im.crop(rect) for im in effect.frames]
            if not any(im.getchannel('A').getbbox() for im in seq):
                continue
            # Canonical transparent RGB permits the blank hold to be shared.
            for i,im in enumerate(seq):
                if not im.getchannel('A').getbbox():seq[i]=blank((32,32))
            yield effect.x//32+cx,effect.y//32+cy,seq


def build(preview=None):
    source_path=SOURCE/'map/butterfly-campus.tmj'
    source_bytes=source_path.read_bytes()
    original=json.loads(source_bytes)
    result=copy.deepcopy(original)
    effects=[make_water(),make_butterflies(),make_portal_shimmer(),
             make_portal_ripples(),make_lanterns(),make_threshold()]
    atlases=[Atlas(1)]
    firstgid=max(s['firstgid']+s['tilecount'] for s in original['tilesets'])
    records=[]; layer_records=[]; nextid=original['nextlayerid']
    for effect in effects:
        data=[0]*(original['width']*original['height'])
        count=0
        for x,y,seq in tile_sequences(effect):
            assert 0<=x<original['width'] and 0<=y<original['height']
            fit=[a for a in atlases if len(a.cells)+a.additions(seq,effect.animated)<=ATLAS_TILES]
            if fit:
                # Prefer reuse, then fill the fullest compatible atlas.
                atlas=min(fit,key=lambda a:(a.additions(seq,effect.animated),-len(a.cells)))
            else:
                atlas=Atlas(len(atlases)+1);atlases.append(atlas)
            local=atlas.add(seq,effect.duration,effect.animated)
            gid=firstgid+(atlas.number-1)*ATLAS_TILES+local
            data[y*original['width']+x]=gid
            records.append((effect,atlas.number,local,x,y,seq))
            count+=1
        existing=next((l for l in result['layers'] if l['name']==effect.name),None)
        if existing is None:
            existing={'id':nextid,'name':effect.name,'type':'tilelayer',
                      'width':original['width'],'height':original['height'],
                      'x':0,'y':0,'opacity':1}
            nextid+=1
            insertion=next(i for i,l in enumerate(result['layers']) if l['name']=='floorLayer')
            result['layers'].insert(insertion,existing)
        existing['data']=data
        existing['visible']=effect.visible
        existing['properties']=[]
        if effect.animated:
            existing['properties'].append({'name':'reducedMotionHide','type':'bool','value':True})
        existing['properties'] += [{'name':n,'type':t,'value':v} for n,t,v in effect.extra]
        layer_records.append({'name':effect.name,'id':existing['id'],'cells':count,
                              'frames':len(effect.frames),'durationMs':len(effect.frames)*effect.duration,
                              'visible':effect.visible})
    assert len(atlases)<=4, f'Budget exceeded: {len(atlases)} additional atlases, used {[len(a.cells) for a in atlases]}, layers {layer_records}'
    output=ROOT/'map/tilesets';output.mkdir(parents=True,exist_ok=True)
    texture_bytes=0
    for atlas in atlases:
        rows=math.ceil(len(atlas.cells)/32)
        sheet=blank((1024,rows*32))
        for i,cell in enumerate(atlas.cells):sheet.paste(cell,((i%32)*32,(i//32)*32))
        name=PREFIX+f'{atlas.number:02}'
        file='tilesets/'+name+'.png'
        sheet.save(ROOT/'map'/file,optimize=True)
        texture_bytes+=sheet.width*sheet.height*4
        result['tilesets'].append({'firstgid':firstgid+(atlas.number-1)*ATLAS_TILES,
            'name':name,'image':file,'imagewidth':sheet.width,'imageheight':sheet.height,
            'tilewidth':32,'tileheight':32,'columns':32,'tilecount':rows*32,
            'margin':0,'spacing':0,'tiles':atlas.animations})
    result['nextlayerid']=nextid
    target=ROOT/'map/butterfly-campus.tmj'
    target.write_text(json.dumps(result,separators=(',',':')))

    # Verify the immutable base, all old atlases/animation IDs, geometry and all
    # unrelated layer definitions. Decode every generated frame from its atlas.
    assert source_path.read_bytes()==source_bytes, 'Source TMJ changed'
    assert result['tilesets'][:len(original['tilesets'])]==original['tilesets']
    changed={effect.name for effect in effects}
    for layer in original['layers']:
        if layer['name'] not in changed:
            assert next(l for l in result['layers'] if l['id']==layer['id'])==layer,layer['name']
    sheets={a.number:Image.open(output/(PREFIX+f'{a.number:02}.png')).convert('RGBA') for a in atlases}
    decoded_frames=0
    for effect,number,local,x,y,expected in records:
        atlas=atlases[number-1];sheet=sheets[number]
        if effect.animated:
            entry=next(t for t in atlas.animations if t['id']==local)
            # AnimatedTiles.getAnimatedTiles requires a matching initial GID.
            assert entry['animation'][0]['tileid']==local
            assert next(i for i,f in enumerate(entry['animation']) if f['tileid']==local)==0
            assert sum(t['duration'] for t in entry['animation'])==len(expected)*effect.duration
            expanded=[]
            for frame in entry['animation']:
                assert 0<=frame['tileid']<len(atlas.cells)
                assert frame['duration']>0 and frame['duration']%effect.duration==0
                expanded.extend([frame['tileid']]*(frame['duration']//effect.duration))
        else:expanded=[local]
        assert len(expanded)==len(expected)
        for tid,im in zip(expanded,expected):
            left=(tid%32)*32;top=(tid//32)*32
            actual=sheet.crop((left,top,left+32,top+32))
            assert actual.tobytes()==im.tobytes(),(effect.name,number,local,tid)
            decoded_frames+=1
    # Motion is tested on actual pixels, not animation metadata alone.
    motion={}
    for effect in effects:
        if effect.animated:
            hashes={hashlib.sha256(im.tobytes()).hexdigest() for im in effect.frames}
            assert len(hashes)>len(effect.frames)*.7,(effect.name,len(hashes))
            a=effect.frames[0];b=effect.frames[len(effect.frames)//4]
            pixels=sum(1 for p in ImageChops.difference(a,b).getdata() if p!=(0,0,0,0))
            assert pixels>30,effect.name
            motion[effect.name]={'uniqueFrames':len(hashes),'quarterCycleChangedPixels':pixels}
    # The two aperture layers must have zero alpha outside the traced contour.
    mask=aperture_mask()
    exterior=mask.point(lambda v:255 if v==0 else 0)
    for effect in effects:
        if effect.name.startswith('gate-portal-'):
            for im in effect.frames:
                assert not ImageChops.multiply(im.getchannel('A'),exterior).getbbox()
    # Source-to-portal displacement at one second is meaningful at native 1x.
    xa,ya=butterfly_path(.2,0);xb,yb=butterfly_path(.2+1/7.2,0)
    assert ya-yb>100
    report={'sourcePreserved':True,'unchangedLayersVerified':len(original['layers'])-2,
            'legacyTilesetsPreserved':len(original['tilesets']),
            'additionalAtlases':len(atlases),'textureBytesRGBA':texture_bytes,
            'atlasUsedTiles':[len(a.cells) for a in atlases],
            'decodedFramesVerified':decoded_frames,'layers':layer_records,
            'actualPixelMotion':motion,'butterflyPixelsPerSecond':round(math.hypot(xb-xa,yb-ya),2),
            'apertureClippingVerified':True}
    if preview:
        # Optional review files are kept out of the production map directory.
        dest=Path(preview);dest.mkdir(parents=True,exist_ok=True)
        bg=Image.open(SOURCE/'art-source/gate-original.png').convert('RGBA').resize((960,1440),Image.Resampling.LANCZOS)
        for time_ms in (0,1200,2400,3600):
            frame=bg.copy()
            for effect in effects:
                if effect.visible:
                    f=(time_ms//effect.duration)%len(effect.frames)
                    frame.alpha_composite(effect.frames[f],(effect.x-32,effect.y-1664))
            frame.save(dest/f'gate-{time_ms:04}.png')
        # A useful isolated contact sheet makes tiny native sprites inspectable.
        strip=blank((560,100));sd=ImageDraw.Draw(strip)
        for i in range(7):
            glyph=butterfly(i*.55,.9,i in (2,5)).resize((80,80),Image.Resampling.NEAREST)
            strip.alpha_composite(glyph,(i*80,10))
        strip.save(dest/'butterfly-native-design.png')
        (dest/'gate-effects-integrity.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',help='Optional proof output directory outside map assets')
    args=parser.parse_args()
    build(args.preview)
