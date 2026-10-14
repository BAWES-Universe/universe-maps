from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];out=R/'Butterfly-Town-v2-source-review.zip';files=[]
for folder in ['map','baseline-map','art-source','qa','tools','tests','candidate']:
 for p in (R/folder).rglob('*'):
  if not p.is_file() or any(n in p.parts for n in ['__pycache__','node_modules','.git']):continue
  if p.suffix.lower() in ['.wav','.pyc']:continue
  if p.name=='inspect-v2.cjs':continue
  files.append(p)
for name in ['README.md','RELEASE-V2.json','layout.json','AUDIO-INTEGRATION.md','CLAUDE-REVIEW.md']:files.append(R/name)
for pattern in ['scenery-*.json','scenery-*.log','state-tests.json','state-tests.log','engine-validation.json','engine-validation.log','repository-build.log','frozen-v1-sha256.json','closed-cavities.json','build-manifest.json','before-*.png','after-*.png','rendered-v2.json','click-arrival.json','water-*.json','water-*.log','water-*.png','butterfly-v2-pixels.json','butterfly-*.png']:
 files.extend((R/'evidence').glob(pattern))
files.extend(p for p in (R/'evidence/water-regression-before').glob('*') if p.is_file())
files.extend(p for p in (R/'evidence').rglob('*') if p.is_file() and p.suffix in ['.json','.md'] and 'water-regression-before' not in str(p))
files.extend((R/'evidence').glob('integrated-*.png'))
files.extend((R/'evidence').glob('gate-revision-*.png'))
files.extend((R/'evidence/gate-revision').glob('*.png'))
files.extend((R/'evidence/boundary-audit').glob('*.png'))
files=sorted(set(p for p in files if not any(token in p.name.lower() for token in ['library','upload','materializ','source-package'])));
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6) as z:
 for p in files:z.write(p,'Butterfly-Town-v2/'+str(p.relative_to(R)))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None; names=z.namelist()
 assert 'Butterfly-Town-v2/map/butterfly-town.tmj' in names
 assert 'Butterfly-Town-v2/qa/scenery-tests.js' in names
 assert 'Butterfly-Town-v2/candidate/public/butterfly-town/v2/scripts/town-audio-runtime.mjs' in names
 assert 'Butterfly-Town-v2/candidate/public/butterfly-town/v2/assets/audio/cascade-soft.mp3' in names
report={'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(files),'zipIntegrity':'passed'}
(R/'evidence/source-package-v2.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
