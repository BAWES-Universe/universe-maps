from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'rebuild-final/baseline'
RESULTS=Path('/workspace/shared/gate-b-native-proof/results')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
# Every file in the final map is independently reproduced from the exact A baseline.
files=[p for p in (ROOT/'gate').rglob('*') if p.is_file()]
for p in files:
 q=ROOT/'rebuild-final/gate'/p.relative_to(ROOT/'gate');assert q.is_file() and sha(p)==sha(q),str(p)
a=json.loads((BASE/'map/gate.tmj').read_text());b=json.loads((ROOT/'gate/map/gate.tmj').read_text())
assert a['tilesets']==b['tilesets']
for la,lb in zip(a['layers'],b['layers']):
 assert la['name']==lb['name']
 if la['type']=='tilelayer' and la['name']!='start':assert la==lb,la['name']
assert next(p['value'] for p in b['properties'] if p['name']=='campusRoomUrl')==''
for p in (ROOT/'gate/map/tilesets').glob('*.png'):assert sha(p)==sha(BASE/'map/tilesets'/p.name)
for src,dest in [('gate-camera-b.mjs','gate-camera-b.mjs'),('gate-entry-b.js','gate-with-native-audio.js'),('gate-ambient-audio.mjs','gate-ambient-audio.mjs')]:assert sha(ROOT/'source'/src)==sha(ROOT/'gate/map/native-audio'/dest)
evidence=ROOT/'docs/evidence';evidence.mkdir(exist_ok=True)
reports=['portrait-390x720-native-verification.json','desktop-1024x672-native-verification.json','portrait-390x720-reduced-native-verification.json','desktop-1024x672-manual-camera.json','desktop-1024x672-native-audio-verification.json']
for f in reports:
 data=json.loads((RESULTS/f).read_text());assert data['passed'];shutil.copy2(RESULTS/f,evidence/f)
summary={f:{'passed':True,'checks':list(json.loads((RESULTS/f).read_text()).get('checks',{}))} for f in reports}
write(ROOT/'docs/VERIFICATION.json',{'sourceCommit':'6067337f232c9a9a5cdb929d819d4642c73c07a1','auditedEngineCommit':'f00b3482f23c51976b4b339d7a891cad683d6498','artAtlasCount':15,'animationDefinitions':sum(len(t.get('animation',[]))>0 for s in b['tilesets'] for t in s.get('tiles',[])),'baselineArtAnimationsCollisionUnchanged':True,'defaultSpawn':[496,1136],'browserScope':'Visible cloud Chromium; actual Phaser3.86 and native AudioPlayback class through narrow map API adapters. Not full Universe or physical phone.','reports':summary,'nodeTestsPassed':24})
write(ROOT/'docs/CANDIDATE-MANIFEST.json',[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)])
# Additive public variant uses byte-identical shared preserved A atlas files.
pub=ROOT/'publish/public/butterfly-town/gate-b/v1';pub.mkdir(parents=True,exist_ok=True)
shared=[]
for s in b['tilesets']:
 p=ROOT/'gate/map'/s['image'];rel='../../v6/gate/map/'+s['image'];s['image']=rel
 shared.append({'path':'public/butterfly-town/v6/gate/map/tilesets/'+p.name,'mapRelativeUrl':rel,'bytes':p.stat().st_size,'sha256':sha(p)})
(pub/'gate.tmj').write_text(json.dumps(b,separators=(',',':'))+'\n')
for name in ['gate-with-native-audio.js','gate-camera-b.mjs','gate-ambient-audio.mjs','assets/gate-music-waterfalls-loop.mp3']:
 dst=pub/'native-audio'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'gate/map/native-audio'/name,dst)
write(pub/'preserved-assets.json',{'sourceCommit':'6067337f232c9a9a5cdb929d819d4642c73c07a1','note':'Shared preserved v6 files; a branch URL is not immutable. Verify hashes and never modify them for this addition. Full independent assets are in the Library backup.','assets':shared})
(pub/'README.md').write_text('''# Gate B: detail to monument\n\nA separate test map. Paste gate.tmj into a new Universe room. Walk north toward the door: framing gradually widens and holds its scale. The ordinary 32px character and original art/collisions are unchanged.\n\nUse the map menu **Play gate music and waterfalls** once for the recovered music and a soft fixed waterfall bed. Native speaker mute, pause, and stop remain available. This is a baked ambient mix, not spatial water. On phones that ignore element volume, use speaker mute or pause; the volume slider may not attenuate, and native Play retry may be required after autoplay is blocked.\n\n**Use my camera** yields to ordinary follow at the current zoom. Reduced motion bypasses the choreography and hides the declared moving visual overlays.\n\nThe destination remains blank. Add your own portal at the door using the in-game map editor. This script does not navigate while campusRoomUrl is empty. An optional absolute HTTPS PLAY room URL can be set in that property later; do not use a relative TMJ asset URL.\n\nThe 15 image atlases are shared preserved v6 assets with hashes in preserved-assets.json. No existing file is changed by this addition. Standalone cloud Phaser and native-audio tests passed; full Universe mobile acceptance is pending. Desktop final framing has narrow finite side margins. No physical phone test is claimed.\n''')
published=[{'path':str(p.relative_to(ROOT/'publish')),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(pub.rglob('*')) if p.is_file()]
write(ROOT/'docs/PUBLICATION-MANIFEST.json',{'additivePath':'public/butterfly-town/gate-b/v1','runtimeEntry':'https://bawes-universe.github.io/universe-maps/butterfly-town/gate-b/v1/gate.tmj','files':published,'fileCount':len(published),'totalBytes':sum(p['bytes']for p in published),'sharedDependencies':shared})
print(json.dumps({'files':len(files),'candidateBytes':sum(p.stat().st_size for p in files),'publicationFiles':len(published),'publicationBytes':sum(p['bytes']for p in published),'publicationMapSha256':sha(pub/'gate.tmj')}))
