"""Create a self-contained native16 runtime staging directory. Never uploads."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent
source=R.parent/'source/native-cafe-trial/playable'
target=R/'package';(target/'art').mkdir(parents=True,exist_ok=True)
m=json.loads((source/'campus.tmj').read_text())
for s in m['tilesets']:
 p=(source/s['image']).resolve();blob=p.read_bytes();name=hashlib.sha256(blob).hexdigest()[:20]+'.png'
 (target/'art'/name).write_bytes(blob);s['image']='art/'+name
for p in m.get('properties',[]):
 if p['name']=='script':p['value']='runtime.js'
(target/'campus.tmj').write_text(json.dumps(m,separators=(',',':')))
shutil.copyfile(source/'runtime.js',target/'runtime.js')
(target/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BAWES sky campus recovery review</title><style>body{font:18px system-ui;background:#112331;color:#f8edda;max-width:760px;margin:60px auto;padding:24px}a{color:#ffcf77}</style><h1>BAWES sky campus</h1><p>Recovery review candidate. Acceptance testing is in progress; this is not a published or approved map.</p><p><a href="campus.tmj">TMJ map</a> · <a href="PUBLICATION.json">Package record</a></p><p>Keep the TMJ, runtime.js and art directory together. Import the map URL into the Universe client to play. This page is a package index, not a substitute for the game client.</p></html>''')
files={str(p.relative_to(target)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.rglob('*')) if p.is_file() and p.name!='PUBLICATION.json' and 'dist' not in p.relative_to(target).parts and p.name!='vite.config.ts'}
(target/'PUBLICATION.json').write_text(json.dumps({'status':'unpublished-test-candidate','tileSize':16,'sourceCommit':'08485166c2f9dfb208318ef862a46a031cbfdb8a','recoveryBranch':'recovery/bawes-sky-campus-20261021','proposedDestination':'gh-pages:previews/bawes-sky-campus-recovery-20261021/','files':files},indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':sum(p.stat().st_size for p in target.rglob('*') if p.is_file()),'target':str(target)}))
