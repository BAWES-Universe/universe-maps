from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys,shutil
R=Path(__file__).resolve().parents[1];ID=sys.argv[1];P=R/ID
js=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((P/'validation/native-arrival-routes.json').read_text());assert a['allPass'];layout=json.loads((P/'source/layout.json').read_text());matched=[]
for t in layout['anchors']:
 row=next(r for r in a['rows'] if r['id']=='spawn-to-'+t['id'] and r['input']=='desktop');assert row['final']==[t['x'],t['y']],(t,row['final']);matched.append(dict(id=t['id'],final=row['final'],direction=row['finalDirection']))
js(P/'validation/anchor-endpoints.json',dict(allNativeEndpointsEqualAuthored=True,anchors=matched))
# Native-arrival directions are separate evidence from authored presentation directions.
m=json.loads((P/'map32'/f'{ID}.tmj').read_text());base=Image.new('RGBA',(m['width']*32,m['height']*32));above=base.copy();dest=base
atlas_cache={v['image']:Image.open(P/'map32'/v['image']).convert('RGBA') for v in m['tilesets']}
for l in m['layers']:
 if l['name']=='floorLayer':dest=above
 if l['type']!='tilelayer' or not l.get('opacity',1):continue
 for i,g in enumerate(l['data']):
  if not g:continue
  ts=max((s for s in m['tilesets'] if s['firstgid']<=g),key=lambda s:s['firstgid']);at=atlas_cache[ts['image']];n=g-ts['firstgid'];x=n%ts['columns']*32;y=n//ts['columns']*32;dest.alpha_composite(at.crop((x,y,x+32,y+32)),(i%m['width']*32,i//m['width']*32))
meta=json.loads((R/'fixtures/ACTOR-PROVENANCE.json').read_text())['actors'];directions={0:'south',1:'west',2:'east',3:'north'}
actual=base.copy()
for i,t in enumerate(layout['anchors']):
 ar=next(x for x in matched if x['id']==t['id']);face=directions[ar['direction']];who=meta[i%len(meta)];ox,oy=who['anchor'];frame=Image.open(R/'fixtures'/f'proof-actors-{face}.png').convert('RGBA').crop((ox-16,oy-16,ox+16,oy+16));actual.alpha_composite(frame,(t['x']-16,t['y']-16))
actual.alpha_composite(above);actual.save(P/'review/actual-native-arrivals.png')
seats=[t for t in layout['anchors'] if t['kind']=='seat'];contact=Image.new('RGB',(len(seats)*160,320),'#202020')
for i,t in enumerate(seats):
 box=(t['x']-20,t['y']-20,t['x']+20,t['y']+20);contact.paste(Image.alpha_composite(base,above).crop(box).resize((160,160),Image.Resampling.NEAREST),(i*160,0));contact.paste(actual.crop(box).resize((160,160),Image.Resampling.NEAREST),(i*160,160))
contact.save(P/'review/seat-contact-empty-actual-4x.png')
probes=[t for t in layout['anchors'] if any(k in t['id'] for k in ['canopy','arch-','window'])]
if probes:
 contact=Image.new('RGB',(len(probes)*240,260),'#202020');draw=ImageDraw.Draw(contact)
 for i,t in enumerate(probes):
  ar=next(x for x in matched if x['id']==t['id']);face=directions[ar['direction']];who=meta[i%len(meta)];ox,oy=who['anchor'];frame=Image.open(R/'fixtures'/f'proof-actors-{face}.png').convert('RGBA').crop((ox-16,oy-16,ox+16,oy+16));one=base.copy();one.alpha_composite(frame,(t['x']-16,t['y']-16));one.alpha_composite(above);contact.paste(one.crop((t['x']-40,t['y']-40,t['x']+40,t['y']+40)).resize((240,240),Image.Resampling.NEAREST),(i*240,20));draw.text((i*240+4,2),t['id'],fill='white')
 contact.save(P/'review/route-depth-contact-3x.png')
