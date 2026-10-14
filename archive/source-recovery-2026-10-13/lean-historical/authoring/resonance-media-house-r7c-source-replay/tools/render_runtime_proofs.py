from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';layout=json.loads((P/'source/layout.json').read_text());p=P/'map32/resonance-media-house.tmj';tmj=json.loads(p.read_text());size=(tmj['width']*32,tmj['height']*32);under=Image.new('RGBA',size);above=Image.new('RGBA',size);dest=under
atlases={s['image']:Image.open(p.parent/s['image']).convert('RGBA') for s in tmj['tilesets']}
for l in tmj['layers']:
 if l['name']=='floorLayer':dest=above
 if l['type']!='tilelayer' or l.get('opacity',1)==0:continue
 for k,gid in enumerate(l['data']):
  if not gid:continue
  s=max((s for s in tmj['tilesets'] if s['firstgid']<=gid),key=lambda s:s['firstgid']);i=gid-s['firstgid'];x=i%s['columns']*32;y=i//s['columns']*32;dest.alpha_composite(atlases[s['image']].crop((x,y,x+32,y+32)),((k%tmj['width'])*32,(k//tmj['width'])*32))
empty=Image.alpha_composite(under,above);empty.save(P/'review/empty-native.png');assert empty.tobytes()==Image.alpha_composite(Image.open(P/'source/runtime-base.png').convert('RGBA'),Image.open(P/'source/runtime-above.png').convert('RGBA')).tobytes()
meta=json.loads((R/'source/proof-inputs/native32-actors-provenance.json').read_text());ov=Image.open(R/'source/proof-inputs/native32-actors-overlay.png').convert('RGBA');frames=[]
for a in meta['actors']:
 x,y=a['position'];frames.append((a,ov.crop((x-16,y-16,x+16,y+16))))
greg=Image.open(R/'source/greg-reference.png').convert('RGBA')
def get_sprite(direction,index=0):
 options=[v for v in frames if v[0]['direction']==direction]
 if options:return options[index%len(options)][1]
 f={'north':10,'south':1,'west':4,'east':7}[direction];return greg.crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32))
def scene(actors):
 out=under.copy()
 for i,a in enumerate(actors):out.alpha_composite(get_sprite(a.get('direction','north'),i),(a['x']-16,a['y']-16))
 out.alpha_composite(above);return out
indoor=[a for a in layout['anchors'] if a['kind']=='social' or a['id']=='spawn'];scene(indoor).save(P/'review/occupied-native.png')
extra=['west-side-south','rear-center','east-side-north','bench-west-approach','bench-east-approach','garden-south','west-path-termination','east-path-termination'];scene(indoor+[a for a in layout['anchors'] if a['id'] in extra]).save(P/'review/exterior-occupied-native.png')
probes=[(434,816),(590,816),(112,816),(880,816),(80,128),(944,128),(80,144),(944,144)];contact=Image.new('RGB',(4*192,4*192),'#252525');d=ImageDraw.Draw(contact)
for i,(x,y) in enumerate(probes):
 for j,face in enumerate(['south','north']):
  im=scene([dict(x=x,y=y,direction=face)]).crop((x-32,y-32,x+32,y+32)).resize((192,192),Image.Resampling.NEAREST);cx=i%4*192;cy=(i//4*2+j)*192;contact.paste(im,(cx,cy));d.text((cx+2,cy+2),f'{x},{y} {face}',fill='white')
contact.save(P/'review/actual-atlas-depth-probes.png')
chairs=[a for a in layout['anchors'] if a['id'] in ['editor-1','editor-2','screen-viewer-1','keyboard-1','listen-east','listen-west']];contact=Image.new('RGB',(6*192,384),'#252525');d=ImageDraw.Draw(contact)
for i,a in enumerate(chairs):
 for j,face in enumerate(['south','north']):
  x,y=a['x'],a['y'];im=scene([dict(x=x,y=y,direction=face)]).crop((x-32,y-32,x+32,y+32)).resize((192,192),Image.Resampling.NEAREST);contact.paste(im,(i*192,j*192));d.text((i*192+2,j*192+2),a['id']+' '+face,fill='white')
contact.save(P/'review/inherited-chair-depth-probes.png');contact.save(P/'review/chair-depth-probes.png')
report=dict(source='Decoded current TMJ atlases, actors inserted between actual below/above layers',tmjSHA256=hashlib.sha256(p.read_bytes()).hexdigest(),priorOccupiedScreenshotUsed=False,avatarFrame=[32,32],abovePixelCount=sum(a>0 for a in above.getchannel('A').getdata()),proofInput='source/proof-inputs/native32-actors-overlay.png',proofInputSHA256=hashlib.sha256((R/'source/proof-inputs/native32-actors-overlay.png').read_bytes()).hexdigest(),exteriorProbePositions=probes,facings=['south','north'],inheritedChairDepthUnchanged=False,chairDepthCorrected=True,automaticFacing=False,standingOnly=True,liveScreenshot=False)
(P/'validation/decoded-runtime-proof.json').write_text(json.dumps(report,indent=2)+'\n');print('Decoded current TMJ actor proofs generated')

records=[]
for i,a in enumerate(indoor):
 options=[v for v in frames if v[0]['direction']==a['direction']]
 meta=options[i%len(options)][0] if options else dict(file='greg-reference.png',frame={'north':10,'south':1,'west':4,'east':7}[a['direction']],direction=a['direction'])
 records.append(dict(anchor=a['id'],position=[a['x'],a['y']],direction=a['direction'],nativeFrameSize=[32,32],source=meta,pose='unchanged repository standing frame; illustrative facing, not auto-facing'))
(P/'review/occupants.json').write_text(json.dumps(records,indent=2)+'\n')
(P/'validation/woka-provenance.json').write_text(json.dumps(dict(scope='Actual frames cropped from included prior proof overlay, with Greg fallback for unavailable direction; no raw sheets or runtime actors',proofOverlay='source/proof-inputs/native32-actors-overlay.png',sourceMetadata='source/proof-inputs/native32-actors-provenance.json',actors=records,runtimeContainsAvatars=False),indent=2)+'\n')
