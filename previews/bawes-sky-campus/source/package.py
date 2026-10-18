"""Package the native16 review map without the repository's 32px-only optimizer."""
from pathlib import Path
import json,zipfile,hashlib
r=Path(__file__).resolve().parents[1];target=Path('/workspace/bawes-sky-campus-review.zip');m=json.loads((r/'campus.tmj').read_text());files=[r/'campus.tmj',r/'runtime.js',r/'README.md',r/'review/FOOTPRINT-REDESIGN.md',r/'review/footprint-exterior.png',r/'review/footprint-interior.png',r/'review/furniture-clearances.svg',r/'review/entrance-closed.png',r/'review/entrance-open.png',r/'review/runtime-campus-exterior.png',r/'review/runtime-full-interior.png',r/'review/runtime-native-interior.png',r/'source/runtime/run-local.sh',r/'source/runtime/serve-map.py']+[r/t['image'] for t in m['tilesets']]
files += [r/'review'/name for name in ['INTERIOR-REDO-BRIEF.md','FRESH-INTERIOR-SPATIAL-STUDY.svg','normal-interior-no-popup.png','normal-transition-composite.png','normal-transition-base-only.png','consistency-checks.json','GATE-AND-FLOOR.md','native-animation-capability.json','COMPOSITION-PASS.md','composition-camera-checks.json','seat-checks.json','gate-interaction.mp4','beverage-interaction.mp4','gate-timeline.json','gate-capture-timing.json','beverage-capture-timing.json','project-room-close.png','reception-active.png','reception-reduced-motion.png','mobile-bounded-chair.png','footprint-audit.json','footprint-checks.json','final-visual-checks.json','optimizer-equivalence.json']]
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(files)):z.write(p,p.relative_to(r))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'entries':len(set(files)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
