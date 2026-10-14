# Bundled author replay of project QA decoder/head-mask algorithm. Independent review is separate.
#!/usr/bin/env python3
"""Read-only finite orthogonal TMJ source/static audit. Writes only the QA output.
Unsupported map features fail closed; this is deliberately not a Phaser renderer.
"""
from pathlib import Path
from collections import deque
import argparse, hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def props(o): return {p['name']: p['value'] for p in o.get('properties', [])}
def load_map(path, shown=(), hidden=()):
    path=Path(path).resolve(); m=json.loads(path.read_text())
    assert not m.get('infinite') and m.get('orientation','orthogonal')=='orthogonal', 'Only finite orthogonal TMJ supported'
    assert m['tilewidth']==m['tileheight']==32, 'Native fixture requires 32px map tiles'
    W,H=m['width'],m['height']; ts=[]; provenance={str(path):sha(path)}
    for entry in m['tilesets']:
        t=dict(entry); base=path.parent
        if 'source' in t:
            q=(base/t['source']).resolve(); provenance[str(q)]=sha(q); t={**json.loads(q.read_text()),'firstgid':t['firstgid']}; base=q.parent
        assert t.get('columns',0)>0 and 'image' in t, 'Image collection tilesets need a dedicated decoder'
        assert t['tilewidth']==t['tileheight']==32 and not t.get('tileoffset'), 'Unsupported tileset geometry'
        p=(base/t['image']).resolve(); provenance[str(p)]=sha(p); t['_image']=Image.open(p).convert('RGBA')
        t['_props']={i['id']:props(i) for i in t.get('tiles',[])}
        assert not any(i.get('animation') for i in t.get('tiles',[])), 'Animated tiles require explicit frame audit'
        ts.append(t)
    ts.sort(key=lambda t:t['firstgid']); grid=np.zeros((H,W),bool); layers=[]
    def flatten(items, visible=True, opacity=1):
        for l in items:
            assert not l.get('offsetx') and not l.get('offsety') and not l.get('x') and not l.get('y'), 'Layer offsets need a dedicated audit'
            v=(l.get('visible',True) and visible) if l['name'] not in shown else True
            if l['name'] in hidden:v=False
            a=opacity*l.get('opacity',1)
            if l['type']=='group': yield from flatten(l['layers'],v,a)
            else:yield l,v,a
    all_layers=list(flatten(m['layers'])); names={l['name'] for l,_,_ in all_layers}
    assert not (set(shown)|set(hidden))-names, 'Unknown visibility state layer'
    above=False; foreground=Image.new('RGBA',(W*32,H*32)); canvas=foreground.copy()
    for l,v,opacity in all_layers:
        if l['name']=='floorLayer':above=True
        if l['type']!='tilelayer':
            assert l['type']=='objectgroup', 'Unsupported visible image layer'
            continue
        assert isinstance(l['data'],list) and len(l['data'])==W*H, 'Compressed/chunked or differently sized tile layer unsupported'
        art=Image.new('RGBA',canvas.size)
        for idx,gid in enumerate(l['data']):
            if not gid:continue
            assert gid < (1<<29), 'Flipped tile flags require explicit decoder support'
            t=next((t for t in reversed(ts) if t['firstgid']<=gid),None); assert t is not None
            k=gid-t['firstgid']; assert 0<=k<t['tilecount'], 'Tile ID beyond tileset range'
            if v and (props(l).get('collides') is True or t['_props'].get(k,{}).get('collides') is True):grid[idx//W,idx%W]=True
            if not v or opacity==0:continue
            margin=t.get('margin',0); step=32+t.get('spacing',0)
            x=margin+(k%t['columns'])*step;y=margin+(k//t['columns'])*step
            assert x+32<=t['_image'].width and y+32<=t['_image'].height
            tile=t['_image'].crop((x,y,x+32,y+32));art.alpha_composite(tile,(idx%W*32,idx//W*32))
        if opacity!=1:art.putalpha(art.getchannel('A').point(lambda a:round(a*opacity)))
        if v and opacity:
            canvas=Image.alpha_composite(canvas,art)
            if above:foreground=Image.alpha_composite(foreground,art)
            layers.append((l,art))
    return m,grid,canvas,foreground,layers,provenance

def body_clear(g,x,y):
    h,w=g.shape; e=1e-7
    if x-8 < 0 or x+8>w*32 or y<0 or y+16>h*32:return False
    return not g[math.floor((y+e)/32):math.floor((y+16-e)/32)+1,math.floor((x-8+e)/32):math.floor((x+8-e)/32)+1].any()

def trace(g,points):
    if len(points)<2:raise ValueError('A visible path needs at least two distinct origins')
    if not all(len(p)==2 and all(math.isfinite(v) for v in p) for p in points):raise ValueError('Invalid path origin')
    bad=[];samples=0
    for a,b in zip(points,points[1:]):
        n=max(1,math.ceil(math.dist(a,b)/.5))
        for i in range(n+1):
            p=[a[k]+(b[k]-a[k])*i/n for k in (0,1)];samples+=1
            if not body_clear(g,*p) and len(bad)<12:bad.append(p)
    return {'samples':samples,'pass':not bad,'first_blocked_origins':bad}

def body_origins(g):
    blocked=g.repeat(32,0).repeat(32,1);h,w=blocked.shape
    ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)))
    y,x=np.indices((h,w));l=np.maximum(0,x-8);r=np.minimum(w,x+8);b=np.minimum(h,y+16)
    return (ii[b,r]-ii[y,r]-ii[b,l]+ii[y,l]==0)&(x>=8)&(x+8<=w)&(y+16<=h)

def head_audit(g,fg,mask_file):
    mask=np.asarray(json.loads(Path(mask_file).read_text())['mask'],bool);clear=body_origins(g)
    if mask.ndim!=2 or mask.shape[1]!=32 or not(1<=mask.shape[0]<=32) or not mask.any():raise ValueError('Expected nonempty pinned native32-width head union; height may be the documented head-only rows')
    alpha=np.asarray(fg)[:,:,3];h,w=alpha.shape;max_alpha=0;hits=np.zeros_like(clear);examples=[]
    for yy,xx in np.argwhere(mask):
        dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(w,w-dx);y0=max(0,-dy);y1=min(h,h-dy)
        a=alpha[y0+dy:y1+dy,x0+dx:x1+dx];c=clear[y0:y1,x0:x1]
        if c.any():max_alpha=max(max_alpha,int(a[c].max()))
        hits[y0:y1,x0:x1]|=c&(a>0)
    for y,x in np.argwhere(hits)[:12]:examples.append([int(x),int(y)])
    return {'body_clear_integer_origins':int(clear.sum()),'head_mask_pixels':int(mask.sum()),'origins_with_any_foreground_alpha':int(hits.sum()),'max_foreground_alpha':max_alpha,'first_origins':examples,'pass':not hits.any(),'head_mask_sha256':sha(mask_file),'scope':'Exhaustive integer-origin mask intersection, supplied pinned native32 head union; no runtime character pose/render claim. Any alpha is reported; accepted translucent canopies require explicit separate visual exception.'}
