"""Reconstruct the delivered TMJ's ordinary native Tiled animations, offline.

No generated replacement painting or browser claim. The output resolves the
compiled GIDs, owning layers, and per-frame duration just as a Tiled renderer.
"""
from pathlib import Path
from bisect import bisect_right
from PIL import Image
import hashlib, json, math
import numpy as np

R = Path(__file__).resolve().parents[1]
M = R / 'map32'
O = R / 'docs' / 'timed10'
O.mkdir(exist_ok=True)
m = json.loads((M / 'magical-campus.tmj').read_text())
spec = json.loads((R / 'effects/effects.json').read_text())
T = m['tilewidth']
assert T == m['tileheight'] == 32
atlas = []
for ts in m['tilesets']:
    im = Image.open(M / ts['image']).convert('RGBA')
    animations = {t['id']: t['animation'] for t in ts.get('tiles', []) if 'animation' in t}
    for seq in animations.values():
        assert seq and all(0 <= f['tileid'] < ts['tilecount'] and f['duration'] > 0 for f in seq)
    atlas.append((ts, im, animations))
atlas.sort(key=lambda a: a[0]['firstgid'])
starts = [a[0]['firstgid'] for a in atlas]

def render(box, time_ms):
    l, t, r, b = box
    out = Image.new('RGBA', (r-l, b-t), (12, 32, 41, 255))
    for layer in m['layers']:
        if layer['type'] != 'tilelayer' or not layer.get('visible', True) or layer.get('opacity', 1) == 0:
            continue
        assert layer.get('opacity', 1) == 1, 'Semi-opaque visual layers need explicit compositing'
        assert not layer.get('offsetx', 0) and not layer.get('offsety', 0)
        lim = Image.new('RGBA', out.size)
        for y in range(max(0, t//T), min(m['height'], math.ceil(b/T))):
            for x in range(max(0, l//T), min(m['width'], math.ceil(r/T))):
                gid = layer['data'][y*m['width']+x]
                if not gid:
                    continue
                assert gid < 0x10000000, 'Unexpected transformed GID'
                ts, image, animations = atlas[bisect_right(starts, gid)-1]
                idx = gid-ts['firstgid']
                assert 0 <= idx < ts['tilecount']
                if idx in animations:
                    seq = animations[idx]
                    tick = time_ms % sum(f['duration'] for f in seq)
                    for f in seq:
                        if tick < f['duration']:
                            idx = f['tileid']
                            break
                        tick -= f['duration']
                c = ts['columns']
                tile = image.crop((idx%c*T, idx//c*T, (idx%c+1)*T, (idx//c+1)*T))
                lim.paste(tile, (x*T-l, y*T-t))
        out.alpha_composite(lim)
    return out.convert('RGB')

base = Image.open(R/'layers/campus-base.png').convert('RGBA')
above = Image.open(R/'layers/campus-above.png').convert('RGBA')
reports = []
for e in spec['effects']:
    x, y = e['origin']
    source = [Image.open(R/p).convert('RGBA') for p in e['frames']]
    w, h = source[0].size
    box = (x, y, x+w, y+h)
    durations = e.get('durations', [e['duration']]*len(source))
    times = np.cumsum([0]+durations[:-1]).tolist()
    frames = [render(box, tick) for tick in times]
    for src, compiled in zip(source, frames):
        expected = Image.new('RGBA', (w,h), (12,32,41,255))
        expected.alpha_composite(base.crop(box))
        if e.get('layer','below') == 'below':
            expected.alpha_composite(src)
            expected.alpha_composite(above.crop(box))
        else:
            expected.alpha_composite(above.crop(box))
            expected.alpha_composite(src)
        assert compiled.tobytes() == expected.convert('RGB').tobytes(), e['name']
    pixels = np.stack([np.asarray(f) for f in frames]).astype('int16')
    swing = np.ptp(pixels, axis=0).max(2)
    union = np.stack([np.asarray(f)[:,:,3] for f in source]).max(0)>0
    frames[0].save(O/f"{e['name']}-tmj-native-timed.png", save_all=True,
                   append_images=frames[1:], duration=durations, loop=0)
    for i in [0, len(frames)//2, len(frames)-1]:
        frames[i].save(O/f"{e['name']}-{times[i]:04}ms-native.png")
    reports.append({'name':e['name'], 'origin':[x,y], 'size':[w,h],
        'frames':len(frames), 'distinctVisibleFrames':len({f.tobytes() for f in frames}),
        'loopMs':sum(durations), 'visiblePixelsChangingOver3RGB':int((swing>3).sum()),
        'visiblePixelsChangingOver16RGB':int((swing>16).sum()),
        'abovePixelsOnOwner':int(((np.asarray(above.crop(box))[:,:,3]>0)&union).sum()),
        'nativeSourceToCompiledPixelsIdentical':True})
report = {'scope':'Compiled candidate TMJ GID/layer/duration reconstruction. Offline, no browser or live-room claim.',
    'mapSHA256':hashlib.sha256((M/'magical-campus.tmj').read_bytes()).hexdigest(),
    'effects':reports, 'ordinaryTiledAnimationsValid':True}
full = render((0,0,m['width']*T,m['height']*T), 0)
full.save(R/'docs/Campus10-compiled-native.png')
full.resize((full.width//2,full.height//2), Image.Resampling.LANCZOS).save(R/'docs/Campus10-compiled-half.png')
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
