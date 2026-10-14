"""Behavior-only local prototype. Artwork is still rejected v05 baseline, not final A."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1]; S=R/'source/baseline-v05'; O=R/'map32'
for p in S.glob('*.png'): shutil.copy2(p,O/p.name)
m=json.loads((S/'grand-auditorium.tmj').read_text());w,h=m['width'],m['height']
quiet=next(l for l in m['layers'] if any(p.get('name')=='silent' and p.get('value') is True for p in l.get('properties',[])))
gid=next(v for v in quiet['data'] if v);quiet['name']='quiet-spawn-receiver';quiet['data']=[0]*(w*h)
# Four native cells per side. Covers the64×64 default spawn plus one32px landing allowance.
quiet_rect=[704,1760,128,128]
for y in range(55,59):
 for x in range(22,26):quiet['data'][y*w+x]=gid
areas=next(l for l in m['layers'] if l['name']=='map-areas')
areas['objects'].append({'id':m['nextobjectid'],'name':'flagship-a-native-stage-focus','class':'area','type':'area','x':0,'y':0,'width':1536,'height':1008,'rotation':0,'visible':True,'properties':[{'name':'focusable','type':'bool','value':True},{'name':'zoomMargin','type':'float','value':0.15}]});m['nextobjectid']+=1
for p in m['properties']:
 if p['name']=='name':p['value']='Astral Concourse / Corrective A behavior prototype'
 if p['name']=='status':p['value']='Local behavior-only prototype; rejected baseline artwork not yet replaced'
(O/'grand-auditorium.tmj').write_text(json.dumps(m,indent=2)+'\n')
wam=json.loads((S/'grand-auditorium.wam').read_text())
s=json.dumps(wam).replace('astral-flagship-v05','astral-flagship-v07').replace('Flagship v05','Flagship v07')
(O/'grand-auditorium.wam').write_text(json.dumps(json.loads(s),indent=2)+'\n')
report={'status':'Behavior-only prototype; not visually accepted or route-tested','focus':{'nativeObject':[0,0,1536,1008],'zoomMargin':.15,'cameraOnly':True,'script':False,'resizeLimitation':'Source-native resize may drop margin and retain stale camera zoom; not resolved by this map prototype'},'quietReceiverXYWH':quiet_rect,'quietCells':sum(bool(v) for v in quiet['data']),'baselineQuietCells':333,'collisionUnchanged':next(l for l in m['layers']if l['name']=='collision-permanent')==next(l for l in json.loads((S/'grand-auditorium.tmj').read_text())['layers']if l['name']=='collision-permanent'),'artworkStillBaseline':True,'atlasBytesUnchanged':all(hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((S/p.name).read_bytes()).digest()for p in O.glob('*.png')),'liveVerified':False}
(R/'validation/behavior-prototype.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
