#!/usr/bin/env python3
"""Restore a verified additive furniture-access revision without touching originals."""
import argparse,pathlib,json,hashlib,shutil
p=argparse.ArgumentParser();p.add_argument('--bundle',type=pathlib.Path,default=pathlib.Path(__file__).parent/'reviewed-revision');p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
m=json.loads((a.bundle/'manifest.json').read_text());source=(a.bundle/'runtime').resolve();dest=a.output.resolve()
assert source!=dest and source not in dest.parents and dest not in source.parents,'Use an independent output directory'
assert not dest.exists(),'Output must be a new path; originals are never overwritten'
for f in m['files']:
 rel=pathlib.Path(f['path']);assert not rel.is_absolute() and '..' not in rel.parts
 data=(source/rel).read_bytes();assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],f['path']
shutil.copytree(source,dest)
for f in m['files']:assert hashlib.sha256((dest/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
print(json.dumps({'restored_maps':m['summary']['map_count'],'verified_files':len(m['files']),'output':str(dest),'originals_untouched':True,'publication_performed':False},indent=2))
