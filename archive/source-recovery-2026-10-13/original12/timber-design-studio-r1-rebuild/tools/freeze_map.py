from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,zipfile,shutil,sys
R=Path(__file__).resolve().parents[1];slug=sys.argv[1];p=R/slug;release=sys.argv[2] if len(sys.argv)>2 else slug;out=R/'releases'/release
if out.exists():raise SystemExit('Refusing to overwrite immutable release '+str(out))
out.mkdir(parents=True)
# Visualize actual solid tile cells, not a hand-made floor plan.
l=json.loads((p/'source/layout.json').read_text());im=Image.open(p/'review/empty-native.png').convert('RGBA');ov=Image.new('RGBA',im.size);d=ImageDraw.Draw(ov)
for y,row in enumerate(l['collision']):
 for x,v in enumerate(row):
  if v:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(220,35,60,85))
im.alpha_composite(ov);im.save(p/'review/collision-overlay.png')
for item in p.iterdir():
 if item.is_dir():shutil.copytree(item,out/item.name,dirs_exist_ok=True)
 else:shutil.copy2(item,out/item.name)
files=[dict(path=str(q.relative_to(out)),bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()) for q in sorted(out.rglob('*')) if q.is_file() and q.name!='FREEZE.json']
manifest={'title':l['title'],'slug':slug,'native32':True,'status':'Frozen local review candidate, not published','runtime':'map32/map.tmj','companion':'map32/map.wam','overview':'review/overview.png','occupiedNative':'review/occupied-native.png','checks':['VALIDATION.json','NATIVE-ROUTES.json'],'livePlaytest':False,'integrationsVerified':False,'files':files}
(out/'FREEZE.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out.parent/(release+'-runtime.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for q in (out/'map32').glob('*'):z.write(q,'map32/'+q.name)
 z.write(out/'GUIDE.md','GUIDE.md')
with zipfile.ZipFile(out.parent/(release+'-source.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for q in out.rglob('*'):
  if q.is_file():z.write(q,slug+'/'+str(q.relative_to(out)))
 for folder in ['tools','source-assets']:
  for q in (R/folder).rglob('*'):
   if q.is_file() and '__pycache__' not in str(q):z.write(q,str(q.relative_to(R)))
 for fn in ['ASSET-PROVENANCE.md','requirements.txt']:z.write(R/fn,fn)
print(out/'FREEZE.json')
