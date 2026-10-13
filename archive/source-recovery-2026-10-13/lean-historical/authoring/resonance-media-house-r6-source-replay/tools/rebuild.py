from build_maps import *
SLUG='resonance-media-house'
m=Map(SLUG,'Resonance Media House · human scale',768,512,'Media creation / local template','Compact walnut studios, charcoal task seating and listening benches')
m.base=rgba(S/'media-environment-clean-seats-master.png').resize((768,512),Image.Resampling.LANCZOS)
# Architecture and desks are genuinely half-sized in world coordinates; all Wokas remain 32x32.
# Refit the tall boom/tripod lower assembly to a compact studio stand.
# This physically clears the native32 corridor north of the separate planter.
stand=m.base.crop((561,71,608,114));rug=m.base.crop((543,90,558,113)).resize((47,43),Image.Resampling.LANCZOS);m.base.paste(rug,(561,71));m.base.alpha_composite(stand.resize((47,23),Image.Resampling.LANCZOS),(561,71))
# Refit lower cabinet/key-console joinery to the native256px floor line.
# Bodies can now approach the actual fronts without foot overlap.
for x0,x1 in [(64,274),(504,578),(628,698)]:
 lower=m.base.crop((x0,240,x1,270));floor=m.base.crop((x0,270,x1,274)).resize((x1-x0,14),Image.Resampling.LANCZOS)
 m.base.paste(floor,(x0,256));m.base.alpha_composite(lower.resize((x1-x0,16),Image.Resampling.LANCZOS),(x0,240))
# Compact doorway plants so their complete pots end above the256px threshold line.
for x0,x1,top in [(272,293,214),(474,506,204)]:
 plant=m.base.crop((x0,top,x1,278));floor=m.base.crop((320,256,320+x1-x0,278));m.base.paste(floor,(x0,256));m.base.alpha_composite(plant.resize((x1-x0,256-top),Image.Resampling.LANCZOS),(x0,top))
