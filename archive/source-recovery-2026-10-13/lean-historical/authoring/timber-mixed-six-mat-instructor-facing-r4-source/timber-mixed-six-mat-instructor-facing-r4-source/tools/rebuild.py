from pathlib import Path
import subprocess,sys,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'timber-mixed-six-mat-instructor-facing-r4';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in ['build.py','check_geometry.py']:subprocess.run([sys.executable,str(R/'tools'/f)],check=True,cwd=R)
native=json.loads((R/'evidence/NATIVE-ROUTES.json').read_text())
assert native['allRoutesPass'] and not native['failures'] and native['ordinaryFailures']==native['sameCellFailures']==native['bodyCollisionSamples']==0
assert len(native['startupPositions'])==4 and native['everyAdmittedCellArrivalAndReturnFromEachStartup']
for name,h in native['inputHashes'].items():assert sha(O/name)==h,'Native evidence stale: '+name
shutil.copyfile(R/'evidence/NATIVE-ROUTES.json',O/'NATIVE-ROUTES.json');shutil.copyfile(R/'GUIDE.md',O/'GUIDE.md')
manifest={'slug':O.name,'world':[960,864],'nativeTileSize':32,'status':'Unpublished candidate; user design approval and live testing separate','files':{str(p.relative_to(O)):sha(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}}
(O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
expected=R/'EXPECTED-OUTPUTS.json'
if expected.exists():
 e=json.loads(expected.read_text());got={str(p.relative_to(O)):sha(p) for p in sorted(O.rglob('*')) if p.is_file()};assert e==got,'Runtime output differs from immutable expected hashes'
 print('PASS byte-exact rebuild:',len(got),'runtime files')
else:print('Initial build; expected hash freeze not yet installed')
