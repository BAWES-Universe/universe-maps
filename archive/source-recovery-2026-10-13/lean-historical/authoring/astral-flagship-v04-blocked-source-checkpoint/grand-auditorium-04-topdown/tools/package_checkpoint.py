from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path(__file__).resolve().parents[1]
O=Path('/workspace/scratch/41c8dbf833be/flagship-v04-library-checkpoint');O.mkdir(exist_ok=True)
files=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name!='SOURCE-CHECKPOINT-FREEZE.json':files.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
freeze={'status':'Blocked local visual/source checkpoint; dynamic native route acceptance failed','runtime':json.loads((R/'RUNTIME-MANIFEST.json').read_text()),'files':files}
(R/'SOURCE-CHECKPOINT-FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
for src,dst in [('review/runtime-overview.png','astral-flagship-v04-blocked-visual-overview.png'),('review/runtime-layer-states.png','astral-flagship-v04-blocked-layer-states.png'),('review/runtime-foyer-occupied-native.png','astral-flagship-v04-foyer-native.png'),('review/runtime-terrace-occupied-native.png','astral-flagship-v04-terrace-native.png'),('integration/ROOM-SETUP.md','astral-flagship-v04-blocked-setup-guide.md')]:shutil.copy2(R/src,O/dst)
for name,root in [('native32-same-tile-replan-reproduction.zip',R/'validation/minimal-native32-repro'),('astral-flagship-v04-blocked-source-checkpoint.zip',R)]:
 with zipfile.ZipFile(O/name,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for p in sorted(root.rglob('*')):
   if p.is_file():z.write(p,Path(root.name)/p.relative_to(root))
 with zipfile.ZipFile(O/name)as z:assert z.testzip()is None
rows=[{'filename':p.name,'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(O.iterdir())if p.is_file()and p.name!='checkpoint-manifest.json']
(O/'checkpoint-manifest.json').write_text(json.dumps({'status':'Blocked visual/source checkpoint, no accepted runtime release','files':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
