"""Static route/asset checks only; does not launch Universe or move a Woka."""
import json
from collections import deque
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'campus.tmj').read_text()); layout=json.loads((root/'source/layout.json').read_text())
w,h=m['width'],m['height']; layers={x['name']:x for x in m['layers']}
assert m['orientation']=='orthogonal' and m['tilewidth']==m['tileheight']==32
assert all(len(l['data'])==w*h for l in m['layers'] if l['type']=='tilelayer')
assert [l['name'] for l in m['layers']].index('floorLayer') < [l['name'] for l in m['layers']].index('tower-glass-cover')
for t in m['tilesets']:
    with Image.open(root/t['image']) as im: assert im.size==(t['imagewidth'],t['imageheight'])
assert (root/'runtime.js').is_file()
assert not any(p['name'] in ('silent','playAudio','playAudioLoop','openWebsite','openTab') for p in m['properties'])
b=layers['persistent-collision']['data']
spawn=tuple(layout['spawn']); seen={spawn}; q=deque([spawn])
while q:
    x,y=q.popleft()
    for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
        a,c=p
        if 0<=a<w and 0<=c<h and not b[c*w+a] and p not in seen: seen.add(p);q.append(p)
assert len(seen)==sum(v==0 for v in b)
for p in layout['seats']:
    x,y=p
    assert (x,y) in seen and (x,y+1) in seen
# Every unobstructed cell beneath the complete shell is interior and connected.
for room in layout['buildings']:
    ix,iy,iw,ih=room['interior']
    for y in range(iy,iy+ih):
        for x in range(ix,ix+iw):
            assert layers[room['name']+'-interior']['data'][y*w+x]
            if not b[y*w+x]: assert (x,y) in seen
for portal in layout['portal_slots']:
    assert (portal['x']//32,portal['y']//32) in seen
    assert portal['properties']==[]
for key in ['entrance','rear_entrance']:
    x,y,ww,hh=layout[key]
    for xx in range(x,x+ww): assert (xx,y) in seen
for point in [(7,7),(37,7),(22,3),(50,20)]: assert point in seen
assert not layers['tower-interior']['data'][spawn[1]*w+spawn[0]]
assert sum(bool(v) for v in layers['start']['data'])==1
logic=next(t for t in m['tilesets'] if t['name']=='logic')
assert all(v != logic['firstgid'] for v in layers['tower-glass-cover']['data'])
result={'scope':'static cell connectivity and asset integrity only','walkable_cells':len(seen),'reachable_seats':len(layout['seats']),'entrance_width_px':192,'studenthub_reserve_connected':True,'runtime_coverage':'none in this static check; see separate actual-client evidence','visual_acceptance':'NOT REVIEWED'}
(root/'review/static-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
