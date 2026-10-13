from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'deliverables';D.mkdir(exist_ok=True)
# Ready-to-add release contains only the new family/version directory.
with zipfile.ZipFile(D/'Butterfly-Campus-v3-Git-ready-map.zip','w',zipfile.ZIP_DEFLATED,6) as z:
 for p in sorted((R/'repo-addition').rglob('*')):
  if p.is_file():z.write(p,p.relative_to(R/'repo-addition'))
 z.write(R/'docs/family-index-proposal.patch','review/family-index-proposal.patch')
 z.write(R/'docs/REVIEW-NOTES.md','review/REVIEW-NOTES.md')
# Complete source is independent of native engine files; vendor and compiled schema harness are included.
exclude_names={'prototype.py','assemble_proof.py','prototype-layout.json','refined-layout.json','landscape-alpha-proof.png','refined_prototype.py','parquet-original.png','room-shell-original.png','validate-engine.cjs'}
selected_evidence={'campus-overview-exterior.png','campus-overview-interiors.png','HQ-full-interior.png','event-hall.png','footprints.json','static-map-checks.json','native-contract-validation.json','native-validator-provenance.json','static-build-check.json'}
selected_qa={'browser-checks.json','runtime-tests.json','source-pin.json','static-map-checks.json','visible-water-pixels.json','final-depth-proof.json','final-hq-woka-2x.png','final-hq-behind-table.png','final-hq-front-table.png','final-campus-overview.png','full-physical-tour.json','final-tour-acceptance.json','final-captures.json','final-quick-acceptance.json','sales-fountain-regression.json','threshold-face-proof.json','transit-route-checks.json','complete-light-acceptance.json','video-delivery-summary.json','final-hq-native-review.png','final-portrait-hq.png','final-landscape-hq.png'}
raw=json.load(open(R/'map/butterfly-campus.tmj'));maprefs={'butterfly-campus.tmj'}|{t['image'] for t in raw['tilesets']}|{str(p.relative_to(R/'map')) for folder in ['scripts','audio'] for p in (R/'map'/folder).rglob('*') if p.is_file()}
paths=[]
for base in ['art-source','assets','docs','integration','tools','qa','map','evidence']:
 for p in sorted((R/base).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts or 'archive' in p.parts or p.name in exclude_names:continue
  rel=p.relative_to(R)
  if base=='art-source' and (p.name.startswith('landscape-crop-') or '-qa.' in p.name or p.name.endswith('-proof.png')):continue
  if base=='evidence' and p.name not in selected_evidence:continue
  if base=='qa' and 'results' in rel.parts and p.name not in selected_qa:continue
  if base=='map' and str(p.relative_to(R/'map')) not in maprefs:continue
  paths.append(p)
paths.extend([R/'README.md',R/'layout.json',R/'RELEASE.json',R/'RESUME-SCOPE.md',R/'requirements-build.txt'])
paths.extend(sorted((R/'interior-proposal-light/art-source').glob('*.png')))
with zipfile.ZipFile(D/'Butterfly-Campus-v3-source-review.zip','w',zipfile.ZIP_DEFLATED,6) as z:
 for p in paths:z.write(p,Path('Butterfly-Campus-v3')/p.relative_to(R))
for p in [D/'Butterfly-Campus-v3-Git-ready-map.zip',D/'Butterfly-Campus-v3-source-review.zip']:
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 print(json.dumps({'file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
