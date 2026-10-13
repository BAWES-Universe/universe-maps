from pathlib import Path
from PIL import Image, ImageDraw
import compiler as b
import json, hashlib
R=Path(__file__).resolve().parents[1]
b.C,b.N,b.W,b.H=24,19,768,608
m=b.Map('timber-movement-studio-r1','Timber Movement Studio','Activity / open class',b.P)
original=Image.open(R/'source-assets/movement-concept-original.png').convert('RGBA')
north=Image.open(R/'source-assets/timber-north-context.png').convert('RGBA')
m.base=Image.new('RGBA',(768,608));m.base.paste(north.resize((768,96),Image.Resampling.LANCZOS),(0,0));m.base.paste(original.resize((768,512),Image.Resampling.LANCZOS),(0,96));m.d=ImageDraw.Draw(m.base)
m.above=Image.new('RGBA',(768,608));m.a=ImageDraw.Draw(m.above);m.spawn=(12,17)
# Whole tile conservative clear floor, keeping all projected walls, pots, rails and stage solid.
for r in [(10,6,4,1),(4,7,16,6),(3,9,18,4),(3,13,4,1),(9,13,6,1),(17,13,2,1),(11,14,2,1),(11,15,2,4)]:m.block(*r,0)
# Native-position participants use genuine idle poses, not authored dancing animation.
for name,x,y in [('instructor position',12,6),('west front participant',7,9),('center front participant',11,9),('east front participant',16,9),('west rear participant',7,11),('center rear participant',11,11),('east rear participant',16,11),('barre approach',4,11),('storage approach',19,10),('arrival threshold',12,14),('arrival',12,17),('waiting bench approach',18,13)]:m.anchor(name,x,y)
m.zone('Instructor front',10,6,4,2,'speaker')
m.zone('Open movement floor',5,8,14,5,'listener')
m.zone('Arrival conversation',10,13,5,2)
m.cropboxes=[('classroom',(96,176,672,448)),('entry',(224,416,544,608)),('waiting',(544,352,768,544))]
# Depth is derived from the source art, preserving the empty composite exactly.
import numpy as np
art=np.array(m.base); candidate=Image.new('L',m.base.size);d=ImageDraw.Draw(candidate)
for polygon in [
 [(30,200),(78,180),(94,213),(75,272),(45,315),(10,321)],
 [(0,364),(36,360),(55,397),(40,443),(0,450)],
 [(695,209),(725,177),(755,202),(768,408),(739,406),(727,360)],
 [(250,482),(287,480),(303,516),(290,549),(261,548)],
 [(473,481),(505,481),(522,533),(481,550)],
 [(272,150),(308,151),(309,194),(279,194)],
 [(458,151),(493,151),(496,196),(461,195)]
]:d.polygon(polygon,fill=255)
# Exhaustively remove any candidate pixel that could cover a reachable native upper head.
g=np.array(m.g);blocked=g.repeat(32,0).repeat(32,1);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));Y,X=np.indices(blocked.shape);xa=np.maximum(0,X-8);xb=np.minimum(768,X+8);yb=np.minimum(608,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=768)&(Y+16<=608)
head=np.array(json.loads((R/'source-assets/native-head-union.json').read_text())['mask'],bool)
unsafe=np.zeros((608,768),bool)
for yy,xx in np.argwhere(head):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(768,768-dx);y0=max(0,-dy);y1=min(608,608-dy);unsafe[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
safe=(np.array(candidate)>0)&~unsafe;lo=art.copy();hi=np.zeros_like(lo);hi[safe]=lo[safe];lo[safe]=0;m.base=Image.fromarray(lo);m.above=Image.fromarray(hi)
assert Image.alpha_composite(m.base,m.above).tobytes()==Image.fromarray(art).tobytes()
m.finish()
out=R/m.slug
# Replace compiler's reference-only occupancy with unchanged varied repository Wokas.
base=m.base.copy();base.alpha_composite(Image.open(R/'source-assets/occupied-proof-overlay.png').convert('RGBA'));base.alpha_composite(m.above)
base.save(out/'review/occupied-native.png');base.save(out/'review/overview.png')
for name,box in m.cropboxes:base.crop(box).save(out/'review'/f'{name}-occupied-native.png')
(R/'preview').mkdir(exist_ok=True);base.save(R/'preview/first-preview.png')
(out/'source/WOKA-PROOF.json').write_bytes((R/'source-assets/WOKA-PROOF.json').read_bytes())
# Actual native anchor reaches the supported dais front edge, without teleport or focus.
layout=json.loads((out/'source/layout.json').read_text());layout['anchors'][0].update(anchor=[400,192],floorClick=[400,208]);b.js(out/'source/layout.json',layout)
wam=json.loads((out/'map32/map.wam').read_text())
for a in wam['areas']:
 for prop in a['properties']:
  if prop['type']=='livekitRoomProperty':prop['livekitRoomConfig']['startWithVideoMuted']=True
b.js(out/'map32/map.wam',wam)
b.js(out/'DEPTH-PROOF.json',dict(sourceCompositeExact=True,nativeBodyClearPositions=int(clear.sum()),safeForegroundPixels=int(safe.sum()),unsafeCandidatePixelsRetainedBelow=int(((np.array(candidate)>0)&unsafe).sum()),headMask='Union of upper14 rows of all12 directional frames from11 varied actual repository Wokas',bench='Solid scenery with clear approach; no seating claim',dais='Supported front edge reached by actual native anchor [400,192]',world=[768,608],sourceUniformScale=0.5,originalConceptPreserved=True))

(out/'GUIDE.md').write_bytes((R/'GUIDE.md').read_bytes())
files=[]
for folder in ['assets','map32','source','review']:
 for p in sorted((out/folder).rglob('*')):
  if p.is_file():files.append(dict(path=str(p.relative_to(out)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
for name in ['GUIDE.md','DEPTH-PROOF.json','VALIDATION.json']:
 p=out/name;files.append(dict(path=name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
b.js(out/'MANIFEST.json',dict(slug=m.slug,title=m.title,nativeTileSize=32,world=[768,608],status='Unpublished source/static candidate; independent review and user acceptance separate',files=files))
