from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];P=R/'integrated/public/butterfly-town/gate-b/v3';checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
d=json.loads((P/'gate.tmj').read_text());g=json.loads((R/'baseline/reviewed-geometry.tmj').read_text());v2=json.loads((R/'baseline/v2-map.tmj').read_text());manifest=json.loads((R/'GEOMETRY-INTEGRATION-MANIFEST.json').read_text())
check('frozen Bv2 source map',sha(R/'baseline/v2-map.tmj')=='90727495f43b9fc8107cffb287f2b748029ae42f6c9f43f9b2a61dbac95c150b')
check('reviewed geometry source bytes',sha(R/'baseline/reviewed-geometry.tmj')==manifest['integrationFiles'][0]['sha256'])
for k in d:
 if k!='properties':check('exact geometry field '+k,d[k]==g[k])
check('exact native audio mix',sha(P/'native-audio/assets/gate-music-waterfalls-loop.mp3')==manifest['unchangedPayloadFiles'][0]['sha256'])
check('exact foreground PNG',sha(P/'tilesets/gate-balcony-foreground.png')==manifest['integrationFiles'][1]['sha256'])
script=(P/'native-audio/gate-with-native-audio.js').read_bytes();core=(R/'baseline/v2-script.js').read_bytes();check('V2 core byte-identical embedded block',script.count(core)==1)
for module in ['gate-reveal.mjs','mobile-arrival-experiment.mjs']:
 check('exact module '+module,(R/'source'/module).read_text().replace('export function','function').encode() in script)
for forbidden in ['WA.controls.','WA.sound.','WA.ui.','setViewport','requestAnimationFrame','innerWidth','innerHeight']:
 # iframe dimension words appear only in an explanatory comment in module; no access is allowed.
 if forbidden in ['innerWidth','innerHeight']:check('no iframe dimension read '+forbidden,('window.'+forbidden).encode() not in script)
 else:check('no forbidden operation '+forbidden,forbidden.encode() not in script)
props=lambda obj:{p['name']:p['value'] for p in obj.get('properties',[])}
check('blank destination',props(d)['campusRoomUrl']=='')
check('standard32',d['tilewidth']==d['tileheight']==32 and d['width']==30 and d['height']==45)
check('audio carrier preserved',next(l for l in d['layers'] if l['name']=='campus-audio-control')==next(l for l in v2['layers'] if l['name']=='campus-audio-control'))
for asset in json.loads((P/'preserved-assets.json').read_text())['assets']:
 p=R/'dependencies'/asset['path'];check('exact shared asset '+p.name,sha(p)==asset['sha256'])
for pin in json.loads((R/'PIN-ORIGINS.json').read_text()):
 b=(R/'pinned-source'/pin['file']).read_bytes();check('exact pinned Git blob '+pin['file'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==pin['sha'])
subprocess.run(['node','--check',str(P/'native-audio/gate-with-native-audio.js')],check=True);checks.append('integrated script syntax')
files=[{'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.rglob('*')) if p.is_file()]
result={'status':'PASS','checks':checks,'checkCount':len(checks),'files':files,'publicationAuthorized':False}
(R/'INTEGRATED-VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'files':len(files)}))
