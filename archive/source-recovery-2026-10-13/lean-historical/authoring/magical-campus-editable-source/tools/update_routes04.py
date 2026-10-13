from pathlib import Path
p=Path(__file__).resolve().parent/'plan_routes.py';s=p.read_text()
s=s.replace("marketgoals=[]", """# Coarser derivative preserves the exact four native bench destinations. Only two empty
# approach waypoints move8px to stay clear of the conservatively enlarged solid cells.
if T==16:
 for g in gardengoals:
  if g['id']=='firepit-bench-south':g['approach']={'x':2672,'y':2512}
  if g['id']=='firepit-bench-west':g['approach']={'x':2584,'y':2440}
marketgoals=[]""")
s=s.replace("byid['reception-visitor']", "byid['reception-visitor-1'],byid['reception-visitor-2'],byid['reception-visitor-3']")
s=s.replace("-workbench-south-1'", "-island-left-south'")
s=s.replace("spawn={'x':1504", """safe_paths={}
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
spawn={'x':1504""")
old="""  endpoint=g.get('approach',g['target']);p=(endpoint['x'],endpoint['y']);leg={'goal':g,**route(current,p)}
  if 'approach' in g:
   end=tuple(g['target'].values());contact=route(p,end);leg['contactApproachSweep']=contact;current=end
  else:current=p
  legs.append(leg)"""
new="""  prefix=[]
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
  previous_goal=g['id'];legs.append(leg)"""
assert old in s;s=s.replace(old,new)
s=s.replace("'scope':'Offline 1px native-body sweeps against exact compiled permanent 8px tiles. Actual Phaser runtime is separate.'", "'tileSize':T,'officeRevision':'04-social-reception','scope':f'Offline 1px native-body sweeps against compiled permanent {T}px tiles. Source-prescribed social routes preserved for teams and reception; actual Phaser runtime is separate.'")
p.write_text(s)
