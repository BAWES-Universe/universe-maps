"""Package the native16 review map without the repository's 32px-only optimizer."""
from pathlib import Path
import json,zipfile,hashlib
r=Path(__file__).resolve().parents[1];target=Path('/workspace/bawes-sky-campus-review.zip');m=json.loads((r/'campus.tmj').read_text());files=[r/'campus.tmj',r/'runtime.js',r/'README.md',r/'review/VALIDATION.md',r/'review/REFINEMENT.md',r/'review/COMPOSITING.md',r/'review/SEAMS-AND-COMPOSITION.md',r/'review/FOOTPRINT-REDESIGN.md',r/'review/footprint-exterior.png',r/'review/footprint-interior.png',r/'review/furniture-clearances.svg',r/'review/entrance-closed.png',r/'review/entrance-open.png',r/'review/runtime-campus-exterior.png',r/'review/runtime-full-interior.png',r/'review/runtime-native-interior.png',r/'review/runtime-registered-glass.png',r/'source/runtime/run-local.sh',r/'source/runtime/serve-map.py']+[r/t['image'] for t in m['tilesets']]
files += [r/'review'/name for name in ['project-room-close.png','reception-active.png','reception-reduced-motion.png','mobile-bounded-chair.png','footprint-audit.json','footprint-checks.json','footprint-glass-checks.json','final-visual-checks.json','optimizer-equivalence.json']]
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(files)):z.write(p,p.relative_to(r))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'entries':len(set(files)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
