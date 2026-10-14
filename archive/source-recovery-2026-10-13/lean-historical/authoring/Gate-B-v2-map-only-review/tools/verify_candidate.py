"""Verify the packaged final candidate, without a browser or engine changes."""
from pathlib import Path, PurePosixPath
import copy
import hashlib
import json
import posixpath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'publish/public/butterfly-town/gate-b/v2'
checks = []
def check(name, condition):
    assert condition, name
    checks.append(name)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((ROOT / 'PUBLICATION-MANIFEST.json').read_text())
base = json.loads((ROOT / 'baseline/gate-b-v1.tmj').read_text())
candidate = json.loads((OUT / 'gate.tmj').read_text())
check('frozen-B-v1-base-hash', digest(ROOT / 'baseline/gate-b-v1.tmj') == '83f3d0ef4b3c8cc7706710a25910a9491904ee2ca728931dcd0d5713d7973677')
check('frozen-A-base-hash', digest(ROOT / 'baseline/gate-a.tmj') == 'd284ee94a6c608903e3858efc30fcae12837d4ee7e89a6cf9f49c5a5cec8f104')
check('standard-32-grid', (candidate['tilewidth'],candidate['tileheight'],candidate['width'],candidate['height']) == (32,32,30,45))
check('all-tilesets-art-animation-collision-identical', base['tilesets'] == candidate['tilesets'])
check('all-object-geometry-and-layer-data-identical', [{k:v for k,v in layer.items() if k != 'properties'} for layer in base['layers']] == [{k:v for k,v in layer.items() if k != 'properties'} for layer in candidate['layers']])
carrier = next(layer for layer in candidate['layers'] if layer['name'] == 'campus-audio-control')
expected_audio = [
    {'name':'playAudio','type':'string','value':'native-audio/assets/gate-music-waterfalls-loop.mp3'},
    {'name':'audioLoop','type':'bool','value':True},
    {'name':'audioVolume','type':'float','value':1},
]
check('static-native-audio-properties',carrier['properties'] == expected_audio)
check('full-map-audio-coverage',carrier['width'] == 30 and carrier['height'] == 45 and len(carrier['data']) == 1350 and all(gid > 0 for gid in carrier['data']) and not any(carrier.get(name,0) for name in ('x','y','offsetx','offsety')))
check('no-competing-audio-properties',sum(prop['name'] in ('playAudio','playAudioLoop') for layer in candidate['layers'] for prop in layer.get('properties',[])) == 1)
allowed = copy.deepcopy(base)
allowed['properties'] = [prop for prop in allowed['properties'] if prop['name'] not in ('gateAmbientAudio','audioEnabled','campusVersion','gateCameraVersion')]
allowed['properties'] += [
    {'name':'campusVersion','type':'string','value':'gate-b-v2-native-follow-32'},
    {'name':'gateCameraVersion','type':'string','value':'B v2: normal native follow and manual zoom'},
]
next(layer for layer in allowed['layers'] if layer['name'] == 'campus-audio-control')['properties'] = expected_audio
check('TMJ-diff-limited-to-native-audio-and-version-metadata',allowed == candidate)
check('onward-destination-remains-editor-configurable-and-blank', next(prop['value'] for prop in candidate['properties'] if prop['name'] == 'campusRoomUrl') == '')
check('mixed-audio-exact-existing-bytes',digest(OUT / expected_audio[0]['value']) == '449b6c5d32a9a9589d8297676001a19cf92ab86162758a6bdfc8430bdc2207e3')
check('pure-music-preserved',digest(ROOT / 'originals/gate-music.mp3') == '3f859b065fecd1f09c306db77051efdcba4477cb6f8e49481c225c60c42c76ea')
check('cascade-stem-preserved',digest(ROOT / 'originals/cascade-soft.mp3') == '40a838261cd33bbb1d1f4ad8c271ca821ffc76c7923d8bf6a2cea4198a815ff8')

