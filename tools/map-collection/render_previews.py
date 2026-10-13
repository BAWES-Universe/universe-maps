#!/usr/bin/env python3
"""Render a bounded, deterministic scene catalogue from exact recovered Tiled data.

Requires Pillow. No game, browser, network, generated artwork, or source edits.
Renders finite orthogonal maps, inline/JSON external tilesets, authored tile order,
GID transforms, layer/group offsets and opacity, margins/spacing, and animation
frame zero. Unsupported visual constructs fail instead of being approximated.

Tiled reference: https://doc.mapeditor.org/en/stable/reference/global-tile-ids/
                https://doc.mapeditor.org/en/stable/manual/layers/
An earlier recovered map_render.py demonstrated this collection's GID renderer.
This implementation generalizes it and validates every image region used.
"""
import argparse, hashlib, json, math, re
from bisect import bisect_right
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFont, __version__ as pillow_version

BASE = 'archive/runtime-recovery-2026-10-13'
NOTE = ('Static source-rendered scene, using the TMJ initial authored visibility and '
        'the first frame of each Tiled animation. No live game acceptance, runtime '
        'script state, WAM entities, avatars, audio or interaction is established.')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def color(s):
    if not s: return (0, 0, 0, 0)
    if len(s) == 9: return (*ImageColor.getrgb('#'+s[3:]), int(s[1:3],16))
    return ImageColor.getcolor(s, 'RGBA')

def intpos(v):
    if int(v) != v: raise ValueError('Subpixel offset not supported by this source-pixel renderer')
    return int(v)

