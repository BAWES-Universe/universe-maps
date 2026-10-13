from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'candidate';read=lambda p:json.loads(p.read_text());m=read(O/'map32/map.tmj');l=read(O/'source/layout.json');w=read(O/'map32/map.wam');static=read(O/'STATIC-CHECKS.json');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (m['width'],m['height'],m['tilewidth'],m['tileheight'])==(24,16,32,32)
assert static['all_open_cells_connected'] and static['head_intersections']==0 and all(a['clear'] and a['connected'] for a in static['anchor_checks'])
assert len(l['seats'])==10 and len(w['areas'])==3 and len({a['properties'][0]['roomName'] for a in w['areas']})==3
members=[]
for i,s in enumerate(l['seats']):
 expected=0 if i<4 else 1 if i<8 else 2
 for role,point in [('sprite',s['anchor']),('floorClick',s['floorClick'])]:
  x,y=point;found=[j for j,a in enumerate(w['areas']) if a['x']<x<a['x']+a['width'] and a['y']<y<a['y']+a['height']];assert found==[expected],(s,role,found);members.append({'seat':s['name'],'point':role,'conversation':w['areas'][expected]['name']})
orig=np.array(Image.open(R/'source-assets/original-approved-concept.png').convert('RGBA').resize((768,512),Image.Resampling.LANCZOS));art=np.array(Image.open(R/'working/art-native.png').convert('RGBA'));changed=np.any(orig!=art,axis=2);allowed=np.zeros((512,768),bool);bounds=[(56,128,171,234),(203,193,347,324),(420,192,568,324),(594,134,718,245)]
for x0,y0,x1,y1 in bounds:allowed[y0:y1,x0:x1]=True
outside=int((changed&~allowed).sum());assert outside==0,outside
pres={'approved_original_sha256':sha(R/'source-assets/original-approved-concept.png'),'runtime_uniform_scale':.5,'changed_native_pixels':int(changed.sum()),'allowed_native_repair_envelopes':bounds,'changed_pixels_outside_envelopes':outside,'original_immutable':True};(O/'SOURCE-PRESERVATION.json').write_text(json.dumps(pres,indent=2))
for n in ['frozen-seat-route-traces.json','frozen-spawn-seat-arrivals.json']:
 for f,h in read(R/'source-assets'/n)['inputHashes'].items():assert sha(O/f)==h,(f,'stale native evidence')
assert all(r['anchor_exact'] and r['upper14_foreground']==0 for r in read(O/'SEAT-DEPTH-CHECKS.json'))
report={'map_sha256':sha(O/'map32/map.tmj'),'layout_sha256':sha(O/'source/layout.json'),'tmj_wam_shape_checks':True,'unique_conversation_rooms':3,'all_20_endpoint_memberships_correct':True,'memberships':members,'outside_art_changes':outside,'native_evidence_binding':True,'live_testing':'Not run','runtime_functions':'Normal movement/facing only; no automatic sitting, snapping or turning'};(O/'RELEASE-CHECKS.json').write_text(json.dumps(report,indent=2))
expected=R/'EXPECTED-OUTPUTS.json'
if expected.exists():
 entries=read(expected)['files'];fail=[f['path'] for f in entries if not (R/f['path']).exists() or sha(R/f['path'])!=f['sha256']];assert not fail,fail
 print('All',len(entries),'frozen generated files rebuild exactly.')
print('Structural, endpoint, source-preservation and evidence-binding checks passed.')
