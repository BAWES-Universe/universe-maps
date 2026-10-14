from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
folders=['publish','source','pinned-source','tests','baseline','dependencies','geometry-evidence','framing','tools','validation']
files=[]
for folder in folders:
 files.extend(p for p in (R/folder).rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.suffix!='.pyc')
for name in ['README.md','SOURCE-FINDINGS.md','CANDIDATE-MANIFEST.json','INTEGRITY-VERIFICATION.json','CAMERA-VERIFICATION.json','PIN-ORIGINS.json','V3-TO-V4-SCRIPT.patch','GEOMETRY-INTEGRATION-MANIFEST.json','CALIBRATION-V3-REFERENCE.md','MOBILE-DETECTION-V3-REFERENCE.md','package.json','FINAL-TEST-RESULTS.txt']:files.append(R/name)
files=sorted(set(files));entries=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in files]
(R/'CHECKPOINT-CONTENTS.json').write_text(json.dumps({'scope':'Separate Gate B v4 map/script and exact dependency copies; source-class evidence only; no engine patch','files':entries},indent=2)+'\n');files.append(R/'CHECKPOINT-CONTENTS.json')
out=R/'Gate-B-v4-static-view-review.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6)as z:
 for p in files:z.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None
 for item in entries:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
 assert not any('engine-patch'in n or 'camera-adapter'in n for n in z.namelist())
d={'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(files),'archiveHashesVerified':True,'enginePatchIncluded':False};(R/'CHECKPOINT-VERIFICATION.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
