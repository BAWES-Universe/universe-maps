from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];d=json.load(open(R/'source/design.json'));rooms={}
def add(r,n,pts):r['visiblePaths'].append(dict(name=n,origins=pts))
for q in d['rooms']:rooms[q['id']]={'visiblePaths':[],'visibleFloor':[]}
a=rooms['courtyard']
for n,p in [
 ('Full central north-south main lane west edge',[[584,352],[584,784]]),('Full central north-south main lane east edge',[[680,352],[680,784]]),
 ('Main crossing upper width',[[240,592],[976,592]]),('Main crossing lower width',[[240,656],[976,656]]),
 ('North clear transverse lane',[[240,336],[528,336]]),('North clear transverse lane second width',[[240,368],[528,368]]),
 ('Northeast transverse lane',[[592,336],[976,336]]),('Northeast transverse lane second width',[[592,384],[976,384]]),
 ('Full cistern west bypass outer',[[208,384],[208,560]]),('Full cistern west bypass inner',[[240,384],[240,560]]),
 ('Full cistern east bypass outer',[[536,400],[536,576]]),('Full cistern east bypass inner',[[584,400],[584,576]]),
 ('South gate west width',[[584,784],[584,960]]),('South gate east width',[[680,784],[680,960]]),
 ('West guest threshold and 64-wide landing',[[344,288],[344,336],[408,336]]),('East guest threshold and 64-wide landing',[[912,288],[912,336],[976,336]]),('Roof room threshold approach',[[656,303],[656,352]]),
 ('West bench north approach',[[344,672],[344,719]]),('West bench return around east foot',[[408,704],[408,784],[344,784]]),
 ('East bench north approach',[[936,672],[936,719]]),('East bench south-clear floor strip',[[840,800],[1032,800]]),
 ('Packing bay vertical approach',[[1008,480],[1008,656]]),('Arrival apron upper wide lane',[[456,976],[904,976]]),('Arrival apron middle wide lane',[[456,1008],[936,1008]]),('Arrival apron lower wide lane',[[552,1088],[808,1088]]),('Arrival apron broad center west',[[584,944],[584,1088]]),('Arrival apron broad center east',[[712,944],[712,1088]])]:add(a,n,p)
for k,center,left,right in [('wind-cell',240,200,328),('landmark-cell',624,584,712),('roof-stair-room',1008,968,1064)]:
 r=rooms[k];oy=1248
 for n,p in [('Main aisle west width',[[left,528],[left,672]]),('Main aisle east width',[[right,528],[right,672]]),('Door approach center',[[center,640],[center,736]]),('South doorway west width',[[center-32,672],[center-32,736]]),('South doorway east width',[[center+32,672],[center+32,736]]),('Full center cross-room width',[[left,608],[right,608]])]:add(r,n,[[x,y+oy]for x,y in p])
for n,p in [('West guest full clear northern floor',[[176,496],[328,496]]),('West guest east aisle',[[368,512],[368,656]])]:add(rooms['wind-cell'],n,[[x,y+1248]for x,y in p])
for n,p in [('East guest full clear northern floor',[[560,496],[720,496]]),('East guest west aisle',[[536,528],[536,656]])]:add(rooms['landmark-cell'],n,[[x,y+1248]for x,y in p])
for n,p in [('Stair wide bottom landing north band',[[1008,608],[1160,608]]),('Stair wide bottom landing south band',[[1008,656],[1160,656]]),('Native stair west fitting body-origin extreme',[[1128,608],[1128,384]]),('Native stair east fitting body-origin extreme',[[1144,608],[1144,384]]),('Upper landing lateral fitting extent',[[1128,384],[1144,384]]),('Right room west aisle',[[872,528],[872,656]])]:add(rooms['roof-stair-room'],n,[[x,y+1248]for x,y in p])
# Floor click endpoints require tile+0..15 in y; body-width polylines above deliberately cover the full continuously clear floor separately.
for id,r in rooms.items():
 seen=set()
 for path in r['visiblePaths']:
  for x,y in path['origins']:
   y=min(y//32*32+15,y);x=min(x//32*32+24,max(x//32*32+8,x))
   if (x,y)not in seen:r['visibleFloor'].append(dict(name=path['name']+' exact-fit endpoint',origin=[x,y]));seen.add((x,y))
(R/'source/visible-floor.json').write_text(json.dumps({'scope':'Author art-selected full-width routes and incidental stair fit extrema. Continuous body clearance is distinct from native click fitting. Independent completeness review remains required.','rooms':rooms},indent=2)+'\n')
