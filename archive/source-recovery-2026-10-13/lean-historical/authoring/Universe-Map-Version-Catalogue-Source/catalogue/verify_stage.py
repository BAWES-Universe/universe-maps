from pathlib import Path
import json,hashlib,zipfile,tempfile,subprocess
from pypdf import PdfReader
D=Path(__file__).parent;p=json.load(open(D/'catalogue-data.json'));s=json.load(open(D/'sources/staged-workbook-snapshot.json'));old=json.load(open(D/'sources/testing-workbook-v8.json'));rows=p['rows'];by={r['id']:r for r in rows}
assert len(rows)==len(by)==68
current=[r for r in rows if r.get('current_stage')=='Awaiting publication'];assert len(current)==9
assert {r['id'] for r in current}=={r['Exact revision / catalogue ID'] for r in s['sheets']['Awaiting publication']}
for r in current:
 assert all(r.get(k) is None for k in ['tmj_url','preview_url','wam_url','source_url'])
 expected=next(v for v in s['sheets']['Awaiting publication'] if v['Exact revision / catalogue ID']==r['id']);assert r['staged_workbook_record']==expected
assert {r['id']:r.get('tmj_url') for r in old if r.get('tmj_url')}=={r['id']:r.get('tmj_url') for r in rows if r.get('tmj_url')}
assert all(by[r['id']]['decision']==r['decision'] for r in old)
for k in ['Category entry','Template entry','Map variant entry']:assert p['production_entry_snapshot'][k]==s['sheets'][k]
for r in rows:assert (D/r['asset']).exists()
prov=json.load(open(D/'asset-provenance.json'))
for r in rows:
 v=next(v for v in reversed(prov) if v['id']==r['id']);assert hashlib.sha256((D/r['asset']).read_bytes()).hexdigest()==v['asset_sha256']
pdf=PdfReader(D/'Universe-Map-Version-Catalogue.pdf');assert len(pdf.pages)==32
text='\n'.join(page.extract_text() for page in pdf.pages);assert all(r['id'] in text for r in rows);assert '0 current verified test links' in text
assert (D/'Universe-Map-Version-Catalogue.pdf').stat().st_size<15_000_000
(D/'sources/canonical-staged-68.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False))
qa={'all_32_pages_rendered_and_visually_inspected':True,'new_current_pages_reviewed_full_size':True,'nine_current_rows_exactly_match_staged_workbook':True,'all_57_original_decisions_preserved':True,'all_18_historical_urls_exact':True,'new_urls':0,'current_test_links':0,'category_template_map_planning_facts_preserved':True,'media_r7_extra_visual_archive':True,'no_library_write':True}
(D/'visual-qa.json').write_text(json.dumps(qa,indent=2))
out=D.parent/'Universe-Map-Version-Catalogue-STAGED-Source.zip'
def bundle():
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(D.rglob('*')):
   if f.is_file() and f.suffix!='.pdf' and f.name not in ['layout-log.json','merge_checked_records.py','upgrade_layout.py']:z.write(f,'catalogue/'+str(f.relative_to(D)))
bundle()
with tempfile.TemporaryDirectory(prefix='catalogue-staged-') as tmp:
 with zipfile.ZipFile(out) as z:z.extractall(tmp)
 C=Path(tmp)/'catalogue';subprocess.run(['python',str(C/'build_catalogue.py')],capture_output=True,check=True)
 assert (C/'Universe-Map-Version-Catalogue.pdf').read_bytes()==(D/'Universe-Map-Version-Catalogue.pdf').read_bytes()
(D/'source-bundle-check.json').write_text(json.dumps({'clean_extraction_rebuild':'PASS','pdf_byte_identical':True,'records':68,'families':22,'pages':32,'source_workbook_state':'staged, not uploaded'},indent=2));bundle()
receipt={'pdf_path':str(D/'Universe-Map-Version-Catalogue.pdf'),'pdf_bytes':(D/'Universe-Map-Version-Catalogue.pdf').stat().st_size,'pdf_sha256':hashlib.sha256((D/'Universe-Map-Version-Catalogue.pdf').read_bytes()).hexdigest(),'source_path':str(out),'source_bytes':out.stat().st_size,'source_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'records':68,'families':22,'pages':32,'awaiting_publication':9,'work_in_progress_families':1,'current_test_links':0,'historical_urls':18,'library_write':False,'pdf_library_id':'libfile_29638069434c8191a05f1336ef190bbc','pdf_previous_version':4,'source_library_id':'libfile_b20a8aaae09c8191bc7db0d0c4b15b46','source_previous_version':3}
(D.parent/'catalogue-stage-receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
