from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[2];N=R/'native-integration';base=Image.open(R/'layers/garden-base.png').convert('RGBA');old=json.loads((R/'garden-manifest.json').read_text())
# Semantics are architectural, fixed in world coordinates, and independent of avatar pixels.
structures={
'north':{'above':[
 [(430,377),(445,373),(448,407),(444,417),(434,417)],[(540,373),(553,377),(556,417),(544,416)],
 ],'behind':'North backrail and low front seat fascia stay in the base: the backrail is behind the occupant and the fascia is below head/body occlusion height.'},
'south':{'above':[
 [(434,608),(445,607),(448,638),(443,649),(434,646)],[(541,607),(553,610),(554,647),(543,648)],
 [(445,635),(539,635),(547,642),(543,650),(443,650),(438,642)]
 ],'behind':'Seat slats stay below the avatar. The nearer south backrail and arms are fixed foreground.'},
'west':{'above':[
 [(350,475),(360,469),(366,475),(365,555),(359,566),(351,560)],
 [(361,469),(390,470),(397,478),(392,486),(364,486)],
 [(362,554),(391,554),(398,562),(391,570),(362,568)]
 ],'behind':'Seat slats and fire-facing low edge stay in base. Actual outside west back and end arms remain fixed foreground.'},
'east':{'above':[
 [(624,472),(633,475),(635,559),(628,568),(623,557)],
 [(592,469),(622,470),(629,478),(623,486),(592,486)],
 [(592,554),(621,554),(629,562),(622,570),(590,569)]
 ],'behind':'Seat slats and fire-facing low edge stay in base. Actual outside east back and end arms remain fixed foreground.'}}
combined=Image.new('L',(1024,1024),0)
for name,s in structures.items():
 mask=Image.new('L',(1024,1024),0);d=ImageDraw.Draw(mask)
 for p in s['above']:d.polygon(p,fill=255);ImageDraw.Draw(combined).polygon(p,fill=255)
 mask.save(N/f'masks/bench-{name}-fixed-mask.png');im=base.copy();im.putalpha(mask);im.save(N/f'masks/bench-{name}-fixed-foreground.png')
fg=base.copy();fg.putalpha(combined);fg.save(N/'masks/benches-fixed-foreground.png');combined.save(N/'masks/benches-fixed-mask.png')
# Permanent physical structure. Cushion slots and their face-side approaches are always open.
rects={
'north':[(416,360,32,64),(536,360,32,64),(448,368,88,16)],
'south':[(416,600,32,64),(536,600,32,64),(448,640,88,16)],
'west':[(344,448,24,136),(368,448,32,40),(368,552,32,32)],
'east':[(624,448,24,136),(584,448,40,40),(584,552,40,32)]}
obstacles=[o for o in old['obstacles'] if not o['id'].endswith('-bench')]
for name,rs in rects.items():
 for i,(x,y,w,h) in enumerate(rs):obstacles.append({'id':f'{name}-permanent-structure-{i}','type':'rect','x':x,'y':y,'width':w,'height':h})
spots=[
 {'id':'north','facing':'down','spriteRow':0,'approach':{'x':496,'y':432},'position':{'x':496,'y':392}},
 {'id':'south','facing':'up','spriteRow':3,'approach':{'x':496,'y':584},'position':{'x':496,'y':624}},
 {'id':'west','facing':'right','spriteRow':2,'approach':{'x':416,'y':520},'position':{'x':384,'y':520}},
 {'id':'east','facing':'left','spriteRow':1,'approach':{'x':568,'y':520},'position':{'x':608,'y':520}}]
manifest={'format':'riverside-native-static-variant-v1','worldOrigin':old['worldOrigin'],'size':old['nativeSize'],'tileSize':8,'artGrid':32,'avatar':old['avatar'],'entry':old['entry'],'attachment':old['attachment'],'walkable':old['walkable'],'obstacles':obstacles,'spots':spots,'fixedForegroundSemantics':structures,'base':'../layers/garden-base.png','foreground':'masks/benches-fixed-foreground.png','modeDependentCollision':False,'avatarDependentMasking':False,'sittingAnimation':False,'status':'awaiting exact grid/pixel tests','sourceArtSha256':hashlib.sha256((R/'layers/garden-base.png').read_bytes()).hexdigest()}
(N/'native-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
