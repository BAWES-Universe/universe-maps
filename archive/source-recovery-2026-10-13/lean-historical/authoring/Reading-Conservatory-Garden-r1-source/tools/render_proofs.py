from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];O=R/'candidate';S=R/'source-assets';V=O/'review';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();layout=read(O/'source/layout.json');native=read(O/'NATIVE-ROUTES.json');traces=read(O/'source/GARDEN-ROUTE-TRACES.json');seattraces=read(O/'source/SEAT-ROUTE-TRACES.json');actors=read(S/'ACTOR-PROVENANCE.json')['actors'];dirs=['south','west','east','north'];ovs={d:Image.open(S/f'proof-actors-{d}.png').convert('RGBA') for d in dirs};fg=Image.open(V/'foreground-native.png').convert('RGBA');empty=Image.open(V/'empty-native.png').convert('RGBA');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for evidence in [native,traces,seattraces]:
 for path,h in evidence['inputHashes'].items():assert sha(O/path)==h,(path,'stale evidence')
def frame(i,d):
 a=actors[i%10];x,y=a['anchor'];f=ovs[d].crop((x-16,y-16,x+16,y+16));assert hashlib.sha256(f.tobytes()).hexdigest()==a['frames'][d]['rgba_sha256'];return f
def arrival(name):return next(r for r in native['rows'] if r['name']==name+' exact authored arrival')
def render(placements):
 out=empty.copy()
 for i,(xy,di) in enumerate(placements):x,y=xy;out.alpha_composite(frame(i,dirs[di]),(round(x)-16,round(y)-16))
 out.alpha_composite(fg);return out
selected=layout['seats']+[next(a for a in layout['anchors'] if a['name']==n) for n in ['West standing reading desk','East standing reading desk','Fountain north','Fountain east','Fountain south','Fountain west']]
checks=[];placements=[]
for i,s in enumerate(selected):
 r=arrival(s['name']);assert r['final']==s['anchor'];placements.append((r['final'],r['nativeFinalDirection']));x,y=r['final'];f=frame(i,dirs[r['nativeFinalDirection']]);am=np.array(f)[:,:,3]>0;fm=np.array(fg.crop((x-16,y-16,x+16,y+16)))[:,:,3]>0;head=int((am[:14]&fm[:14]).sum());assert head==0;checks.append({'name':s['name'],'anchor':s['anchor'],'native_arrival_facing':dirs[r['nativeFinalDirection']],'upper14_foreground_pixels':head,'lower18_foreground_pixels':int((am[14:]&fm[14:]).sum()),'auto_turn':False,'source_actor':actors[i%10]['seat'],'frame_sha256':hashlib.sha256(f.tobytes()).hexdigest()})
occupied=render(placements);occupied.save(V/'actual-arrival-native.png');occupied.crop((0,480,768,832)).save(V/'garden-actual-arrivals.png')
for name,box in [('west',(192,180,348,320)),('east',(412,180,568,320)),('mentorship',(580,136,730,252)),('study',(48,118,184,236))]:
 for kind,im in [('empty',empty),('actual-arrival',occupied)]:im.crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.NEAREST).save(V/f'{name}-{kind}-4x.png')
# Exact native positions/directions at all cardinal ring points and both side-lane extrema.
board=Image.new('RGB',(1000,820),'#f4f0e5');d=ImageDraw.Draw(board);d.text((16,12),'Garden routes: native arrivals, real 32px sprites / 16px bodies',font=font,fill='#214c3b')
names=['Fountain north','Fountain northeast','Fountain east','Fountain southeast','Fountain south','Fountain southwest','Fountain west','Fountain northwest','West edge upper','West edge lower','East edge upper','East edge lower']
for i,name in enumerate(names):
 row=arrival(name);x,y=row['final'];im=render([(row['final'],row['nativeFinalDirection'])]);box=(max(0,min(672,x-48)),max(480,min(736,y-48)));crop=im.crop((box[0],box[1],box[0]+96,box[1]+96)).resize((192,192),Image.Resampling.NEAREST);col=i%4;rr=i//4;board.paste(crop,(16+col*248,55+rr*254));d.text((16+col*248,250+rr*254),name,font=font,fill='#214c3b');d.text((16+col*248,269+rr*254),dirs[row['nativeFinalDirection']]+f' at {x},{y}',font=font,fill='#496155')
board.save(V/'garden-route-arrivals.png')
# Time-indexed water is decoded from actual runtime tile animation, below all players.
m=read(O/'map32/map.tmj');atlases={t['image']:Image.open(O/'map32'/t['image']).convert('RGBA') for t in m['tilesets']};water_ts=next(t for t in m['tilesets'] if t['name']=='fountain-water');water_layer=next(l for l in m['layers'] if l['name']=='fountain-water');water_frames=[]
for fi in range(8):
 im=Image.open(V/'base-native.png').convert('RGBA')
 for j,v in enumerate(water_layer['data']):
  if not v:continue
  idx=v-water_ts['firstgid'];entry=next(e for e in water_ts['tiles'] if e['id']==idx);n=entry['animation'][fi]['tileid'];x=n%water_ts['columns']*32;y=n//water_ts['columns']*32;im.alpha_composite(atlases[water_ts['image']].crop((x,y,x+32,y+32)),(j%24*32,j//24*32))
 im.alpha_composite(fg);water_frames.append(im)
water_frames[0].crop((288,544,480,704)).resize((576,480)).save(V/'fountain-water-detail.gif',save_all=True,append_images=[f.crop((288,544,480,704)).resize((576,480)) for f in water_frames[1:]],duration=140,loop=0,disposal=2)
for ri,route in enumerate(traces['captures'][:2]):
 movie=[]
 for i in range(0,len(route['points']),8):
  x,y=route['points'][i];di=route['directions'][i];im=water_frames[(i//8)%8].copy();im.alpha_composite(frame(ri,dirs[di]),(round(x)-16,round(y)-16));im.alpha_composite(fg);movie.append(im.crop((0,480,768,832)))
 movie[0].save(V/f'garden-native-ring-{ri+1}.gif',save_all=True,append_images=movie[1:],duration=133,loop=0,disposal=2)
(O/'ACTUAL-ARRIVAL-CHECKS.json').write_text(json.dumps({'scope':'Actual native source-route endpoints/facings with authentic repository standing-idle proof frames. Rendered illustrations, not live browser or walking animation.','rows':checks},indent=2)+'\n');print('Rendered actual arrivals, twelve route detail panels and two native route GIFs.')
