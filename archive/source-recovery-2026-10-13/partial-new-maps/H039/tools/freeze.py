from pathlib import Path
import json,hashlib,shutil,datetime,sys,os,subprocess
R=Path(__file__).resolve().parents[1];name=sys.argv[1]if len(sys.argv)>1 else'H039-r1';F=R/'freezes'/name;assert not F.exists(),'Never overwrite an immutable freeze'
receipt=json.loads((R/'validation/exact-rebuild-receipt.json').read_text());assert receipt['exactRuntime']and receipt['ownDisposableRebuildRemoved'],'Source-clean byte-exact receipt and cleanup required before freeze'
F.mkdir(parents=True)
def cp(a,b):
 if Path(a).suffix.lower()=='.png':os.link(a,b)
 else:shutil.copy2(a,b)
for d in ['art','source','tools','runtime','review','validation','licenses']:shutil.copytree(R/d,F/d,copy_function=cp,ignore=shutil.ignore_patterns('__pycache__'))
for f in ['README.md','NATIVE-SPAWN-CHECKS.json']:shutil.copy2(R/f,F/f)
subprocess.run([sys.executable,str(F/'tools/make-spec.py'),str(F)],check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(dirs):return{str(p.relative_to(F)):sha(p)for d in dirs for p in sorted((F/d).rglob('*'))if p.is_file()}
D=json.loads((F/'source/design.json').read_text());manifest=dict(freeze=name,root=str(F),timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),title=D['title'],experience='Choose Swirl, Rake and Comb once each per sheet, in any order, creating eight original wet patterns. Explicitly lift a nonblank pattern to the drying rack. Wet changes and fresh sheets preserve the previous print.64 local physical states.',rebuild_command=['sh','tools/rebuild.sh'],generated_output_directories=['runtime','review','validation'],generated_source_assets=['source/mill-native.png','source/layout.json'],source=inv(['art','source','tools','licenses']),runtime=inv(['runtime']),review_evidence=inv(['review','validation']),entrypoint='runtime/map.tmj',status='AUTHOR_READY_FOR_INDEPENDENT_REVIEW',independent_source_accepted=False,live_verified=False,published=False,limitations=['Historical pinned native-source/stub-scene replay only','Actual GPU, live desktop/touch/mobile, camera, browser UI, avatar seating/facing and AV remain unverified','No deployment, publication, merge, engine edit, accounts or shared multiplayer persistence','External source/spreadsheet/preview links pending'])
for f in ['README.md','NATIVE-SPAWN-CHECKS.json','qa-spec.json']:manifest['source'][f]=sha(F/f)
(F/'FREEZE.json').write_text(json.dumps(manifest,indent=2)+'\n');ready=dict(freeze=name,root=str(F),manifest='FREEZE.json',manifestSHA256=sha(F/'FREEZE.json'),tmj='runtime/map.tmj',tmjSHA256=sha(F/'runtime/map.tmj'),runtimeFiles=len(manifest['runtime']),sourceFiles=len(manifest['source']),status='AUTHOR_READY_FOR_INDEPENDENT_REVIEW',qaSpec='qa-spec.json',independentSourceAccepted=False,liveVerified=False,published=False,githubSourceUrl=None,spreadsheetRowUrl=None,previewUrl=None);(F/'READY.json').write_text(json.dumps(ready,indent=2)+'\n');(R/'READY.json').write_text(json.dumps(ready,indent=2)+'\n')
# Verify the exact freeze immediately, with no subsequent in-place writes.
for section in ['source','runtime','review_evidence']:
 for rel,h in manifest[section].items():assert sha(F/rel)==h,(section,rel)
print(json.dumps(ready,indent=2))
