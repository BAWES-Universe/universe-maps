from pathlib import Path
import zipfile,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];release=sys.argv[1];key=sys.argv[2];rel=R/'releases';out=rel/(release+'-rebuild.zip');assert not out.exists(),out
keep={'academy':'academy-environment-final.png','cowork':'cowork-environment-final.png','observatory':'observatory-environment-ring.png','command':'command-environment-clear.png'}[key]
common={'greg-reference.png','chair-below-safe.png','chair-foreground-safe.png','podium-below.png','podium-above.png','low-lounge-table.png','light-desk.png','industrial-chair40-native.png','industrial-chair-provenance.json'}
slug=json.loads((rel/release/'FREEZE.json').read_text())['slug']
with zipfile.ZipFile(rel/(release+'-source.zip')) as src,zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for item in src.infolist():
  if item.filename=='requirements.txt':continue
  if item.filename.startswith('source-assets/') and Path(item.filename).name not in common|{keep}:continue
  z.writestr(item,src.read(item.filename))
 z.writestr('requirements.txt','Pillow>=9\nnumpy>=1.23\n')
 z.writestr('REBUILD-INSTRUCTIONS.md',f'# Rebuild {slug}\n\nThis lean self-contained archive includes the frozen original environment, native furniture, compiler and unmodified pinned engine fixtures.\n\n1. Install Python3, Pillow and NumPy (requirements.txt), plus Node.js for the movement tests.\n2. From this archive root run: python tools/build_environments.py {key}\n3. Verify native routes: node tools/verify_native_routes.cjs {slug}\n4. The rebuilt runtime is in {slug}/map32. Serve this entire folder together.\n\nOnly the selected map source artwork is included; use the named build target above rather than the default all-maps target. No API, generation, network service, secret or paid account is needed to rebuild. Previews are static atlas renders. Live room/media tests remain separate.\n')
replay=R/'rebuild-checks'/release;replay.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out) as z:z.extractall(replay)
r=subprocess.run([sys.executable,'tools/build_environments.py',key],cwd=replay,capture_output=True,text=True);assert r.returncode==0,r.stderr
before=rel/release/'map32';after=replay/slug/'map32';hashes=lambda p:{q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in p.glob('*') if q.is_file()};assert hashes(before)==hashes(after),'Runtime hash mismatch'
report=dict(release=release,rebuildArchive=out.name,archiveSha256=hashlib.sha256(out.read_bytes()).hexdigest(),archiveBytes=out.stat().st_size,runtimeFiles=len(hashes(before)),runtimeByteExact=True,selectedTarget=key,buildOutput=r.stdout.strip())
(rel/(release+'-REBUILD-VERIFICATION.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
