"""Package the native16 review map without the repository's 32px-only optimizer."""
from pathlib import Path
import json,zipfile,hashlib
r=Path(__file__).resolve().parents[1];target=Path('/workspace/bawes-sky-campus-review.zip');m=json.loads((r/'campus.tmj').read_text());files=[r/'campus.tmj',r/'runtime.js',r/'README.md',r/'review/VALIDATION.md',r/'source/runtime/run-local.sh',r/'source/runtime/serve-map.py']+[r/t['image'] for t in m['tilesets']]
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(files)):z.write(p,p.relative_to(r))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'entries':len(set(files)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
