"""Package the isolated optimized native16 map and current review evidence."""
from pathlib import Path
import json,zipfile,hashlib,subprocess
r=Path(__file__).resolve().parents[1];target=Path('/workspace/bawes-sky-campus-review.zip')
checks=json.loads((r/'review/optimizer-equivalence.json').read_text());assert checks['allLayerPixelsAndTilePropertiesEqual'] and checks['runtimeScriptByteIdentical']
files=[(p,p.relative_to(r/'dist')) for p in (r/'dist').rglob('*') if p.is_file()]
names=['review/COUNTER-RESUME-2026-10-20.md','review/COUNTER-CANDIDATE-ASSESSMENT.md','review/counter-candidate-assessment.json','review/counter-no-integration-checks.json','review/counter-registration-comparison.png','review/counter-rejected-local-alignment.png','review/counter-native-384-assessment.png','review/counter-runtime-before-unchanged.png','review/COUNTER-AND-NAVIGATION.md','review/counter-source-inspection.png','review/stage-navigation-before.json','review/stage-navigation-after.json','review/entrance-proximity-check.json','README.md','review/REPLACEMENT-INTERIOR.md','review/OUTDOOR-RESTORATION-PASS.md','review/CAFE-RESTORATION.md','review/REMAINING-DISTRICTS.md','review/geometry.json','review/optimizer-equivalence.json','review/cafe-preservation.json','review/cafe-clearance.json','review/cafe-runtime-checks.json','review/district-runtime-checks.json','review/stage-restored.png','review/conservatory-restored.png','review/district-occupied-audience.png','review/district-occupied-conservatory-lounge.png','review/cafe-full.png','review/cafe-native-close.png','review/cafe-occupied-cafe-lounge.png','review/cafe-occupied-cafe-armchair.png','review/cafe-occupied-cafe-bar.png','review/runtime-campus-outdoor-restored.png','review/runtime-campus-cafe-restored.png','source/cafe-candidates/counter-adaptation-blocker.json']
files += [(r/n,Path(n)) for n in names]
files += [(p,p.relative_to(r)) for folder in ['review/resume-2026-10-20','source/counter-repair-request'] for p in sorted((r/folder).rglob('*')) if p.is_file()]
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p,n in files:z.write(p,n)
 z.writestr('REVIEW-COMMIT.txt',subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode())
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'entries':len(files)+1,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
