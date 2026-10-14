"""Continuous native-body routes checked against the actual compiled TMJ grid."""
from pathlib import Path
import json,heapq,functools
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--map-dir',default='map');args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/args.map_dir
grid=json.loads((OUT/'collision-grid.json').read_text());COLS,ROWS=grid['width'],grid['height'];T=grid['tileSize'];W,H=COLS*T,ROWS*T;blocked=set(grid['blockedIndices'])
@functools.lru_cache(maxsize=500000)
def clear(p,margin=0):
 x,y=p
 if x-8-margin<0 or y-margin<0 or x+8+margin>W or y+16+margin>H:return False
 return all(yy*COLS+xx not in blocked for yy in range((y-margin)//T,(y+15+margin)//T+1) for xx in range((x-8-margin)//T,(x+7+margin)//T+1))
def safe_neighbor(p,toward):
 if clear(p,1):return p
 opts=[]
 for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
  q=(p[0]+dx,p[1]+dy)
  if clear(q,1) and all(clear((p[0]+dx*k//4,p[1]+dy*k//4)) for k in range(5)):opts.append(q)
 if not opts:raise ValueError(f'No 1px-clear neighbor for {p}')
 return min(opts,key=lambda q:abs(q[0]-toward[0])+abs(q[1]-toward[1]))
def route(start,end,clearance=1):
 if not clear(start) or not clear(end):raise ValueError(f'Blocked endpoint {start}->{end}; start={clear(start)} end={clear(end)}')
 origstart,origend=start,end
 if clearance:
  try:start,end=safe_neighbor(start,end),safe_neighbor(end,start)
  except ValueError:return route(origstart,origend,0)
 front=[(0,0,start)];best={start:0};came={}
 while front:
  _,cost,p=heapq.heappop(front)
  if cost!=best[p]:continue
  if p==end:
   path=[p]
   while p!=start:p=came[p];path.append(p)
   path.reverse()
   if origstart!=start:path.insert(0,origstart)
   if origend!=end:path.append(origend)
   compressed=[path[0]]
   for i in range(1,len(path)-1):
    a,b,c=path[i-1:i+2]
    if (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]):compressed.append(b)
   if len(path)>1:compressed.append(origend)
   n=0
   for a,b in zip(compressed,compressed[1:]):
    steps=abs(a[0]-b[0])+abs(a[1]-b[1])
    for k in range(steps+1):
     q=(a[0]+(b[0]-a[0])*k//max(1,steps),a[1]+(b[1]-a[1])*k//max(1,steps))
     if not clear(q):raise AssertionError(f'Body intersects real compiled cell at {q}')
     n+=1
   return {'points':[{'x':x,'y':y} for x,y in compressed],'length':sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(compressed,compressed[1:])),'bodySweepSamples':n,'travelClearancePixels':clearance,'endpointClearancePixels':0}
  for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
   q=(p[0]+dx,p[1]+dy)
   if clear(q,clearance) and cost+4<best.get(q,10**12):best[q]=cost+4;came[q]=p;heapq.heappush(front,(cost+4+abs(q[0]-end[0])+abs(q[1]-end[1]),cost+4,q))
 if clearance:return route(origstart,origend,0)
 raise ValueError(f'No route {start}->{end}')
def goal(ident,x,y,**kw):return {'id':ident,'name':ident.replace('-',' '),'target':{'x':x,'y':y},'kind':'place',**kw}
office=json.loads((ROOT/'sources/office/checkpoint-manifest-full-canvas.json').read_text())['goals'];officegoals=[]
for g in office:
 if g['kind']=='checkpoint':continue
 k=goal(g['id'],g['x']+480,g['y']+288,facing={'south':'down','north':'up','west':'left','east':'right'}.get(g.get('facing')),source='office')
 if g.get('approach'):k['approach']={'x':g['approach']['x']+480,'y':g['approach']['y']+288}
 if g.get('contactDirection'):k['contactDirection']=g['contactDirection']
 officegoals.append(k)
civic=json.loads((ROOT/'sources/civic/module.json').read_text());civicgoals=[]
for g in civic['students']+civic['audience']+[civic['teacher'],civic['speaker']]:civicgoals.append(goal(g['id'],g['center'][0],g['center'][1]+1792,facing='up' if g.get('frame')==10 else 'down',source='civic'))
garden=json.loads((ROOT/'sources/garden/native-manifest.json').read_text());gardengoals=[]
for g in garden['spots']:gardengoals.append(goal('firepit-bench-'+g['id'],g['position']['x']+2176,g['position']['y']+1920,facing=g['facing'],approach={'x':g['approach']['x']+2176,'y':g['approach']['y']+1920},source='garden'))
# Coarser derivative preserves the exact four native bench destinations. Only two empty
# approach waypoints move8px to stay clear of the conservatively enlarged solid cells.
if T==16:
 for g in gardengoals:
  if g['id']=='firepit-bench-south':g['approach']={'x':2672,'y':2512}
  if g['id']=='firepit-bench-west':g['approach']={'x':2584,'y':2440}
marketgoals=[]
marketpath=ROOT/'sources/market/module.json'
if marketpath.exists():
 market=json.loads(marketpath.read_text())
 for m in market['stalls']:marketgoals.append(goal('market-'+m['id'],m['customerAnchor'][0]+512,m['customerAnchor'][1],facing='up',source='market'))
allgoals=officegoals+civicgoals+gardengoals+marketgoals
byid={g['id']:g for g in allgoals}
main=[goal('fountain-south-view',1192,2216),byid['reception-visitor-1'],byid['reception-visitor-2'],byid['reception-visitor-3']]
for team in ['operations','recruitment','sales','tech','research','marketing','design-media']:main.append(byid[f'studenthub-{team}-island-left-south'])
main += [byid[x] for x in ['meeting-a-south-place','meeting-b-south-place','conference-south-place-2','student-2','teacher','student-5','speaker','attendee-8','attendee-23']]
main +=gardengoals+marketgoals+[goal('return-to-fountain',1192,2216),goal('return-to-arrival',1504,2912)]
safe_paths={}
for r in json.loads((ROOT/'sources/office/social-egress-route-manifest-full-canvas.json').read_text())['routes']:
 safe_paths[r['targetStationId']]=[(p['x']+480,p['y']+288) for p in r['fullEntranceRoute']]
for r in json.loads((ROOT/'sources/office/reception-social-route-manifest.json').read_text())['routes']:
 safe_paths[r['targetStationId']]=[(p['x']+512,p['y']+320) for p in r['points']]
def fixed_route(points):
 n=0;length=0
 for a,b in zip(points,points[1:]):
  steps=abs(a[0]-b[0])+abs(a[1]-b[1]);length+=steps
  for k in range(steps+1):
   q=(a[0]+(b[0]-a[0])*k//max(1,steps),a[1]+(b[1]-a[1])*k//max(1,steps))
   assert clear(q),f'Source social route touches compiled solid at {q}'
   n+=1
 return {'points':[{'x':x,'y':y} for x,y in points],'length':length,'bodySweepSamples':n,'sourceSocialRoute':True}
previous_goal=None
spawn={'x':1504,'y':2912};current=tuple(spawn.values());legs=[];failures=[]
for g in main:
 try:
  prefix=[]
  if previous_goal in safe_paths:prefix=safe_paths[previous_goal];current=prefix[-1]
  if g['id'] in safe_paths:
   entering=list(reversed(safe_paths[g['id']]));join=route(current,entering[0]);pts=prefix+[tuple(p.values()) for p in join['points']]+entering
   leg={'goal':g,**fixed_route(pts)};current=entering[-1]
  else:
   endpoint=g.get('approach',g['target']);p=(endpoint['x'],endpoint['y']);travel=route(current,p)
   leg={'goal':g,**fixed_route(prefix+[tuple(p.values()) for p in travel['points']])}
   if 'approach' in g:
    end=tuple(g['target'].values());contact=route(p,end);leg['contactApproachSweep']=contact;current=end
   else:current=p
  leg['sourceSocialRoute']=g['id'] in safe_paths or previous_goal in safe_paths
  previous_goal=g['id'];legs.append(leg)
 except (ValueError,AssertionError) as e:failures.append({'goal':g['id'],'error':str(e)})
# Every authored destination must be collision-clear and connected to main campus.
allchecks=[]
for g in allgoals:
 p=tuple(g['target'].values())
 try:r=route((1504,2216),p);allchecks.append({'id':g['id'],'pass':True,'routeLength':r['length'],'bodySweepSamples':r['bodySweepSamples']})
 except (ValueError,AssertionError) as e:allchecks.append({'id':g['id'],'pass':False,'error':str(e)})
result={'status':'pass' if not failures and all(x['pass'] for x in allchecks) else 'blocked','spawn':spawn,'legs':legs,'failures':failures,'allDestinationChecks':allchecks,'allGoals':allgoals,'bodySweepSamples':sum(l['bodySweepSamples']+l.get('contactApproachSweep',{}).get('bodySweepSamples',0) for l in legs),'length':sum(l['length']+l.get('contactApproachSweep',{}).get('length',0) for l in legs),'tileSize':T,'officeRevision':'04-social-reception','scope':f'Offline 1px native-body sweeps against compiled permanent {T}px tiles. Source-prescribed social routes preserved for teams and reception; actual Phaser runtime is separate.'}
(OUT/'route-plan.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('legs','allGoals','allDestinationChecks')},indent=2));print('Destinations',len(allchecks),'failures',[x for x in allchecks if not x['pass']])
