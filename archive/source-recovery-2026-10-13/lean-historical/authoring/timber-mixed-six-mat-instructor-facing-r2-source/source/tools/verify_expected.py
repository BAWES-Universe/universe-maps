from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];e=json.loads((R/'EXPECTED-OUTPUTS.json').read_text());bad=[]
for f in e['files']:
 p=R/f['path'];actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 if actual!=f['sha256']:bad.append(dict(path=f['path'],expected=f['sha256'],actual=actual))
print(json.dumps(dict(outputs=len(e['files']),allExact=not bad,failures=bad),indent=2));assert not bad
