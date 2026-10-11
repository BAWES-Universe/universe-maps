from pathlib import Path
import zipfile,hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'deliverables';D.mkdir(exist_ok=True)
# Core bytes must still match the last independent-review input.
core=json.loads((R/'CORE-FREEZE.json').read_text())
for a in core['files']:assert hashlib.sha256((R/a['path']).read_bytes()).hexdigest()==a['sha256'],a['path']
packages=[]
for name,files in [('lantern-congress-runtime.zip',[*sorted((R/'map32').glob('*')),R/'README.md',R/'integration/ROOM-SETUP.md',R/'RUNTIME-MANIFEST.json']),('lantern-congress-source-complete.zip',[p for p in sorted(R.rglob('*'))if p.is_file()and'deliverables'not in p.relative_to(R).parts and'__pycache__'not in p.parts and p.name not in['PACKAGE-MANIFEST.json','SOURCE-FREEZE.json']])]:
 entries=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in files]
 with zipfile.ZipFile(D/name,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for p in files:z.write(p,p.relative_to(R).as_posix())
  z.writestr('ARCHIVE-CONTENTS.json',json.dumps({'files':entries,'exclusions':['deliverables (recursive ZIPs)','Python bytecode caches','self-referential package/source manifests']},indent=2)+'\n')
 with zipfile.ZipFile(D/name)as z:
  assert z.testzip()is None
  for a in entries:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256']
 packages.append({'path':'deliverables/'+name,'bytes':(D/name).stat().st_size,'sha256':hashlib.sha256((D/name).read_bytes()).hexdigest(),'entryCount':len(entries)+1,'crcAndAllPayloadHashesVerified':True})
(R/'PACKAGE-MANIFEST.json').write_text(json.dumps({'packages':packages,'runtimePublished':False,'liveMediaVerified':False},indent=2)+'\n');print(json.dumps(packages,indent=2))
