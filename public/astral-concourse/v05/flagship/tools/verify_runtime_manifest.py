#!/usr/bin/env python3
"""Verify the standalone nine-file runtime closure; works with Python -O."""
from pathlib import Path
import hashlib, json, struct

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'RUNTIME-MANIFEST.json').read_text())
runtime=root/'map32'
def require(ok,message):
    if not ok: raise RuntimeError(message)
for row in manifest['files']:
    p=root/row['path']
    require(p.is_file(),'Missing '+row['path'])
    data=p.read_bytes()
    require(len(data)==row['bytes'],'Length mismatch '+row['path'])
    require(hashlib.sha256(data).hexdigest()==row['sha256'],'SHA mismatch '+row['path'])
m=json.loads((runtime/'grand-auditorium.tmj').read_text())
w=json.loads((runtime/'grand-auditorium.wam').read_text())
require((m['width'],m['height'],m['tilewidth'],m['tileheight'])==(80,60,32,32),'Unexpected map geometry')
require(m['orientation']=='orthogonal','Unexpected projection')
require(not any(p['name']=='script' for p in m.get('properties',[])),'Unexpected map script')
require(not any(l['type']=='group' for l in m['layers']),'Unexpected toggle groups')
require(w['mapUrl']=='./grand-auditorium.tmj','Wrong companion target')
expected={'grand-auditorium.tmj','grand-auditorium.wam'}
for ts in m['tilesets']:
    name=ts['image'];require('/' not in name and '\\' not in name,'Non-local atlas')
    data=(runtime/name).read_bytes();require(data[:8]==b'\x89PNG\r\n\x1a\n','Not PNG '+name)
    require(struct.unpack('>II',data[16:24])==(ts['imagewidth'],ts['imageheight']),'Atlas dimension mismatch '+name)
    expected.add(name)
require(len(expected)==9,'Unexpected closure size')
require(expected=={Path(row['path']).name for row in manifest['files']},'Manifest closure mismatch')
print('PASS: nine exact runtime files; native32 orthogonal map; local closure; no script.')
