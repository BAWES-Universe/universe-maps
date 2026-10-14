"""New reconstruction wrapper. Original r7c artwork stays unchanged."""
import argparse, pathlib, json, shutil, hashlib, sys
import build_maps as b
p=argparse.ArgumentParser();p.add_argument('--baseline',required=True,type=pathlib.Path);p.add_argument('--original',action='store_true');a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]; baseline=a.baseline.resolve();slug='resonance-media-house'; original=baseline/slug
b.R=root/('baseline-rebuild' if a.original else 'candidate');b.S=baseline/'source'
layout=json.loads((root/('baseline' if a.original else 'source')/'layout.json').read_text());m=b.Map(slug,layout['title'],*layout['world'],layout['category'],layout['style'])
m.base=b.rgba(original/'source/runtime-base.png');m.above=b.rgba(original/'source/runtime-above.png');m.grid=b.np.array(layout['grid'],b.np.uint8);m.quiet=b.np.array(layout['quiet'],b.np.uint8);m.spawn=tuple(layout['start']);m.anchors=layout['anchors'];m.areas=layout['areas'];m.objects=layout['objects'];m.fixtures=layout['protectedFixtures']
shutil.copy2(root/('baseline' if a.original else 'source')/'layout.json',m.r/'source/layout.json');m.compile();m.validate();m.render()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for f in sorted((m.r/'map32').iterdir()):
 other=original/'map32'/f.name;checks.append(dict(file=f.name,sha256=digest(f),originalSHA256=digest(other),sameBytes=f.read_bytes()==other.read_bytes()))
(m.r/'validation/baseline-comparison.json').write_text(json.dumps(checks,indent=2)+'\n')
if a.original:assert all(x['sameBytes'] for x in checks),checks
else:assert all(x['sameBytes'] for x in checks if x['file'].endswith(('.png','.wam')))
assert json.loads((m.r/'validation/geometry.json').read_text())['allPass']
print('EXACT ORIGINAL REBUILD' if a.original else 'RECONSTRUCTED CANDIDATE: unchanged art and collision; additional bench-front route targets only')
