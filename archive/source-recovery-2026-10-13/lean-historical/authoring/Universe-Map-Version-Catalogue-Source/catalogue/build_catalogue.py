from pathlib import Path
import json,html,hashlib,datetime
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab import rl_config
rl_config.useA85 = 0
from reportlab.lib.colors import HexColor,Color
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D=Path(__file__).parent
pack=json.load(open(D/'catalogue-data.json')); rows=pack['rows']; families=pack['families']; bynum={r['row']:r for r in rows}
active=[f for f in families if not f['archived']]; archives=[f for f in families if f['archived']]
index_cards=active+[{'archive_group':True,'name':'Rejected map archive','families':archives}]
index_count=(len(index_cards)+8)//9
register_rows_per_page=19
history_extra_pages=sum((max(0,len(f['rows'])-5)+5)//6 for f in active)
active_start=index_count+2; archive_page=active_start+len(active)+history_extra_pages; register_start=archive_page+1; register_end=register_start+(len(rows)+register_rows_per_page-1)//register_rows_per_page-1
W,H=1000,740; M=36
for name,p in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+p))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='Bold',italic='Sans',boldItalic='Bold')
INK=HexColor('#142623'); MUTED=HexColor('#58675F'); TEAL=HexColor('#1C7062'); PALE=HexColor('#F0F4F0'); LINE=HexColor('#D6DDD8'); RED=HexColor('#8E3B31'); GOLD=HexColor('#886321')
OUT=D/'Universe-Map-Version-Catalogue.pdf'
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1,invariant=1);c.setTitle('Universe Map Version Catalogue');c.setAuthor('Universe')
log=[]
def clean(t):return str(t or '').replace('·',' / ').replace('–','-').replace('—','-').replace('’',"'")
def txt(t,x,y,w,size=11,leading=None,bold=False,color=INK,limit=None):
 st=ParagraphStyle('x',fontName='Bold' if bold else 'Sans',fontSize=size,leading=leading or size*1.38,textColor=color)
 p=Paragraph(t,st);ww,hh=p.wrap(w,1000)
 if limit is not None and hh>limit:raise RuntimeError(f'Overflow p{c.getPageNumber()}: {t[:90]}: {hh} > {limit}')
 p.drawOn(c,x,y-hh);log.append({'page':c.getPageNumber(),'text':t,'bounds':[x,y-hh,w,hh]});return y-hh

def e(t):return html.escape(clean(t))
def image(row,x,y,w,h):
 p=D/row['asset'];im=Image.open(p);iw,ih=im.size;s=min(w/iw,h/ih);a,b=iw*s,ih*s
 c.setFillColor(PALE);c.rect(x,y,w,h,fill=1,stroke=0)
 c.drawImage(ImageReader(str(p)),x+(w-a)/2,y+(h-b)/2,width=a,height=b,mask='auto')
def footer():
 c.setFont('Sans',8.5);c.setFillColor(MUTED);c.drawString(M,20,'TESTING PAUSED  |  11 October 2026  |  Source/native previews; no live acceptance')
 c.drawRightString(W-M,20,str(c.getPageNumber()))
def page_end():footer();c.showPage()
def decision(r):return {'Approve':'Approved design','Pending':'Design pending','Tweak':'Changes requested','Reject':'Rejected design'}.get(r['decision'],r['decision'])
def qa(r):
 s=r.get('source_validation','');slo=s.lower()
 if r.get('implementation')=='Visual concept only':return 'Concept only / no runtime'
 if any(t in slo for t in ['blocked','defect','fault']):return 'Blocked / qualified'
 if 'study' in slo or 'not ' in slo or 'pending' in slo:return 'Study / unverified'
 if 'pass' in slo:return 'Source check passed'
 return 'See source scope'
