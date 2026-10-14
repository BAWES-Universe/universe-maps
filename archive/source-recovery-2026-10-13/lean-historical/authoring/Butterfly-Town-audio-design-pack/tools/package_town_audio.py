#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile
r=Path(__file__).resolve().parents[1]
files=[r/'AUDIO-INTEGRATION.md',r/'map/scripts/town-audio.mjs']
files+=sorted((r/'map/assets/audio').glob('*'))
files += [r/'tools'/x for x in ['generate_town_audio.py','render_native_scene_audio.py','render_audio_preview.py','package_town_audio.py']]
files += [r/'tests'/x for x in ['run-audio-tests.mjs','check_audio_assets.py','reproduce-native-audio.cjs','check-audio-browser.cjs','analyze_audio_master.py']]
files += sorted(p for p in (r/'evidence/audio').rglob('*') if p.is_file() and p.name!='preview-before-mastering.mp3')
files += [r/'audio-preview'/x for x in ['Butterfly-Town-sound-sketch.mp3','README.json','PACK-README.md','index.html']]
manifest={'status':'Quiet-world policy v2 candidate; historical scored preview superseded; no live activation or engine modifications','previewMastering':'Revised -16.27 LUFS integrated / -3.80 dBTP true peak. Native runtime assets unchanged.','files':[{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in files]}
out=r/'Butterfly-Town-audio-design-pack.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in files:z.write(p,p.relative_to(r))
 z.writestr('AUDIO-PACK-MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None
 for e in manifest['files']:assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256']
print(json.dumps({'archive':str(out),'bytes':out.stat().st_size,'files':len(files),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'validated':True}))
