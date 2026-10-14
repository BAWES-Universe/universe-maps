"""Package the current map-only review and receipts, excluding helpers and engine patches."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
excluded = {'PACKAGE-MANIFEST.json','library-receipt.json','ZIP-VERIFICATION.json'}
files = sorted(path for path in ROOT.rglob('*') if path.is_file() and '.library-helper' not in path.parts and path.suffix != '.zip' and path.name not in excluded)
assert not any(path.name in {'PRESERVE-NATIVE-FOLLOW.patch','build_engine_patch.py'} or 'engine-patch' in path.parts or 'proposal-native-api' in path.parts for path in files)
records = [{'path':str(path.relative_to(ROOT)), 'bytes':path.stat().st_size, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path in files]
(ROOT / 'PACKAGE-MANIFEST.json').write_text(json.dumps({'files':records},indent=2)+'\n')
files.append(ROOT / 'PACKAGE-MANIFEST.json')
archive = ROOT / 'Gate-B-v2-map-only-review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as bundle:
    for path in files: bundle.write(path,str(path.relative_to(ROOT)))
with tempfile.TemporaryDirectory(prefix='gate-b-v2-package-') as folder:
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        bundle.extractall(folder)
    for record in records:
        assert hashlib.sha256((Path(folder) / record['path']).read_bytes()).hexdigest() == record['sha256']
    result = subprocess.run(['python',str(Path(folder) / 'tools/verify_candidate.py')],capture_output=True,text=True)
    assert result.returncode == 0,result.stdout+result.stderr
report = {'file':str(archive),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':len(files),'zipCrcPassed':True,'extractedHashesPassed':True,'extractedVerificationPassed':True,'enginePatchIncluded':False}
(ROOT / 'ZIP-VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
