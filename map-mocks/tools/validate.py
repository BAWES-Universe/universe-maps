#!/usr/bin/env python3
"""Validate archive integrity and local Tiled/runtime asset closure (Python 3)."""
from pathlib import Path
import hashlib,json,re,struct,sys,urllib.parse,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
errors=[];checked_refs=0;checked_maps=0

def fail(message):errors.append(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(base,value,boundary,context):
 global checked_refs
 if not value or not isinstance(value,str):return
 if value.startswith(('http:','https:','data:')):
  fail(f'{context}: external runtime dependency {value}');return
 value=urllib.parse.unquote(value.split('#',1)[0].split('?',1)[0])
 p=(base/value).resolve();checked_refs+=1
 if not p.is_relative_to(boundary.resolve()):fail(f'{context}: dependency escapes candidate: {value}')
 elif not p.is_file():fail(f'{context}: missing dependency: {value}')

def visit_json(n,base,boundary,context):
 if isinstance(n,dict):
  for key in ['image','source','mapUrl','imagePath']:
   if key in n:ref(base,n[key],boundary,context)
  for p in n.get('properties',[]):
   if p.get('name') in ['script','playAudio','playAudioLoop'] and isinstance(p.get('value'),str) and p['value']:ref(base,p['value'],boundary,context)
  for k,v in n.items():visit_json(v,base,boundary,context)
 elif isinstance(n,list):
  for v in n:visit_json(v,base,boundary,context)

catalog=json.loads((ROOT/'catalog.json').read_text())
for item in catalog['templates']:
 d=ROOT/item['id'];meta=json.loads((d/'template.json').read_text())
 if meta!=item:fail(f'{d.name}: catalog metadata differs')
 if not (d/'README.md').is_file():fail(f'{d.name}: README missing')
 if not (d/meta['screenshot']).is_file():fail(f'{d.name}: screenshot missing')
 if meta['kind']=='visual-proposal' and meta['map'] is not None:fail(f'{d.name}: visual-only proposal claims TMJ')
 if meta['kind']=='tiled-map' and not (d/meta['map']).is_file():fail(f'{d.name}: map missing')
 if meta['catalogReady'] is not False:fail(f'{d.name}: candidate incorrectly advertised ready')
 for p in (d/'map').rglob('*') if (d/'map').exists() else []:
  if not p.is_file():continue
  if p.suffix in ['.tmj','.tsj','.wam'] or p.parent.name=='collections' and p.suffix=='.json':
   j=json.loads(p.read_text());visit_json(j,p.parent,d,str(p.relative_to(ROOT)))
   if p.suffix=='.wam':
    for c in j.get('entityCollections',[]):ref(p.parent,c.get('url'),d,str(p.relative_to(ROOT)))
   if p.suffix=='.tmj':
    checked_maps+=1
    if digest(p)!=meta['sourceMapSha256'].get(p.name):fail(f'{d.name}/{p.name}: original TMJ hash changed')
    def layers(ls):
     for l in ls:
      if l.get('type')=='tilelayer' and isinstance(l.get('data'),list) and len(l['data'])!=l['width']*l['height']:fail(f'{d.name}/{p.name}: invalid tile data length {l.get("name")}')
      layers(l.get('layers',[]))
    layers(j.get('layers',[]))
    for t in j.get('tilesets',[]):
     if 'image' in t:
      im=p.parent/t['image']
      if im.exists() and im.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n':
       w,h=struct.unpack('>II',im.read_bytes()[16:24])
       if (w,h)!=(t.get('imagewidth'),t.get('imageheight')):fail(f'{d.name}: tileset dimensions differ: {t["image"]}')
  elif p.suffix in ['.js','.mjs']:
   s=p.read_text()
   for value in re.findall(r'''(?:from\s+|import\s*\()\s*["'](\.[^"']+)["']''',s):ref(p.parent,value,d,str(p.relative_to(ROOT)))
   for value,anchor in re.findall(r'''new URL\s*\(\s*["']([^"']+)["']\s*,\s*(WA\.room\.mapURL|import\.meta\.url)''',s):ref(d/'map' if anchor=='WA.room.mapURL' else p.parent,value,d,str(p.relative_to(ROOT)))
   for value in re.findall(r'''["']((?:assets/)?audio/[^"']+\.(?:mp3|ogg|wav))["']''',s):ref(d/'map',value,d,str(p.relative_to(ROOT)))
 for line in (d/'SHA256SUMS.txt').read_text().splitlines():
  expected,name=line.split('  ',1);p=d/name
  if not p.is_file() or digest(p)!=expected:fail(f'{d.name}: checksum mismatch: {name}')
 for p in d.rglob('*'):
  if p.is_symlink():fail(f'{d.name}: symlink is not self-contained: {p.name}')
  if p.is_file() and p.suffix in ['.py','.js','.mjs','.json','.tmj','.md','.txt','.wam']:
   text=p.read_text(errors='replace')
   for token in ['/workspace/','libfile_','Bearer ','PRIVATE KEY-----']:
    if token in text:fail(f'{d.name}: private/environment-specific marker in {p.relative_to(d)}: {token}')
print(json.dumps({'passed':not errors,'candidates':len(catalog['templates']),'tiledMaps':checked_maps,'localReferencesChecked':checked_refs,'errors':errors},indent=2))
sys.exit(bool(errors))
