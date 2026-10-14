from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parent
names=['tea-keyboard-retest','tea-touch','roof-camera','door-demo-retest','desktop-retest','departure-rejoin-retest','public-mobile-retest','audio-stop']
results=[]
for name in names:
 print('RUN',name,flush=True)
 with (r/(name+'.log')).open('w') as log:p=subprocess.run(['/workspace/scratch/universe-local/local-env.sh','node',str(r/(name+'.cjs'))],stdout=log,stderr=subprocess.STDOUT,timeout=360)
 data=json.loads((r/'evidence'/(name+'-results.json')).read_text());row={'script':name,'exit':p.returncode,'passed':sum(c['status']=='pass' for c in data['checks']),'failed':[c['name'] for c in data['checks'] if c['status']!='pass']};results.append(row);print(row,flush=True)
 (r/'suite-results.json').write_text(json.dumps(results,indent=2))
