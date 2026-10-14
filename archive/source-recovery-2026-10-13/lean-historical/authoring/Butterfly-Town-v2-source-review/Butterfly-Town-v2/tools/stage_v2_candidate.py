"""Prepare a self-contained v2 addition only. Never modifies v1 or deploys."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1]
DEST=R/'candidate/public/butterfly-town/v2'
DEST.mkdir(parents=True,exist_ok=True)
mapdata=json.loads((R/'map/butterfly-town.tmj').read_text())
paths=['butterfly-town.tmj','README.md','ART-PROVENANCE.md']+[t['image'] for t in mapdata['tilesets']]
paths += [str(p.relative_to(R/'map')) for p in (R/'map/scripts').glob('*') if p.is_file()]
paths += ['assets/audio/fountain.mp3','assets/audio/fountain.ogg','assets/audio/cascade-soft.mp3','assets/audio/cascade-soft.ogg','assets/audio/gate-crossing.mp3','assets/audio/LICENSE.txt','assets/audio/runtime-policy.json']
for name in sorted(set(paths)):
 source=R/'map'/name
 if not source.is_file():raise RuntimeError('Missing runtime dependency: '+name)
 target=DEST/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
manifest={name:hashlib.sha256((DEST/name).read_bytes()).hexdigest() for name in sorted(set(paths))}
(DEST/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'candidate/INDEX-PROPOSAL.md').write_text('''# Butterfly Town v2 index proposal

Review candidate only. Do not overwrite or repoint v1.

- Add `public/butterfly-town/v2/` as a complete versioned folder.
- Keep the existing `public/butterfly-town/v1/` and all unrelated maps byte-identical.
- Add one new optional entry to the family README/index: “Butterfly Town v2 (review candidate)” → `v2/butterfly-town.tmj`.
- Keep the default/current entry on v1 until owner approves v2.
- Audio is OFF in `v2/scripts/town.js`. Set `ENABLE_NATIVE_AUDIO = true` only after compatible native PR712 is deployed and device/listening acceptance is complete.
- Do not alter the engine, WAM objects, user zoom, Places controls, or existing map routes from this addition.

No PR, push, merge or deployment has been performed by this staging tool.
''')
report={'root':str(DEST),'files':len(manifest),'bytes':sum((DEST/p).stat().st_size for p in manifest),'audioDefault':'OFF','selfContained':True,'filesSha256':manifest}
(R/'evidence/v2-staged-candidate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='filesSha256'},indent=2))
