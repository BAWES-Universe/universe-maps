"""Archive only referenced native dependencies; no optimizer or upload step."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent;root=R/'compact';m=json.loads((root/'campus.tmj').read_text())
names=sorted({s['image'] for s in m['tilesets']}|{'campus.tmj','runtime.js','index.html'})
checks=R/'evidence/compact-final-checks.json'
tested=False
if checks.exists():
 rows=json.loads(checks.read_text());tested=len(rows)>=170 and all(r['pass'] for r in rows)
status='runtime-tested-unpublished-review' if tested else 'unpublished-validation-in-progress'
(root/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BAWES sky campus</title><style>body{{font:18px system-ui;background:#112331;color:#f8edda;max-width:760px;margin:60px auto;padding:24px}}a{{color:#ffcf77}}</style><h1>BAWES sky campus</h1><p>Status: {status}.</p><p><a href="campus.tmj">TMJ map</a> · <a href="PUBLICATION.json">Package record</a></p><p>Import the hosted TMJ URL into Universe to play. Keep the map, runtime and art directory together. This package index is not the game client.</p><p>Desktop and mobile viewport tests use cloud Chromium. Physical-phone testing and public hosting are separate.</p></html>''')
hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
(root/'PUBLICATION.json').write_text(json.dumps({'status':status,'tileSize':16,'packaging':'self-contained native assets; no resampling','recoveryBranch':'recovery/bawes-sky-campus-20261021','proposedDestination':'gh-pages:previews/bawes-sky-campus-recovery-20261021/','files':hashes},indent=2)+'\n')
target=R/'bawes-sky-campus-native-review.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in names+['PUBLICATION.json']:z.write(root/n,n)
with zipfile.ZipFile(target) as z:assert z.testzip() is None
record={'archive':target.name,'status':status,'entries':len(names)+1,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'mapSha256':hashes['campus.tmj'],'runtimeSha256':hashes['runtime.js']}
(R/'evidence/native-archive-integrity.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
