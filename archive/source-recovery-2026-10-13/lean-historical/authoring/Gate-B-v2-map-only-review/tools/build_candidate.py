"""Reproducible, separate map-only B v2; never modifies A, B v1 or engine source."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_ROOT = Path('/workspace/shared/gate-b-experience')
BASE = BASE_ROOT / 'publish/public/butterfly-town/gate-b/v1'
OUT = ROOT / 'publish/public/butterfly-town/gate-b/v2'
PIN = 'd2bc57b63b4abab9303fb3cbcecf1a0450fd15cc'
REPO = Path('/workspace/shared/native-soundscape-proof/full-checkout')

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def property_list(properties, changes, remove=()):
    result = [prop for prop in properties if prop['name'] not in changes and prop['name'] not in remove]
    for name, (kind, value) in changes.items(): result.append({'name':name, 'type':kind, 'value':value})
    return result

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'native-audio/assets').mkdir(parents=True, exist_ok=True)
candidate = json.loads((BASE / 'gate.tmj').read_text())
candidate['properties'] = property_list(candidate['properties'], {
    'campusVersion': ('string', 'gate-b-v2-native-follow-32'),
    'gateCameraVersion': ('string', 'B v2: normal native follow and manual zoom'),
}, remove=('gateAmbientAudio', 'audioEnabled'))
carrier = next(layer for layer in candidate['layers'] if layer['name'] == 'campus-audio-control')
carrier['properties'] = [
    {'name':'playAudio', 'type':'string', 'value':'native-audio/assets/gate-music-waterfalls-loop.mp3'},
    {'name':'audioLoop', 'type':'bool', 'value':True},
    {'name':'audioVolume', 'type':'float', 'value':1},
]
(OUT / 'gate.tmj').write_text(json.dumps(candidate, separators=(',', ':')) + '\n')
shutil.copy2(ROOT / 'source/gate-with-native-audio.js', OUT / 'native-audio/gate-with-native-audio.js')
for name in ('native-audio/assets/gate-music-waterfalls-loop.mp3', 'preserved-assets.json'):
    shutil.copy2(BASE / name, OUT / name)
shutil.copy2(ROOT / 'README.md', OUT / 'README.md')

# Preserve pure music and water separately as review inputs, outside the additive publication payload.
originals = ROOT / 'originals'
originals.mkdir(exist_ok=True)
for name in ('gate-music.mp3', 'cascade-soft.mp3'):
    shutil.copy2(BASE_ROOT / 'originals' / name, originals / name)

# Exact existing shared PNGs make the review package independently usable offline.
base_manifest = json.loads((BASE_ROOT / 'docs/PUBLICATION-MANIFEST.json').read_text())
for dependency in base_manifest['sharedDependencies']:
    source = BASE_ROOT / 'gate/map/tilesets' / Path(dependency['path']).name
    assert digest(source) == dependency['sha256']
    target = ROOT / 'dependencies' / dependency['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

pins = ROOT / 'source-audit/camera'
pins.mkdir(parents=True, exist_ok=True)
source_paths = {
    'camera.ts':'play/src/front/Api/Iframe/camera.ts',
    'CameraManager.ts':'play/src/front/Phaser/Game/CameraManager.ts',
    'GameMapPropertiesListener.ts':'play/src/front/Phaser/Game/GameMapPropertiesListener.ts',
    'HdpiManager.ts':'play/src/front/Phaser/Services/HdpiManager.ts',
    'WaScaleManager.ts':'play/src/front/Phaser/Services/WaScaleManager.ts',
    'GameMapProperties.ts':'libs/map-editor/src/types.ts',
}
source_manifest = []
for name, path in source_paths.items():
    data = subprocess.check_output(['git', '-C', str(REPO), 'show', f'{PIN}:{path}'])
    (pins / name).write_bytes(data)
    source_manifest.append({'path':path, 'sha256':hashlib.sha256(data).hexdigest(), 'url':f'https://github.com/BAWES-Universe/workadventure-universe/blob/{PIN}/{path}'})
(ROOT / 'SOURCE-MANIFEST.json').write_text(json.dumps({'engineCommit':PIN, 'files':source_manifest}, indent=2) + '\n')
files = [{'path':str(path.relative_to(ROOT / 'publish')), 'bytes':path.stat().st_size, 'sha256':digest(path)} for path in sorted(OUT.rglob('*')) if path.is_file()]
manifest = {
    'stage':'feedback-candidate-source-snapshot', 'grid':32, 'engineCommit':PIN,
    'proposedAdditivePath':'public/butterfly-town/gate-b/v2',
    'baseTmjSha256':digest(BASE / 'gate.tmj'), 'files':files,
    'fileCount':len(files), 'totalBytes':sum(item['bytes'] for item in files),
    'sharedDependencies':base_manifest['sharedDependencies'],
    'preservedOriginalAudio':[{'path':str(path.relative_to(ROOT)), 'bytes':path.stat().st_size, 'sha256':digest(path)} for path in sorted(originals.glob('*.mp3'))],
    'omittedModules':['native-audio/gate-camera-b.mjs', 'native-audio/gate-ambient-audio.mjs'],
}
(ROOT / 'PUBLICATION-MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'files':len(files), 'bytes':manifest['totalBytes'], 'tmjSha256':digest(OUT / 'gate.tmj')}))
