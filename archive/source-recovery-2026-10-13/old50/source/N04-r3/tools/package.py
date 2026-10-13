"""Package only exact independently accepted freezes; never alter a freeze."""
from pathlib import Path
import json,hashlib,zipfile,tempfile,subprocess,sys,io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];B=R.parent;OUT=R/'artifacts';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
idx=json.loads((B/'qa/index.json').read_text());rows=[m for m in idx['maps'] if m.get('owner')=='social' and m.get('qa')=='PASS_SCOPED' and m.get('test_ready')];records=[]
def writezip(path,files,extra):
 with zipfile.ZipFile(path,'w') as z:
  for name,p in sorted(files.items()):
   info=zipfile.ZipInfo(name,(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
  for name,data in sorted(extra.items()):
   info=zipfile.ZipInfo(name,(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
for m in rows:
 ID=m['id'];F=R/'freezes'/m['freeze'];ready=json.loads((F/'READY.json').read_text());rt=F/ID/'map32';assert sha(rt/f'{ID}.tmj')==m['tmj_sha256']
 for f in ready['files']:assert sha(F/f['path'])==f['sha256'],f['path']
 sp=OUT/f'{F.name}-source.zip';rp=OUT/f'{F.name}-runtime.zip';verify=OUT/f'{F.name}-package-check.json'
 if not(sp.exists() and rp.exists() and verify.exists()):
  source_files={str(p.relative_to(F)):p for p in F.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
  portable=f'''{ready['title']} / {F.name}\n\nLocal authorable map; live play is untested, not published.\n\nRebuild from this extracted directory:\n  python tools/build.py {ID}\n  node tools/native/arrival-audit.cjs {ID}\n\nLoad {ID}/map32/{ID}.wam with the complete map32 folder.\nDependencies: Python3, Pillow, Node.js. Native fixture and EasyStar are included.\nThe READY.json absolute paths describe the original immutable review location; the relative commands above are portable.\nThe source package preserves all original raster assets, compiler, fixture, native source pin, runtime, author proofs and hashes.\nStanding frame proofs do not provide sitting animation, automatic facing, gameplay or activity integrations.\n'''
  writezip(sp,source_files,{'PORTABLE-README.txt':portable})
  writezip(rp,{p.name:p for p in rt.iterdir() if p.is_file()},{'README.txt':f"Load {ID}.wam with every file in this directory. Local authorable candidate; not live-tested or published.\n"})
  with tempfile.TemporaryDirectory(prefix='social-zip-') as td:
   U=Path(td)
   with zipfile.ZipFile(sp) as z:z.extractall(U)
   for f in ready['files']:assert sha(U/f['path'])==f['sha256']
   expected={p.name:sha(p) for p in rt.iterdir() if p.is_file()}
   subprocess.run([sys.executable,str(U/'tools/build.py'),ID],check=True,capture_output=True)
   actual={p.name:sha(p) for p in (U/ID/'map32').iterdir() if p.is_file()};assert actual==expected
   check=dict(id=ID,freeze=F.name,allFrozenFilesSurviveZipExtraction=True,cleanExtractedSourceRebuildRuntimeByteExact=True,runtimeHashes=actual,sourceZipSHA256=sha(sp),runtimeZipSHA256=sha(rp),independentQA=m['qa'],livePlay=False,published=False)
   verify.write_text(json.dumps(check,indent=2)+'\n')
 records.append(dict(id=ID,title=m['title'],freeze=F.name,ready=str(F/'READY.json'),readySHA256=sha(F/'READY.json'),tmjSHA256=m['tmj_sha256'],sourceArtifact=dict(path=str(sp),sha256=sha(sp),bytes=sp.stat().st_size),runtimeArtifact=dict(path=str(rp),sha256=sha(rp),bytes=rp.stat().st_size),packageCheck=str(verify),independentQA='PASS_SCOPED',livePlay=False,published=False))
 print('Packaged',F.name,flush=True)
signature=hashlib.sha256(json.dumps([(r['freeze'],r['tmjSHA256']) for r in records]).encode()).hexdigest()[:10]
pdf=OUT/f'social-proof-review-{len(records):02}-{signature}.pdf'
pdfmetrics.registerFont(TTFont('Sans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
c=canvas.Canvas(str(pdf),pagesize=(1120,1000));c.setTitle('Social maps - exact checked scenes and native arrivals');page=0
for rec in records:
 F=R/'freezes'/rec['freeze'];ID=rec['id'];layout=json.loads((F/ID/'source/layout.json').read_text());n=len([a for a in layout['anchors'] if a['kind']=='seat'])
 for occupied in [False,True]:
  page+=1;c.setFillColorRGB(.955,.951,.93);c.rect(0,0,1120,1000,fill=1,stroke=0)
  c.setFillColorRGB(.09,.2,.23);c.setFont('Bold',27);c.drawString(42,952,ID+' / '+rec['title']);c.setFont('Sans',13);c.drawString(42,928,rec['freeze']+' | '+('Actual native-arrival standing-frame proof' if occupied else 'Full scene decoded from checked TMJ atlases'))
  p=F/ID/'review'/('actual-native-arrivals.png' if occupied else 'empty-native.png');im=Image.open(p).convert('RGB');buf=io.BytesIO();im.save(buf,format='JPEG',quality=94,subsampling=0);buf.seek(0);iw,ih=im.size;s=min(1036/iw,806/ih);c.drawImage(ImageReader(buf),(1120-iw*s)/2,103+(806-ih*s)/2,iw*s,ih*s)
  c.setFont('Sans',11);c.drawString(42,70,f'{n} authored seat contacts | independent scoped local QA passed | clean extracted source ZIP rebuild is byte-exact')
  c.drawString(42,49,'Live browser, multiplayer, automatic sitting/facing, animation and activity integrations are unverified. Not published.')
  c.setFont('Bold',9);c.drawString(42,25,'TMJ SHA256 '+rec['tmjSHA256']);c.drawRightString(1078,25,str(page));c.showPage()
c.save();manifest=dict(lane='Social and activities',checkedUniqueConcepts=len(records),target=17,proofPDF=dict(path=str(pdf),sha256=sha(pdf),pages=page),maps=records,scope='Only exact independent PASS_SCOPED freezes. All others remain pending and are omitted. Revisions do not increase concept count.');(OUT/'PACKAGES.json').write_text(json.dumps(manifest,indent=2)+'\n');print(pdf)
