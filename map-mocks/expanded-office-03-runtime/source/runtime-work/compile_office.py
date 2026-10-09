"""Lossless native-pixel TMJ compiler. Only writes compiled-work and runtime-work.

Art geometry stays in native pixels; 16px cells preserve exact workbench edges.
The collision input is authoritative geometry, never inferred from an art alpha.
"""
from pathlib import Path
from PIL import Image, ImageChops
import argparse
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'compiled-work'
CELL = 16
W, H = 2496, 1408
COLS, ROWS = W // CELL, H // CELL
LAYER_ORDER = ['floor', 'environment', 'rugs', 'objects', 'foreground', 'glass', 'overhead-shade', 'labels']


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (OUT / name).write_text(json.dumps(value, separators=(',', ':')) + '\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def properties(**values):
    return [{'name': k, 'type': 'bool' if isinstance(v, bool) else 'int' if isinstance(v, int) else 'string', 'value': v} for k, v in values.items()]


def tilelayer(name, data, ident, **kw):
    return dict(id=ident, name=name, type='tilelayer', x=0, y=0, width=COLS, height=ROWS,
                visible=True, opacity=1, data=data, **kw)


def pack_layer(name, firstgid):
    source = ROOT / 'layers' / f'office-v2-{name}.png'
    art = Image.open(source).convert('RGBA')
    if art.size != (W, H):
        raise ValueError(f'{source}: expected {(W,H)}, found {art.size}')
    cells, by_bytes, data = [], {}, []
    for y in range(0, H, CELL):
        for x in range(0, W, CELL):
            cell = art.crop((x, y, x + CELL, y + CELL))
            if cell.getchannel('A').getbbox() is None:
                data.append(0)
                continue
            blob = cell.tobytes()
            if blob not in by_bytes:
                by_bytes[blob] = len(cells)
                cells.append(cell)
            data.append(firstgid + by_bytes[blob])
    atlas_cols = min(64, max(1, len(cells)))
    atlas_rows = max(1, math.ceil(len(cells) / atlas_cols))
    atlas = Image.new('RGBA', (atlas_cols * CELL, atlas_rows * CELL))
    for i, cell in enumerate(cells):
        atlas.paste(cell, ((i % atlas_cols) * CELL, (i // atlas_cols) * CELL))
    atlas_path = OUT / f'office-{name}-atlas.png'
    atlas.save(atlas_path)
    reconstructed = Image.new('RGBA', (W, H))
    for i, gid in enumerate(data):
        if gid:
            reconstructed.paste(cells[gid-firstgid], ((i % COLS)*CELL, (i//COLS)*CELL))
    # Transparent RGB bytes do not affect rendering; compare composited RGBA pixels.
    back = Image.new('RGBA', (W, H), (12, 32, 41, 255))
    if ImageChops.difference(Image.alpha_composite(back, art).convert('RGB'), Image.alpha_composite(back, reconstructed).convert('RGB')).getbbox():
        raise AssertionError(f'Native pixel round-trip mismatch in {name}')
    ts = dict(firstgid=firstgid, name=f'office-{name}', image=atlas_path.name,
              imagewidth=atlas.width, imageheight=atlas.height, tilewidth=CELL, tileheight=CELL,
              margin=0, spacing=0, columns=atlas_cols, tilecount=len(cells))
    info = dict(source=str(source.relative_to(ROOT)), sha256=digest(source), occupiedCells=sum(bool(v) for v in data),
                distinctCells=len(cells), atlas=atlas_path.name, nativePixelRoundTrip=True)
    return ts, data, info


def translated(value, dx, dy):
    if isinstance(value, list):
        return [translated(v, dx, dy) for v in value]
    if isinstance(value, dict):
        result = {k: translated(v, dx, dy) for k, v in value.items()}
        if 'x' in result and 'y' in result and isinstance(result['x'], (int, float)) and isinstance(result['y'], (int, float)):
            result['x'] += dx
            result['y'] += dy
        return result
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--geometry-dir', type=Path, default=ROOT/'geometry-work/revision-02')
    parser.add_argument('--collision-grid', type=Path)
    parser.add_argument('--collision-full-canvas', action='store_true')
    parser.add_argument('--extra-obstacles', type=Path, help='JSON list, or object containing rectangles; coordinates in unshifted source geometry')
    parser.add_argument('--final', action='store_true', help='Only use after the source author confirms geometry/art freeze')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    geom_path = args.geometry_dir / 'source-coordinate-geometry.json'
    geometry = read(geom_path)
    grid_path = args.collision_grid or args.geometry_dir / 'collision-grid.json'
    grid = read(grid_path)
    if grid['tileSize'] != CELL:
        raise ValueError('Exact 16px collision cells required; no rounding from a different grid is allowed')
    blocked = [1] * (COLS * ROWS)
    gx, gy = (0, 0) if args.collision_full_canvas else (2, 2)
    source_blocked = set(grid['blockedIndices'])
    for y in range(grid['height']):
        for x in range(grid['width']):
            if not 0 <= x+gx < COLS or not 0 <= y+gy < ROWS:
                raise ValueError('Collision grid exceeds final finite map')
            blocked[(y+gy)*COLS+x+gx] = int(y*grid['width']+x in source_blocked)
    extras=[]
    if args.extra_obstacles:
        extra_data=read(args.extra_obstacles)
        extras=extra_data if isinstance(extra_data,list) else extra_data['rectangles']
        for r in extras:
            vals=[r[k] for k in ('x','y','width','height')]
            if any(v % CELL for v in vals):
                raise ValueError(f'Unaligned obstacle requires source correction, not collider rounding: {r}')
            x,y,w,h=vals
            for yy in range((y+32)//CELL,(y+32+h)//CELL):
                for xx in range((x+32)//CELL,(x+32+w)//CELL):
                    blocked[yy*COLS+xx]=1
    layers, tilesets, audit = [], [], []
    gid=1
    for name in LAYER_ORDER:
        if name=='foreground':
            layers.append(dict(id=len(layers)+1,name='floorLayer',type='objectgroup',x=0,y=0,opacity=1,visible=True,objects=[],draworder='topdown'))
        ts,data,info=pack_layer(name,gid)
        layers.append(tilelayer(f'office-{name}',data,len(layers)+1))
        tilesets.append(ts); audit.append(info); gid+=ts['tilecount']
    collision_gid=gid
    Image.new('RGBA',(CELL,CELL),(225,39,96,100)).save(OUT/'collision-cell.png')
    tilesets.append(dict(firstgid=collision_gid,name='exact-collision',image='collision-cell.png',imagewidth=CELL,imageheight=CELL,
                         tilewidth=CELL,tileheight=CELL,margin=0,spacing=0,columns=1,tilecount=1,
                         tiles=[dict(id=0,properties=properties(collides=True))]))
    collision=tilelayer('collision-permanent', [collision_gid if v else 0 for v in blocked],len(layers)+1)
    collision['opacity']=0
    collision['properties']=properties(collisionIndependentOfRoof=True,source='Authoritative 16px geometry cells')
    layers.insert(4,collision)
    for i,l in enumerate(layers):l['id']=i+1
    status='final source freeze' if args.final else 'provisional: source author has not frozen all art and geometry'
    tilemap=dict(compressionlevel=-1,height=ROWS,width=COLS,infinite=False,layers=layers,nextlayerid=len(layers)+1,nextobjectid=1,
                 orientation='orthogonal',renderorder='right-down',tiledversion='1.11.2',tileheight=CELL,tilewidth=CELL,
                 tilesets=tilesets,type='map',version='1.10',backgroundcolor='#0c2029',
                 properties=properties(nativeWorldWidth=W,nativeWorldHeight=H,artScale=1,wokaScale=1,collisionCellSize=CELL,status=status))
    write('studenthub-expanded-office.tmj',tilemap)
    write('collision-grid.json',dict(width=COLS,height=ROWS,tileSize=CELL,blockedIndices=[i for i,v in enumerate(blocked) if v],status=status))
    # Source metadata is carried for route/capture QA only; it creates no claims or entities.
    runtime_geometry=translated({k:geometry[k] for k in ('workbenches','stations','pods','rooms','doorOpenings','goals','checkpoints') if k in geometry},32,32)
    entry=next((p for p in runtime_geometry.get('checkpoints',[]) if p['id']=='main-entrance'),{'x':1024,'y':1328})
    runtime_geometry.update(world=[W,H],translation=[32,32],status=status,spawn={'x':entry['x'],'y':entry['y']},
                            body={'x':-8,'y':0,'width':16,'height':16},frame=[32,32],scale=1)
    write('runtime-geometry.json',runtime_geometry)
    manifest=dict(status=status,world=[W,H],tileSize=CELL,grid=[COLS,ROWS],wokaFrame=[32,32],wokaScale=1,
                  translation=[32,32],geometrySource=str(geom_path.relative_to(ROOT)),geometrySha256=digest(geom_path),
                  collisionSource=str(grid_path.relative_to(ROOT)),collisionSha256=digest(grid_path),extraObstacles=extras,
                  blockedCells=sum(blocked),tileCount=gid,layerAudit=audit,
                  noArtRescaling=True,noColliderRounding=True,noPreviewRectangleBodies=True,
                  scope='Finite native-pixel TMJ and Phaser 3.86 source harness. No live Universe, multiplayer, claims, bot or conference-service assertion.')
    write('compile-manifest.json',manifest)
    print(json.dumps({k:manifest[k] for k in ('status','world','tileSize','blockedCells','tileCount','noArtRescaling')},indent=2))


if __name__=='__main__':main()
