"""Plan continuous 4px-anchor routes against actual compiled 16px TMJ collisions."""
from pathlib import Path
import json
import heapq

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'compiled-work'


def main():
    grid=json.loads((OUT/'collision-grid.json').read_text())
    geo=json.loads((OUT/'runtime-geometry.json').read_text())
    blocked=set(grid['blockedIndices']); cols,rows=grid['width'],grid['height']
    W,H=cols*16,rows*16
    def clear(p,margin=0):
        x,y=p
        if x-8-margin<0 or y-margin<0 or x+8+margin>W or y+16+margin>H:return False
        return all(yy*cols+xx not in blocked for yy in range((y-margin)//16,(y+15+margin)//16+1) for xx in range((x-8-margin)//16,(x+7+margin)//16+1))
    def safe_neighbor(p,toward):
        if clear(p,1):return p
        options=[]
        for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
            q=(p[0]+dx,p[1]+dy)
            if clear(q,1) and all(clear((p[0]+dx*k//4,p[1]+dy*k//4)) for k in range(5)):
                options.append(q)
        if not options:raise ValueError(f'No 1px-clear travel connector beside exact endpoint {p}')
        return min(options,key=lambda q:abs(q[0]-toward[0])+abs(q[1]-toward[1]))
    def route(start,end,clearance=1):
        if not clear(start) or not clear(end): raise ValueError(f'Blocked endpoint: {start} -> {end}; start clear={clear(start)}, end clear={clear(end)}')
        original_start,original_end=start,end
        if clearance:start,end=safe_neighbor(start,end),safe_neighbor(end,start)
        frontier=[(0,0,start)]; best={start:0}; came={}
        while frontier:
            _,cost,p=heapq.heappop(frontier)
            if cost!=best[p]:continue
            if p==end:
                path=[p]
                while p!=start:p=came[p];path.append(p)
                path.reverse()
                if original_start!=start:path.insert(0,original_start)
                if original_end!=end:path.append(original_end)
                compressed=[path[0]]
                for i in range(1,len(path)-1):
                    a,b,c=path[i-1:i+2]
                    if (b[0]-a[0],b[1]-a[1]) != (c[0]-b[0],c[1]-b[1]):compressed.append(b)
                if len(path)>1:compressed.append(original_end)
                # Sweeping the unchanged 16px body each pixel independently proves the compressed path.
                count=0
                for a,b in zip(compressed,compressed[1:]):
                    steps=abs(a[0]-b[0])+abs(a[1]-b[1])
                    for k in range(steps+1):
                        q=(a[0]+(b[0]-a[0])*k//max(1,steps),a[1]+(b[1]-a[1])*k//max(1,steps))
                        if not clear(q):raise AssertionError(f'Route sweep intersects real collision at {q}')
                        count+=1
                return {'points':[{'x':x,'y':y} for x,y in compressed], 'length':sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(compressed,compressed[1:])),
                        'bodySweepSamples':count,'travelClearancePixels':clearance,'endpointClearancePixels':0}
            for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
                q=(p[0]+dx,p[1]+dy)
                if clear(q,clearance) and cost+4<best.get(q,10**12):
                    best[q]=cost+4;came[q]=p
                    heapq.heappush(frontier,(cost+4+abs(q[0]-end[0])+abs(q[1]-end[1]),cost+4,q))
        if clearance:return route(original_start,original_end,0)
        raise ValueError(f'No collision-clear connection: {start} -> {end}')
    spawn=(geo['spawn']['x'],geo['spawn']['y']); goals=[]
    # Every bench is visited continuously, followed by the furnished gallery and foyer.
    for bench in geo['workbenches']:
        stations=[s for s in geo['stations'] if s['sharedWorkbenchId']==bench['id']]
        for station in stations:
            seat=station['seat']; direction=1 if seat['facing']=='south' else -1
            # Registered receiver cabinets may occupy the old 32px rear approach.
            # Use an authored contact anchor when supplied, otherwise choose the
            # longest actually-clear cardinal entry among native 8px anchor steps.
            approach=station.get('contactApproach')
            if approach is None:
                candidates=[{'x':seat['x'],'y':seat['y']-direction*d} for d in (32,24,16,8)]
                approach=next((p for p in candidates if clear((p['x'],p['y']))),None)
            if approach is None:
                raise ValueError(f'No physical cardinal contact approach exists for {station["id"]}; source geometry must resolve it')
            goals.append(dict(id=station['id'],name=station['name'],kind='workbench-seat',target={'x':seat['x'],'y':seat['y']},
                              approach=approach,pushDirection=direction,benchId=bench['id'],frameIndex=seat['frameIndex']))
    goals_file=ROOT/'runtime-work'/'shared-destinations.json'
    shared=json.loads(goals_file.read_text()) if goals_file.exists() else [
        {'id':'meeting-a','name':'Meeting A threshold','target':{'x':2192,'y':616}},
        {'id':'meeting-b','name':'Meeting B threshold','target':{'x':2192,'y':840}},
        {'id':'conference','name':'Conference threshold','target':{'x':2192,'y':1160}},
        {'id':'reception','name':'Reception approach','target':{'x':1136,'y':1280}},
        {'id':'lounge','name':'Lounge approach','target':{'x':432,'y':1328}}]
    if geo.get('goals'):
        shared=[{'id':p['id'],'name':p['id'].replace('-',' '),'target':{'x':p['x'],'y':p['y']},'facing':p.get('facing'),
                 'sourceKind':p['kind'],'contactDirection':p.get('contactDirection')} for p in geo['goals'] if p['kind'] not in ('team-seat','checkpoint')]
    goals.extend(dict(kind='shared-space',**x) for x in shared)
    current=spawn; legs=[]; failures=[]
    for goal in goals:
        destination=goal.get('approach',goal['target']); end=(destination['x'],destination['y'])
        try:
            leg=dict(goal=goal,**route(current,end))
            if goal['kind']=='workbench-seat':
                seat=goal['target']; p=(seat['x'],seat['y'])
                contact=route(end,p)
                leg['contactApproachSweep']=contact
                after=(p[0],p[1]+goal['pushDirection'])
                if clear(after):raise AssertionError(f'Seat does not contact exact table at {p}')
                leg['exactContactStop']=True
                current=p
            else:current=end
            legs.append(leg)
        except (ValueError,AssertionError) as error:
            failures.append({'goal':goal['id'],'error':str(error)})
    result=dict(status='pass' if not failures else 'blocked',sourceStatus=geo['status'],spawn=geo['spawn'],legs=legs,failures=failures,
                bodySweepSamples=sum(x['bodySweepSamples']+x.get('contactApproachSweep',{}).get('bodySweepSamples',0) for x in legs),
                scope='Offline route planning against the exact compiled TMJ collision cells; browser physics execution is separate.')
    (OUT/'route-plan.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='legs'},indent=2))


if __name__=='__main__':main()
