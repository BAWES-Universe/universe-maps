#!/usr/bin/env python3
"""Build Gate B beside an immutable source06 gate directory; never overwrite input."""
from pathlib import Path
import argparse,shutil,json,hashlib

def build(baseline,output):
 baseline=Path(baseline).resolve();output=Path(output).resolve();here=Path(__file__).resolve().parent
 assert baseline!=output and baseline not in output.parents,'Use an independent output directory'
 assert not output.exists(),'Choose a fresh output directory'
 assert (baseline/'map/gate.tmj').is_file()
 shutil.copytree(baseline,output)
 m=json.loads((output/'map/gate.tmj').read_text())
 assert (m['width'],m['height'],m['tilewidth'],m['tileheight'])==(30,45,32,32)
 start=next(l for l in m['layers']if l['name']=='start');gid=next(x for x in start['data']if x)
 start['data']=[0]*len(start['data']);start['data'][35*m['width']+15]=gid
 for l in m['layers']:
  for o in l.get('objects',[]):
   if o['name']=='gate-spawn':o['x'],o['y']=496,1136
   if o['name']=='start':o['x'],o['y'],o['width'],o['height']=464,1120,64,32
 m['properties']=[p for p in m['properties']if p['name']!='nativeNearbyAudio']
 m['properties'].append(json.loads((here/'gateAmbientAudio-property.json').read_text()))
 for p in m['properties']:
  if p['name']=='campusVersion':p['value']='gate-b-detail-to-monument'
 m['properties'].append({'name':'gateCameraVersion','type':'string','value':'B: progressive pullback, hold, native manual opt-out'})
 (output/'map/gate.tmj').write_text(json.dumps(m,separators=(',',':'))+'\n')
 for src,dest in [('gate-entry-b.js','gate-with-native-audio.js'),('gate-camera-b.mjs','gate-camera-b.mjs'),('gate-ambient-audio.mjs','gate-ambient-audio.mjs')]:
  shutil.copy2(here/src,output/'map/native-audio'/dest)
 shutil.copy2(here.parent/'gate/map/native-audio/assets/gate-music-waterfalls-loop.mp3',output/'map/native-audio/assets/gate-music-waterfalls-loop.mp3')
 return [{'path':str(p.relative_to(output)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(output.rglob('*'))if p.is_file()]
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('baseline');p.add_argument('output');a=p.parse_args()
 print(json.dumps(build(a.baseline,a.output),indent=2))
