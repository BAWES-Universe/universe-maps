"""Inspect unchanged Tiled data and render atlas composition; not browser evidence."""
from pathlib import Path
import hashlib, json, math
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parent
BASELINE=Path('/workspace/shared/recovered-campus06/public/butterfly-town/v6/gate/map')
GREG=Path('/workspace/shared/recovered-original-assets/map-mocks/civic-rooms-01/source/assets/greg.png')
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
MAP=json.loads((ROOT/'map/gate.tmj').read_text())
W,H=MAP['width']*32,MAP['height']*32
SETS=MAP['tilesets']; IMAGES={s['name']:Image.open(ROOT/'map'/s['image']).convert('RGBA') for s in SETS}
ANIMS={s['firstgid']+t['id']:(s,t['animation']) for s in SETS for t in s.get('tiles',[]) if 'animation' in t}
COLLIDES={s['firstgid']+t['id'] for s in SETS for t in s.get('tiles',[]) if any(p['name']=='collides' and p['value'] for p in t.get('properties',[]))}
BLOCKED={(i%MAP['width'],i//MAP['width']) for l in MAP['layers'] if l['type']=='tilelayer' for i,gid in enumerate(l['data']) if gid&0x0fffffff in COLLIDES}

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def sprite(gid,ms=0):
    flags=gid&0xf0000000; gid &= 0x0fffffff
    if gid in ANIMS:
        source,frames=ANIMS[gid]; tick=ms%sum(f['duration'] for f in frames)
        for f in frames:
            if tick<f['duration']:
                gid=source['firstgid']+f['tileid'];break
            tick-=f['duration']
    ts=next(s for s in reversed(SETS) if s['firstgid']<=gid)
    local=gid-ts['firstgid']; x=(local%ts['columns'])*32;y=(local//ts['columns'])*32
    tile=IMAGES[ts['name']].crop((x,y,x+32,y+32))
    if flags&0x20000000:tile=tile.transpose(Image.Transpose.TRANSPOSE)
    if flags&0x80000000:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if flags&0x40000000:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return tile
def compose(ms=0,greg=False):
    image=Image.new('RGBA',(W,H),MAP['backgroundcolor'])
    for layer in MAP['layers']:
        if layer['type']!='tilelayer' or not layer.get('visible',True):continue
        for index,gid in enumerate(layer['data']):
            if not gid:continue
            tile=sprite(gid,ms)
            if layer.get('opacity',1)!=1:tile.putalpha(tile.getchannel('A').point(lambda p:round(p*layer['opacity'])))
            image.alpha_composite(tile,((index%MAP['width'])*32,(index//MAP['width'])*32))
    if greg:
        sheet=Image.open(ROOT/'assets/greg.png').convert('RGBA')
        image.alpha_composite(sheet.crop((32,96,64,128)),(496-16,1136-16))
    return image
def can_stand(x,y):
    left,right,top,bottom=x-8,x+8,y,y+16
    if left<0 or top<0 or right>W or bottom>H:return False
    return all((col,row) not in BLOCKED for col in range(math.floor(left/32),math.ceil(right/32)) for row in range(math.floor(top/32),math.ceil(bottom/32)))

manifest=[]
for file in [Path('gate.tmj'),*[Path(s['image']) for s in SETS]]:
    source,target=BASELINE/file,ROOT/'map'/file
    manifest.append({'file':str(file),'sha256':digest(target),'baselineSha256':digest(source),'identical':digest(source)==digest(target)})
manifest.append({'file':'assets/greg.png','sha256':digest(ROOT/'assets/greg.png'),'baselineSha256':digest(GREG),'identical':digest(ROOT/'assets/greg.png')==digest(GREG)})
center=[{'x':496,'y':y,'walkable':can_stand(496,y)} for y in range(544,1137)]
boundaries=[]
for y in (1136,960,800,640,560,544):
    valid=[x for x in range(W) if can_stand(x,y)]
    boundaries.append({'y':y,'minX':min(valid),'maxX':max(valid),'onePixelPastLeftBlocked':not can_stand(min(valid)-1,y),'onePixelPastRightBlocked':not can_stand(max(valid)+1,y)})
first=compose(0);next_frame=compose(600)
delta=ImageChops.difference(first,next_frame).convert('RGB')
changed=sum(any(pixel) for pixel in delta.getdata())
first.save(OUT/'baseline-atlas-composite-full.png')
compose(0,True).save(OUT/'baseline-atlas-composite-greg-b-spawn.png')
next_frame.save(OUT/'baseline-atlas-composite-600ms.png')
report={'evidenceType':'Offline Tiled atlas composition and geometric checks. Native browser proof still required.',
 'mapPixels':[W,H],'tileSize':32,'tileLayers':sum(l['type']=='tilelayer' for l in MAP['layers']),
 'tilesets':len(SETS),'animationDefinitions':len(ANIMS),'collisionCells':len(BLOCKED),
 'assetsUnchanged':all(x['identical'] for x in manifest),'manifest':manifest,
 'sourceBodyContract':{'container':[16,16],'containerOrigin':[.5,.5],'offset':[0,8],'childSprite':[32,32],'childOrigin':[.5,.5], 'bodyBoundsRelativeToPlayer':[-8,0,8,16],'equivalent32pxSpriteOffset':[8,16]},
 'centerPath':{'x':496,'fromY':1136,'toY':544,'samples':len(center),'allWalkable':all(p['walkable'] for p in center)},
 'boundaries':boundaries,'upperBoundary':{'y544Walkable':can_stand(496,544),'y543Blocked':not can_stand(496,543)},
 'lowerWorldBoundary':{'y1424Walkable':can_stand(496,1424),'y1425Blocked':not can_stand(496,1425)},
 'visibleCompositeAnimation':{'t0':0,'t1':600,'changedPixels':changed,'passed':changed>0},
 'browserRun':False}
(OUT/'offline-verification.json').write_text(json.dumps(report,indent=2))
assert report['assetsUnchanged'] and report['centerPath']['allWalkable'] and changed>0
assert all(b['onePixelPastLeftBlocked'] and b['onePixelPastRightBlocked'] for b in boundaries)
assert report['upperBoundary']['y543Blocked'] and report['lowerWorldBoundary']['y1425Blocked']
print(json.dumps({k:v for k,v in report.items() if k not in ('manifest',)},indent=2))
