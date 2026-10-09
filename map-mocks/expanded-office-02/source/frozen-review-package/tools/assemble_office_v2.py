from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import json, math
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'geometry-work/source-coordinate-geometry.json').read_text())
W,H=2496,1408; O=32
P=Image.open(R/'materials/receiver-panel-native-01.png').convert('RGBA')
L={n:Image.new('RGBA',(W,H)) for n in ['floor','environment','rugs','objects','foreground','glass','labels']}
def put(n,im,x,y):L[n].alpha_composite(im,(int(x+O),int(y+O)))
def piece(box):return P.crop(box)
# All pixels below are composited native painted source art. No enlarged bitmap or generated vector decoration.
tile=piece((256,304,384,432))
for ex,ey,ew,eh in [(0,0,1984,1344),(1984,448,448,896)]:
 for y in range(ey,ey+eh,128):
  for x in range(ex,ex+ew,128):
   put('floor',tile.crop((0,0,min(128,ex+ew-x),min(128,ey+eh-y))),x,y)
# Two connected north-facing receiver panels. The interior perimeter strips are omitted to retain the central spine.
put('environment',piece((0,0,928,448)),0,0)
put('environment',piece((64,0,992,448)),1056,0)
put('environment',piece((448,0,576,176)),928,0)
# Common cross-aisle uses the actual painted floor/light receiver, with external walls only at outer ends.
put('environment',piece((0,448,928,704)),0,448)
put('environment',piece((64,448,992,704)),1056,448)
# Continuous central promenade drawn from the authored floor strip, with no interior wall across it.
strip=piece((448,176,576,704))
for y in [176,704,1232]:
 put('environment',strip.crop((0,0,128,min(528,1344-y))),928,y)
# Southern team bays reuse low built-in/cabinet receiver planes, rather than roof-height walls.
for px in [64,544,1056,1536]:
 srcx=96 if px in [64,1056] else 576
 put('environment',piece((srcx,128,srcx+352,448)),px+32,768)
# Native outer wall strips remain continuous along the south bays/foyer.
put('environment',piece((0,32,96,448)),0,704)
put('environment',piece((928,32,992,448)),1920,704)
put('environment',piece((0,448,96,672)),0,1120)
put('environment',piece((928,448,992,672)),1920,1120)
# Use exact workbench/chair assets and keep the growth bay open.
wb=Image.open(R/'art-workbench/assets/workbench-four-empty-native.png').convert('RGBA')
wf=Image.open(R/'art-workbench/assets/workbench-four-foreground-native.png').convert('RGBA')
bench=[]
for pod in D['pods']:
 if pod['kind']!='team-pod':continue
 tx,ty=pod['x']+112,pod['y']+144
 put('objects',wb,tx-64,ty-80);put('foreground',wf,tx-64,ty-80)
 bench.append(dict(team=pod['name'],table=[tx,ty,128,96],seats=[[tx+32,ty-16,'south'],[tx+96,ty-16,'south'],[tx+32,ty+96,'north'],[tx+96,ty+96,'north']]))
# Purposeful informal meeting pockets in the shared cross-aisle, each with a compact carpet and a pair of sofas.
ar=R/'art-reception-lounge/native'
so=Image.open(ar/'sofa.png').convert('RGBA');sf=Image.open(ar/'sofa-foreground.png').convert('RGBA')
cf=Image.open(ar/'coffee-table.png').convert('RGBA');cff=Image.open(ar/'coffee-table-front-occluder.png').convert('RGBA')
rug=Image.open(R/'materials/pod-rug.png').convert('RGBA')
for x in [176,1168]:
 put('rugs',rug.resize((208,192),Image.Resampling.LANCZOS),x-32,472)
 put('objects',so,x,464);put('foreground',sf,x,464)
 put('objects',cf,x+32,560);put('foreground',cff,x+32,560)
 # A true north-facing guest chair completes this small face-to-face conversation group.
 chair=Image.open(R/'art-meeting/assets/chair-north-native.png').convert('RGBA');chairfg=Image.open(R/'art-meeting/assets/chair-north-foreground-native.png').convert('RGBA')
 put('objects',chair,x+56,584);put('foreground',chairfg,x+56,584)
