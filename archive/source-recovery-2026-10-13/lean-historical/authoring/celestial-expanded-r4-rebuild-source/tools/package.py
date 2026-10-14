from pathlib import Path
import hashlib,json,zipfile,datetime
R=Path(__file__).resolve().parents[1];P=R/'celestial-transit-garden'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for folder in ['map32','source','review','validation'] for p in (P/folder).rglob('*') if p.is_file()]
freeze={'revision':'celestial-transit-garden-expanded-r2','createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(p.relative_to(P)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)]};freeze['aggregateSha256']=hashlib.sha256(json.dumps(freeze['files'],sort_keys=True).encode()).hexdigest();(P/'FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
with zipfile.ZipFile(R/'celestial-transit-garden-expanded-r2-runtime.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((P/'map32').glob('*')):z.write(p,'map32/'+p.name)
 z.write(R/'README.md','README.md')
with zipfile.ZipFile(R/'celestial-transit-garden-expanded-r2-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for directory in [R/'tools',R/'source',P/'validation']:
  for p in sorted(directory.rglob('*')):
   if p.is_file() and '__pycache__' not in str(p) and p.name not in ['generated-wide-context.png','expanded-context.png','final-composite.png','preservation-alpha.png','registration.json','register_context.py']:z.write(p,str(p.relative_to(R)))
 z.write(R/'README.md','README.md')
 z.write(P/'FREEZE.json','celestial-transit-garden/FREEZE.json')
print('FREEZE',freeze['aggregateSha256'])
for p in R.glob('*.zip'):print(p.name,p.stat().st_size,sha(p))