def status_color(r):return RED if r['decision']=='Reject' or 'Blocked' in qa(r) else TEAL if r['decision']=='Approve' else MUTED
# Release status is separate from retained design approval and historical publication.
c.bookmarkPage('release-status');c.addOutlineEntry('Testing pause and release status','release-status',0)
txt('Map Review / Testing Paused',M,H-38,928,29,bold=True)
txt('<b>9 checked candidates await publication. 0 current verified test links.</b>',M,H-90,928,17,bold=True,color=TEAL)
txt('This is a local staged review. Do not use old URLs or archived versions for testing. Exact hosted verification and a corrected current list are still required.',M,H-132,928,12,color=MUTED)
current=[r for r in rows if r.get('current_stage')=='Awaiting publication']
y=H-196
for j,r in enumerate(current):
 if j%2==0:c.setFillColor(PALE);c.rect(M,y-30,928,35,fill=1,stroke=0)
 txt(e(r['title']),M+8,y,540,11,bold=True,limit=32)
 txt(e(r['version']),595,y,132,10,limit=30)
 txt('Awaiting publication',748,y,210,10,color=TEAL,limit=30)
 y-=39
txt('<b>In progress:</b> The calmer Celestial rebuild is not a checked release. <b>Concept only:</b> Saltwind Performance Courtyard. Neither is a current test candidate.',M,166,928,11)
txt('Standing native avatars and actual arrival proofs are shown for checked builds. No automatic sitting, snapping, turning or live browser/device/AV acceptance is implied. Garden paths meet boundaries; no cross-map transition is configured.',M,116,928,10,color=MUTED)
txt(f"{len(rows)} retained versions and studies / {len(families)} visual families. Historical links appear only as archive references. Categories and production-entry facts are preserved at the end.",M,60,928,10,color=MUTED)
page_end()
for start in range(0,len(index_cards),9):
 c.bookmarkPage('index'+str(start));c.addOutlineEntry('Visual family index' if start==0 else 'Visual family index continued','index'+str(start),0)
 txt('Universe Map Version Catalogue' if start==0 else 'Map Families at a Glance',M,H-38,928,27,bold=True)
 if start==0:
  txt(f'<b>{len(rows)} tracked versions and studies across {len(families)} map families.</b> {len(active)} family comparisons and {len(archives)} rejected archives. Each family preserves its earlier versions; these are not {len(rows)} distinct maps.',M,H-84,928,12)
  txt('Checked candidates lead their families; other images remain archived history. Testing is paused. Design approval, source checks, hosted verification and live testing are separate.',M,H-124,928,10.5,color=MUTED)
 else:
  txt('Click a family for its visual history. Awaiting publication does not mean ready to test. Archived and rejected maps are not current recommendations.',M,H-86,928,12)
 ytop=H-184 if start==0 else H-144
 for pos,f in enumerate(index_cards[start:start+9]):
  row,col=divmod(pos,3);x=M+col*316;y=ytop-row*171
  if f.get('archive_group'):
   for j,a in enumerate(f['families']):image(bynum[a['latest']],x+j*152,y-111,144,111)
   txt('Lantern Congress and Circuit Arena',x,y-119,296,11,bold=True)
   txt('Rejected designs / archived',x,y-140,296,9,color=RED)
   c.linkRect('','family-Lantern Congress',(x,y-160,x+296,y),relative=0,thickness=0)
  else:
   r=bynum[f['latest']];image(r,x,y-111,296,111)
   txt(e(f['name']),x,y-119,296,12,bold=True)
   tag=f"{r['version']} / {len(f['rows'])} versions / "+('awaiting publication' if r.get('current_stage')=='Awaiting publication' else 'concept only' if r.get('current_stage')=='Concept only' else 'archive')
   txt(e(tag),x,y-140,296,9,color=MUTED)
   c.linkRect('',f"family-{f['name']}",(x,y-160,x+296,y),relative=0,thickness=0)
 txt(f'Pages {active_start}-{archive_page-1}: family comparisons. Page {archive_page}: rejected archive. Pages {register_start}-{register_end}: every tracked version and archived TMJ reference.',M,47,928,9,color=MUTED)
 page_end()
