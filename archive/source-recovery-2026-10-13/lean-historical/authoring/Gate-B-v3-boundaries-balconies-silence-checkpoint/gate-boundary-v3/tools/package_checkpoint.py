from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
paths=[]
for d in ['baseline','dependencies','publish','source-audit','stairs-only','validation']:
 paths.extend(p for p in (R/d).rglob('*')if p.is_file())
paths.extend(p for p in (R/'tools').iterdir()if p.is_file()and p.suffix in('.py','.mjs','.cjs'))
paths.extend(p for p in (R/'results').glob('*.json'))
paths.extend(R/'results'/n for n in ['native32-occlusion-contact-sheet.png','annotation-boundary-comparison.png','candidate-grid.png'])
paths.extend([R/'README.md',R/'GEOMETRY-INTEGRATION-MANIFEST.json'])
files={str(p.relative_to(R)):p.read_bytes()for p in sorted(paths)}
files['baseline/marked-gate.png']=Path('/workspace/shared/gate-user-boundary-feedback/marked-gate.png').read_bytes()
files['RESTORE.md']=b'''# Gate boundary checkpoint recovery\n\nThis archive contains the final unpublished geometry-only candidate, stairs-only fallback, exact Bv2 baseline TMJ, shared art dependencies, original unchanged script/music, native source snapshots, native32 Woka/EasyStar assets, tests, results, and visual proofs. No camera changes or engine edits are included.\n\nUnpack to one directory. Verify CHECKPOINT-CONTENTS.json hashes before using. The authoritative integration manifest identifies the exact TMJ and new foreground PNG; preserve both as-is until combined camera review.\n\nThe verification scripts resolve their root relative to their own path, so verify_routes.mjs, verify_tolerant_taps.mjs, verify_art.py, and build_native_model.cjs can run from this unpacked directory with Node22+ and Python/Pillow. verify_silent.cjs additionally references the existing Svelte store dependency in the original source checkout; provide that dependency path before rerunning on another machine. Its completed source-backed results and exact source are included.\n\nThe historical build and annotation-registration scripts preserve the original absolute input paths for provenance. The matching Bv2 TMJ and all required bytes are in this archive; update only input paths in a working copy if replaying elsewhere. The marked annotation is baseline/marked-gate.png. The frozen base artwork composite is included. No existing Bv2 package needs to be overwritten.\n\nHistorical Bv2 Library checkpoint: libfile_351f7f53d1408191b73ce9ac6f5edeee, version1, archive SHA256 a9ae0cba4cfd8a75b6b9fd099a465e83a134b0e459675429b8fa8634683de218. Current source pin: universe-develop 75666c0ccae779515b6fcbd83446ebd1eee29d1b. Deployed revision is unverified.\n\nMap-only spawn silence cannot guarantee zero transient proximity bubble during initial room-join handshake; read the source audit and README. No live/browser/iPhone validation is claimed.\n'''
manifest={'title':'Gate B v3 geometry, balcony and spawn-silence checkpoint','status':'unpublished integration-review candidate','engineBranch':'universe-develop','engineCommit':'75666c0ccae779515b6fcbd83446ebd1eee29d1b','baselineTmjSha256':sha(files['baseline/gate-b-v2.tmj']),'candidateTmjSha256':sha(files['publish/public/butterfly-town/gate-b/v3/gate.tmj']),'entries':[{'path':p,'bytes':len(b),'sha256':sha(b)}for p,b in sorted(files.items())]}
files['CHECKPOINT-CONTENTS.json']=(json.dumps(manifest,indent=2)+'\n').encode()
z=R/'Gate-B-v3-boundaries-balconies-silence-checkpoint.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as out:
 for p,b in sorted(files.items()):
  i=zipfile.ZipInfo('gate-boundary-v3/'+p,date_time=(2026,10,10,8,32,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;out.writestr(i,b)
with zipfile.ZipFile(z)as check:
 assert check.testzip()is None
 for e in manifest['entries']:assert sha(check.read('gate-boundary-v3/'+e['path']))==e['sha256']
receipt={'path':str(z),'bytes':z.stat().st_size,'sha256':sha(z.read_bytes()),'entries':len(files),'allZipEntriesVerified':True,'baselineTmjSha256':manifest['baselineTmjSha256'],'candidateTmjSha256':manifest['candidateTmjSha256'],'engineCommit':manifest['engineCommit']}
(R/'CHECKPOINT-PACKAGE-VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
