from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import json,sys,shutil,hashlib,zipfile,subprocess
R=Path(__file__).resolve().parents[1];slug=sys.argv[1];p=R/slug;s=json.loads((p/'source/spec.json').read_text());ID=s['id'];assert json.loads((p/'validation/geometry.json').read_text())['allPass'];assert all(x['exact'] for x in json.loads((p/'validation/anchor-endpoints.json').read_text()));assert (p/'review/actual-native-arrivals.png').exists();root=R/'freezes'/(ID+'-'+(sys.argv[2] if len(sys.argv)>2 else 'r1'));assert not root.exists();root.mkdir(parents=True);q=root/slug;shutil.copytree(p,q)
limits=['Local candidate; independent review and live browser/gameplay pending.','Standing native32 Woka proofs; benches have approach anchors, no sitting animation.','No live services, automated event, transport or puzzle mechanics configured.','Areas are editor-ready metadata, with no broadcast/audio configuration.']
if s.get('event'):limits[2]='WAM speaker/listener and bounded focus source-configured; live camera/audio/video services untested.';limits[3]='Load WAM for event hooks. TMJ alone provides base map only.'
if s.get('seats'):limits[1]=str(len(s['seats']))+' native-fit visual chair anchors with lower-backrail layering; standing frames, no autositting or autofacing.'
readme='# '+s['title']+'\n\n'+s['style']+'\n\n'+ '\n'.join('- '+x for x in limits)+'\n\nHost complete map32 folder. Runtime uses native32 orthogonal TMJ and WAM without external dependencies. Rebuild: python tools/build_one.py '+slug+' from source archive root. Python3, Pillow, NumPy; Node24 for source-extracted native checks.\n\nLesson: '+s['lesson']+'\n'
(q/'README.md').write_text(readme)
# Landscape review with full occupied art and candid validation caption, second page collision proof.
pdf=root/(slug+'-review.pdf');c=canvas.Canvas(str(pdf),pagesize=(864,648))
for k,name in enumerate(['actual-native-arrivals.png','collision-native.png']):
 c.setFillColorRGB(.055,.10,.14);c.rect(0,0,864,648,fill=1,stroke=0);c.setFillColorRGB(.95,.85,.60);c.setFont('Helvetica-Bold',19);c.drawString(28,612,ID+' / '+s['title']);c.setFillColorRGB(.8,.86,.87);c.setFont('Helvetica',10);c.drawString(28,591,'Native32 actual-arrival occupied proof' if k==0 else 'Collision mask and anchor coverage / pink = blocked');c.drawImage(str(q/'review'/name),28,40,width=808,height=539,preserveAspectRatio=True,mask='auto');c.setFont('Helvetica',9);c.drawString(28,22,'Local source / static / native-method checks only. Live playtest and independent QA pending.');c.showPage()
c.save();subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','1200','-png',str(pdf),str(root/'pdf-review-page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def zipdir(path,out):
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(path.rglob('*')):
   if f.is_file() and '__pycache__' not in str(f):z.write(f,f.relative_to(path))
runtime=root/(slug+'-runtime.zip');zipdir(q/'map32',runtime)
b=root/'source-rebuild';b.mkdir()
for sub in ['tools','source']:shutil.copytree(R/sub,b/sub,ignore=shutil.ignore_patterns('__pycache__'))
for sub in ['art','specs']:(b/sub).mkdir();shutil.copy(R/sub/(slug+('.png' if sub=='art' else '.json')),b/sub)
(b/'README.md').write_text(readme);source=root/(slug+'-source.zip');zipdir(b,source)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ready=dict(id=ID,title=s['title'],concept=s['category'],freeze_root=str(q),source_rebuild_command='python tools/build_one.py '+slug,runtime={'path':str(runtime),'sha256':sha(runtime)},source={'path':str(source),'sha256':sha(source)},tmj=str(q/'map32'/(slug+'.tmj')),tmj_sha256=sha(q/'map32'/(slug+'.tmj')),decoded_art=str(q/'review/empty-native.png'),occupied_proof=str(q/'review/actual-native-arrivals.png'),review_pdf=str(pdf),review_png=str(root/'pdf-review-page.png'),engine_revision='60e7afdc3f96ef32525597cd46bd41175d61a2ef',author_checks={'geometry':json.loads((q/'validation/geometry.json').read_text())['allPass'],'native_routes':json.loads((q/'validation/native-arrival-routes.json').read_text())['allPass'],'exact_anchor_endpoints':True,'spawn_near_one':str(q/'NATIVE-SPAWN-CHECKS.json')},seat_anchors=s.get('seats',[]),bench_approach_anchors=[a for a in s['anchors'] if 'bench' in a[0]],required_dependencies=['Python3','Pillow','NumPy','Node24'],known_limits=limits,lesson=s['lesson'],status='author_checks_pass_independent_review_pending')
(root/'READY.json').write_text(json.dumps(ready,indent=2));print(root/'READY.json')
