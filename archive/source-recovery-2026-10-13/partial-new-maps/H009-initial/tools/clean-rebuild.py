from pathlib import Path
import json,hashlib,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1];tag=sys.argv[1]if len(sys.argv)>1 else'r1';C=Path('/tmp')/(R.name+'-'+tag+'-clean-build');assert not C.exists();C.mkdir();files={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for folder in ['art','source','tools','tests','licenses']:
 for p in(R/folder).rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts and p.relative_to(R).as_posix()!='source/layout-definition.json':
   rel=p.relative_to(R);dst=C/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);files[str(rel)]=sha(p)
shutil.copy2(R/'README.md',C/'README.md');files['README.md']=sha(R/'README.md');(R/'evidence'/f'{tag}-clean-source-inputs.json').write_text(json.dumps({'sourceOnly':True,'files':files},indent=2))
with(R/'evidence'/f'{tag}-clean-build-log.txt').open('w')as log:subprocess.run(['bash','tools/rebuild.sh'],cwd=C,stdout=log,stderr=subprocess.STDOUT,check=True)
live={p.name:sha(p)for p in(R/'runtime').iterdir()if p.is_file()};rebuilt={p.name:sha(p)for p in(C/'runtime').iterdir()if p.is_file()};assert live==rebuilt
report={'allPass':True,'sourceOnly':True,'sourceInputs':len(files),'runtimeFiles':len(live),'runtimeHashes':live,'cleanRuntimeHashes':rebuilt,'runtimeByteExact':True,'cleanPath':str(C),'scope':'Author exact source-only clean rebuild and all offline gates; independent review and live gameplay remain separate.'};(R/'evidence/author-clean-rebuild.json').write_text(json.dumps(report,indent=2))
receipt={'path':str(C),'reason':'Own disposable source-only build has passed every gate and reproduced all runtime bytes exactly. Original sources, masters, evidence and frozen packages are preserved.','sourceInputs':len(files),'runtimeHashes':rebuilt,'verifiedBeforeRemoval':True};shutil.rmtree(C);receipt['removed']=not C.exists();(R/'evidence'/f'{tag}-clean-build-cleanup.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:v for k,v in report.items()if'Hashes'not in k},indent=2))