for f in active:
 r=bynum[f['latest']];c.bookmarkPage('family-'+f['name']);c.addOutlineEntry(f['name'],'family-'+f['name'],0)
 txt(e(f['name']),M,H-34,928,26,bold=True)
 txt(f"RETAINED VERSION  /  {e(r['version'])}  /  RECORD {r['row']:02d}",M,H-76,928,10,bold=True,color=TEAL)
 image(r,M,292,620,338)
 txt('Visual concept / runtime not built' if r.get('implementation')=='Visual concept only' else 'Occupied source composition' if r['row'] not in [16,17] else 'Recorded source preview',M,284,620,9,color=MUTED)
 x=682;y=630;tw=282
 stage='Awaiting publication' if r.get('current_stage')=='Awaiting publication' else 'Concept / no runtime' if r.get('current_stage')=='Concept only' else 'Archive / do not test'
 y=txt(e(stage),x,y,tw,14,bold=True,color=TEAL if stage=='Awaiting publication' else RED)-7
 y=txt('<b>Design / authorization</b><br/>'+e(r.get('design_authorization',decision(r))),x,y,tw,9.6)-8
 y=txt('<b>Source validation</b><br/>'+e(r['source_validation']),x,y,tw,9.6)-10
 y=txt('<b>Live testing</b><br/>'+e(r.get('live_playtest','Not verified'))+'. No live acceptance is inferred.',x,y,tw,9.6)-10
 if r.get('tmj_url'):
  y=txt('<b>Publication</b><br/>'+e(r['publication'])+f'<br/><link href="{e(r["tmj_url"])}" color="#1C7062"><u>Archived TMJ - not for testing</u></link>',x,y,tw,9.6)-10
 else:y=txt('<b>Publication</b><br/>No verified current URL. '+e(r.get('publication','Unpublished')),x,y,tw,9.6)-10
 y=txt('<b>What changed</b><br/>'+e(r['caption']),x,y,tw,9.6)-10
 if f.get('work_in_progress'):note=f['work_in_progress']
 elif r.get('current_stage') in ['Awaiting publication','Concept only']:note=r.get('current_limits','Source checks do not establish live browser/device acceptance.')
 else:note=r.get('archive_reason','Historical version only; not for current testing.')
 y=txt(e(note),x,y,tw,9.2,color=MUTED)
 if y<292:raise RuntimeError(f'Metadata overflow {f["name"]}: {y}')
 allhist=[bynum[n] for n in f['rows'] if n!=f['latest']];hist=allhist[-4:];extra=allhist[:-4]
 txt('Earlier versions / archive only' if hist else 'Review and next step',M,248,928,14,bold=True)
 if hist:
  n=len(hist);slot=928/n;iw=min(slot-16,290)
  for j,h in enumerate(hist):
   xx=M+j*slot;image(h,xx,108,iw,111)
   txt(f"{h['row']:02d}  {e(h['version'])}  /  {e(h['decision'])} / archive",xx,103,slot-16,9.2,leading=11.2,bold=True,color=status_color(h),limit=24)
   txt(e(h['caption']),xx,70,slot-16,8.5,leading=11.5,limit=35,color=MUTED)
 else:
  tx=txt(e(r['caption']),M,217,600,12)
  tx=txt('Testing is paused. Retain this image for review; wait for the corrected current test list and verified hosting before testing.',M,tx-12,870,10.5,color=MUTED)
 if extra:txt('Earlier history continues on the next page.',M,45,928,9,color=MUTED)
 c.linkRect('','index0',(M,H-83,W-M,H-24),relative=0,thickness=0)
 page_end()
 for start in range(0,len(extra),6):
  txt(e(f['name'])+' / earlier archive',M,H-36,928,25,bold=True)
  txt('Historical visual references only. Retained approvals do not make superseded builds current test candidates.',M,H-84,928,11,color=MUTED)
  for j,h in enumerate(extra[start:start+6]):
   row,col=divmod(j,3);xx=M+col*316;yy=H-140-row*260
   image(h,xx,yy-170,296,170)
   txt(f"{h['row']:02d}  {e(h['version'])} / {e(h['decision'])}",xx,yy-180,296,11,bold=True)
   txt(e(h['caption']),xx,yy-202,296,10,limit=48,color=MUTED)
  page_end()