# Foyer: welcome/reception beside the central route and a second relaxed conversation corner.
put('objects',Image.open(ar/'reception.png').convert('RGBA'),1120,1168)
put('foreground',Image.open(ar/'reception-front-occluder.png').convert('RGBA'),1120,1168)
put('rugs',rug.resize((256,224),Image.Resampling.LANCZOS),256,1104)
for x in [304]:
 put('objects',so,x,1104);put('foreground',sf,x,1104)
 put('objects',cf,x+32,1184);put('foreground',cff,x+32,1184)
 put('objects',Image.open(ar/'sofa-north.png').convert('RGBA'),x,1216)
 put('foreground',Image.open(ar/'sofa-north-foreground.png').convert('RGBA'),x,1216)
# Gallery: native clear glazed wall and door openings plus actual four-/six-seat meeting fixtures.
a=R/'art-meeting/assets'
for y in [480,672]:
 put('objects',Image.open(a/'small-four-cardinal-empty-native.png').convert('RGBA'),2144,y)
 put('foreground',Image.open(a/'small-four-cardinal-foreground-native.png').convert('RGBA'),2144,y)
put('objects',Image.open(a/'conference-six-empty-native.png').convert('RGBA'),2144,896)
put('foreground',Image.open(a/'conference-six-foreground-native.png').convert('RGBA'),2144,896)
# Authored gallery receiver has measured visible doors; it replaces the draft vector wall shell.
put('environment',Image.open(R/'materials/gallery-native-02-open-doors.png').convert('RGBA'),1984,448)
# Clear the common-office west connection exactly opposite the visible gallery doorway.
em=Image.new('L',(W,H),255);ImageDraw.Draw(em).rectangle((1920+O,1088+O,1984+O-1,1136+O-1),fill=0)
L['environment'].putalpha(ImageChops.multiply(L['environment'].getchannel('A'),em))
# Glazing itself is a translucent renderer plane; a flattened floor is never placed over Wokas.
gd=ImageDraw.Draw(L['glass'])
for x,y,w,h in [(2112,448,16,112),(2112,640,16,96),(2112,816,16,208),(2112,1120,16,160),(2128,640,272,16),(2128,848,272,16)]:
 gd.rectangle((x+O,y+O-16,x+w+O-1,y+h+O-1),fill=(48,139,145,32))
# Labels are source-native typography, separate from artwork.
dr=ImageDraw.Draw(L['labels']);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for p in D['pods']:
 x=p['x']+p['width']//2+O;y=(400 if p['y']<448 else 1056)+O
 dr.text((x,y),p['name'],font=font,anchor='mm',fill=(24,61,64),stroke_width=2,stroke_fill=(246,224,175))
for text,x,y in [('Welcome · Reception',1200,1296),('Shared lounge',432,1312),('Meeting A',2272,492),('Meeting B',2272,694),('Conference',2272,934)]:
 dr.text((x+O,y+O),text,font=font,anchor='mm',fill=(24,61,64),stroke_width=2,stroke_fill=(246,224,175))
out=Image.new('RGBA',(W,H),(12,32,41,255))
for n in ['floor','environment','rugs','objects']:out.alpha_composite(L[n])
g=Image.open('../universe-native-team-fixture/assets/greg-reference.png').convert('RGBA')
# Only a few unchanged scale fixtures; their duplicated appearance is not a multiplayer claim.
for b in bench[:2]:
 for x,y,f in b['seats']:
  out.alpha_composite(g.crop((32,0 if f=='south' else 96,64,32 if f=='south' else 128)),(x+O-16,y+O-16))
out.alpha_composite(g.crop((32,0,64,32)),(1184+O,1136+O))
for n in ['foreground','glass','labels']:out.alpha_composite(L[n])
for n,im in L.items():im.save(R/'layers'/f'office-v2-{n}.png')
out.save(R/'docs/office-interior-assembly-02-native.png')
out.resize((1248,704),Image.Resampling.LANCZOS).save(R/'docs/office-interior-assembly-02-overview.png')
out.crop((32,32,1056,736)).save(R/'docs/office-two-teams-02-native.png')
(R/'docs/assembly-02-manifest.json').write_text(json.dumps({'status':'full-room source composition, no runtime claim','canvas':[W,H],'translation':[O,O],'nativeReceiver':[1024,704],'benchPlacements':bench,'pending':['precise built-in collision mask','foreground structural alpha','final transition roof treatment','runtime route validation']},indent=2))

