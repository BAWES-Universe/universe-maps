from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'map32';V=R/'validation';m=json.loads((O/'grand-auditorium.tmj').read_text());w=json.loads((O/'grand-auditorium.wam').read_text());checks=[]
def ck(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
ck('native32_finite_orthogonal',m['tilewidth']==m['tileheight']==32 and[m['width'],m['height']]==[80,60]and not m['infinite']and m['orientation']=='orthogonal');ck('portable_companion_url',w['mapUrl']=='./grand-auditorium.tmj');sets=[];closure={'grand-auditorium.tmj','grand-auditorium.wam'}
for t in m['tilesets']:
 p=O/t['image'];closure.add(t['image']);im=Image.open(p).convert('RGBA');sets.append((t,im));ck('atlas_'+t['name'],im.size==(t['imagewidth'],t['imageheight'])and max(im.size)<=1024 and t['tilewidth']==t['tileheight']==32)
rendered={}
for layer,source in [('hall-base','runtime-base.png'),('hall-above','runtime-above.png')]:
 l=next(l for l in m['layers']if l['name']==layer);im=Image.new('RGBA',(2560,1920));ck(layer+'_data_count',len(l['data'])==4800)
 for i,gid in enumerate(l['data']):
  if not gid:continue
  t,a=next((t,a)for t,a in reversed(sets)if t['firstgid']<=gid);v=gid-t['firstgid'];assert v<t['tilecount'];x=v%t['columns']*32;y=v//t['columns']*32;im.paste(a.crop((x,y,x+32,y+32)),(i%80*32,i//80*32))
 ck(layer+'_exact_compiled_pixels',im.tobytes()==Image.open(R/'assets'/source).convert('RGBA').tobytes());rendered[layer]=im
v1base=Image.open(R/'source/v01-runtime-base.png').convert('RGBA');v1above=Image.open(R/'source/v01-runtime-above.png').convert('RGBA')
for layer,im in [('hall-base',v1base),('hall-above',v1above)]:ck(layer+'_preserved_v01_top944',rendered[layer].crop((0,0,1536,944)).tobytes()==im.crop((0,0,1536,944)).tobytes())
ck('no_unlisted_runtime_files',closure=={p.name for p in O.iterdir()if p.is_file()});names=[l['name']for l in m['layers']];ck('floor_depth_order',names.index('hall-base')<names.index('floorLayer')<names.index('hall-above'))
text=json.dumps(m)+json.dumps(w);ck('no_external_services_scripts_audio_or_exit_links',not any(s in text for s in['http://','https://','jitsi','script','playAudio','soundscape','exitUrl','exitSceneUrl']))
ck('234_seat_records',len(json.loads((R/'source/seats.json').read_text()))==210 and len(json.loads((R/'source/runtime-layout.json').read_text())['socialAnchors'])==24)
for name in ['geometry.json','native-routes.json']:
 a=json.loads((V/name).read_text());ck(name,a['allPass']);
 if name=='native-routes.json':ck('no_hypothetical_geometry_in_final_route_test',not a['hypotheticalDividerExperiment']);ck('recorded_all_route_samples',a['sampleCount']>0)
for name in ['v03-zone-verification.json','v03-independent-route-verification.json']:
 a=json.loads((V/name).read_text());ck(name,a['allPassed']);ck(name+'_hash_matches',all(hashlib.sha256((R/path).read_bytes()).hexdigest()==value for path,value in a['hashes'].items()))
files=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()];report={'allPass':all(c['pass']for c in checks),'checks':checks,'runtimeFiles':files,'runtimeBytes':sum(x['bytes']for x in files),'sourceOnly':True,'browserVerified':False,'mediaVerified':False,'multiplayerVerified':False,'published':False};(V/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'allPass':report['allPass'],'checks':len(checks),'runtimeFiles':len(files),'runtimeBytes':report['runtimeBytes'],'failures':[c for c in checks if not c['pass']]},indent=2));assert report['allPass']