# Archives share one page without presenting them as current candidates.
for name in ['Lantern Congress','Circuit Arena']:c.bookmarkPage('family-'+name)
c.addOutlineEntry('Rejected archive','family-Lantern Congress',0)
txt('Rejected Map Archive',M,H-36,928,27,bold=True)
txt('Both maps were rejected by the user. They remain indexed for history and are not recommended for current review or testing.',M,H-86,928,12,color=MUTED)
for j,n in enumerate([9,10]):
 r=bynum[n];x=M+j*474;image(r,x,245,450,336)
 txt(e(r['title']),x,232,450,18,bold=True)
 txt('Rejected design / archived',x,199,450,12,bold=True,color=RED)
 txt('Historical source checks passed. No live-game acceptance is recorded. The published link is retained in the version register for reference only.',x,174,450,11,color=MUTED)
 txt('Row '+str(n)+' / '+e(r['version']),x,112,450,9.5,color=MUTED)
page_end()
# Complete row register. Published links are copied verbatim from the canonical sheet data.
for start in range(0,len(rows),register_rows_per_page):
 c.bookmarkPage('register'+str(start));c.addOutlineEntry('Version register '+str(start+1)+'-'+str(min(start+register_rows_per_page,len(rows))),'register'+str(start),0)
 txt('Complete Version Register',M,H-36,928,27,bold=True)
 txt(f'Records {start+1}-{min(start+register_rows_per_page,len(rows))} of {len(rows)}. IDs retain source history and the staged release queue; ordinals are not worksheet rows. All links here are archival; none is a current test recommendation.',M,H-83,928,11,color=MUTED)
 xs=[36,65,371,553,661,823];widths=[23,298,174,100,154,141]
 heads=['#','Tracked version ID','Version','Design','Source QA','Archived TMJ']
 for x,w,t in zip(xs,widths,heads):txt(t,x,618,w,9,bold=True)
 yy=590
 for r in rows[start:start+register_rows_per_page]:
  if (r['row']-start)%2:c.setFillColor(PALE);c.rect(M,yy-25,928,28,fill=1,stroke=0)
  values=[str(r['row']),r['id'],r['version'],('Pending' if len(str(r['decision']))>15 else r['decision']),qa(r)]
  for k,v in enumerate(values):txt(e(v),xs[k],yy,widths[k],8.5,leading=10.4,limit=25,color=status_color(r) if k==3 else INK)
  link=('<link href="'+e(r['tmj_url'])+'" color="#1C7062"><u>Archive only</u></link>') if r.get('tmj_url') else 'No verified current URL'
  if r['row'] in [9,10]:link+='<br/>Archive only'
  txt(link,xs[5],yy,widths[5],8.5,leading=10.4,limit=25,color=MUTED)
  yy-=28
 txt('All rows are retained for history. Current release status is shown on page 1. Source QA is not live acceptance; archived URLs must not be used for current testing.',M,54,928,9,color=MUTED)
 page_end()
