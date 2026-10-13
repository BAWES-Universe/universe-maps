from pathlib import Path
import json,hashlib,shutil,subprocess,sys,datetime
R=Path(__file__).resolve().parents[1];T=Path(sys.argv[1]if len(sys.argv)>1 else'/tmp/h025-clean-source');assert not T.exists(),'Never overwrite a pre-existing clean slot'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={};T.mkdir()
for name in ['source','art','tools','licenses']:
 for p in sorted((R/name).rglob('*')):
  if p.is_file()and'__pycache__'not in p.parts:
   rel=p.relative_to(R);dest=T/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);inputs[str(rel)]=sha(p)
for name in ['README.md']:shutil.copy2(R/name,T/name);inputs[name]=sha(R/name)
# Inputs only: no generated map32/review/validation/evidence or root spawn result.
assert not any((T/q).exists()for q in ['map32','review','validation','evidence','NATIVE-SPAWN-CHECKS.json'])
E=R/'evidence/clean-rebuild';E.mkdir(parents=True,exist_ok=True)
with (E/'rebuild.log').open('w')as f:process=subprocess.run(['sh','tools/rebuild.sh'],cwd=T,stdout=f,stderr=subprocess.STDOUT)
expected={str(p.relative_to(R/'map32')):sha(p)for p in(R/'map32').rglob('*')if p.is_file()};actual={str(p.relative_to(T/'map32')):sha(p)for p in(T/'map32').rglob('*')if p.is_file()};ok=process.returncode==0 and expected==actual
report={'scope':'Private source-only rebuild without any original runtime or evidence inputs; actual emitted runtime bytes compared.','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':str(T),'inputCount':len(inputs),'inputs':inputs,'exitCode':process.returncode,'runtimeFiles':len(expected),'runtimeExact':expected==actual,'pass':ok,'expected':expected,'actual':actual};(E/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['inputs','expected','actual']},indent=2))
if ok:
 allfiles={str(p.relative_to(T)):sha(p)for p in T.rglob('*')if p.is_file()};size=sum(p.stat().st_size for p in T.rglob('*')if p.is_file());assert all(sha(T/p)==h for p,h in allfiles.items());shutil.rmtree(T);(E/'cleanup.json').write_text(json.dumps({'scope':'Only this tool-owned disposable exact-verified successful source-only build was removed; all master/source/proof/candidate material stays in H025.','path':str(T),'removedBytes':size,'verifiedFiles':allfiles,'removed':not T.exists()},indent=2)+'\n')
else:sys.exit(1)
