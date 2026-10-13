from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];out=R/'publish/public/butterfly-town/gate-b/v4';v3=Path('/workspace/shared/gate-cinematic-v3/integrated/public/butterfly-town/gate-b/v3');checks=[]
def check(name,condition):
 assert condition,name
 checks.append({'name':name,'pass':True})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((out/'gate.tmj').read_text());old=json.loads((R/'baseline/gate.tmj').read_text())
check('standard32 30x45 map',d['tilewidth']==d['tileheight']==32 and d['width']==30 and d['height']==45)
for key in d:
 if key!='properties':check('unchanged TMJ '+key,d[key]==old[key])
changed=[]
for prop in d['properties']:
 prior=next(x for x in old['properties']if x['name']==prop['name'])
 if prop!=prior:changed.append(prop['name'])
check('only two version metadata values changed',sorted(changed)==['campusVersion','gateCameraVersion'])
raw=(out/'gate.tmj').read_text()
for name in changed:
 a=next(x['value']for x in d['properties']if x['name']==name);b=next(x['value']for x in old['properties']if x['name']==name);raw=raw.replace(json.dumps(a),json.dumps(b),1)
check('every other TMJ byte preserved',raw.encode()==(R/'baseline/gate.tmj').read_bytes())
check('accepted public v3 map unchanged',sha(v3/'gate.tmj')=='6358b9af1de298916e73aa6ed3385896dc97a230cbb776562662bb987e66c21d')
for name in ['native-audio/assets/gate-music-waterfalls-loop.mp3','preserved-assets.json','tilesets/gate-balcony-foreground.png']:
 check('byte-identical '+name,sha(out/name)==sha(v3/name))
check('silent spawn layer retained',any(l['id']==55 and l['name']=='spawn-silent-zone'for l in d['layers']))
check('balcony foreground layer retained',any(l['id']==56 and l['name']=='gate-balcony-foreground'for l in d['layers']))
check('portal destination blank',next(x['value']for x in d['properties']if x['name']=='campusRoomUrl')=='')
script=(out/'native-audio/gate-with-native-audio.js').read_bytes();core=(R/'source/preserved-portal-audio-core.js').read_bytes()
check('portal/audio core exact',core in script and core in (R/'baseline/gate-with-native-audio.js').read_bytes())
check('only one camera.set site',script.count(b'WA.camera.set(')==1)
for token in [b'WA.camera.followPlayer(',b'installGateReveal',b'installMobileArrivalExperiment',b'setViewport(',b'WA.controls.',b'WA.sound.']:
 check('absent '+token.decode(),token not in script)
for p in json.loads((R/'PIN-ORIGINS.json').read_text()):
 b=(R/'pinned-source'/p['file']).read_bytes();check('exact pinned source '+p['file'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p['sha'])
deps=json.loads((out/'preserved-assets.json').read_text())['assets']
for a in deps:check('dependency '+a['path'],sha(R/'dependencies'/a['path'])==a['sha256'])
for t in d['tilesets']:
 target=(out/t['image']).resolve()
 if not target.exists():target=(R/'dependencies/public/butterfly-town/gate-b/v4'/t['image']).resolve()
 check('tileset resolves '+t['name'],target.is_file())
layers=d['layers'];audio=next(l for l in layers if l['name']=='campus-audio-control');props={x['name']:x['value']for x in audio['properties']}
check('native full-coverage static looping audio',props['playAudio']=='native-audio/assets/gate-music-waterfalls-loop.mp3' and props['audioLoop']is True and props['audioVolume']==1 and all(audio['data']))
files=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(out.rglob('*'))if p.is_file()];check('six runtime files',len(files)==6)
manifest={'status':'LOCAL REVIEW ONLY; unpublished; two native pre-first-move limitations documented','engineRef':'75666c0ccae779515b6fcbd83446ebd1eee29d1b','baselineV3MapSha256':sha(R/'baseline/gate.tmj'),'geometryLayersTilesetsAndOtherMapBytesPreserved':True,'desktopCameraCalls':0,'coarseDeviceInitialCameraCalls':1,'laterScriptedCameraCalls':0,'files':files}
(R/'CANDIDATE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');(R/'INTEGRITY-VERIFICATION.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(json.dumps({'passed':len(checks),'failed':0,'files':files},indent=2))
