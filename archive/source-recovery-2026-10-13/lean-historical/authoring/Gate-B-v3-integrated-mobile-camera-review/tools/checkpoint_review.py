from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
roots=['integrated','source','pinned-source','tests','baseline','dependencies','geometry-evidence','filmstrips','tools']
files=[]
for root in roots:
 for p in (R/root).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':files.append(p)
for name in ['README.md','CALIBRATION.md','CAMERA-ISSUE-DRAFTS.md','PUBLICATION-PLAN.md','INTEGRATED-MANIFEST.json','INTEGRATED-VERIFICATION.json','GEOMETRY-INTEGRATION-MANIFEST.json','PIN-ORIGINS.json','VERIFICATION.json','MOBILE-ARRIVAL-EXPERIMENT.json','MOBILE-REVERSALS.json','TRANSITION-EDGE-CASES.json','package.json','FINAL-TEST-RESULTS.txt','DEVICE-DETECTION.json','MOBILE-DETECTION-EVIDENCE.md']:
 files.append(R/name)
files=sorted(set(files))
entries=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest={'scope':'Selected unpublished integrated Gate B v3; exact shared dependencies and source-class review evidence. No engine patch or earlier review-control candidate included.','files':entries}
(R/'CHECKPOINT-CONTENTS.json').write_text(json.dumps(manifest,indent=2)+'\n');files.append(R/'CHECKPOINT-CONTENTS.json')
archive=R/'Gate-B-v3-integrated-mobile-camera-review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(archive) as z:
 for e in entries:assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256']
 assert not any('engine-patch' in n or n.startswith('candidates/') or 'setViewport' in n for n in z.namelist())
receipt={'path':str(archive),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':len(files),'archiveHashesVerified':True,'enginePatchIncluded':False}
(R/'CHECKPOINT-VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
