#!/usr/bin/env python3
"""New structural/grid tests, not native-engine or physical-body replay."""
import collections,hashlib,json,pathlib,re,struct
ROOT=pathlib.Path(__file__).resolve().parents[1];runtime=ROOT/'build/runtime'
def load(p):return json.loads(p.read_text())
m=load(runtime/'keepers-return.tmj');wam=load(runtime/'keepers-return.wam');a=load(ROOT/'source/anchors.json')['anchors'];checks=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
check('native32_dimensions',(m['width'],m['height'],m['tilewidth'],m['tileheight'])==(128,128,32,32))
check('wam_relative_map',wam['mapUrl']=='./keepers-return.tmj')
layers={l['name']:l for l in m['layers']};check('unique_layer_names',len(layers)==len(m['layers']))
check('unique_layer_ids',len({l['id'] for l in m['layers']})==len(m['layers']))
for l in m['layers']:
 if l['type']=='tilelayer':check('grid_size:'+l['name'],len(l['data'])==l['width']*l['height'])
for ts in m['tilesets']:
 p=runtime/ts['image'];check('texture_exists:'+ts['name'],p.is_file());data=p.read_bytes();check('png_dimensions:'+ts['name'],data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==(ts['imagewidth'],ts['imageheight']))
validgids={0}
for ts in m['tilesets']:validgids.update(range(ts['firstgid'],ts['firstgid']+ts['tilecount']))
for l in m['layers']:
 if l['type']=='tilelayer':check('valid_gids:'+l['name'],all((gid&0x0fffffff) in validgids for gid in l['data']))
collision=layers['collision-permanent']['data'];quiet=layers['silent-spawn-only']['data'];check('quiet_single_start_tile',sum(bool(v) for v in quiet)==1)
cell=lambda p:(int(p['x']//32),int(p['y']//32));open_cells={(i%128,i//128) for i,g in enumerate(collision) if not g};components={};component=0
for start in sorted(open_cells):
 if start in components:continue
 component+=1;queue=collections.deque([start]);components[start]=component
 while queue:
  x,y=queue.popleft()
  for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if n in open_cells and n not in components:components[n]=component;queue.append(n)
for name,anchor in a.items():
 check('anchor_open:'+name,cell(anchor) in open_cells)
 if 'to' in anchor:check('reciprocal_door:'+name,anchor['to'] in a and a[anchor['to']].get('to')==name)
popupnames={o['name'] for o in layers['inside-popups']['objects']};check('popup_for_every_anchor',all('inside-popup-'+n in popupnames for n in a))
groups={'exterior':['dock','houseDoor','towerDoor'],'house':['houseExit','chart','key','hearth'],'workshop':['towerExit','fuse','wheel','stairsUp'],'lantern':['stairsDown','telescope','lens','console']}
for label,names in groups.items():check('connected_grid:'+label,len({components[cell(a[n])] for n in names})==1)
check('four_distinct_spaces',len({components[cell(a[v[0]])] for v in groups.values()})==4)
for n in ['inside-house-key','inside-lens-focused','inside-workshop-power','inside-lantern-lit','inside-exterior-lit']:check('initial_state_hidden:'+n,layers[n]['visible'] is False)
check('only_spawn_quiet',all(not quiet[y*128+x] for n,p in a.items() if n!='dock' for x,y in [cell(p)]))
check('no_external_dependency',all('://' not in t['image'] for t in m['tilesets']) and all(p.get('value')=='keeper.js' for p in m['properties'] if p['name']=='script'))
result={'scope':'JSON, asset, anchor and point-grid connectivity only; not native body, live GPU or gameplay proof','passed':len(checks),'failed':0,'checks':checks,'open_grid_cells':len(open_cells),'grid_components':component,'portal_pairs':sum('to' in p for p in a.values())//2}
(ROOT/'evidence/structure.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['passed','failed','open_grid_cells','grid_components','portal_pairs']}))
