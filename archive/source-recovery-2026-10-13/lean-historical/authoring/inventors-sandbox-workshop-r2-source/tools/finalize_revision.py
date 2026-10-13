from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];M=R/'inventors-sandbox-workshop';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(M/'HEAD-GEOMETRY.json').write_bytes((R/'geometry-checks'/M.name/'independent-checks.json').read_bytes())
l=load(M/'source/layout.json');g=l['collision'];rt=load(M/'NATIVE-ROUTES.json');assert rt['allRoutesPass'];assert not load(M/'HEAD-GEOMETRY.json')['issues']
for s in l['seats']:
 row=next(r for r in rt['rows'] if r['name']==s['name']+' authored-click from spawn');assert row['final']==s['anchor'],(s,row)
assert load(M/'HEAD-GEOMETRY.json')['unreachable_cells']==0
for o in load(M/'source/scenery-footprints.json'):
 x,y,w,h=o['pixelRect'];assert all(g[yy//32][xx//32] for yy in range(y,y+h) for xx in range(x,x+w)),o
for o in load(M/'source/furniture-footprints.json'):
 x,y,w,h=o['rect'];assert all(g[yy//32][xx//32] for yy in range(y,y+h) for xx in range(x,x+w)),o
m=load(M/'map32/map.tmj');assert len([r for r in m['layers'] if r['name']=='floorLayer'])==1
for t in m['tilesets']:assert (M/'map32'/t['image']).is_file()
assert load(M/'map32/map.wam')['mapUrl']=='./map.tmj';assert not any('script'==p['name'] for p in m['properties'])
report=dict(pass_=True,seats=12,allAuthoredTapArrivalsEqualAnchors=True,substantialFurnitureRectanglesProtected=True,allWalkableCellsConnected=True,nativeScale=32,benchSprite=[64,23],stoolSprite=[24,20],collaborationTable=[64,32],liveAV=False,newSeatedAnimation=False,rawPipoyaSheetsRedistributed=False)
(M/'REVISION-VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
# Paired empty/occupied native crops, actual tested authored tap positions.
base=Image.open(R/'geometry-checks'/M.name/'decoded-below.png').convert('RGBA');above=Image.open(R/'geometry-checks'/M.name/'decoded-above.png').convert('RGBA');occupied=base.copy()
for i,s in enumerate(l['seats']):
 p=R/'source-assets'/f'woka-proof-{i%8}.png';w=Image.open(p if p.exists() else R/'source-assets/greg-reference.png').convert('RGBA');x,y=next(r['final'] for r in rt['rows'] if r['name']==s['name']+' authored-click from spawn');row=0 if s['direction']=='south' else 3;occupied.alpha_composite(w.crop((32,row*32,64,row*32+32)),(round(x)-16,round(y)-16))
occupied.alpha_composite(above);occupied.save(M/'review/actual-tap-all-12-native.png');empty=Image.alpha_composite(base,above)
for name,box in [('indoor-bench',(288,336,416,432)),('collaboration',(1088,640,1280,784)),('courtyard-bench',(1056,896,1184,1008))]:
 a=empty.crop(box);b=occupied.crop(box);pair=Image.new('RGBA',(a.width*2+8,a.height),'#27382b');pair.paste(a,(0,0));pair.paste(b,(a.width+8,0));pair.resize((pair.width*3,pair.height*3),Image.Resampling.NEAREST).save(M/'review'/(name+'-empty-occupied-3x.png'))
ov=Image.new('RGBA',empty.size);d=ImageDraw.Draw(ov)
for y,row in enumerate(g):
 for x,v in enumerate(row):
  if v:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(220,35,60,85))
empty.alpha_composite(ov);empty.save(M/'review/collision-overlay.png')

# Inventory annotation and real above-player architecture proof, review-only labels.
inv=Image.alpha_composite(base,above);idraw=ImageDraw.Draw(inv)
for i,o in enumerate(load(M/'source/scenery-footprints.json')):
 x,y,w,h=o['pixelRect'];idraw.rectangle((x,y,x+w-1,y+h-1),outline='#ffdf62',width=2);idraw.text((x+2,y+2),str(i+1),fill='white',stroke_width=1,stroke_fill='black')
inv.save(M/'review/solid-fixture-inventory.png')
behind=base.copy();placement=[]
for i,(x,y,direction) in enumerate([(696,240,0),(824,240,3)]):
 assert all(not g[yy//32][xx//32] for yy in range(y,y+16) for xx in range(x-8,x+8));w=Image.open(R/'source-assets'/f'woka-proof-{i+2}.png').convert('RGBA');behind.alpha_composite(w.crop((32,direction*32,64,direction*32+32)),(x-16,y-16));placement.append(dict(anchor=[x,y],direction=['south','north'][i],bodyOnPavedGround=True,projectingMasonryAbovePlayer=True))
behind.alpha_composite(above);behind.crop((640,192,896,320)).resize((1024,512),Image.Resampling.NEAREST).save(M/'review/north-cap-two-directions-4x.png');(M/'source/architectural-projection-proof.json').write_text(json.dumps(placement,indent=2)+'\n')

(M/'GUIDE.md').write_text('''# Inventor’s Workshop r2\n\nA native32 brick, brass, green and oak workshop with three open creation pads, six indoor workbench places, a four-place collaboration nook and a two-place outdoor workbench. South testing court, west doorway, north terrace and garden landing are connected usable destinations. Side garden paths connect via the visible doors/courtyard; planted bases stay solid. 48×36 tiles /1536×1152 pixels.\n\n## Runtime\nHost map32 together and import map.wam/map.tmj in the Universe editor. No engine changes, scripts, new audio, integrations or service activations. Native bounded LiveKit meeting-area metadata is supplied for the collaboration nook; live multi-user, AV and editor import are untested. Spawn silence is confined to the one start tile. Screens, tools and creation pads are decorative/editor-ready placeholders, not running tools.\n\n## Seats and proof\nAll12 authored taps were replayed through pinned source-derived native pathfinding/movement and land exactly at stool/body anchors. Existing native standing idle frames illustrate occupancy; there is no new seated animation. The primary occupied proof is reconstructed from runtime atlases at actual tested arrival endpoints, not a live game screenshot. Furniture silhouettes are inside their solid tile cells; stools are walkable visual destinations. Every walkable cell is connected; exhaustive head tests cover nine local reference sheets /108 frames.\n\n## Rebuild\nPython3 + Pillow + NumPy and Node.js. Run python tools/build_workshop.py, node tools/verify_native_routes.cjs inventors-sandbox-workshop, python tools/check_head_geometry.py inventors-sandbox-workshop. Generation is not needed for rebuilding. Frozen source masters are included. Build and checks are local; no API, credential or purchase required. Raw Pipoya sheets are deliberately excluded; standard proof falls back to the existing reference avatar, and the derived head-union mask preserves runtime safety. Supply your licensed repository Woka sheets locally for varied preview rebuilding.\n\n## Review limits\nRouting uses pinned unmodified source extracts in a stub scene, not browser/network/physics gameplay. The regular replay return targets the nearest native floor-fit point (spawn Y minus1); independent QA separately verifies true-spawn return behavior. No publication or deployment has occurred.\n''')
prov='''# Asset provenance\n\nWorkshop shell, north garden continuation, workbench, backless stool and compact collaboration table were generated with the built-in image generation tool for this requested revision. The shell retains the approved brick/brass/green inventor theme and main functional arrangement while replacing the oversized baked benches. Frozen generated masters and deterministic sprite sizing are included. Original shell reference is the prior inventor workshop r1; its restyling/scale correction and functional indoor/outdoor expansion were requested.\n\nNative movement fixture is pinned to commit60e7afdc3f96ef32525597cd46bd41175d61a2ef from BAWES-Universe/workadventure-universe. No engine source modified. Existing greg-reference fixture comes from the prior supplied bundle. Review-only varied sprites are repository Pipoya Male/Female01,03,05,07-1. Pipoya permits game usage, not standalone raw asset redistribution; raw sheets are excluded from packages. Occupied scene renders and a derived binary head union are included. DejaVu font license is supplied.\n'''
(R/'ASSET-PROVENANCE.md').write_text(prov);(M/'ASSET-PROVENANCE.md').write_text(prov);(R/'requirements.txt').write_text('Pillow\nnumpy\nreportlab\n')
files=[dict(path=str(p.relative_to(M)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(M.rglob('*')) if p.is_file() and p.name not in ('FREEZE.json','MANIFEST.json')]
(M/'FREEZE.json').write_text(json.dumps(dict(version='inventors-sandbox-workshop-r2',status='Frozen local review candidate; not published',files=files),indent=2)+'\n')
for kind in ['runtime','source']:
 with zipfile.ZipFile(R/f'inventors-sandbox-workshop-r2-{kind}.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in (M/'map32').rglob('*'):
   if p.is_file():z.write(p,('inventors-sandbox-workshop/' if kind=='source' else '')+str(p.relative_to(M)))
  z.write(M/'GUIDE.md',('inventors-sandbox-workshop/' if kind=='source' else '')+'GUIDE.md')
  if kind=='source':
   for folder in ['tools','source-assets']:
    for p in (R/folder).rglob('*'):
     if p.is_file() and '__pycache__' not in str(p) and not p.name.startswith('woka-proof-') and p.name not in ('original-theme-reference.png','workshop-shell-master.png','preview_scale.py'):z.write(p,str(p.relative_to(R)))
   for fn in ['ASSET-PROVENANCE.md','requirements.txt']:z.write(R/fn,fn)
print('FREEZE',sha(M/'FREEZE.json'))
