from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'candidate';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=read(O/'map32/map.tmj');l=read(O/'source/layout.json');b=read(R/'baseline-r2/source/layout.json');w=read(O/'map32/map.wam');s=read(O/'STATIC-CHECKS.json');anim=read(O/'WATER-ANIMATION-CHECKS.json');art=read(R/'source-assets/ART-GEOMETRY-ACCEPTANCE.json')
assert (m['width'],m['height'],m['tilewidth'],m['tileheight'])==(24,26,32,32)
assert l['collision'][:16]==b['collision'] and l['seats']==b['seats'] and l['spawn']==b['spawn']
assert s['all_open_cells_connected'] and s['head_intersections']==0 and s['new_garden_cells']==70 and s['body_clear_integer_positions']==114688
assert Image.open(O/'review/empty-native.png').crop((0,0,768,512)).tobytes()==Image.open(R/'source-assets/validated-interior-native.png').tobytes()
assert sha(R/'working/art-native.png')=='c4828fb823e3f6a4107fa6809b7de0a5b155b0c810eb0601ff0fb7e4f529e148'
assert anim['frames']==8 and all(v['atlas_exact'] and v['outside_water_mask']==0 and v['changed_water_pixels']>0 for v in anim['frames_decoded_from_actual_atlas'])
assert len(w['areas'])==3 and len({a['properties'][0]['roomName'] for a in w['areas']})==3
for i,seat in enumerate(l['seats']):
 expected=0 if i<4 else 1 if i<8 else 2
 for x,y in [seat['anchor'],seat['floorClick']]:assert [j for j,a in enumerate(w['areas']) if a['x']<x<a['x']+a['width'] and a['y']<y<a['y']+a['height']]==[expected]
for p in [O/'NATIVE-ROUTES.json',O/'source/SEAT-ROUTE-TRACES.json',O/'source/GARDEN-ROUTE-TRACES.json']:
 for f,h in read(p)['inputHashes'].items():assert sha(O/f)==h
assert read(O/'NATIVE-ALL-SPAWN-ROUTES.json')['allPass']
for row in read(O/'ACTUAL-ARRIVAL-CHECKS.json')['rows']:assert row['upper14_foreground_pixels']==0 and not row['auto_turn']
report={'source_static_native_checks':True,'frozen_evidence_bound':True,'art_hash_bound':True,'base_interior_exact':True,'three_unique_conversation_areas':True,'live_test':'Not run','map_sha256':sha(O/'map32/map.tmj'),'layout_sha256':sha(O/'source/layout.json')};(O/'RELEASE-CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
if (R/'EXPECTED-OUTPUTS.json').exists():
 rows=read(R/'EXPECTED-OUTPUTS.json')['files'];bad=[e['path'] for e in rows if not (R/e['path']).is_file() or sha(R/e['path'])!=e['sha256']];assert not bad,bad;print('All',len(rows),'frozen outputs rebuilt exactly.')
print('Garden source/static/native-evidence checks passed; live testing unclaimed.')
