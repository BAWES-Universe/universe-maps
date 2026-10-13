from pathlib import Path
import zipfile,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];D=Path('/workspace/scratch/41c8dbf833be/flagship-c-delivery');D.mkdir(exist_ok=True)
items=[('review/building-c-compiled-overview.png','astral-flagship-c-v09-overview.png','image'),('review/building-c-south-sequence-native.png','astral-flagship-c-v09-entry-native.png','image'),('review/building-c-hall-east-sequence-native.png','astral-flagship-c-v09-side-porch-native.png','image'),('review/building-c-focus-source-calculated-sheet.png','astral-flagship-c-v09-focus-source-calculated.png','image'),('integration/ROOM-SETUP.md','astral-flagship-c-v09-room-setup.md','report')]
for src,name,typ in items:shutil.copy2(R/src,D/name)
runtime=D/'astral-flagship-c-v09-runtime.zip'
with zipfile.ZipFile(runtime,'w',zipfile.ZIP_DEFLATED,compresslevel=8)as z:
 for p in sorted((R/'map32').iterdir()):
  if p.is_file():z.write(p,'map32/'+p.name)
 for rel in ['README.md','PROVENANCE.md','RUNTIME-MANIFEST.json','integration/ROOM-SETUP.md','validation/ACCEPTANCE.md']:
  z.write(R/rel,rel)
source=D/'astral-flagship-c-v09-standalone-source.zip'
excluded=[]
for p in R.rglob('*.png'):
 if 'review' in p.parts and ('-empty-native' in p.name or '-occupied-native' in p.name or p.name in {'runtime-empty-native.png','runtime-collision-overlay-native.png'}):excluded.append(str(p.relative_to(R)))
(R/'ARCHIVE-CONTENTS.json').write_text(json.dumps({'scope':'Standalone inputs, runtime, source, masters/prompts, scripts, proofs and selected review sheets','excludedRegenerableFullCanvasReviewPngs':excluded,'reason':'Avoid duplicate giant composites; exact source hashes and deterministic render commands are preserved. All art/source/runtime inputs are included.'},indent=2)+'\n')
freezeFiles=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(R.rglob('*'))if p.is_file()and '__pycache__'not in p.parts and p.suffix not in {'.pyc','.log'} and p.name!='SOURCE-FREEZE.json']
(R/'SOURCE-FREEZE.json').write_text(json.dumps({'status':'Frozen C reviewed source/runtime; known native camera limits documented; actual room acceptance pending','excludedLogs':True,'files':freezeFiles},indent=2)+'\n')
with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=8)as z:
 for p in sorted(R.rglob('*')):
  if '__pycache__' in p.parts:continue
  if p.is_dir():z.writestr(str(p.relative_to(R))+'/',b'');continue
  if not p.is_file()or p.suffix in {'.pyc','.log'} or str(p.relative_to(R))in excluded:continue
  z.write(p,p.relative_to(R))
for p in [runtime,source]:
 with zipfile.ZipFile(p)as z:assert z.testzip()is None
items +=[('',runtime.name,'other'),('',source.name,'other')]
rows=[]
for _,name,typ in items:
 p=D/name;rows.append({'local_path':str(p),'filename':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'library_artifact_type':typ})
(R.parent/'grand-auditorium-v09-local-delivery-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
(D/'upload-request.json').write_text(json.dumps({'uploads':[{'local_path':r['local_path'],'purpose':'create_library_file','library_artifact_type':r['library_artifact_type']}for r in rows]},indent=2)+'\n')
print(json.dumps(rows,indent=2))
