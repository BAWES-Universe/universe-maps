from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'candidate'
for p in (R/'evidence').glob('*.json'):
 j=json.loads(p.read_text())
 for f,h in j.get('inputHashes',{}).items():assert hashlib.sha256((O/f).read_bytes()).hexdigest()==h,(f,'stale native evidence')
 dest=O/'source'/p.name if p.name in ['SEAT-ROUTE-TRACES.json','GARDEN-ROUTE-TRACES.json'] else O/p.name
 shutil.copy2(p,dest)
print('Restored frozen, hash-bound source replay evidence; no new engine test was run.')
