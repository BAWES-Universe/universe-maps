from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];G=Path('/workspace/shared/gate-boundary-v3');manifest=json.loads((G/'GEOMETRY-INTEGRATION-MANIFEST.json').read_text());out=R/'integrated/public/butterfly-town/gate-b/v3';out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in manifest['integrationFiles']:assert sha(Path(f['source']))==f['sha256']
source=G/'publish/public/butterfly-town/gate-b/v3'
for f in source.rglob('*'):
 if f.is_file():
  target=out/f.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
script=R/'candidates/mobile-arrival/public/butterfly-town/gate-b/v3/native-audio/gate-with-native-audio.js';shutil.copyfile(script,out/'native-audio/gate-with-native-audio.js')
d=json.loads((out/'gate.tmj').read_text());original=json.loads((source/'gate.tmj').read_text())
for p in d['properties']:
 if p['name']=='campusVersion':p['value']='gate-b-v3-experimental-mobile-arrival-balconies-32'
 if p['name']=='gateCameraVersion':p['value']='Portrait overview to native walking zoom, one modest landing reveal held through retreat'
(out/'gate.tmj').write_text(json.dumps(d,separators=(',',':'))+'\n')
for key in d:
 if key!='properties':assert d[key]==original[key],key
for name in ['campusRoomUrl','script','boundedLifecyclePending','liveRoomLinkPending']:
 assert next(p['value'] for p in d['properties'] if p['name']==name)==next(p['value'] for p in original['properties'] if p['name']==name)
assert sha(out/'tilesets/gate-balcony-foreground.png')==manifest['integrationFiles'][1]['sha256']
for f in manifest['unchangedPayloadFiles']:
 if f['path']!='native-audio/gate-with-native-audio.js':assert sha(out/f['path'])==f['sha256']
shutil.copyfile(G/'GEOMETRY-INTEGRATION-MANIFEST.json',R/'GEOMETRY-INTEGRATION-MANIFEST.json')
result={'status':'LOCAL INTEGRATED REVIEW; UNPUBLISHED','geometryManifestSha256':sha(G/'GEOMETRY-INTEGRATION-MANIFEST.json'),'geometryExactExceptTwoCameraVersionProperties':True,'baseV2CoreBytesPreserved':Path('/workspace/shared/gate-b-map-only-v2/source/gate-with-native-audio.js').read_bytes() in (out/'native-audio/gate-with-native-audio.js').read_bytes(),'files':[{'path':str(f.relative_to(out)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(out.rglob('*')) if f.is_file()]}
(R/'INTEGRATED-MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
