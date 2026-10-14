from pathlib import Path
import tempfile,shutil,json,hashlib,subprocess,os
R=Path(__file__).resolve().parents[1];C=Path(tempfile.mkdtemp(prefix='h039-own-rebuild-'));count=0
for directory in ['art','source','tools','licenses']:
 for p in (R/directory).rglob('*'):
  if not p.is_file()or p.name=='mill-native.png'or '__pycache__'in p.parts:continue
  q=C/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True)
  if p.suffix.lower()=='.png':
   try:os.link(p,q)
   except OSError:shutil.copy2(p,q)
  else:shutil.copy2(p,q)
  count+=1
shutil.copy2(R/'README.md',C/'README.md');count+=1
proc=subprocess.run(['sh','tools/rebuild.sh'],cwd=C,capture_output=True,text=True);(R/'validation/exact-rebuild-log.txt').write_text(proc.stdout+proc.stderr)
def inv(root):return{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in root.rglob('*')if p.is_file()}
a=inv(R/'runtime');b=inv(C/'runtime');missing=sorted(set(a)-set(b));extra=sorted(set(b)-set(a));different=[p for p in a.keys()&b.keys()if a[p]!=b[p]];result=dict(sourceFilesCopied=count,runtimeFiles=len(a),exitCode=proc.returncode,exactRuntime=not(missing or extra or different or proc.returncode),missing=missing,extra=extra,different=different,scope='Author fresh empty-output source-only rebuild; not independent reviewer acceptance.',temporaryPath=str(C),ownDisposableRebuildRemoved=False)
if result['exactRuntime']:shutil.rmtree(C);result['ownDisposableRebuildRemoved']=True
(R/'validation/exact-rebuild-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['exactRuntime']
