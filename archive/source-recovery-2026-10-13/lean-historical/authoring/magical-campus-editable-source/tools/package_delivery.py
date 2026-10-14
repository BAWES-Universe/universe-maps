"""Build relative-path delivery ZIPs; preserve bulky evidence separately."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def tree(*names):
 out=set()
 for name in names:
  p=R/name
  if p.is_file():out.add(p)
  elif p.is_dir():out.update(q for q in p.rglob('*') if q.is_file() and '__pycache__' not in q.parts)
  else:raise FileNotFoundError(p)
 return out
runtime=tree('map16','runtime16','runtime/vendor','runtime/assets','runtime/server.py','audio','gate')
inventory={'scope':'Relative bundled local runtime files. Source provenance paths are not runtime fetch dependencies.','files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(runtime)]}
(R/'docs/portable-runtime-files.json').write_text(json.dumps(inventory,indent=2)+'\n')
subprocess.run([sys.executable,str(R/'tools/write_delivery.py')],check=True)
delivery=json.loads((R/'DELIVERY.json').read_text())
reports=set()
for value in delivery['evidence'].values():
 if isinstance(value,str) and value.endswith('.json') and (R/value).exists():reports.add(R/value)
for value in ['runtime/results/continuous-campus16-walk-audio-energy.json','runtime/results/continuous-campus16-timestamp-reconciliation.json','runtime/results/continuous-campus16-walk-recording-manifest.json']:
 reports.add(R/value)
common=tree('README.md','DELIVERY.json','docs')|reports
sets=[('magical-campus-runnable-preview.zip',runtime|common,'Self-contained local preview. Extract and run python3 runtime/server.py --port 8850, then open http://127.0.0.1:8850/runtime16/?gate=1. Dependencies: Python standard library and a browser. All browser assets are relative and bundled. Source provenance and video paths in DELIVERY.json refer to the companion source package and separate evidence, where omitted here.'),('magical-campus-native-maps.zip',tree('map16','gate/map')|common,'Native Tiled payload: map16/magical-campus.tmj and gate/map/gate.tmj with every atlas and native script. Real room URLs are blank. Preview code, production audio routing and registration are separate. Runtime and source evidence paths in DELIVERY.json are shared references, not dependencies of the TMJs.'),('magical-campus-editable-source.zip',tree('sources','layers','effects','tools','map16','runtime/vendor','runtime/assets','map/magical-campus.tmj','map/collision-grid.json','map/compile-manifest.json')|common,'Editable frozen native layers, geometry, masks and compiler inputs. With Python Pillow and NumPy installed, run python3 tools/rebuild_frozen_layers.py, then python3 tools/compile16.py. The reconstruction checks exact RGBA bytes. Recompilation intentionally resets runtime acceptance to pending; it does not inherit a recorded proof. map/ is historical 8px compiler input only and omits its superseded atlas payload. Use map16/ as the native default. Original full-resolution art masters and generation history are preserved separately in the original module packages; source provenance retains their locations. The original build_campus.py additionally requires those original sibling trees. Recorded videos are delivered separately.')]
result={'defaultMap':'map16/magical-campus.tmj','archives':[],'videos':'Separate raw and converted evidence; no recorder chunks or decoded WAVs are bundled.'}
for name,files,note in sets:
 p=D/name;index=[]
 with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  z.writestr('BUNDLE-CONTENTS.txt',note+'\n')
  for f in sorted(files):
   relative=f.relative_to(R).as_posix();assert not relative.startswith('/') and '..' not in Path(relative).parts
   assert '-chunk-' not in relative and f.suffix.lower() not in ('.wav','.webm','.mp4')
   z.write(f,relative);index.append({'path':relative,'bytes':f.stat().st_size,'sha256':sha(f)})
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  names=set(z.namelist())
  for mapname in ('map16/magical-campus.tmj',)+(() if name=='magical-campus-editable-source.zip' else ('gate/map/gate.tmj',)):
   m=json.loads(z.read(mapname));parent=Path(mapname).parent
   for ts in m['tilesets']:assert (parent/ts['image']).as_posix() in names
   props={x['name']:x['value'] for x in m.get('properties',[])}
   for key in ('gateRoomUrl','campusRoomUrl'):
    if key in props:assert props[key]==''
 record={'path':'dist/'+name,'bytes':p.stat().st_size,'sha256':sha(p),'fileCount':len(index)+1,'files':index}
 (D/(name+'.index.json')).write_text(json.dumps(record,indent=2)+'\n');result['archives'].append({k:v for k,v in record.items() if k!='files'})
 (D/'delivery-bundles.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['archives'][-1]),flush=True)