# Read enum values from pinned source rather than guess.
src=(R/'tools/native/source/play/src/front/Phaser/Player/Player.ts').read_text()
(P/'validation/arrival-facing-enum-note.txt').write_text('Native numeric finalDirection is recorded unchanged in anchor-endpoints.json. Main occupied proof facings are illustrative; actual-native-arrivals.png uses the recorded finalDirection (DOWN=0 LEFT=1 RIGHT=2 UP=3) from pinned source.\n')
lim=['Local authorable candidate, not live-tested or published.','No gameplay, cooking, music, photography, video playback or activity integrations.','No animation; fireplace and scenery are static.','Standing repository frames in decoded proof; manually chosen display facings are not automatic seating.','Collision is native32 tile-based; bounded object footprints are conservative at sprite margins.','Pinned native source-extracted route tests are not a live browser, keyboard physics, conferencing or device test.']
(P/'README.md').write_text('# '+layout['title']+'\n\nHost the complete map32 directory and load '+ID+'.wam in an editor-managed room. The companion defines default arrival; TMJ carries collision, default start, bounded quiet arrival, and ground/floorLayer/foreground.\n\nRebuild: python ../tools/build.py '+ID+' from the social batch root. Then node ../tools/native/arrival-audit.cjs '+str(P)+' and python ../tools/freeze.py '+ID+'. Dependencies: Python 3, Pillow; Node.js, bundled EasyStar.\n\nLimits:\n'+'\n'.join('- '+x for x in lim)+'\n')
lesson={'observed':'Generated atlas did not respect its requested uniform cell grid. Hand-measured asset crop rectangles prevent neighboring art leaking into composed runtime sprites.','applied':'Preserved original imagegen output, explicit crop coordinates, native32 deterministic assembly, and exact atlas round-trip. Seats use low cushions with varied facings rather than inherited north-only backrails.','next':'Ask for wider atlas gutters, retain explicit crop QA, and choose a different circulation topology for N02.'}

if (R/'source'/f'{ID}-lessons.json').exists():lesson=json.loads((R/'source'/f'{ID}-lessons.json').read_text())
js(P/'LESSONS.json',lesson)
# Freeze copies all reproducibility inputs so later batch pipeline changes cannot invalidate it.
revision=sys.argv[2] if len(sys.argv)>2 else 'r1'
F=R/'freezes'/f'{ID}-{revision}';assert not F.exists(),F
F.mkdir(parents=True);shutil.copytree(P,F/ID);shutil.copytree(R/'tools',F/'tools');shutil.copytree(R/'fixtures',F/'fixtures');(F/'source').mkdir();shutil.copy2(R/'source'/f'{ID}-original.png',F/'source')
for extra in (R/'source').glob(f'{ID}-*.png'):shutil.copy2(extra,F/'source')
for extra in (R/'source').glob(f'{ID}-*.txt'):shutil.copy2(extra,F/'source')
for extra in (R/'source').glob(f'{ID}-lessons.json'):shutil.copy2(extra,F/'source')
files=[dict(path=str(p.relative_to(F)),sha256=sha(p),bytes=p.stat().st_size) for p in F.rglob('*') if p.is_file()]
row=dict(id=ID,title=layout['title'],category='Social and activities',status='author-checked candidate; independent review pending',freezeRoot=str(F),runtime=str(F/ID/'map32'/f'{ID}.tmj'),wam=str(F/ID/'map32'/f'{ID}.wam'),occupiedProof=str(F/ID/'review/occupied-native.png'),review=str(F/ID/'review/review.png'),collisionProof=str(F/ID/'review/collision.png'),sourceRebuildCommand=f'python {F}/tools/build.py {ID}',nativeCheckCommand=f'node {F}/tools/native/arrival-audit.cjs {F}/{ID}',nativeSourceRevision='60e7afdc3f96ef32525597cd46bd41175d61a2ef',nativeChecks=dict(legs=a['legs'],samples=a['samples'],failures=0,allNativeEndpointsEqualAuthored=True),seatAnchors=[x for x in layout['anchors'] if x['kind']=='seat'],dependencies=['Python3','Pillow','Node.js','bundled EasyStar 0.4.4'],limits=lim,files=files)
js(F/'READY.json',row);js(P/'catalogue-row.json',row);print(F/'READY.json')