code = (OUT / 'native-audio/gate-with-native-audio.js').read_text()
check('published-script-equals-tested-source',code == (ROOT / 'source/gate-with-native-audio.js').read_text())
for forbidden in ('WA.camera','WA.controls','WA.sound','WA.ui','setProperty','new Audio','AudioContext','installGateCamera','installGateAmbientAudio','setViewport'):
    check('no-runtime-dependency:'+forbidden,forbidden not in code)
check('old-camera-and-custom-audio-modules-absent',not (OUT / 'native-audio/gate-camera-b.mjs').exists() and not (OUT / 'native-audio/gate-ambient-audio.mjs').exists())
check('no-focus-area-properties',not any(prop['name'] == 'focusable' and prop['value'] for layer in candidate['layers'] for obj in [layer,*layer.get('objects',[])] for prop in obj.get('properties',[])))

dependencies = {item['path']:item for item in manifest['sharedDependencies']}
for tileset in candidate['tilesets']:
    resolved = posixpath.normpath(str(PurePosixPath('public/butterfly-town/gate-b/v2') / tileset['image']))
    check('relative-image-resolves:'+tileset['image'],resolved in dependencies)
    check('shared-image-exact:'+tileset['image'],digest(ROOT / 'dependencies' / resolved) == dependencies[resolved]['sha256'])
for item in manifest['files']:
    file = ROOT / 'publish' / item['path']
    check('payload-manifest:'+item['path'],file.stat().st_size == item['bytes'] and digest(file) == item['sha256'])
for item in json.loads((ROOT / 'SOURCE-MANIFEST.json').read_text())['files']:
    filename = 'GameMapProperties.ts' if item['path'] == 'libs/map-editor/src/types.ts' else Path(item['path']).name
    check('camera-source-pin:'+filename,digest(ROOT / 'source-audit/camera' / filename) == item['sha256'])
check('native-audio-test-fixture-exact', (ROOT / 'tests/fixtures/AudioPlayback.ts').read_bytes() == (ROOT / 'source-audit/audio/pinned-source/play/src/front/Components/AudioManager/AudioPlayback.ts').read_bytes())
stop = json.loads((ROOT / 'source-audit/audio/STATIC-LAYER-STOP-RESULTS.json').read_text())
check('native-stop-focused-proof-record-present',stop.get('result') == 'PASS' and len(stop.get('checks',[])) == 6)

# Local workspace baselines are rechecked when present; these checks never mutate them.
old_root = Path('/workspace/shared/gate-b-experience')
if old_root.exists():
    for item in json.loads((ROOT / 'baseline/BV1-MANIFEST.json').read_text())['files']:
        check('original-B-v1-file-unchanged:'+item['path'],digest(old_root / 'publish' / item['path']) == item['sha256'])
    check('original-A-map-unchanged',digest(old_root / 'originals/gate.tmj') == digest(ROOT / 'baseline/gate-a.tmj'))

result = subprocess.run(['node','--check',str(OUT / 'native-audio/gate-with-native-audio.js')],capture_output=True,text=True)
check('script-syntax',result.returncode == 0)
result = subprocess.run(['node','--experimental-transform-types','--test','--test-reporter=tap',*map(str,sorted((ROOT / 'tests').glob('*.test.mjs')))],capture_output=True,text=True)
(ROOT / 'NODE-TEST-RESULTS.txt').write_text(result.stdout + result.stderr)
check('all-21-local-tests-pass',result.returncode == 0 and re.search(r'# pass 21\b',result.stdout) is not None)
report = {
    'stage':'source-and-state-validated','passed':True,'checksPassed':len(checks),'checks':checks,
    'nodeTestsPassed':21,'movementEventSteps':7820,'nativeFramingCases':6,'nativeStopFixtureChecks':6,
    'engineCommit':manifest['engineCommit'],'candidateTmjSha256':digest(OUT / 'gate.tmj'),
    'candidateFiles':manifest['fileCount'],'candidateBytes':manifest['totalBytes'],
    'liveGameVerified':False,'physicalMobileVerified':False,
    'limits':'Static/source/state-model validation only. No rendered HUD, live tap path, physical joystick, audible playback or mobile verification. No automatic zoom, spatial second stream or engine fixes.'
}
(ROOT / 'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key != 'checks'},indent=2))
