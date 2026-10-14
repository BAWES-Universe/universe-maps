from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];O=R/'candidate';S=R/'source-assets';rev=O/'review';base=Image.open(rev/'base-native.png').convert('RGBA');fg=Image.open(rev/'foreground-native.png').convert('RGBA');empty=Image.alpha_composite(base,fg);manual=Image.open(rev/'manually-faced-native.png').convert('RGBA');actors=json.load(open(S/'ACTOR-PROVENANCE.json'))['actors'];traces=json.load(open(O/'source/SEAT-ROUTE-TRACES.json'))['rows'];dirs=['south','west','east','north'];ovs={d:Image.open(S/f'proof-actors-{d}.png').convert('RGBA') for d in dirs};font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
def frame(i,d):
 a=actors[i];x,y=a['anchor'];fr=ovs[d].crop((x-16,y-16,x+16,y+16));assert hashlib.sha256(fr.tobytes()).hexdigest()==a['frames'][d]['rgba_sha256'];return fr
spawn_arrivals=json.load(open(S/'frozen-spawn-seat-arrivals.json'));actual=base.copy();checks=[]
for i,row in enumerate(traces):
 a=actors[i];x,y=a['anchor'];arrival=spawn_arrivals['rows'][i];d=dirs[arrival['nativeFinalDirection']];fr=frame(i,d);actual.alpha_composite(fr,(x-16,y-16));mask=np.array(fr)[:,:,3]>0;f=np.array(fg.crop((x-16,y-16,x+16,y+16)))[:,:,3]>0
 checks.append(dict(seat=a['seat'],anchor=a['anchor'],native_arrival=arrival['final'],anchor_exact=arrival['final']==a['anchor'],actual_arrival_facing=d,arrival_origin='quiet spawn (400,464)',local_approach_facing=dirs[row['approachFinalDirection']],illustrated_manual_facing=row['seat']['direction'],auto_facing=False,upper14_foreground=int((mask[:14]&f[:14]).sum()),lower18_foreground=int((mask[14:]&f[14:]).sum()),exact_arrival_frame_rgba_sha256=hashlib.sha256(fr.tobytes()).hexdigest()))
actual.alpha_composite(fg);actual.save(rev/'actual-arrival-native.png');actual.save(rev/'occupied-native.png')
for name,box in [('west',(192,180,348,320)),('east',(412,180,568,320)),('mentorship',(580,136,730,252)),('study',(48,118,184,236))]:
 for kind,im in [('empty',empty),('actual-arrival',actual),('manually-faced',manual)]:im.crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.NEAREST).save(rev/f'{name}-{kind}-4x.png')
for group,indices in [('west',range(4)),('east',range(4,8)),('mentorship',range(8,10))]:
 board=Image.new('RGB',(768,78+len(indices)*248),'#f3f0e6');d=ImageDraw.Draw(board);d.text((16,12),group.title()+' chairs: local native approach and facing',font=big,fill='#234b3d');d.text((16,40),'Authentic idle frames follow captured native facing; walking animation is not illustrated.',font=font,fill='#4b6054')
 for rr,i in enumerate(indices):
  a=actors[i];row=traces[i];ax,ay=a['anchor'];box=(ax-56,ay-52,ax+56,ay+48)
  ai=max(0,len(row['approach'])//3);di=min(len(row['departure'])-1,len(row['departure'])*2//3)
  pos=[(row['approach'][ai],row['approachDirections'][ai]),(row['approach'][-1],row['approachFinalDirection']),(row['departure'][di],row['departureDirections'][di])]
  d.text((16,78+rr*248),a['seat'],font=font,fill='#234b3d')
  for col,((xx,yy),direction) in enumerate(pos):
   fr=frame(i,dirs[direction]);im=base.copy();im.alpha_composite(fr,(round(xx)-16,round(yy)-16));im.alpha_composite(fg);crop=im.crop(box).resize((224,200),Image.Resampling.NEAREST);board.paste(crop,(16+col*250,99+rr*248))
   d.text((16+col*250,301+rr*248),f'{["Approach","Arrival","Departure"][col]}: {dirs[direction]} ({xx:.0f}, {yy:.0f})',font=font,fill='#4b6054')
 board.save(rev/f'{group}-native-route-positions.png')
original=Image.open(S/'original-approved-concept.png').convert('RGB').resize((768,512),Image.Resampling.LANCZOS);board=Image.new('RGB',(1556,558),'#f3f0e6');d=ImageDraw.Draw(board);d.text((10,12),'Approved concept r1 (retained)',font=big,fill='#234b3d');d.text((788,12),'Functional candidate r2 (under review)',font=big,fill='#234b3d');board.paste(original,(10,40));board.paste(empty.convert('RGB'),(788,40));board.save(rev/'approved-to-functional-comparison.png')
(O/'SEAT-DEPTH-CHECKS.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
