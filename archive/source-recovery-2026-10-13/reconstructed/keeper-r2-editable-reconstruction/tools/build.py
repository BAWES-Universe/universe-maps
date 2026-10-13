#!/usr/bin/env python3
"""Reconstructed, deterministic Keeper r2 emitter; original authoring pipeline is lost.
Consumes editable source JSON/CSV/controller and retained original runtime textures.
Never reads the original runtime directory or an archive.
"""
import argparse,csv,hashlib,json,pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def build(destination,verify=True):
 source=ROOT/'source'; destination=pathlib.Path(destination).resolve()
 if destination==ROOT or destination.is_relative_to(source) or source.is_relative_to(destination):raise ValueError('Build output must not contain or overwrite source')
 destination.mkdir(parents=True,exist_ok=True)
 m=load(source/'map.json'); layers=[]
 for ref in m['layers']:
  p=(source/ref['file']).resolve();assert p.is_relative_to(source.resolve())
  layer=load(p)
  if isinstance(layer.get('data'),dict):
   gridpath=(source/layer['data']['csv']).resolve();assert gridpath.is_relative_to(source.resolve())
   with gridpath.open(newline='') as f: rows=[[int(v) for v in row] for row in csv.reader(f)]
   if len(rows)!=layer['height'] or any(len(row)!=layer['width'] for row in rows):raise ValueError('Invalid grid dimensions: '+layer['name'])
   layer['data']=[v for row in rows for v in row]
  layers.append(layer)
 m['layers']=layers
 (destination/'keepers-return.tmj').write_text(json.dumps(m,ensure_ascii=True,separators=(',',':')),encoding='utf-8')
 anchors=load(source/'anchors.json'); controller=(source/'controller.js').read_text(encoding='utf-8')
 (destination/'keeper.js').write_text('globalThis.IslandLayout = '+json.dumps(anchors,ensure_ascii=True,separators=(',',':'))+';\n'+controller,encoding='utf-8')
 room=load(source/'room.wam.json');(destination/'keepers-return.wam').write_text(json.dumps(room,indent=2,ensure_ascii=True),encoding='utf-8')
 for image in sorted((source/'art').glob('*.png')):shutil.copyfile(image,destination/image.name)
 actual={p.relative_to(destination).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in destination.rglob('*') if p.is_file()}
 baseline=load(source/'runtime-baseline.json'); expected={f['path']:{'bytes':f['bytes'],'sha256':f['sha256']} for f in baseline['files']}
 report={'scope':'Reconstructed editable-source emitter vs original delivered runtime','file_count':len(actual),'exact_original_runtime':actual==expected,'files':actual,'mismatches':[name for name in sorted(set(expected)|set(actual)) if expected.get(name)!=actual.get(name)]}
 if verify and not report['exact_original_runtime']:raise ValueError('Original runtime mismatch: '+str(report['mismatches']))
 return report
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=pathlib.Path,default=ROOT/'build/runtime');parser.add_argument('--allow-edits',action='store_true',help='Build a changed candidate, without claiming original-byte identity');parser.add_argument('--report',type=pathlib.Path)
 args=parser.parse_args();result=build(args.out,not args.allow_edits)
 if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'files':result['file_count'],'exact_original_runtime':result['exact_original_runtime'],'mismatches':result['mismatches']}))
