from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'map32';m=json.loads((O/'grand-auditorium.tmj').read_text());w=json.loads((O/'grand-auditorium.wam').read_text());V=R/'validation';checks=[]
def check(name,pass_,detail=None):checks.append({'check':name,'pass':bool(pass_),'detail':detail})
check('native32_grid',m['tilewidth']==m['tileheight']==32 and(m['width'],m['height'])==(48,40))
check('finite_orthogonal_map',m['infinite']==False and m['orientation']=='orthogonal')
check('companion_relative_url',w['mapUrl']=='./grand-auditorium.tmj')
sets=[]
for ts in m['tilesets']:
 p=O/ts['image'];im=Image.open(p).convert('RGBA');sets.append((ts,im));check('tileset_'+ts['name'],p.exists()and im.size==(ts['imagewidth'],ts['imageheight'])and max(im.size)<=1024)
for layer,name in [('hall-base','hall-base.png'),('hall-above','hall-above.png')]:
 l=next(x for x in m['layers']if x['name']==layer);im=Image.new('RGBA',(1536,1280));check(layer+'_data_count',len(l['data'])==48*40)
 for i,gid in enumerate(l['data']):
  if not gid:continue
  ts,a=next((t,a)for t,a in reversed(sets)if t['firstgid']<=gid);v=gid-ts['firstgid'];assert v<ts['tilecount'];x=v%ts['columns']*32;y=v//ts['columns']*32;im.paste(a.crop((x,y,x+32,y+32)),(i%48*32,i//48*32))
 check(layer+'_source_pixel_roundtrip',ImageChops.difference(im,Image.open(R/'assets'/name).convert('RGBA')).getbbox()is None)
names=[x['name']for x in m['layers']];check('above_after_floorLayer',names.index('hall-above')>names.index('floorLayer')>names.index('hall-base'))
text=json.dumps(m)+json.dumps(w);check('no_external_services_or_custom_scripts',not any(x in text for x in ['http://','https://','script','jitsi','playAudio','audioVolume','soundscape']))
check('all210_seats',len(json.loads((R/'source/seats.json').read_text()))==210)
for name in ['native-routes.json','geometry.json']:
 a=json.loads((V/name).read_text());check(name,a['allPass'])
a=json.loads((V/'spawn-silence.json').read_text());check('spawn_silence',a['after']['allSpawnsProtected'])
a=json.loads((V/'current-source-audit/candidate-wam-verification.json').read_text());
# Independent validator retains its explicit actual check results.
check('wam_audit_matches_current_file',hashlib.sha256((O/'grand-auditorium.wam').read_bytes()).hexdigest()in json.dumps(a))
files=[{'file':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()]
report={'allPass':all(x['pass']for x in checks),'checks':checks,'runtimeFiles':files,'sourceOnly':True,'browserVerified':False,'mediaVerified':False,'multiplayerVerified':False,'deploymentChanged':False};(V/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'allPass':report['allPass'],'checks':len(checks),'runtimeFiles':len(files),'runtimeBytes':sum(x['bytes']for x in files),'failed':[x for x in checks if not x['pass']]},indent=2));assert report['allPass']
