from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path(__file__).resolve().parents[1];D=Path('/workspace/scratch/41c8dbf833be/flagship-v03-library-release');D.mkdir(parents=True,exist_ok=True)
def excluded(p):
 s=str(p.relative_to(R));return s in ['SOURCE-FREEZE.json','library-receipt.json']or'__pycache__'in s or s.endswith('.pyc')or p.name=='native-route-samples.f64'or p.name.startswith('divider-experiment')or p.name=='inspect_route.mjs'
files=[p for p in sorted(R.rglob('*'))if p.is_file()and not excluded(p)]
manifest={'title':'Astral Concourse / Flagship v03 Foyer and Terrace','status':'Local reviewed candidate; user visual approval and publication pending','nativeTileSize':32,'worldPixels':[2560,1920],'originalVersionsPreserved':True,'runtimeFiles':json.load(open(R/'validation/package-verification.json'))['runtimeFiles'],'files':{str(p.relative_to(R)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in files},'omittedReproducibleInputs':['validation/native-route-samples.f64 is retained losslessly as native-route-samples.f64.gz','Superseded diagnostic route experiments are not in this final checkpoint'],'independentReview':'29 zone/schema checks and9 all-sample replay checks pass; no live/media acceptance'}
(R/'SOURCE-FREEZE.json').write_text(json.dumps(manifest,indent=2)+'\n');files.append(R/'SOURCE-FREEZE.json')
with zipfile.ZipFile(D/'astral-flagship-v03-complete-source.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in files:z.write(p,'astral-flagship-v03/'+str(p.relative_to(R)),compress_type=zipfile.ZIP_STORED if p.suffix=='.gz'else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(D/'astral-flagship-v03-runtime-and-setup.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted((R/'map32').iterdir()):z.write(p,str(p.relative_to(R)))
 for name in ['README.md','integration/ROOM-SETUP.md','VALIDATION-SUMMARY.md','validation/package-verification.json']:z.write(R/name,name)
items=[('review/runtime-overview.png','astral-flagship-v03-overview.png'),('review/runtime-indoor-foyer-occupied-native.png','astral-flagship-v03-foyer-native.png'),('review/runtime-terrace-occupied-native.png','astral-flagship-v03-terrace-native.png'),('review/runtime-furniture-depth-native.png','astral-flagship-v03-depth-native.png'),('integration/ROOM-SETUP.md','astral-flagship-v03-room-setup.md')]
for src,dst in items:shutil.copy2(R/src,D/dst)
receipts=[]
for p in sorted(D.iterdir()):
 if p.is_file() and p.name!='local-artifact-manifest.json':receipts.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'local-artifact-manifest.json').write_text(json.dumps(receipts,indent=2)+'\n');print(json.dumps(receipts,indent=2))
