import render_runtime_proofs as p
from PIL import Image,ImageDraw
import json,hashlib
rows=json.loads((p.P/'validation/native-arrival-routes.json').read_text())['rows'];directions={0:'south',1:'west',2:'east',3:'north'};seats=[];records=[]
for a in p.layout['anchors']:
 if not (a['kind']=='social' or a['id']=='spawn' or a['id'] in ['west-side-south','rear-center','east-side-north','bench-west-approach','bench-east-approach','garden-south','west-path-termination','east-path-termination']):continue
 r=next(r for r in rows if r['id']=='spawn-to-'+a['id'] and r['input']=='desktop');x,y=r['final'];
 if a['id'].startswith(('editor-','screen-viewer-','keyboard-','listen-')):assert abs(x-a['x'])<1e-6 and abs(y-a['y'])<1e-6,(a['id'],[a['x'],a['y']],r['final'])
 face=directions[r['finalDirection']];seats.append(dict(id=a['id'],x=round(x),y=round(y),direction=face));records.append(dict(id=a['id'],actualArrival=[x,y],nativeFinalDirection=r['finalDirection'],actualFacing=face,authoredAnchor=[a['x'],a['y']],authoredEqualsNative=abs(x-a['x'])<1e-6 and abs(y-a['y'])<1e-6,intendedConfigFacing=a['direction'],automaticFacing=False,pathPass=r['pass']))
p.scene(seats).save(p.P/'review/native-arrival-occupied.png')
chairs=[a for a in seats if a['id'].startswith(('editor-','screen-viewer-','keyboard-','listen-'))];out=Image.new('RGB',(5*192,2*192),'#202020');d=ImageDraw.Draw(out)
for i,a in enumerate(chairs):
 x,y=a['x'],a['y'];im=p.scene([a]).crop((x-32,y-32,x+32,y+32)).resize((192,192),Image.Resampling.NEAREST);pos=(i%5*192,i//5*192);out.paste(im,pos);d.text((pos[0]+2,pos[1]+2),a['id']+' arrival '+a['direction'],fill='white')
out.save(p.P/'review/actual-native-arrivals.png')
(p.P/'validation/native-arrival-proof.json').write_text(json.dumps(dict(scope='Current native source replay final coordinates and direction from desktop spawn-to-target routes, drawn from decoded TMJ layers; not a live browser screenshot',automaticFacing=False,tmjSHA256=hashlib.sha256((p.P/'map32/resonance-media-house.tmj').read_bytes()).hexdigest(),rows=records),indent=2)+'\n')
# Existing configured direction illustration is retained with an explicit filename/label.
(p.P/'review/intended-seat-facings.png').write_bytes((p.P/'review/actual-seat-facings.png').read_bytes())
(p.P/'review/intended-config-occupied.png').write_bytes((p.P/'review/exterior-occupied-native.png').read_bytes())
print('Actual native arrivals proof generated; configured facing is separately labelled')