class Renderer:
    def __init__(self, path, root):
        self.path, self.root = Path(path), Path(root)
        self.m = json.loads(self.path.read_text())
        if self.m.get('orientation') != 'orthogonal' or self.m.get('infinite'):
            raise ValueError('Only finite orthogonal maps are supported')
        self.tw, self.th = self.m['tilewidth'], self.m['tileheight']
        self.size = self.m['width']*self.tw, self.m['height']*self.th
        self.stats = {'rendered_tile_instances':0, 'transparent_tile_instances':0,
                      'animated_tile_instances':0, 'flipped_tile_instances':0,
                      'rendered_layers':[], 'skipped_layers':[], 'non_visual_objects':0}
        self.assets, self.sets, self.cache = {}, [], {}
        self.warnings = []
        self.register(self.path)
        for original in self.m['tilesets']:
            s = dict(original); base = self.path.parent
            if 'source' in s:
                p = (base / s['source']).resolve(); self.register(p)
                s = json.loads(p.read_text()) | {'firstgid':s['firstgid']}; base=p.parent
            if 'image' not in s or not s.get('columns'):
                raise ValueError('Image collection tilesets unsupported')
            p = (base / s['image']).resolve(); self.register(p)
            im = Image.open(p).convert('RGBA')
            if im.size != (s['imagewidth'], s['imageheight']):
                raise ValueError(f"Tileset image size mismatch: {s['image']}")
            s['_image'] = im
            s['_animation'] = {t['id']:t['animation'] for t in s.get('tiles',[]) if 'animation' in t}
            self.sets.append(s)
        self.sets.sort(key=lambda s:s['firstgid'])
        self.firstgids=[s['firstgid'] for s in self.sets]

    def register(self,p):
        p=Path(p).resolve()
        relative=p.relative_to(self.root)
        self.assets[str(Path(BASE)/relative)]={'sha256':sha(p),'bytes':p.stat().st_size}

    def tile(self,raw):
        if raw in self.cache: return self.cache[raw]
        gid=raw & 0x0fffffff
        si=bisect_right(self.firstgids,gid)-1
        if si<0: raise ValueError(f'No tileset for GID {gid}')
        s=self.sets[si]; local=gid-s['firstgid']
        animated=local in s['_animation']
        if animated:
            frames=s['_animation'][local]
            if not frames: raise ValueError('Empty animation')
            local=frames[0]['tileid']
        if local<0 or local>=s['tilecount']: raise ValueError(f'GID {gid} outside tileset')
        tw,th=s['tilewidth'],s['tileheight']; spacing=s.get('spacing',0); margin=s.get('margin',0)
        x=margin+(local%s['columns'])*(tw+spacing); y=margin+(local//s['columns'])*(th+spacing)
        if x+tw>s['_image'].width or y+th>s['_image'].height:
            raise ValueError(f'GID {gid} outside image')
        im=s['_image'].crop((x,y,x+tw,y+th))
        if raw & 0x20000000: im=im.transpose(Image.Transpose.TRANSPOSE)
        if raw & 0x80000000: im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if raw & 0x40000000: im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        off=s.get('tileoffset',{})
        value=(im, intpos(off.get('x',0)), intpos(off.get('y',0)), animated)
        self.cache[raw]=value
        return value

    def layers(self, canvas, layers, ox=0, oy=0, opacity=1, ancestors=''):
        for l in layers:
            label=ancestors+l.get('name','')
            op=opacity*l.get('opacity',1)
            if not l.get('visible',True) or op<=0:
                self.stats['skipped_layers'].append({'name':label,'reason':'authored invisible' if not l.get('visible',True) else 'authored zero opacity'})
                continue
            if l.get('tintcolor') or l.get('blendmode') not in (None,'normal'):
                raise ValueError(f'Unsupported tint or blend mode: {label}')
            if l.get('parallaxx',1)!=1 or l.get('parallaxy',1)!=1:
                raise ValueError(f'Parallax requires a camera definition: {label}')
            lx=ox+intpos(l.get('offsetx',0)); ly=oy+intpos(l.get('offsety',0))
            if l['type']=='group':
                self.layers(canvas,l['layers'],lx+intpos(l.get('x',0))*self.tw,ly+intpos(l.get('y',0))*self.th,op,label+'/')
            elif l['type']=='objectgroup':
                if any('gid' in obj or 'text' in obj for obj in l.get('objects',[])):
                    raise ValueError(f'Visual object layer requires separate renderer: {label}')
                self.stats['non_visual_objects']+=len(l.get('objects',[]))
                self.stats['skipped_layers'].append({'name':label,'reason':'non-visual area/logic objects; no tile or text objects'})
            elif l['type']=='tilelayer':
                data=l['data']; w=l['width']; h=l['height']
                if not isinstance(data,list) or len(data)!=w*h: raise ValueError(f'Invalid tile data: {label}')
                lx+=intpos(l.get('x',0))*self.tw; ly+=intpos(l.get('y',0))*self.th
                order=self.m.get('renderorder','right-down')
                xs=range(w) if order.startswith('right') else range(w-1,-1,-1)
                ys=range(h) if order.endswith('down') else range(h-1,-1,-1)
                visible=0
                for yy in ys:
                    for xx in xs:
                        raw=data[yy*w+xx]
                        if not raw: continue
                        tile,tx,ty,animated=self.tile(raw)
                        if tile.getchannel('A').getextrema()[1]==0:
                            self.stats['transparent_tile_instances']+=1; continue
                        if op!=1:
                            tile=tile.copy(); tile.putalpha(tile.getchannel('A').point(lambda a:round(a*op)))
                        canvas.alpha_composite(tile,(lx+xx*self.tw+tx,ly+(yy+1)*self.th-tile.height+ty))
                        visible+=1
                        self.stats['animated_tile_instances']+=int(animated)
                        self.stats['flipped_tile_instances']+=int(bool(raw&0xe0000000))
                self.stats['rendered_tile_instances']+=visible
                if visible: self.stats['rendered_layers'].append(label)
                else: self.stats['skipped_layers'].append({'name':label,'reason':'empty or fully transparent authored tile pixels'})
            else: raise ValueError(f"Unsupported visual layer type: {l['type']}")

    def render(self):
        canvas=Image.new('RGBA',self.size,color(self.m.get('backgroundcolor')))
        self.layers(canvas,self.m['layers'])
        if not self.stats['rendered_tile_instances']: raise ValueError('No visible source artwork was rendered')
        if max(self.size)>=4096:
            self.warnings.append('Full authored world extent preserved; separated rooms appear small in this overview.')
        if self.stats['animated_tile_instances']:
            self.warnings.append('Animations frozen at the first defined Tiled frame (t=0 ms).')
        return canvas

def group(mid):
    n=re.match(r'N(\d\d)-',mid)
    if n: return 'n-social' if int(n[1])<=17 else ('n-learning' if int(n[1])<=34 else 'n-exploration')
    if mid.startswith('lighthouse-'): return 'story'
    if mid.startswith(('astral-flagship','flagship-glass')): return 'flagship'
    if mid.startswith('timber-'): return 'wellbeing'
    if mid in ('esports-arena-01-runtime','lantern-congress-runtime'): return 'held-events'
    if mid in ('campus-v11','butterfly-town-v2','butterfly-gate-a-v6','butterfly-gate-b-v4','studenthub-connected-workplace-01','social-outdoor-office-02','astral-concourse-lobby-01'): return 'connected-world'
    return 'shared-spaces'

def contact_sheets(records,out):
    groups={}
    for r in records:
        if r['status']=='rendered': groups.setdefault(r['collection_group'],[]).append(r)
    files=[]
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
        bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
        title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',23)
    except OSError: font=bold=title=ImageFont.load_default()
    for g,rows in groups.items():
        cols=min(4,len(rows)); cellw=280; cellh=258; header=88 if cols<=2 else 74
        sheet=Image.new('RGB',(cols*cellw,header+math.ceil(len(rows)/cols)*cellh),(242,245,244)); d=ImageDraw.Draw(sheet)
        d.text((16,12),f"{g.replace('-',' ').title()} | {len(rows)} maps",font=title,fill=(23,38,42))
        if cols<=2:
            d.text((16,43),'Source scenes | Initial authored visibility',font=font,fill=(61,73,76))
            d.text((16,63),'Static, not live acceptance',font=font,fill=(61,73,76))
        else:
            d.text((16,43),'Source scenes | Initial authored visibility | Static, not live acceptance',font=font,fill=(61,73,76))
        for i,r in enumerate(rows):
            x=(i%cols)*cellw; y=header+(i//cols)*cellh
            im=Image.open(out/r['thumbnail']['filename']).convert('RGBA'); im.thumbnail((cellw-16,200),Image.Resampling.LANCZOS)
            sheet.paste(im,(x+(cellw-im.width)//2,y+(200-im.height)//2),im)
            short=r['runtime_id'].removesuffix('-runtime')
            def fit(s,f):
                while d.textbbox((0,0),s,font=f)[2]>cellw-18: s=s[:-2]+'…'
                return s
            d.text((x+9,y+205),fit(short,bold),font=bold,fill=(20,39,43))
            d.text((x+9,y+227),fit(r['name'],font),font=font,fill=(50,61,65))
        p=out/f'contact-{g}.jpg';sheet.save(p,quality=84,subsampling=0,optimize=True)
        files.append({'collection_group':g,'path':f'docs/map-collection/previews/{p.name}','sha256':sha(p),'bytes':p.stat().st_size,'dimensions':list(sheet.size),'map_count':len(rows)})
    return files

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',type=Path,required=True);ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    cat=json.loads(args.catalog.read_text()); records=[]
    for m in cat['maps']:
        tmjs=[p for p in m['entrypoints'] if p.endswith('.tmj')]
        rec={'runtime_id':m['id'],'name':m['name'],'collection_group':group(m['id']),'note':NOTE}
        try:
            if len(tmjs)!=1: raise ValueError(f'Expected one TMJ entrypoint; got {tmjs}')
            path=args.root/m['path']/tmjs[0]
            rec['source_tmj']={'path':f"{BASE}/{m['path']}/{tmjs[0]}",'sha256':sha(path)}
            renderer=Renderer(path,args.root); im=renderer.render()
            rec['source_dimensions']=list(im.size); rec['full_render_rgba_sha256']=hashlib.sha256(im.tobytes()).hexdigest()
            im.thumbnail((480,480),Image.Resampling.LANCZOS)
            opaque=im.getchannel('A').getextrema()[0]==255
            ext='.jpg' if opaque else '.png'; p=args.output/(m['id']+ext)
            if opaque: im.convert('RGB').save(p,quality=86,subsampling=0,optimize=True)
            else: im.save(p,optimize=True)
            rec.update(status='rendered',thumbnail={'filename':p.name,'path':f'docs/map-collection/previews/{p.name}','sha256':sha(p),'bytes':p.stat().st_size,'dimensions':list(im.size),'format':'JPEG' if opaque else 'PNG','resampling':'Lanczos; no crop or color adjustment'},render_stats=renderer.stats,source_assets=renderer.assets,warnings=renderer.warnings)
            print(f"OK {m['id']} {im.size} {p.stat().st_size}",flush=True)
        except Exception as e:
            rec.update(status='failed',thumbnail=None,warnings=[str(e)]);print(f"FAIL {m['id']}: {e}",flush=True)
        records.append(rec)
    by_render={}
    for rec in records:
        if rec['status']=='rendered': by_render.setdefault(rec['full_render_rgba_sha256'],[]).append(rec)
    for duplicates in by_render.values():
        if len(duplicates)>1:
            for rec in duplicates:
                others=[r['runtime_id'] for r in duplicates if r is not rec]
                rec['identical_initial_scene_to']=others
                rec['warnings'].append('Initial static scene is pixel-identical to '+', '.join(others)+'. Runtime behavior may differ.')
    manifest={'schema_version':1,'description':NOTE,'renderer':{'path':'tools/map-collection/render_previews.py','sha256':sha(__file__),'pillow_version':pillow_version,'max_dimension':480,'animation_time_ms':0,'background':'Authored TMJ background; transparent if absent. No added backdrop in individual thumbnails.','reference_docs':['https://doc.mapeditor.org/en/stable/reference/global-tile-ids/','https://doc.mapeditor.org/en/stable/manual/layers/']},'source_catalog_sha256':sha(args.catalog),'summary':{'map_count':len(records),'rendered':sum(r['status']=='rendered' for r in records),'failed':sum(r['status']!='rendered' for r in records),'thumbnail_bytes':sum((r.get('thumbnail') or {}).get('bytes',0) for r in records)},'maps':records,'contact_sheets':contact_sheets(records,args.output)}
    dest=args.output.parent/'preview-manifest.json';dest.write_text(json.dumps(manifest,indent=2)+'\n');print('MANIFEST',dest);print(json.dumps(manifest['summary']))
    if manifest['summary']['failed']: raise SystemExit(1)
if __name__=='__main__': main()