seats=[]
def chair(id,x,y,direction='north',kind='task'):
 if kind=='task':
  a=rgba(S/'industrial-chair40-native.png').resize((32,36),Image.Resampling.LANCZOS);m.base.alpha_composite(a,(x-16,y-17))
 else:
  name='listening-chair-east' if kind=='bench' else 'screen-chair' if kind=='screen' else 'keyboard-stool'
  a=rgba(S/(name+'.png'))
  if direction=='west':a=ImageOps.mirror(a)
  m.base.alpha_composite(a,(x-a.width//2,y-12))
 m.anchor(id,x,y,direction);seats.append(id)
for i,x in enumerate([136,264,376]):chair('editor-'+str(i+1),x,101)
for i,x in enumerate([112,176,240]):chair('screen-viewer-'+str(i+1),x,320,kind='screen')
for i,x in enumerate([560,656]):chair('keyboard-'+str(i+1),x,278,kind='keyboard')
chair('listen-east',552,345,'east','bench');chair('listen-west',652,345,'west','bench')
# Small shared side table serves the two listening benches; not a restaurant table pair.
table=rgba(S/'congress-low-table.png').resize((40,23),Image.Resampling.LANCZOS);m.base.alpha_composite(table,(582,328))
m.anchor('recording-mic',624,111,'west');m.anchor('host',384,271,'south');m.spawn=(384,463)
for id,x,y in [('preview-door',304,271),('music-door',456,271),('recording-door',456,136),('lobby',384,415)]:m.anchor(id,x,y,'north','landmark')
# Only explicitly authored floor cells are admitted. Narrow thresholds are kept at least one native tile.
for b in [(96,96,448,192),(320,160,448,416),(352,400,416,512),(64,272,288,384),(272,272,352,304),(480,272,704,384),(448,272,512,304),(480,96,608,160),(608,96,672,160),(480,128,704,192),(448,128,512,160)]:m.rect(b,False)
# Conservative fixed fixtures and jambs. No off-room floor admitted to make tests pass.
for name,b in [('mic-stand',(576,32,608,96)),('voice-planter',(560,144,592,176)),('preview-north-jamb',(288,192,320,256)),('preview-south-jamb',(272,320,320,400)),('music-north-jamb',(448,192,480,256)),('music-reception',(448,320,544,400)),('west-arrival-door',(312,400,352,464)),('east-arrival-door',(416,400,464,464))]:m.protect(name,b)
m.protect('voice-right-console',(672,128,704,160));m.protect('music-window-corner-planter',(672,352,704,384));m.protect('listening-table',(576,320,640,352));m.rect((64,256,96,288));m.rect((224,256,256,288));m.rect((448,288,480,320))
# Use no false silent room zones: only arrival.
m.quiet[14,11:13]=1
for args in [('editor','Editor / setup',(96,96,432,176),'Unconfigured creative editor'),('voice','Voice / setup',(480,96,688,176),'Recording-themed area; no recorder configured'),('preview','Screen / setup',(64,272,272,384),'Blank screen; media not configured'),('music','Music / setup',(512,272,704,384),'Keyboard and listening area; no synthesis service configured')]:m.zone(*args)
# North context is additive scenery only; interior pixels and every relative coordinate stay exact.
interior=m.base.copy();north=rgba(S/'north-context-generated-master.png').resize((768,608),Image.Resampling.LANCZOS)
m.H=608;m.N=19;m.base=Image.new('RGBA',(768,608));m.base.alpha_composite(north.crop((0,0,768,96)),(0,0));m.base.alpha_composite(interior,(0,96))
m.above=Image.new('RGBA',(768,608));m.foreground_candidate=Image.new('L',(768,608));m.grid=np.pad(m.grid,((3,0),(0,0)),constant_values=1);m.quiet=np.pad(m.quiet,((3,0),(0,0)),constant_values=0)
for a in m.anchors:a['y']+=96
for a in m.areas:a['y']+=96
for a in m.fixtures:
 b=a['solidXYXY'];a['solidXYXY']=(b[0],b[1]+96,b[2],b[3]+96)
m.spawn=(m.spawn[0],m.spawn[1]+96)
# Preview depicts repository-native standing frames at seat anchors, never invented sitting poses.
import os
repo=Path(os.environ.get('WOKA_REPO','/workspace/shared/native32-replan-baseline'))
ws=repo/'play/public/resources/characters/pipoya'
names=['Female 04-1.png','Male 09-4.png','Female 12-1.png','Male 02-3.png','Female 22-1.png','Male 03-3.png','Female 19-4.png','Male 01-4.png','Female 03-3.png','Male 02-4.png']
files=sorted(ws/n for n in names)
def occupied():
 out=m.base.copy();rows={'north':3,'south':0,'west':1,'east':2};assign=[]
 for i,a in enumerate([a for a in m.anchors if a['kind']=='social']+[dict(id='spawn',x=m.spawn[0],y=m.spawn[1],direction='north')]):
  f=files[i%len(files)];im=rgba(f);r=rows[a['direction']];out.alpha_composite(im.crop((32,r*32,64,r*32+32)),(a['x']-16,a['y']-16));assign.append(dict(anchor=a['id'],sheet=f.name,frame=[1,r],nativeFrameSize=[32,32],pose='unchanged repository standing frame'))
 out.save(m.r/'review/occupied-native.png');jw(m.r/'review/occupants.json',assign)
 return out
m.base.save(m.r/'review/empty-native.png');occupied()
if '--preview' not in __import__('sys').argv:
 # Do not widen spawn collision implicitly; the authored two-tile entrance is retained.
 m.anchor('spawn',*m.spawn,'north','spawn');m.partition_foreground();m.base.save(m.r/'source/runtime-base.png');m.above.save(m.r/'source/runtime-above.png')
 jw(m.r/'source/layout.json',dict(title=m.title,category=m.category,style=m.style,world=[m.W,m.H],start=m.spawn,grid=m.grid.tolist(),quiet=m.quiet.tolist(),anchors=m.anchors,areas=m.areas,objects=m.objects,protectedFixtures=m.fixtures,visualSeats=seats))
 m.compile();m.validate();m.render();occupied()
 jw(m.r/'validation/scale.json',dict(originalWorld=[1536,1024],revisedInteriorWorld=[768,512],revisedWorld=[768,608],northContextHeight=96,architectureScale=.5,wokaScale=1,nativeSpriteFrame=[32,32],taskChair=[32,36],visualSeats=len(seats),liveScreenshot=False))
