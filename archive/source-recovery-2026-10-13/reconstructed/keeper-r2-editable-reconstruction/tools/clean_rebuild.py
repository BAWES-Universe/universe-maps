#!/usr/bin/env python3
"""Source-only clean rebuild and reversible editability probes in a private temp copy."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def inventory(p):return {str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(p.rglob('*')) if f.is_file()}
def run(*args,cwd):return subprocess.run(args,cwd=cwd,check=True,capture_output=True,text=True).stdout.strip()
source_before=inventory(ROOT/'source');logs=[]
with tempfile.TemporaryDirectory(prefix='keeper-r2-clean-') as tmp:
 clean=pathlib.Path(tmp)
 for name in ['source','tools','tests']:shutil.copytree(ROOT/name,clean/name)
 assert not (clean/'build').exists()
 logs.append(run(sys.executable,'tools/build.py','--report','evidence/runtime-comparison.json',cwd=clean))
 logs.append(run(sys.executable,'tests/structure.py',cwd=clean));logs.append(run('node','tests/controller.cjs',cwd=clean))
 baseline=json.loads((clean/'evidence/runtime-comparison.json').read_text());assert baseline['exact_original_runtime'];actual=inventory(clean/'build/runtime');expected={f['path']:{'bytes':f['bytes'],'sha256':f['sha256']} for f in json.loads((clean/'source/runtime-baseline.json').read_text())['files']};assert actual==expected
 # Reject stale nested output files as well as unexpected top-level files.
 stale=clean/'build/runtime/extra-dir/unexpected.txt';stale.parent.mkdir();stale.write_text('stale output probe')
 rejected=subprocess.run([sys.executable,'tools/build.py'],cwd=clean,capture_output=True,text=True)
 assert rejected.returncode!=0 and 'extra-dir/unexpected.txt' in rejected.stderr
 stale.unlink();stale.parent.rmdir()
 # Prove the build consumes editable input, not a hidden runtime snapshot.
 map_path=clean/'source/map.json';mapdata=json.loads(map_path.read_text());name=next(p for p in mapdata['properties'] if p['name']=='name');name['value']+=' [temporary editability probe]';map_path.write_text(json.dumps(mapdata,indent=2)+'\n')
 logs.append(run(sys.executable,'tools/build.py','--out','probe-map','--allow-edits',cwd=clean));changed_map=[n for n,v in inventory(clean/'probe-map').items() if expected.get(n)!=v];assert changed_map==['keepers-return.tmj']
 shutil.copyfile(ROOT/'source/map.json',map_path)
 anchors_path=clean/'source/anchors.json';anchors=json.loads(anchors_path.read_text());anchors['anchors']['houseDoor']['description']+=' [temporary editability probe]';anchors_path.write_text(json.dumps(anchors,indent=2)+'\n')
 logs.append(run(sys.executable,'tools/build.py','--out','probe-anchors','--allow-edits',cwd=clean));changed_anchors=[n for n,v in inventory(clean/'probe-anchors').items() if expected.get(n)!=v];assert changed_anchors==['keeper.js']
result={'scope':'Clean copied source/tools/tests only; no original runtime tree, runtime ZIP or prebuilt output available to emitter','exact_runtime_files':len(expected),'mismatches':[],'source_unchanged':inventory(ROOT/'source')==source_before,'nested_unexpected_output_rejected':True,'editability_probes':{'map_properties_change_only_tmj':changed_map,'anchors_change_only_controller':changed_anchors},'checks':logs,'limits':['Reconstructed source, not original authoring project','Mock controller and point-grid structure tests, not native body replay or live acceptance']}
assert result['source_unchanged'];(ROOT/'evidence/clean-rebuild.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'exact_runtime_files':len(expected),'source_unchanged':True,'editability_probes':2}))