# Later requests are explicit supplements, outside the 51-row baseline count.
if pack.get('supplement'):
 c.bookmarkPage('supplement');c.addOutlineEntry('Latest requested variants and concept','supplement',0)
 txt('Latest Requested Variants and Concept',M,H-36,928,27,bold=True)
 txt('09:15 UTC update. These additions sit outside the 51-row testing-sheet baseline. The two source-validated candidates remain unpublished and await design review. The separate visual concept is not a built map.',M,H-84,928,11,color=MUTED)
 for j,r in enumerate(pack['supplement']):
  x=M+j*316;image(r,x,337,296,242)
  y=txt(e(r['title']),x,321,296,16,bold=True)-12
  y=txt(e(r['status']),x,y,296,11,bold=True,color=TEAL if j==0 else GOLD)-10
  txt(e(r['caption']),x,y,296,11,limit=180,color=MUTED)
 txt('The retained six-mat mixed activity concept is a separate visual reference. Original versions remain available; every future release needs its own source and live-test status.',M,74,928,10,color=MUTED)
 page_end()
c.bookmarkPage('production-categories');c.addOutlineEntry('Production-entry context','production-categories',0)
txt('Categories / Observed and Proposed',M,H-36,928,26,bold=True)
txt('Planning facts copied from the staged workbook. Proposed names, descriptions and order are not deployed changes. Category UUIDs and icons are still blank.',M,H-84,928,11,color=MUTED)
for j,v in enumerate(pack['production_entry_snapshot']['Category entry']):
 row,col=divmod(j,2);x=M+col*474;y=H-144-row*174
 y=txt(e(v['Proposed name']),x,y,448,15,bold=True)-8
 y=txt('<b>Observed:</b> '+e(v.get('Observed name') or 'Not observed; proposed new category'),x,y,448,10)-5
 y=txt('<b>Planning key:</b> '+e(v['slug (verify existing key)'])+' / proposed order '+str(v['order']),x,y,448,10)-5
 y=txt(e(v['description']),x,y,448,10)-5
 txt(e(v['Evidence / status']),x,y,448,9,color=MUTED,limit=40)
page_end()
txt('Template and Map Entry Context',M,H-36,928,26,bold=True)
txt('Eight proposed template entries are retained. UUIDs are blank; categoryId must be the actual saved UUID. Template proposals remain private, inactive and not featured.',M,H-84,928,11,color=MUTED)
y=H-148
for j,v in enumerate(pack['production_entry_snapshot']['Template entry']):
 if j%2==0:c.setFillColor(PALE);c.rect(M,y-40,928,47,fill=1,stroke=0)
 txt(e(v['Proposed name']),M+8,y,220,12,bold=True)
 txt(e(v['slug'])+' / '+e(v['Planning category key']),M+238,y,240,10)
 txt(e(v['shortDescription']),M+498,y,425,10,limit=35)
 y-=53
txt('18 map-variant planning entries are preserved verbatim in the reproducible source snapshot and testing workbook. These are production-entry proposals, not extra verified runtimes or current test links.',M,125,928,11)
txt('Existing observed category names/counts remain separate from proposed copy. Slugs are documented but not runtime-verified; uniqueness must be checked before creation. No production entries were changed.',M,77,928,10,color=MUTED)
page_end()
c.save()
(D/'layout-log.json').write_text(json.dumps(log,indent=2))
# Exact PDF link whitelist check and page-text inventory check.
from pypdf import PdfReader
pdf=PdfReader(OUT);links=[]
for p in pdf.pages:
 for a in p.get('/Annots',[]):
  a=a.get_object();act=a.get('/A',{})
  if act.get('/URI'):links.append(act['/URI'])
allowed={r['tmj_url'] for r in rows if r.get('tmj_url')}
assert set(links)<=allowed,(set(links)-allowed)
full='\n'.join(p.extract_text() for p in pdf.pages)
assert all(r['id'] in full for r in rows)
assert len(rows)==len({r['id'] for r in rows})
(D/'build-validation.json').write_text(json.dumps({'page_count':len(pdf.pages),'tracked_versions':len(rows),'families':len(families),'all_ids_present':True,'published_links_whitelisted':True,'unique_published_urls':len(set(links)),'pdf_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'bytes':OUT.stat().st_size},indent=2))
print(json.dumps({'pdf':str(OUT),'pages':len(pdf.pages),'bytes':OUT.stat().st_size}))
